// Simple service worker for the driver PWA.
// Network-first so drivers always get fresh data; falls back to cache offline.
const CACHE = "tcs-office-v1";

self.addEventListener("install", (e) => {
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  // only handle GET; let POST (forms/uploads) go straight to network
  if (req.method !== "GET") return;
  e.respondWith(
    fetch(req)
      .then((res) => {
        // cache a copy of successful same-origin responses
        if (res && res.status === 200 && req.url.startsWith(self.location.origin)) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      })
      .catch(() => caches.match(req))
  );
});
