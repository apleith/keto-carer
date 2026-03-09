from fastapi import APIRouter, Query
from services.nutrition_service import search_food, NutritionData

router = APIRouter(prefix="/nutrition", tags=["nutrition"])


@router.get("/search")
async def search_nutrition(q: str = Query(..., min_length=2), limit: int = Query(5, le=20)):
    results = await search_food(q, limit)
    return [
        {
            "name": r.name,
            "fdc_id": r.fdc_id,
            "calories_per_100g": r.calories_per_100g,
            "carbs_per_100g": r.carbs_per_100g,
            "net_carbs_per_100g": r.net_carbs_per_100g,
            "protein_per_100g": r.protein_per_100g,
            "fat_per_100g": r.fat_per_100g,
            "fiber_per_100g": r.fiber_per_100g,
        }
        for r in results
    ]
