# Customer Notification Automation — Event Routing & Webhook/API Client

[English](#english) · [繁體中文](#繁體中文)

## English

A **Python event-to-notification workflow demo**. The program reads **sample webhook-shaped events**, validates their structure, builds notifications for business scenarios, and either simulates sending them (default) or POSTs payloads to a configured HTTP API. It is **not yet a listening webhook server**.

## Supported sample events

| Event type | Notification purpose |
| --- | --- |
| `customer.created` | Notify sales about a new customer |
| `customer.high_value` | Alert the sales manager about a high-value customer |
| `complaint.created` | Inform customer support about a complaint |
| `order.cancelled` | Inform customer support about a cancelled order |
| `report.ready` | Inform management when an operations report is ready |

Unknown event types are skipped. All input examples are simulated; the dry-run mode **does not send external HTTP requests**.

## Workflow

```text
Sample events --> validation --> event-type mapping --> notification payload
                                                        |
                                                 Dry run / HTTP POST
                                                        |
                                                  JSONL event log
```

## Setup (Python 3.10+)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
Copy-Item .env.example .env
```

Keep `NOTIFICATION_DRY_RUN=true` for safe local testing:

```powershell
python main.py
python main.py --event-type customer.created
```

To send an actual HTTP POST to `NOTIFICATION_API_URL` with the configured token:

```powershell
python main.py --send
```

**Warning:** `--send` creates real outgoing network requests; use only a test endpoint under your control, with synthetic data. The `.env.example` URL is a public API test endpoint, **not an actual customer notification provider**.

## Configuration

```dotenv
NOTIFICATION_API_TOKEN=replace_with_your_token
NOTIFICATION_API_URL=https://jsonplaceholder.typicode.com/posts
NOTIFICATION_TIMEOUT_SECONDS=10
NOTIFICATION_DRY_RUN=true
```

Do not commit `.env`, API tokens, or real customer events. Send results, including payload data, are written to `logs/notification_log.jsonl`; avoid using real personal information.

## Files

- `main.py` — CLI arguments and event-processing loop
- `src/event_samples.py` — synthetic example events
- `src/event_handler.py` — validation and event-to-message mapping
- `src/notification_client.py` — dry-run/HTTP sender and JSONL logging
- `src/config.py` — environment configuration

## Limitations / improvements

This prototype does not receive real-time incoming webhooks, queue messages, deduplicate event IDs, or provide production retries and delivery guarantees. Next steps include tests, signed webhook verification, retries with backoff, idempotency controls, and a real webhook endpoint.

---

## 繁體中文

這是一個 **Python 事件轉通知的流程練習專案**。程式讀取**模擬 Webhook 格式事件**，驗證欄位、依事件種類產生通知，再選擇只模擬發送（預設）或向指定 HTTP API 執行 POST。**目前並不是能接收外部 Webhook 的伺服器。**

## 支援的示範事件

| 事件 | 通知目的 |
| --- | --- |
| `customer.created` | 新客戶建立，通知業務 |
| `customer.high_value` | 高價值客戶，通知業務主管 |
| `complaint.created` | 新客訴，通知客服 |
| `order.cancelled` | 訂單取消，通知客服 |
| `report.ready` | 營運報表產生完成，通知管理部門 |

不支援的事件種類會略過。全部範例皆為模擬資料；在預設 Dry-run 模式下，**不會向外部發送 HTTP 請求**。

## 流程架構

```text
示範事件 --> 欄位驗證 --> 事件種類對應 --> 通知內容
                                           |
                                  模擬發送 / HTTP POST
                                           |
                                        JSONL 日誌
```

## 安裝方式（Python 3.10+）

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
Copy-Item .env.example .env
```

建議先保留 `NOTIFICATION_DRY_RUN=true` 測試：

```powershell
python main.py
python main.py --event-type customer.created
```

如果要向 `NOTIFICATION_API_URL` 發出真正的 POST：

```powershell
python main.py --send
```

**警告：** `--send` 會真的發出網路請求，僅應對自己掌控的測試端點傳送假資料。`.env.example` 的網址是通用測試 API，**不是正式的客戶通知服務**。

## 環境變數

```dotenv
NOTIFICATION_API_TOKEN=replace_with_your_token
NOTIFICATION_API_URL=https://jsonplaceholder.typicode.com/posts
NOTIFICATION_TIMEOUT_SECONDS=10
NOTIFICATION_DRY_RUN=true
```

請勿提交 `.env`、API Token 或真實客戶事件。系統會將傳送結果及 Payload 寫入 `logs/notification_log.jsonl`，因此不要輸入真實個資。

## 主要檔案

- `main.py`：選項解析與事件處理流程
- `src/event_samples.py`：模擬事件
- `src/event_handler.py`：格式驗證、事件與通知內容對應
- `src/notification_client.py`：Dry-run／HTTP 發送與 JSONL 紀錄
- `src/config.py`：環境變數設定

## 目前限制與後續規劃

目前還沒有接收真實 Webhook、訊息佇列、事件去重、正式的重試策略或傳送保證。可再增加測試、Webhook 簽章驗證、指數退避重試、冪等性處理及真正的 Webhook API 端點。
