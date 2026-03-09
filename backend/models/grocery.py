from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class GroceryList(Base):
    __tablename__ = "grocery_lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), default="Grocery List")
    week_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="grocery_lists")
    items: Mapped[list["GroceryItem"]] = relationship(
        back_populates="grocery_list", cascade="all, delete-orphan"
    )


class GroceryItem(Base):
    __tablename__ = "grocery_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grocery_list_id: Mapped[int] = mapped_column(
        ForeignKey("grocery_lists.id"), nullable=False, index=True
    )
    ingredient_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ingredients.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g. "2 lbs"
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    # Relationships
    grocery_list: Mapped["GroceryList"] = relationship(back_populates="items")
