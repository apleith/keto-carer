from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import init_db
from core.scheduler import scheduler, setup_scheduler

from api.routes import (
    users, meals, nutrition, medications, water, progress, grocery, ai, notifications
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    setup_scheduler()
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown(wait=False)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(meals.router, prefix="/api/v1")
app.include_router(nutrition.router, prefix="/api/v1")
app.include_router(medications.router, prefix="/api/v1")
app.include_router(water.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")
app.include_router(grocery.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION, "ai_provider": settings.AI_PROVIDER}
