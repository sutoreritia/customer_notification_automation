"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for notification delivery."""

    notification_api_url: str
    notification_api_token: str
    timeout_seconds: float
    dry_run: bool
    log_file: Path


def _to_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config(force_send: bool = False) -> AppConfig:
    """Load configuration from .env and process environment."""
    load_dotenv(BASE_DIR / ".env")
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    dry_run = _to_bool(os.getenv("NOTIFICATION_DRY_RUN"), default=True)
    if force_send:
        dry_run = False

    return AppConfig(
        notification_api_url=os.getenv(
            "NOTIFICATION_API_URL",
            "https://jsonplaceholder.typicode.com/posts",
        ),
        notification_api_token=os.getenv("NOTIFICATION_API_TOKEN", "demo_token"),
        timeout_seconds=float(os.getenv("NOTIFICATION_TIMEOUT_SECONDS", "10")),
        dry_run=dry_run,
        log_file=LOG_DIR / "notification_log.jsonl",
    )
