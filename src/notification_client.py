"""Notification API client."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from src.config import AppConfig
from src.event_handler import NotificationMessage


@dataclass(frozen=True)
class SendResult:
    """Result of one notification send attempt."""

    success: bool
    dry_run: bool
    status_code: int | None
    response_text: str
    payload: dict[str, Any]
    error: str | None = None


class NotificationClient:
    """Client for sending notification payloads to a webhook/API endpoint."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def send(self, notification: NotificationMessage) -> SendResult:
        """Send one notification message or simulate sending in dry-run mode."""
        payload = notification.to_payload()

        if self.config.dry_run:
            result = SendResult(
                success=True,
                dry_run=True,
                status_code=None,
                response_text="DRY_RUN: 未送出 HTTP request",
                payload=payload,
            )
            self._write_log(result)
            return result

        headers = {
            "Authorization": f"Bearer {self.config.notification_api_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.config.notification_api_url,
                json=payload,
                headers=headers,
                timeout=self.config.timeout_seconds,
            )
            response.raise_for_status()

            result = SendResult(
                success=True,
                dry_run=False,
                status_code=response.status_code,
                response_text=response.text[:500],
                payload=payload,
            )

        except requests.RequestException as error:
            response = getattr(error, "response", None)

            result = SendResult(
                success=False,
                dry_run=False,
                status_code=response.status_code if response is not None else None,
                response_text=response.text[:500] if response is not None else "",
                payload=payload,
                error=str(error),
            )

        self._write_log(result)
        return result

    def _write_log(self, result: SendResult) -> None:
        """Append a send result to JSONL log file."""
        log_path = Path(self.config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": result.success,
            "dry_run": result.dry_run,
            "status_code": result.status_code,
            "response_text": result.response_text,
            "payload": result.payload,
            "error": result.error,
        }

        with log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")