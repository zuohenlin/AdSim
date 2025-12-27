# Adsim

![Adsim Logo](./static/image/adsim_logo.png)

面向“三创赛-商务大数据分析实战赛”的电商投放策略预演系统：  
用样例数据完成 A/B/C 策略对比，生成可打印报告。

## 目录

- [核心功能闭环](#核心功能闭环)
- [业务价值](#业务价值)
- [创新点](#创新点)
- [系统架构](#系统架构)
- [流程图](#流程图)
- [页面截图](#页面截图)
- [数据字典](#数据字典)
- [指标口径](#指标口径)
- [竞品对比](#竞品对比)
- [评分要点对照](#评分要点对照)
- [API 列表与 Samples](#api-列表与-samples)
- [Windows 快速开始](#windows-快速开始)
- [3 分钟演示流程](#3-分钟演示流程)
- [目录结构](#目录结构)
- [常见问题](#常见问题)
- [致谢](#致谢)

## 核心功能闭环

导入 -> 指标计算 -> 策略对比 -> 证据卡 -> 报告导出

## 两种模式

- **Adsim 数据链路**：面向投放数据、策略对比与报告导出。
- **原始仿真入口**：面向文本/文件驱动的群体智能仿真（继承自 MiroFish）。

## 业务价值

- **快速预演**：用最少数据构建可演示的策略对比闭环。
- **决策解释**：以证据卡形式输出驱动因素与风险点。
- **易复用**：明确 API 与样例数据，便于复现与答辩展示。

## 创新点

- **可解释对比**：不仅给出指标，还给出驱动因素与证据卡。
- **区间估计**：基于历史波动做区间而非单点结论。
- **演示友好**：3 分钟内完成上传、对比与报告导出。

## 系统架构

![Architecture](./docs/architecture.png)


## 流程图

![Flow](./docs/flow.png)


## 页面截图

![Import](./docs/ui-import.png)
![Strategy](./docs/ui-strategy.png)
![Compare](./docs/ui-compare.png)

> 图示为占位，可替换为实际页面截图。

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

> 以上字段与当前接口要求一致，缺失字段允许降级演示。

## 指标口径

- **CTR** = clicks / impressions  
- **CVR** = orders / clicks（可配置 conversions / clicks）  
- **CPA** = spend / orders  
- **ROI_GP** = gross_profit / spend（若无 gross_profit，用 gmv * margin_rate）  
- **退款率** = refund_orders / total_orders

> 所有指标均包含 0 除保护；缺表会降级输出并提示。

## 竞品对比

| 维度 | Adsim | 通用 BI 看板 | 传统投放复盘 |
| --- | --- | --- | --- |
| 目标 | 策略预演与决策辅助 | 数据展示 | 历史复盘 |
| 输出 | 策略对比 + 证据卡 + 报告 | 图表 | 复盘结论 |
| 可解释性 | 高（驱动因素 + 证据卡） | 中 | 低 |
| 演示速度 | 快（3 分钟闭环） | 中 | 慢 |
| 适配赛事 | 高 | 中 | 中 |

### A/B 测试平台（官方来源）

- [Optimizely Web Experimentation](https://www.optimizely.com/products/web-experimentation/)
- [VWO Testing](https://vwo.com/testing/)
- [AB Tasty Web Experimentation](https://www.abtasty.com/web-experimentation/)

### 分析平台（官方来源）

- [Google Analytics](https://analytics.google.com/analytics/web/)
- [Adobe Analytics](https://experienceleague.adobe.com/en/docs/analytics)
- [Mixpanel](https://mixpanel.com/)
- [Amplitude Analytics](https://amplitude.com/amplitude-analytics)

### 中国本土投放/生态平台（官方来源）

- [巨量引擎（OceanEngine）](https://www.oceanengine.com/)
- [腾讯广告](https://e.qq.com/)
- [阿里妈妈](https://www.alimama.com/)
- [京准通（京东营销平台）](https://jzt.jd.com/)
- [友盟+（统计分析与数据平台）](https://www.umeng.com/)

### 产品分析表（功能对比 + 适用场景）

| 产品类型 | 代表平台（官方） | 功能侧重点 | 适用场景 | 定价 | 部署形态 | 数据存储位置 | 合规证书 | 典型行业案例 | 集成难度 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 策略预演与报告 | Adsim（本项目） | 策略对比、证据卡、可打印报告 | 竞赛演示、教学复现、快速答辩 | 本地部署 | 本地 | 本地/自控环境 | 取决于部署环境 | 课堂演示、课程作业、答辩展示 | 低（API + Samples） |
| A/B 测试平台 | Optimizely、VWO、AB Tasty | 实验设计、流量分配、效果评估 | 线上产品/站点体验优化 | 商业订阅/企业定价 | 以平台公示为准 | 以平台公示为准 | 以平台公示为准 | 电商转化、内容推荐、注册转化 | 中（SDK/标签接入） |
| 行为/产品分析 | Google Analytics、Mixpanel、Amplitude、Adobe Analytics | 事件/漏斗/留存分析与归因 | 用户增长、转化分析、运营看板 | 商业订阅/企业定价 | 以平台公示为准 | 以平台公示为准 | 以平台公示为准 | SaaS 增长、App 活跃、内容运营 | 中（埋点/数据接入） |
| 投放平台（国内） | 巨量引擎、腾讯广告、阿里妈妈、京准通 | 媒体投放、账户管理与投放优化 | 广告投放与预算管理 | 平台规则与投放预算 | 以平台公示为准 | 以平台公示为准 | 以平台公示为准 | 电商促销、品牌曝光、本地生活 | 中高（账户/像素/回传） |
| 统计分析（国内） | 友盟+ | 全域统计分析与监测 | 国内站点/小程序/应用数据统计 | 商业订阅/企业定价 | 以平台公示为准 | 以平台公示为准 | 以平台公示为准 | App 运营、小程序分析、网站统计 | 中（SDK/数据接入） |

## 评分要点对照

| 评分关注点 | Adsim 对应能力 | 说明 |
| --- | --- | --- |
| 商业价值 | 策略对比 + 报告导出 | 支持投放决策与汇报 |
| 数据分析 | 指标口径 + 区间估计 | 输出可解释指标 |
| 创新性 | 证据卡 + 风险评分 | 结合可解释输出 |
| 可落地性 | API + Samples | 可快速复现演示 |
| 完整性 | 端到端闭环 | 导入到报告导出 |

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

如需分步安装：

```powershell
cd .

# 根目录与前端依赖
npm run setup

# 后端依赖（uv）
npm run setup:backend
```

### 启动服务

```powershell
cd .

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
