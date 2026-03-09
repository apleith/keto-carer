from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class ResearchEntry(Base):
    """A research summary pulled by the weekly background job."""

    __tablename__ = "research_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    topic: Mapped[str] = mapped_column(String(200), nullable=False)  # e.g. "keto diet", "electrolytes"
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    ai_recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # comma-separated
