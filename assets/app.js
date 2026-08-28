const STORAGE_KEY = "pjilosophy.progress.v1";
const STUDENT_NAME = "Samuel";

const COURSE_URLS = ["./content/course.json", "./course.json"];
const GLOSSARY_URLS = ["./content/glossary.json", "./glossary.json"];

const appEl = document.getElementById("app");
const brandCourseEl = document.getElementById("brand-course");
const progressRail = document.getElementById("progress-rail");
const progressFill = document.getElementById("progress-rail-fill");
const navContinue = document.getElementById("nav-continue");
const navSyllabus = document.getElementById("nav-syllabus");
const navQuizzes = document.getElementById("nav-quizzes");
const navTerms = document.getElementById("nav-terms");

let course = null;
let readings = [];
let progress = loadProgress();
let noteTimer = null;
let scrollTimer = null;
let renderGen = 0;
let quizSession = null;
let glossary = { title: "Philosophical terms", intro: "", terms: [] };
let glossaryUi = { query: "", eraId: "" };
const textCache = new Map();

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completed: {}, notes: {}, scroll: {}, quizzes: {} };
    const parsed = JSON.parse(raw);
    return {
      completed: parsed.completed && typeof parsed.completed === "object" ? parsed.completed : {},
      notes: parsed.notes && typeof parsed.notes === "object" ? parsed.notes : {},
      scroll: parsed.scroll && typeof parsed.scroll === "object" ? parsed.scroll : {},
      quizzes: parsed.quizzes && typeof parsed.quizzes === "object" ? parsed.quizzes : {},
    };
  } catch {
    return { completed: {}, notes: {}, scroll: {}, quizzes: {} };
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
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

function greeting() {
  const hour = new Date().getHours();
  if (hour < 12) return `Morning, ${STUDENT_NAME}.`;
  if (hour < 17) return `Afternoon, ${STUDENT_NAME}.`;
  return `Evening, ${STUDENT_NAME}.`;
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
  const hash = (location.hash || "#/").replace(/^#/, "") || "/";
  const path = hash.startsWith("/") ? hash : `/${hash}`;
  const parts = path.split("/").filter(Boolean);
  if (parts.length === 0) return { name: "home" };
  if (parts[0] === "syllabus") return { name: "syllabus" };
  if (parts[0] === "era" && parts[1]) return { name: "era", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "read" && parts[1]) return { name: "read", id: decodeURIComponent(parts[1]) };
  if (parts[0] === "text" && parts[1]) return { name: "text", id: decodeURIComponent(parts[1]) };
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
      const res = await fetch(url, { cache: "no-store" });
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
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  const data = await res.json();
  if (!data || !Array.isArray(data.eras)) {
    throw new Error(`${url} did not match the course schema`);
  }
  return data;
}

async function loadCourse() {
  const loaded = [];
  let lastError = null;
  for (const url of COURSE_URLS) {
    try {
      loaded.push({ url, data: await fetchCourse(url) });
    } catch (err) {
      lastError = err;
    }
  }
  if (!loaded.length) throw lastError || new Error("Course file could not be loaded");
  loaded.sort((a, b) => {
    const stubDelta = Number(looksLikeStub(a.data)) - Number(looksLikeStub(b.data));
    if (stubDelta) return stubDelta;
    const nDelta = assignmentCount(b.data) - assignmentCount(a.data);
    if (nDelta) return nDelta;
    const quizA = quizTally(a.data);
    const quizB = quizTally(b.data);
    const qDelta = quizB.quizzes + quizB.recaps - (quizA.quizzes + quizA.recaps);
    if (qDelta) return qDelta;
    return COURSE_URLS.indexOf(a.url) - COURSE_URLS.indexOf(b.url);
  });
  return loaded[0].data;
}

async function fetchGlossary(url) {
  const res = await fetch(url, { cache: "no-store" });
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
  return raw.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean);
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
    restoreReaderPosition(route.id);
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
  } else {
    appEl.innerHTML = renderHome();
  }
}

