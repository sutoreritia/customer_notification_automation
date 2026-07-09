"""Sample webhook events for classroom practice"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

WebhookEvent=dict[str,Any]

SAMPLE_EVENTS:list[WebhookEvent]=[
    {
        "event_id":"evt_001",
        "event_type":"customer.created",
        "created_at":"2026-06-01T09:00:00+8:00",
        "data":{
            "customer_id":"C001",
            "customer_name":"王小明",
            "email":"ming@example.com",
            "level":"一般",
            "city":"高雄"
        },
    },
    {
        "event_id":"evt_002",
        "event_type":"customer.high_value",
        "created_at":"2026-06-01T10:15:00+8:00",
        "data":{
            "customer_id":"C002",
            "customer_name":"林雅婷",
            "email":"yating@example.com",
            "total_spent":128000,
            "level":"VIP",
        },
    },
    {
        "event_id":"evt_003",
        "event_type":"complaint.created",
        "created_at":"2026-06-01T11:30:00+8:00",
        "data":{
            "ticket_id":"T20260601001",
            "customer_id":"C003",
            "customer_name":"陳志豪",
            "priority":"high",
            "message":"商品到貨後外箱破損，請客服協助處理。",
        },
    },
    {
        "event_id":"evt_004",
        "event_type":"order.cancelled",
        "created_at":"2026-06-01T13:20:00+8:00",
        "data":{
            "order_id":"O1004",
            "customer_id":"C004",
            "customer_name":"黃怡君",
            "amount":5000,
            "reason":"客戶改買其他方案",
        },
    },
    {
        "event_id":"evt_005",
        "event_type":"report.ready",
        "created_at":"2026-06-01T17:00:00+8:00",
        "data":{
            "report_name":"五月KPI營運報表",
            "report_url":"https://example.com/reports/kpi-2026-05",
            "owner":"營運分析組",
        },
    },
    {
        "event_id":"evt_006",
        "event_type":"unknown.event",
        "created_at":"2026-06-01T18:00:00+8:00",
        "data":{
            "message":"這是一筆未知事件，用來測試防呆流程",
        },
    },
]



def get_sample_events()->list[WenhookEvent]:
    """Return a copy of all sample webhook events."""
    return deepcopy(SAMPLE_EVENTS)
def get_sample_event(event_type: str)->WebhookEvent|None:
    """Return the first sample matching an event type."""
    for event in SAMPLE_EVENTS:
        if event["event_type"]==event_type:
            return deepcopy(event)
    return None