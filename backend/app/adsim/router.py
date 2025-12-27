"""
Adsim API 路由
"""

import json
import os
import uuid
import hashlib
import time
import random
import html as pyhtml
from datetime import datetime

import pandas as pd
from flask import Blueprint, jsonify, request, send_file

adsim_bp = Blueprint('adsim', __name__)

ALLOWED_TABLE_TYPES = {'ad_log', 'orders', 'traffic', 'users', 'reviews'}

REQUIRED_COLUMNS = {
    'ad_log': ['ad_id', 'impressions', 'clicks', 'date'],
    'orders': ['order_id', 'user_id', 'amount', 'order_date'],
    'traffic': ['user_id', 'session_id', 'page', 'timestamp'],
    'users': ['user_id', 'signup_date', 'country'],
    'reviews': ['review_id', 'user_id', 'rating', 'review_date'],
}

COLUMN_TYPES = {
    'ad_log': {
        'ad_id': 'string',
        'impressions': 'int',
        'clicks': 'int',
        'date': 'datetime',
    },
    'orders': {
        'order_id': 'string',
        'user_id': 'string',
        'amount': 'float',
        'order_date': 'datetime',
    },
    'traffic': {
        'user_id': 'string',
        'session_id': 'string',
        'page': 'string',
        'timestamp': 'datetime',
    },
    'users': {
        'user_id': 'string',
        'signup_date': 'datetime',
        'country': 'string',
    },
    'reviews': {
        'review_id': 'string',
        'user_id': 'string',
        'rating': 'float',
        'review_date': 'datetime',
    },
}


def _get_repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


def _safe_div(numerator: float, denominator: float) -> float:
    if not denominator:
        return 0.0
    return float(numerator) / float(denominator)


def _parse_time_range(time_range: dict | None) -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
    if not time_range:
        return None, None
    start = time_range.get('start')
    end = time_range.get('end')
    start_ts = pd.to_datetime(start, errors='coerce') if start else None
    end_ts = pd.to_datetime(end, errors='coerce') if end else None
    return start_ts, end_ts


def _filter_by_time(df: pd.DataFrame, time_col: str | None, start_ts, end_ts) -> pd.DataFrame:
    if not time_col or time_col not in df.columns:
        return df
    series = pd.to_datetime(df[time_col], errors='coerce')
    mask = pd.Series([True] * len(df))
    if start_ts is not None and pd.notna(start_ts):
        mask &= series >= start_ts
    if end_ts is not None and pd.notna(end_ts):
        mask &= series <= end_ts
    return df.loc[mask]


def _load_table(dataset_dir: str, table_type: str) -> pd.DataFrame | None:
    table_path = os.path.join(dataset_dir, f'{table_type}.parquet')
    if not os.path.exists(table_path):
        return None
    return pd.read_parquet(table_path)


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _ensure_samples():
    repo_root = _get_repo_root()
    samples_dir = os.path.join(repo_root, 'samples')
    os.makedirs(samples_dir, exist_ok=True)

    ad_log_path = os.path.join(samples_dir, 'ad_log.csv')
    orders_path = os.path.join(samples_dir, 'orders.csv')

    if not os.path.exists(ad_log_path):
        with open(ad_log_path, 'w', encoding='utf-8') as f:
            f.write('ad_id,impressions,clicks,date\n')
            f.write('ad_001,1200,45,2025-01-01\n')
            f.write('ad_002,800,30,2025-01-02\n')

    if not os.path.exists(orders_path):
        with open(orders_path, 'w', encoding='utf-8') as f:
            f.write('order_id,user_id,amount,order_date\n')
            f.write('ord_001,user_001,99.9,2025-01-03\n')
            f.write('ord_002,user_002,149.5,2025-01-04\n')


def _apply_mapping(df: pd.DataFrame, mapping_json: str | None) -> pd.DataFrame:
    if not mapping_json:
        return df
    try:
        mapping = json.loads(mapping_json)
    except json.JSONDecodeError:
        raise ValueError('mapping_json 不是有效的 JSON')
    if not isinstance(mapping, dict):
        raise ValueError('mapping_json 必须是对象')
    return df.rename(columns=mapping)


