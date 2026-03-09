from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.medication import Medication, MedicationLog
from schemas.medication import (
    MedicationCreate, MedicationRead, MedicationUpdate,
    MedicationLogCreate, MedicationLogRead,
)

router = APIRouter(prefix="/medications", tags=["medications"])


@router.get("/", response_model=list[MedicationRead])
async def list_medications(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medication).where(Medication.user_id == user_id))
    return result.scalars().all()


@router.post("/", response_model=MedicationRead, status_code=201)
async def create_medication(payload: MedicationCreate, db: AsyncSession = Depends(get_db)):
    med = Medication(**payload.model_dump())
    db.add(med)
    await db.flush()
    await db.refresh(med)
    return med


@router.patch("/{med_id}", response_model=MedicationRead)
async def update_medication(
    med_id: int, payload: MedicationUpdate, db: AsyncSession = Depends(get_db)
):
    med = await db.get(Medication, med_id)
    if not med:
        raise HTTPException(404, "Medication not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(med, field, value)
    await db.flush()
    await db.refresh(med)
    return med


@router.delete("/{med_id}", status_code=204)
async def delete_medication(med_id: int, db: AsyncSession = Depends(get_db)):
    med = await db.get(Medication, med_id)
    if not med:
        raise HTTPException(404, "Medication not found")
    await db.delete(med)


@router.post("/logs/", response_model=MedicationLogRead, status_code=201)
async def log_medication(payload: MedicationLogCreate, db: AsyncSession = Depends(get_db)):
    log = MedicationLog(**payload.model_dump())
    db.add(log)
    await db.flush()
    await db.refresh(log)
    return log


@router.get("/logs/", response_model=list[MedicationLogRead])
async def list_medication_logs(
    medication_id: int = Query(...), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MedicationLog).where(MedicationLog.medication_id == medication_id)
    )
    return result.scalars().all()
