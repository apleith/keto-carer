from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "keto-carer"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/keto-carer.db"

    # AI Provider: "claude" | "ollama"
    AI_PROVIDER: str = "ollama"
    ANTHROPIC_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # USDA FoodData Central
    USDA_API_KEY: str = "DEMO_KEY"

    # ntfy.sh
    NTFY_BASE_URL: str = "https://ntfy.sh"

    # Research scheduler (days between pulls)
    RESEARCH_INTERVAL_DAYS: int = 7

    # CORS origins (LAN access)
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()
