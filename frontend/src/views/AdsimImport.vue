<template>
  <div class="page">
    <header class="page-header">
      <div>
        <p class="eyebrow">Adsim · 数据导入</p>
        <h1>上传CSV并生成数据集</h1>
        <p class="sub">
          上传后端支持的表（ad_log/orders/traffic/users/reviews），返回校验结果并保存 dataset_id。
        </p>
      </div>
      <nav class="page-nav">
        <RouterLink class="nav-link" to="/adsim/strategy">策略配置</RouterLink>
        <RouterLink class="nav-link" to="/adsim/compare">对比结果</RouterLink>
      </nav>
    </header>

    <section class="panel">
      <div class="form-grid">
        <label class="field">
          <span>数据表类型</span>
          <select v-model="tableType">
            <option v-for="t in tableTypes" :key="t" :value="t">{{ t }}</option>
          </select>
        </label>
        <label class="field">
          <span>CSV 文件</span>
          <input type="file" accept=".csv" @change="onFileChange" />
        </label>
        <label class="field full">
          <span>mapping_json（可选）</span>
          <textarea
            v-model="mappingJson"
            placeholder='{"adId":"ad_id","imps":"impressions"}'
            rows="3"
          />
        </label>
      </div>

      <div class="actions">
        <button class="btn" :disabled="loading" @click="submitUpload">
          {{ loading ? '上传中...' : '上传并校验' }}
        </button>
        <button class="btn ghost" @click="clearResult">清空结果</button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="datasetId" class="ok">
        已保存 dataset_id：<strong>{{ datasetId }}</strong>
      </p>
    </section>

    <section v-if="result" class="panel">
      <h2>校验结果</h2>
      <div class="grid">
        <div class="card">
          <p class="label">dataset_id</p>
          <p class="value">{{ result.dataset_id }}</p>
        </div>
        <div class="card">
          <p class="label">detected_columns</p>
          <p class="value">{{ result.detected_columns?.join(', ') || '-' }}</p>
        </div>
        <div class="card">
          <p class="label">missing_required_columns</p>
          <p class="value">{{ result.missing_required_columns?.join(', ') || '无' }}</p>
        </div>
        <div class="card">
          <p class="label">saved_path</p>
          <p class="value">{{ result.saved_path }}</p>
        </div>
      </div>

      <h3>样例数据</h3>
      <div class="table-wrap">
        <table v-if="result.sample_rows?.length">
          <thead>
            <tr>
              <th v-for="col in sampleColumns" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in result.sample_rows" :key="idx">
              <td v-for="col in sampleColumns" :key="col">{{ row[col] }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="muted">暂无样例数据</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { uploadAdsimData } from '../api/adsim'

const tableTypes = ['ad_log', 'orders', 'traffic', 'users', 'reviews']
const tableType = ref('ad_log')
const file = ref(null)
const mappingJson = ref('')
const loading = ref(false)
const result = ref(null)
const error = ref('')
const datasetId = ref(localStorage.getItem('adsim_dataset_id') || '')

const sampleColumns = computed(() => {
  if (!result.value?.sample_rows?.length) return []
  return Object.keys(result.value.sample_rows[0])
})

const onFileChange = event => {
  file.value = event.target.files?.[0] || null
}

const submitUpload = async () => {
  error.value = ''
  if (!file.value) {
    error.value = '请先选择CSV文件'
    return
  }
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('table_type', tableType.value)
  if (mappingJson.value.trim()) {
    formData.append('mapping_json', mappingJson.value.trim())
  }

  loading.value = true
  try {
    const data = await uploadAdsimData(formData)
    result.value = data
    datasetId.value = data.dataset_id
    localStorage.setItem('adsim_dataset_id', data.dataset_id)
  } catch (err) {
    error.value = err?.message || '上传失败'
  } finally {
    loading.value = false
  }
}

const clearResult = () => {
  result.value = null
  error.value = ''
}
</script>

<style scoped>
.page {
  padding: 48px 8vw 80px;
  background: linear-gradient(160deg, #faf7f2 0%, #f6f1ea 50%, #ffffff 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 32px;
  align-items: flex-start;
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

.field.full {
  grid-column: 1 / -1;
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

.grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  margin-bottom: 16px;
}

.card {
  background: #f7f0e5;
  border-radius: 12px;
  padding: 16px;
}

.label {
  font-size: 12px;
  color: #7a6a57;
}

.value {
  font-size: 14px;
  margin-top: 6px;
  word-break: break-all;
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

.muted {
  padding: 14px;
  color: #7d7365;
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
