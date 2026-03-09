from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user import User
from services.notification_service import send

router = APIRouter(prefix="/notifications", tags=["notifications"])


class TestNotificationRequest(BaseModel):
    user_id: int
    message: str = "Test notification from keto-carer!"


@router.post("/test")
async def test_notification(payload: TestNotificationRequest, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if not user.ntfy_topic:
        raise HTTPException(400, "User has no ntfy topic configured")

    success = await send(
        topic=user.ntfy_topic,
        title="keto-carer test",
        message=payload.message,
        tags=["white_check_mark"],
    )
    return {"sent": success, "topic": user.ntfy_topic}
