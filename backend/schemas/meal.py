from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MealIngredientCreate(BaseModel):
    ingredient_id: int
    quantity_g: float
    notes: Optional[str] = None


class MealIngredientRead(MealIngredientCreate):
    id: int
    model_config = {"from_attributes": True}


class MealCreate(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    meal_type: Optional[str] = None
    servings: int = 1
    prep_time_minutes: Optional[int] = None
    total_calories: Optional[float] = None
    total_carbs_g: Optional[float] = None
    total_net_carbs_g: Optional[float] = None
    total_protein_g: Optional[float] = None
    total_fat_g: Optional[float] = None
    ai_generated: bool = False
    ingredients: list[MealIngredientCreate] = []


class MealRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    meal_type: Optional[str] = None
    servings: int
    prep_time_minutes: Optional[int] = None
    total_calories: Optional[float] = None
    total_carbs_g: Optional[float] = None
    total_net_carbs_g: Optional[float] = None
    total_protein_g: Optional[float] = None
    total_fat_g: Optional[float] = None
    ai_generated: bool
    created_at: datetime
    ingredients: list[MealIngredientRead] = []

    model_config = {"from_attributes": True}


class MealLogCreate(BaseModel):
    user_id: int
    meal_id: Optional[int] = None
    description: Optional[str] = None
    meal_type: Optional[str] = None
    servings_consumed: float = 1.0
    calories: Optional[float] = None
    carbs_g: Optional[float] = None
    net_carbs_g: Optional[float] = None
    protein_g: Optional[float] = None
    fat_g: Optional[float] = None
    notes: Optional[str] = None


class MealLogRead(MealLogCreate):
    id: int
    logged_at: datetime

    model_config = {"from_attributes": True}
