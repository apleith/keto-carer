"""
Weekly background research pull.
Called by APScheduler — fetches AI summaries on key keto topics
and stores them in the ResearchEntry table.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal
from models.research import ResearchEntry
from services.ai_service import research_summary
from services.notification_service import notify_research_ready

RESEARCH_TOPICS = [
    "ketogenic diet latest research",
    "keto diet and electrolyte management",
    "keto diet medication interactions",
    "ketogenic diet and cardiovascular health",
    "keto diet supplements evidence",
]


async def run_research_pull() -> None:
    """Fetch research summaries and persist them. Called by scheduler."""
    async with AsyncSessionLocal() as db:
        for topic in RESEARCH_TOPICS:
            try:
                summary = await research_summary(topic)
                entry = ResearchEntry(topic=topic, summary=summary)
                db.add(entry)
            except Exception as e:
                print(f"[research] Failed to fetch topic '{topic}': {e}")

        await db.commit()

    # Notify all users with ntfy enabled
    await _notify_users()


async def _notify_users() -> None:
    from models.user import User
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.notifications_enabled.is_(True), User.ntfy_topic.isnot(None))
        )
        users = result.scalars().all()
        for user in users:
            await notify_research_ready(user.ntfy_topic)
