const form = document.getElementById('lessonForm');
const planPanel = document.getElementById('planPanel');
const planSummary = document.getElementById('planSummary');
const compatibilityPanel = document.getElementById('compatibility');
const flowEditor = document.getElementById('flowEditor');
const resultPanel = document.getElementById('resultPanel');
const teacherView = document.getElementById('teacherView');
const studentView = document.getElementById('studentView');
const dataView = document.getElementById('dataView');
const statusPanel = document.getElementById('statusPanel');
const addStageButton = document.getElementById('addStage');
const generateApprovedButton = document.getElementById('generateApproved');
const printStudentButton = document.getElementById('printStudent');

let currentRequest = null;
let currentReview = null;
let currentFlow = [];
let currentResult = null;

const emojiByWord = {
  lion: '🦁',
  monkey: '🐒',
  elephant: '🐘',
  giraffe: '🦒',
  tiger: '🐯',
  zebra: '🦓',
  dog: '🐶',
  cat: '🐱',
  bird: '🐦',
  fish: '🐟',
  rabbit: '🐰',
  ship: '🚢',
  shoe: '👟',
  chair: '🪑',
  cheese: '🧀',
  sun: '☀️',
  moon: '🌙',
  star: '⭐',
  ball: '⚽',
  car: '🚗',
  train: '🚆'
};

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, character => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  })[character]);
}

function requestPayload() {
  return {
    topic: document.getElementById('topic').value.trim(),
    primary_skill: document.getElementById('skill').value,
    target_words: document.getElementById('targetWords').value
      .split(',')
      .map(value => value.trim())
      .filter(Boolean),
    age_min: Number(document.getElementById('ageMin').value),
    age_max: Number(document.getElementById('ageMax').value),
    level_label: document.getElementById('level').value,
    reading_stage: document.getElementById('reading').value,
    latin_writing_stage: document.getElementById('writing').value,
    pencil_control: document.getElementById('pencil').value,
    student_count: 8,
    session_duration_minutes: Number(document.getElementById('duration').value),
    support_needs: ['visual_support'],
    teacher_request: document.getElementById('request').value.trim()
  };
}

async function postJson(path, body) {
  const response = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) {
    const message = Array.isArray(data.detail)
      ? data.detail.map(item => item.msg).join(' ')
      : data.detail;
    throw new Error(message || 'The demo request could not be completed.');
  }
  return data;
}

function setStatus(message, type = 'neutral') {
  statusPanel.className = `card status-card ${type}`;
  statusPanel.innerHTML = `<p>${escapeHtml(message)}</p>`;
}

function stageMinutes(stage) {
  return Math.max(1, Number(stage.end_minute) - Number(stage.start_minute));
}

function normaliseFlow() {
  let cursor = 0;
  currentFlow = currentFlow.map(stage => {
    const minutes = Math.max(1, Number(stage._minutes || stageMinutes(stage)));
    const updated = {
      ...stage,
      start_minute: cursor,
      end_minute: cursor + minutes,
      _minutes: minutes
    };
    cursor += minutes;
    return updated;
  });

  const total = currentRequest.session_duration_minutes;
  const difference = total - cursor;
  if (currentFlow.length && difference !== 0) {
    const preferredIndex = currentFlow.findIndex(stage => stage.stage === 'Student pages');
    const index = preferredIndex >= 0 ? preferredIndex : currentFlow.length - 1;
    currentFlow[index]._minutes = Math.max(
      1,
      currentFlow[index]._minutes + difference
    );

    cursor = 0;
    currentFlow = currentFlow.map(stage => {
      const updated = {
        ...stage,
        start_minute: cursor,
        end_minute: cursor + stage._minutes
      };
      cursor = updated.end_minute;
      return updated;
    });
    currentFlow[currentFlow.length - 1].end_minute = total;
  }
}

