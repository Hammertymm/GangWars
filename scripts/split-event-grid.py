#!/usr/bin/env python3
"""Split the 2×5 standard-event grid into individual popup art assets."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "event-grid-source.png"
FALLBACK_SOURCE = Path(
    r"C:\Users\jarro\.cursor\projects\c-Projects-gang-wars-GangWars\assets"
    r"\c__Users_jarro_AppData_Roaming_Cursor_User_workspaceStorage_b8abd18152c996897b88164cd8a20284"
    r"_images_image-9b10f273-468d-4512-8b7e-1718b8c9ef96.png"
)
OUT_DIR = ROOT / "events"
TARGET_SIZE = (388, 662)  # 2× legacy 194×331 — sharp in popup cover crop

# row-major: top row L→R, then bottom row L→R
EVENTS = [
    "the_feds.png",
    "ambushed_rolled.png",
    "dead_drop.png",
    "packing_iron.png",
    "upgrade_available.png",
    "shortage.png",
    "buying_frenzy.png",
    "flooded_market.png",
    "super_rare_event.png",
    "rare_event_intel.png",
]

V_GUTTERS = [208, 411, 609, 817]
H_GUTTER = 339
GUTTER_TRIM = 3
EDGE_TRIM = 2  # drop seam pixels only — keep title banners and gold frames


def source_path() -> Path:
    if SOURCE.exists():
        return SOURCE
    if FALLBACK_SOURCE.exists():
        return FALLBACK_SOURCE
    raise FileNotFoundError("event grid source image not found")


def column_bounds(width: int) -> list[tuple[int, int]]:
    edges = [0] + V_GUTTERS + [width]
    bounds: list[tuple[int, int]] = []
    for i in range(5):
        left = edges[i] + (GUTTER_TRIM if i > 0 else EDGE_TRIM)
        right = edges[i + 1] - (GUTTER_TRIM if i < 4 else EDGE_TRIM)
        bounds.append((left, right))
    return bounds


def row_bounds(height: int) -> list[tuple[int, int]]:
    return [
        (EDGE_TRIM, H_GUTTER - GUTTER_TRIM),
        (H_GUTTER + GUTTER_TRIM, height - EDGE_TRIM),
    ]


def enhance_panel(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=110, threshold=2))
    return img


def fit_popup_panel(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Scale to fill popup left panel — top-aligned, matches object-fit: cover."""
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.0))


def backup_existing() -> Path | None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = OUT_DIR / f"_backup-standard-{stamp}"
    existing = [OUT_DIR / name for name in EVENTS if (OUT_DIR / name).exists()]
    if not existing:
        return None
    backup.mkdir(parents=True)
    for path in existing:
        shutil.copy2(path, backup / path.name)
    return backup


def main() -> None:
    src = source_path()
    if not SOURCE.exists() and src == FALLBACK_SOURCE:
        shutil.copy2(src, SOURCE)

    im = Image.open(src).convert("RGB")
    cols = column_bounds(im.width)
    rows = row_bounds(im.height)

    backup = backup_existing()
    if backup:
        print(f"Backed up previous standard events to {backup.relative_to(ROOT)}")

    idx = 0
    for ry, (y0, y1) in enumerate(rows):
        for cx, (x0, x1) in enumerate(cols):
            panel = im.crop((x0, y0, x1, y1))
            panel = enhance_panel(panel)
            panel = fit_popup_panel(panel, TARGET_SIZE)
            out = OUT_DIR / EVENTS[idx]
            panel.save(out, optimize=True)
            print(f"  {EVENTS[idx]:24s}  {panel.size}  (grid r{ry}c{cx})")
            idx += 1

    print(f"\nSaved {idx} standard event images to {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
