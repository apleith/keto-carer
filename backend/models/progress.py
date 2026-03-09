from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class ProgressEntry(Base):
    """A body measurement / weight snapshot for a user."""

    __tablename__ = "progress_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    weight_lbs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    waist_inches: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hips_inches: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    chest_inches: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    neck_inches: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bmi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    body_fat_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ketone_level: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # mmol/L
    blood_glucose: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # mg/dL

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="progress_entries")


class LabResult(Base):
    """An uploaded or manually-entered lab result for a user."""

    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    lab_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="manual")  # manual | pdf
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Structured values (common labs)
    hba1c: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fasting_glucose: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_cholesterol: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ldl: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hdl: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    triglycerides: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    creatinine: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    egfr: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Raw extracted text from PDF (for AI analysis)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # AI-generated interpretation
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="lab_results")
