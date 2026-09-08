const STORAGE_KEY = "pjilosophy.progress.v1";
const ANNOTATION_KEY = "pjilosophy.annotations.v1";
const THEME_KEY = "pjilosophy.theme";

const COURSE_URLS = ["./content/course.json", "./course.json"];
const GLOSSARY_URLS = ["./content/glossary.json", "./glossary.json"];
const THINKER_URLS = ["./content/thinkers.json", "./thinkers.json"];

const appEl = document.getElementById("app");
const brandCourseEl = document.getElementById("brand-course");
const progressRail = document.getElementById("progress-rail");
const progressFill = document.getElementById("progress-rail-fill");
const navContinue = document.getElementById("nav-continue");
const navSyllabus = document.getElementById("nav-syllabus");
const navQuizzes = document.getElementById("nav-quizzes");
const navTerms = document.getElementById("nav-terms");
const navTracks = document.getElementById("nav-tracks");
const themeToggleEl = document.getElementById("theme-toggle");
const themeColorMeta = document.getElementById("meta-theme-color");

let course = null;
let readings = [];
let progress = loadProgress();
let annotations = loadAnnotations();
let noteTimer = null;
let paraNoteTimer = null;
let scrollTimer = null;
let renderGen = 0;
let quizSession = null;
let glossary = { title: "Philosophical terms", intro: "", terms: [] };
let glossaryUi = { query: "", eraId: "" };
let thinkerIndex = [];
const textCache = new Map();

function getStoredTheme() {
  try {
    const value = localStorage.getItem(THEME_KEY);
    if (value === "dark" || value === "light") return value;
  } catch {
    /* ignore */
  }
  return null;
}

function systemPrefersDark() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function effectiveTheme() {
  return getStoredTheme() || (systemPrefersDark() ? "dark" : "light");
}

function applyThemeAttribute(theme) {
  if (theme === "dark" || theme === "light") {
    document.documentElement.setAttribute("data-theme", theme);
  } else {
    document.documentElement.removeAttribute("data-theme");
  }
}

function syncThemeChrome() {
  const theme = effectiveTheme();
  const nextLabel = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
  if (themeToggleEl) {
    themeToggleEl.setAttribute("aria-label", nextLabel);
    themeToggleEl.setAttribute("title", nextLabel);
  }
  if (themeColorMeta) {
    themeColorMeta.setAttribute("content", theme === "dark" ? "#161310" : "#f2ebe0");
  }
}

function setTheme(theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    /* ignore */
  }
  applyThemeAttribute(theme);
  syncThemeChrome();
}

function toggleTheme() {
  setTheme(effectiveTheme() === "dark" ? "light" : "dark");
}

function initTheme() {
  const stored = getStoredTheme();
  applyThemeAttribute(stored);
  syncThemeChrome();
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  const onSchemeChange = () => {
    if (getStoredTheme()) return;
    syncThemeChrome();
  };
  if (typeof mq.addEventListener === "function") {
    mq.addEventListener("change", onSchemeChange);
  } else if (typeof mq.addListener === "function") {
    mq.addListener(onSchemeChange);
  }
  themeToggleEl?.addEventListener("click", (event) => {
    event.preventDefault();
    toggleTheme();
  });
}

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completed: {}, notes: {}, scroll: {}, quizzes: {}, bookmarks: {} };
    const parsed = JSON.parse(raw);
    return {
      completed: parsed.completed && typeof parsed.completed === "object" ? parsed.completed : {},
      notes: parsed.notes && typeof parsed.notes === "object" ? parsed.notes : {},
      scroll: parsed.scroll && typeof parsed.scroll === "object" ? parsed.scroll : {},
      quizzes: parsed.quizzes && typeof parsed.quizzes === "object" ? parsed.quizzes : {},
      bookmarks: parsed.bookmarks && typeof parsed.bookmarks === "object" ? parsed.bookmarks : {},
    };
  } catch {
    return { completed: {}, notes: {}, scroll: {}, quizzes: {}, bookmarks: {} };
  }
}

function bookmarkFor(assignmentId) {
  if (!assignmentId) return null;
  const raw = progress.bookmarks?.[assignmentId];
  if (!raw || typeof raw !== "object") return null;
  const sectionId = text(raw.sectionId);
  const paragraphIndex = Number(raw.paragraphIndex);
  if (!sectionId || !Number.isInteger(paragraphIndex) || paragraphIndex < 0) return null;
  return { sectionId, paragraphIndex, updatedAt: raw.updatedAt };
}

function setBookmark(assignmentId, sectionId, paragraphIndex) {
  if (!assignmentId || !sectionId) return;
  if (!progress.bookmarks || typeof progress.bookmarks !== "object") progress.bookmarks = {};
  progress.bookmarks[assignmentId] = {
    sectionId,
    paragraphIndex,
    updatedAt: new Date().toISOString(),
  };
  saveProgress();
}

function clearBookmark(assignmentId) {
  if (!assignmentId || !progress.bookmarks) return;
  delete progress.bookmarks[assignmentId];
  saveProgress();
}

function bookmarkDomId(sectionId, paragraphIndex) {
  return `line-${sectionId}-${paragraphIndex}`;
}

function paraDomId(assignmentId, sectionId, paragraphIndex) {
  return `p:${assignmentId}:${sectionId}:${paragraphIndex}`;
}

function loadAnnotations() {
  try {
    const raw = localStorage.getItem(ANNOTATION_KEY);
    if (!raw) return { highlights: [], notes: [] };
    const parsed = JSON.parse(raw);
    return {
      highlights: sanitizeHighlights(parsed.highlights),
      notes: sanitizeNotes(parsed.notes),
    };
  } catch {
    return { highlights: [], notes: [] };
  }
}

function sanitizeHighlights(list) {
  if (!Array.isArray(list)) return [];
  const out = [];
  const seen = new Set();
  for (const item of list) {
    if (!item || typeof item !== "object") continue;
    const assignmentId = text(item.assignmentId);
    const sectionId = text(item.sectionId);
    const paragraphIndex = Number(item.paragraphIndex);
    if (!assignmentId || !sectionId || !Number.isInteger(paragraphIndex) || paragraphIndex < 0) continue;
    const id = text(item.id, paraDomId(assignmentId, sectionId, paragraphIndex));
    if (seen.has(id)) continue;
    seen.add(id);
    out.push({
      id,
      assignmentId,
      sectionId,
      paragraphIndex,
      createdAt: text(item.createdAt, new Date().toISOString()),
    });
  }
  return out;
}

function sanitizeNotes(list) {
  if (!Array.isArray(list)) return [];
  const out = [];
  const seen = new Set();
  for (const item of list) {
    if (!item || typeof item !== "object") continue;
    const assignmentId = text(item.assignmentId);
    const sectionId = text(item.sectionId);
    const paragraphIndex = Number(item.paragraphIndex);
    const body = text(item.text);
    if (!assignmentId || !sectionId || !Number.isInteger(paragraphIndex) || paragraphIndex < 0 || !body) continue;
    const id = text(item.id, paraDomId(assignmentId, sectionId, paragraphIndex));
    if (seen.has(id)) continue;
    seen.add(id);
    out.push({
      id,
      assignmentId,
      sectionId,
      paragraphIndex,
      text: body,
      createdAt: text(item.createdAt, new Date().toISOString()),
      updatedAt: text(item.updatedAt, text(item.createdAt, new Date().toISOString())),
    });
  }
  return out;
}

let storageWarningEl = null;

function isQuotaError(err) {
  if (!err) return false;
  if (err.name === "QuotaExceededError" || err.name === "NS_ERROR_DOM_QUOTA_REACHED") return true;
  if (err.code === 22) return true;
  return /quota/i.test(String(err.message || ""));
}

function showStorageWarning() {
  if (storageWarningEl) {
    storageWarningEl.hidden = false;
    return;
  }
  storageWarningEl = document.createElement("aside");
  storageWarningEl.id = "storage-warning";
  storageWarningEl.className = "storage-warning";
  storageWarningEl.setAttribute("role", "alert");
  storageWarningEl.innerHTML = `<p class="storage-warning-text">Browser storage is full. Your notes and progress may not save until you free space or export them.</p>
    <div class="storage-warning-actions">
      <button type="button" class="btn btn-secondary" data-export="md">Export Markdown</button>
      <button type="button" class="btn btn-secondary" data-export="json">Export JSON</button>
      <button type="button" class="btn-ghost storage-warning-dismiss">Dismiss</button>
    </div>`;
  const header = document.querySelector(".site-header");
  if (header) header.insertAdjacentElement("afterend", storageWarningEl);
  else document.body.insertBefore(storageWarningEl, appEl);
  storageWarningEl.querySelector(".storage-warning-dismiss")?.addEventListener("click", () => {
    storageWarningEl.hidden = true;
  });
}

function safeSetItem(key, value) {
  try {
    localStorage.setItem(key, value);
    return true;
  } catch (err) {
    if (isQuotaError(err)) showStorageWarning();
    return false;
  }
}

function saveAnnotations() {
  safeSetItem(ANNOTATION_KEY, JSON.stringify(annotations));
}

function coordsFromPara(para) {
  if (!para) return null;
  const assignmentId = text(para.getAttribute("data-assignment-id"));
  const sectionId = text(para.getAttribute("data-section-id"));
  const paragraphIndex = Number(para.getAttribute("data-para-index"));
  if (!assignmentId || !sectionId || !Number.isInteger(paragraphIndex) || paragraphIndex < 0) return null;
  return { assignmentId, sectionId, paragraphIndex };
}

function highlightAt(assignmentId, sectionId, paragraphIndex) {
  const id = paraDomId(assignmentId, sectionId, paragraphIndex);
  return (
    annotations.highlights.find(
      (h) =>
        h.id === id ||
        (h.assignmentId === assignmentId && h.sectionId === sectionId && h.paragraphIndex === paragraphIndex)
    ) || null
  );
}

function noteAt(assignmentId, sectionId, paragraphIndex) {
  const id = paraDomId(assignmentId, sectionId, paragraphIndex);
  return (
    annotations.notes.find(
      (n) =>
        n.id === id ||
        (n.assignmentId === assignmentId && n.sectionId === sectionId && n.paragraphIndex === paragraphIndex)
    ) || null
  );
}

function toggleHighlight(assignmentId, sectionId, paragraphIndex) {
  const existing = highlightAt(assignmentId, sectionId, paragraphIndex);
  if (existing) {
    annotations.highlights = annotations.highlights.filter((h) => h.id !== existing.id);
  } else {
    annotations.highlights.push({
      id: paraDomId(assignmentId, sectionId, paragraphIndex),
      assignmentId,
      sectionId,
      paragraphIndex,
      createdAt: new Date().toISOString(),
    });
  }
  saveAnnotations();
}

function upsertParaNote(assignmentId, sectionId, paragraphIndex, value) {
  const id = paraDomId(assignmentId, sectionId, paragraphIndex);
  const body = text(value);
  const existing = noteAt(assignmentId, sectionId, paragraphIndex);
  if (!body) {
    annotations.notes = annotations.notes.filter((n) => n.id !== (existing ? existing.id : id));
    saveAnnotations();
    return;
  }
  const now = new Date().toISOString();
  if (existing) {
    existing.text = body;
    existing.updatedAt = now;
  } else {
    annotations.notes.push({
      id,
      assignmentId,
      sectionId,
      paragraphIndex,
      text: body,
      createdAt: now,
      updatedAt: now,
    });
  }
  saveAnnotations();
}

function notesForAssignment(assignmentId) {
  return annotations.notes
    .filter((n) => n.assignmentId === assignmentId)
    .sort((a, b) => a.sectionId.localeCompare(b.sectionId) || a.paragraphIndex - b.paragraphIndex);
}

function sittingNotesListHtml(assignmentId) {
  const notes = notesForAssignment(assignmentId);
  if (!notes.length) {
    return `<div class="empty-state empty-state--compact">
        <p class="empty-state-title">No notes yet</p>
        <p class="empty-state-hint">Tap ✎ on any paragraph to jot a margin note. It stays in this browser.</p>
      </div>`;
  }
  return `<ul class="sitting-note-list">${notes
    .map((n) => {
      const excerpt = n.text.length > 90 ? `${n.text.slice(0, 90)}…` : n.text;
      return `<li><button type="button" class="sitting-note-jump" data-jump-para="${escapeHtml(n.id)}">${escapeHtml(excerpt)}</button></li>`;
    })
    .join("")}</ul>`;
}

function exportMenuHtml(where) {
  return `<details class="export-menu" data-export-menu="${escapeHtml(where || "page")}">
      <summary>Export notes</summary>
      <div class="export-menu-panel" role="menu">
        <button type="button" data-export="md">Markdown</button>
        <button type="button" data-export="json">JSON</button>
      </div>
    </details>`;
}

function courseTracks() {
  const raw = (course && course.tracks) || (course && course.course && course.course.tracks);
  const list = Array.isArray(raw) ? raw : [];
  return list.filter((t) => t && text(t.id));
}

function trackById(id) {
  if (!id) return null;
  return courseTracks().find((t) => t.id === id) || null;
}

function tracksForAssignment(assignment) {
  if (!assignment) return [];
  const explicit = new Set(listOf(assignment.trackIds));
  return courseTracks().filter((t) => explicit.has(t.id) || listOf(t.assignmentIds).includes(assignment.id));
}

function trackBadgeHtml(assignment) {
  const tracks = tracksForAssignment(assignment);
  if (!tracks.length) return "";
  return tracks
    .map(
      (t) =>
        `<a class="track-badge" href="#/track/${encodeURIComponent(t.id)}">${escapeHtml(text(t.title, t.id))}</a>`
    )
    .join("");
}

function trackItems(track) {
  const out = [];
  const seen = new Set();
  for (const id of listOf(track && track.assignmentIds)) {
    if (seen.has(id)) continue;
    seen.add(id);
    const found = readingById(id);
    if (found) out.push(found);
  }
  return out;
}

function trackCardsHtml() {
  const tracks = courseTracks();
  if (!tracks.length) return "";
  return `<section class="track-cards" aria-label="Reading tracks">
      ${tracks
        .map((t) => {
          const items = trackItems(t);
          const done = items.filter((item) => isComplete(item.assignment.id)).length;
          const pct = items.length ? Math.round((done / items.length) * 100) : 0;
          return `<article class="track-card">
            <p class="here-label">Track</p>
            <h2><a href="#/track/${encodeURIComponent(t.id)}">${escapeHtml(text(t.title, t.id))}</a></h2>
            ${text(t.subtitle) ? `<p class="meta-line">${escapeHtml(t.subtitle)}</p>` : ""}
            <div class="track-card-progress" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100" aria-label="${done} of ${items.length} sittings complete">
              <span class="track-card-progress-fill" style="width:${pct}%"></span>
            </div>
            <p class="muted">${done} of ${items.length} sittings in this thread</p>
            <p class="actions"><a class="btn btn-secondary" href="#/track/${encodeURIComponent(t.id)}">Open the thread</a></p>
          </article>`;
        })
        .join("")}
    </section>`;
}

