from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Medication(Base):
    """A medication or supplement tracked for a user."""

    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), default="supplement")  # medication | supplement
    dosage: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g. "500mg"
    frequency: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # e.g. "twice daily"
    reminder_times: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )  # comma-separated HH:MM
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Keto interaction notes (AI-populated)
    keto_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="medications")
    logs: Mapped[list["MedicationLog"]] = relationship(
        back_populates="medication", cascade="all, delete-orphan"
    )


class MedicationLog(Base):
    """A record of taking a medication/supplement."""

    __tablename__ = "medication_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    medication_id: Mapped[int] = mapped_column(
        ForeignKey("medications.id"), nullable=False, index=True
    )
    taken_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    dosage_taken: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    medication: Mapped["Medication"] = relationship(back_populates="logs")
