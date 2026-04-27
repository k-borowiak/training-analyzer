from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    strava_athlete_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    strava_token = relationship("StravaToken", back_populates="user", uselist=False)
    sessions = relationship("Session", back_populates="user")


class StravaToken(Base):
    __tablename__ = "strava_tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    access_token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)

    # Strava daje expires_at jako epoch seconds (int)
    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)

    scope: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="strava_token")


class Session(Base):
    __tablename__ = "sessions"

    # losowy token sesji, w cookie jako session_id
    id: Mapped[str] = mapped_column(String(64), primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")