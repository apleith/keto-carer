from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.meal import Meal, MealLog
from schemas.meal import MealCreate, MealRead, MealLogCreate, MealLogRead

router = APIRouter(prefix="/meals", tags=["meals"])


# --- Meals (recipes) ---

@router.get("/", response_model=list[MealRead])
async def list_meals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Meal).options(selectinload(Meal.ingredients)))
    return result.scalars().all()


@router.post("/", response_model=MealRead, status_code=201)
async def create_meal(payload: MealCreate, db: AsyncSession = Depends(get_db)):
    meal = Meal(**payload.model_dump(exclude={"ingredients"}))
    db.add(meal)
    await db.flush()
    await db.refresh(meal)
    return meal


@router.get("/{meal_id}", response_model=MealRead)
async def get_meal(meal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Meal).where(Meal.id == meal_id).options(selectinload(Meal.ingredients))
    )
    meal = result.scalar_one_or_none()
    if not meal:
        raise HTTPException(404, "Meal not found")
    return meal


@router.delete("/{meal_id}", status_code=204)
async def delete_meal(meal_id: int, db: AsyncSession = Depends(get_db)):
    meal = await db.get(Meal, meal_id)
    if not meal:
        raise HTTPException(404, "Meal not found")
    await db.delete(meal)


# --- Meal logs ---

@router.get("/logs/", response_model=list[MealLogRead])
async def list_meal_logs(
    user_id: int = Query(...),
    day: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    filters = [MealLog.user_id == user_id]
    if day:
        from sqlalchemy import func, cast
        import sqlalchemy as sa
        filters.append(sa.cast(MealLog.logged_at, sa.Date) == day)
    result = await db.execute(select(MealLog).where(and_(*filters)))
    return result.scalars().all()


@router.post("/logs/", response_model=MealLogRead, status_code=201)
async def log_meal(payload: MealLogCreate, db: AsyncSession = Depends(get_db)):
    log = MealLog(**payload.model_dump())
    db.add(log)
    await db.flush()
    await db.refresh(log)
    return log


@router.delete("/logs/{log_id}", status_code=204)
async def delete_meal_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log = await db.get(MealLog, log_id)
    if not log:
        raise HTTPException(404, "Log not found")
    await db.delete(log)
