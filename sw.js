/* Service worker for Simple Drawing Pad.
 *
 * Bump CACHE_VERSION whenever a precached asset changes; the old cache is
 * dropped on activate. index.html is served network-first so a plain reload
 * always picks up a new build when the user is online. */
const CACHE_VERSION = "v2";
const CACHE_NAME = "drawing-pad-" + CACHE_VERSION;

// Relative to the service worker's own URL, so this works whether the app is
// hosted at the domain root or in a subdirectory (e.g. GitHub Pages /notes/).
const PRECACHE = [
    "./",
    "./index.html",
    "./manifest.json",
    "./favicon.png",
    "./icon-192.png",
    "./icon-512.png",
    "./icon-maskable-192.png",
    "./icon-maskable-512.png",
    "./pen-cursor.svg",
    "./rectangle-cursor.svg",
    "./circle-cursor.svg",
    "./arrow-cursor.svg",
    "./line-cursor.svg",
    "./eraser-cursor.svg"
];

self.addEventListener("install", event => {
    event.waitUntil((async () => {
        const cache = await caches.open(CACHE_NAME);
        // Individually, so one missing file can't fail the whole install.
        await Promise.all(PRECACHE.map(url =>
            cache.add(new Request(url, { cache: "reload" })).catch(() => {})
        ));
    })());
});

self.addEventListener("activate", event => {
    event.waitUntil((async () => {
        const names = await caches.keys();
        await Promise.all(names
            .filter(name => name.startsWith("drawing-pad-") && name !== CACHE_NAME)
            .map(name => caches.delete(name)));
        await self.clients.claim();
    })());
});

// The page asks us to take over immediately when the user accepts an update.
self.addEventListener("message", event => {
    if (event.data && event.data.type === "SKIP_WAITING") self.skipWaiting();
});

async function networkFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    try {
        const response = await fetch(request);
        if (response && response.ok) cache.put(request, response.clone());
        return response;
    } catch (err) {
        const cached = await cache.match(request) || await cache.match("./index.html");
        if (cached) return cached;
        throw err;
    }
}

async function cacheFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) {
        // Refresh in the background; the next load gets the newer copy.
        fetch(request).then(response => {
            if (response && response.ok) cache.put(request, response.clone());
        }).catch(() => {});
        return cached;
    }
    const response = await fetch(request);
    if (response && response.ok) cache.put(request, response.clone());
    return response;
}

self.addEventListener("fetch", event => {
    const request = event.request;
    if (request.method !== "GET") return;

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) return;

    if (request.mode === "navigate") {
        event.respondWith(networkFirst(request));
        return;
    }
    event.respondWith(cacheFirst(request));
});
