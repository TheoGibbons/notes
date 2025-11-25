# Simple Drawing Pad

An in-browser drawing pad built with plain HTML5 canvas and vanilla JavaScript. No build tools or external dependencies are required.

## Demo

[Demo](https://theogibbons.github.io/notes/index.html)

## Features
- Pen, Text, Eraser, Select/Move, and Hand/Pan tools
- Adjustable pen size, text size, and color
- Zoom with the mouse wheel and pan with the Hand tool or middle mouse button
- Undo/Redo history
- Export as PNG image or JSON data
- Local saves stored in your browser via `localStorage`

## How to Run
1. Clone or copy this folder to your machine.
2. Open `index.html` directly in a browser.

No server or installation is required.

## Basic Usage
- **Draw:** Select **Pen**, click and drag on the canvas.
- **Change color/size:** Use the toolbar controls for color and pen size.
- **Add text:** Select **Text**, click on the canvas, and enter your text.
- **Edit/move:** Use **Select/Move** to pick and drag existing strokes or text.
- **Pan/zoom:** Use **Hand/Pan** or middle mouse to pan, and the mouse wheel to zoom.
- **Undo/Redo:** Use the toolbar buttons or `Ctrl+Z` / `Ctrl+Y`.
- **Clear:** Click **Clear** to wipe the canvas.

## Local Saves
- Click **Save** to store the current drawing in browser `localStorage` under a name you choose.
- Use the dropdown to load a previously saved drawing (in the same browser on the same device).
- Saved data is browser-specific and may be cleared if you clear site data or switch browsers/devices.
