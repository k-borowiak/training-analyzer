from fastapi import APIRouter, Depends
from ...dependencies.auth import get_current_user
from ...models import User

router = APIRouter(prefix="/me", tags=["me"])

@router.get("")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "stravaAthleteId": user.strava_athlete_id}