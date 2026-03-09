from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(**payload.model_dump())
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.flush()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    await db.delete(user)