def _build_quality_report(df: pd.DataFrame, table_type: str) -> dict:
    required_cols = REQUIRED_COLUMNS.get(table_type, [])
    type_map = COLUMN_TYPES.get(table_type, {})

    missing_columns = [c for c in required_cols if c not in df.columns]
    null_counts = {c: int(df[c].isna().sum()) for c in df.columns}
    type_errors = {}

    for col, dtype in type_map.items():
        if col not in df.columns:
            continue
        series = df[col]
        if dtype == 'int':
            converted = pd.to_numeric(series, errors='coerce')
            type_errors[col] = int((series.notna() & converted.isna()).sum())
            df[col] = converted
        elif dtype == 'float':
            converted = pd.to_numeric(series, errors='coerce')
            type_errors[col] = int((series.notna() & converted.isna()).sum())
            df[col] = converted
        elif dtype == 'datetime':
            converted = pd.to_datetime(series, errors='coerce')
            type_errors[col] = int((series.notna() & converted.isna()).sum())
            df[col] = converted
        else:
            df[col] = series.astype('string')
            type_errors[col] = 0

    return {
        'table_type': table_type,
        'row_count': int(len(df)),
        'missing_required_columns': missing_columns,
        'null_counts': null_counts,
        'type_conversion_errors': type_errors,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
    }


def _load_cache(cache_dir: str, key: str) -> dict | None:
    cache_path = os.path.join(cache_dir, f'{key}.json')
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _save_cache(cache_dir: str, key: str, payload: dict) -> str:
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f'{key}.json')
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return cache_path


def _bootstrap_interval(values: list[float], iterations: int = 300) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], values[0]
    samples = []
    for _ in range(iterations):
        batch = [random.choice(values) for _ in range(len(values))]
        samples.append(sum(batch) / len(batch))
    samples.sort()
    low_idx = int(len(samples) * 0.1)
    high_idx = int(len(samples) * 0.9) - 1
    return samples[low_idx], samples[max(high_idx, low_idx)]


def _format_date(value) -> str | None:
    if value is None:
        return None
    try:
        ts = pd.to_datetime(value, errors='coerce')
    except Exception:
        return str(value)
    if pd.isna(ts):
        return None
    return ts.isoformat()


def _build_evidence_cards(drivers: list[dict], max_cards: int = 3) -> list[dict]:
    cards = []
    for driver in drivers[:max_cards]:
        cards.append({
            'title': driver.get('factor', '未知因素'),
            'insight': driver.get('note', ''),
            'impact': driver.get('impact', 'medium'),
        })
    if len(cards) < 2:
        cards.append({
            'title': '数据覆盖',
            'insight': '样本量有限，指标波动可能偏大。',
            'impact': 'low',
        })
    return cards[:5]


def _format_float(value, digits: int = 4) -> str:
    if value is None:
        return '-'
    try:
        return f'{float(value):.{digits}f}'
    except (ValueError, TypeError):
        return '-'


def _render_line_svg(points: list[dict]) -> str:
    if not points:
        return '<div class="empty">暂无曲线数据</div>'
    values = [float(p.get('clicks', 0) or 0) for p in points]
    max_val = max(values) if values else 1
    min_val = min(values) if values else 0
    width = 640
    height = 200
    coords = []
    for idx, val in enumerate(values):
        x = (idx / max(len(values) - 1, 1)) * width
        y = height - ((val - min_val) / max(max_val - min_val, 1)) * height
        coords.append(f'{x:.2f},{y:.2f}')
    polyline = ' '.join(coords)
    return (
        f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none">'
        f'<polyline points="{polyline}" fill="none" stroke="#111" stroke-width="2"/>'
        '</svg>'
    )


