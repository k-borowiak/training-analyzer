from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    strava_athlete_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    strava_token = relationship("StravaToken", back_populates="user", uselist=False)
    sessions = relationship("Session", back_populates="user")