<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-brand">ADSIM</div>
      <div class="nav-links">
        <a href="https://github.com/zuohenlin/AdSim" target="_blank" class="github-link">
          项目地址 Adsim <span class="arrow">-&gt;</span>
        </a>
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          原项目 MiroFish <span class="arrow">-&gt;</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- 上半部分：Hero 区域 -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">电商投放策略预演与对比引擎</span>
            <span class="version-text">/ V1.0-预览版</span>
          </div>
          
          <h1 class="main-title">
            导入投放数据<br>
            <span class="gradient-text">即刻对比策略</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <span class="highlight-bold">Adsim</span> 面向电商活动投放，提供从数据导入到指标计算、策略对比、证据卡与报告导出的完整闭环。用最小样例复现策略A/B/C的效果差异，让决策更可解释、更可复盘。
            </p>
            <p class="slogan-text">
              让策略在数据中预演，让结论在证据中落地<span class="blinking-cursor">_</span>
            </p>
          </div>

           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Logo 区域 -->
          <div class="logo-container">
            <img src="../assets/logo/adsim_logo.png" alt="Adsim Logo" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- 下半部分：双栏布局 -->
      <section class="dashboard-section">
        <!-- 左栏：状态与步骤 -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> 系统状态
          </div>
          
          <h2 class="section-title">投放预演就绪</h2>
          <p class="section-desc">
            支持样例或真实投放数据导入，快速完成指标与策略对比的演示闭环
          </p>
          
          <!-- 数据指标卡片 -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">快启动</div>
              <div class="metric-label">3分钟闭环演示</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">可解释</div>
              <div class="metric-label">证据卡+区间估计</div>
            </div>
          </div>

          <!-- 项目模拟步骤介绍 (新增区域) -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> 策略预演流程
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">
                    数据导入
                    <a href="/adsim/import" class="step-link">进入导入</a>
                  </div>
                  <div class="step-desc">CSV上传 & 字段映射 & 数据落盘</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">指标计算</div>
                  <div class="step-desc">CTR/CVR/CPA/ROI等关键口径</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">策略对比</div>
                  <div class="step-desc">A/B/C 方案与区间估计输出</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">证据卡与驱动</div>
                  <div class="step-desc">风险点、驱动因素与可解释结论</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">报告导出</div>
                  <div class="step-desc">HTML可打印报告一键生成</div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- 右栏：交互控制台 -->
        <div class="right-panel">
          <div class="console-box">
            <!-- 上传区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / 现实种子</span>
                <span class="console-meta">支持格式: PDF, MD, TXT</span>
              </div>
              <div class="llm-config">
                <div class="llm-title">LLM 配置（原始仿真入口）</div>
                <div class="llm-row">
                  <label class="llm-label">API Key</label>
                  <input
                    v-model="llmConfig.apiKey"
                    type="password"
                    class="llm-input"
                    placeholder="sk-..."
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">API 地址</label>
                  <input
                    v-model="llmConfig.baseUrl"
                    type="text"
                    class="llm-input"
                    placeholder="https://api.openai.com/v1"
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">模型名称</label>
                  <input
                    v-model="llmConfig.modelName"
                    type="text"
                    class="llm-input"
                    placeholder="gpt-4o-mini / qwen-plus"
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">ZEP API</label>
                  <input
                    v-model="llmConfig.zepApiKey"
                    type="password"
                    class="llm-input"
                    placeholder="zep-..."
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">加速 Key</label>
                  <input
                    v-model="llmConfig.boostApiKey"
                    type="password"
                    class="llm-input"
                    placeholder="可选"
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">加速地址</label>
                  <input
                    v-model="llmConfig.boostBaseUrl"
                    type="text"
                    class="llm-input"
                    placeholder="可选"
                  />
                </div>
                <div class="llm-row">
                  <label class="llm-label">加速模型</label>
                  <input
                    v-model="llmConfig.boostModelName"
                    type="text"
                    class="llm-input"
                    placeholder="可选"
                  />
                </div>
                <div class="llm-actions">
                  <button
                    class="llm-save"
                    :disabled="configSaving"
                    @click="saveLlmConfig"
                  >
                    <span v-if="!configSaving">保存到 .env</span>
                    <span v-else>保存中...</span>
                  </button>
                  <span v-if="configStatus" class="llm-status">{{ configStatus }}</span>
                </div>
                <div class="llm-hint">仅用于原始仿真入口，本地调试模式可用</div>
              </div>

              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">拖拽文件上传</div>
                  <div class="upload-hint">或点击浏览文件系统</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分割线 -->
            <div class="console-divider">
              <span>输入参数</span>
            </div>

            <!-- 输入区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / 模拟提示词</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// 用自然语言输入模拟或预测需求（例.春节大促预算不变，A/B/C三种投放策略哪一种ROI更高）"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">引擎: Adsim-V1.0</div>
              </div>
            </div>

            <!-- 启动按钮 -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">启动引擎</span>
                <span v-else>初始化中...</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { updateLlmConfig } from '../api/system'