function assignmentExportMeta(assignmentId) {
  const item = readingById(assignmentId);
  if (!item) return { assignmentId, missing: true };
  const a = item.assignment;
  return {
    assignmentId,
    assignmentTitle: text(a.title, a.work),
    author: text(a.author),
    work: text(a.work),
    locator: text(a.text && a.text.locator, text(a.pages, a.selection)),
    thinker: formatThinkerNames(thinkersForAssignment(a, item.unit, item.era)),
    eraTitle: text(item.era && item.era.title),
  };
}

function resolveSection(sections, sectionId) {
  for (let i = 0; i < sections.length; i++) {
    const sid = text(sections[i] && sections[i].id) || `anon-${i}`;
    if (sid === sectionId) return sections[i];
  }
  return null;
}

async function paragraphQuote(assignmentId, sectionId, paragraphIndex) {
  const item = readingById(assignmentId);
  if (!item || !hasInAppText(item.assignment)) return "";
  try {
    const doc = await loadTextDoc(item.assignment.text);
    const sections = scopedSections(doc, item.assignment.text);
    const sec = resolveSection(sections, sectionId);
    const paras = listOf(sec && sec.paragraphs);
    return text(paras[paragraphIndex]);
  } catch {
    return "";
  }
}

function downloadFile(filename, mime, content) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function exportPayload() {
  const highlights = [];
  for (const h of annotations.highlights) {
    highlights.push({
      ...h,
      paragraphId: paraDomId(h.assignmentId, h.sectionId, h.paragraphIndex),
      ...assignmentExportMeta(h.assignmentId),
    });
  }
  const notes = [];
  for (const n of annotations.notes) {
    notes.push({
      ...n,
      paragraphId: paraDomId(n.assignmentId, n.sectionId, n.paragraphIndex),
      ...assignmentExportMeta(n.assignmentId),
    });
  }
  return { exportedAt: new Date().toISOString(), highlights, notes };
}

async function exportMarkdown() {
  const data = await exportPayload();
  const byAssignment = new Map();
  const add = (item, kind) => {
    const id = item.assignmentId;
    if (!byAssignment.has(id)) byAssignment.set(id, { meta: assignmentExportMeta(id), entries: new Map() });
    const bucket = byAssignment.get(id);
    const key = paraDomId(item.assignmentId, item.sectionId, item.paragraphIndex);
    if (!bucket.entries.has(key)) {
      bucket.entries.set(key, {
        sectionId: item.sectionId,
        paragraphIndex: item.paragraphIndex,
        paragraphId: key,
        highlight: false,
        note: "",
      });
    }
    const entry = bucket.entries.get(key);
    if (kind === "highlight") entry.highlight = true;
    if (kind === "note") entry.note = item.text;
  };
  for (const h of data.highlights) add(h, "highlight");
  for (const n of data.notes) add(n, "note");

  const order = readings.map((r) => r.assignment.id);
  const ids = [...byAssignment.keys()].sort((a, b) => {
    const ia = order.indexOf(a);
    const ib = order.indexOf(b);
    return (ia < 0 ? 9999 : ia) - (ib < 0 ? 9999 : ib);
  });

  const lines = [
    "# pjilosophy notes",
    "",
    `Exported ${data.exportedAt}. Local study file — not synced.`,
    "",
  ];
  if (!ids.length) {
    lines.push("No highlights or paragraph notes yet.");
    return `${lines.join("\n")}\n`;
  }
  for (const assignmentId of ids) {
    const bucket = byAssignment.get(assignmentId);
    const meta = bucket.meta;
    const heading = meta.thinker || meta.author || "Unknown";
    lines.push(`## ${heading} — ${meta.assignmentTitle || assignmentId}`);
    const locBits = [meta.work, meta.locator, meta.eraTitle].filter(Boolean);
    if (locBits.length) lines.push(`*${locBits.join(" · ")}*`);
    lines.push("");
    const entries = [...bucket.entries.values()].sort(
      (a, b) => a.sectionId.localeCompare(b.sectionId) || a.paragraphIndex - b.paragraphIndex
    );
    for (const entry of entries) {
      lines.push(`### ${entry.sectionId} · ¶ ${entry.paragraphIndex + 1}`);
      lines.push("");
      lines.push(`\`${entry.paragraphId}\``);
      lines.push("");
      const quote = await paragraphQuote(assignmentId, entry.sectionId, entry.paragraphIndex);
      if (quote) {
        for (const qline of quote.split("\n")) lines.push(`> ${qline}`);
        lines.push("");
      } else {
        lines.push("*Passage is not in this edition (or is bibliographic).*");
        lines.push("");
      }
      if (entry.note) {
        lines.push(entry.note);
        lines.push("");
      } else if (entry.highlight) {
        lines.push("*Highlighted.*");
        lines.push("");
      }
    }
  }
  return `${lines.join("\n").trim()}\n`;
}

async function runExport(kind) {
  if (kind === "json") {
    const data = await exportPayload();
    downloadFile("pjilosophy-notes.json", "application/json", `${JSON.stringify(data, null, 2)}\n`);
    return;
  }
  const md = await exportMarkdown();
  downloadFile("pjilosophy-notes.md", "text/markdown", md);
}

function saveProgress() {
  safeSetItem(STORAGE_KEY, JSON.stringify(progress));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function text(value, fallback = "") {
  if (value == null) return fallback;
  const s = String(value).trim();
  return s || fallback;
}

function listOf(value) {
  return Array.isArray(value) ? value.filter((item) => text(item)) : [];
}

function safeUrl(url) {
  if (!url) return "";
  try {
    const parsed = new URL(String(url), window.location.href);
    if (parsed.protocol === "http:" || parsed.protocol === "https:") return parsed.href;
  } catch {
    return "";
  }
  return "";
}

function minutesLabel(minutes) {
  const n = Number(minutes);
  if (!Number.isFinite(n) || n <= 0) return "";
  if (n < 60) return `${Math.round(n)} min`;
  const hours = n / 60;
  const rounded = hours >= 10 ? Math.round(hours) : Math.round(hours * 10) / 10;
  return `${rounded} hr`;
}

function byOrder(a, b) {
  return (Number(a.order) || 0) - (Number(b.order) || 0);
}

function flattenCourse(data) {
  const eras = [...(data.eras || [])].sort(byOrder);
  const flat = [];
  for (const era of eras) {
    const units = [...(era.units || [])].sort(byOrder);
    for (const unit of units) {
      const assignments = [...(unit.assignments || [])].sort(byOrder);
      for (const assignment of assignments) {
        if (!assignment || !assignment.id) continue;
        flat.push({
          assignment,
          unit,
          era,
        });
      }
    }
  }
  return flat.map((item, index) => ({
    ...item,
    index,
    prevId: index > 0 ? flat[index - 1].assignment.id : null,
    nextId: index < flat.length - 1 ? flat[index + 1].assignment.id : null,
  }));
}

function readingById(id) {
  return readings.find((item) => item.assignment.id === id) || null;
}

function isComplete(id) {
  return Boolean(progress.completed[id]);
}

function nextUnread() {
  return readings.find((item) => !isComplete(item.assignment.id)) || null;
}

function eraComplete(era) {
  const ids = readings.filter((item) => item.era.id === era.id).map((item) => item.assignment.id);
  return ids.length > 0 && ids.every((id) => isComplete(id));
}

function completedCount() {
  return readings.filter((item) => isComplete(item.assignment.id)).length;
}

function quizzesCompletedCount() {
  return flattenQuizzes(course).filter((item) => isQuizComplete(item.quizId)).length;
}

function progressRingHtml(pct, label) {
  const r = 42;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - Math.min(100, Math.max(0, pct)) / 100);
  return `<div class="progress-ring" role="img" aria-label="${escapeHtml(label)}">
      <svg viewBox="0 0 96 96" aria-hidden="true">
        <circle class="progress-ring-bg" cx="48" cy="48" r="${r}"/>
        <circle class="progress-ring-fill" cx="48" cy="48" r="${r}" stroke-dasharray="${circumference.toFixed(2)}" stroke-dashoffset="${offset.toFixed(2)}"/>
      </svg>
      <span class="progress-ring-text"><strong>${pct}</strong><span class="progress-ring-unit">%</span></span>
    </div>`;
}

function homeStatsHtml() {
  const total = readings.length;
  const done = completedCount();
  const pct = total ? Math.round((done / total) * 100) : 0;
  const erasDone = erasCompletedCount();
  const eraTotal = (course.eras || []).length;
  const quizTotal = flattenQuizzes(course).length;
  const quizzesDone = quizzesCompletedCount();
  const hoursLeft = remainingMinutes() ? minutesLabel(remainingMinutes()) : "none listed";
  return `<div class="dashboard-stats" aria-label="Course progress">
      ${progressRingHtml(pct, `${done} of ${total} readings complete`)}
      <dl class="stat-grid">
        <div class="stat-item"><dt>Readings</dt><dd><strong>${done}</strong> of ${total}</dd></div>
        <div class="stat-item"><dt>Eras</dt><dd><strong>${erasDone}</strong> of ${eraTotal}</dd></div>
        <div class="stat-item"><dt>Quizzes</dt><dd><strong>${quizzesDone}</strong> of ${quizTotal}</dd></div>
        <div class="stat-item"><dt>Time left</dt><dd>~<strong>${escapeHtml(hoursLeft)}</strong></dd></div>
      </dl>
    </div>`;
}

function bookmarkCalloutHtml(assignment) {
  if (!assignment?.id || !bookmarkFor(assignment.id)) return "";
  const href = `#/text/${encodeURIComponent(assignment.id)}`;
  return `<aside class="bookmark-callout" aria-label="Resume reading">
      <p class="bookmark-callout-label">Resume your line</p>
      <p class="bookmark-callout-text">You marked a paragraph in this sitting. Pick up where you stopped.</p>
      <p class="actions"><a class="btn" href="${href}">Continue from your line</a></p>
    </aside>`;
}

function remainingMinutes() {
  return readings.reduce((sum, item) => {
    if (isComplete(item.assignment.id)) return sum;
    const n = Number(item.assignment.estimatedMinutes);
    return sum + (Number.isFinite(n) ? n : 0);
  }, 0);
}

function erasCompletedCount() {
  const eras = [...(course.eras || [])];
  return eras.filter((era) => eraComplete(era)).length;
}

