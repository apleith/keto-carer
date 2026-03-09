from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class GroceryItemCreate(BaseModel):
    name: str
    quantity: Optional[str] = None
    category: Optional[str] = None
    is_checked: bool = False
    notes: Optional[str] = None
    ingredient_id: Optional[int] = None


class GroceryItemRead(GroceryItemCreate):
    id: int
    grocery_list_id: int

    model_config = {"from_attributes": True}


class GroceryItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    category: Optional[str] = None
    is_checked: Optional[bool] = None
    notes: Optional[str] = None


class GroceryListCreate(BaseModel):
    user_id: int
    name: str = "Grocery List"
    week_start: Optional[datetime] = None
    items: list[GroceryItemCreate] = []


class GroceryListRead(BaseModel):
    id: int
    user_id: int
    name: str
    week_start: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    items: list[GroceryItemRead] = []

    model_config = {"from_attributes": True}
