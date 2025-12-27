<template>
  <div class="page">
    <header class="page-header">
      <div>
        <p class="eyebrow">Adsim · 对比结果</p>
        <h1>策略表现对比与洞察</h1>
        <p class="sub">
          展示 summary_table、日度曲线、驱动因素与证据卡片，并支持导出报告。
        </p>
      </div>
      <nav class="page-nav">
        <RouterLink class="nav-link" to="/adsim/import">数据导入</RouterLink>
        <RouterLink class="nav-link" to="/adsim/strategy">策略配置</RouterLink>
      </nav>
    </header>

    <section class="panel" v-if="!compareData">
      <p class="muted">暂无对比结果，请先完成策略配置。</p>
    </section>

    <section v-if="compareData" class="panel">
      <div class="header-row">
        <h2>Summary Table</h2>
        <button class="btn ghost" @click="exportReport">导出报告</button>
      </div>
      <div class="table-wrap">
        <table v-if="compareData.summary_table?.length">
          <thead>
            <tr>
              <th>策略</th>
              <th>区间</th>
              <th>CTR</th>
              <th>CVR</th>
              <th>CPA</th>
              <th>ROI_GP</th>
              <th>退款率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in compareData.summary_table" :key="row.strategy">
              <td>{{ row.strategy }}</td>
              <td>{{ row.window_start }} ~ {{ row.window_end }}</td>
              <td>{{ formatMetric(row.ctr) }}</td>
              <td>{{ formatMetric(row.cvr) }}</td>
              <td>{{ formatMetric(row.cpa) }}</td>
              <td>{{ formatMetric(row.roi_gp) }}</td>
              <td>{{ formatMetric(row.refund_rate) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="muted">summary_table 为空</p>
      </div>
    </section>

    <section v-if="compareData" class="panel">
      <h2>日度曲线（Clicks）</h2>
      <div v-if="chartPoints.length" class="chart-wrap">
        <svg viewBox="0 0 600 160" preserveAspectRatio="none">
          <polyline
            :points="chartPoints"
            fill="none"
            stroke="#111"
            stroke-width="2"
          />
        </svg>
      </div>
      <p v-else class="muted">暂无 time_series 数据</p>
    </section>

    <section v-if="compareData" class="panel">
      <h2>Drivers</h2>
      <div class="driver-grid">
        <div v-for="(driver, idx) in compareData.drivers" :key="idx" class="driver-card">
          <p class="driver-title">{{ driver.factor }}</p>
          <p class="driver-note">{{ driver.note }}</p>
          <span class="tag">{{ driver.impact }}</span>
        </div>
      </div>
    </section>

    <section v-if="compareData" class="panel">
      <h2>Evidence Cards</h2>
      <div class="card-grid">
        <div v-for="(card, idx) in compareData.evidence_cards" :key="idx" class="evidence-card">
          <h3>{{ card.title }}</h3>
          <p>{{ card.insight }}</p>
          <span class="tag">{{ card.impact }}</span>
        </div>
      </div>
    </section>

    <section v-if="compareData" class="panel">
      <h2>提示</h2>
      <ul>
        <li v-for="(note, idx) in compareData.notes || []" :key="idx">{{ note }}</li>
        <li v-if="!compareData.notes || compareData.notes.length === 0">暂无额外提示</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { exportAdsimReport } from '../api/adsim'

const stored = localStorage.getItem('adsim_compare_result')
const compareData = ref(stored ? JSON.parse(stored) : null)

const chartPoints = computed(() => {
  const series = compareData.value?.time_series || []
  if (!series.length) return ''
  const values = series.map(item => Number(item.clicks || 0))
  const maxVal = Math.max(...values, 1)
  const minVal = Math.min(...values, 0)
  const width = 600
  const height = 160
  return values
    .map((val, idx) => {
      const x = (idx / Math.max(values.length - 1, 1)) * width
      const y = height - ((val - minVal) / Math.max(maxVal - minVal, 1)) * height
      return `${x},${y}`
    })
    .join(' ')
})

const formatMetric = value => {
  if (value === null || value === undefined) return '-'
  return Number(value).toFixed(4)
}

const exportReport = async () => {
  if (!compareData.value) return
  try {
    await exportAdsimReport(compareData.value)
    alert('已触发导出（占位接口）')
  } catch (err) {
    alert('导出接口尚未实现（占位调用）')
  }
}
</script>

<style scoped>
.page {
  padding: 48px 8vw 80px;
  background: linear-gradient(180deg, #fbf6ef 0%, #ffffff 70%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 32px;
  margin-bottom: 32px;
}

.eyebrow {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #8d7f6c;
  margin-bottom: 12px;
}

h1 {
  font-size: clamp(28px, 4vw, 40px);
  margin-bottom: 12px;
}

.sub {
  max-width: 520px;
  color: #4f4f4f;
  line-height: 1.6;
}

.page-nav {
  display: flex;
  gap: 12px;
}

.nav-link {
  padding: 8px 14px;
  border: 1px solid #111;
  color: #111;
  text-decoration: none;
  font-size: 14px;
  border-radius: 999px;
}

.panel {
  background: #ffffff;
  border: 1px solid #ddd2c2;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.06);
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.btn {
  background: #111;
  color: #fff;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
}

.btn.ghost {
  background: transparent;
  color: #111;
  border: 1px solid #111;
}

.table-wrap {
  overflow: auto;
  border: 1px solid #eadfcf;
  border-radius: 12px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th,
td {
  border-bottom: 1px solid #eadfcf;
  padding: 10px 12px;
  text-align: left;
}

.chart-wrap {
  border: 1px solid #eadfcf;
  border-radius: 12px;
  padding: 12px;
  background: #fffaf2;
}

svg {
  width: 100%;
  height: 160px;
}

.driver-grid,
.card-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.driver-card,
.evidence-card {
  border: 1px solid #eadfcf;
  background: #f9f2e7;
  border-radius: 16px;
  padding: 16px;
}

.driver-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.driver-note {
  color: #4f4f4f;
  margin-bottom: 12px;
}

.tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: #111;
  color: #fff;
  font-size: 12px;
}

.muted {
  color: #7d7365;
}

@media (max-width: 900px) {
  .page-header {
    flex-direction: column;
  }
}
</style>
