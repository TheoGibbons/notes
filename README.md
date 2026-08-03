# Simple Drawing Pad

An in-browser drawing pad built with plain HTML5 canvas and vanilla JavaScript. No build tools or external dependencies are required.

## Demo

[Demo](https://theogibbons.github.io/notes/index.html)

## Features
- Pen, Text, Eraser, Select/Move, and Hand/Pan tools
- Adjustable stroke size (pen, rectangle, circle, arrow), text size, and color
- Zoom with the mouse wheel and pan with the Hand tool or middle mouse button
- Undo/Redo history
- Export as PNG image or JSON data
- Local saves stored in your browser via `localStorage`
- Installable as an app (PWA) and fully usable offline

## How to Run
1. Clone or copy this folder to your machine.
2. Open `index.html` directly in a browser.

No build step or installation is required.

To exercise the offline/install behaviour you need an HTTP origin, because
service workers do not run on `file://` URLs. Any static server works:

```
python -m http.server 8765
```

then open `http://localhost:8765/`.

## Install as an App
- On desktop Chrome/Edge, click **Install** in the toolbar (it appears once the
  browser offers the prompt), or use the install icon in the address bar.
- On iOS Safari, use **Share → Add to Home Screen**.
- Once installed, the app opens in its own window and works with no network.

After the first visit, a service worker (`sw.js`) caches the app shell — the
page, cursors, and icons — so it loads offline. Drawings live in the browser's
own storage, so they are available offline too.

### Releasing an update
`index.html` is fetched network-first, so an online reload always picks up a new
build. When a new service worker is waiting, an **Update** button appears in the
toolbar; clicking it activates the new version and reloads. Bump
`CACHE_VERSION` in `sw.js` whenever a precached asset changes, so stale copies
of the cursors or icons are dropped.

### Icons
`icon-*.png` are generated from `favicon.png` by `tools/make-icons.py` (pure
standard library, no dependencies). Regenerate them after changing the favicon:

```
python tools/make-icons.py
```

## Basic Usage
- **Draw:** Select **Pen**, click and drag on the canvas.
- **Change color/size:** Use the toolbar controls for color and size.
- **Add text:** Select **Text**, click on the canvas, and enter your text.
- **Edit/move:** Use **Select/Move** to pick and drag existing strokes or text.
- **Pan/zoom:** Use **Hand/Pan** or middle mouse to pan, and the mouse wheel to zoom.
- **Fit to view:** Press `Space` to zoom and pan so everything you have drawn fits
  on screen (ignored while the Text tool is active or you are editing text).
- **Undo/Redo:** Use the toolbar buttons or `Ctrl+Z` / `Ctrl+Y`.
- **Clear:** Click **Clear** to wipe the canvas.

## Local Saves
- Click **Save** to store the current drawing in browser `localStorage` under a name you choose.
- Use the dropdown to load a previously saved drawing (in the same browser on the same device).
- Saved data is browser-specific and may be cleared if you clear site data or switch browsers/devices.
