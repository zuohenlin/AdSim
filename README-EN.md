# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

Ad campaign planning: A/B/C strategy rehearsal and report.

## What it does

Import ? Metrics ? Strategy Compare ? Evidence Cards ? Report Export

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

## API List (Adsim)

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

## Credits

This project is a competition-focused adaptation based on:
https://github.com/666ghj/MiroFish
