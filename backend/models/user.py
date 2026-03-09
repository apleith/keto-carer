from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Profile
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight_lbs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    height_inches: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    activity_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Daily macro targets
    daily_carb_goal_g: Mapped[float] = mapped_column(Float, default=20.0)
    daily_protein_goal_g: Mapped[float] = mapped_column(Float, default=100.0)
    daily_fat_goal_g: Mapped[float] = mapped_column(Float, default=150.0)
    daily_calories_goal: Mapped[float] = mapped_column(Float, default=1800.0)
    daily_water_goal_oz: Mapped[float] = mapped_column(Float, default=64.0)

    # Notification settings
    ntfy_topic: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_meal_reminder: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_medication: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_water: Mapped[bool] = mapped_column(Boolean, default=True)
    meal_reminder_times: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, default="08:00,12:00,18:00"
    )  # comma-separated HH:MM

    # Preferences
    simplified_ui: Mapped[bool] = mapped_column(Boolean, default=False)  # for Person B

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    ingredient_ratings: Mapped[list["UserIngredientRating"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    meal_logs: Mapped[list["MealLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    medications: Mapped[list["Medication"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    water_logs: Mapped[list["WaterLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    progress_entries: Mapped[list["ProgressEntry"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    lab_results: Mapped[list["LabResult"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    grocery_lists: Mapped[list["GroceryList"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