function renderHome() {
  const info = course.course || {};
  const next = nextUnread();
  const total = readings.length;
  const done = completedCount();
  const remaining = remainingMinutes();
  const erasDone = erasCompletedCount();
  const eraTotal = (course.eras || []).length;
  const hoursLeft = remaining ? minutesLabel(remaining) : "none listed";

  const stats = `
    <div class="stats" aria-label="Progress">
      <span><strong>${done}</strong> of ${total} readings</span>
      <span><strong>${erasDone}</strong> of ${eraTotal} eras complete</span>
      <span>~<strong>${escapeHtml(hoursLeft)}</strong> remaining</span>
    </div>
  `;

  if (!next) {
    return `
      <p class="kicker">${escapeHtml(text(info.title, "Western philosophy"))}</p>
      <h1 class="page-title">${escapeHtml(STUDENT_NAME)}, the sequence is finished.</h1>
      <p class="lede">That is not the same as finishing philosophy. Re-read the texts that still resist you. The syllabus remains open.</p>
      ${stats}
      <article class="done-card">
        <p class="here-label">Complete</p>
        <h2>You have marked every assignment.</h2>
        <p class="muted">If a later version of the reading list appears, refresh. New unread items will show up here.</p>
        <p class="actions">
          <a class="btn" href="#/syllabus">Review the syllabus</a>
          <a class="btn btn-secondary" href="#/quizzes">Quizzes</a>
        </p>
      </article>
    `;
  }

  const a = next.assignment;
  const bits = metaBits(a).map(escapeHtml).join(" · ");
  const why = text(a.why);

  return `
    <p class="kicker">${escapeHtml(text(info.subtitle, text(info.title)))}</p>
    <h1 class="page-title">${escapeHtml(greeting())} We pick up here.</h1>
    <p class="lede">${escapeHtml(text(info.method, "Read the assigned pages. Then go on."))}</p>
    ${stats}
    <article class="next-card">
      <p class="here-label">Next reading</p>
      <h2>${escapeHtml(text(a.title, text(a.work, "Untitled assignment")))}</h2>
      <p class="meta-line">${bits}</p>
      ${why ? `<p class="why-excerpt">${escapeHtml(why)}</p>` : ""}
      ${
        usableQuiz(a.quiz) && !isQuizComplete(quizIdFor(a.quiz, `${a.id}-quiz`))
          ? `<p class="muted">The check for this reading is still open. Take it after the pages, not before.</p>`
          : ""
      }
      <p class="actions">
        ${
          hasInAppText(a)
            ? `<a class="btn" href="#/text/${encodeURIComponent(a.id)}">Read in the app</a>
               <a class="btn-ghost btn" href="#/read/${encodeURIComponent(a.id)}">Assignment notes</a>`
            : `<a class="btn" href="#/read/${encodeURIComponent(a.id)}">Open the assignment</a>`
        }
        ${usableQuiz(a.quiz) ? `<a class="btn-ghost btn" href="${assignmentQuizHref(a)}">Take the quiz</a>` : ""}
        <a class="btn-ghost btn" href="#/era/${encodeURIComponent(next.era.id)}">Era introduction</a>
      </p>
    </article>
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
        <a class="btn" href="#/text/${encodeURIComponent(a.id)}">Read in the app</a>
        ${
          available && href
            ? `<a class="btn btn-secondary" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Another edition</a>`
            : ""
        }
      </p>`
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
      <h1>${escapeHtml(text(a.title, text(a.work, "Untitled")))}</h1>
      <p class="meta-line">${metaBits(a).map(escapeHtml).join(" · ")}</p>
    </header>
    <dl class="dl-meta">
      ${text(a.author) ? `<dt>Author</dt><dd>${escapeHtml(a.author)}</dd>` : ""}
      ${text(a.work) ? `<dt>Work</dt><dd>${escapeHtml(a.work)}</dd>` : ""}
      ${translator ? `<dt>Translator</dt><dd>${escapeHtml(translator)}</dd>` : ""}
      ${text(a.selection) ? `<dt>Selection</dt><dd>${escapeHtml(a.selection)}</dd>` : ""}
      ${text(a.pages) ? `<dt>Pages</dt><dd>${escapeHtml(a.pages)}</dd>` : ""}
      ${minutesLabel(a.estimatedMinutes) ? `<dt>Time</dt><dd>${escapeHtml(minutesLabel(a.estimatedMinutes))}</dd>` : ""}
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
  const selection = text(a.text && a.text.locator, text(a.pages, text(a.selection)));
  const license = text(doc.license, "public-domain");
  const attribution = text(doc.attribution);
  const src = doc.source || {};
  const srcUrl = safeUrl(src.url);

  const sectionHtml = sections
    .map((sec) => {
      const sid = text(sec && sec.id);
      const paras = listOf(sec && sec.paragraphs);
      const heading = text(sec && sec.heading);
      const loc = text(sec && sec.locator);
      return `
        <section class="reader-section" id="sec-${escapeHtml(sid)}" data-section-id="${escapeHtml(sid)}">
          <div class="section-locator">
            ${loc ? `<span class="loc">${escapeHtml(loc)}</span>` : ""}
            ${heading ? `<h2>${escapeHtml(heading)}</h2>` : ""}
          </div>
          ${paras.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
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
            <h1 class="work-title">${escapeHtml(text(doc.title, text(a.work, a.title)))}</h1>
            <p class="work-byline">${escapeHtml(text(doc.author, a.author))}${translator ? ` · tr. ${escapeHtml(translator)}` : ""}</p>
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
      </div>
      ${
        guideBits.length
          ? `<details class="reader-guide" open><summary>Keep these in view</summary>${guideBits.join("")}</details>`
          : ""
      }
    </div>
  `;
}

function restoreReaderPosition(assignmentId) {
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
      document.querySelector(`[data-section-id="${CSS.escape(start)}"]`)
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
              const bits = metaBits(a).slice(0, 3).map(escapeHtml).join(" · ");
              const time = minutesLabel(a.estimatedMinutes);
              return `
                <li>
                  <a class="${currentClass}" href="${assignmentHref(a)}" ${a.id === currentId ? 'aria-current="location"' : ""}>
                    <span class="mark ${done ? "done" : ""}" aria-hidden="true">${done ? "✓" : "○"}</span>
                    <span>
                      <span class="asg-title">${escapeHtml(text(a.title, text(a.work, "Untitled")))}</span>
                      <span class="kind-pill">${escapeHtml(kindLabel(a.kind))}</span>
                    </span>
                    <span class="asg-time">${escapeHtml(time)}</span>
                    <span class="asg-sub">${bits}</span>
                  </a>
                </li>`;
            })
            .join("");
          return `
            <div class="unit-block">
              <h3 class="unit-title">${escapeHtml(text(unit.title, "Unit"))}</h3>
              ${
                usableQuiz(unit.recapQuiz)
                  ? `<p class="era-intro-link"><a href="${recapHref(unit)}">Unit recap quiz</a> · ${escapeHtml(quizStatusLabel(quizIdFor(unit.recapQuiz, `${unit.id}-recap`)))}</p>`
                  : ""
              }
              <ul class="assignment-list">${items}</ul>
            </div>`;
        })
        .join("");

      const done = eraComplete(era);
      return `
        <section class="era-block">
          <div class="era-head">
            <h2><a href="#/era/${encodeURIComponent(era.id)}">${escapeHtml(text(era.title, "Era"))}</a></h2>
            <span class="era-years">${escapeHtml(text(era.years))}${done ? " · complete" : ""}</span>
          </div>
          <p class="era-intro-link"><a href="#/era/${encodeURIComponent(era.id)}">Professor’s introduction</a></p>
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
    <p class="print-only">${escapeHtml(text(info.title))} — ${escapeHtml(STUDENT_NAME)}</p>
    <div class="syllabus">${eraHtml}</div>
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

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/syllabus">Syllabus</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(text(era.title, "Era"))}</span>
    </nav>
    <p class="kicker">${escapeHtml(text(era.years, "Era"))}${done ? " · complete" : ""}</p>
    <h1 class="page-title">${escapeHtml(text(era.title, "Untitled era"))}</h1>
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
    return `<p class="muted">No terms match that filter.</p>`;
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

  const seeHtml = see.length
    ? `<p class="term-see">See also: ${see
        .map((sid) => {
          const found = termById(sid);
          const label = found ? text(found.term, sid) : sid;
          return found
            ? `<a href="#/terms/${encodeURIComponent(sid)}">${escapeHtml(label)}</a>`
            : escapeHtml(label);
        })
        .join("; ")}</p>`
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
      <h1 class="page-title">${escapeHtml(text(term.term, term.id))}</h1>
      ${aliases.length ? `<p class="term-aliases">${aliases.map((a) => escapeHtml(a)).join(" · ")}</p>` : ""}
      ${
        paras.length
          ? paras.map((p) => `<p class="term-def">${escapeHtml(p)}</p>`).join("")
          : text(term.short)
            ? `<p class="term-def">${escapeHtml(term.short)}</p>`
            : `<p class="muted">No definition was provided.</p>`
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

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/quizzes">Quizzes</a>
      <span class="crumb-sep">/</span>
      <span>${escapeHtml(crumbTitle)}</span>
    </nav>
    <article class="quiz-card">
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

  return `
    <nav class="crumb" aria-label="Breadcrumb">
      <a href="#/quizzes">Quizzes</a>
      <span class="crumb-sep">/</span>
      <span>Score</span>
    </nav>
    <article class="quiz-card done-card">
      <p class="here-label">Finished</p>
      <h1 class="page-title">${escapeHtml(text(session.quiz.title, "Quiz"))}</h1>
      <p class="quiz-score"><strong>${score}</strong> / ${total}</p>
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
  if (!area) return;
  const id = area.getAttribute("data-notes-for");
  progress.notes[id] = area.value;
  clearTimeout(noteTimer);
  noteTimer = setTimeout(saveProgress, 200);
}

function isTypingTarget(el) {
  if (!el) return false;
  const tag = el.tagName;
  return tag === "TEXTAREA" || tag === "INPUT" || el.isContentEditable;
}

function onKeydown(event) {
  if (isTypingTarget(event.target)) return;
  const route = parseRoute();
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

start();
