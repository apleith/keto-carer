"""
Nutrition lookup via USDA FoodData Central.
Falls back to Open Food Facts if USDA returns no results.
"""
import httpx
from typing import Optional

from core.config import settings

USDA_BASE = "https://api.nal.usda.gov/fdc/v1"
OFF_BASE = "https://world.openfoodfacts.org/api/v2"


class NutritionData:
    def __init__(
        self,
        name: str,
        fdc_id: Optional[str] = None,
        calories_per_100g: Optional[float] = None,
        carbs_per_100g: Optional[float] = None,
        net_carbs_per_100g: Optional[float] = None,
        protein_per_100g: Optional[float] = None,
        fat_per_100g: Optional[float] = None,
        fiber_per_100g: Optional[float] = None,
    ):
        self.name = name
        self.fdc_id = fdc_id
        self.calories_per_100g = calories_per_100g
        self.carbs_per_100g = carbs_per_100g
        self.net_carbs_per_100g = net_carbs_per_100g
        self.protein_per_100g = protein_per_100g
        self.fat_per_100g = fat_per_100g
        self.fiber_per_100g = fiber_per_100g


def _nutrient_value(nutrients: list[dict], nutrient_id: int) -> Optional[float]:
    for n in nutrients:
        if n.get("nutrientId") == nutrient_id or n.get("nutrient", {}).get("id") == nutrient_id:
            return n.get("value") or n.get("amount")
    return None


async def search_usda(query: str, limit: int = 5) -> list[NutritionData]:
    """Search USDA FoodData Central and return nutrition data."""
    params = {
        "query": query,
        "pageSize": limit,
        "api_key": settings.USDA_API_KEY,
        "dataType": "Foundation,SR Legacy,Branded",
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{USDA_BASE}/foods/search", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    results = []
    for food in data.get("foods", []):
        nutrients = food.get("foodNutrients", [])
        calories = _nutrient_value(nutrients, 1008)    # Energy
        carbs = _nutrient_value(nutrients, 1005)       # Carbohydrates
        fiber = _nutrient_value(nutrients, 1079)       # Fiber
        protein = _nutrient_value(nutrients, 1003)     # Protein
        fat = _nutrient_value(nutrients, 1004)         # Total fat
        net_carbs = None
        if carbs is not None and fiber is not None:
            net_carbs = max(0.0, carbs - fiber)

        results.append(
            NutritionData(
                name=food.get("description", query),
                fdc_id=str(food.get("fdcId")),
                calories_per_100g=calories,
                carbs_per_100g=carbs,
                net_carbs_per_100g=net_carbs,
                protein_per_100g=protein,
                fat_per_100g=fat,
                fiber_per_100g=fiber,
            )
        )
    return results


async def search_open_food_facts(query: str, limit: int = 5) -> list[NutritionData]:
    """Fallback search via Open Food Facts."""
    params = {"search_terms": query, "page_size": limit, "json": 1}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{OFF_BASE}/search", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    results = []
    for product in data.get("products", []):
        n = product.get("nutriments", {})
        carbs = n.get("carbohydrates_100g")
        fiber = n.get("fiber_100g")
        net_carbs = None
        if carbs is not None and fiber is not None:
            net_carbs = max(0.0, carbs - fiber)

        results.append(
            NutritionData(
                name=product.get("product_name", query),
                calories_per_100g=n.get("energy-kcal_100g"),
                carbs_per_100g=carbs,
                net_carbs_per_100g=net_carbs,
                protein_per_100g=n.get("proteins_100g"),
                fat_per_100g=n.get("fat_100g"),
                fiber_per_100g=fiber,
            )
        )
    return results


async def search_food(query: str, limit: int = 5) -> list[NutritionData]:
    """Search USDA first; fall back to Open Food Facts if empty."""
    results = await search_usda(query, limit)
    if not results:
        results = await search_open_food_facts(query, limit)
    return results