def _render_report_html(compare_result: dict, selected_strategy: str) -> str:
    summary_table = compare_result.get('summary_table') or []
    time_series = compare_result.get('time_series') or []
    drivers = compare_result.get('drivers') or []
    evidence_cards = compare_result.get('evidence_cards') or []

    summary_row = next(
        (row for row in summary_table if row.get('strategy') == selected_strategy),
        summary_table[0] if summary_table else None
    )

    summary_block = '<p>暂无摘要数据</p>'
    if summary_row:
        summary_block = (
            '<div class="summary-grid">'
            f'<div><span>策略</span><strong>{pyhtml.escape(str(summary_row.get("strategy", "-")))}</strong></div>'
            f'<div><span>CTR</span><strong>{_format_float(summary_row.get("ctr"))}</strong></div>'
            f'<div><span>CVR</span><strong>{_format_float(summary_row.get("cvr"))}</strong></div>'
            f'<div><span>CPA</span><strong>{_format_float(summary_row.get("cpa"))}</strong></div>'
            f'<div><span>ROI_GP</span><strong>{_format_float(summary_row.get("roi_gp"))}</strong></div>'
            f'<div><span>退款率</span><strong>{_format_float(summary_row.get("refund_rate"))}</strong></div>'
            '</div>'
        )

    table_rows = []
    for row in summary_table:
        table_rows.append(
            '<tr>'
            f'<td>{pyhtml.escape(str(row.get("strategy", "-")))}</td>'
            f'<td>{pyhtml.escape(str(row.get("window_start", "-")))}</td>'
            f'<td>{pyhtml.escape(str(row.get("window_end", "-")))}</td>'
            f'<td>{_format_float(row.get("ctr"))}</td>'
            f'<td>{_format_float(row.get("cvr"))}</td>'
            f'<td>{_format_float(row.get("cpa"))}</td>'
            f'<td>{_format_float(row.get("roi_gp"))}</td>'
            f'<td>{_format_float(row.get("refund_rate"))}</td>'
            '</tr>'
        )
    table_html = (
        '<table><thead><tr>'
        '<th>策略</th><th>开始</th><th>结束</th><th>CTR</th><th>CVR</th><th>CPA</th><th>ROI_GP</th><th>退款率</th>'
        '</tr></thead><tbody>'
        + ''.join(table_rows) +
        '</tbody></table>'
    )

    drivers_html = ''.join(
        f'<li><strong>{pyhtml.escape(str(d.get("factor", "-")))}</strong>：{pyhtml.escape(str(d.get("note", "")))}</li>'
        for d in drivers
    ) or '<li>暂无风险点</li>'

    evidence_html = ''.join(
        '<div class="card">'
        f'<h4>{pyhtml.escape(str(c.get("title", "-")))}</h4>'
        f'<p>{pyhtml.escape(str(c.get("insight", "")))}</p>'
        f'<span class="tag">{pyhtml.escape(str(c.get("impact", "")))}</span>'
        '</div>'
        for c in evidence_cards
    ) or '<p>暂无证据卡</p>'

    action_items = []
    for d in drivers:
        factor = str(d.get('factor', '')).strip()
        if factor:
            action_items.append(f'<li>针对 {pyhtml.escape(factor)} 制定优化动作。</li>')
    if not action_items:
        action_items.append('<li>补充订单与退款数据，提高评估完整性。</li>')

    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Adsim 策略对比报告</title>
  <style>
    body {{ font-family: 'JetBrains Mono','Noto Sans SC',sans-serif; margin: 0; color: #111; background: #f7f2ea; }}
    .page {{ padding: 32px 7vw 48px; }}
    h1 {{ margin-bottom: 8px; font-size: 28px; }}
    h2 {{ margin-top: 28px; }}
    .meta {{ color: #6b6155; }}
    .panel {{ background: #fff; border: 1px solid #e5d9c8; border-radius: 14px; padding: 18px; margin-top: 16px; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }}
    .summary-grid span {{ display: block; color: #7d6f61; font-size: 12px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border-bottom: 1px solid #eadfcf; padding: 8px; text-align: left; }}
    .chart {{ background: #fffaf2; border: 1px solid #eadfcf; border-radius: 12px; padding: 12px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid #eadfcf; border-radius: 12px; padding: 12px; background: #f9f2e7; }}
    .tag {{ display: inline-block; margin-top: 8px; padding: 2px 8px; border-radius: 999px; background: #111; color: #fff; font-size: 12px; }}
    ul {{ padding-left: 18px; }}
    .print {{ margin-top: 16px; }}
    @media print {{ body {{ background: #fff; }} .print {{ display: none; }} }}
  </style>
</head>
<body>
  <div class="page">
    <h1>Adsim 策略对比报告</h1>
    <div class="meta">策略：{pyhtml.escape(selected_strategy)} · 生成时间：{datetime.utcnow().isoformat()}Z</div>

    <section class="panel">
      <h2>摘要</h2>
      {summary_block}
    </section>

    <section class="panel">
      <h2>对比表</h2>
      {table_html}
    </section>

    <section class="panel">
      <h2>曲线</h2>
      <div class="chart">{_render_line_svg(time_series)}</div>
    </section>

    <section class="panel">
      <h2>风险点</h2>
      <ul>{drivers_html}</ul>
    </section>

    <section class="panel">
      <h2>证据卡</h2>
      <div class="cards">{evidence_html}</div>
    </section>

    <section class="panel">
      <h2>行动清单</h2>
      <ul>{''.join(action_items)}</ul>
    </section>

    <div class="print">
      <button onclick="window.print()">打印报告</button>
    </div>
  </div>
</body>
</html>
"""


@adsim_bp.get('/health')
def health():
    return {'ok': True, 'service': 'adsim'}


@adsim_bp.post('/data/upload')
def upload_data():
    try:
        _ensure_samples()

        table_type = request.form.get('table_type', '').strip()
        if table_type not in ALLOWED_TABLE_TYPES:
            return jsonify({
                'error': 'table_type 无效',
                'allowed': sorted(ALLOWED_TABLE_TYPES),
            }), 400

        file_storage = request.files.get('file')
        if not file_storage or not file_storage.filename:
            return jsonify({'error': '必须上传 file'}), 400

        mapping_json = request.form.get('mapping_json')

        df = pd.read_csv(file_storage)
        df = _apply_mapping(df, mapping_json)

        required_cols = REQUIRED_COLUMNS.get(table_type, [])
        missing_required = [c for c in required_cols if c not in df.columns]
        quality_report = _build_quality_report(df, table_type)

        dataset_id = uuid.uuid4().hex
        repo_root = _get_repo_root()
        dataset_dir = os.path.join(repo_root, 'data_store', dataset_id)
        os.makedirs(dataset_dir, exist_ok=True)

        parquet_path = os.path.join(dataset_dir, f'{table_type}.parquet')
        df.to_parquet(parquet_path, index=False)

        quality_path = os.path.join(dataset_dir, f'quality_{table_type}.json')
        with open(quality_path, 'w', encoding='utf-8') as f:
            json.dump(quality_report, f, ensure_ascii=False, indent=2)

        sample_rows = df.head(5).to_dict(orient='records')

        return jsonify({
            'dataset_id': dataset_id,
            'detected_columns': list(df.columns),
            'missing_required_columns': missing_required,
            'sample_rows': sample_rows,
            'saved_path': parquet_path,
        })
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'上传失败: {exc}'}), 500


@adsim_bp.post('/metrics/compute')
def compute_metrics():
    try:
        payload = request.get_json(silent=True) or {}
        dataset_id = (payload.get('dataset_id') or '').strip()
        time_range = payload.get('time_range') or {}
        group_by = payload.get('group_by') or []
        cvr_numerator = (payload.get('cvr_numerator') or 'orders').strip()
        margin_rate = float(payload.get('margin_rate', 0.3))

        if not dataset_id:
            return jsonify({'error': 'dataset_id is required'}), 400

        dataset_dir = os.path.join(_get_repo_root(), 'data_store', dataset_id)
        if not os.path.isdir(dataset_dir):
            return jsonify({'error': 'dataset_id not found'}), 404

        start_ts, end_ts = _parse_time_range(time_range)

        ad_log = _load_table(dataset_dir, 'ad_log')
        orders = _load_table(dataset_dir, 'orders')

        missing_tables = []
        available_tables = []
        if ad_log is None:
            missing_tables.append('ad_log')
        else:
            available_tables.append('ad_log')
        if orders is None:
            missing_tables.append('orders')
        else:
            available_tables.append('orders')

        time_cols = {
            'ad_log': 'date',
            'orders': 'order_date',
        }

        if ad_log is not None:
            ad_log = _filter_by_time(ad_log, time_cols['ad_log'], start_ts, end_ts)
        if orders is not None:
            orders = _filter_by_time(orders, time_cols['orders'], start_ts, end_ts)

        base_group_by = []
        if group_by:
            if ad_log is not None:
                base_group_by = [c for c in group_by if c in ad_log.columns]
            elif orders is not None:
                base_group_by = [c for c in group_by if c in orders.columns]

        metrics_rows = []

        ad_log_agg = None
        if ad_log is not None:
            spend_col = _pick_column(ad_log, ['spend', 'cost'])
            gmv_col = _pick_column(ad_log, ['gmv'])
            conv_col = _pick_column(ad_log, ['conversions'])
            agg_map = {
                'impressions': ('impressions', 'sum') if 'impressions' in ad_log.columns else None,
                'clicks': ('clicks', 'sum') if 'clicks' in ad_log.columns else None,
                'spend': (spend_col, 'sum') if spend_col else None,
                'gmv': (gmv_col, 'sum') if gmv_col else None,
                'conversions': (conv_col, 'sum') if conv_col else None,
            }
            agg_map = {k: v for k, v in agg_map.items() if v is not None}
            if base_group_by:
                ad_log_agg = ad_log.groupby(base_group_by, dropna=False).agg(**{
                    k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                }).reset_index()
            else:
                ad_log_agg = ad_log.agg(**{
                    k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                }).to_frame().T

        orders_agg = None
        orders_groupable = False
        if orders is not None:
            orders_groupable = all(c in orders.columns for c in base_group_by) if base_group_by else True
            if orders_groupable:
                gmv_col = _pick_column(orders, ['gmv', 'amount', 'order_amount'])
                gp_col = _pick_column(orders, ['gross_profit'])
                conv_col = _pick_column(orders, ['conversions'])
                refund_col = _pick_column(orders, ['refund_orders', 'refund_count', 'refunds'])
                refund_flag_col = _pick_column(orders, ['is_refund', 'refunded', 'refund'])

                def _refund_agg(series: pd.Series) -> float:
                    return float(series.fillna(0).sum())

                def _refund_flag_agg(series: pd.Series) -> float:
                    return float(series.fillna(False).astype(bool).sum())

                agg_map = {
                    'orders': ('order_id', 'count') if 'order_id' in orders.columns else None,
                    'gmv': (gmv_col, 'sum') if gmv_col else None,
                    'gross_profit': (gp_col, 'sum') if gp_col else None,
                    'conversions': (conv_col, 'sum') if conv_col else None,
                    'refund_orders': (refund_col, _refund_agg) if refund_col else None,
                    'refund_orders_flag': (refund_flag_col, _refund_flag_agg) if refund_flag_col else None,
                }
                agg_map = {k: v for k, v in agg_map.items() if v is not None}
                if base_group_by:
                    orders_agg = orders.groupby(base_group_by, dropna=False).agg(**{
                        k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                    }).reset_index()
                else:
                    orders_agg = orders.agg(**{
                        k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                    }).to_frame().T

        if ad_log_agg is not None:
            metrics_rows = ad_log_agg.copy()
        elif orders_agg is not None:
            metrics_rows = orders_agg.copy()
        else:
            metrics_rows = pd.DataFrame()

        if not metrics_rows.empty and orders_agg is not None and orders_groupable:
            if base_group_by:
                metrics_rows = metrics_rows.merge(orders_agg, on=base_group_by, how='left')
            else:
                metrics_rows = metrics_rows.merge(orders_agg, how='left')

        if metrics_rows.empty and orders_agg is not None:
            metrics_rows = orders_agg.copy()

        metrics_table = []
        for _, row in metrics_rows.iterrows():
            impressions = float(row.get('impressions', 0) or 0)
            clicks = float(row.get('clicks', 0) or 0)
            spend = float(row.get('spend', 0) or 0)
            orders_count = float(row.get('orders', 0) or 0)
            conversions = float(row.get('conversions', 0) or 0)
            gmv = float(row.get('gmv', 0) or 0)
            gross_profit = float(row.get('gross_profit', 0) or 0)

            if not gross_profit and gmv and margin_rate:
                gross_profit = gmv * margin_rate

            if cvr_numerator == 'conversions' and conversions:
                cvr_num = conversions
            else:
                cvr_num = orders_count

            refund_orders = float(row.get('refund_orders', 0) or 0)
            if not refund_orders:
                refund_orders = float(row.get('refund_orders_flag', 0) or 0)

            ctr = _safe_div(clicks, impressions)
            cvr = _safe_div(cvr_num, clicks)
            cpa = _safe_div(spend, orders_count)
            roi_gp = _safe_div(gross_profit, spend)
            refund_rate = _safe_div(refund_orders, orders_count)

            record = {
                'impressions': impressions or None,
                'clicks': clicks or None,
                'orders': orders_count or None,
                'conversions': conversions or None,
                'spend': spend or None,
                'gmv': gmv or None,
                'gross_profit': gross_profit or None,
                'ctr': ctr,
                'cvr': cvr,
                'cpa': cpa,
                'roi_gp': roi_gp,
                'refund_rate': refund_rate,
            }
            if base_group_by:
                for col in base_group_by:
                    record[col] = row.get(col)
            metrics_table.append(record)

        summary = {
            'dataset_id': dataset_id,
            'time_range': time_range,
            'group_by': base_group_by,
            'available_tables': available_tables,
            'missing_tables': missing_tables,
            'notes': [],
        }

        if not available_tables:
            summary['notes'].append('no tables available for metrics')
        if orders is None:
            summary['notes'].append('orders table missing, orders-based metrics may be empty')
        if ad_log is None:
            summary['notes'].append('ad_log table missing, ad delivery metrics may be empty')
        if group_by and not base_group_by:
            summary['notes'].append('group_by columns not found in available tables')
        if orders is not None and base_group_by and not orders_groupable:
            summary['notes'].append('orders table missing group_by columns, metrics merged from ad_log only')

        return jsonify({
            'metrics_table': metrics_table,
            'summary': summary,
        })
    except Exception as exc:
        return jsonify({'error': f'metrics compute failed: {exc}'}), 500


@adsim_bp.post('/strategy/compare')
def compare_strategy():
    try:
        payload = request.get_json(silent=True) or {}
        dataset_id = (payload.get('dataset_id') or '').strip()
        window = payload.get('window') or {}
        strategies = payload.get('strategies') or []
        demo_mode = bool(payload.get('demo_mode', False))
        mode = (payload.get('mode') or 'baseline').strip()

        if mode != 'baseline':
            return jsonify({'error': 'only baseline mode is supported'}), 400
        if not dataset_id:
            return jsonify({'error': 'dataset_id is required'}), 400
        if not strategies:
            return jsonify({'error': 'strategies is required'}), 400

        cache_key = hashlib.md5(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()
        cache_dir = os.path.join(_get_repo_root(), 'cache')
        cached = _load_cache(cache_dir, cache_key)
        if cached:
            cached['cache_hit'] = True
            return jsonify(cached)

        dataset_dir = os.path.join(_get_repo_root(), 'data_store', dataset_id)
        if not os.path.isdir(dataset_dir):
            return jsonify({'error': 'dataset_id not found'}), 404

        start_ts, end_ts = _parse_time_range(window)
        ad_log = _load_table(dataset_dir, 'ad_log')
        orders = _load_table(dataset_dir, 'orders')

        missing_tables = []
        available_tables = []
        if ad_log is None:
            missing_tables.append('ad_log')
        else:
            available_tables.append('ad_log')
        if orders is None:
            missing_tables.append('orders')
        else:
            available_tables.append('orders')

        if ad_log is not None:
            ad_log = _filter_by_time(ad_log, 'date', start_ts, end_ts)
        if orders is not None:
            orders = _filter_by_time(orders, 'order_date', start_ts, end_ts)

        spend_col = _pick_column(ad_log, ['spend', 'cost']) if ad_log is not None else None
        gmv_col_orders = _pick_column(orders, ['gmv', 'amount', 'order_amount']) if orders is not None else None
        gross_profit_col = _pick_column(orders, ['gross_profit']) if orders is not None else None
        refund_col = _pick_column(orders, ['refund_orders', 'refund_count', 'refunds']) if orders is not None else None
        refund_flag_col = _pick_column(orders, ['is_refund', 'refunded', 'refund']) if orders is not None else None

        ad_daily = None
        if ad_log is not None:
            ad_daily = ad_log.copy()
            if 'date' in ad_daily.columns:
                ad_daily['date'] = pd.to_datetime(ad_daily['date'], errors='coerce')
            agg_map = {
                'impressions': ('impressions', 'sum') if 'impressions' in ad_daily.columns else None,
                'clicks': ('clicks', 'sum') if 'clicks' in ad_daily.columns else None,
                'spend': (spend_col, 'sum') if spend_col else None,
            }
            agg_map = {k: v for k, v in agg_map.items() if v is not None}
            if agg_map:
                ad_daily = ad_daily.groupby('date', dropna=False).agg(**{
                    k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                }).reset_index()

        orders_daily = None
        if orders is not None:
            orders_daily = orders.copy()
            if 'order_date' in orders_daily.columns:
                orders_daily['order_date'] = pd.to_datetime(orders_daily['order_date'], errors='coerce')
            agg_map = {
                'orders': ('order_id', 'count') if 'order_id' in orders_daily.columns else None,
                'gmv': (gmv_col_orders, 'sum') if gmv_col_orders else None,
                'gross_profit': (gross_profit_col, 'sum') if gross_profit_col else None,
                'refund_orders': (refund_col, 'sum') if refund_col else None,
                'refund_orders_flag': (refund_flag_col, lambda s: float(s.fillna(False).astype(bool).sum())) if refund_flag_col else None,
            }
            agg_map = {k: v for k, v in agg_map.items() if v is not None}
            if agg_map:
                orders_daily = orders_daily.groupby('order_date', dropna=False).agg(**{
                    k: pd.NamedAgg(column=v[0], aggfunc=v[1]) for k, v in agg_map.items()
                }).reset_index().rename(columns={'order_date': 'date'})

        merged_daily = None
        if ad_daily is not None and orders_daily is not None:
            merged_daily = ad_daily.merge(orders_daily, on='date', how='left')
        elif ad_daily is not None:
            merged_daily = ad_daily.copy()
        elif orders_daily is not None:
            merged_daily = orders_daily.copy()
        else:
            merged_daily = pd.DataFrame()

        if merged_daily.empty:
            result = {
                'summary_table': [],
                'time_series': [],
                'drivers': [],
                'evidence_cards': [],
                'cache_hit': False,
                'missing_tables': missing_tables,
                'notes': ['no data available for requested window'],
            }
            _save_cache(cache_dir, cache_key, result)
            return jsonify(result)

        margin_rate = float(payload.get('margin_rate', 0.3))
        merged_daily['ctr'] = merged_daily.apply(
            lambda r: _safe_div(r.get('clicks', 0) or 0, r.get('impressions', 0) or 0), axis=1
        )
        merged_daily['cvr'] = merged_daily.apply(
            lambda r: _safe_div(r.get('orders', 0) or 0, r.get('clicks', 0) or 0), axis=1
        )
        merged_daily['roi_gp'] = merged_daily.apply(
            lambda r: _safe_div(
                (r.get('gross_profit', 0) or (r.get('gmv', 0) or 0) * margin_rate),
                r.get('spend', 0) or 0
            ), axis=1
        )
        merged_daily['refund_rate'] = merged_daily.apply(
            lambda r: _safe_div(
                r.get('refund_orders', 0) or r.get('refund_orders_flag', 0) or 0,
                r.get('orders', 0) or 0
            ), axis=1
        )
        merged_daily['cpa'] = merged_daily.apply(
            lambda r: _safe_div(r.get('spend', 0) or 0, r.get('orders', 0) or 0), axis=1
        )

        ctr_vals = merged_daily['ctr'].dropna().tolist()
        cvr_vals = merged_daily['cvr'].dropna().tolist()
        roi_vals = merged_daily['roi_gp'].dropna().tolist()
        cpa_vals = merged_daily['cpa'].dropna().tolist()
        refund_vals = merged_daily['refund_rate'].dropna().tolist()

        iterations = 200 if demo_mode else 600
        ctr_ci = _bootstrap_interval(ctr_vals, iterations=iterations)
        cvr_ci = _bootstrap_interval(cvr_vals, iterations=iterations)
        roi_ci = _bootstrap_interval(roi_vals, iterations=iterations)
        cpa_ci = _bootstrap_interval(cpa_vals, iterations=iterations)
        refund_ci = _bootstrap_interval(refund_vals, iterations=iterations)

        total_impressions = float(merged_daily['impressions'].fillna(0).sum()) if 'impressions' in merged_daily.columns else 0.0
        total_clicks = float(merged_daily['clicks'].fillna(0).sum()) if 'clicks' in merged_daily.columns else 0.0
        total_orders = float(merged_daily['orders'].fillna(0).sum()) if 'orders' in merged_daily.columns else 0.0
        total_spend = float(merged_daily['spend'].fillna(0).sum()) if 'spend' in merged_daily.columns else 0.0
        total_gmv = float(merged_daily['gmv'].fillna(0).sum()) if 'gmv' in merged_daily.columns else 0.0
        total_gp = float(merged_daily['gross_profit'].fillna(0).sum()) if 'gross_profit' in merged_daily.columns else 0.0
        if not total_gp and total_gmv:
            total_gp = total_gmv * margin_rate

        summary_table = []
        for strat in strategies:
            summary_table.append({
                'strategy': strat,
                'window_start': window.get('start'),
                'window_end': window.get('end'),
                'ctr': _safe_div(total_clicks, total_impressions),
                'ctr_ci': {'low': ctr_ci[0], 'high': ctr_ci[1]},
                'cvr': _safe_div(total_orders, total_clicks),
                'cvr_ci': {'low': cvr_ci[0], 'high': cvr_ci[1]},
                'cpa': _safe_div(total_spend, total_orders),
                'cpa_ci': {'low': cpa_ci[0], 'high': cpa_ci[1]},
                'roi_gp': _safe_div(total_gp, total_spend),
                'roi_gp_ci': {'low': roi_ci[0], 'high': roi_ci[1]},
                'refund_rate': _safe_div(
                    float(merged_daily['refund_rate'].fillna(0).sum()),
                    max(len(merged_daily), 1)
                ),
                'refund_rate_ci': {'low': refund_ci[0], 'high': refund_ci[1]},
            })

        time_series = []
        for _, row in merged_daily.iterrows():
            time_series.append({
                'date': _format_date(row.get('date')),
                'impressions': float(row.get('impressions', 0) or 0),
                'clicks': float(row.get('clicks', 0) or 0),
                'orders': float(row.get('orders', 0) or 0),
                'spend': float(row.get('spend', 0) or 0),
                'gmv': float(row.get('gmv', 0) or 0),
                'gross_profit': float(row.get('gross_profit', 0) or 0),
                'ctr': row.get('ctr', 0),
                'cvr': row.get('cvr', 0),
                'cpa': row.get('cpa', 0),
                'roi_gp': row.get('roi_gp', 0),
                'refund_rate': row.get('refund_rate', 0),
            })

        drivers = []
        if refund_vals:
            drivers.append({
                'factor': '退款率',
                'impact': 'high' if sum(refund_vals) / len(refund_vals) > 0.1 else 'medium',
                'note': '退款率偏高可能侵蚀净利润。',
            })
        if roi_vals:
            roi_vol = _bootstrap_interval(roi_vals, iterations=100)
            drivers.append({
                'factor': 'ROI波动',
                'impact': 'high' if roi_vol[1] - roi_vol[0] > 0.5 else 'medium',
                'note': 'ROI区间较宽，收益不确定性较高。',
            })
        if cpa_vals:
            cpa_avg = sum(cpa_vals) / len(cpa_vals)
            drivers.append({
                'factor': 'CPA异常',
                'impact': 'high' if cpa_avg > 100 else 'medium',
                'note': 'CPA偏高可能压缩投放规模。',
            })

        if not drivers:
            drivers.append({
                'factor': '数据完整性',
                'impact': 'low',
                'note': '缺少关键表，指标受限。',
            })

        evidence_cards = _build_evidence_cards(drivers, max_cards=3)

        result = {
            'summary_table': summary_table,
            'time_series': time_series,
            'drivers': drivers,
            'evidence_cards': evidence_cards,
            'cache_hit': False,
            'missing_tables': missing_tables,
            'notes': [],
        }

        if missing_tables:
            result['notes'].append(f'missing tables: {", ".join(missing_tables)}')
        if demo_mode:
            result['notes'].append('demo_mode enabled, using faster estimation')

        _save_cache(cache_dir, cache_key, result)
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': f'compare failed: {exc}'}), 500


@adsim_bp.post('/report/export')
def export_report():
    try:
        payload = request.get_json(silent=True) or {}
        compare_result = payload.get('compare_result')
        selected_strategy = (payload.get('selected_strategy') or '').strip()
        if not compare_result or not selected_strategy:
            return jsonify({'error': 'compare_result and selected_strategy are required'}), 400

        report_id = uuid.uuid4().hex
        reports_dir = os.path.join(_get_repo_root(), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        report_path = os.path.join(reports_dir, f'{report_id}.html')

        html_content = _render_report_html(compare_result, selected_strategy)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        download_url = f'/api/v1/adsim/report/download/{report_id}'
        return jsonify({
            'report_id': report_id,
            'download_url': download_url
        })
    except Exception as exc:
        return jsonify({'error': f'export failed: {exc}'}), 500


@adsim_bp.get('/report/download/<report_id>')
def download_report(report_id: str):
    reports_dir = os.path.join(_get_repo_root(), 'reports')
    report_path = os.path.join(reports_dir, f'{report_id}.html')
    if not os.path.exists(report_path):
        return jsonify({'error': 'report not found'}), 404
    return send_file(report_path, mimetype='text/html')
