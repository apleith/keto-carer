from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class WaterLog(Base):
    """A water intake log entry for a user."""

    __tablename__ = "water_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    amount_oz: Mapped[float] = mapped_column(Float, nullable=False)
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notes: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="water_logs")
