# Adsim 使用文档

> 适用于“三创赛-商务大数据分析实战赛”演示与答辩。

## 目录

- [快速开始](#快速开始)
- [核心流程（Adsim 数据链路）](#核心流程adsim-数据链路)
- [原始仿真入口（现实种子/模拟提示词）](#原始仿真入口现实种子模拟提示词)
- [报告导出与查看](#报告导出与查看)
- [样例数据与请求](#样例数据与请求)
- [常见问题](#常见问题)

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- uv（Python 包管理器）

### 安装依赖

```powershell
cd .

# 一键安装（根目录 + 前端 + 后端）
npm run setup:all
```

### 启动服务

```powershell
cd .

# 同时启动前后端
npm run dev
```

默认端口：
- 前端：`http://localhost:3000`
- 后端：`http://localhost:5001`

健康检查：

```powershell
curl.exe "http://localhost:5001/health"
```

期望输出：

```json
{"status":"ok","service":"Adsim Backend"}
```

## 核心流程（Adsim 数据链路）

### 入口页面

- 数据导入：`http://localhost:3000/adsim/import`
- 策略配置：`http://localhost:3000/adsim/strategy`
- 对比结果：`http://localhost:3000/adsim/compare`

## 两种模式说明

- **Adsim 数据链路**：面向投放数据、策略对比与报告导出。
- **原始仿真入口**：面向文本/文件驱动的群体智能仿真（继承自 MiroFish）。

### 1) 上传数据（生成 dataset_id）

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

返回包含：`dataset_id`、`detected_columns`、`missing_required_columns`、`sample_rows`、`saved_path`。

### 2) 计算指标

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/metrics/compute" `
  -H "Content-Type: application/json" `
  -d "@samples/metrics_request.json"
```

### 3) 策略对比

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
```

## 原始仿真入口（现实种子/模拟提示词）

首页的“现实种子”和“模拟提示词”仍然用于原始仿真流程（继承自 MiroFish）。
它与 Adsim 的电商投放链路是两条独立入口：

- **Adsim 数据链路**：面向投放数据、策略对比与报告导出。
- **原始仿真入口**：面向文本/文件驱动的群体智能仿真。

若你只做 Adsim 演示，可忽略该入口；需要展示原始仿真时：

1) 在首页“现实种子”上方填写 LLM 配置（保存后写入项目根目录 `.env`，仅调试模式可写入）：  
   - `LLM_API_KEY`  
   - `LLM_BASE_URL`  
   - `LLM_MODEL_NAME`  
   - `ZEP_API_KEY`  
   - `LLM_BOOST_API_KEY`（可选）  
   - `LLM_BOOST_BASE_URL`（可选）  
   - `LLM_BOOST_MODEL_NAME`（可选）  
2) 上传 `pdf/md/txt` 文件并填写“模拟提示词”。  

## 报告导出与查看

```powershell
$tmp = Join-Path $env:TEMP "adsim_compare.json"
$export = Join-Path $env:TEMP "adsim_export.json"

# 保存对比结果
$compare = curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
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

## 样例数据与请求

- `samples/ad_log.csv`
- `samples/orders.csv`
- `samples/ad_log_100.csv`
- `samples/orders_100.csv`
- `samples/metrics_request.json`
- `samples/compare_request.json`

## 常见问题

### 1) 端口占用

- 前端 3000 被占用时，Vite 会自动切换到 3001/3002。
- 后端 5001 被占用时，请先关闭占用进程或修改 `FLASK_PORT`。

### 2) 后端启动失败

```powershell
cd backend
uv sync
```

### 3) Windows 的 curl 提示安全警告

使用 `curl.exe`，避免 PowerShell `Invoke-WebRequest` 的脚本提示。
