from datetime import datetime
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session as DbSession

from .db import get_db
from .models import Session as UserSession, User


def get_current_user(request: Request, db: DbSession = Depends(get_db)) -> User:
    sid = request.cookies.get("session_id")
    if not sid:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sess = db.query(UserSession).filter(UserSession.id == sid).one_or_none()
    if not sess:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Naive UTC  (pasuje do DateTime bez timezone)
    if sess.expires_at < datetime.utcnow():
        db.delete(sess)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == sess.user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user