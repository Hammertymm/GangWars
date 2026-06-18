#!/usr/bin/env python3
"""Create original landscape draft previews for end-screen rank cards.

The output is intentionally separate from cards/. These are approval previews,
not integrated game assets.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "review" / "score-rank-landscape-drafts"
LW, LH = 341, 192
SCALE = 2

INK = (8, 6, 4)
BLACK = (13, 9, 5)
BROWN = (42, 25, 10)
BRONZE = (104, 63, 24)
GOLD = (204, 139, 55)
AMBER = (231, 200, 121)
DIM = (116, 78, 36)


RANKS = [
    ("nobody", "NOBODY", "Everyone starts somewhere...", "alley"),
    ("pickpocket", "PICKPOCKET", "Light fingers, heavy nerves.", "pickpocket"),
    ("hustler", "HUSTLER", "If you can talk it, you can walk it.", "hustler"),
    ("rum-runner", "RUM RUNNER", "Fast cars. Faster excuses.", "rumrunner"),
    ("bootlegger", "BOOTLEGGER", "Making spirits (and money).", "bootlegger"),
    ("racketeer", "RACKETEER", "Polite reminder: we collect.", "racketeer"),
    ("wise-guy", "WISE GUY", "Charm, wit, and a mean right hook.", "wiseguy"),
    ("crew-boss", "CREW BOSS", "You bark the orders. They fetch.", "crewboss"),
    ("underboss", "UNDERBOSS", "Running the show while the boss relaxes.", "underboss"),
    ("godfather", "GODFATHER", "Respect is earned. Fear is free.", "godfather"),
    ("big-daddy-j", "BIG DADDY J", "You didn't just build an empire. You became the legend.", "bdj"),
]


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\courbd.ttf" if bold else r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE_FONT = font(19, True)
TAG_FONT = font(10, True)


def rect(d: ImageDraw.ImageDraw, xy, fill, outline=None, width=1):
    d.rectangle(tuple(map(int, xy)), fill=fill, outline=outline, width=width)


def line(d: ImageDraw.ImageDraw, xy, fill, width=1):
    d.line(tuple(map(int, xy)), fill=fill, width=width)


def ellipse(d: ImageDraw.ImageDraw, xy, fill, outline=None, width=1):
    d.ellipse(tuple(map(int, xy)), fill=fill, outline=outline, width=width)


def poly(d: ImageDraw.ImageDraw, pts, fill, outline=None):
    d.polygon([(int(x), int(y)) for x, y in pts], fill=fill, outline=outline)


def wrap(draw: ImageDraw.ImageDraw, text: str, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=TAG_FONT)[2] <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


def base(seed: str) -> tuple[Image.Image, ImageDraw.ImageDraw, random.Random]:
    rng = random.Random(seed)
    im = Image.new("RGB", (LW, LH), BLACK)
    d = ImageDraw.Draw(im)

    for y in range(LH):
        v = int(6 + y * 0.06)
        line(d, (0, y, LW, y), (12 + v, 8 + v // 2, 4))

    horizon = 108 + rng.randint(-8, 5)
    for side in (0, 1):
        for i in range(6):
            bw = rng.randint(22, 55)
            bh = rng.randint(68, 130)
            x = -12 + i * rng.randint(22, 38) if side == 0 else LW - (i + 1) * rng.randint(24, 39) - bw // 2
            y = horizon - bh + rng.randint(-5, 12)
            rect(d, (x, y, x + bw, LH), (20, 13, 6), (37, 23, 10))
            for wy in range(y + 12, min(horizon + 16, LH - 18), 14):
                for wx in range(x + 7, x + bw - 5, 12):
                    if rng.random() < 0.32:
                        rect(d, (wx, wy, wx + 3, wy + 5), (143, 87, 29))

    cx = LW // 2 + rng.randint(-18, 16)
    poly(d, [(cx - 34, horizon), (cx + 34, horizon), (LW - 42, LH), (42, LH)], (28, 17, 7))
    for i in range(6):
        y = horizon + i * 12
        line(d, (cx - 22 - i * 15, y, 23, LH), DIM)
        line(d, (cx + 22 + i * 15, y, LW - 23, LH), DIM)

    for x in (42 + rng.randint(-5, 6), LW - 54 + rng.randint(-5, 6)):
        line(d, (x, 66, x, 146), BRONZE, 2)
        ellipse(d, (x - 6, 57, x + 6, 71), (155, 96, 36), GOLD)
        rect(d, (x - 4, 66, x + 4, 75), (181, 112, 40))

    for _ in range(90):
        x = rng.randrange(LW)
        y = rng.randrange(18, LH)
        line(d, (x, y, x - 1, y + rng.randint(4, 9)), (97, 62, 27))

    return im, d, rng


def draw_person(d, x, y, scale=1.0, pose="stand", heavy=False):
    s = scale
    suit = (28, 19, 10)
    shade = (8, 6, 4)
    face = (175, 118, 52)
    w = 12 * s if not heavy else 18 * s
    h = 30 * s if not heavy else 34 * s
    ellipse(d, (x - 5 * s, y - h - 11 * s, x + 5 * s, y - h + 1 * s), face, shade)
    rect(d, (x - 10 * s, y - h - 14 * s, x + 10 * s, y - h - 10 * s), shade)
    rect(d, (x - 6 * s, y - h - 20 * s, x + 6 * s, y - h - 11 * s), shade)
    poly(d, [(x - w, y - h), (x + w, y - h), (x + w * .7, y - 3 * s), (x - w * .7, y - 3 * s)], suit, BRONZE)
    line(d, (x, y - h, x, y - 4 * s), GOLD)
    if pose == "reach":
        line(d, (x - w, y - h + 8 * s, x - 28 * s, y - h + 15 * s), face, max(1, int(2 * s)))
        line(d, (x + w, y - h + 8 * s, x + 17 * s, y - h + 22 * s), face, max(1, int(2 * s)))
    elif pose == "sit":
        line(d, (x - w, y - 5 * s, x - 19 * s, y + 7 * s), suit, max(1, int(3 * s)))
        line(d, (x + w, y - 5 * s, x + 20 * s, y + 7 * s), suit, max(1, int(3 * s)))
    else:
        line(d, (x - w, y - h + 9 * s, x - 18 * s, y - h + 24 * s), face, max(1, int(2 * s)))
        line(d, (x + w, y - h + 9 * s, x + 18 * s, y - h + 23 * s), face, max(1, int(2 * s)))
    line(d, (x - 4 * s, y - 3 * s, x - 9 * s, y + 15 * s), shade, max(1, int(3 * s)))
    line(d, (x + 4 * s, y - 3 * s, x + 9 * s, y + 15 * s), shade, max(1, int(3 * s)))


def draw_car(d, x, y, scale=1.0):
    s = scale
    poly(d, [(x - 45*s, y), (x - 34*s, y - 17*s), (x + 18*s, y - 19*s), (x + 47*s, y - 2*s), (x + 42*s, y + 13*s), (x - 43*s, y + 13*s)], (20, 13, 7), GOLD)
    rect(d, (x - 20*s, y - 15*s, x + 12*s, y - 3*s), (58, 34, 13), BRONZE)
    ellipse(d, (x - 38*s, y + 6*s, x - 20*s, y + 24*s), INK, GOLD)
    ellipse(d, (x + 19*s, y + 6*s, x + 37*s, y + 24*s), INK, GOLD)
    ellipse(d, (x - 47*s, y - 1*s, x - 39*s, y + 7*s), AMBER)
    ellipse(d, (x + 38*s, y - 1*s, x + 46*s, y + 7*s), AMBER)


def draw_scene(d, scene: str):
    if scene == "alley":
        rect(d, (184, 76, 250, 160), (21, 13, 6), BRONZE)
        draw_person(d, 218, 156, 1.35)
        rect(d, (70, 132, 102, 164), (24, 14, 7), BRONZE)
    elif scene == "pickpocket":
        draw_person(d, 234, 157, 1.2, "reach")
        draw_person(d, 279, 153, 1.4)
        line(d, (219, 120, 204, 127), AMBER, 2)
    elif scene == "hustler":
        rect(d, (208, 134, 315, 164), (32, 19, 8), BRONZE)
        draw_person(d, 262, 143, 1.35, "sit")
        for x in (226, 243, 294):
            ellipse(d, (x, 132, x + 10, 137), (18, 11, 6), GOLD)
    elif scene == "rumrunner":
        draw_car(d, 250, 133, 1.25)
        rect(d, (207, 74, 231, 103), (52, 29, 10), GOLD)
        rect(d, (231, 71, 254, 101), (52, 29, 10), GOLD)
    elif scene == "bootlegger":
        rect(d, (224, 76, 244, 151), (38, 23, 9), GOLD)
        ellipse(d, (211, 64, 257, 87), (38, 23, 9), GOLD)
        line(d, (244, 88, 286, 88), GOLD, 3)
        draw_person(d, 285, 158, 1.1, "reach")
    elif scene == "racketeer":
        rect(d, (217, 73, 264, 160), (22, 14, 7), GOLD)
        ellipse(d, (250, 115, 255, 120), AMBER)
        draw_person(d, 290, 156, 1.25)
        line(d, (271, 121, 251, 121), AMBER, 2)
    elif scene == "wiseguy":
        rect(d, (214, 134, 315, 164), (32, 19, 8), BRONZE)
        draw_person(d, 269, 143, 1.3, "sit")
        ellipse(d, (228, 127, 243, 136), (20, 12, 7), GOLD)
        rect(d, (243, 121, 252, 136), (80, 49, 18), GOLD)
    elif scene == "crewboss":
        rect(d, (202, 126, 330, 166), (32, 19, 8), BRONZE)
        draw_person(d, 270, 133, 1.65, "sit", True)
        rect(d, (218, 115, 236, 127), (12, 8, 4), GOLD)
        ellipse(d, (221, 110, 233, 121), (12, 8, 4), GOLD)
    elif scene == "underboss":
        rect(d, (203, 116, 328, 166), (34, 20, 8), GOLD)
        draw_person(d, 270, 133, 1.45, "sit", True)
        line(d, (236, 151, 216, 172), BLACK, 4)
        ellipse(d, (305, 117, 323, 135), AMBER, GOLD)
    elif scene == "godfather":
        rect(d, (202, 122, 327, 166), (26, 16, 7), GOLD)
        draw_person(d, 270, 134, 1.55, "sit", True)
        ellipse(d, (220, 130, 246, 151), (20, 13, 7), GOLD)
        line(d, (215, 88, 325, 88), DIM)
    elif scene == "bdj":
        rect(d, (202, 79, 328, 167), (27, 17, 8), GOLD)
        rect(d, (213, 91, 317, 160), (17, 11, 6), BRONZE)
        draw_person(d, 265, 142, 1.75, "sit", True)
        line(d, (232, 101, 232, 147), AMBER, 2)


def decorate(im: Image.Image, title: str, tagline: str) -> Image.Image:
    d = ImageDraw.Draw(im)
    for y in range(0, LH, 3):
        line(d, (0, y, LW, y), (0, 0, 0))

    rect(d, (5, 5, LW - 6, LH - 6), None, GOLD, 1)
    rect(d, (9, 9, LW - 10, LH - 10), None, DIM, 1)

    title_w = min(LW - 28, 39 + len(title) * 14)
    rect(d, (13, 13, 13 + title_w, 43), INK, GOLD, 1)
    d.text((21, 16), title, font=TITLE_FONT, fill=AMBER)

    cap = (13, 119, 202, 171)
    rect(d, cap, (10, 7, 4), DIM, 1)
    lines = wrap(d, tagline, cap[2] - cap[0] - 16)
    y = cap[1] + 18 if len(lines) == 1 else cap[1] + max(5, (cap[3] - cap[1] - len(lines) * 13) // 2)
    for text in lines:
        tw = d.textbbox((0, 0), text, font=TAG_FONT)[2]
        d.text((cap[0] + (cap[2] - cap[0] - tw) // 2, y), text, font=TAG_FONT, fill=AMBER)
        y += 13

    return im


def finish(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = im.convert("P", palette=Image.Palette.ADAPTIVE, colors=36).convert("RGB")
    return im.resize((LW * SCALE, LH * SCALE), Image.Resampling.NEAREST)


def make_card(slug: str, title: str, tagline: str, scene: str) -> Image.Image:
    im, d, rng = base(slug)
    draw_scene(d, scene)
    for _ in range(650):
        x = rng.randrange(LW)
        y = rng.randrange(LH)
        if rng.random() < 0.55:
            im.putpixel((x, y), tuple(max(0, c + rng.randint(-16, 12)) for c in im.getpixel((x, y))))
    return finish(decorate(im, title, tagline))


def make_sheet(paths: list[Path]) -> None:
    w, h = LW * SCALE, LH * SCALE
    sheet = Image.new("RGB", (w * 2, h * 6), (21, 17, 11))
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        sheet.paste(im, ((i % 2) * w, (i // 2) * h))
    sheet.save(OUT / "_contact-sheet.png", optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for slug, title, tagline, scene in RANKS:
        im = make_card(slug, title, tagline, scene)
        path = OUT / f"{slug}.png"
        im.save(path, optimize=True)
        paths.append(path)
        print(f"{path.relative_to(ROOT)} {im.size}")
    make_sheet(paths)
    print(f"{(OUT / '_contact-sheet.png').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
