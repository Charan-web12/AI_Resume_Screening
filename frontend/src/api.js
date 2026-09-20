const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchTemplates() {
  const res = await fetch(`${API_BASE}/job-description/templates`);
  return res.json();
}

export async function fetchLatestJD() {
  const res = await fetch(`${API_BASE}/job-description/latest`);
  return res.json();
}

export async function submitJobDescription(payload) {
  const res = await fetch(`${API_BASE}/job-description`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to submit Job Description');
  }
  return res.json();
}

export async function uploadResumes(files) {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  const res = await fetch(`${API_BASE}/resumes/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to upload resumes');
  }
  return res.json();
}

export async function fetchCandidates() {
  const res = await fetch(`${API_BASE}/candidates`);
  return res.json();
}

export async function fetchCandidateDetail(id) {
  const res = await fetch(`${API_BASE}/candidates/${id}`);
  if (!res.ok) {
    throw new Error('Candidate not found');
  }
  return res.json();
}

export async function analyzeCandidates(payload = {}) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to analyze candidates');
  }
  return res.json();
}

export async function fetchRankings(jdId = null) {
  const url = jdId ? `${API_BASE}/rankings?jd_id=${jdId}` : `${API_BASE}/rankings`;
  const res = await fetch(url);
  return res.json();
}

export async function loadSampleData() {
  const res = await fetch(`${API_BASE}/load-samples`, {
    method: 'POST',
  });
  if (!res.ok) {
    throw new Error('Failed to load sample data');
  }
  return res.json();
}

export async function clearAllData() {
  const res = await fetch(`${API_BASE}/clear`, {
    method: 'POST',
  });
  return res.json();
}