function renderCompatibility(compatibility) {
  const warnings = compatibility.warnings || [];
  const blocking = compatibility.blocking_issues || [];
  const modes = compatibility.allowed_response_modes || [];

  compatibilityPanel.innerHTML = `
    <div class="compat-card">
      <strong>Compatible response modes</strong>
      <div class="chip-row">
        ${modes.map(mode => `<span class="chip">${escapeHtml(mode.replaceAll('_', ' '))}</span>`).join('')}
      </div>
    </div>
    ${warnings.length ? `
      <div class="compat-card warning">
        <strong>Support notes</strong>
        <ul>${warnings.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      </div>
    ` : ''}
    ${blocking.length ? `
      <div class="compat-card danger">
        <strong>Blocking issues</strong>
        <ul>${blocking.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      </div>
    ` : ''}
  `;
}

function renderPlan() {
  normaliseFlow();

  planSummary.innerHTML = `
    <div class="summary-card">
      <span>Lesson goal</span>
      <strong>${escapeHtml(currentReview.lesson_goal)}</strong>
    </div>
    <div class="summary-card">
      <span>Duration</span>
      <strong>${currentReview.session_duration_minutes} minutes</strong>
    </div>
    <div class="summary-card">
      <span>Student pages</span>
      <strong>${currentReview.worksheet_count}</strong>
    </div>
  `;

  renderCompatibility(currentReview.compatibility);

  flowEditor.innerHTML = currentFlow.map((stage, index) => {
    const protectedStage = stage.stage === 'Student pages';
    return `
      <article class="flow-card" data-stage-id="${escapeHtml(stage.stage_id)}">
        <div class="flow-time">
          <strong>${stage.start_minute}–${stage.end_minute}</strong>
          <span>${stage._minutes || stageMinutes(stage)} min</span>
        </div>
        <div class="flow-fields">
          <label>
            Stage
            <input
              data-field="stage"
              value="${escapeHtml(stage.stage)}"
              ${protectedStage ? 'readonly' : ''}
            >
          </label>
          <label>
            Teacher action
            <textarea data-field="teacher_action">${escapeHtml(stage.teacher_action)}</textarea>
          </label>
          <label>
            Student action
            <textarea data-field="student_action">${escapeHtml(stage.student_action)}</textarea>
          </label>
        </div>
        <div class="flow-controls" aria-label="Stage controls">
          <button type="button" class="icon-button" data-action="up" ${index === 0 ? 'disabled' : ''}>↑</button>
          <button type="button" class="icon-button" data-action="down" ${index === currentFlow.length - 1 ? 'disabled' : ''}>↓</button>
          <button
            type="button"
            class="icon-button danger-button"
            data-action="delete"
            ${protectedStage ? 'disabled title="Student pages is required"' : ''}
          >×</button>
        </div>
      </article>
    `;
  }).join('');

  planPanel.classList.remove('hidden');
  planPanel.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function stageIndexFromElement(element) {
  const card = element.closest('[data-stage-id]');
  if (!card) return -1;
  return currentFlow.findIndex(stage => stage.stage_id === card.dataset.stageId);
}

flowEditor.addEventListener('input', event => {
  const field = event.target.dataset.field;
  if (!field) return;
  const index = stageIndexFromElement(event.target);
  if (index < 0) return;
  currentFlow[index][field] = event.target.value.trim();
});

flowEditor.addEventListener('click', event => {
  const action = event.target.dataset.action;
  if (!action) return;

  const index = stageIndexFromElement(event.target);
  if (index < 0) return;

  if (action === 'up' && index > 0) {
    [currentFlow[index - 1], currentFlow[index]] = [
      currentFlow[index],
      currentFlow[index - 1]
    ];
  }

  if (action === 'down' && index < currentFlow.length - 1) {
    [currentFlow[index + 1], currentFlow[index]] = [
      currentFlow[index],
      currentFlow[index + 1]
    ];
  }

  if (action === 'delete') {
    const stage = currentFlow[index];
    if (stage.stage === 'Student pages') return;

    const removedMinutes = stage._minutes || stageMinutes(stage);
    currentFlow.splice(index, 1);
    const receiverIndex = Math.max(0, index - 1);
    if (currentFlow[receiverIndex]) {
      currentFlow[receiverIndex]._minutes = (
        currentFlow[receiverIndex]._minutes
        || stageMinutes(currentFlow[receiverIndex])
      ) + removedMinutes;
    }
  }

  renderPlan();
});

addStageButton.addEventListener('click', () => {
  const donorIndex = currentFlow
    .map((stage, index) => ({index, minutes: stage._minutes || stageMinutes(stage)}))
    .filter(item => item.minutes >= 6)
    .sort((a, b) => b.minutes - a.minutes)[0]?.index;

  if (donorIndex === undefined) {
    setStatus('There is not enough time to add another stage.', 'warning');
    return;
  }

  currentFlow[donorIndex]._minutes = (
    currentFlow[donorIndex]._minutes
    || stageMinutes(currentFlow[donorIndex])
  ) - 3;

  const reviewIndex = currentFlow.findIndex(stage => stage.stage === 'Review and close');
  const insertIndex = reviewIndex >= 0 ? reviewIndex : currentFlow.length;

  currentFlow.splice(insertIndex, 0, {
    stage_id: `demo_stage_custom_${Date.now()}`,
    start_minute: 0,
    end_minute: 3,
    stage: 'Extra guided practice',
    teacher_action: 'Model one additional supported example.',
    student_action: 'Try the example with a partner or visual cue.',
    materials: [],
    _minutes: 3
  });

  renderPlan();
});

function publicFlowPayload() {
  return currentFlow.map(({_minutes, ...stage}) => stage);
}

function wordEmoji(word) {
  return emojiByWord[String(word).toLowerCase()] || '🖼️';
}

function maskedWord(word) {
  const value = String(word);
  const index = value.search(/[aeiou]/i);
  if (index >= 0) {
    return `${value.slice(0, index)}_${value.slice(index + 1)}`;
  }
  return value.length > 1 ? `${value.slice(0, -1)}_` : '_';
}

function renderTeacherActivity(activity) {
  return `
    <div class="teacher-activity">
      <div class="activity-meta">
        <span class="section-badge ${escapeHtml(activity.section)}">
          ${activity.section === 'extra' ? 'Extra / finish later' : 'Core practice'}
        </span>
        <span>${escapeHtml(activity.activity_type.replaceAll('_', ' '))}</span>
      </div>
      <h4>${escapeHtml(activity.instruction)}</h4>
      <p><strong>Items:</strong> ${activity.items.map(escapeHtml).join(', ')}</p>
      <p><strong>Answer:</strong> ${escapeHtml(activity.answer)}</p>
    </div>
  `;
}

function renderTeacherView(result) {
  const document = result.document;
  const checks = Object.entries(result.validation.checks);

  teacherView.innerHTML = `
    <section class="teacher-summary">
      <h3>${escapeHtml(document.title)}</h3>
      <p>${escapeHtml(document.learner_summary)}</p>
      <div class="validation-banner ${result.validation.valid ? 'valid' : 'invalid'}">
        ${result.validation.valid ? 'Validated demo pack' : 'Validation needs attention'}
      </div>
    </section>

    <section>
      <h3>Approved class flow</h3>
      <div class="teacher-flow">
        ${document.class_flow.map(stage => `
          <div class="teacher-flow-row">
            <strong>${stage.start_minute}–${stage.end_minute}</strong>
            <div>
              <h4>${escapeHtml(stage.stage)}</h4>
              <p><strong>Teacher:</strong> ${escapeHtml(stage.teacher_action)}</p>
              <p><strong>Students:</strong> ${escapeHtml(stage.student_action)}</p>
            </div>
          </div>
        `).join('')}
      </div>
    </section>

    ${document.worksheets.map(page => `
      <section class="teacher-page">
        <div class="page-heading">
          <div>
            <p class="eyebrow">Page ${page.page_number}</p>
            <h3>${escapeHtml(page.title)}</h3>
          </div>
          <span>${page.practice_minutes} min</span>
        </div>
        <p>${escapeHtml(page.purpose)}</p>
        ${page.activities.map(renderTeacherActivity).join('')}
      </section>
    `).join('')}

    <section>
      <h3>Answer key</h3>
      <ol>${document.answer_key.map(answer => `<li>${escapeHtml(answer)}</li>`).join('')}</ol>
    </section>

    <section>
      <h3>Validation checks</h3>
      <div class="check-grid">
        ${checks.map(([name, passed]) => `
          <div class="check-item ${passed ? 'passed' : 'failed'}">
            <span>${passed ? '✓' : '!'}</span>
            ${escapeHtml(name.replaceAll('_', ' '))}
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function renderStudentActivity(activity, number) {
  const items = activity.items || [];

  if (activity.activity_type === 'complete_word') {
    return `
      <section class="student-activity">
        <h3>${number}. ${escapeHtml(activity.instruction)}</h3>
        <div class="student-word-grid">
          ${items.map((word, index) => `
            <div class="student-word-card">
              <span class="item-number">${index + 1}</span>
              <span class="visual">${wordEmoji(word)}</span>
              <strong>${escapeHtml(maskedWord(word))}</strong>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  }

  if (activity.activity_type === 'write_word') {
    return `
      <section class="student-activity">
        <h3>${number}. ${escapeHtml(activity.instruction)}</h3>
        <div class="student-word-grid">
          ${items.map((word, index) => `
            <div class="student-word-card writing-card">
              <span class="item-number">${index + 1}</span>
              <span class="visual">${wordEmoji(word)}</span>
              <span class="writing-line"></span>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  }

  if (activity.activity_type === 'sort') {
    return `
      <section class="student-activity">
        <h3>${number}. ${escapeHtml(activity.instruction)}</h3>
        <div class="sort-bank">
          ${items.map(word => `<span>${escapeHtml(word)}</span>`).join('')}
        </div>
        <div class="sort-zones">
          <div>Group A</div>
          <div>Group B</div>
        </div>
      </section>
    `;
  }

  return `
    <section class="student-activity">
      <h3>${number}. ${escapeHtml(activity.instruction)}</h3>
      <div class="choice-grid">
        ${items.map((word, index) => `
          <div class="choice-card">
            <span class="item-number">${index + 1}</span>
            <span class="visual">${wordEmoji(word)}</span>
            <strong>${escapeHtml(word)}</strong>
            <span class="circle-target" aria-hidden="true"></span>
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function renderStudentView(result) {
  studentView.innerHTML = result.document.worksheets.map(page => `
    <article class="student-sheet">
      <div class="student-header">
        <span>Name: ____________________</span>
        <span>Date: ____________________</span>
      </div>
      <h2>${escapeHtml(result.document.title)}</h2>
      <p class="student-page-title">${escapeHtml(page.title)}</p>
      ${page.activities.map((activity, index) => renderStudentActivity(activity, index + 1)).join('')}
      <span class="page-number">${page.page_number}</span>
    </article>
  `).join('');
}

function renderResult(result) {
  currentResult = result;
  renderTeacherView(result);
  renderStudentView(result);
  dataView.innerHTML = `<pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre>`;
  resultPanel.classList.remove('hidden');
  activateTab('teacher');
  resultPanel.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function activateTab(name) {
  document.querySelectorAll('.tab').forEach(button => {
    button.classList.toggle('active', button.dataset.tab === name);
  });
  teacherView.classList.toggle('hidden', name !== 'teacher');
  studentView.classList.toggle('hidden', name !== 'student');
  dataView.classList.toggle('hidden', name !== 'data');
}

document.querySelector('.tabs').addEventListener('click', event => {
  const name = event.target.dataset.tab;
  if (name) activateTab(name);
});

form.addEventListener('submit', async event => {
  event.preventDefault();
  setStatus('Creating a deterministic review plan…');

  try {
    currentRequest = requestPayload();
    currentReview = await postJson('/api/quick-review', currentRequest);
    currentFlow = currentReview.class_flow.map(stage => ({
      ...stage,
      _minutes: stageMinutes(stage)
    }));
    renderPlan();
    setStatus('Review plan ready. The Student pages stage is protected.', 'success');
  } catch (error) {
    setStatus(error.message, 'error');
  }
});

generateApprovedButton.addEventListener('click', async () => {
  if (!currentRequest || !currentFlow.length) return;

  const studentPagesCount = currentFlow.filter(
    stage => stage.stage === 'Student pages'
  ).length;

  if (studentPagesCount !== 1) {
    setStatus('The flow must contain exactly one Student pages stage.', 'error');
    return;
  }

  setStatus('Generating a safe deterministic demo pack…');

  try {
    const result = await postJson('/api/generate-approved', {
      request: currentRequest,
      approved_flow: publicFlowPayload()
    });
    renderResult(result);
    setStatus('Validated demo pack generated.', 'success');
  } catch (error) {
    setStatus(error.message, 'error');
  }
});

printStudentButton.addEventListener('click', () => {
  if (!currentResult) return;
  activateTab('student');
  document.body.classList.add('printing-student');
  window.print();
  document.body.classList.remove('printing-student');
});

window.addEventListener('afterprint', () => {
  document.body.classList.remove('printing-student');
});

fetch('/api/health')
  .then(response => response.json())
  .then(data => {
    document.getElementById('versionLabel').textContent = data.appVersion;
  })
  .catch(() => {});
