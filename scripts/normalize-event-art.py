#!/usr/bin/env python3
"""Normalize rare, super-rare, godlike, and golden event art for full-bleed popups."""

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "events"

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from event_art import export_panel, needs_normalize  # noqa: E402

GLOBS = ("rare_*.png", "super_*.png", "godlike_*.png")


def main() -> None:
    paths: list[Path] = []
    for pattern in GLOBS:
        paths.extend(EVENTS.glob(pattern))
    paths = sorted(set(paths))

    todo = [p for p in paths if needs_normalize(p)]
    if not todo:
        print("All rare/super/godlike event art already normalized.")
        return

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = EVENTS / f"_backup-tier-{stamp}"
    backup.mkdir(parents=True)
    for path in todo:
        shutil.copy2(path, backup / path.name)
    print(f"Backed up {len(todo)} files to {backup.relative_to(ROOT)}")

    for path in todo:
        im = export_panel(Image.open(path).convert("RGB"))
        im.save(path, optimize=True, compress_level=9)
        print(f"  {path.name:28s}  {im.size}")

    print(f"\nNormalized {len(todo)} tier event images.")


if __name__ == "__main__":
    main()
