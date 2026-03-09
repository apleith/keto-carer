from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    usda_fdc_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    brand: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Macros per 100g
    calories_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    carbs_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    net_carbs_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    protein_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fat_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fiber_per_100g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Category for filtering
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user_ratings: Mapped[list["UserIngredientRating"]] = relationship(
        back_populates="ingredient", cascade="all, delete-orphan"
    )
    meal_ingredients: Mapped[list["MealIngredient"]] = relationship(
        back_populates="ingredient"
    )


class UserIngredientRating(Base):
    """Per-user 1–10 rating for how well an ingredient fits their keto lifestyle."""

    __tablename__ = "user_ingredient_ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), nullable=False, index=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–10
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="ingredient_ratings")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="user_ratings")
