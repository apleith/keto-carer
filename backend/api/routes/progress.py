import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings, BASE_DIR
from core.database import get_db
from models.progress import LabResult, ProgressEntry
from schemas.progress import (
    LabResultRead, ProgressEntryCreate, ProgressEntryRead
)
from services.ai_service import interpret_lab_results
from services.pdf_service import extract_text

router = APIRouter(prefix="/progress", tags=["progress"])

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# --- Progress entries ---

@router.get("/", response_model=list[ProgressEntryRead])
async def list_progress(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProgressEntry)
        .where(ProgressEntry.user_id == user_id)
        .order_by(ProgressEntry.recorded_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=ProgressEntryRead, status_code=201)
async def create_progress(payload: ProgressEntryCreate, db: AsyncSession = Depends(get_db)):
    entry = ProgressEntry(**payload.model_dump())
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    return entry


# --- Lab results ---

@router.get("/labs/", response_model=list[LabResultRead])
async def list_labs(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LabResult)
        .where(LabResult.user_id == user_id)
        .order_by(LabResult.lab_date.desc())
    )
    return result.scalars().all()


@router.post("/labs/upload/", response_model=LabResultRead, status_code=201)
async def upload_lab_pdf(
    user_id: int = Form(...),
    notes: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a lab result PDF — extracts text and runs AI interpretation."""
    file_path = UPLOAD_DIR / f"user{user_id}_{file.filename}"
    content = await file.read()
    file_path.write_bytes(content)

    raw_text = extract_text(file_path)
    ai_summary = await interpret_lab_results(raw_text)

    lab = LabResult(
        user_id=user_id,
        source="pdf",
        file_path=str(file_path),
        raw_text=raw_text,
        ai_summary=ai_summary,
        notes=notes,
    )
    db.add(lab)
    await db.flush()
    await db.refresh(lab)
    return lab


@router.post("/labs/manual/", response_model=LabResultRead, status_code=201)
async def create_lab_manual(
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    lab = LabResult(**payload, source="manual")
    db.add(lab)
    await db.flush()
    await db.refresh(lab)
    return lab