function parseRoute() {
  const raw = (location.hash || "#/").replace(/^#/, "") || "/";
  const qIndex = raw.indexOf("?");
  const pathOnly = qIndex >= 0 ? raw.slice(0, qIndex) : raw;
  const query = new URLSearchParams(qIndex >= 0 ? raw.slice(qIndex + 1) : "");
  const path = pathOnly.startsWith("/") ? pathOnly : `/${pathOnly}`;
  const parts = path.split("/").filter(Boolean);
  if (parts.length === 0) return { name: "home" };
  if (parts[0] === "tracks") return { name: "tracks" };
  if (parts[0] === "track" && parts[1]) return { name: "track", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "syllabus") return { name: "syllabus" };
  if (parts[0] === "era" && parts[1]) return { name: "era", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "read" && parts[1]) return { name: "read", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "text" && parts[1]) {
    return {
      name: "text",
      id: decodeURIComponent(parts[1]),
      fromStart: query.get("from") === "start",
    };
  }
  if (parts[0] === "quizzes") return { name: "quizzes" };
  if (parts[0] === "quiz" && parts[1]) return { name: "quiz", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "recap" && parts[1]) return { name: "recap", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "terms") {
    if (parts[1]) return { name: "term", id: decodeURIComponent(parts[1]) };
    return { name: "terms" };
  }
  return { name: "home" };
}

function setNav(routeName) {
  if (routeName === "home") navContinue.setAttribute("aria-current", "page");
  else navContinue.removeAttribute("aria-current");
  if (routeName === "syllabus") navSyllabus.setAttribute("aria-current", "page");
  else navSyllabus.removeAttribute("aria-current");
  if (navQuizzes) {
    if (routeName === "quizzes" || routeName === "quiz" || routeName === "recap") {
      navQuizzes.setAttribute("aria-current", "page");
    } else {
      navQuizzes.removeAttribute("aria-current");
    }
  }
  if (navTerms) {
    if (routeName === "terms" || routeName === "term") {
      navTerms.setAttribute("aria-current", "page");
    } else {
      navTerms.removeAttribute("aria-current");
    }
  }
  if (navTracks) {
    if (routeName === "tracks" || routeName === "track") {
      navTracks.setAttribute("aria-current", "page");
    } else {
      navTracks.removeAttribute("aria-current");
    }
  }
}

function updateProgressChrome() {
  const total = readings.length;
  const done = completedCount();
  const pct = total ? Math.round((done / total) * 100) : 0;
  progressFill.style.width = `${pct}%`;
  progressRail.setAttribute("aria-valuenow", String(pct));
  progressRail.setAttribute("aria-valuetext", `${done} of ${total} readings complete`);
}

function kindLabel(kind) {
  if (kind === "secondary") return "Secondary";
  if (kind === "bibliographic") return "Bibliographic";
  return "Primary";
}

function difficultyInfo(assignment) {
  const n = Number(assignment && assignment.difficulty);
  if (n === 1) return { n: 1, label: "Accessible" };
  if (n === 2) return { n: 2, label: "Intermediate" };
  if (n === 3) return { n: 3, label: "Advanced" };
  return null;
}

function wordCountLabel(assignment) {
  const n = Number(assignment && assignment.wordCount);
  if (!Number.isFinite(n) || n <= 0) return "";
  const rounded = n >= 400 ? Math.round(n / 100) * 100 : Math.round(n);
  return `~${rounded.toLocaleString("en-US")} words`;
}

function isPublicDomainSitting(assignment) {
  if (!assignment) return false;
  if (hasInAppText(assignment)) return true;
  const source = assignment.source || {};
  const license = text(source.license).toLowerCase().replace(/_/g, "-");
  if (license.includes("public-domain") || license.includes("public domain") || license === "pd") return true;
  return source.available === true;
}

function readingTagsHtml(assignment) {
  const diff = difficultyInfo(assignment);
  const words = wordCountLabel(assignment);
  if (!diff && !words) return "";
  const tagged = isPublicDomainSitting(assignment);
  return `<span class="reading-tags${tagged ? " is-tagged" : ""}">
      ${
        diff
          ? `<span class="diff-pill" data-diff="${diff.n}" aria-label="Difficulty ${diff.n} of 3: ${escapeHtml(diff.label)}"><span class="diff-n" aria-hidden="true">${diff.n}</span> ${escapeHtml(diff.label)}</span>`
          : ""
      }
      ${words ? `<span class="word-count">${escapeHtml(words)}</span>` : ""}
    </span>`;
}

function metaBits(assignment) {
  const bits = [];
  if (text(assignment.author)) bits.push(text(assignment.author));
  if (text(assignment.work)) bits.push(text(assignment.work));
  const pages = text(assignment.pages) || text(assignment.selection);
  if (pages) bits.push(pages);
  const time = minutesLabel(assignment.estimatedMinutes);
  if (time) bits.push(time);
  return bits;
}

function sourceAvailable(assignment) {
  const source = assignment.source || {};
  return source.available === true && Boolean(safeUrl(source.url));
}

function isBibliographic(assignment) {
  const source = assignment.source || {};
  return assignment.kind === "bibliographic" || source.available === false;
}

function hasInAppText(assignment) {
  const pointer = assignment && assignment.text;
  return Boolean(pointer && (pointer.id || pointer.path));
}

function assignmentHref(assignment) {
  if (!assignment?.id) return "#/";
  if (hasInAppText(assignment)) return `#/text/${encodeURIComponent(assignment.id)}`;
  return `#/read/${encodeURIComponent(assignment.id)}`;
}

function readCtaHtml(assignment) {
  if (!hasInAppText(assignment)) return "";
  const href = `#/text/${encodeURIComponent(assignment.id)}`;
  if (bookmarkFor(assignment.id)) {
    return `<a class="btn" href="${href}">Continue from your line</a>
            <a class="btn btn-secondary" href="${href}?from=start">Start from the beginning</a>`;
  }
  return `<a class="btn" href="${href}">Read in the app</a>`;
}

function neighborHref(assignmentId) {
  const found = readingById(assignmentId);
  return found ? assignmentHref(found.assignment) : "#/";
}

function textUrls(pointer) {
  const urls = [];
  const path = text(pointer?.path);
  const id = text(pointer?.id);
  if (path) {
    const cleaned = path.replace(/^\.\//, "").replace(/^\/+/, "");
    urls.push(`./content/${cleaned}`);
    urls.push(`./${cleaned}`);
  }
  if (id) {
    urls.push(`./content/texts/${id}.json`);
    urls.push(`./texts/${id}.json`);
  }
  return [...new Set(urls)];
}

async function loadTextDoc(pointer) {
  const cacheKey = text(pointer?.id) || text(pointer?.path);
  if (cacheKey && textCache.has(cacheKey)) return textCache.get(cacheKey);
  let lastError = null;
  for (const url of textUrls(pointer)) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        lastError = new Error(`${url} → ${res.status}`);
        continue;
      }
      const data = await res.json();
      if (data && Array.isArray(data.sections)) {
        if (cacheKey) textCache.set(cacheKey, data);
        return data;
      }
      lastError = new Error(`${url} did not match the text schema`);
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError || new Error("Text file could not be loaded");
}

function scopedSections(doc, pointer) {
  const sections = Array.isArray(doc?.sections) ? doc.sections : [];
  const start = text(pointer?.start);
  const end = text(pointer?.end);
  if (!start && !end) return sections;
  let from = 0;
  let to = sections.length - 1;
  if (start) {
    const i = sections.findIndex((section) => section && section.id === start);
    if (i >= 0) from = i;
  }
  if (end) {
    const i = sections.findIndex((section) => section && section.id === end);
    if (i >= 0) to = i;
  }
  if (to < from) {
    const swap = from;
    from = to;
    to = swap;
  }
  return sections.slice(from, to + 1);
}

function cacheKeyFor(pointer) {
  return text(pointer?.id) || text(pointer?.path);
}

function usableQuiz(quiz) {
  return Boolean(
    quiz &&
      typeof quiz === "object" &&
      Array.isArray(quiz.questions) &&
      quiz.questions.some((question) => question && text(question.prompt))
  );
}

function quizIdFor(quiz, fallback) {
  return text(quiz && quiz.id, fallback);
}

function assignmentQuizHref(assignment) {
  if (!assignment?.id) return "#/quizzes";
  return `#/quiz/${encodeURIComponent(assignment.id)}`;
}

function recapHref(unit) {
  if (!unit?.id) return "#/quizzes";
  return `#/recap/${encodeURIComponent(unit.id)}`;
}

function quizCta(assignment) {
  if (usableQuiz(assignment && assignment.quiz)) {
    const record = quizRecord(quizIdFor(assignment.quiz, `${assignment.id}-quiz`));
    const label = record.completed ? "Review the quiz" : "Take the quiz";
    return `<p class="actions quiz-cta-row">
        <a class="btn btn-secondary" href="${assignmentQuizHref(assignment)}">${label}</a>
      </p>
      <p class="muted quiz-meant">Meant after the reading, not instead of it.</p>`;
  }
  return `<p class="muted">Quiz not ready for this reading.</p>`;
}

function flattenQuizzes(data) {
  const out = [];
  const eras = [...(data.eras || [])].sort(byOrder);
  for (const era of eras) {
    const units = [...(era.units || [])].sort(byOrder);
    for (const unit of units) {
      const assignments = [...(unit.assignments || [])].sort(byOrder);
      for (const assignment of assignments) {
        if (!usableQuiz(assignment.quiz)) continue;
        out.push({
          kind: "assignment",
          quiz: assignment.quiz,
          quizId: quizIdFor(assignment.quiz, `${assignment.id}-quiz`),
          assignment,
          unit,
          era,
        });
      }
      if (usableQuiz(unit.recapQuiz)) {
        out.push({
          kind: "recap",
          quiz: unit.recapQuiz,
          quizId: quizIdFor(unit.recapQuiz, `${unit.id}-recap`),
          unit,
          era,
        });
      }
    }
  }
  return out;
}

function findUnitById(unitId) {
  for (const era of course.eras || []) {
    for (const unit of era.units || []) {
      if (unit && unit.id === unitId) return { unit, era };
    }
  }
  return null;
}

function quizRecord(quizId) {
  const rec = progress.quizzes && progress.quizzes[quizId];
  if (!rec || typeof rec !== "object") {
    return { completed: false, lastScore: null, lastTotal: null, bestScore: null, bestTotal: null, session: null };
  }
  return rec;
}

function isQuizComplete(quizId) {
  return Boolean(quizRecord(quizId).completed);
}

function quizQuestions(quiz) {
  return Array.isArray(quiz?.questions) ? quiz.questions.filter((q) => q && text(q.prompt)) : [];
}

function quizOptions(question) {
  const type = text(question?.type, "multiple-choice");
  const raw = Array.isArray(question?.options) ? question.options.filter((opt) => opt && text(opt.id)) : [];
  if (type === "true-false" && raw.length < 2) {
    return [
      { id: "true", text: "True" },
      { id: "false", text: "False" },
    ];
  }
  return raw;
}

function questionType(question) {
  const type = text(question?.type, "multiple-choice");
  if (type === "multiple-select" || type === "true-false" || type === "multiple-choice") return type;
  if (quizOptions(question).length) return "multiple-choice";
  return "unknown";
}

function selectedFromForm(form) {
  if (!form) return [];
  const inputs = [...form.querySelectorAll("input[name='answer']:checked")];
  return inputs.map((el) => el.value);
}

function isSelectionCorrect(question, selected) {
  const type = questionType(question);
  const chosen = [...selected].map(String).sort();
  if (type === "multiple-select") {
    const want = Array.isArray(question.correct)
      ? question.correct.map(String).sort()
      : question.correct != null
        ? [String(question.correct)]
        : [];
    return JSON.stringify(want) === JSON.stringify(chosen);
  }
  let want = question.correct;
  if (typeof want === "boolean") want = want ? "true" : "false";
  if (want == null) return false;
  return chosen.length === 1 && chosen[0] === String(want);
}

function persistQuizSession() {
  if (!quizSession) return;
  if (!progress.quizzes || typeof progress.quizzes !== "object") progress.quizzes = {};
  const prev = quizRecord(quizSession.id);
  progress.quizzes[quizSession.id] = {
    ...prev,
    session: quizSession.finished
      ? null
      : { index: quizSession.index, responses: quizSession.responses, finished: false },
  };
  saveProgress();
}

function finishQuizAttempt() {
  if (!quizSession) return;
  const questions = quizQuestions(quizSession.quiz);
  let score = 0;
  for (const q of questions) {
    const qid = text(q.id, questions.indexOf(q).toString());
    if (quizSession.responses[qid]?.correct) score += 1;
  }
  const total = questions.length;
  const prev = quizRecord(quizSession.id);
  const bestScore =
    prev.bestScore == null ? score : Math.max(Number(prev.bestScore) || 0, score);
  quizSession.finished = true;
  quizSession.lastScore = score;
  quizSession.lastTotal = total;
  if (!progress.quizzes || typeof progress.quizzes !== "object") progress.quizzes = {};
  progress.quizzes[quizSession.id] = {
    completed: true,
    lastScore: score,
    lastTotal: total,
    bestScore,
    bestTotal: total,
    session: null,
  };
  saveProgress();
}

function ensureQuizSession(kind, ownerId) {
  let quiz = null;
  let fallbackId = "";
  const meta = { kind, ownerId };
  if (kind === "quiz") {
    const item = readingById(ownerId);
    quiz = item?.assignment?.quiz || null;
    fallbackId = `${ownerId}-quiz`;
    meta.assignment = item?.assignment;
    meta.unit = item?.unit;
    meta.era = item?.era;
    meta.item = item;
  } else {
    const found = findUnitById(ownerId);
    quiz = found?.unit?.recapQuiz || null;
    fallbackId = `${ownerId}-recap`;
    meta.unit = found?.unit;
    meta.era = found?.era;
  }
  const id = quizIdFor(quiz, fallbackId);
  if (quizSession && quizSession.id === id && quizSession.kind === kind) return quizSession;
  const stored = quizRecord(id);
  if (stored.session && stored.session.finished === false) {
    quizSession = {
      id,
      kind,
      ownerId,
      quiz,
      meta,
      index: Number.isFinite(stored.session.index) ? stored.session.index : 0,
      responses: stored.session.responses && typeof stored.session.responses === "object" ? { ...stored.session.responses } : {},
      finished: false,
    };
    return quizSession;
  }
  if (stored.completed && !stored.session) {
    quizSession = {
      id,
      kind,
      ownerId,
      quiz,
      meta,
      index: quizQuestions(quiz).length,
      responses: {},
      finished: true,
      lastScore: stored.lastScore,
      lastTotal: stored.lastTotal,
    };
    return quizSession;
  }
  quizSession = {
    id,
    kind,
    ownerId,
    quiz,
    meta,
    index: 0,
    responses: {},
    finished: false,
  };
  return quizSession;
}

function quizStatusLabel(quizId) {
  const rec = quizRecord(quizId);
  if (rec.session && rec.session.finished === false) {
    const extra = rec.completed && rec.bestScore != null ? ` · best ${rec.bestScore}/${rec.bestTotal}` : "";
    return `In progress${extra}`;
  }
  if (rec.completed && rec.lastScore != null) {
    const best =
      rec.bestScore != null && rec.bestScore !== rec.lastScore ? ` · best ${rec.bestScore}/${rec.bestTotal}` : "";
    return `${rec.lastScore}/${rec.lastTotal}${best}`;
  }
  return "Not started";
}

function assignmentCount(data) {
  let n = 0;
  for (const era of data.eras || []) {
    for (const unit of era.units || []) {
      const assignments = unit.assignments || [];
      for (const assignment of assignments) {
        if (assignment && assignment.id) n += 1;
      }
    }
  }
  return n;
}

function quizTally(data) {
  let quizzes = 0;
  let recaps = 0;
  for (const era of data.eras || []) {
    for (const unit of era.units || []) {
      if (usableQuiz(unit.recapQuiz)) recaps += 1;
      for (const assignment of unit.assignments || []) {
        if (usableQuiz(assignment && assignment.quiz)) quizzes += 1;
      }
    }
  }
  return { quizzes, recaps };
}

function looksLikeStub(data) {
  const desc = text(data.course && data.course.description);
  if (/placeholder syllabus/i.test(desc)) return true;
  for (const era of data.eras || []) {
    if (String(era && era.id ? era.id : "").startsWith("stub-")) return true;
    for (const unit of era.units || []) {
      for (const assignment of unit.assignments || []) {
        if (String(assignment && assignment.id ? assignment.id : "").startsWith("stub-")) return true;
      }
    }
  }
  return false;
}

async function fetchCourse(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  const data = await res.json();
  if (!data || !Array.isArray(data.eras)) {
    throw new Error(`${url} did not match the course schema`);
  }
  return data;
}

async function loadCourse() {
  let primaryError = null;
  try {
    const data = await fetchCourse(COURSE_URLS[0]);
    if (!looksLikeStub(data)) return data;
  } catch (err) {
    primaryError = err;
  }
  try {
    return await fetchCourse(COURSE_URLS[1]);
  } catch (err) {
    throw primaryError || err || new Error("Course file could not be loaded");
  }
}

async function fetchGlossary(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  const data = await res.json();
  if (!data || !Array.isArray(data.terms)) {
    throw new Error(`${url} did not match the glossary schema`);
  }
  return data;
}

async function loadGlossary() {
  const loaded = [];
  for (const url of GLOSSARY_URLS) {
    try {
      loaded.push({ url, data: await fetchGlossary(url) });
    } catch {
      /* try the next path */
    }
  }
  if (!loaded.length) return { title: "Philosophical terms", intro: "", terms: [] };
  loaded.sort((a, b) => {
    const n = (b.data.terms || []).length - (a.data.terms || []).length;
    if (n) return n;
    return GLOSSARY_URLS.indexOf(a.url) - GLOSSARY_URLS.indexOf(b.url);
  });
  return loaded[0].data;
}

async function loadThinkers() {
  for (const url of THINKER_URLS) {
    try {
      const res = await fetch(url);
      if (!res.ok) continue;
      const data = await res.json();
      const list = Array.isArray(data)
        ? data
        : data && Array.isArray(data.thinkers)
          ? data.thinkers
          : [];
      if (list.length) return list.filter((t) => t && (t.id || t.name));
    } catch {
      /* try the next path */
    }
  }
  return [];
}

function thinkerCatalog() {
  return Array.isArray(thinkerIndex) ? thinkerIndex : [];
}

function thinkerById(id) {
  if (!id) return null;
  return thinkerCatalog().find((t) => t && t.id === id) || null;
}

function normalizePersonName(name) {
  return text(name)
    .replace(/\(.*?\)/g, "")
    .split(",")[0]
    .trim();
}

function thinkerByName(name) {
  const n = normalizePersonName(name).toLowerCase();
  if (!n) return null;
  const catalog = thinkerCatalog();
  const exact = catalog.find((t) => text(t.name).toLowerCase() === n);
  if (exact) return exact;
  const last = n.split(/\s+/).filter(Boolean).pop();
  if (last && last.length > 2) {
    const byLast = catalog.find((t) => {
      const parts = text(t.name).toLowerCase().split(/\s+/);
      return parts[parts.length - 1] === last;
    });
    if (byLast) return byLast;
  }
  return (
    catalog.find((t) => {
      const tn = text(t.name).toLowerCase();
      return tn.length > 3 && (n.includes(tn) || tn.includes(n));
    }) || null
  );
}

function asThinkerRecord(item) {
  if (!item) return null;
  if (typeof item === "string") {
    return thinkerById(item) || thinkerByName(item) || { id: item, name: item };
  }
  if (typeof item === "object") {
    const found = thinkerById(item.id) || thinkerByName(item.name);
    return (
      found || {
        id: item.id,
        name: text(item.name, item.id),
        image: item.image,
        imageCredit: item.imageCredit,
      }
    );
  }
  return null;
}

function uniqueThinkers(list) {
  const seen = new Set();
  const out = [];
  for (const t of list) {
    if (!t || !text(t.name, t.id)) continue;
    const key = text(t.id) || text(t.name).toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(t);
  }
  return out;
}

function resolveThinkers(source) {
  if (!source || typeof source !== "object") return [];
  const raw = [];
  if (source.thinkerId) raw.push(source.thinkerId);
  for (const id of listOf(source.thinkerIds)) raw.push(id);
  if (Array.isArray(source.thinkers)) raw.push(...source.thinkers);
  return uniqueThinkers(raw.map(asThinkerRecord));
}

function peopleFromAuthorString(author) {
  const cleaned = normalizePersonName(author);
  if (!cleaned) return [];
  const parts = cleaned.split(/\s+(?:and|&)\s+/i).map((p) => p.trim()).filter(Boolean);
  return uniqueThinkers(parts.map((name) => thinkerByName(name) || { name }));
}

function thinkersForAssignment(assignment, unit, era) {
  let list = resolveThinkers(assignment);
  if (!list.length && assignment) list = peopleFromAuthorString(assignment.author);
  if (!list.length && unit) list = resolveThinkers(unit);
  if (!list.length && era) list = resolveThinkers(era);
  return list;
}

function thinkersForUnit(unit, era) {
  let list = resolveThinkers(unit);
  if (list.length) return list;
  const derived = [];
  for (const assignment of unit?.assignments || []) {
    derived.push(...thinkersForAssignment(assignment, unit, era));
  }
  return uniqueThinkers(derived);
}

function thinkersForEra(era) {
  let list = resolveThinkers(era);
  if (list.length) return list.slice(0, 8);
  const derived = [];
  for (const unit of era?.units || []) {
    derived.push(...thinkersForUnit(unit, era));
  }
  return uniqueThinkers(derived).slice(0, 8);
}

function thinkersForTerm(term) {
  const aid = text(term && term.firstAppearsIn);
  const found = aid ? readingById(aid) : null;
  if (found) return thinkersForAssignment(found.assignment, found.unit, found.era).slice(0, 1);
  const eraId = listOf(term && term.eraIds)[0];
  const era = eraId ? eraById(eraId) : null;
  return era ? thinkersForEra(era).slice(0, 1) : [];
}

function formatThinkerNames(people) {
  const names = people.map((t) => text(t.name)).filter(Boolean);
  if (!names.length) return "";
  if (names.length === 1) return names[0];
  if (names.length === 2) return `${names[0]} & ${names[1]}`;
  return `${names.slice(0, -1).join(", ")} & ${names[names.length - 1]}`;
}

function portraitSrc(thinker) {
  const path = text(thinker && thinker.image);
  if (!path) return "";
  const cleaned = path.replace(/^\.\//, "").replace(/^\/+/, "");
  if (/^https?:/i.test(cleaned)) return "";
  if (cleaned.startsWith("content/")) return `./${cleaned}`;
  return `./content/${cleaned}`;
}

function portraitInitials(name) {
  const parts = text(name).split(/\s+/).filter(Boolean);
  if (parts.length >= 2) {
    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
  }
  const s = text(name);
  if (s.length >= 2) return s.slice(0, 2).toUpperCase();
  return s.charAt(0).toUpperCase() || "?";
}

function portraitHtml(thinker, size) {
  if (!thinker || !text(thinker.name, thinker.id)) return "";
  const src = portraitSrc(thinker);
  const credit = text(thinker.imageCredit);
  const label = text(thinker.name, thinker.id);
  const initials = portraitInitials(label);
  const tip = credit ? ` title="${escapeHtml(credit)}"` : "";
  const loading = size === "lg" ? "eager" : "lazy";
  const img = src
    ? `<img class="portrait-img" src="${escapeHtml(src)}" alt="" width="96" height="96" loading="${loading}" decoding="async"${tip}>`
    : "";
  return `<span class="portrait portrait--${size || "md"}${src ? "" : " no-photo"}" role="img" aria-label="${escapeHtml(label)}"${tip}>
      <span class="portrait-fallback" aria-hidden="true">${escapeHtml(initials)}</span>
      ${img}
    </span>`;
}

function portraitStackHtml(people, size) {
  if (!people.length) return "";
  if (people.length === 1) return portraitHtml(people[0], size);
  return `<span class="portrait-row">${people.map((t) => portraitHtml(t, size === "lg" ? "md" : "sm")).join("")}</span>`;
}

function thinkerBannerHtml(people, opts = {}) {
  const names = formatThinkerNames(people);
  const subtitle = text(opts.subtitle);
  if (!names && !subtitle) return "";
  const size = opts.size || "lg";
  const nameTag = opts.nameTag || "p";
  const subTag = opts.subTag || "p";
  const subClass = opts.subClass || "thinker-sub";
  const href = text(opts.href);
  const credit =
    size === "lg" && people.length === 1 && text(people[0] && people[0].imageCredit)
      ? `<span class="portrait-credit">${escapeHtml(people[0].imageCredit)}</span>`
      : "";
  const linked = (inner) => (href ? `<a href="${escapeHtml(href)}">${inner}</a>` : inner);
  const nameHtml = names ? `<${nameTag} class="thinker-name">${linked(escapeHtml(names))}</${nameTag}>` : "";
  const subHtml = subtitle ? `<${subTag} class="${subClass}">${linked(escapeHtml(subtitle))}</${subTag}>` : "";
  return `<div class="thinker-banner thinker-banner--${size}">
      ${people.length ? portraitStackHtml(people, size) : ""}
      <div class="thinker-banner-text">
        ${nameHtml}
        ${subHtml}
        ${credit}
      </div>
    </div>`;
}

function sittingMeta(assignment) {
  const bits = [];
  if (text(assignment.work)) bits.push(text(assignment.work));
  const pages = text(assignment.pages) || text(assignment.selection);
  if (pages) bits.push(pages);
  const time = minutesLabel(assignment.estimatedMinutes);
  if (time) bits.push(time);
  return bits;
}

function glossaryTerms() {
  return Array.isArray(glossary?.terms) ? glossary.terms.filter((t) => t && (t.id || t.term)) : [];
}

function termById(id) {
  if (!id) return null;
  return glossaryTerms().find((t) => t.id === id) || null;
}

function termSortKey(term) {
  return text(term.sortKey, text(term.term, term.id)).toLowerCase();
}

function sortedTerms() {
  return [...glossaryTerms()].sort((a, b) => termSortKey(a).localeCompare(termSortKey(b)));
}

function termsForAssignment(assignmentId) {
  if (!assignmentId) return [];
  return sortedTerms().filter(
    (t) => listOf(t.assignmentIds).includes(assignmentId) || text(t.firstAppearsIn) === assignmentId
  );
}

function erasOnTerms() {
  const ids = new Set();
  for (const term of glossaryTerms()) {
    for (const eraId of listOf(term.eraIds)) ids.add(eraId);
  }
  return [...(course?.eras || [])].filter((era) => ids.has(era.id)).sort(byOrder);
}

function eraById(id) {
  return (course?.eras || []).find((era) => era && era.id === id) || null;
}

function visibleTerms() {
  const q = glossaryUi.query.trim().toLowerCase();
  const era = glossaryUi.eraId;
  return sortedTerms().filter((term) => {
    if (era && !listOf(term.eraIds).includes(era)) return false;
    if (!q) return true;
    const hay = [term.term, term.id, term.short, term.definition, ...listOf(term.aliases)]
      .map((part) => String(part || ""))
      .join(" ")
      .toLowerCase();
    return hay.includes(q);
  });
}

function definitionParagraphs(definition) {
  const raw = text(definition);
  if (!raw) return [];
  return raw
    .split(/\n{2,}/)
    .map((p) => p.replace(/\s*\n\s*/g, " ").replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

function termsSittingHtml(assignmentId) {
  const terms = termsForAssignment(assignmentId);
  if (!terms.length) return "";
  const links = terms
    .map(
      (t) =>
        `<li><a href="#/terms/${encodeURIComponent(t.id)}">${escapeHtml(text(t.term, t.id))}</a>${
          text(t.short) ? ` — <span class="muted">${escapeHtml(t.short)}</span>` : ""
        }</li>`
    )
    .join("");
  return `<section class="panel">
      <h2>Terms in this sitting</h2>
      <ul class="term-sitting">${links}</ul>
    </section>`;
}

async function render() {
  if (!course) return;
  const gen = ++renderGen;
  const route = parseRoute();
  const isReader = route.name === "text";
  document.body.classList.toggle("reader-mode", isReader);
  setNav(route.name);
  updateProgressChrome();

  if (isReader) {
    const item = readingById(route.id);
    const key = cacheKeyFor(item?.assignment?.text);
    if (!key || !textCache.has(key)) {
      appEl.innerHTML = `<p class="loading-line">Opening the text…</p>`;
    }
    const html = await renderReader(route.id);
    if (gen !== renderGen) return;
    appEl.innerHTML = html;
    restoreReaderPosition(route.id, { fromStart: route.fromStart });
    appEl.focus({ preventScroll: true });
    return;
  }

  window.scrollTo(0, 0);
  if (route.name === "syllabus") {
    appEl.innerHTML = renderSyllabus();
  } else if (route.name === "era") {
    appEl.innerHTML = renderEra(route.id);
  } else if (route.name === "read") {
    appEl.innerHTML = renderAssignment(route.id);
  } else if (route.name === "quizzes") {
    appEl.innerHTML = renderQuizList();
  } else if (route.name === "quiz" || route.name === "recap") {
    appEl.innerHTML = renderQuizView(route.name, route.id);
  } else if (route.name === "terms") {
    appEl.innerHTML = renderTermsIndex();
  } else if (route.name === "term") {
    appEl.innerHTML = renderTermEntry(route.id);
  } else if (route.name === "tracks") {
    appEl.innerHTML = renderTracksIndex();
  } else if (route.name === "track") {
    appEl.innerHTML = renderTrack(route.id);
  } else {
    appEl.innerHTML = renderHome();
  }
  appEl.focus({ preventScroll: true });
}

function renderHome() {
  const info = course.course || {};
  const next = nextUnread();
  const stats = homeStatsHtml();

  if (!next) {
    return `
      <p class="kicker">${escapeHtml(text(info.title, "Western philosophy"))}</p>
      <h1 class="page-title">The sequence is finished.</h1>
      <p class="lede">That is not the same as finishing philosophy. Re-read the texts that still resist you. The syllabus remains open.</p>
      ${stats}
      <article class="done-card">
        <p class="here-label">Complete</p>
        <h2>You have marked every assignment.</h2>
        <p class="muted">If a later version of the reading list appears, refresh. New unread items will show up here.</p>
        <p class="actions">
          <a class="btn" href="#/syllabus">Review the syllabus</a>
          <a class="btn btn-secondary" href="#/tracks">Tracks</a>
          <a class="btn btn-secondary" href="#/quizzes">Quizzes</a>
        </p>
      </article>
      ${trackCardsHtml()}
    `;
  }

  const a = next.assignment;
  const people = thinkersForAssignment(a, next.unit, next.era);
  const bits = (people.length ? sittingMeta(a) : metaBits(a)).map(escapeHtml).join(" · ");
  const why = text(a.why);
  const sittingTitle = text(a.title, text(a.work, "Untitled assignment"));
  const hasBookmark = Boolean(bookmarkFor(a.id));

  return `
    <p class="kicker">${escapeHtml(text(info.subtitle, text(info.title)))}</p>
    <h1 class="page-title">We pick up here.</h1>
    ${stats}
    ${bookmarkCalloutHtml(a)}
    <article class="next-card${hasBookmark ? " next-card--bookmarked" : ""}">
      <p class="here-label">${hasBookmark ? "Your line" : "Next reading"}</p>
      ${
        people.length
          ? thinkerBannerHtml(people, { size: "lg", nameTag: "h2", subtitle: sittingTitle, subClass: "sitting-title" })
          : `<h2>${escapeHtml(sittingTitle)}</h2>`
      }
      <p class="meta-line">${bits}</p>
      ${readingTagsHtml(a)}
      ${trackBadgeHtml(a)}
      ${why ? `<p class="why-excerpt">${escapeHtml(why)}</p>` : ""}
      ${
        usableQuiz(a.quiz) && !isQuizComplete(quizIdFor(a.quiz, `${a.id}-quiz`))
          ? `<p class="muted">The check for this reading is still open. Take it after the pages, not before.</p>`
          : ""
      }
      <p class="actions">
        ${
          hasInAppText(a)
            ? `${readCtaHtml(a)}
               <a class="btn-ghost btn" href="#/read/${encodeURIComponent(a.id)}">Assignment notes</a>`
            : `<a class="btn" href="#/read/${encodeURIComponent(a.id)}">Open the assignment</a>`
        }
        ${usableQuiz(a.quiz) ? `<a class="btn-ghost btn" href="${assignmentQuizHref(a)}">Take the quiz</a>` : ""}
        <a class="btn-ghost btn" href="#/era/${encodeURIComponent(next.era.id)}">Era introduction</a>
      </p>
    </article>
    ${trackCardsHtml()}
  `;
}

function renderAssignment(id) {
  const item = readingById(id);
  if (!item) {
    return `
      <h1 class="page-title">That assignment is not on the list.</h1>
      <p class="lede">It may have been removed from a newer syllabus. Return to the next unread reading.</p>
      <p class="actions"><a class="btn" href="#/">Continue</a></p>
    `;
  }

  const a = item.assignment;
  const source = a.source || {};
  const done = isComplete(a.id);
  const available = sourceAvailable(a);
  const bibliographic = isBibliographic(a);
  const note = progress.notes[a.id] || "";
  const lookFor = listOf(a.lookFor);
  const questions = listOf(a.questions);
  const prereqs = listOf(a.prerequisites);
  const unitNote = text(item.unit.professorNote);
  const translator = text(a.translator);
  const locator = text(source.locator);
  const edition = text(source.edition);
  const href = safeUrl(source.url);

  const prereqHtml = prereqs.length
    ? `<p class="muted">Assumes: ${prereqs
        .map((pid) => {
          const found = readingById(pid);
          const label = found ? text(found.assignment.title, pid) : pid;
          return found
            ? `<a href="#/read/${encodeURIComponent(pid)}">${escapeHtml(label)}</a>`
            : escapeHtml(label);
        })
        .join("; ")}</p>`
    : "";

  const lookHtml = lookFor.length
    ? `<section class="panel">
        <h2>Look for</h2>
        <ul>${lookFor.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
      </section>`
    : "";

  const qHtml = questions.length
    ? `<section class="panel">
        <h2>Sit with these questions</h2>
        <ol>${questions.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ol>
      </section>`
    : "";

  const sourceBlock = hasInAppText(a)
    ? `<p class="source-open">
        ${readCtaHtml(a)}
        ${
          available && href
            ? `<a class="btn btn-secondary" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Another edition</a>`
            : ""
        }
      </p>
      ${bookmarkFor(a.id) ? `<p class="muted">A paragraph is marked in this sitting. Open it to pick up there, or start from the beginning.</p>` : ""}`
    : bibliographic || !available
      ? `<section class="panel legal-note">
        <h2>Obtain this legally</h2>
        <p>This text is not hosted here${a.kind === "bibliographic" ? " (bibliographic item)" : ""}. Get a printed or licensed copy — library, bookstore, or a database your school pays for. Do not use a pirated scan.</p>
        <p><strong>${escapeHtml(text(a.author, "Author unknown"))}</strong>, <em>${escapeHtml(text(a.work, text(a.title)))}</em>${text(a.selection) ? ` — ${escapeHtml(a.selection)}` : ""}${text(a.pages) ? `; ${escapeHtml(a.pages)}` : ""}.</p>
        ${edition ? `<p>Edition: ${escapeHtml(edition)}</p>` : ""}
        ${text(source.name) ? `<p>Suggested source: ${escapeHtml(source.name)}${locator ? ` (${escapeHtml(locator)})` : ""}.</p>` : ""}
        ${href ? `<p><a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Catalog or publisher page</a></p>` : ""}
      </section>`
      : `<p class="source-open">
        <a class="btn" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Open the text</a>
        <span class="muted">${escapeHtml(text(source.name, "External source"))}${locator ? ` · ${escapeHtml(locator)}` : ""}</span>
      </p>`;

  const prev = item.prevId
    ? `<a class="btn btn-secondary" href="${neighborHref(item.prevId)}" data-prev>Previous</a>`
    : `<span></span>`;
  const next = item.nextId
    ? `<a class="btn btn-secondary" href="${neighborHref(item.nextId)}" data-next>Next assignment</a>`
    : `<span></span>`;
  const people = thinkersForAssignment(a, item.unit, item.era);
  const sittingTitle = text(a.title, text(a.work, "Untitled"));
  const headBits = (people.length ? sittingMeta(a) : metaBits(a)).map(escapeHtml).join(" · ");

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/syllabus">Syllabus</a>
      <span class="crumb-sep">/</span>
      <a href="#/era/${encodeURIComponent(item.era.id)}">${escapeHtml(text(item.era.title, "Era"))}</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(text(item.unit.title, "Unit"))}</span>
    </nav>
    <header class="assignment-head">
      <p class="kicker">${escapeHtml(kindLabel(a.kind))}${done ? " · complete" : ""}</p>
      ${
        people.length
          ? thinkerBannerHtml(people, { size: "lg", nameTag: "h1", subtitle: sittingTitle, subClass: "sitting-title" })
          : `<h1>${escapeHtml(sittingTitle)}</h1>`
      }
      <p class="meta-line">${headBits}</p>
      ${readingTagsHtml(a)}
      ${trackBadgeHtml(a)}
    </header>
    <dl class="dl-meta">
      ${text(a.author) && !people.length ? `<dt>Author</dt><dd>${escapeHtml(a.author)}</dd>` : ""}
      ${text(a.work) ? `<dt>Work</dt><dd>${escapeHtml(a.work)}</dd>` : ""}
      ${translator ? `<dt>Translator</dt><dd>${escapeHtml(translator)}</dd>` : ""}
      ${text(a.selection) ? `<dt>Selection</dt><dd>${escapeHtml(a.selection)}</dd>` : ""}
      ${text(a.pages) ? `<dt>Pages</dt><dd>${escapeHtml(a.pages)}</dd>` : ""}
      ${minutesLabel(a.estimatedMinutes) ? `<dt>Time</dt><dd>${escapeHtml(minutesLabel(a.estimatedMinutes))}</dd>` : ""}
      ${difficultyInfo(a) ? `<dt>Difficulty</dt><dd>${difficultyInfo(a).n} · ${escapeHtml(difficultyInfo(a).label)}</dd>` : ""}
      ${wordCountLabel(a) ? `<dt>Length</dt><dd>${escapeHtml(wordCountLabel(a))}</dd>` : ""}
      ${edition ? `<dt>Edition</dt><dd>${escapeHtml(edition)}</dd>` : ""}
    </dl>
    ${prereqHtml}
    ${text(a.why) ? `<section class="panel why-panel"><h2>Why this</h2><p>${escapeHtml(a.why)}</p></section>` : ""}
    ${unitNote ? `<section class="panel"><h2>Why this now</h2><p>${escapeHtml(unitNote)}</p></section>` : ""}
    ${lookHtml}
    ${qHtml}
    ${sourceBlock}
    ${termsSittingHtml(a.id)}
    <section class="panel">
      <h2>After the reading</h2>
      ${quizCta(a)}
    </section>
    ${text(a.nextHint) ? `<p class="next-hint">${escapeHtml(a.nextHint)}</p>` : ""}
    <label class="notes-label" for="assignment-notes">Your notes (this browser only)</label>
    <textarea id="assignment-notes" class="notes" data-notes-for="${escapeHtml(a.id)}">${escapeHtml(note)}</textarea>
    <p class="actions">
      <button type="button" class="btn" data-toggle-complete="${escapeHtml(a.id)}">
        ${done ? "Mark unread" : "Mark complete"}
      </button>
      ${done && item.nextId ? `<a class="btn btn-secondary" href="${neighborHref(item.nextId)}">Continue to the next</a>` : ""}
    </p>
    <div class="pager">${prev}${next}</div>
    <p class="kbd-hint">j / k or arrow keys move to the next or previous assignment. They do nothing while you are typing notes.</p>
  `;
}

async function renderReader(id) {
  const item = readingById(id);
  if (!item) {
    return `
      <div class="reader-error">
        <h1 class="page-title">That assignment is not on the list.</h1>
        <p class="actions"><a class="btn" href="#/">Continue</a></p>
      </div>`;
  }

  const a = item.assignment;
  if (!hasInAppText(a)) {
    return renderAssignment(a.id);
  }

  let doc = null;
  let loadError = "";
  try {
    doc = await loadTextDoc(a.text);
  } catch (err) {
    loadError = err && err.message ? err.message : "Could not load the text.";
  }

  if (!doc) {
    const expected = text(a.text.path, a.text.id ? `texts/${a.text.id}.json` : "texts/…");
    const href = safeUrl(a.source && a.source.url);
    return `
      <div class="reader-error">
        <h1 class="page-title">The text is not on the shelf yet.</h1>
        <p class="lede">Expected a file at <code>content/${escapeHtml(expected)}</code>. ${escapeHtml(loadError)}</p>
        <p class="actions">
          <a class="btn" href="#/read/${encodeURIComponent(a.id)}">Open the assignment</a>
          ${
            href
              ? `<a class="btn btn-secondary" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Open an external edition</a>`
              : ""
          }
        </p>
      </div>`;
  }

  const sections = scopedSections(doc, a.text);
  const done = isComplete(a.id);
  const lookFor = listOf(a.lookFor);
  const questions = listOf(a.questions);
  const why = text(a.why);
  const translator = text(doc.translator, text(a.translator));
  const people = thinkersForAssignment(a, item.unit, item.era);
  const selection = text(a.text && a.text.locator, text(a.pages, text(a.selection)));
  const license = text(doc.license, "public-domain");
  const attribution = text(doc.attribution);
  const src = doc.source || {};
  const srcUrl = safeUrl(src.url);

  const marked = bookmarkFor(a.id);
  const sectionHtml = sections
    .map((sec, sIndex) => {
      const sid = text(sec && sec.id) || `anon-${sIndex}`;
      const paras = listOf(sec && sec.paragraphs);
      const heading = text(sec && sec.heading);
      const loc = text(sec && sec.locator);
      const paraHtml = paras
        .map((paragraph, i) => {
          const isMarked = marked && marked.sectionId === sid && marked.paragraphIndex === i;
          const isHi = Boolean(highlightAt(a.id, sid, i));
          const paraNote = noteAt(a.id, sid, i);
          const pid = paraDomId(a.id, sid, i);
          return `<div class="reader-para${isMarked ? " is-bookmarked" : ""}${isHi ? " is-highlighted" : ""}${paraNote ? " has-note" : ""}" id="${escapeHtml(pid)}" data-para-id="${escapeHtml(pid)}" data-assignment-id="${escapeHtml(a.id)}" data-section-id="${escapeHtml(sid)}" data-para-index="${i}">
            <span class="para-gutter">
              <button type="button" class="para-mark" data-bookmark-para aria-pressed="${isMarked ? "true" : "false"}" aria-label="${isMarked ? "Clear your line" : "Bookmark this paragraph"}">¶</button>
              <button type="button" class="para-hi" data-highlight-para aria-pressed="${isHi ? "true" : "false"}" aria-label="${isHi ? "Remove highlight" : "Highlight this paragraph"}">†</button>
              <button type="button" class="para-note-btn" data-open-note aria-expanded="false" aria-label="${paraNote ? "Edit note on this paragraph" : "Add a note on this paragraph"}">✎</button>
            </span>
            ${isMarked ? `<span class="para-ribbon">Your line</span>` : ""}
            <p class="para-body">${escapeHtml(paragraph)}</p>
            <div class="para-note-wrap" hidden>
              <label>
                <span class="para-note-label">Note on this paragraph</span>
                <textarea class="para-note" data-para-note rows="3">${paraNote ? escapeHtml(paraNote.text) : ""}</textarea>
              </label>
            </div>
          </div>`;
        })
        .join("");
      return `
        <section class="reader-section" id="sec-${escapeHtml(sid)}" data-section-id="${escapeHtml(sid)}">
          <div class="section-locator">
            ${loc ? `<span class="loc">${escapeHtml(loc)}</span>` : ""}
            ${heading ? `<h2>${escapeHtml(heading)}</h2>` : ""}
          </div>
          ${paraHtml}
        </section>`;
    })
    .join("");

  const guideBits = [];
  if (why) guideBits.push(`<h2>Why this</h2><p class="guide-why">${escapeHtml(why)}</p>`);
  if (lookFor.length) {
    guideBits.push(`<h2>Look for</h2><ul>${lookFor.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>`);
  }
  if (questions.length) {
    guideBits.push(`<h2>Questions</h2><ol>${questions.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ol>`);
  }
  const sittingTerms = termsForAssignment(a.id);
  if (sittingTerms.length) {
    guideBits.push(
      `<h2>Terms</h2><ul>${sittingTerms
        .map((t) => `<li><a href="#/terms/${encodeURIComponent(t.id)}">${escapeHtml(text(t.term, t.id))}</a></li>`)
        .join("")}</ul>`
    );
  }

  const prev = item.prevId
    ? `<a class="btn btn-secondary" href="${neighborHref(item.prevId)}">Previous</a>`
    : `<span></span>`;
  const next = item.nextId
    ? `<a class="btn btn-secondary" href="${neighborHref(item.nextId)}">Next assignment</a>`
    : `<span></span>`;

  return `
    <div class="reader-layout">
      <div class="reader-main">
        <div class="reader-toolbar">
          <a class="btn btn-ghost" href="#/read/${encodeURIComponent(a.id)}">Assignment</a>
          ${readingTagsHtml(a)}
          <p class="bookmark-status" id="bookmark-status" ${marked ? "" : "hidden"}>
            Your line is marked.
            <button type="button" class="btn btn-ghost" data-clear-bookmark>Clear</button>
          </p>
          ${exportMenuHtml("reader")}
          <p class="actions">
            ${
              usableQuiz(a.quiz)
                ? `<a class="btn btn-secondary" href="${assignmentQuizHref(a)}">Take the quiz</a>`
                : ""
            }
            <button type="button" class="btn" data-toggle-complete="${escapeHtml(a.id)}">
              ${done ? "Mark unread" : "Mark complete"}
            </button>
            ${done && item.nextId ? `<a class="btn btn-secondary" href="${neighborHref(item.nextId)}">Continue to the next</a>` : ""}
          </p>
        </div>
        <article class="reader-prose">
          <header>
            <p class="kicker">${escapeHtml(text(item.era.title))} · ${escapeHtml(kindLabel(a.kind))}${done ? " · complete" : ""}</p>
            ${thinkerBannerHtml(people, { size: "lg", nameTag: "p" })}
            <h1 class="work-title">${escapeHtml(text(doc.title, text(a.work, a.title)))}</h1>
            ${
              people.length
                ? translator
                  ? `<p class="work-byline">tr. ${escapeHtml(translator)}</p>`
                  : ""
                : `<p class="work-byline">${escapeHtml(text(doc.author, a.author))}${translator ? ` · tr. ${escapeHtml(translator)}` : ""}</p>`
            }
            <p class="work-assignment">${escapeHtml(selection)}</p>
          </header>
          ${sectionHtml || `<p class="muted">This file has no sections yet.</p>`}
          <footer class="reader-attribution">
            <p>${escapeHtml(attribution || `${text(doc.author)}, ${text(doc.title)}. ${license}.`)}</p>
            ${
              text(src.name) || srcUrl
                ? `<p>${escapeHtml(text(src.name))}${text(src.edition) ? ` · ${escapeHtml(src.edition)}` : ""}${
                    srcUrl
                      ? ` · <a href="${escapeHtml(srcUrl)}" target="_blank" rel="noopener noreferrer">Source edition</a>`
                      : ""
                  }</p>`
                : ""
            }
          </footer>
        </article>
        <div class="pager reader-pager">${prev}${next}</div>
        <p class="kbd-hint">¶ marks where you stopped. † highlights a passage. ✎ opens a local note. Press b for your line, h to highlight the paragraph in view. j / k move assignments.</p>
      </div>
      <div class="reader-side">
        ${
          guideBits.length
            ? `<details class="reader-guide" open><summary>Keep these in view</summary>${guideBits.join("")}</details>`
            : ""
        }
        <aside class="sitting-notes-panel" aria-label="Notes in this sitting">
          <h2>Notes in this sitting</h2>
          <div id="sitting-notes">${sittingNotesListHtml(a.id)}</div>
        </aside>
      </div>
    </div>
  `;
}

function nearestParagraphInView() {
  const paras = [...document.querySelectorAll(".reader-para")];
  if (!paras.length) return null;
  const line = window.innerHeight * 0.28;
  let chosen = paras[0];
  for (const para of paras) {
    const top = para.getBoundingClientRect().top;
    if (top <= line) chosen = para;
    else break;
  }
  return chosen;
}

function syncBookmarkUi(assignmentId) {
  const marked = bookmarkFor(assignmentId);
  document.querySelectorAll(".reader-para").forEach((para) => {
    const sid = para.getAttribute("data-section-id");
    const idx = Number(para.getAttribute("data-para-index"));
    const on = Boolean(marked && marked.sectionId === sid && marked.paragraphIndex === idx);
    para.classList.toggle("is-bookmarked", on);
    const btn = para.querySelector("[data-bookmark-para]");
    if (btn) {
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.setAttribute("aria-label", on ? "Clear your line" : "Bookmark this paragraph");
      btn.setAttribute("title", on ? "Clear your line" : "Mark this as your line");
    }
    let ribbon = para.querySelector(".para-ribbon");
    if (on && !ribbon) {
      ribbon = document.createElement("span");
      ribbon.className = "para-ribbon";
      ribbon.textContent = "Your line";
      const body = para.querySelector(".para-body");
      if (body) para.insertBefore(ribbon, body);
      else para.prepend(ribbon);
    } else if (!on && ribbon) {
      ribbon.remove();
    }
  });
  const status = document.getElementById("bookmark-status");
  if (status) status.hidden = !marked;
}

function syncAnnotUi(assignmentId) {
  document.querySelectorAll(".reader-para").forEach((para) => {
    const coords = coordsFromPara(para);
    if (!coords) return;
    const hi = Boolean(highlightAt(coords.assignmentId, coords.sectionId, coords.paragraphIndex));
    const note = noteAt(coords.assignmentId, coords.sectionId, coords.paragraphIndex);
    para.classList.toggle("is-highlighted", hi);
    para.classList.toggle("has-note", Boolean(note));
    const hiBtn = para.querySelector("[data-highlight-para]");
    if (hiBtn) {
      hiBtn.setAttribute("aria-pressed", hi ? "true" : "false");
      hiBtn.setAttribute("aria-label", hi ? "Remove highlight" : "Highlight this paragraph");
    }
    const noteBtn = para.querySelector("[data-open-note]");
    if (noteBtn) {
      noteBtn.setAttribute("aria-label", note ? "Edit note on this paragraph" : "Add a note on this paragraph");
    }
    const area = para.querySelector("[data-para-note]");
    if (area && document.activeElement !== area) area.value = note ? note.text : "";
  });
  const host = document.getElementById("sitting-notes");
  if (host) host.innerHTML = sittingNotesListHtml(assignmentId);
}

function jumpToPara(paraId) {
  const el = document.getElementById(paraId) || document.querySelector(`[data-para-id="${CSS.escape(paraId)}"]`);
  if (!el) return;
  const y = el.getBoundingClientRect().top + window.scrollY - 96;
  window.scrollTo(0, Math.max(0, y));
  el.classList.add("just-restored");
  window.setTimeout(() => el.classList.remove("just-restored"), 1600);
  const wrap = el.querySelector(".para-note-wrap");
  const btn = el.querySelector("[data-open-note]");
  if (wrap && btn) {
    closeParaNotes(wrap);
    wrap.hidden = false;
    btn.setAttribute("aria-expanded", "true");
    const area = wrap.querySelector("[data-para-note]");
    if (area) area.focus();
  }
}

function closeParaNotes(exceptWrap) {
  document.querySelectorAll(".para-note-wrap").forEach((wrap) => {
    if (exceptWrap && wrap === exceptWrap) return;
    const area = wrap.querySelector("[data-para-note]");
    if (area) commitParaNote(area);
    wrap.hidden = true;
    wrap.closest(".reader-para")?.querySelector("[data-open-note]")?.setAttribute("aria-expanded", "false");
  });
}

function commitParaNote(textarea) {
  if (!textarea) return;
  const para = textarea.closest(".reader-para");
  const coords = coordsFromPara(para);
  if (!coords) return;
  upsertParaNote(coords.assignmentId, coords.sectionId, coords.paragraphIndex, textarea.value);
  syncAnnotUi(coords.assignmentId);
  if (!text(textarea.value)) {
    const wrap = textarea.closest(".para-note-wrap");
    if (wrap) wrap.hidden = true;
    para?.querySelector("[data-open-note]")?.setAttribute("aria-expanded", "false");
  }
}

function toggleBookmarkAt(assignmentId, sectionId, paragraphIndex) {
  const existing = bookmarkFor(assignmentId);
  if (existing && existing.sectionId === sectionId && existing.paragraphIndex === paragraphIndex) {
    clearBookmark(assignmentId);
  } else {
    setBookmark(assignmentId, sectionId, paragraphIndex);
  }
  syncBookmarkUi(assignmentId);
}

function restoreReaderPosition(assignmentId, opts = {}) {
  const fromStart = Boolean(opts.fromStart);
  if (fromStart) {
    const item = readingById(assignmentId);
    const start = text(item?.assignment?.text?.start);
    const firstSection = document.querySelector(".reader-section");
    const target = start
      ? document.getElementById(`sec-${start}`) ||
        document.querySelector(`.reader-section[data-section-id="${CSS.escape(start)}"]`)
      : null;
    if (target && firstSection && target !== firstSection) {
      const y = target.getBoundingClientRect().top + window.scrollY - 96;
      window.scrollTo(0, Math.max(0, y));
    } else {
      window.scrollTo(0, 0);
    }
    const clean = `#/text/${encodeURIComponent(assignmentId)}`;
    if (location.hash !== clean) history.replaceState(null, "", `${location.pathname}${location.search}${clean}`);
    return;
  }

  const marked = bookmarkFor(assignmentId);
  if (marked) {
    const el =
      document.getElementById(paraDomId(assignmentId, marked.sectionId, marked.paragraphIndex)) ||
      document.getElementById(bookmarkDomId(marked.sectionId, marked.paragraphIndex)) ||
      document.querySelector(
        `.reader-para[data-section-id="${CSS.escape(marked.sectionId)}"][data-para-index="${marked.paragraphIndex}"]`
      );
    if (el) {
      const y = el.getBoundingClientRect().top + window.scrollY - 96;
      window.scrollTo(0, Math.max(0, y));
      el.classList.add("just-restored");
      window.setTimeout(() => el.classList.remove("just-restored"), 1600);
      return;
    }
  }

  const saved = progress.scroll?.[assignmentId];
  if (typeof saved === "number" && saved > 40) {
    window.scrollTo(0, saved);
    return;
  }
  const item = readingById(assignmentId);
  const start = text(item?.assignment?.text?.start);
  const firstSection = document.querySelector(".reader-section");
  const target = start
    ? document.getElementById(`sec-${start}`) ||
      document.querySelector(`.reader-section[data-section-id="${CSS.escape(start)}"]`)
    : null;
  if (target && firstSection && target !== firstSection) {
    const y = target.getBoundingClientRect().top + window.scrollY - 88;
    window.scrollTo(0, Math.max(0, y));
    return;
  }
  window.scrollTo(0, 0);
}

function snapshotScroll() {
  const route = parseRoute();
  if (route.name !== "text") return;
  if (!progress.scroll || typeof progress.scroll !== "object") progress.scroll = {};
  progress.scroll[route.id] = Math.round(window.scrollY);
}

function renderSyllabus() {
  const info = course.course || {};
  const current = nextUnread();
  const currentId = current ? current.assignment.id : null;
  const eras = [...(course.eras || [])].sort(byOrder);

  const eraHtml = eras
    .map((era) => {
      const units = [...(era.units || [])].sort(byOrder);
      const unitHtml = units
        .map((unit) => {
          const assignments = [...(unit.assignments || [])].sort(byOrder);
          const items = assignments
            .map((a) => {
              if (!a?.id) return "";
              const done = isComplete(a.id);
              const currentClass = a.id === currentId ? " current" : "";
              const who = formatThinkerNames(thinkersForAssignment(a, unit, era));
              const bits = sittingMeta(a).slice(0, 3).map(escapeHtml).join(" · ");
              const time = minutesLabel(a.estimatedMinutes);
              return `
                <li>
                  <a class="${currentClass}" href="${assignmentHref(a)}" ${a.id === currentId ? 'aria-current="location"' : ""}>
                    <span class="mark ${done ? "done" : ""}" aria-hidden="true">${done ? "✓" : "○"}</span>
                    <span>
                      ${who ? `<span class="asg-who">${escapeHtml(who)}</span>` : ""}
                      <span class="asg-title">${escapeHtml(text(a.title, text(a.work, "Untitled")))}</span>
                      <span class="kind-pill">${escapeHtml(kindLabel(a.kind))}</span>
                      ${trackBadgeHtml(a)}
                      ${bookmarkFor(a.id) ? `<span class="line-mark" title="A line is marked">¶</span>` : ""}
                    </span>
                    <span class="asg-time">${escapeHtml(time)}</span>
                    <span class="asg-sub">${bits}${readingTagsHtml(a)}</span>
                  </a>
                </li>`;
            })
            .join("");
          const unitPeople = thinkersForUnit(unit, era);
          const unitDone = assignments.filter((asg) => asg?.id && isComplete(asg.id)).length;
          return `
            <details class="unit-accordion"${unitDone === assignments.length && assignments.length ? "" : " open"}>
              <summary class="unit-summary">
                ${thinkerBannerHtml(unitPeople, {
                  size: "md",
                  nameTag: "p",
                  subtitle: text(unit.title, "Unit"),
                  subTag: "h3",
                  subClass: "unit-title",
                })}
                <span class="unit-progress">${unitDone}/${assignments.length}</span>
              </summary>
              ${
                usableQuiz(unit.recapQuiz)
                  ? `<p class="era-intro-link"><a href="${recapHref(unit)}">Unit recap quiz</a> · ${escapeHtml(quizStatusLabel(quizIdFor(unit.recapQuiz, `${unit.id}-recap`)))}</p>`
                  : ""
              }
              <ul class="assignment-list">${items}</ul>
            </details>`;
        })
        .join("");

      const done = eraComplete(era);
      const eraPeople = thinkersForEra(era);
      const eraHref = `#/era/${encodeURIComponent(era.id)}`;
      const eraAssignmentCount = units.reduce((n, u) => n + (u.assignments || []).filter((asg) => asg?.id).length, 0);
      const eraDoneCount = readings.filter((r) => r.era.id === era.id && isComplete(r.assignment.id)).length;
      return `
        <section class="era-block${done ? " era-block--complete" : ""}">
          <div class="era-head">
            ${thinkerBannerHtml(eraPeople, {
              size: "md",
              nameTag: "p",
              subtitle: text(era.title, "Era"),
              subTag: "h2",
              subClass: "era-title-sub",
              href: eraHref,
            })}
            <div class="era-meta">
              <span class="era-years">${escapeHtml(text(era.years))}</span>
              <span class="era-progress-badge${done ? " is-complete" : ""}">${eraDoneCount}/${eraAssignmentCount}${done ? " · complete" : ""}</span>
            </div>
          </div>
          <p class="era-intro-link"><a href="${eraHref}">Professor’s introduction</a></p>
          ${unitHtml}
        </section>`;
    })
    .join("");

  return `
    <p class="kicker">${escapeHtml(text(info.title, "Course"))}</p>
    <h1 class="page-title">Syllabus</h1>
    <p class="lede">${escapeHtml(text(info.description, "The full sequence, in order. You may browse ahead. Home always names the next unread assignment."))}</p>
    <div class="toolbar">
      <button type="button" class="btn btn-secondary" data-print>Print or save as PDF</button>
    </div>
    <p class="print-only">${escapeHtml(text(info.title))}</p>
    ${trackCardsHtml()}
    <div class="syllabus">${eraHtml}</div>
  `;
}

function renderTracksIndex() {
  const tracks = courseTracks();
  if (!tracks.length) {
    return `
      <p class="kicker">Threads through the syllabus</p>
      <h1 class="page-title">Tracks</h1>
      <p class="lede">No tracks yet. When the syllabus names a thread — for example Philosophy of Science & Epistemology — it will appear here.</p>
      <p class="actions"><a class="btn btn-secondary" href="#/syllabus">Syllabus</a></p>
    `;
  }
  return `
    <p class="kicker">Threads through the syllabus</p>
    <h1 class="page-title">Tracks</h1>
    <p class="lede">These cut across eras. Read the main sequence in order; use a track when you want one argument followed through.</p>
    ${trackCardsHtml()}
  `;
}

function renderTrack(id) {
  const track = trackById(id);
  if (!track) {
    return `
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="#/tracks">Tracks</a>
        <span class="crumb-sep">/</span>
        <span>Missing</span>
      </nav>
      <h1 class="page-title">That track is not on the syllabus.</h1>
      <p class="lede">${courseTracks().length ? "It may have been renamed. Return to Tracks." : "No tracks yet."}</p>
      <p class="actions"><a class="btn" href="#/tracks">Tracks</a></p>
    `;
  }

  const items = trackItems(track);
  const done = items.filter((item) => isComplete(item.assignment.id)).length;
  const pct = items.length ? Math.round((done / items.length) * 100) : 0;
  const rows = items
    .map((item, index) => {
      const a = item.assignment;
      const who = formatThinkerNames(thinkersForAssignment(a, item.unit, item.era));
      const bits = sittingMeta(a).slice(0, 3).map(escapeHtml).join(" · ");
      const time = minutesLabel(a.estimatedMinutes);
      const markedDone = isComplete(a.id);
      const isLast = index === items.length - 1;
      return `
        <li class="track-step${markedDone ? " is-done" : ""}${isLast ? " is-last" : ""}">
          <span class="track-node" aria-hidden="true"></span>
          <a href="${assignmentHref(a)}">
            <span class="mark ${markedDone ? "done" : ""}" aria-hidden="true">${markedDone ? "✓" : "○"}</span>
            <span>
              ${who ? `<span class="asg-who">${escapeHtml(who)}</span>` : ""}
              <span class="asg-title">${escapeHtml(text(a.title, text(a.work, "Untitled")))}</span>
              <span class="kind-pill">${escapeHtml(kindLabel(a.kind))}</span>
              ${bookmarkFor(a.id) ? `<span class="line-mark" title="A line is marked">¶</span>` : ""}
            </span>
            <span class="asg-time">${escapeHtml(time)}</span>
            <span class="asg-sub">${bits}${readingTagsHtml(a)}</span>
          </a>
        </li>`;
    })
    .join("");

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/tracks">Tracks</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(text(track.title, track.id))}</span>
    </nav>
    <p class="kicker">Track</p>
    <h1 class="page-title">${escapeHtml(text(track.title, track.id))}</h1>
    ${text(track.subtitle) ? `<p class="lede">${escapeHtml(track.subtitle)}</p>` : ""}
    <div class="track-header-stats">
      <div class="track-card-progress track-card-progress--wide" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100" aria-label="${done} of ${items.length} sittings complete">
        <span class="track-card-progress-fill" style="width:${pct}%"></span>
      </div>
      <p class="muted">${done} of ${items.length} sittings complete</p>
    </div>
    <div class="panel">
      <h2>Professor’s note</h2>
      <p>${escapeHtml(text(track.intro, "No introduction was provided for this track."))}</p>
    </div>
    ${
      items.length
        ? `<ol class="track-timeline assignment-list">${rows}</ol>`
        : `<div class="empty-state"><p class="empty-state-title">No sittings linked</p><p class="empty-state-hint">This track names no readings on the current syllabus.</p></div>`
    }
    <p class="actions"><a class="btn btn-secondary" href="#/syllabus">Full syllabus</a></p>
  `;
}

function renderEra(id) {
  const era = (course.eras || []).find((item) => item.id === id);
  if (!era) {
    return `
      <h1 class="page-title">That era is not on the syllabus.</h1>
      <p class="actions"><a class="btn" href="#/syllabus">Back to the syllabus</a></p>
    `;
  }

  const themes = listOf(era.themes);
  const firstUnread = readings.find((item) => item.era.id === era.id && !isComplete(item.assignment.id));
  const firstInEra = readings.find((item) => item.era.id === era.id);
  const target = firstUnread || firstInEra;
  const done = eraComplete(era);
  const eraPeople = thinkersForEra(era);

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/syllabus">Syllabus</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(text(era.title, "Era"))}</span>
    </nav>
    <p class="kicker">${escapeHtml(text(era.years, "Era"))}${done ? " · complete" : ""}</p>
    ${
      eraPeople.length
        ? thinkerBannerHtml(eraPeople, {
            size: "lg",
            nameTag: "h1",
            subtitle: text(era.title, "Untitled era"),
            subClass: "era-page-sub",
          })
        : `<h1 class="page-title">${escapeHtml(text(era.title, "Untitled era"))}</h1>`
    }
    ${themes.length ? `<ul class="themes">${themes.map((t) => `<li>${escapeHtml(t)}</li>`).join("")}</ul>` : ""}
    <div class="panel">
      <h2>Professor’s note</h2>
      <p>${escapeHtml(text(era.intro, "No introduction was provided for this era."))}</p>
    </div>
    <p class="actions">
      ${
        target
          ? `<a class="btn" href="${assignmentHref(target.assignment)}">${
              firstUnread ? "Begin the next unread reading" : "Open the first reading"
            }</a>`
          : ""
      }
      <a class="btn btn-secondary" href="#/syllabus">Full syllabus</a>
    </p>
  `;
}

function renderTermIndexRows(terms) {
  if (!terms.length) {
    const hasFilter = Boolean(glossaryUi.query.trim() || glossaryUi.eraId);
    return `<li class="empty-state">
        <p class="empty-state-title">${hasFilter ? "No terms match" : "No terms yet"}</p>
        <p class="empty-state-hint">${
          hasFilter
            ? "Try a shorter phrase, a different era, or clear the filters above."
            : "The glossary will populate as terms are added to the course."
        }</p>
      </li>`;
  }
  let letter = "";
  const parts = [];
  for (const term of terms) {
    const next = termSortKey(term).charAt(0).toUpperCase();
    const heading = /[A-Z]/.test(next) ? next : "#";
    if (heading !== letter) {
      letter = heading;
      parts.push(`<li class="term-letter" aria-hidden="true">${escapeHtml(letter)}</li>`);
    }
    const href = term.id ? `#/terms/${encodeURIComponent(term.id)}` : "#/terms";
    parts.push(`
      <li>
        <a class="term-row" href="${href}">
          <span class="asg-title">${escapeHtml(text(term.term, term.id))}</span>
          ${text(term.short) ? `<span class="asg-sub">${escapeHtml(term.short)}</span>` : ""}
        </a>
      </li>`);
  }
  return parts.join("");
}

function renderTermsIndex() {
  const all = glossaryTerms();
  const visible = visibleTerms();
  const eras = erasOnTerms();
  const info = glossary || {};
  if (!all.length) {
    return `
      <p class="kicker">Vocabulary</p>
      <h1 class="page-title">Terms</h1>
      <p class="lede">The glossary is not on the table yet. Place a file at <code>content/glossary.json</code> and refresh.</p>
    `;
  }

  const chips = [
    `<button type="button" class="term-chip${!glossaryUi.eraId ? " is-on" : ""}" data-era-filter="" ${!glossaryUi.eraId ? 'aria-pressed="true"' : 'aria-pressed="false"'}>All eras</button>`,
    ...eras.map((era) => {
      const on = glossaryUi.eraId === era.id;
      return `<button type="button" class="term-chip${on ? " is-on" : ""}" data-era-filter="${escapeHtml(era.id)}" ${on ? 'aria-pressed="true"' : 'aria-pressed="false"'}>${escapeHtml(text(era.title, era.id))}</button>`;
    }),
  ].join("");

  return `
    <p class="kicker">Vocabulary for the course</p>
    <h1 class="page-title">${escapeHtml(text(info.title, "Terms"))}</h1>
    ${text(info.intro) ? `<p class="lede">${escapeHtml(info.intro)}</p>` : ""}
    <div class="term-tools">
      <label class="term-search-label" for="term-search">Search</label>
      <input id="term-search" class="term-search" type="search" data-term-search placeholder="Term, alias, or phrase" value="${escapeHtml(glossaryUi.query)}" autocomplete="off" />
      ${eras.length ? `<div class="term-chips" role="group" aria-label="Filter by era">${chips}</div>` : ""}
      <p class="muted" id="term-count">${visible.length} of ${all.length}</p>
    </div>
    <ul class="term-index" id="term-index">${renderTermIndexRows(visible)}</ul>
  `;
}

function renderTermEntry(id) {
  const term = termById(id);
  if (!term) {
    return `
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="#/terms">Terms</a>
        <span class="crumb-sep">/</span>
        <span>Missing</span>
      </nav>
      <h1 class="page-title">That term is not in the glossary.</h1>
      <p class="actions"><a class="btn" href="#/terms">All terms</a></p>
    `;
  }

  const aliases = listOf(term.aliases);
  const paras = definitionParagraphs(term.definition);
  const see = listOf(term.seeAlso);
  const assignmentIds = [...new Set([text(term.firstAppearsIn), ...listOf(term.assignmentIds)].filter(Boolean))];
  const eraIds = listOf(term.eraIds);
  const people = thinkersForTerm(term);

  const seeHtml = see.length
    ? `<div class="term-see"><span class="term-see-label">See also</span> ${see
        .map((sid) => {
          const found = termById(sid);
          const label = found ? text(found.term, sid) : sid;
          return found
            ? `<a class="term-pill" href="#/terms/${encodeURIComponent(sid)}">${escapeHtml(label)}</a>`
            : `<span class="term-pill term-pill--plain">${escapeHtml(label)}</span>`;
        })
        .join("")}</div>`
    : "";

  const whereHtml = assignmentIds.length
    ? `<section class="panel">
        <h2>In the course</h2>
        <ul>${assignmentIds
          .map((aid) => {
            const found = readingById(aid);
            if (!found) return `<li>${escapeHtml(aid)}</li>`;
            const first = text(term.firstAppearsIn) === aid;
            return `<li><a href="${assignmentHref(found.assignment)}">${escapeHtml(
              text(found.assignment.title, aid)
            )}</a>${first ? " <span class=\"muted\">(first appears)</span>" : ""} · ${escapeHtml(
              text(found.era.title)
            )}</li>`;
          })
          .join("")}</ul>
      </section>`
    : "";

  const eraHtml = eraIds.length
    ? `<p class="muted">Eras: ${eraIds
        .map((eid) => {
          const era = eraById(eid);
          return era
            ? `<a href="#/era/${encodeURIComponent(eid)}">${escapeHtml(text(era.title, eid))}</a>`
            : escapeHtml(eid);
        })
        .join("; ")}</p>`
    : "";

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/terms">Terms</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(text(term.term, term.id))}</span>
    </nav>
    <article class="term-entry">
      <p class="kicker">Definition</p>
      <div class="term-entry-head">
        ${people.length ? portraitHtml(people[0], "md") : ""}
        <div>
          <h1 class="page-title">${escapeHtml(text(term.term, term.id))}</h1>
          ${aliases.length ? `<p class="term-aliases">${aliases.map((a) => escapeHtml(a)).join(" · ")}</p>` : ""}
        </div>
      </div>
      ${
        text(term.short)
          ? `<p class="term-short">${escapeHtml(term.short)}</p>`
          : ""
      }
      ${
        paras.length
          ? `<div class="term-def-block">${paras.map((p) => `<p class="term-def">${escapeHtml(p)}</p>`).join("")}</div>`
          : !text(term.short)
            ? `<div class="empty-state empty-state--compact"><p class="empty-state-title">No definition yet</p></div>`
            : ""
      }
      ${seeHtml}
      ${eraHtml}
      ${whereHtml}
      <p class="actions"><a class="btn btn-secondary" href="#/terms">All terms</a></p>
    </article>
  `;
}

function renderQuizList() {
  const items = flattenQuizzes(course);
  if (!items.length) {
    return `
      <p class="kicker">Checks</p>
      <h1 class="page-title">Quizzes</h1>
      <p class="lede">No quizzes are on the syllabus yet. When the reading list includes them, they will appear here.</p>
    `;
  }

  const completed = items.filter((item) => isQuizComplete(item.quizId)).length;
  const rows = items
    .map((item) => {
      const status = quizStatusLabel(item.quizId);
      const rec = quizRecord(item.quizId);
      const href = item.kind === "recap" ? recapHref(item.unit) : assignmentQuizHref(item.assignment);
      const kind = item.kind === "recap" ? "Unit recap" : "After reading";
      const title = text(item.quiz.title, item.kind === "recap" ? text(item.unit.title) : text(item.assignment.title));
      const where = item.kind === "recap"
        ? `${text(item.era.title)} · ${text(item.unit.title)}`
        : `${text(item.era.title)} · ${text(item.assignment.author)} · ${text(item.assignment.work)}`;
      const markClass = rec.completed ? "done" : rec.session ? "current-mark" : "";
      const glyph = rec.completed ? "✓" : rec.session ? "◌" : "○";
      return `
        <li>
          <a class="${rec.session && !rec.completed ? " current" : ""}" href="${href}">
            <span class="mark ${markClass}" aria-hidden="true">${glyph}</span>
            <span>
              <span class="asg-title">${escapeHtml(title)}</span>
              <span class="kind-pill">${escapeHtml(kind)}</span>
            </span>
            <span class="asg-time">${escapeHtml(status)}</span>
            <span class="asg-sub">${escapeHtml(where)}</span>
          </a>
        </li>`;
    })
    .join("");

  return `
    <p class="kicker">Checks on the reading</p>
    <h1 class="page-title">Quizzes</h1>
    <p class="lede">These follow the pages. They are a check, not a prize. You may open one before you have read; you should not.</p>
    <p class="quiz-summary muted"><strong>${completed}</strong> of ${items.length} checks completed</p>
    <ul class="assignment-list quiz-list">${rows}</ul>
  `;
}

function renderQuizView(kind, ownerId) {
  const session = ensureQuizSession(kind, ownerId);
  if (!usableQuiz(session.quiz)) {
    const back = kind === "recap" ? "#/quizzes" : ownerId ? `#/read/${encodeURIComponent(ownerId)}` : "#/quizzes";
    return `
      <h1 class="page-title">Quiz not ready for this reading.</h1>
      <p class="lede">The syllabus has not attached a check yet. Read the assignment; return here when questions appear.</p>
      <p class="actions"><a class="btn" href="${back}">Back</a></p>
    `;
  }

  const questions = quizQuestions(session.quiz);
  if (!questions.length) {
    return `
      <h1 class="page-title">Quiz not ready for this reading.</h1>
      <p class="actions"><a class="btn" href="#/quizzes">All quizzes</a></p>
    `;
  }

  if (session.finished || session.index >= questions.length) {
    if (!session.finished) finishQuizAttempt();
    return renderQuizResults(session);
  }

  const q = questions[session.index];
  const qid = text(q.id, String(session.index));
  const type = questionType(q);
  const options = quizOptions(q);
  const submitted = session.responses[qid];
  const n = session.index + 1;
  const crumbTitle =
    session.kind === "recap"
      ? text(session.meta.unit && session.meta.unit.title, "Unit recap")
      : text(session.meta.assignment && session.meta.assignment.title, "Assignment");

  if (type === "unknown" || !options.length) {
    return `
      <article class="quiz-card">
        <p class="kicker">Question ${n} of ${questions.length}</p>
        <h1 class="page-title">${escapeHtml(text(session.quiz.title, "Quiz"))}</h1>
        <p class="lede">${escapeHtml(text(q.prompt))}</p>
        <p class="muted">This question cannot be shown (missing options or an unknown type).</p>
        <p class="actions">
          <button type="button" class="btn" data-quiz-skip>Skip</button>
        </p>
      </article>
    `;
  }

  const inputType = type === "multiple-select" ? "checkbox" : "radio";
  const optionHtml = options
    .map((opt) => {
      const oid = text(opt.id);
      const chosen = submitted ? (submitted.selected || []).includes(oid) : false;
      const showMark = Boolean(submitted);
      let extra = "";
      if (showMark) {
        extra = submitted.correct && chosen ? " is-right" : !submitted.correct && chosen ? " is-wrong" : "";
      }
      return `
        <label class="quiz-option${extra}">
          <input type="${inputType}" name="answer" value="${escapeHtml(oid)}" ${chosen ? "checked" : ""} ${submitted ? "disabled" : ""} />
          <span>${escapeHtml(text(opt.text, oid))}</span>
        </label>`;
    })
    .join("");

  const hint =
    type === "multiple-select"
      ? "Select every option that holds."
      : type === "true-false"
        ? "True or false, as the text has it."
        : "Choose the best account.";

  const feedback = submitted
    ? `<div class="quiz-feedback ${submitted.correct ? "is-right" : "is-wrong"}" role="status">
        <p class="quiz-verdict">${submitted.correct ? "Yes." : "No."}</p>
        ${text(q.explanation) ? `<p>${escapeHtml(q.explanation)}</p>` : ""}
      </div>
      <p class="actions">
        <button type="button" class="btn" data-quiz-next>${session.index + 1 >= questions.length ? "See the score" : "Next question"}</button>
      </p>`
    : `<p class="actions">
        <button type="submit" class="btn">Check this answer</button>
      </p>`;

  const backHref =
    session.kind === "recap"
      ? "#/quizzes"
      : `#/read/${encodeURIComponent(session.ownerId)}`;

  const quizPct = Math.round((n / questions.length) * 100);

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/quizzes">Quizzes</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(crumbTitle)}</span>
    </nav>
    <article class="quiz-card panel">
      <div class="quiz-progress" role="progressbar" aria-valuenow="${n}" aria-valuemin="0" aria-valuemax="${questions.length}" aria-label="Question ${n} of ${questions.length}">
        <span class="quiz-progress-fill" style="width:${quizPct}%"></span>
      </div>
      <p class="kicker">${escapeHtml(session.kind === "recap" ? "Unit recap" : "After the reading")} · ${n} of ${questions.length}</p>
      <h1 class="page-title">${escapeHtml(text(session.quiz.title, "Quiz"))}</h1>
      ${text(session.quiz.intro) && session.index === 0 && !submitted ? `<p class="lede">${escapeHtml(session.quiz.intro)}</p>` : ""}
      <form data-quiz-form>
        <h2 class="quiz-prompt" id="quiz-question">${escapeHtml(text(q.prompt))}</h2>
        <p class="muted quiz-hint">${escapeHtml(hint)}</p>
        <div class="quiz-options" role="group" aria-labelledby="quiz-question">${optionHtml}</div>
        ${feedback}
      </form>
      <p class="kbd-hint"><a href="${backHref}">Back</a>. Answers are not shown until you check this question.</p>
    </article>
  `;
}

function renderQuizResults(session) {
  const rec = quizRecord(session.id);
  const score = rec.lastScore ?? session.lastScore ?? 0;
  const total = rec.lastTotal ?? session.lastTotal ?? quizQuestions(session.quiz).length;
  const ratio = total ? score / total : 0;
  let line = "Return to the pages. The quiz is a check, not a prize.";
  if (ratio === 1) line = "That will hold. Go on.";
  else if (ratio >= 0.6) line = "Some of this still needs another look at the pages.";
  const item = session.meta.item;
  const nextHref = item?.nextId ? neighborHref(item.nextId) : "#/";
  const backHref =
    session.kind === "recap"
      ? "#/syllabus"
      : `#/read/${encodeURIComponent(session.ownerId)}`;

  const resultClass =
    ratio === 1 ? " quiz-results--perfect" : ratio >= 0.6 ? " quiz-results--good" : " quiz-results--review";

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/quizzes">Quizzes</a>
      <span class="crumb-sep">/</span>
      <span>Score</span>
    </nav>
    <article class="quiz-card quiz-results done-card${resultClass}">
      <p class="here-label">${ratio === 1 ? "Perfect" : "Finished"}</p>
      <h1 class="page-title">${escapeHtml(text(session.quiz.title, "Quiz"))}</h1>
      <div class="quiz-score-ring" aria-label="${score} out of ${total} correct">
        <p class="quiz-score"><strong>${score}</strong><span class="quiz-score-denom"> / ${total}</span></p>
      </div>
      <p class="lede">${escapeHtml(line)}</p>
      ${rec.bestScore != null && rec.bestScore !== score ? `<p class="muted">Best so far: ${rec.bestScore}/${rec.bestTotal}</p>` : ""}
      <p class="actions">
        <a class="btn btn-secondary" href="${backHref}">${session.kind === "recap" ? "Back to syllabus" : "Back to assignment"}</a>
        ${session.kind === "quiz" && item?.nextId ? `<a class="btn" href="${nextHref}">Next reading</a>` : `<a class="btn" href="#/">Continue</a>`}
        <button type="button" class="btn btn-ghost" data-quiz-retake>Retake</button>
      </p>
    </article>
  `;
}

function onClick(event) {
  const markBtn = event.target.closest("[data-bookmark-para]");
  if (markBtn) {
    event.preventDefault();
    const para = markBtn.closest(".reader-para");
    const coords = coordsFromPara(para);
    const route = parseRoute();
    if (!coords || route.name !== "text") return;
    toggleBookmarkAt(coords.assignmentId, coords.sectionId, coords.paragraphIndex);
    return;
  }

  const hiBtn = event.target.closest("[data-highlight-para]");
  if (hiBtn) {
    event.preventDefault();
    const para = hiBtn.closest(".reader-para");
    const coords = coordsFromPara(para);
    if (!coords) return;
    toggleHighlight(coords.assignmentId, coords.sectionId, coords.paragraphIndex);
    syncAnnotUi(coords.assignmentId);
    return;
  }

  const noteBtn = event.target.closest("[data-open-note]");
  if (noteBtn) {
    event.preventDefault();
    const para = noteBtn.closest(".reader-para");
    const wrap = para && para.querySelector(".para-note-wrap");
    if (!wrap) return;
    const opening = wrap.hidden;
    if (opening) closeParaNotes(wrap);
    wrap.hidden = !opening;
    noteBtn.setAttribute("aria-expanded", opening ? "true" : "false");
    if (opening) {
      const area = wrap.querySelector("[data-para-note]");
      if (area) area.focus();
    } else {
      commitParaNote(wrap.querySelector("[data-para-note]"));
    }
    return;
  }

  const jumpBtn = event.target.closest("[data-jump-para]");
  if (jumpBtn) {
    event.preventDefault();
    jumpToPara(jumpBtn.getAttribute("data-jump-para"));
    return;
  }

  const clearBtn = event.target.closest("[data-clear-bookmark]");
  if (clearBtn) {
    event.preventDefault();
    const route = parseRoute();
    if (route.name !== "text") return;
    clearBookmark(route.id);
    syncBookmarkUi(route.id);
    return;
  }

  const completeBtn = event.target.closest("[data-toggle-complete]");
  if (completeBtn) {
    snapshotScroll();
    const id = completeBtn.getAttribute("data-toggle-complete");
    if (isComplete(id)) {
      delete progress.completed[id];
    } else {
      progress.completed[id] = new Date().toISOString();
    }
    saveProgress();
    render();
    return;
  }

  if (event.target.closest("[data-print]")) {
    window.print();
    return;
  }

  if (event.target.closest("[data-quiz-next]")) {
    event.preventDefault();
    advanceQuiz();
    return;
  }
  if (event.target.closest("[data-quiz-skip]")) {
    event.preventDefault();
    skipQuizQuestion();
    return;
  }
  if (event.target.closest("[data-quiz-retake]")) {
    event.preventDefault();
    retakeQuiz();
    return;
  }

  const eraChip = event.target.closest("[data-era-filter]");
  if (eraChip) {
    glossaryUi.eraId = eraChip.getAttribute("data-era-filter") || "";
    render();
  }
}

function advanceQuiz() {
  if (!quizSession) return;
  const questions = quizQuestions(quizSession.quiz);
  quizSession.index += 1;
  if (quizSession.index >= questions.length) finishQuizAttempt();
  persistQuizSession();
  render();
}

function skipQuizQuestion() {
  if (!quizSession) return;
  const questions = quizQuestions(quizSession.quiz);
  const q = questions[quizSession.index];
  if (!q) return;
  const qid = text(q.id, String(quizSession.index));
  quizSession.responses[qid] = { selected: [], correct: false };
  advanceQuiz();
}

function retakeQuiz() {
  if (!quizSession) return;
  quizSession.index = 0;
  quizSession.responses = {};
  quizSession.finished = false;
  persistQuizSession();
  render();
}

function onSubmit(event) {
  const form = event.target.closest("[data-quiz-form]");
  if (!form) return;
  event.preventDefault();
  if (!quizSession) return;
  const questions = quizQuestions(quizSession.quiz);
  const q = questions[quizSession.index];
  if (!q) return;
  const qid = text(q.id, String(quizSession.index));
  if (quizSession.responses[qid]) return;
  const selected = selectedFromForm(form);
  if (!selected.length && questionType(q) !== "multiple-select") {
    form.classList.add("needs-answer");
    const first = form.querySelector("input[name='answer']");
    if (first) first.focus();
    return;
  }
  form.classList.remove("needs-answer");
  quizSession.responses[qid] = {
    selected,
    correct: isSelectionCorrect(q, selected),
  };
  persistQuizSession();
  render();
}

function onInput(event) {
  const search = event.target.closest("[data-term-search]");
  if (search) {
    glossaryUi.query = search.value;
    const host = document.getElementById("term-index");
    const count = document.getElementById("term-count");
    const visible = visibleTerms();
    if (host) host.innerHTML = renderTermIndexRows(visible);
    if (count) count.textContent = `${visible.length} of ${glossaryTerms().length}`;
    return;
  }
  const area = event.target.closest("[data-notes-for]");
  if (area) {
    const id = area.getAttribute("data-notes-for");
    progress.notes[id] = area.value;
    clearTimeout(noteTimer);
    noteTimer = setTimeout(saveProgress, 200);
    return;
  }
  const paraNote = event.target.closest("[data-para-note]");
  if (!paraNote) return;
  const coords = coordsFromPara(paraNote.closest(".reader-para"));
  if (!coords) return;
  clearTimeout(paraNoteTimer);
  paraNoteTimer = setTimeout(() => {
    upsertParaNote(coords.assignmentId, coords.sectionId, coords.paragraphIndex, paraNote.value);
    syncAnnotUi(coords.assignmentId);
  }, 250);
}

function isTypingTarget(el) {
  if (!el) return false;
  const tag = el.tagName;
  return tag === "TEXTAREA" || tag === "INPUT" || el.isContentEditable;
}

function onKeydown(event) {
  if (isTypingTarget(event.target)) return;
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  const route = parseRoute();
  if (route.name === "text" && event.key.toLowerCase() === "b") {
    event.preventDefault();
    const para = nearestParagraphInView();
    const coords = coordsFromPara(para);
    if (!coords) return;
    toggleBookmarkAt(coords.assignmentId, coords.sectionId, coords.paragraphIndex);
    return;
  }
  if (route.name === "text" && event.key.toLowerCase() === "h") {
    event.preventDefault();
    const para = nearestParagraphInView();
    const coords = coordsFromPara(para);
    if (!coords) return;
    toggleHighlight(coords.assignmentId, coords.sectionId, coords.paragraphIndex);
    syncAnnotUi(coords.assignmentId);
    return;
  }
  if (route.name !== "read" && route.name !== "text") return;
  const item = readingById(route.id);
  if (!item) return;
  if (event.key === "j" || event.key === "ArrowRight") {
    if (item.nextId) location.hash = neighborHref(item.nextId);
  } else if (event.key === "k" || event.key === "ArrowLeft") {
    if (item.prevId) location.hash = neighborHref(item.prevId);
  }
}

async function start() {
  try {
    course = await loadCourse();
    readings = flattenCourse(course);
    try {
      glossary = await loadGlossary();
    } catch {
      glossary = { title: "Philosophical terms", intro: "", terms: [] };
    }
    try {
      thinkerIndex = await loadThinkers();
    } catch {
      thinkerIndex = [];
    }
    const info = course.course || {};
    brandCourseEl.textContent = text(info.title, "Directed reading");
    document.title = `${text(info.title, "pjilosophy")} — directed reading`;
    render();
  } catch (err) {
    appEl.innerHTML = `
      <h1 class="page-title">The reading list is not on the table yet.</h1>
      <p class="lede">Place a course file at <code>content/course.json</code> or <code>course.json</code> and refresh. ${escapeHtml(err && err.message ? err.message : "")}</p>
    `;
  }
}

appEl.addEventListener("click", onClick);
appEl.addEventListener("input", onInput);
appEl.addEventListener("submit", onSubmit);
appEl.addEventListener(
  "focusout",
  (event) => {
    const wrap = event.target.closest(".para-note-wrap");
    if (!wrap) return;
    if (wrap.contains(event.relatedTarget)) return;
    commitParaNote(wrap.querySelector("[data-para-note]"));
  }
);
document.addEventListener("click", (event) => {
  const exportBtn = event.target.closest("[data-export]");
  if (!exportBtn) return;
  event.preventDefault();
  runExport(exportBtn.getAttribute("data-export"));
  document.querySelectorAll("details.export-menu").forEach((el) => {
    el.open = false;
  });
});
appEl.addEventListener(
  "load",
  (event) => {
    const img = event.target;
    if (!(img instanceof HTMLImageElement) || !img.classList.contains("portrait-img")) return;
    const wrap = img.closest(".portrait");
    if (wrap) wrap.classList.remove("no-photo");
  },
  true
);
appEl.addEventListener(
  "error",
  (event) => {
    const img = event.target;
    if (!(img instanceof HTMLImageElement) || !img.classList.contains("portrait-img")) return;
    const wrap = img.closest(".portrait");
    if (wrap) wrap.classList.add("no-photo");
    img.remove();
  },
  true
);
window.addEventListener("hashchange", () => {
  render();
});
window.addEventListener("keydown", onKeydown);
window.addEventListener(
  "scroll",
  () => {
    const route = parseRoute();
    if (route.name !== "text") return;
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      snapshotScroll();
      saveProgress();
    }, 200);
  },
  { passive: true }
);

initTheme();
start();
