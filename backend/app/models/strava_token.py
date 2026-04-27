from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db.base import Base

class StravaToken(Base):
    __tablename__ = "strava_tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    access_token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)  # epoch seconds
    scope: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="strava_token")