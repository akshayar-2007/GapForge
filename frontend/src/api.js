const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export async function startWithResume(file, targetCompany) {
  const formData = new FormData()
  formData.append('resume', file)
  const url = `${API_URL}/api/start?target_company=${encodeURIComponent(targetCompany)}`
  const res = await fetch(url, { method: 'POST', body: formData })
  return handleResponse(res)
}

export async function startManual(profile) {
  const res = await fetch(`${API_URL}/api/start-manual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  })
  return handleResponse(res)
}

export async function sendFeedback(sessionId, feedback) {
  const url = `${API_URL}/api/feedback?session_id=${sessionId}&feedback=${encodeURIComponent(feedback)}`
  const res = await fetch(url, { method: 'POST' })
  return handleResponse(res)
}

export async function selectIdea(sessionId, ideaIndex) {
  const url = `${API_URL}/api/select?session_id=${sessionId}&idea_index=${ideaIndex}`
  const res = await fetch(url, { method: 'POST' })
  return handleResponse(res)
}
