const API = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api').replace(/\/$/, '')
async function request(url, options) {
  let response
  try { response = await fetch(`${API}${url}`, options) }
  catch { throw new Error('Could not reach EcoVision’s server. Check that the backend is running, then try again.') }
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.error || 'The request could not be completed. Please try again.')
  return body
}
export const getHealth = () => request('/health')
export const detectWaste = (file) => { const data = new FormData(); data.append('image', file); return request('/detect', { method: 'POST', body: data }) }
export const findNearby = (lat, lon) => request(`/recycling/nearby?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`)
