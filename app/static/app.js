const versionLabel = document.getElementById('versionLabel');
const engineeringGrid = document.getElementById('engineeringGrid');
const qaList = document.getElementById('qaList');
const privateList = document.getElementById('privateList');

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, character => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  })[character]);
}

function renderSnapshot(snapshot) {
  versionLabel.textContent = snapshot.edition;

  engineeringGrid.innerHTML = snapshot.engineering_highlights.map((item, index) => `
    <article class="feature-card">
      <div class="feature-icon">${String(index + 1).padStart(2, '0')}</div>
      <h3>${escapeHtml(item)}</h3>
      <p>${escapeHtml(featureDescription(item))}</p>
    </article>
  `).join('');

  qaList.innerHTML = snapshot.qa_principles.map(item => `
    <div><span>✓</span>${escapeHtml(item)}</div>
  `).join('');

  privateList.innerHTML = snapshot.private_by_design.map(item => `
    <li>${escapeHtml(item)}</li>
  `).join('');
}

function featureDescription(item) {
  const descriptions = {
    'FastAPI and Pydantic architecture': 'Clear public contracts, typed responses, and a small read-only API surface.',
    'Teacher-in-the-loop approval workflow': 'The product concept keeps professional judgement between planning and publication.',
    'Separate teacher and student presentation layers': 'Internal guidance and student-facing materials are treated as different products.',
    'Automated regression testing': 'Known failures are preserved as tests to prevent silent reintroduction.',
    'Responsive, accessible frontend design': 'The interface prioritises readability, hierarchy, and practical use across devices.'
  };
  return descriptions[item] || 'A selected public highlight from the private product architecture.';
}

fetch('/api/project-snapshot')
  .then(response => {
    if (!response.ok) throw new Error('Portfolio metadata unavailable');
    return response.json();
  })
  .then(renderSnapshot)
  .catch(() => {
    versionLabel.textContent = 'Portfolio edition';
  });
