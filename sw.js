// Bump when the caching strategy changes; content updates don't need a bump.
const VERSION = "v1";
const SHELL_CACHE = `pjilosophy-shell-${VERSION}`;
const TEXT_CACHE = `pjilosophy-texts-${VERSION}`;
const MEDIA_CACHE = `pjilosophy-media-${VERSION}`;
const KNOWN_CACHES = [SHELL_CACHE, TEXT_CACHE, MEDIA_CACHE];

const SHELL_FILES = [
  "./",
  "./index.html",
  "./assets/app.js",
  "./assets/styles.css",
  "./assets/favicon.svg",
  "./content/course.json",
  "./content/glossary.json",
  "./content/thinkers.json",
];

const FONT_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_FILES))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith("pjilosophy-") && !KNOWN_CACHES.includes(key))
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

function isCacheable(response) {
  return response && (response.ok || response.type === "opaque");
}

// Shell and syllabus data: always try the network so app.js and course.json stay in step.
async function networkFirst(request, cacheName, fallbackUrl) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (isCacheable(response)) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const cached =
      (await cache.match(request, { ignoreSearch: true })) ||
      (fallbackUrl ? await cache.match(fallbackUrl) : undefined);
    if (cached) return cached;
    throw err;
  }
}

// Texts, portraits, fonts: serve the saved copy at once and refresh it in the background.
async function staleWhileRevalidate(event, cacheName) {
  const { request } = event;
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const refresh = fetch(request)
    .then((response) => {
      if (isCacheable(response)) cache.put(request, response.clone());
      return response;
    })
    .catch(() => undefined);
  if (cached) {
    event.waitUntil(refresh);
    return cached;
  }
  const response = await refresh;
  return response || Response.error();
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  const url = new URL(request.url);

  if (FONT_HOSTS.includes(url.hostname)) {
    event.respondWith(staleWhileRevalidate(event, MEDIA_CACHE));
    return;
  }
  if (url.origin !== self.location.origin) return;

  const scopePath = new URL(self.registration.scope).pathname;
  const path = url.pathname.startsWith(scopePath) ? url.pathname.slice(scopePath.length) : url.pathname;

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request, SHELL_CACHE, "./index.html"));
  } else if (path.startsWith("content/texts/") || path.startsWith("texts/")) {
    event.respondWith(staleWhileRevalidate(event, TEXT_CACHE));
  } else if (path.startsWith("content/images/")) {
    event.respondWith(staleWhileRevalidate(event, MEDIA_CACHE));
  } else {
    event.respondWith(networkFirst(request, SHELL_CACHE));
  }
});
