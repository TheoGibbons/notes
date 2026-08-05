# Simple Drawing Pad

An in-browser drawing pad built with plain HTML5 canvas and vanilla JavaScript. No build tools or external dependencies are required.

## Demo

[Demo](https://theogibbons.github.io/notes/index.html)

## Features
- Pen, Text, Eraser, Select/Move, and Hand/Pan tools
- Select one item or many, then move, restyle, reorder, or delete them together
- Insert images and crop them non-destructively
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
- **Select several items:** `Ctrl+click` (or `Shift+click`) each one to add it to the
  selection, or click it again to drop it. `Ctrl+A` selects everything and switches
  to **Select/Move**. Dragging any selected item moves the whole group; clicking one
  without dragging narrows the selection back down to that item, and clicking empty
  canvas clears it.
- **Delete:** Press `Delete` to remove everything currently selected — `Ctrl+A` then
  `Delete` wipes the drawing. Colour, size, fill, and **Send to Back**/**Bring to
  Front** also apply to the whole selection, skipping items they cannot affect (a
  fill colour ignores text, for example). Resize and rotate handles, and **Crop**,
  need exactly one item selected.
- **Pan/zoom:** Use **Hand/Pan** or middle mouse to pan, and the mouse wheel to zoom.
- **Fit to view:** Press `Space` to zoom and pan so everything you have drawn fits
  on screen (ignored while the Text tool is active or you are editing text).
- **Undo/Redo:** Use the toolbar buttons or `Ctrl+Z` / `Ctrl+Y`.
- **Crop an image:** Select an image and click **Crop** (or double-click the
  image). Drag the corner and edge handles to set the crop window, or drag
  inside it to slide the window over the picture. **Apply** (or `Enter`, or a
  click outside) keeps the crop, **Cancel** (or `Esc`) discards it, and
  **Reset** brings the whole picture back. Cropping never discards pixels, so
  cropping again — even after moving, resizing, or rotating the image — starts
  from the full original.
- **Export PNG:** Click **PNG** under Export or press `Ctrl+S` (`Cmd+S` on macOS).
- **Clear:** Click **Clear** to wipe the canvas.

## Local Saves
- Click **Save** to store the current drawing in browser `localStorage` under a name you choose.
- Use the dropdown to load a previously saved drawing (in the same browser on the same device).
- Saved data is browser-specific and may be cleared if you clear site data or switch browsers/devices.
