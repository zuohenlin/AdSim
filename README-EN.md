# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

Ad campaign planning for the competition track:  
Rehearse A/B/C strategies and export a printable report.

## Contents

- [Core Flow](#core-flow)
- [Use Cases](#use-cases)
- [Feature Overview](#feature-overview)
- [Quick Start (Windows)](#quick-start-windows)
- [3-Minute Demo](#3-minute-demo)
- [API List and Samples](#api-list-and-samples)
- [Project Structure](#project-structure)
- [FAQ](#faq)

## Core Flow

Import -> Metrics -> Strategy Compare -> Evidence Cards -> Report Export

## Use Cases

- E-commerce campaign review and comparison
- Competition demo with minimal setup
- Teaching demo for data-driven strategy evaluation

## Feature Overview

- Data upload (CSV) with dataset_id
- KPI calculations (CTR/CVR/CPA/ROI)
- Strategy compare with interval estimates and risk factors
- Evidence cards to explain drivers
- HTML report export (browser-friendly, printable)

## Quick Start (Windows)

### Requirements

- Node.js 18+
- Python 3.11+
- uv (Python package manager)

### Install

```powershell
cd "f:/Projects/AdSim"

# All-in-one install (root + frontend + backend)
npm run setup:all
```

Or step by step:

```powershell
cd "f:/Projects/AdSim"

# Root + frontend
npm run setup

# Backend (uv)
npm run setup:backend
```

### Run

```powershell
cd "f:/Projects/AdSim"

# Start frontend + backend
npm run dev
```

Default ports:
- Frontend: `http://localhost:3000` (auto-increments if busy)
- Backend: `http://localhost:5001`

Health check:

```powershell
curl.exe "http://localhost:5001/health"
```

Expected:

```json
{"status":"ok","service":"Adsim Backend"}
```

## 3-Minute Demo

1) Upload sample CSV (get dataset_id)

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@F:\Projects\AdSim\samples\ad_log.csv" `
  -F "table_type=ad_log"
```

2) Strategy compare (use samples request)

Edit `F:\Projects\AdSim\samples\compare_request.json` and set `dataset_id`.

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@F:\Projects\AdSim\samples\compare_request.json"
```

3) Export report

```powershell
$tmp = Join-Path $env:TEMP "adsim_compare.json"
$export = Join-Path $env:TEMP "adsim_export.json"

$compare = curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@F:\Projects\AdSim\samples\compare_request.json"
$compare | Set-Content -Encoding utf8 -Path $tmp

$payload = @{ compare_result = (Get-Content -Raw $tmp | ConvertFrom-Json); selected_strategy = "A" } | ConvertTo-Json -Depth 8
$payload | Set-Content -Encoding utf8 -Path $export

curl.exe -X POST "http://localhost:5001/api/v1/adsim/report/export" `
  -H "Content-Type: application/json" `
  -d "@$export"
```

Open the returned `download_url` in a browser.

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
- `samples/metrics_request.json`
- `samples/compare_request.json`

## Project Structure

```
AdSim/
├─ backend/                 # Flask backend
├─ frontend/                # Vite + Vue frontend
├─ samples/                 # Minimal datasets and requests
├─ reports/sample/          # Report placeholder
├─ docs/                    # Competition docs
├─ static/                  # Static images
├─ cache/                   # Runtime cache (ignored)
├─ data_store/              # Dataset outputs (ignored)
└─ README-EN.md
```

## FAQ

### 1) Port in use

- Frontend 3000 is busy -> Vite switches to 3001/3002
- Backend 5001 is busy -> close the process or set `FLASK_PORT`

### 2) .env config

Backend uses `.env` for external services. Template: `F:\Projects\AdSim\.env.example`.  
For Adsim demo flow only, you can keep defaults without external LLM calls.

### 3) Install issues

- Ensure Node `>=18`, Python `>=3.11`
- Use `npm run setup:all`
- If backend fails:

```powershell
cd "f:/Projects/AdSim/backend"
uv sync
```

## Credits

Competition-focused adaptation based on:
https://github.com/666ghj/MiroFish
