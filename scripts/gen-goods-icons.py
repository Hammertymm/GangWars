from PIL import Image, ImageDraw

SIZE = 40
BG = (0, 0, 0, 0)
DARK = (35, 22, 8, 255)
MID = (90, 58, 18, 255)
BRONZE = (139, 95, 28, 255)
GOLD = (201, 162, 74, 255)
LIGHT = (231, 200, 121, 255)
PALE = (245, 228, 180, 255)


def new():
    return Image.new("RGBA", (SIZE, SIZE), BG)


def save(img, name):
    img.save(f"assets/goods/{name}.png")


def jug(img):
    d = ImageDraw.Draw(img)
    d.ellipse([10, 22, 30, 38], fill=MID, outline=GOLD)
    d.ellipse([12, 24, 28, 36], fill=DARK)
    d.rectangle([15, 10, 25, 24], fill=BRONZE, outline=GOLD)
    d.polygon([(15, 10), (25, 10), (23, 6), (17, 6)], fill=GOLD, outline=LIGHT)
    d.arc([24, 14, 34, 28], 270, 90, fill=GOLD, width=2)
    for i in range(3):
        d.rectangle([16 + i * 3, 14, 18 + i * 3, 18], fill=LIGHT)


def cigars(img):
    d = ImageDraw.Draw(img)
    d.rectangle([5, 18, 35, 36], fill=DARK, outline=GOLD)
    d.rectangle([7, 20, 33, 34], fill=(30, 18, 6, 255))
    d.polygon([(5, 18), (35, 18), (33, 12), (7, 12)], fill=BRONZE, outline=GOLD)
    for i, x in enumerate([10, 16, 22, 28]):
        d.rectangle([x, 4 + i % 2, x + 5, 14], fill=MID, outline=GOLD)
        d.ellipse([x + 1, 2, x + 4, 6], fill=LIGHT)


def bathgin(img):
    d = ImageDraw.Draw(img)
    d.rectangle([13, 12, 27, 36], fill=MID, outline=GOLD)
    d.rectangle([14, 14, 26, 34], fill=(25, 35, 45, 255))
    d.line([(16, 16), (16, 32)], fill=(60, 80, 100, 180), width=2)
    d.rectangle([14, 20, 26, 28], fill=PALE, outline=GOLD)
    d.rectangle([16, 22, 24, 24], fill=DARK)
    d.rectangle([16, 25, 24, 26], fill=DARK)
    d.rectangle([14, 6, 26, 12], fill=GOLD)
    d.rectangle([16, 4, 24, 7], fill=LIGHT)


def art_icon(img):
    d = ImageDraw.Draw(img)
    d.rectangle([4, 5, 36, 35], fill=GOLD)
    d.rectangle([7, 8, 33, 32], fill=DARK)
    d.rectangle([9, 20, 31, 30], fill=(40, 70, 35, 255))
    d.polygon([(9, 20), (28, 12), (31, 20)], fill=(55, 95, 45, 255))
    d.ellipse([18, 22, 24, 28], fill=(200, 180, 60, 255))
    d.rectangle([9, 28, 31, 30], fill=(60, 45, 25, 255))


def scotch(img):
    d = ImageDraw.Draw(img)
    d.polygon([(12, 8), (28, 8), (29, 34), (11, 34)], fill=MID, outline=GOLD)
    d.polygon([(13, 10), (27, 10), (28, 32), (12, 32)], fill=(30, 18, 6, 255))
    d.rectangle([15, 4, 25, 9], fill=GOLD)
    d.ellipse([13, 4, 27, 8], fill=LIGHT)
    d.rectangle([14, 14, 26, 24], fill=PALE, outline=BRONZE)
    d.rectangle([17, 16, 23, 22], fill=DARK)


def counterfeits(img):
    d = ImageDraw.Draw(img)
    for i in range(4):
        ox, oy = i * 2, i * 3
        d.rectangle([6 + ox, 8 + oy, 30 + ox, 24 + oy], fill=PALE, outline=GOLD)
        d.ellipse([14 + ox, 12 + oy, 22 + ox, 20 + oy], fill=MID, outline=BRONZE)
        d.rectangle([16 + ox, 14 + oy, 20 + ox, 18 + oy], fill=DARK)


def cognac(img):
    d = ImageDraw.Draw(img)
    d.ellipse([9, 18, 31, 38], fill=MID, outline=GOLD)
    d.ellipse([11, 20, 29, 36], fill=(45, 25, 8, 255))
    d.rectangle([14, 6, 26, 20], fill=BRONZE, outline=GOLD)
    d.arc([12, 4, 28, 12], 0, 180, fill=LIGHT, width=2)
    d.rectangle([17, 2, 23, 6], fill=GOLD)
    d.arc([12, 20, 22, 34], 200, 320, fill=LIGHT, width=1)


def furcoats(img):
    d = ImageDraw.Draw(img)
    d.arc([10, 3, 30, 14], 180, 0, fill=GOLD, width=2)
    d.line([(20, 3), (20, 8)], fill=GOLD, width=2)
    d.polygon([(7, 12), (33, 12), (35, 36), (5, 36)], fill=BRONZE, outline=GOLD)
    d.polygon([(10, 14), (30, 14), (32, 34), (8, 34)], fill=MID)
    for y in range(16, 32, 3):
        d.line([(9, y), (31, y)], fill=DARK)
    d.line([(20, 14), (16, 28)], fill=DARK, width=2)
    d.line([(20, 14), (24, 28)], fill=DARK, width=2)


def champagne(img):
    d = ImageDraw.Draw(img)
    d.polygon([(13, 10), (27, 10), (28, 36), (12, 36)], fill=MID, outline=GOLD)
    d.polygon([(14, 12), (26, 12), (27, 34), (13, 34)], fill=(35, 20, 5, 255))
    d.rectangle([12, 4, 28, 11], fill=GOLD)
    d.polygon([(12, 4), (28, 4), (26, 1), (14, 1)], fill=LIGHT)
    d.line([(13, 12), (27, 12)], fill=LIGHT)
    d.line([(14, 20), (26, 20)], fill=(50, 30, 10, 255))


def diamonds(img):
    d = ImageDraw.Draw(img)
    d.polygon([(20, 2), (36, 18), (20, 38), (4, 18)], fill=GOLD)
    d.polygon([(20, 5), (33, 18), (20, 35), (7, 18)], fill=LIGHT)
    d.polygon([(20, 5), (33, 18), (20, 18)], fill=PALE)
    d.polygon([(20, 5), (7, 18), (20, 18)], fill=LIGHT)
    d.polygon([(20, 35), (33, 18), (20, 18)], fill=BRONZE)
    d.polygon([(20, 35), (7, 18), (20, 18)], fill=MID)
    d.line([(20, 5), (20, 35)], fill=GOLD)
    d.line([(7, 18), (33, 18)], fill=GOLD)


icons = {
    "moonshine": jug,
    "cigars": cigars,
    "bathgin": bathgin,
    "art": art_icon,
    "scotch": scotch,
    "counterfeits": counterfeits,
    "cognac": cognac,
    "furcoats": furcoats,
    "champagne": champagne,
    "diamonds": diamonds,
}

for name, fn in icons.items():
    im = new()
    fn(im)
    save(im, name)
    print("ok", name)
