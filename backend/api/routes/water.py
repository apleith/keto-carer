from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_, cast, Date, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.water import WaterLog
from schemas.water import WaterLogCreate, WaterLogRead

router = APIRouter(prefix="/water", tags=["water"])


@router.get("/", response_model=list[WaterLogRead])
async def list_water_logs(
    user_id: int = Query(...),
    day: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    filters = [WaterLog.user_id == user_id]
    if day:
        import sqlalchemy as sa
        filters.append(sa.cast(WaterLog.logged_at, sa.Date) == day)
    result = await db.execute(select(WaterLog).where(and_(*filters)))
    return result.scalars().all()


@router.get("/today-total")
async def today_total(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    import sqlalchemy as sa
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).date()
    result = await db.execute(
        select(func.sum(WaterLog.amount_oz)).where(
            WaterLog.user_id == user_id,
            sa.cast(WaterLog.logged_at, sa.Date) == today,
        )
    )
    total = result.scalar() or 0.0
    return {"total_oz": total, "date": str(today)}


@router.post("/", response_model=WaterLogRead, status_code=201)
async def log_water(payload: WaterLogCreate, db: AsyncSession = Depends(get_db)):
    log = WaterLog(**payload.model_dump())
    db.add(log)
    await db.flush()
    await db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=204)
async def delete_water_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log = await db.get(WaterLog, log_id)
    if not log:
        raise HTTPException(404, "Log not found")
    await db.delete(log)
