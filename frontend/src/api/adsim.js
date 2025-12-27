import service from './index'

export function uploadAdsimData(formData) {
  return service({
    url: '/api/v1/adsim/data/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function computeAdsimMetrics(payload) {
  return service({
    url: '/api/v1/adsim/metrics/compute',
    method: 'post',
    data: payload
  })
}

export function compareAdsimStrategy(payload) {
  return service({
    url: '/api/v1/adsim/strategy/compare',
    method: 'post',
    data: payload
  })
}

export function exportAdsimReport(payload) {
  return service({
    url: '/api/v1/adsim/report/export',
    method: 'post',
    data: payload
  })
}
