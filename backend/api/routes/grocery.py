from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.grocery import GroceryItem, GroceryList
from schemas.grocery import (
    GroceryItemUpdate, GroceryListCreate, GroceryListRead,
)

router = APIRouter(prefix="/grocery", tags=["grocery"])


@router.get("/", response_model=list[GroceryListRead])
async def list_grocery_lists(user_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GroceryList)
        .where(GroceryList.user_id == user_id)
        .options(selectinload(GroceryList.items))
        .order_by(GroceryList.created_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=GroceryListRead, status_code=201)
async def create_grocery_list(payload: GroceryListCreate, db: AsyncSession = Depends(get_db)):
    grocery_list = GroceryList(**payload.model_dump(exclude={"items"}))
    db.add(grocery_list)
    await db.flush()

    for item_data in (payload.items or []):
        item = GroceryItem(grocery_list_id=grocery_list.id, **item_data.model_dump())
        db.add(item)

    await db.flush()
    await db.refresh(grocery_list)
    return grocery_list


@router.get("/{list_id}", response_model=GroceryListRead)
async def get_grocery_list(list_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GroceryList)
        .where(GroceryList.id == list_id)
        .options(selectinload(GroceryList.items))
    )
    gl = result.scalar_one_or_none()
    if not gl:
        raise HTTPException(404, "Grocery list not found")
    return gl


@router.patch("/items/{item_id}", status_code=200)
async def update_grocery_item(
    item_id: int, payload: GroceryItemUpdate, db: AsyncSession = Depends(get_db)
):
    item = await db.get(GroceryItem, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.flush()
    return {"ok": True}


@router.delete("/{list_id}", status_code=204)
async def delete_grocery_list(list_id: int, db: AsyncSession = Depends(get_db)):
    gl = await db.get(GroceryList, list_id)
    if not gl:
        raise HTTPException(404, "Grocery list not found")
    await db.delete(gl)
