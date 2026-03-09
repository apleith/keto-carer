from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WaterLogCreate(BaseModel):
    user_id: int
    amount_oz: float
    notes: Optional[str] = None


class WaterLogRead(WaterLogCreate):
    id: int
    logged_at: datetime

    model_config = {"from_attributes": True}
