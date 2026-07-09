"""Webhook event validation and notification message building."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

WebhookEvent = dict[str, Any]


@dataclass(frozen=True)
class NotificationMessage:
    """Notification payload prepared from a webhook event."""

    event_id: str
    event_type: str
    title: str
    target_channel: str
    message: str
    priority: str
    data: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        """Convert the notification message to a JSON-friendly payload."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "target_channel": self.target_channel,
            "title": self.title,
            "message": self.message,
            "priority": self.priority,
            "data": self.data,
        }


def validate_event(event: WebhookEvent) -> None:
    """Validate the minimum shape of a webhook event."""
    required_keys = ["event_id", "event_type", "created_at", "data"]
    missing = [key for key in required_keys if key not in event]

    if missing:
        raise ValueError(f"Webhook event 缺少必要欄位: {missing}")

    if not isinstance(event["data"], dict):
        raise ValueError("Webhook event 的 data 必須是 dict。")


def build_notification_message(event: WebhookEvent) -> NotificationMessage | None:
    """Build a notification message from one webhook event."""
    validate_event(event)

    event_type = event["event_type"]
    data = event["data"]

    builders = {
        "customer.created": _build_customer_created,
        "customer.high_value": _build_customer_high_value,
        "complaint.created": _build_complaint_created,
        "order.cancelled": _build_order_cancelled,
        "report.ready": _build_report_ready,
    }

    builder = builders.get(event_type)

    if builder is None:
        return None

    return builder(event, data)


def _build_customer_created(
    event: WebhookEvent,
    data: dict[str, Any],
) -> NotificationMessage:
    customer_name = data.get("customer_name", "未命名客戶")
    city = data.get("city", "未提供城市")

    return NotificationMessage(
        event_id=event["event_id"],
        event_type=event["event_type"],
        target_channel="sales",
        title="新增客戶通知",
        message=f"新增客戶 {customer_name}，城市：{city}，請業務完成首次關懷。",
        priority="normal",
        data=data,
    )


def _build_customer_high_value(
    event: WebhookEvent,
    data: dict[str, Any],
) -> NotificationMessage:
    customer_name = data.get("customer_name", "未命名客戶")
    total_spent = data.get("total_spent", 0)

    return NotificationMessage(
        event_id=event["event_id"],
        event_type=event["event_type"],
        target_channel="sales_manager",
        title="高價值客戶通知",
        message=f"{customer_name} 已成為高價值客戶，累積消費 {total_spent} 元，建議安排專人經營。",
        priority="high",
        data=data,
    )


def _build_complaint_created(
    event: WebhookEvent,
    data: dict[str, Any],
) -> NotificationMessage:
    customer_name = data.get("customer_name", "未命名客戶")
    ticket_id = data.get("ticket_id", "未提供單號")
    complaint_message = data.get("message", "未提供內容")
    priority = data.get("priority", "high")

    return NotificationMessage(
        event_id=event["event_id"],
        event_type=event["event_type"],
        target_channel="customer_service",
        title="客訴案件通知",
        message=f"客戶 {customer_name} 建立客訴案件 {ticket_id}：{complaint_message}",
        priority=priority,
        data=data,
    )


def _build_order_cancelled(
    event: WebhookEvent,
    data: dict[str, Any],
) -> NotificationMessage:
    order_id = data.get("order_id", "未知訂單")
    customer_name = data.get("customer_name", "未命名客戶")
    amount = data.get("amount", 0)
    reason = data.get("reason", "未提供原因")

    return NotificationMessage(
        event_id=event["event_id"],
        event_type=event["event_type"],
        target_channel="customer_service",
        title="訂單取消通知",
        message=f"訂單 {order_id} 已取消，客戶 {customer_name}，金額 {amount} 元，原因：{reason}",
        priority="normal",
        data=data,
    )


def _build_report_ready(
    event: WebhookEvent,
    data: dict[str, Any],
) -> NotificationMessage:
    report_name = data.get("report_name", "未命名報表")
    report_url = data.get("report_url", "未提供連結")

    return NotificationMessage(
        event_id=event["event_id"],
        event_type=event["event_type"],
        target_channel="management",
        title="營運報表完成通知",
        message=f"{report_name} 已產生完成，請至 {report_url} 查看。",
        priority="normal",
        data=data,
    )