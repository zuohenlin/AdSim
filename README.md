# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

面向“三创赛-商务大数据分析实战赛”的电商投放策略预演系统。  
以样例数据复现 A/B/C 策略对比，输出可解释证据与可打印报告。

## 核心闭环

导入数据 -> 指标计算 -> 策略对比 -> 证据卡 -> 报告导出

## 两种模式

- **Adsim 数据链路**：投放数据/订单数据驱动的策略对比与报告导出。
- **原始仿真入口**：文本/文件驱动的群体智能仿真（继承自 MiroFish）。

### 两种模式优缺点

| 模式 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| Adsim 数据链路 | 不依赖 LLM、结果稳定、便于演示 | 依赖投放/订单数据质量 | 策略复盘、投放对比、竞赛演示 |
| 原始仿真入口 | 可处理非结构化文本、可解释性强 | 需要 LLM API 与外部配置 | 舆情推演、多智能体场景模拟 |

## 项目简介

Adsim 将投放数据转化为可解释的策略对比结果，通过证据卡与区间估计帮助评委和业务方快速理解“为什么 A/B/C 不同”。系统强调演示闭环、复现成本低、输出可打印报告。

## 主要创新点

- **可解释对比**：输出指标 + 驱动因素 + 证据卡。
- **区间估计**：给出波动区间，避免单点结论。
- **流程闭环**：3 分钟内完成上传、对比与报告导出。

## 主要创意点

- **双模式并行**：数据链路 + 原始仿真入口可独立展示。
- **证据卡表达**：更适合答辩的结论结构。
- **样例即用**：内置样例数据与请求模板。

## 主要创业点

- **贴合真实投放流程**：对齐常用投放/订单字段口径。
- **低成本部署**：本地即可运行，易于中小团队试用。
- **可扩展商业化**：可对接平台拉数、报告订阅、行业模版。

## 系统架构

![Architecture](./docs/architecture.png)

## 流程图

![Flow](./docs/flow.png)

## 页面截图

![Import](./docs/ui-import.png)
![Strategy](./docs/ui-strategy.png)
![Compare](./docs/ui-compare.png)

## 数据字典

### ad_log（投放日志）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| ad_id | string | 广告或活动 ID |
| impressions | int | 展示量 |
| clicks | int | 点击量 |
| date | datetime | 日期 |
| spend | float | 消耗（可选） |
| gmv | float | GMV（可选） |
| conversions | int | 转化数（可选） |

### orders（订单）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| order_id | string | 订单 ID |
| user_id | string | 用户 ID |
| amount | float | 订单金额（或 gmv） |
| order_date | datetime | 订单日期 |
| gross_profit | float | 毛利（可选） |
| refund_orders | int | 退款订单数（可选） |
| is_refund | bool | 是否退款（可选） |

## 指标口径

- **CTR** = clicks / impressions  
- **CVR** = orders / clicks（可配置 conversions / clicks）  
- **CPA** = spend / orders  
- **ROI_GP** = gross_profit / spend（若无 gross_profit，用 gmv * margin_rate）  
- **退款率** = refund_orders / total_orders

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
- `samples/ad_log_100.csv`
- `samples/orders_100.csv`
- `samples/metrics_request.json`
- `samples/compare_request.json`

使用文档：
- `docs/USAGE.md`

## Windows 快速开始

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

## Docker 部署（多容器）

```powershell
docker compose up --build
```

前端/后端地址：
- `http://localhost:3000`
- `http://localhost:5001`

本地后端（host）覆盖：

```powershell
docker compose -f docker-compose.yml -f docker-compose.override.local.yml up --build
```

## 3 分钟演示流程

1) 上传样例 CSV（生成 dataset_id）

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

2) 策略对比（使用 samples 请求模板）

先编辑 `samples/compare_request.json`，将 `dataset_id` 改为上一步返回值。

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/strategy/compare" `
  -H "Content-Type: application/json" `
  -d "@samples/compare_request.json"
```

3) 导出报告

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

接口返回 `download_url` 后，在浏览器打开：

```
http://localhost:5001/api/v1/adsim/report/download/<report_id>
```

## 目录结构

```
AdSim/
├─ backend/                 # 后端（Flask）
├─ frontend/                # 前端（Vite + Vue）
├─ samples/                 # 样例数据与请求
├─ docs/                    # 参赛文档与说明
├─ static/                  # 静态图片
└─ README.md
```

说明：`data_store/`、`cache/`、`reports/` 为运行时产物，运行后自动生成，不建议入库。

## 常见问题

### 1) 端口占用

- 前端端口 3000 被占用时，Vite 会自动切换到 3001/3002。
- 后端 5001 被占用时，请先关闭占用进程或修改环境变量 `FLASK_PORT`。

### 2) .env 配置

后端依赖 `.env` 中的外部服务配置，模板见：`.env.example`。  
若仅演示 Adsim 数据链路，可先保持默认并不调用外部 LLM 相关功能。

### 3) 依赖安装失败

- 请确认 Node 版本 `>=18`，Python `>=3.11`。
- 推荐使用 `npm run setup:all` 一键安装。
- 若后端依赖失败，可尝试：

```powershell
cd backend
uv sync
```

## 致谢

本项目基于开源项目二次开发：  
https://github.com/666ghj/MiroFish
