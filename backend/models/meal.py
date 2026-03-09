from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Meal(Base):
    """A named, reusable meal recipe."""

    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meal_type: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # breakfast | lunch | dinner | snack
    servings: Mapped[int] = mapped_column(Integer, default=1)
    prep_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Computed totals (per serving)
    total_calories: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_carbs_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_net_carbs_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_protein_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_fat_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # AI-generated flag
    ai_generated: Mapped[bool] = mapped_column(Integer, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    ingredients: Mapped[list["MealIngredient"]] = relationship(
        back_populates="meal", cascade="all, delete-orphan"
    )
    logs: Mapped[list["MealLog"]] = relationship(
        back_populates="meal"
    )


class MealIngredient(Base):
    """Junction: ingredient in a meal with quantity."""

    __tablename__ = "meal_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), nullable=False, index=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), nullable=False, index=True
    )
    quantity_g: Mapped[float] = mapped_column(Float, nullable=False)  # grams
    notes: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relationships
    meal: Mapped["Meal"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="meal_ingredients")


class MealLog(Base):
    """A logged meal entry for a user on a specific date/time."""

    __tablename__ = "meal_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    meal_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("meals.id"), nullable=True, index=True
    )  # nullable for freeform logs

    # Freeform log (no linked meal)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    meal_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    servings_consumed: Mapped[float] = mapped_column(Float, default=1.0)

    # Macros at time of log (denormalized for history accuracy)
    calories: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    carbs_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    net_carbs_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    protein_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fat_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="meal_logs")
    meal: Mapped[Optional["Meal"]] = relationship(back_populates="logs")
