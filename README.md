# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

面向“三创赛-商务大数据分析实战赛”的电商投放策略预演系统：  
用样例数据完成 A/B/C 策略对比，生成可打印报告。

## 目录

- [核心功能闭环](#核心功能闭环)
- [适用场景](#适用场景)
- [功能概览](#功能概览)
- [Windows 快速开始](#windows-快速开始)
- [3 分钟演示流程](#3-分钟演示流程)
- [API 列表与 Samples](#api-列表与-samples)
- [目录结构](#目录结构)
- [常见问题](#常见问题)

## 核心功能闭环

导入 -> 指标计算 -> 策略对比 -> 证据卡 -> 报告导出

## 适用场景

- 电商活动投放复盘：对比 A/B/C 策略收益与风险
- 课程或赛事演示：快速生成可展示的分析结果
- 教学实验：展示数据驱动的策略评估流程

## 功能概览

- 数据导入：CSV 上传，保存 dataset_id
- 指标计算：CTR/CVR/CPA/ROI 等口径输出
- 策略对比：区间估计 + 风险评分 + 驱动因素
- 证据卡：关键因素摘要与解释
- 报告导出：HTML 报告可浏览、可打印

## Windows 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- uv（Python 包管理器）

### 安装依赖

```powershell
cd "f:/Projects/AdSim"

# 一键安装（根目录 + 前端 + 后端）
npm run setup:all
```

如需分步安装：

```powershell
cd "f:/Projects/AdSim"

# 根目录与前端依赖
npm run setup

# 后端依赖（uv）
npm run setup:backend
```

### 启动服务

```powershell
cd "f:/Projects/AdSim"

# 同时启动前后端
npm run dev
```

默认端口：
- 前端：`http://localhost:3000`（若占用会自动递增）
- 后端：`http://localhost:5001`

健康检查：

```powershell
curl.exe "http://localhost:5001/health"
```

期望输出：

```json
{"status":"ok","service":"Adsim Backend"}
```

## 3 分钟演示流程

1) 上传样例 CSV（生成 dataset_id）

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@F:\Projects\AdSim\samples\ad_log.csv" `
  -F "table_type=ad_log"
```

2) 策略对比（使用 samples 请求模板）

先编辑 `F:\Projects\AdSim\samples\compare_request.json`，将 `dataset_id` 改为上一步返回值。

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@F:\Projects\AdSim\samples\compare_request.json"
```

3) 导出报告

```powershell
$tmp = Join-Path $env:TEMP "adsim_compare.json"
$export = Join-Path $env:TEMP "adsim_export.json"

# 保存对比结果
$compare = curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@F:\Projects\AdSim\samples\compare_request.json"
$compare | Set-Content -Encoding utf8 -Path $tmp

# 组装导出请求
$payload = @{ compare_result = (Get-Content -Raw $tmp | ConvertFrom-Json); selected_strategy = "A" } | ConvertTo-Json -Depth 8
$payload | Set-Content -Encoding utf8 -Path $export

curl.exe -X POST "http://localhost:5001/api/v1/adsim/report/export" `
  -H "Content-Type: application/json" `
  -d "@$export"
```

接口返回 `download_url` 后，在浏览器打开：

```
http://localhost:5001/api/v1/adsim/report/download/<report_id>
```

## API 列表与 Samples

API：
- `GET /api/v1/adsim/health`
- `POST /api/v1/adsim/data/upload`
- `POST /api/v1/adsim/metrics/compute`
- `POST /api/v1/adsim/strategy/compare`
- `POST /api/v1/adsim/report/export`
- `GET /api/v1/adsim/report/download/{report_id}`

Samples：
- `samples/ad_log.csv`
- `samples/orders.csv`
- `samples/metrics_request.json`
- `samples/compare_request.json`

## 目录结构

```
AdSim/
├─ backend/                 # 后端（Flask）
├─ frontend/                # 前端（Vite + Vue）
├─ samples/                 # 最小可用样例数据与请求
├─ reports/sample/          # 报告样例占位（避免提交产物）
├─ docs/                    # 参赛文档与说明
├─ static/                  # 静态图片
├─ cache/                   # 运行缓存（不入库）
├─ data_store/              # 数据集产物（不入库）
└─ README.md
```

## 常见问题

### 1) 端口占用

- 前端端口 3000 被占用时，Vite 会自动切换到 3001/3002。
- 后端 5001 被占用时，请先关闭占用进程或修改环境变量 `FLASK_PORT`。

### 2) .env 配置

后端依赖 `.env` 中的外部服务配置，模板见：`F:\Projects\AdSim\.env.example`。  
若仅演示 Adsim 数据链路，可先保持默认并不调用外部 LLM 相关功能。

### 3) 依赖安装失败

- 请确认 Node 版本 `>=18`，Python `>=3.11`。
- 推荐使用 `npm run setup:all` 一键安装。
- 若后端依赖失败，可尝试：

```powershell
cd "f:/Projects/AdSim/backend"
uv sync
```
