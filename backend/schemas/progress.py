from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProgressEntryCreate(BaseModel):
    user_id: int
    weight_lbs: Optional[float] = None
    waist_inches: Optional[float] = None
    hips_inches: Optional[float] = None
    chest_inches: Optional[float] = None
    neck_inches: Optional[float] = None
    bmi: Optional[float] = None
    body_fat_pct: Optional[float] = None
    ketone_level: Optional[float] = None
    blood_glucose: Optional[float] = None
    notes: Optional[str] = None


class ProgressEntryRead(ProgressEntryCreate):
    id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


class LabResultRead(BaseModel):
    id: int
    user_id: int
    recorded_at: datetime
    lab_date: Optional[datetime] = None
    source: str
    file_path: Optional[str] = None
    hba1c: Optional[float] = None
    fasting_glucose: Optional[float] = None
    total_cholesterol: Optional[float] = None
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    creatinine: Optional[float] = None
    egfr: Optional[float] = None
    raw_text: Optional[str] = None
    ai_summary: Optional[str] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
