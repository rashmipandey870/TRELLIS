"""TRELLIS Application Configuration & Environment Settings."""

from pathlib import Path

from pydantic import model_validator
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

    @property
    def ENVIRONMENT(self) -> str:
        return self.TRELLIS_ENV

    @ENVIRONMENT.setter
    def ENVIRONMENT(self, val: str) -> None:
        self.TRELLIS_ENV = val

    # Database Configuration (Defaults to shared Neon Serverless PostgreSQL Cloud Database)
    DATABASE_URL: str = (
        "postgresql+psycopg2://neondb_owner:REDACTED_PASSWORD@ep-weathered-base-az6lrn9p.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )
    DATABASE_MIGRATION_URL: str = (
        "postgresql+psycopg2://neondb_owner:REDACTED_PASSWORD@ep-weathered-base-az6lrn9p.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )

    # Redis Cache & Message Broker
    REDIS_URL: str = "redis://127.0.0.1:6379/0"

    # Security & Asymmetric JWT
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY_PATH: str = "secrets/jwt_private.pem"
    JWT_PUBLIC_KEY_PATH: str = "secrets/jwt_public.pem"
    JWT_KEY_ROTATION_DIR: str = "secrets/rotated_keys"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Field-level Encryption (AES-256 / Fernet key for sensitive columns e.g. totp_secret at rest)
    FIELD_ENCRYPTION_KEY: str = "gAAAAABnhX-dummy-fernet-key-32bytes-base64-dev-only="
    LEDGER_SALT_KEY: str = "trellis-ledger-pseudonym-salt-2026"
    SECRET_KEY: str = "trellis-secret-key-salt-2026"

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

    # Code Execution Runner Configuration ("judge0", "docker", or dev-only "local")
    CODE_RUNNER: str = "local"
    JUDGE0_URL: str = "http://localhost:2358"
    JUDGE0_API_KEY: str = ""

    # Meeting Allowed Hostnames (configurable allow-list)
    MEETING_ALLOWLIST_HOSTS: list[str] = [
        "teams.microsoft.com",
        "meet.google.com",
        "zoom.us",
        "csm.tech",
    ]

    # AI Practice, Role Assistant & Analytics Engine Configuration
    AI_PROVIDER: str = "auto"  # "auto", "ollama", "local", "anthropic", "openai", "smart_template"
    AI_MODEL_ID: str = "qwen2.5-coder:7b"
    AI_REQUEST_TIMEOUT_SECONDS: int = 45
    AI_API_KEY: str = ""
    AI_BASE_URL: str = "https://api.anthropic.com"
    AI_LOCAL_URL: str = "http://localhost:11434"

    @model_validator(mode="after")
    def validate_production_invariants(self) -> "Settings":
        """Strictly refuse startup in non-dev environments if secrets or keys are missing."""
        if self.TRELLIS_ENV != "dev":
            if not self.DATABASE_URL:
                raise RuntimeError(
                    "FATAL: DATABASE_URL must be provided via environment variables in non-dev environment."
                )
            if not self.DATABASE_MIGRATION_URL:
                raise RuntimeError(
                    "FATAL: DATABASE_MIGRATION_URL must be provided via environment variables in non-dev environment."
                )
            priv = Path(self.JWT_PRIVATE_KEY_PATH)
            pub = Path(self.JWT_PUBLIC_KEY_PATH)
            if not priv.exists() or not pub.exists():
                raise RuntimeError(
                    f"FATAL: Production JWT signing keys missing ({self.JWT_PRIVATE_KEY_PATH}, {self.JWT_PUBLIC_KEY_PATH}). "
                    "Ephemeral development keys are strictly forbidden outside TRELLIS_ENV=dev."
                )
            if not self.FIELD_ENCRYPTION_KEY or "dev-only" in self.FIELD_ENCRYPTION_KEY:
                raise RuntimeError(
                    "FATAL: FIELD_ENCRYPTION_KEY must be provided as a secure production key in non-dev environment."
                )
            if self.CODE_RUNNER not in {"judge0", "docker"}:
                raise RuntimeError(
                    f"FATAL: In production (TRELLIS_ENV={self.TRELLIS_ENV}), CODE_RUNNER must be 'judge0' or 'docker', "
                    f"got '{self.CODE_RUNNER}'. Local subprocess execution is strictly forbidden outside dev."
                )
        return self


settings = Settings()
