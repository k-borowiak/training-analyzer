import secrets
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session as DbSession

from .config import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    STRAVA_REDIRECT_URI,
    STRAVA_SCOPE,
    APP_REDIRECT_AFTER_LOGIN,
    COOKIE_SECURE,
)
from .db import get_db
from .models import User, StravaToken, Session as UserSession


router = APIRouter(prefix="/auth/strava", tags=["auth"])


@router.get("/login")
def strava_login():
    """
    1) Tworzy 'state'
    2) Przekierowuje na Strava authorize
    """
    if not STRAVA_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Missing STRAVA_CLIENT_ID")

    state = secrets.token_urlsafe(32)

    url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&approval_prompt=auto"
        f"&scope={STRAVA_SCOPE}"
        f"&state={state}"
    )

    resp = RedirectResponse(url=url, status_code=302)
    resp.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=10 * 60,  # 10 minut
    )
    return resp


@router.get("/callback")
def strava_callback(
    request: Request,
    code: str,
    state: str | None = None,
    db: DbSession = Depends(get_db),
):
    """
    Strava wraca tu z ?code=...&state=...
    
    1) sprawdzam state
    2) wymieniam code -> tokeny
    3) find-or-create user
    4) zapis tokenów
    5) tworzy sesję i cookie session_id
    """

    # 1) sprawdź state
    cookie_state = request.cookies.get("oauth_state")
    if not state or not cookie_state or state != cookie_state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    # 2) code -> tokeny
    token_data = exchange_code_for_token(code)

    athlete = token_data.get("athlete") or {}
    athlete_id = athlete.get("id")
    if not athlete_id:
        raise HTTPException(status_code=400, detail="Missing athlete id from Strava")

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    expires_at = token_data["expires_at"]
    scope = token_data.get("scope")

    # 3) find-or-create user
    user = db.query(User).filter(User.strava_athlete_id == athlete_id).one_or_none()
    if not user:
        user = User(strava_athlete_id=athlete_id)
        db.add(user)
        db.flush()  # dostajemy user.id bez commita

    # 4) upsert tokenów
    st = db.query(StravaToken).filter(StravaToken.user_id == user.id).one_or_none()
    if not st:
        st = StravaToken(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            scope=scope,
        )
        db.add(st)
    else:
        st.access_token = access_token
        st.refresh_token = refresh_token
        st.expires_at = expires_at
        st.scope = scope

    # 5) utwórz sesję
    session_id = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(days=30)

    sess = UserSession(
        id=session_id,
        user_id=user.id,
        expires_at=expires,
    )
    db.add(sess)

    db.commit()

    # 6) cookie i redirect
    resp = RedirectResponse(url=APP_REDIRECT_AFTER_LOGIN, status_code=302)
    resp.delete_cookie("oauth_state")
    resp.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=30 * 24 * 3600,
    )
    return resp


@router.post("/logout")
def logout(request: Request, db: DbSession = Depends(get_db)):
    """
    Wylogowanie = usuń sesję z DB + usuń cookie
    """
    sid = request.cookies.get("session_id")
    if sid:
        db.query(UserSession).filter(UserSession.id == sid).delete()
        db.commit()

    resp = RedirectResponse(url="/", status_code=302)
    resp.delete_cookie("session_id")
    return resp


def exchange_code_for_token(code: str) -> dict:
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Missing STRAVA_CLIENT_ID/SECRET")

    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }

    with httpx.Client(timeout=15) as client:
        r = client.post(url, data=payload)
        if r.status_code >= 400:
            raise HTTPException(status_code=400, detail=f"Strava token exchange failed: {r.text}")
        return r.json()