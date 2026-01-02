# Adsim Usage Guide

> For competition demo and TA review.

## Contents

- [Quick Start (Interactive Script)](#quick-start-interactive-script)
- [Core Flow (Adsim Data Pipeline)](#core-flow-adsim-data-pipeline)
- [Adsim Insight → Adsim Pipeline](#adsim-insight--adsim-pipeline)
- [Original Simulation Entry (Seed Text/Prompt)](#original-simulation-entry-seed-textprompt)
- [Report Export and View](#report-export-and-view)
- [Samples and Requests](#samples-and-requests)
- [FAQ](#faq)

## Quick Start (Interactive Script)

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

Endpoints:  
- Adsim Frontend: `http://localhost:3000`  
- Adsim Backend: `http://localhost:5001`  
- Adsim Insight (Flask): `http://localhost:5000`  
- Adsim Insight (Streamlit): `http://localhost:8501`  

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

## Adsim Insight → Adsim Pipeline

Goal: generate a research report in Adsim Insight, then use it as the “seed file” in Adsim for prediction/simulation.

Steps:
1) Start Adsim Insight  
2) Generate a research report (HTML/MD/PDF)  
3) Open Adsim home page and upload the report as “seed file”  
4) Enter the simulation prompt to run prediction/simulation  

Note: This pipeline depends on external LLM and online access and is suitable for demonstrating the full loop.

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

Open the returned `download_url` in a browser:

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

### 2) .env config

Backend uses `.env` for external services. Template: `.env.example`.  
For Adsim data pipeline demo, you can keep defaults without external LLM calls.
