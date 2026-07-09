"""Run the customer notification automation workflow."""

from __future__ import annotations

import argparse
from typing import Iterable

from src.config import load_config
from src.event_handler import build_notification_message
from src.event_samples import WebhookEvent, get_sample_event, get_sample_events
from src.notification_client import NotificationClient, SendResult


def process_events(
    events: Iterable[WebhookEvent],
    force_send: bool = False,
) -> list[SendResult]:
    """Process webhook events and send mapped notifications."""
    config = load_config(force_send=force_send)
    client = NotificationClient(config)
    results: list[SendResult] = []

    print("客戶通知自動化系統啟動")
    print(f"通知 API URL：{config.notification_api_url}")
    print(f"Dry run 模式：{config.dry_run}")
    print()

    for event in events:
        event_id = event.get("event_id", "unknown")
        event_type = event.get("event_type", "unknown")

        print(f"處理事件：{event_id} / {event_type}")

        notification = build_notification_message(event)
        if notification is None:
            print(" 未支援的 event_type，略過通知。")
            continue

        result = client.send(notification)
        results.append(result)

        if result.success:
            mode = "DRY_RUN" if result.dry_run else f"HTTP {result.status_code}"
            print(f" 通知成功：{notification.title} / {mode}")
        else:
            print(f" 通知失敗：{result.error}")

    print()
    print(f"完成：共送出或模擬 {len(results)} 筆通知。")
    print(f"Log 位置：{config.log_file}")

    return results


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Customer notification automation demo")

    parser.add_argument(
        "--event-type",
        default=None,
        help="只處理指定的 event_type，例如 customer.created。未指定則處理全部範例事件。",
    )

    parser.add_argument(
        "--send",
        action="store_true",
        help="實際送出 HTTP request。預設為 dry-run，不會打外部 API。",
    )

    return parser.parse_args()


def main() -> None:
    """Run the notification workflow."""
    args = parse_args()

    if args.event_type:
        event = get_sample_event(args.event_type)

        if event is None:
            print(f"找不到 event_type：{args.event_type}")
            return

        events = [event]
    else:
        events = get_sample_events()

    process_events(events, force_send=args.send)


if __name__ == "__main__":
    main()