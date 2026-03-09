from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.config import settings

scheduler = AsyncIOScheduler(timezone="UTC")


def setup_scheduler() -> None:
    """Register all background jobs."""
    from services.research_service import run_research_pull

    scheduler.add_job(
        run_research_pull,
        trigger=IntervalTrigger(days=settings.RESEARCH_INTERVAL_DAYS),
        id="research_pull",
        replace_existing=True,
        name="Weekly keto research pull",
    )
