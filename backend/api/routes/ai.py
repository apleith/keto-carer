"""AI endpoints — meal suggestions, lab interpretation, Ollama model management."""
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from models.ingredient import UserIngredientRating
from models.user import User
from services.ai_service import chat, meal_suggestions

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    messages: list[dict]
    temperature: float = 0.7
    max_tokens: int = 1024


@router.post("/chat")
async def ai_chat(payload: ChatRequest):
    response = await chat(payload.messages, payload.temperature, payload.max_tokens)
    return {"response": response, "provider": settings.AI_PROVIDER}


@router.get("/meal-suggestions")
async def get_meal_suggestions(
    user_id: int = Query(...),
    meal_type: str = Query("any"),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Get top-rated ingredients for this user
    result = await db.execute(
        select(UserIngredientRating)
        .where(UserIngredientRating.user_id == user_id)
        .order_by(UserIngredientRating.rating.desc())
        .limit(10)
    )
    ratings = result.scalars().all()

    top_ingredients: list[str] = []
    if ratings:
        from sqlalchemy.orm import selectinload
        from models.ingredient import Ingredient
        ids = [r.ingredient_id for r in ratings]
        ing_result = await db.execute(
            select(Ingredient).where(Ingredient.id.in_(ids))
        )
        top_ingredients = [i.name for i in ing_result.scalars().all()]

    suggestions = await meal_suggestions(
        user_name=user.display_name,
        top_ingredients=top_ingredients,
        daily_carb_goal=user.daily_carb_goal_g,
        meal_type=meal_type,
    )
    return {"suggestions": suggestions, "provider": settings.AI_PROVIDER}


# --- Ollama model management ---

@router.get("/ollama/models")
async def list_ollama_models():
    """List models installed in local Ollama."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise HTTPException(503, f"Ollama not reachable: {e}")


@router.post("/ollama/pull")
async def pull_ollama_model(model: str = Query(...)):
    """Trigger an Ollama model pull (streaming — runs in background)."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/pull",
                json={"name": model, "stream": False},
                timeout=300,
            )
            resp.raise_for_status()
            return {"ok": True, "model": model}
    except Exception as e:
        raise HTTPException(503, f"Pull failed: {e}")


@router.get("/provider")
async def get_provider():
    return {"provider": settings.AI_PROVIDER, "ollama_model": settings.OLLAMA_MODEL}
