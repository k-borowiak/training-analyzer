import time
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session as DbSession

from ..core.config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
from ..models import StravaToken

STRAVA_OAUTH_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def _refresh_tokens(refresh_token: str) -> dict:
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Missing STRAVA_CLIENT_ID/SECRET")

    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    with httpx.Client(timeout=15) as client:
        r = client.post(STRAVA_OAUTH_TOKEN_URL, data=payload)
        if r.status_code >= 400:
            raise HTTPException(status_code=400, detail=f"Strava refresh failed: {r.text}")
        return r.json()

def get_valid_access_token(db: DbSession, user_id: int) -> str:
    st = db.query(StravaToken).filter(StravaToken.user_id == user_id).one_or_none()
    if not st:
        raise HTTPException(status_code=400, detail="User has no Strava tokens")

    now = int(time.time())
    if st.expires_at > now + 60:
        return st.access_token

    data = _refresh_tokens(st.refresh_token)
    st.access_token = data["access_token"]
    st.refresh_token = data["refresh_token"]
    st.expires_at = data["expires_at"]
    st.scope = data.get("scope", st.scope)
    db.commit()
    return st.access_token

def strava_get(db: DbSession, user_id: int, path: str, params: dict | None = None) -> dict:
    token = get_valid_access_token(db, user_id)
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{STRAVA_API_BASE}{path}"

    with httpx.Client(timeout=20) as client:
        r = client.get(url, headers=headers, params=params)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=f"Strava API error: {r.text}")
        return r.json()