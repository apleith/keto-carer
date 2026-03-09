"""
Notification service via ntfy.sh.
Server POSTs outbound to ntfy.sh — no inbound access needed.
Phone installs ntfy app and subscribes to the user's topic.
"""
import httpx
from core.config import settings


async def send(
    topic: str,
    title: str,
    message: str,
    priority: str = "default",
    tags: list[str] | None = None,
) -> bool:
    """Send a push notification to a ntfy topic. Returns True on success."""
    if not topic:
        return False
    url = f"{settings.NTFY_BASE_URL}/{topic}"
    headers = {
        "Title": title,
        "Priority": priority,
    }
    if tags:
        headers["Tags"] = ",".join(tags)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=message, headers=headers, timeout=10)
            return resp.status_code == 200
    except Exception:
        return False


async def notify_meal_reminder(topic: str, user_name: str) -> bool:
    return await send(
        topic=topic,
        title="Time to log your meal!",
        message=f"Hey {user_name}, don't forget to log what you ate. Staying on track!",
        tags=["fork_and_knife"],
    )


async def notify_medication(topic: str, user_name: str, med_name: str) -> bool:
    return await send(
        topic=topic,
        title=f"Medication reminder: {med_name}",
        message=f"Time to take your {med_name}, {user_name}.",
        tags=["pill"],
        priority="high",
    )


async def notify_water(topic: str, user_name: str, current_oz: float, goal_oz: float) -> bool:
    remaining = max(0, goal_oz - current_oz)
    return await send(
        topic=topic,
        title="Stay hydrated!",
        message=f"{user_name}, you've had {current_oz:.0f} oz today. {remaining:.0f} oz to go!",
        tags=["droplet"],
    )


async def notify_research_ready(topic: str) -> bool:
    return await send(
        topic=topic,
        title="New keto research available",
        message="Your weekly research update is ready. Check the app for the latest findings.",
        tags=["books"],
    )
