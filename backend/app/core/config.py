"""TRELLIS Application Configuration & Environment Settings."""

import base64
import os
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_REPO_DIR = _BASE_DIR.parent


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=(
            str(_BASE_DIR / ".env"),
            str(_REPO_DIR / ".env"),
            ".env",
        ),
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

    # Database Configuration (Environment-driven, clean non-owner credentials)
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://trellis_app:trellis_app_pass@localhost:5432/trellis_db",
    )
    DATABASE_MIGRATION_URL: str = os.environ.get(
        "DATABASE_MIGRATION_URL",
        "postgresql+psycopg2://trellis_migrator:trellis_migrator_pass@localhost:5432/trellis_db",
    )
    # Read-only connection string for demo sessions ensuring no destructive operations
    DEMO_READONLY_DATABASE_URL: str | None = os.environ.get("DEMO_READONLY_DATABASE_URL", None)

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
    FIELD_ENCRYPTION_KEY: str = ""
    LEDGER_SALT_KEY: str = ""
    SECRET_KEY: str = ""

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

    # SMTP / MailHog Service Configuration (Phase 3.1)
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = False
    EMAILS_FROM_EMAIL: str = "notifications@csmtech.internal"
    EMAILS_FROM_NAME: str = "CSM TRELLIS Platform"

    # Demo Convenience Configuration (Phase A3 - enabled in dev by default)
    DEMO_MODE: bool = True
    DEMO_ACCOUNTS_JSON: str = ""

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
            if not self.LEDGER_SALT_KEY:
                raise RuntimeError(
                    "FATAL: LEDGER_SALT_KEY must be provided via environment variables in non-dev environment."
                )
            if not self.SECRET_KEY:
                raise RuntimeError(
                    "FATAL: SECRET_KEY must be provided via environment variables in non-dev environment."
                )
        else:
            # Ephemeral keys & demo database defaults for local development
            import secrets as _secrets
            if not self.DATABASE_URL:
                repo_db = Path(__file__).resolve().parent.parent.parent.parent / "trellis_demo.db"
                backend_db = Path(__file__).resolve().parent.parent.parent / "trellis_demo.db"
                resolved_db = repo_db if repo_db.exists() else backend_db
                self.DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{resolved_db.as_posix()}")
            if not self.DATABASE_MIGRATION_URL:
                self.DATABASE_MIGRATION_URL = self.DATABASE_URL
            if not self.FIELD_ENCRYPTION_KEY:
                self.FIELD_ENCRYPTION_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode()
            if not self.LEDGER_SALT_KEY:
                self.LEDGER_SALT_KEY = _secrets.token_hex(16)
            if not self.SECRET_KEY:
                self.SECRET_KEY = _secrets.token_hex(32)
        return self


settings = Settings()
