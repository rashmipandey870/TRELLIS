"""TRELLIS Application Configuration & Environment Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Project Metadata
    PROJECT_NAME: str = "TRELLIS"
    TAGLINE: str = "Where every Tendril climbs"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    TRELLIS_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    # Database Configuration
    DATABASE_URL: str = (
        "mysql+asyncmy://trellis_app:trellis_app_secret_2026@127.0.0.1:3306/trellis_db"
    )
    DATABASE_MIGRATION_URL: str = (
        "mysql+asyncmy://trellis_migrator:trellis_migrator_secret_2026@127.0.0.1:3306/trellis_db"
    )

    # Redis Cache & Message Broker
    REDIS_URL: str = "redis://127.0.0.1:6379/0"

    # Security & Asymmetric JWT
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY_PATH: str = "secrets/jwt_private.pem"
    JWT_PUBLIC_KEY_PATH: str = "secrets/jwt_public.pem"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Argon2id Parameters
    ARGON2_TIME_COST: int = 3
    ARGON2_MEMORY_COST: int = 65536
    ARGON2_PARALLELISM: int = 4

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:8000",
    ]


settings = Settings()
