# Adsim Usage Guide

> For competition demo and TA review.

## Contents

- [Quick Start](#quick-start)
- [Core Flow (Adsim Data Pipeline)](#core-flow-adsim-data-pipeline)
- [Original Simulation Entry (Seed Text/Prompt)](#original-simulation-entry-seed-textprompt)
- [Report Export and View](#report-export-and-view)
- [Samples and Requests](#samples-and-requests)
- [FAQ](#faq)

## Quick Start

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

## Core Flow (Adsim Data Pipeline)

### Entry Pages

- Import: `http://localhost:3000/adsim/import`
- Strategy: `http://localhost:3000/adsim/strategy`
- Compare: `http://localhost:3000/adsim/compare`

## Two Modes

- **Adsim data pipeline**: ad data, strategy comparison, report export.
- **Original simulation entry**: text/file-driven multi-agent simulation (inherited from MiroFish).
- **Opinion analysis module**: news/text search and hotness estimate.

### 1) Upload data (get dataset_id)

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

Response includes: `dataset_id`, `detected_columns`, `missing_required_columns`, `sample_rows`, `saved_path`.

### 2) Compute metrics

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/metrics/compute" `
  -H "Content-Type: application/json" `
  -d "@samples/metrics_request.json"
```

### 3) Compare strategies

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
```

## Original Simulation Entry (Seed Text/Prompt)

The home page fields “seed files” and “simulation prompt” are still used by the original simulation flow (inherited from MiroFish). This is separate from the Adsim data pipeline:

- **Adsim data pipeline**: data import, metrics, strategy comparison, report export.
- **Original simulation entry**: text/file-driven multi-agent simulation.

If you only demo Adsim, you can ignore this entry. To use it:

1) Fill in LLM config above the seed upload (saved to project root `.env`, debug mode only):  
   - `LLM_API_KEY`  
   - `LLM_BASE_URL`  
   - `LLM_MODEL_NAME`  
   - `ZEP_API_KEY`  
   - `LLM_BOOST_API_KEY` (optional)  
   - `LLM_BOOST_BASE_URL` (optional)  
   - `LLM_BOOST_MODEL_NAME` (optional)  
2) Upload `pdf/md/txt` files and provide a simulation prompt on the home page.  

## Report Export and View

```powershell
$tmp = Join-Path $env:TEMP "adsim_compare.json"
$export = Join-Path $env:TEMP "adsim_export.json"

# Save compare result
$compare = curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
$compare | Set-Content -Encoding utf8 -Path $tmp

# Build export payload
$payload = @{ compare_result = (Get-Content -Raw $tmp | ConvertFrom-Json); selected_strategy = "A" } | ConvertTo-Json -Depth 8
$payload | Set-Content -Encoding utf8 -Path $export

curl.exe -X POST "http://localhost:5001/api/v1/adsim/report/export" `
  -H "Content-Type: application/json" `
  -d "@$export"
```

Open `download_url` in browser:

```
http://localhost:5001/api/v1/adsim/report/download/<report_id>
```

## Samples and Requests

- `samples/ad_log.csv`
- `samples/orders.csv`
- `samples/ad_log_100.csv`
- `samples/orders_100.csv`
- `samples/metrics_request.json`
- `samples/compare_request.json`


## FAQ

### 1) Port in use

- Frontend 3000 busy -> Vite switches to 3001/3002
- Backend 5001 busy -> close the process or set `FLASK_PORT`

### 2) Backend fails to start

```powershell
cd backend
uv sync
```

### 3) PowerShell curl security warning

Use `curl.exe` to avoid `Invoke-WebRequest` script warning.
