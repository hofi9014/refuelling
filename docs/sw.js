// Bump VERSION on every release so phones pick up the new files.
const VERSION = "v14";
const CACHE = "refuelling-" + VERSION;
// Big libraries in vendor/ are cached on first use, in a cache kept across versions (rename it when a library changes).
const VENDOR_CACHE = "refuelling-vendor-1";
const ASSETS = ["./", "./index.html", "./notify.js", "./manifest.webmanifest",
  "./icons/icon-192.png", "./icons/icon-512.png", "./icons/maskable-512.png", "./icons/apple-touch-icon.png", "./icons/favicon-32.png",
  ...["de", "fr", "es", "it", "pt", "nl", "da", "sv", "nb", "fi", "is", "cs", "sk", "hu", "ro", "bg", "uk", "tr", "hi", "ja"].map(l => `./lang/${l}.js`),
  ...["barlow-latin-400", "barlow-latin-500", "barlow-latin-600", "barlow-latin-ext-400", "barlow-latin-ext-500", "barlow-latin-ext-600",
      "barlow-condensed-latin-500", "barlow-condensed-latin-600", "barlow-condensed-latin-700",
      "barlow-condensed-latin-ext-500", "barlow-condensed-latin-ext-600", "barlow-condensed-latin-ext-700"].map(f => `./fonts/${f}-normal.woff2`)];

importScripts("notify.js");

self.addEventListener("install", e => {
  // cache: "reload" so a new version never stores stale copies from the browser's HTTP cache
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS.map(u => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith("refuelling-") && k !== CACHE && k !== VENDOR_CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Pages: network first so updates show up when online, cache when offline. Other files: cache first.
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  if (req.mode === "navigate") {
    // no-cache: skip the browser's HTTP cache (GitHub Pages keeps pages for 10 min) so updates arrive on the next launch
    e.respondWith(fetch(req, { cache: "no-cache" }).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put("./index.html", copy));
      return res;
    }).catch(() => caches.match("./index.html")));
    return;
  }
  if (new URL(req.url).pathname.includes("/vendor/")) {
    e.respondWith(caches.open(VENDOR_CACHE).then(c => c.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok) c.put(req, res.clone());
      return res;
    }))));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});

/* ---------- reminders while the app is closed (Periodic Background Sync, installed app on Chrome/Android) ---------- */
function kv(mode, fn) {
  return new Promise((res, rej) => {
    const open = indexedDB.open("refuelling", 1);
    open.onupgradeneeded = () => open.result.createObjectStore("kv");
    open.onerror = () => rej(open.error);
    open.onsuccess = () => {
      const tx = open.result.transaction("kv", mode), st = tx.objectStore("kv"), out = fn(st);
      tx.oncomplete = () => res(out.result);
      tx.onerror = () => rej(tx.error);
    };
  });
}
const pad = n => String(n).padStart(2, "0");
const today = () => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };

async function checkReminders() {
  const S = await kv("readonly", st => st.get("state"));
  if (!S || !S.settings || !S.settings.notify) return;
  const notified = (await kv("readonly", st => st.get("notified"))) || {};
  for (const n of dueNotifications(S, notified, today())) {
    await self.registration.showNotification(n.title, { body: n.body, tag: n.tag, icon: "icons/icon-192.png", badge: "icons/favicon-32.png" });
    notified[n.key] = today();
  }
  await kv("readwrite", st => st.put(notified, "notified"));
}

self.addEventListener("periodicsync", e => {
  if (e.tag === "reminders") e.waitUntil(checkReminders());
});

self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
    const c = list[0];
    return c ? c.focus() : self.clients.openWindow("./");
  }));
});
