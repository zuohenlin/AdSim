import service from './index'

export const updateLlmConfig = (payload) => {
  return service.post('/api/system/llm-config', payload)
}
