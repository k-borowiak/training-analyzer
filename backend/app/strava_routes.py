from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from .db import get_db
from .deps import get_current_user
from .models import User
from .strava_service import strava_get

router = APIRouter(prefix="/api/strava", tags=["strava"])


@router.get("/athlete")
def get_athlete(user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    """
    Pobiera profil zalogowanego usera ze Stravy.
    """
    return strava_get(db, user.id, "/athlete")


@router.get("/activities")
def get_activities(
    per_page: int = 30,
    page: int = 1,
    user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db),
):
    """
    Pobiera listę aktywności ze Stravy. - ---->> domyślne 30 będzie do zmiany <<----
    """
    return strava_get(db, user.id, "/athlete/activities", params={"per_page": per_page, "page": page})