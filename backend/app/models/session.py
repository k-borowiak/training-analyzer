from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")