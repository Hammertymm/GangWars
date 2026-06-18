#!/usr/bin/env python3
"""Measure title-screen button hitboxes on 472x1024 canvas."""

from __future__ import annotations

from PIL import Image, ImageDraw

ROOT = __file__
im = Image.open("title-screen.png").convert("RGB")
px = im.load()
W, H = im.size

# Full outer button rects — measured from visible gold rounded borders.
# Row 1: y=831–905, Row 2: y=921–995 (approx); refined by edge scan below.


def is_border(r: int, g: int, b: int) -> bool:
    return r > 75 and g > 55 and b < 85 and (r + g) > 140


def scan_button(x0: int, x1: int, y0: int, y1: int) -> tuple[int, int, int, int] | None:
    bw = x1 - x0
    border_rows: list[tuple[int, list[int]]] = []
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if is_border(*px[x, y])]
        if len(xs) > bw * 0.35:
            border_rows.append((y, xs))
    if len(border_rows) < 2:
        return None
    top_y, top_xs = border_rows[0]
    bot_y, bot_xs = border_rows[-1]
    lx = min(top_xs[0], bot_xs[0])
    rx = max(top_xs[-1], bot_xs[-1]) + 1
    return lx, top_y, rx - lx, bot_y - top_y + 1


# Row 2 has clear top/bottom gold borders; row 1 shares survival-panel spacing — use visual rects.
MANUAL = {
    "new": (18, 816, 214, 85),
    "continue": (240, 816, 214, 85),
    "ledger": (18, 921, 214, 74),
    "scores": (240, 921, 214, 74),
}

quads = [
    ("new", 10, 236, 820, 910),
    ("cont", 236, 472, 820, 910),
    ("ledger", 10, 236, 910, 1000),
    ("scores", 236, 472, 910, 1000),
]

results: dict[str, tuple[int, int, int, int]] = {}
for label, x0, x1, y0, y1 in quads:
    scanned = scan_button(x0, x1, y0, y1)
    key = label.replace("cont", "continue")
    if scanned:
        results[key if key != "cont" else "continue"] = scanned
        print(f"{label} scanned: {scanned}")
    else:
        manual_key = "continue" if label == "cont" else label
        results[manual_key] = MANUAL[manual_key]
        print(f"{label} manual: {MANUAL[manual_key]}")

debug = im.copy()
draw = ImageDraw.Draw(debug)
for name, (x, y, bw, bh) in results.items():
    draw.rectangle((x, y, x + bw, y + bh), outline="lime", width=3)
    print(
        f"{name}: left={x/W*100:.3f}% top={y/H*100:.3f}% "
        f"width={bw/W*100:.3f}% height={bh/H*100:.3f}%"
    )
debug.save("docs/review/screenshots/title-hitbox-debug.png")
