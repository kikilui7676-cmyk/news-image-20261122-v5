#!/usr/bin/env python3
"""Render the v5 'poster edition' entry image: one dramatic lead visual
(a cracked globe with a rising thermometer over an Antalya skyline),
a huge date, and the rest of the day compressed into ten short lines.

Output: entry.png (1024x1024) next to this script.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
BG = (250, 246, 238)        # warm off-white
INK = (19, 17, 15)          # ink black
SOFT = (96, 90, 84)         # muted ink for captions
ACCENT = (196, 48, 18)      # deep orange-red
SILHOUETTE = (38, 35, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, target, min_size, max_width):
    """Largest font size <= target (and >= min_size) that fits max_width."""
    size = target
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def centered(draw, text, f, y, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

MARGIN = 48
RIGHT = W - MARGIN

# ---------------------------------------------------------------- masthead
f_mast = font(BOLD, 26)
centered(d, "THE WORLD IN ONE IMAGE — SUNDAY EDITION", f_mast, 30, INK)
d.rectangle([MARGIN, 74, RIGHT, 78], fill=ACCENT)

# ---------------------------------------------------------------- date
f_date = fit_font(d, "SUNDAY 22 NOVEMBER 2026", BOLD, 68, 58, RIGHT - MARGIN)
centered(d, "SUNDAY 22 NOVEMBER 2026", f_date, 94, INK)

# ---------------------------------------------------------------- skyline
BASE = 512
for x0, top, x1 in [(56, 452, 110), (118, 428, 168), (176, 462, 214),
                    (560, 438, 612), (660, 448, 706)]:
    d.rectangle([x0, top, x1, BASE], fill=SILHOUETTE)
# domed hall
d.rectangle([452, 472, 542, BASE], fill=SILHOUETTE)
d.pieslice([452, 436, 542, 512], 180, 360, fill=SILHOUETTE)
# minaret
d.rectangle([628, 404, 646, BASE], fill=SILHOUETTE)
d.polygon([(624, 404), (650, 404), (637, 372)], fill=SILHOUETTE)
d.rectangle([635, 352, 639, 372], fill=SILHOUETTE)

# ---------------------------------------------------------------- globe
CX, CY, R = 392, 338, 152
d.ellipse([CX - R, CY - R, CX + R, CY + R], fill=BG, outline=INK, width=6)
GRID = (110, 104, 98)
for k in (0.38, 0.72):
    d.ellipse([CX - R * k, CY - R, CX + R * k, CY + R], outline=GRID, width=3)
d.line([CX, CY - R, CX, CY + R], fill=GRID, width=3)
for phi_deg in (-50, -25, 0, 25, 50):
    phi = math.radians(phi_deg)
    hc = R * math.cos(phi)
    yy = CY - R * math.sin(phi)
    d.ellipse([CX - hc, yy - hc * 0.16, CX + hc, yy + hc * 0.16],
              outline=GRID, width=3)
# cracks — the poster's wound, in accent
d.line([(322, 232), (368, 292), (344, 348), (392, 412), (376, 468)],
       fill=ACCENT, width=7, joint="curve")
d.line([(344, 348), (296, 382)], fill=ACCENT, width=4)
d.line([(368, 292), (318, 262)], fill=ACCENT, width=4)
d.line([(452, 224), (428, 282), (468, 338)], fill=ACCENT, width=6,
       joint="curve")
d.line([(428, 282), (478, 254)], fill=ACCENT, width=4)

# ---------------------------------------------------------------- thermometer
TX0, TX1 = 756, 794
d.rounded_rectangle([TX0, 196, TX1, 452], radius=19, outline=INK, width=5)
d.rounded_rectangle([767, 236, 783, 458], radius=8, fill=ACCENT)
d.ellipse([741, 430, 809, 498], fill=ACCENT, outline=INK, width=5)
for ty in (230, 280, 330, 380):
    d.line([TX1 + 8, ty, TX1 + 26, ty], fill=INK, width=4)
d.line([TX0 - 26, 214, TX0 - 8, 214], fill=INK, width=4)

# ---------------------------------------------------------------- lead text
f_lead = fit_font(d, "COP31 ENDS WITHOUT A DEAL", BOLD, 58, 46, RIGHT - MARGIN)
centered(d, "COP31 ENDS WITHOUT A DEAL", f_lead, 532, ACCENT)
f_cap = fit_font(
    d,
    "Nearly 200 nations split over fossil fuels and climate finance in Antalya, Turkey.",
    REG, 22, 19, RIGHT - MARGIN)
centered(
    d,
    "Nearly 200 nations split over fossil fuels and climate finance in Antalya, Turkey.",
    f_cap, 606, INK)

# ---------------------------------------------------------------- ten lines
d.rectangle([MARGIN, 652, RIGHT, 655], fill=INK)
f_head = font(BOLD, 30)
d.text((MARGIN, 672), "THE DAY IN TEN LINES", font=f_head, fill=INK)
d.rectangle([MARGIN, 712, 190, 718], fill=ACCENT)

LINES = [
    ("2", "MISSILES LAND IN POLAND", "NATO calls it a violation"),
    ("3", "SEA DRONES HIT WARSHIP", "Russian ship at Benghazi, Libya"),
    ("4", "IRAN ATTACK IN BAHRAIN", "Plant hit; tankers near Hormuz"),
    ("5", "ICJ: MYANMAR GENOCIDE", "Court rules on the Rohingya"),
    ("6", "FIVE KILLED IN UKRAINE", "Kyiv flats; hometown struck"),
    ("7", "FUNERAL BOAT CAPSIZES", "Nigeria: at least 24 dead"),
    ("8", "CARTEL LEADER CAPTURED", "Mexico: 11 dead in firefights"),
    ("9", "SEARCH FOR 34 MISSING", "Indonesia candy factory fire"),
    ("10", "BRITAIN & EU: CLOSER TIES", "Major post-Brexit agreement"),
    ("11", "SHURI CASTLE RESTORED", "Okinawa, 7 years after fire"),
]

COL_X = [MARGIN, 524]
TEXT_W = 404
ROW_Y0 = 730
PITCH = 51
f_num = font(BOLD, 20)
f_hl = font(BOLD, 22)
f_cp = font(REG, 19)

for i, (num, head, cap) in enumerate(LINES):
    col = 0 if i < 5 else 1
    row = i % 5
    x = COL_X[col]
    y = ROW_Y0 + row * PITCH
    d.ellipse([x, y + 4, x + 36, y + 40], fill=ACCENT)
    nw = d.textlength(num, font=f_num)
    d.text((x + 18 - nw / 2, y + 11), num, font=f_num, fill=(255, 255, 255))
    tx = x + 48
    fh = fit_font(d, head, BOLD, 22, 20, TEXT_W)
    d.text((tx, y), head, font=fh, fill=INK)
    fc = fit_font(d, cap, REG, 19, 17, TEXT_W)
    d.text((tx, y + 27), cap, font=fc, fill=SOFT)

# ---------------------------------------------------------------- footer
f_foot = font(BOLD, 14)
centered(d, "E L E V E N   S T O R I E S  —  O N E   D A Y  —  O N E   I M A G E",
         f_foot, 1000, SOFT)

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
