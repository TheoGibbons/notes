"""Generate PWA icons from favicon.png. Pure stdlib (zlib), no dependencies.

favicon.png is normalised in place first: any white matte left in its rounded
corners by the original export is converted back to transparency.

Run from the repo root:  python tools/make-icons.py
"""
import struct
import zlib

SRC = "favicon.png"


def read_png(path):
    data = open(path, "rb").read()
    w, h, bitdepth, colortype, _, _, interlace = struct.unpack(">IIBBBBB", data[16:29])
    if (bitdepth, colortype, interlace) != (8, 6, 0):
        raise SystemExit("expected 8-bit RGBA, non-interlaced source")

    idat = b""
    i = 8
    while i < len(data):
        ln = struct.unpack(">I", data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        if typ == b"IDAT":
            idat += data[i + 8:i + 8 + ln]
        i += 12 + ln

    raw = zlib.decompress(idat)
    stride = w * 4
    px = bytearray(w * h * 4)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        for x in range(stride):
            a = line[x - 4] if x >= 4 else 0
            b = prev[x]
            c = prev[x - 4] if x >= 4 else 0
            if f == 1:
                line[x] = (line[x] + a) & 0xFF
            elif f == 2:
                line[x] = (line[x] + b) & 0xFF
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 0xFF
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        px[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, px


def write_png(path, w, h, px):
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]

    def chunk(typ, payload):
        return (struct.pack(">I", len(payload)) + typ + payload
                + struct.pack(">I", zlib.crc32(typ + payload) & 0xFFFFFFFF))

    out = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(out)


def resize(sw, sh, src, dw, dh):
    """Box-filter resample (area average), good for both up- and down-scaling."""
    dst = bytearray(dw * dh * 4)
    for dy in range(dh):
        y0, y1 = dy * sh // dh, max(dy * sh // dh + 1, (dy + 1) * sh // dh)
        for dx in range(dw):
            x0, x1 = dx * sw // dw, max(dx * sw // dw + 1, (dx + 1) * sw // dw)
            # Average in premultiplied space so transparent pixels don't bleed
            # their (meaningless) colour into the edges of the artwork.
            r = g = b = a = n = 0
            for sy in range(y0, y1):
                base = (sy * sw) * 4
                for sx in range(x0, x1):
                    o = base + sx * 4
                    pa = src[o + 3]
                    r += src[o] * pa
                    g += src[o + 1] * pa
                    b += src[o + 2] * pa
                    a += pa
                    n += 1
            o = (dy * dw + dx) * 4
            if a:
                dst[o] = r // a
                dst[o + 1] = g // a
                dst[o + 2] = b // a
            dst[o + 3] = a // n
    return dst


def solid(w, h, rgb):
    px = bytearray(w * h * 4)
    for i in range(w * h):
        px[i * 4:i * 4 + 4] = bytes(rgb) + b"\xff"
    return px


def paste(dst, dw, src, sw, sh, ox, oy):
    """Alpha-composite src over dst; the source's rounded corners are transparent."""
    for y in range(sh):
        for x in range(sw):
            s = (y * sw + x) * 4
            a = src[s + 3]
            if a == 0:
                continue
            d = ((oy + y) * dw + ox + x) * 4
            if a == 255:
                dst[d:d + 4] = src[s:s + 4]
            else:
                for k in range(3):
                    dst[d + k] = (src[s + k] * a + dst[d + k] * (255 - a)) // 255


def clear_corner_matte(w, h, px):
    """Replace the white matte outside the rounded corners with transparency.

    The source artwork was rendered onto an opaque white page, so its corners
    carry white pixels rather than empty ones and the icon shows four white
    notches on any non-white background.  Every corner pixel is either the blue
    field, the white page, or an antialiased mix of the two, so the mix ratio
    recovers the coverage the renderer meant to write into the alpha channel.

    Only the wedge of matte reachable from the outer corner is touched, so
    white belonging to the artwork can never be dissolved.  Compositing the
    result back onto white reproduces the source, and a corner that is already
    clear is left alone, so this is a no-op on an icon that has been fixed.
    """
    box = int(min(w, h) * 0.22)
    for ox, oy in ((0, 0), (w - box, 0), (0, h - box), (w - box, h - box)):
        cx = ox if ox == 0 else ox + box - 1
        cy = oy if oy == 0 else oy + box - 1
        if px[(cy * w + cx) * 4 + 3] == 0:
            continue

        # Field colour, averaged over the corner's opaque pixels that are
        # nowhere near white and so cannot be matte or a blend of it.
        acc = [0, 0, 0]
        n = 0
        for y in range(oy, oy + box):
            for x in range(ox, ox + box):
                o = (y * w + x) * 4
                if px[o + 3] == 255 and px[o] < 20:
                    for k in range(3):
                        acc[k] += px[o + k]
                    n += 1
        if not n:
            continue
        field = [c // n for c in acc]
        d = [255 - c for c in field]
        dd = float(sum(v * v for v in d))

        def coverage(x, y):
            o = (y * w + x) * 4
            a = px[o + 3] / 255.0
            # How far the pixel, composited over the white page, sits along the
            # line from white to the field colour.
            t = sum((255 - (px[o + k] * a + 255 * (1 - a))) * d[k]
                    for k in range(3)) / dd
            return max(0.0, min(1.0, t))

        stack = [(cx, cy)]
        seen = set(stack)
        while stack:
            x, y = stack.pop()
            c = coverage(x, y)
            if c > 0.9:
                continue                    # solid field; the matte ends here
            # Sub-1% coverage is the page's own off-white, not artwork.
            alpha = int(c * 255 + 0.5) if c > 0.01 else 0
            o = (y * w + x) * 4
            px[o:o + 4] = bytes(field) + bytes([alpha])
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (ox <= nx < ox + box and oy <= ny < oy + box
                        and (nx, ny) not in seen):
                    seen.add((nx, ny))
                    stack.append((nx, ny))


sw, sh, src = read_png(SRC)
before = bytes(src)
clear_corner_matte(sw, sh, src)
if bytes(src) != before:
    write_png(SRC, sw, sh, src)
    print("rewrote %s with transparent corners" % SRC)

# Plain "any" icons: straight resample of the source artwork.
for size in (192, 512):
    write_png("icon-%d.png" % size, size, size, resize(sw, sh, src, size, size))

# Maskable icon: full-bleed field colour with the artwork inset, so the glyph
# survives the aggressive circular crop launchers apply.
bg = tuple(src[(3 * sw + sw // 2) * 4 + k] for k in range(3))

# The source is a rounded square with transparent corners.  Flood those
# corners with the field colour first, otherwise the inset artwork lands on
# the blue field with four notches cut out around it.
flat = bytearray(src)
corner = int(sw * 0.2)
for y in range(sh):
    for x in range(sw):
        if min(x, sw - 1 - x) >= corner or min(y, sh - 1 - y) >= corner:
            continue
        o = (y * sw + x) * 4
        r, g, b, a = flat[o:o + 4]
        if a < 255 or not (b > 150 and r < 120):
            flat[o:o + 4] = bytes(bg) + b"\xff"

for size in (192, 512):
    inner = int(size * 0.86) // 2 * 2
    canvas = solid(size, size, bg)
    paste(canvas, size, resize(sw, sh, flat, inner, inner), inner, inner,
          (size - inner) // 2, (size - inner) // 2)
    write_png("icon-maskable-%d.png" % size, size, size, canvas)

print("background colour: #%02x%02x%02x" % bg)
print("wrote icon-192.png icon-512.png icon-maskable-192.png icon-maskable-512.png")
