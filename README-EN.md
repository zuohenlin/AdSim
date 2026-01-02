# Adsim

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](./package.json)

E-commerce campaign strategy rehearsal and decision report system for the  
“National College Entrepreneurship Competition - Business Big Data Analysis Track”.  
Reproduce A/B/C strategy differences with minimal samples, and export explainable reports.

![Adsim Logo](./static/image/adsim_logo.png)

## Table of Contents

- [Positioning & Core Loop](#positioning--core-loop)
- [Capabilities & Differentiation](#capabilities--differentiation)
- [System Modes](#system-modes)
- [Launch & Endpoints (Interactive Script)](#launch--endpoints-interactive-script)
- [3-Minute Demo](#3-minute-demo)
- [Adsim Insight → Adsim Pipeline](#adsim-insight--adsim-pipeline)
- [Frontend Routes](#frontend-routes)
- [Key APIs](#key-apis)
- [Data Specs & Metrics](#data-specs--metrics)
- [Architecture & Structure](#architecture--structure)
- [Comparison vs. Alternatives](#comparison-vs-alternatives)
- [Innovation / Creativity / Entrepreneurship](#innovation--creativity--entrepreneurship)
- [Screenshots & Assets](#screenshots--assets)
- [Compliance & Third-Party](#compliance--third-party)
- [FAQ](#faq)
- [Pre-Submit Checklist](#pre-submit-checklist)

## Positioning & Core Loop

**Positioning**: strategy rehearsal and decision reporting for e-commerce ad campaigns.  
**Loop**: Import → Metrics → Strategy Compare → Evidence Cards → Report Export

## Capabilities & Differentiation

- **Explainable comparison**: metrics + drivers + evidence cards.  
- **Interval estimates**: show uncertainty, avoid single-point bias.  
- **3-minute demo**: sample upload → compare → export.  
- **Offline-ready**: Adsim data pipeline runs without external LLM.  
- **Printable reports**: HTML report for presentation and scoring.  

## System Modes

- **Adsim data pipeline**: ad/order data-driven comparison and report export (offline).  
- **Original simulation entry**: text/file-driven multi-agent simulation (requires LLM).  
- **Adsim Insight (based on BettaFish)**: optional public-opinion/text analysis module, not required for the competition main demo.  

## Launch & Endpoints (Interactive Script)

> Use the interactive script for guided start, status check, and endpoints display.

### Requirements

- Node.js 18+  
- Python 3.11+  
- uv (Python package manager)  
- Docker (optional, for Adsim Insight)

### Install

```powershell
cd .
npm run setup:all
```

Recommended: copy and verify `.env` (you can keep defaults if no external LLM is used):

```powershell
Copy-Item ".env.example" ".env"
```

Optional: prepare `third_party/BettaFish/.env` based on `third_party/BettaFish/.env.example` and fill API keys.

### Start (recommended)

```powershell
./tools/run_all.ps1
```

The script can:
- Start Adsim + Adsim Insight  
- Start Adsim only  
- Start Adsim Insight only  
- Status check / stop services  

### Endpoints

- Adsim Frontend: `http://localhost:3000`  
- Adsim Backend: `http://localhost:5001`  
- Adsim Insight (Flask): `http://localhost:5000`  
- Adsim Insight (Streamlit): `http://localhost:8501`  

### Health check

```powershell
curl.exe "http://localhost:5001/health"
```

Expected:

```json
{"status":"ok","service":"Adsim Backend"}
```

### Adsim Insight only (fallback)

```powershell
docker compose -f docker-compose.bettafish.yml up --build
```

Stop:

```powershell
docker compose -f docker-compose.bettafish.yml down
```

## 3-Minute Demo

> Use `samples/` data and templates. This flow is fully offline-capable.

### Option A: UI (recommended)

1) Start services: `./tools/run_all.ps1`  
2) Import page: `/adsim/import`  
3) Upload `samples/ad_log.csv` and `samples/orders.csv`  
4) Strategy page: `/adsim/strategy`  
5) Compare page: `/adsim/compare`  
6) Click “Export Report”  

### Option B: API (PowerShell)

1) Upload data (get dataset_id)

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

2) Strategy compare

Edit `samples/compare_request.json` and set `dataset_id` from step 1.

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

Open the returned `download_url`:  
`http://localhost:5001/api/v1/adsim/report/download/<report_id>`

## Adsim Insight → Adsim Pipeline

Goal: generate a research report in Adsim Insight, then use it as the “seed file” in Adsim for prediction/simulation.

Flow:
1) Start Adsim Insight  
2) Generate a research report (HTML/MD/PDF)  
3) Open Adsim home page and upload the report as the “seed file”  
4) Enter the simulation prompt to run prediction/simulation  

Note: This pipeline depends on external LLM and online access and is suitable for demonstrating the full loop.

## Frontend Routes

- Home: `/`  
- Data import: `/adsim/import`  
- Strategy config: `/adsim/strategy`  
- Compare results: `/adsim/compare`  

Original simulation routes (from MiroFish):  
- `/process/:projectId`  
- `/simulation/:simulationId`  
- `/simulation/:simulationId/start`  
- `/report/:reportId`  
- `/interaction/:reportId`  

## Key APIs

- `GET /health`  
- `GET /api/v1/adsim/health`  
- `POST /api/v1/adsim/data/upload`  
- `POST /api/v1/adsim/metrics/compute`  
- `POST /api/v1/adsim/strategy/compare`  
- `POST /api/v1/adsim/report/export`  
- `GET /api/v1/adsim/report/download/{report_id}`  

## Data Specs & Metrics

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

### Metric Definitions

- **CTR** = clicks / impressions  
- **CVR** = orders / clicks (or conversions / clicks)  
- **CPA** = spend / orders  
- **ROI_GP** = gross_profit / spend (fallback to gmv * margin_rate)  
- **Refund Rate** = refund_orders / total_orders  

## Architecture & Structure

### Architecture (ASCII)

```
Frontend (Vite+Vue) -> Adsim API (Flask) -> Metrics / Compare / Report
                           |
                           +-- Optional: Adsim Insight (BettaFish)
```

### Project Structure

```
AdSim/
├─ archive/                 # Archived non-demo resources
├─ backend/                 # Flask backend
├─ docs/                    # Competition docs
├─ frontend/                # Vite + Vue frontend
├─ samples/                 # Sample data & requests
├─ static/                  # Static images
├─ third_party/             # Adsim Insight (BettaFish)
└─ tools/                   # Utility scripts
```

Note: `data_store/`, `cache/`, and `reports/` are runtime outputs and should not be committed.

## Comparison vs. Alternatives

| Category | Typical Form | Coverage | Explainability | Rehearsal/Uncertainty | Deployment Cost | Competition Fit | Adsim Advantage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Traditional BI | Tableau/PowerBI/custom reports | Strong reporting | Medium | No | Medium | Medium | Adsim adds rehearsal + evidence cards |
| Ad Platform Backend | Native platform dashboards | Strong platform data | Low-Med | No | High (platform bound) | Medium | Adsim is offline & explainable |
| Attribution Tools | Marketing attribution products | Strong attribution | Medium | No | Med-High | Medium | Adsim focuses on strategy rehearsal |
| Prediction Demos | Academic/contest models | Strong prediction | Low | No | Low | Low-Med | Adsim provides end-to-end loop |

**Key differentiation**: strategy rehearsal, interval uncertainty, evidence cards, one-click report, offline demo stability.

## Innovation / Creativity / Entrepreneurship

### Innovation
- Evidence-card driven explainability for A/B/C strategy comparison.  
- Interval estimates for risk-aware decisions.  
- One-click report export for competition defense.  

### Creativity
- “3-minute demo loop” designed for judges.  
- Interactive script for guided start and endpoints.  
- Optional Adsim Insight for future expansion.  

### Entrepreneurship
- Aligns with real e-commerce ad workflow.  
- Offline-ready deployment lowers adoption barrier.  
- Report templates as deliverable for commercialization.  

## Screenshots & Assets

Existing assets in this repo (replace files to update):
- Import: `./docs/ui-import.png`  
- Strategy: `./docs/ui-strategy.png`  
- Compare: `./docs/ui-compare.png`  
- Architecture: `./docs/architecture.png`  
- Flow: `./docs/flow.png`  

![Import](./docs/ui-import.png)
![Strategy](./docs/ui-strategy.png)
![Compare](./docs/ui-compare.png)

## Compliance & Third-Party

- Main license: `./LICENSE` (AGPL-3.0)  
- Adsim Insight (BettaFish) license: `./third_party/BettaFish/LICENSE` (GPL-2.0)  
- Third-Party notices: `./THIRD_PARTY_NOTICES.md`  

## FAQ

### 1) Port in use

- Frontend 3000 busy -> Vite switches to 3001/3002  
- Backend 5001 busy -> close the process or set `FLASK_PORT`  

### 2) .env config

Backend uses `.env` for external services. Template: `.env.example`.  
For Adsim data pipeline demo, you can keep defaults without external LLM calls.

### 3) Install issues

- Ensure Node `>=18`, Python `>=3.11`  
- Use `npm run setup:all`  
- If backend fails:

```powershell
cd backend
uv sync
```

## Pre-Submit Checklist

- `git status` is clean  
- `.gitignore` excludes runtime artifacts  
- `./tools/run_all.ps1` starts services and shows endpoints  
- `curl.exe "http://localhost:5001/health"` returns `ok`  
- `strategy/compare` and `report/export` respond correctly  
