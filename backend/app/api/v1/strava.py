from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from ...core.db.session import get_db
from ...dependencies.auth import get_current_user
from ...models import User
from ...services.strava import strava_get

router = APIRouter(prefix="/strava", tags=["strava"])

@router.get("/athlete")
def athlete(user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    return strava_get(db, user.id, "/athlete")

@router.get("/activities")
def activities(per_page: int = 30, page: int = 1, user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    return strava_get(db, user.id, "/athlete/activities", params={"per_page": per_page, "page": page})