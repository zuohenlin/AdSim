# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

E-commerce ad campaign rehearsal for the competition track.  
Compare A/B/C strategies with samples and export a printable report.

## Core Flow

Import -> Metrics -> Strategy Compare -> Evidence Cards -> Report Export

## Two Modes

- **Adsim data pipeline**: ad/order data driven strategy comparison and report export.
- **Original simulation entry**: text/file-driven multi-agent simulation (inherited from MiroFish).

### Mode Pros and Cons

| Mode | Pros | Cons | Best For |
| --- | --- | --- | --- |
| Adsim data pipeline | No LLM dependency, stable demos, controllable data | Depends on data quality | Competition demo, strategy review |
| Original simulation entry | Handles unstructured text, strong explainability | Requires LLM API and external services | Public opinion simulation, multi-agent rehearsal |

## Project Summary

Adsim turns ad data into explainable strategy comparisons, with evidence cards and interval estimates for fast evaluation and defense demos.

## Key Innovations

- **Explainable comparison**: metrics + drivers + evidence cards
- **Interval estimates** for uncertainty
- **End-to-end demo** within minutes

## Key Creative Ideas

- **Dual-mode presentation** for data-driven and text-driven demos
- **Evidence-card storytelling** for clear defense narrative
- **Sample-first onboarding** with ready-to-run assets

## Key Entrepreneurship Points

- **Business-ready scope** aligned to ad/commerce data
- **Low-cost deployment** for small teams
- **Extensible monetization** via data connectors and report templates

## Architecture

![Architecture](./docs/architecture.png)

## Flow

![Flow](./docs/flow.png)

## UI Screenshots

![Import](./docs/ui-import.png)
![Strategy](./docs/ui-strategy.png)
![Compare](./docs/ui-compare.png)

## Data Dictionary

### ad_log

| Field | Type | Description |
| --- | --- | --- |
| ad_id | string | Campaign or ad ID |
| impressions | int | Impressions |
| clicks | int | Clicks |
| date | datetime | Date |
| spend | float | Spend (optional) |
| gmv | float | GMV (optional) |
| conversions | int | Conversions (optional) |

### orders

| Field | Type | Description |
| --- | --- | --- |
| order_id | string | Order ID |
| user_id | string | User ID |
| amount | float | Amount (or gmv) |
| order_date | datetime | Order date |
| gross_profit | float | Gross profit (optional) |
| refund_orders | int | Refund order count (optional) |
| is_refund | bool | Refund flag (optional) |

## Metric Definitions

- **CTR** = clicks / impressions  
- **CVR** = orders / clicks (or conversions / clicks)  
- **CPA** = spend / orders  
- **ROI_GP** = gross_profit / spend (fallback to gmv * margin_rate)  
- **Refund Rate** = refund_orders / total_orders

## API List and Samples

API:
- `GET /api/v1/adsim/health`
- `POST /api/v1/adsim/data/upload`
- `POST /api/v1/adsim/metrics/compute`
- `POST /api/v1/adsim/strategy/compare`
- `POST /api/v1/adsim/report/export`
- `GET /api/v1/adsim/report/download/{report_id}`

Samples:
- `samples/ad_log.csv`
- `samples/orders.csv`
- `samples/ad_log_100.csv`
- `samples/orders_100.csv`
- `samples/metrics_request.json`
- `samples/compare_request.json`

Usage guide:
- `docs/USAGE-EN.md`

## Quick Start (Windows)

### Requirements

- Node.js 18+
- Python 3.11+
- uv (Python package manager)

### Install

```powershell
cd .

# All-in-one install (root + frontend + backend)
npm run setup:all
```

### Run

```powershell
cd .

# Start frontend + backend
npm run dev
```

Default ports:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5001`

Health check:

```powershell
curl.exe "http://localhost:5001/health"
```

Expected:

```json
{"status":"ok","service":"Adsim Backend"}
```

## Docker (Multi-Container)

```powershell
docker compose up --build
```

Frontend/Backend:
- `http://localhost:3000`
- `http://localhost:5001`

Override for local backend:

```powershell
docker compose -f docker-compose.yml -f docker-compose.override.local.yml up --build
```

## 3-Minute Demo

1) Upload sample CSV (get dataset_id)

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

2) Strategy compare (use samples request)

Edit `samples/compare_request.json` and set `dataset_id`.

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
```

3) Export report

```powershell
$tmp = Join-Path $env:TEMP "adsim_compare.json"
$export = Join-Path $env:TEMP "adsim_export.json"

$compare = curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
$compare | Set-Content -Encoding utf8 -Path $tmp

$payload = @{ compare_result = (Get-Content -Raw $tmp | ConvertFrom-Json); selected_strategy = "A" } | ConvertTo-Json -Depth 8
$payload | Set-Content -Encoding utf8 -Path $export

curl.exe -X POST "http://localhost:5001/api/v1/adsim/report/export" `
  -H "Content-Type: application/json" `
  -d "@$export"
```

Open the returned `download_url` in a browser.

## Project Structure

```
AdSim/
|-- backend/                 # Flask backend
|-- frontend/                # Vite + Vue frontend
|-- samples/                 # Sample datasets and requests
|-- docs/                    # Competition docs
|-- static/                  # Static images
`-- README-EN.md
```

Note: `data_store/`, `cache/`, and `reports/` are runtime outputs generated on demand and should not be committed.

## FAQ

### 1) Port in use

- Frontend 3000 busy -> Vite switches to 3001/3002
- Backend 5001 busy -> close the process or set `FLASK_PORT`

### 2) .env config

Backend uses `.env` for external services. Template: `.env.example`.  
For Adsim demo flow only, you can keep defaults without external LLM calls.

### 3) Install issues

- Ensure Node `>=18`, Python `>=3.11`
- Use `npm run setup:all`
- If backend fails:

```powershell
cd backend
uv sync
```

## Credits

Competition-focused adaptation based on:
https://github.com/666ghj/MiroFish
