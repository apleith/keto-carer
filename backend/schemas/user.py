from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    display_name: str
    is_admin: bool = False
    age: Optional[int] = None
    weight_lbs: Optional[float] = None
    height_inches: Optional[float] = None
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    daily_carb_goal_g: float = 20.0
    daily_protein_goal_g: float = 100.0
    daily_fat_goal_g: float = 150.0
    daily_calories_goal: float = 1800.0
    daily_water_goal_oz: float = 64.0
    ntfy_topic: Optional[str] = None
    notifications_enabled: bool = True
    notify_meal_reminder: bool = True
    notify_medication: bool = True
    notify_water: bool = True
    meal_reminder_times: Optional[str] = "08:00,12:00,18:00"
    simplified_ui: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    age: Optional[int] = None
    weight_lbs: Optional[float] = None
    height_inches: Optional[float] = None
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    daily_carb_goal_g: Optional[float] = None
    daily_protein_goal_g: Optional[float] = None
    daily_fat_goal_g: Optional[float] = None
    daily_calories_goal: Optional[float] = None
    daily_water_goal_oz: Optional[float] = None
    ntfy_topic: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    notify_meal_reminder: Optional[bool] = None
    notify_medication: Optional[bool] = None
    notify_water: Optional[bool] = None
    meal_reminder_times: Optional[str] = None
    simplified_ui: Optional[bool] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
