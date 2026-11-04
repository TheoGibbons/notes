# Simple Drawing Pad

An in-browser drawing pad built with plain HTML5 canvas and vanilla JavaScript. No build tools or external dependencies are required.

## Demo

[Demo](https://theogibbons.github.io/notes/index.html)

## Features
- Pen, Text, Eraser, Select/Move, and Hand/Pan tools
- Select one item or many, then move, resize, rotate, restyle, reorder, or delete
  them together
- Copy, cut and paste shapes; paste images or text from other apps
- Insert, paste, or drag and drop images, then crop them non-destructively
- Adjustable stroke size, line style (solid, dashed, dotted), opacity, text size,
  rounded rectangle corners, pen smoothing, and color — with colour swatches and
  your recent colours
- Optional rectangle, ellipse, and text fills; rotate text and geometric shapes
- `Shift` draws squares, circles and 15° lines, and snaps rotation to 15°
- An eraser that rubs out just part of a pen stroke, with an adjustable size
- Zoom with the mouse wheel, a trackpad pinch, the zoom buttons or keyboard;
  pan with a trackpad, the Hand tool or the middle mouse button
- Right-click menu, and a keyboard shortcut list (`?`)
- Undo/Redo history
- Save as a high-resolution PNG, JPEG, WebP, vector SVG or PDF — trimmed to your
  drawing, with your choice of resolution, padding and background — or
  export/import JSON, from the **Save/Import** menu
- Local saves stored in your browser, with full-canvas previews, rename and delete
- Works the same on Windows, Linux and macOS (`Ctrl` or `Cmd`)
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
Shortcuts below say `Ctrl`; on a Mac, `Cmd` works everywhere `Ctrl` does. Press
`?` (or click **Shortcuts**) for the full list.

- **Draw:** Select **Pen** or a shape tool, then click and drag on the canvas.
  The finished item remains selected for immediate editing while its drawing
  tool stays active, so you can continue drawing more items of the same kind.
  Hold `Shift` to draw a square or circle, or to snap a line or arrow to 15° steps.
- **Change color/size and style:** Use the floating settings panel on the right.
  It shows the options supported by the active drawing tool or current selection:
  colour (with swatches and your recent colours), fill, size, line style (solid,
  dashed or dotted), corner rounding for rectangles, smoothing for pen strokes, and
  opacity. Each setting applies to new items and to every selected item it suits.
- **Change order:** Use **Send to Back** or **Bring to Front** in the floating
  settings panel when one or more items are selected.
- **Add text:** Select **Text**, click on the canvas, and enter your text.
- **Edit/move:** Use **Select/Move** to pick and drag existing strokes or text.
- **Select several items:** `Ctrl+click` (or `Shift+click`) each one to add it to the
  selection, or click it again to drop it. `Ctrl+A` selects everything and switches
  to **Select/Move**. Dragging any selected item moves the whole group; clicking one
  without dragging narrows the selection back down to that item, and clicking empty
  canvas clears it.
- **Nudge:** Press the arrow keys to move the selection one pixel at a time, or
  hold `Shift` to move ten. Holding a key down counts as a single undo step.
- **Duplicate:** Press `Ctrl+D` to copy everything currently selected. The copies
  appear slightly offset, on top of the stack, and become the new selection, so
  you can drag them straight where you want them.
- **Copy, cut and paste:** `Ctrl+C` copies the selection, `Ctrl+X` cuts it, and
  `Ctrl+V` pastes it under the pointer as editable shapes. Copying also puts a
  tightly cropped, transparent PNG of the selection on the clipboard, so pasting
  into another app gives a picture. Pasting an image or text copied from another
  app adds it as an image or a text item.
- **Right-click:** Right-click an item (or empty canvas) for Cut, Copy, Paste,
  Duplicate, Delete, ordering, Select All and Zoom to Fit.
- **Delete:** Press `Delete` or `Backspace` to remove everything currently selected —
  `Ctrl+A` then `Delete` wipes the drawing. Colour, size, fill, style and **Send to
  Back**/**Bring to Front** also apply to the whole selection, skipping items they
  cannot affect (a fill colour ignores pen strokes, for example).
- **Resize and rotate:** Drag a corner handle to resize, or the blue handle above
  to rotate. With several items selected, the box around them all has the same
  handles: corners scale the whole group evenly and the top handle rotates it.
  Hold `Shift` while resizing one item to keep its proportions, or while rotating
  to turn in 15° steps. **Crop** needs exactly one image selected.
- **Escape:** Press `Esc` once to clear the current selection. Press it again
  when nothing is selected to switch to **Select/Move**. Mid-drag, `Esc` cancels it.
- **Pan/zoom:** On a trackpad, scroll with two fingers to pan and pinch to zoom.
  With a mouse, the wheel zooms and the middle button (or **Hand/Pan**) pans. The
  zoom buttons in the bottom-right corner show the current zoom: `−`/`+` step it,
  clicking the percentage resets it to 100%, and **Fit** shows everything. The
  keyboard works too: `Ctrl+=` / `Ctrl+−` to zoom and `Ctrl+0` for 100%.
- **Fit to view:** Press `Space` to zoom and pan so everything you have drawn fits
  on screen (ignored while the Text tool is active or you are editing text).
- **Undo/Redo:** Use the toolbar buttons, `Ctrl+Z`, and `Ctrl+Shift+Z` or `Ctrl+Y`.
- **Erase:** With the **Eraser**, drag over a pen stroke to rub out just that part
  of it; other items are removed whole. Switch **Erase** to **Whole item** to
  remove complete strokes instead, and use **Eraser size** to change its width (a
  circle on the canvas shows the eraser's footprint).
- **Crop an image:** Select an image and click **Crop** in the floating settings
  panel (or double-click the image). Drag a rectangle over the image to draw a new crop window, drag its
  corner or edge handles to resize it, or drag inside it to slide it over the
  picture. `Shift`-drag draws a replacement window from inside an existing one.
  **Apply** (or `Enter`, or a click outside) keeps the crop, **Cancel** (or `Esc`)
  discards it, and **Reset** brings the whole picture back. Cropping never
  discards pixels, so cropping again — even after moving, resizing, or rotating
  the image — starts from the full original.
- **Add an image:** Click **Image**, paste an image with `Ctrl+V`, or drop an image
  file onto the canvas. Pasted and dropped images are placed at the pointer.
- **Lines and arrows:** Drag either endpoint of a line or arrow to resize and
  rotate it (`Shift` snaps it to 15° steps). The arrowhead scales along with the
  **Size** control.
- **Arrowhead style:** With the Arrow tool active, or arrows selected, use
  **Arrowhead** in the floating settings panel to put the head at the **Start**
  (where you began dragging), the **End**, or **Both** ends.
- **Fill text or shapes:** Choose **Fill** while using the Text, Rectangle, or
  Circle tool, or select existing items and change their fill together.
- **Save an image:** Choose **Save Image…** from the **Save/Import** menu to pick
  the file name, format, resolution, padding and background colour, or press
  `Ctrl+S` to skip the dialog and save a 2× PNG straight away. Either way the
  image is cropped to what you have drawn — the empty canvas around it is never
  included. Formats:
  - **PNG**, **JPEG**, **WebP** — pictures at the chosen resolution.
  - **SVG** — vector shapes that stay sharp at any size (resolution doesn't apply).
  - **PDF** — one page the size of the drawing, holding it as a high-quality image
    at the chosen resolution. Made without a PDF library, so it costs nothing to
    load.
- **Open a drawing file:** Drop a `.json` file exported from **Export JSON** onto
  the canvas to open it, the same as **Import JSON**.
- **Clear:** Click **Clear** (or press `Ctrl+N`) to wipe the canvas. Undo brings it back.

## Save/Import Menu
Hover over (or click) **Save/Import** in the toolbar to open it. Clicking pins the
menu open; click again, press `Esc`, or click elsewhere to close it. It holds:

- **Save Image…** — open the save dialog to download the drawing as an image.
- **Export JSON** — download the drawing as data.
- **Import JSON** — load a drawing previously exported as JSON.
- **Local saves** — **Save now…** asks for a name and stores the current drawing
  in this browser; every existing save is listed below it, newest timestamp shown
  alongside each name. Hover over or focus a save to preview it on the full canvas;
  moving away restores the current drawing, and clicking loads the save. Automatic
  saves are listed in blue under **Autosaves**. Hover over a save to show its
  **✎** (rename — for an autosave, keep it as a named save) and **✕** (delete)
  buttons.

Unsaved changes are autosaved before you load or import another drawing, so
switching drawings never silently discards work.

## Local Saves
- Saves live in the browser's IndexedDB storage on the device you made them on.
- Save names cannot begin with "Autosave", which is reserved for automatic saves.
- Saved data is browser-specific and may be cleared if you clear site data or switch browsers/devices.

### Autosaves
Changes are autosaved every 30 seconds and when you leave the page. Each autosave
replaces the previous one, so a drawing session keeps a single, up-to-date entry.
A new autosave entry is started — leaving the previous one untouched — when:

- the page is opened or reloaded,
- you **Clear** the canvas (or press `Ctrl+N`),
- one step removes more than half of the items on the board, or
- you open another drawing (carrying on with an opened autosave keeps updating it).

Before a Clear or a large delete, whatever was on the board is written into the
previous autosave, so it can be recovered from **Autosaves**. The ten most recent
autosaves are kept.
