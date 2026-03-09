from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MedicationCreate(BaseModel):
    user_id: int
    name: str
    type: str = "supplement"
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    reminder_times: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True
    keto_notes: Optional[str] = None


class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    reminder_times: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    keto_notes: Optional[str] = None


class MedicationRead(MedicationCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MedicationLogCreate(BaseModel):
    medication_id: int
    dosage_taken: Optional[str] = None
    notes: Optional[str] = None


class MedicationLogRead(MedicationLogCreate):
    id: int
    taken_at: datetime

    model_config = {"from_attributes": True}
