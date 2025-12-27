<template>
  <div class="page">
    <header class="page-header">
      <div>
        <p class="eyebrow">Adsim · 策略配置</p>
        <h1>配置 A/B/C 并对比策略表现</h1>
        <p class="sub">
          设置时间窗口与策略参数，调用 /strategy/compare 生成对比结果。
        </p>
      </div>
      <nav class="page-nav">
        <RouterLink class="nav-link" to="/adsim/import">数据导入</RouterLink>
        <RouterLink class="nav-link" to="/adsim/compare">对比结果</RouterLink>
      </nav>
    </header>

    <section class="panel">
      <div class="form-grid">
        <label class="field">
          <span>dataset_id</span>
          <input v-model="datasetId" placeholder="从导入页自动填充" />
        </label>
        <label class="field">
          <span>demo_mode</span>
          <select v-model="demoMode">
            <option :value="true">true</option>
            <option :value="false">false</option>
          </select>
        </label>
        <label class="field">
          <span>window.start</span>
          <input v-model="windowStart" type="date" />
        </label>
        <label class="field">
          <span>window.end</span>
          <input v-model="windowEnd" type="date" />
        </label>
      </div>
    </section>

    <section class="panel">
      <h2>策略参数</h2>
      <div class="strategy-grid">
        <div v-for="(item, idx) in strategies" :key="item.name" class="strategy-card">
          <p class="strategy-title">策略 {{ item.name }}</p>
          <label class="field">
            <span>预算上限</span>
            <input v-model="item.budget" placeholder="例如 10000" />
          </label>
          <label class="field">
            <span>出价策略</span>
            <input v-model="item.bid" placeholder="例如 2.5" />
          </label>
          <label class="field">
            <span>说明</span>
            <textarea v-model="item.note" rows="3" placeholder="策略简述"></textarea>
          </label>
          <button class="btn ghost" @click="resetStrategy(idx)">重置</button>
        </div>
      </div>
      <div class="actions">
        <button class="btn" :disabled="loading" @click="submitCompare">
          {{ loading ? '计算中...' : '运行对比' }}
        </button>
        <button class="btn ghost" @click="saveDraft">保存参数</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="info" class="ok">{{ info }}</p>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { compareAdsimStrategy } from '../api/adsim'
import { useRouter } from 'vue-router'

const router = useRouter()
const datasetId = ref(localStorage.getItem('adsim_dataset_id') || '')
const windowStart = ref('2025-01-01')
const windowEnd = ref('2025-01-31')
const demoMode = ref(true)
const loading = ref(false)
const error = ref('')
const info = ref('')

const strategies = ref([
  { name: 'A', budget: '', bid: '', note: '' },
  { name: 'B', budget: '', bid: '', note: '' },
  { name: 'C', budget: '', bid: '', note: '' }
])

const resetStrategy = idx => {
  const name = strategies.value[idx].name
  strategies.value[idx] = { name, budget: '', bid: '', note: '' }
}

const saveDraft = () => {
  localStorage.setItem('adsim_strategy_params', JSON.stringify(strategies.value))
  info.value = '已保存策略参数'
  setTimeout(() => {
    info.value = ''
  }, 1500)
}

const submitCompare = async () => {
  error.value = ''
  if (!datasetId.value.trim()) {
    error.value = '请先填写 dataset_id'
    return
  }

  loading.value = true
  try {
    const payload = {
      mode: 'baseline',
      dataset_id: datasetId.value.trim(),
      window: {
        start: windowStart.value,
        end: windowEnd.value
      },
      strategies: strategies.value.map(item => item.name),
      demo_mode: demoMode.value
    }
    const data = await compareAdsimStrategy(payload)
    localStorage.setItem('adsim_compare_result', JSON.stringify(data))
    localStorage.setItem('adsim_dataset_id', datasetId.value.trim())
    saveDraft()
    router.push('/adsim/compare')
  } catch (err) {
    error.value = err?.message || '策略对比失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page {
  padding: 48px 8vw 80px;
  background: radial-gradient(circle at top, #fdf7ef 0%, #f3efe9 50%, #ffffff 100%);
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

.form-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
}

input,
select,
textarea {
  border: 1px solid #d7c7b2;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
  background: #fffaf2;
}

.strategy-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.strategy-card {
  background: #f9f2e7;
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #eadfcf;
}

.strategy-title {
  font-weight: 600;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 18px;
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

.error {
  color: #c0392b;
  margin-top: 12px;
}

.ok {
  color: #2c7a7b;
  margin-top: 12px;
}

@media (max-width: 900px) {
  .page-header {
    flex-direction: column;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
