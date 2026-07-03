const form = document.getElementById('lessonForm');
const output = document.getElementById('output');
const generateButton = document.getElementById('generate');

function payload() {
  return {
    topic: document.getElementById('topic').value,
    primary_skill: 'phonics',
    target_words: document.getElementById('targetWords').value.split(',').map(v => v.trim()).filter(Boolean),
    age_min: Number(document.getElementById('ageMin').value),
    age_max: Number(document.getElementById('ageMax').value),
    level_label: document.getElementById('level').value,
    reading_stage: document.getElementById('reading').value,
    latin_writing_stage: document.getElementById('writing').value,
    pencil_control: 'age_appropriate',
    student_count: 8,
    session_duration_minutes: Number(document.getElementById('duration').value),
    support_needs: ['visual_support'],
    teacher_request: document.getElementById('request').value
  };
}

async function callApi(path) {
  output.innerHTML = '<p>Working…</p>';
  const response = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload())
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || 'Request failed');
  output.innerHTML = `<pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>`;
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  })[character]);
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  try { await callApi('/api/quick-review'); }
  catch (error) { output.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`; }
});

generateButton.addEventListener('click', async () => {
  try { await callApi('/api/generate'); }
  catch (error) { output.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`; }
});