const router = useRouter()

// 表单数据
const formData = ref({
  simulationRequirement: ''
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)
const configSaving = ref(false)
const configStatus = ref('')
const llmConfig = ref({
  apiKey: '',
  baseUrl: '',
  modelName: '',
  zepApiKey: '',
  boostApiKey: '',
  boostBaseUrl: '',
  boostModelName: ''
})

// 文件输入引用
const fileInput = ref(null)

// 计算属性:是否可以提交
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

const saveLlmConfig = async () => {
  if (!llmConfig.value.apiKey.trim()) {
    configStatus.value = '请填写 API Key'
    return
  }
  configSaving.value = true
  configStatus.value = ''
  try {
    await updateLlmConfig({
      api_key: llmConfig.value.apiKey.trim(),
      base_url: llmConfig.value.baseUrl.trim(),
      model_name: llmConfig.value.modelName.trim(),
      zep_api_key: llmConfig.value.zepApiKey.trim(),
      boost_api_key: llmConfig.value.boostApiKey.trim(),
      boost_base_url: llmConfig.value.boostBaseUrl.trim(),
      boost_model_name: llmConfig.value.boostModelName.trim()
    })
    llmConfig.value.apiKey = ''
    configStatus.value = '已写入 .env'
  } catch (err) {
    configStatus.value = `保存失败: ${err.message || '未知错误'}`
  } finally {
    configSaving.value = false
  }
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // 存储待上传的数据
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    
    // 立即跳转到Process页面（使用特殊标识表示新建项目）
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* 全局变量与重置 */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    使用 Space Grotesk 作为主要标题字体，JetBrains Mono 作为代码/标签字体
    确保已在 index.html 引入这些 Google Fonts 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 顶部导航 */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

.nav-button {
  background: var(--orange);
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 800;
  padding: 10px 18px;
  border: 1px solid var(--orange);
  border-radius: 6px;
  letter-spacing: 0.8px;
  box-shadow: 0 6px 14px rgba(255, 69, 0, 0.25);
  transition: all 0.2s;
}

.step-link {
  display: inline-flex;
  align-items: center;
  margin-left: 12px;
  font-family: inherit;
  font-size: 1rem;
  color: var(--black);
  text-decoration: none;
  border-bottom: 1px solid var(--black);
  line-height: 1.2;
}

.step-link::after {
  content: ' ->';
  margin-left: 4px;
}

.step-link:hover {
  color: var(--orange);
  border-color: var(--orange);
}

.nav-button:hover {
  background: #ff5a1f;
  border-color: #ff5a1f;
  color: var(--white);
  transform: translateY(-1px);
}

/* 主要内容区 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px; /* 调整logo大小 */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* 外部实线 */
  padding: 8px; /* 内边距形成双重边框感 */
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.llm-config {
  border: 1px solid #EEE;
  padding: 16px;
  margin-bottom: 16px;
  background: #FAFAFA;
}

.llm-title {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 12px;
}

.llm-row {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}

.llm-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #555;
}

.llm-input {
  border: 1px solid #DDD;
  background: var(--white);
  padding: 8px 10px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  outline: none;
}

.llm-input:focus {
  border-color: var(--black);
}

.llm-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 6px;
}

.llm-save {
  background: var(--black);
  color: var(--white);
  border: 1px solid var(--black);
  padding: 8px 12px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  cursor: pointer;
}

.llm-save:disabled {
  background: #E5E5E5;
  color: #999;
  border-color: #E5E5E5;
  cursor: not-allowed;
}

.llm-status {
  font-size: 0.75rem;
  color: #666;
}

.llm-hint {
  font-size: 0.75rem;
  color: #999;
  margin-top: 8px;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>
