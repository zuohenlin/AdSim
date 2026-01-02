# Adsim

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](./package.json)

面向“三创赛-商务大数据分析实战赛”的电商活动投放策略预演系统。  
以最小样例复现 A/B/C 策略差异，输出可解释证据、区间估计与可打印报告。

![Adsim Logo](./static/image/adsim_logo.png)

## 目录

- [项目定位与核心闭环](#项目定位与核心闭环)
- [核心能力与差异化](#核心能力与差异化)
- [系统模式说明](#系统模式说明)
- [启动与访问（交互脚本）](#启动与访问交互脚本)
- [3分钟演示流程](#3分钟演示流程)
- [Adsim Insight → Adsim 联动流程](#adsim-insight--adsim-联动流程)
- [前端页面与路由入口](#前端页面与路由入口)
- [主要API](#主要api)
- [数据规范与指标口径](#数据规范与指标口径)
- [系统架构与目录结构](#系统架构与目录结构)
- [同类方案对比](#同类方案对比)
- [项目创新点/创意点/创业点](#项目创新点创意点创业点)
- [截图与素材](#截图与素材)
- [合规与第三方说明](#合规与第三方说明)
- [常见问题](#常见问题)
- [自检清单](#自检清单)

## 项目定位与核心闭环

**定位**：电商活动投放策略预演与决策报告系统。  
**闭环**：导入数据 → 指标计算 → 策略对比 → 证据卡 → 报告导出

## 核心能力与差异化

- **可解释对比**：指标 + 驱动因素 + 证据卡，便于答辩说明“为什么”。  
- **区间估计**：给出波动区间，降低单点结论风险。  
- **3分钟可演示**：上传样例→策略对比→导出报告。  
- **离线可跑**：Adsim 数据链路无需外部 LLM，可稳定演示。  
- **报告可打印**：导出 HTML 报告，适配现场展示与评分。  

## 系统模式说明

- **Adsim 数据链路**：投放/订单数据驱动的策略对比与报告导出（可离线演示）。  
- **原始仿真入口**：文本/文件驱动的群体智能仿真（需要 LLM 配置）。  
- **Adsim Insight（基于 BettaFish）**：可选的舆情/文本分析模块，非比赛主演示必需。  

## 启动与访问（交互脚本）

> 推荐使用交互脚本，一次性完成“启动选择 + 入口提示 + 端口检查”。

### 环境要求

- Node.js 18+  
- Python 3.11+  
- uv（Python 包管理器）  
- Docker（可选，用于 Adsim Insight）

### 安装依赖

```powershell
cd .
npm run setup:all
```

建议：先复制并检查 `.env`，不使用外部 LLM 可保持默认值：  

```powershell
Copy-Item ".env.example" ".env"
```

可选：如需 Adsim Insight，请准备 `third_party/BettaFish/.env`（基于 `third_party/BettaFish/.env.example`，并填写相关 API Key）。

### 启动服务（推荐）

```powershell
./tools/run_all.ps1
```

脚本可选择：
- 同时启动 Adsim + Adsim Insight  
- 仅启动 Adsim  
- 仅启动 Adsim Insight  
- 状态检查 / 停止服务  

### 访问地址

- Adsim 前端：`http://localhost:3000`  
- Adsim 后端：`http://localhost:5001`  
- Adsim Insight（Flask）：`http://localhost:5000`  
- Adsim Insight（Streamlit）：`http://localhost:8501`  

### 健康检查

```powershell
curl.exe "http://localhost:5001/health"
```

期望输出：

```json
{"status":"ok","service":"Adsim Backend"}
```

### Adsim Insight（仅启动时的备用方式）

```powershell
docker compose -f docker-compose.bettafish.yml up --build
```

停止：

```powershell
docker compose -f docker-compose.bettafish.yml down
```

## 3分钟演示流程

> 以下流程使用 `samples/` 中的样例数据与模板，完全可离线演示。

### 方式A：前端页面（推荐演示）

1) 先用交互脚本启动服务：`./tools/run_all.ps1`  
2) 打开导入页：`/adsim/import`  
3) 上传 `samples/ad_log.csv` 与 `samples/orders.csv`  
4) 跳转策略配置页：`/adsim/strategy`  
5) 跳转对比页：`/adsim/compare`，查看 summary/曲线/证据卡  
6) 点击“导出报告”按钮，打开生成的报告  

### 方式B：API（PowerShell）

1) 导入数据（生成 dataset_id）

```powershell
curl.exe -X POST "http://localhost:5001/api/v1/adsim/data/upload" `
  -F "file=@samples/ad_log.csv" `
  -F "table_type=ad_log"
```

2) 策略对比（使用模板）

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
`http://localhost:5001/api/v1/adsim/report/download/<report_id>`

## Adsim Insight → Adsim 联动流程

目标：用 Adsim Insight 生成研究报告，再作为 Adsim 的“现实种子”输入，结合提示词进行预测/仿真。

流程：
1) 启动 Adsim Insight（交互脚本或 Docker Compose）  
2) 在 Adsim Insight 生成研究报告（HTML/MD/PDF）  
3) 打开 Adsim 首页，在“现实种子”上传该报告文件  
4) 输入“模拟提示词”，触发预测/仿真流程  

说明：此联动依赖外部 LLM 与联网能力，适合展示“舆情→策略预演”的完整闭环。

## 前端页面与路由入口

- 首页：`/`  
- 数据导入：`/adsim/import`  
- 策略配置：`/adsim/strategy`  
- 对比结果：`/adsim/compare`  

原始仿真入口（继承自 MiroFish）：  
- `/process/:projectId`  
- `/simulation/:simulationId`  
- `/simulation/:simulationId/start`  
- `/report/:reportId`  
- `/interaction/:reportId`  

## 主要API

- `GET /health`  
- `GET /api/v1/adsim/health`  
- `POST /api/v1/adsim/data/upload`  
- `POST /api/v1/adsim/metrics/compute`  
- `POST /api/v1/adsim/strategy/compare`  
- `POST /api/v1/adsim/report/export`  
- `GET /api/v1/adsim/report/download/{report_id}`  

## 数据规范与指标口径

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

### 指标口径

- **CTR** = clicks / impressions  
- **CVR** = orders / clicks（可配置 conversions / clicks）  
- **CPA** = spend / orders  
- **ROI_GP** = gross_profit / spend（若无 gross_profit，用 gmv * margin_rate）  
- **退款率** = refund_orders / total_orders  

## 系统架构与目录结构

### 架构（ASCII）

```
前端(Vite+Vue)  ->  Adsim API(Flask)  ->  数据处理/策略对比/报告导出
                         |
                         +-- 可选: Adsim Insight（BettaFish 子模块）
```

### 目录结构

```
AdSim/
├─ archive/                 # 归档的非比赛演示资源
├─ backend/                 # 后端（Flask）
├─ docs/                    # 参赛文档与说明
├─ frontend/                # 前端（Vite + Vue）
├─ samples/                 # 样例数据与请求
├─ static/                  # 静态图片
├─ third_party/             # 子模块（Adsim Insight 基于 BettaFish）
└─ tools/                   # 工具脚本
```

说明：`data_store/`、`cache/`、`reports/` 为运行时产物，运行后自动生成，不建议入库。

## 同类方案对比

| 方案类型 | 代表形态 | 功能覆盖 | 可解释性 | 预演/区间不确定性 | 部署成本 | 比赛适配度 | Adsim差异化 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 传统 BI 看板 | Tableau/PowerBI/自建报表 | 统计展示强 | 中 | 无 | 中 | 中 | Adsim 提供策略预演与证据卡 |
| 广告平台原生后台 | 投放平台后台能力抽象 | 投放数据强 | 低-中 | 无 | 高 | 中 | Adsim 可离线演示、可解释 |
| 通用营销归因工具 | 归因/分析产品 | 归因强 | 中 | 无 | 中-高 | 中 | Adsim 强在策略预演 |
| 预测模型 Demo | 学术/竞赛模型 | 预测强 | 低 | 无 | 低 | 低-中 | Adsim 提供闭环与报告 |

**核心差异**：策略预演、区间不确定性、证据卡解释、可一键生成报告、离线演示稳定。

## 项目创新点/创意点/创业点

### 创新点
- 以“策略对比 + 证据卡”替代单点指标，提升可解释性。  
- 引入区间估计，表达投放波动与风险。  
- 报告导出一键完成，适配答辩场景。  

### 创意点
- 以“3分钟闭环演示”组织流程，降低评审理解成本。  
- 交互脚本统一启动体验，降低上手门槛。  
- 可选引入 Adsim Insight，形成“数据+舆情”扩展空间。  

### 创业点
- 贴合电商投放真实流程，易于小团队落地。  
- 本地离线可跑，降低试用门槛。  
- 报告模板可作为商业化交付物。  

## 截图与素材

当前仓库已包含截图（如需更新，请替换对应文件）：  
- 导入页：`./docs/ui-import.png`  
- 策略页：`./docs/ui-strategy.png`  
- 对比页：`./docs/ui-compare.png`  
- 架构图：`./docs/architecture.png`  
- 流程图：`./docs/flow.png`  

![Import](./docs/ui-import.png)
![Strategy](./docs/ui-strategy.png)
![Compare](./docs/ui-compare.png)

## 合规与第三方说明

- 主仓库许可证：`./LICENSE`（AGPL-3.0）  
- Adsim Insight 基于 BettaFish，保留其原始 LICENSE：`./third_party/BettaFish/LICENSE`  
- Third-Party 说明：`./THIRD_PARTY_NOTICES.md`  

## 常见问题

### 1) 端口占用

- 前端 3000 被占用时，Vite 会自动切换到 3001/3002。  
- 后端 5001 被占用时，请关闭占用进程或修改环境变量 `FLASK_PORT`。  

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

## 自检清单

- `git status` 是否干净  
- `.gitignore` 是否忽略运行产物  
- `./tools/run_all.ps1` 是否可交互启动  
- `curl.exe "http://localhost:5001/health"` 是否返回 `ok`  
- `strategy/compare` 与 `report/export` 是否可用  
