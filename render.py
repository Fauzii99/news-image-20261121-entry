#!/usr/bin/env python3
"""v5: THE GLOBAL DISPATCH — 6 big illustrated hero cards (3x2),
7 regions x 3 one-line stories, real Natural Earth map.
1024x1024. Deterministic. DO NOT SUBMIT before user ACC.
Peru quake standardised to M6.8 everywhere.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 244, 235)
CARD = (250, 247, 240)
INK = (17, 19, 23)
RED = (200, 50, 40)
NAVY = (29, 53, 87)
GOLD = (201, 162, 39)
GREY = (110, 110, 105)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, max_w, leading, color=INK, max_lines=None):
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


# ------------------------------------------------- hero illustrations (316x84 art)
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    for sx, sy in [(18, 10), (70, 20), (130, 8), (190, 16), (250, 10), (290, 22)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w - 40, y + 8, x + w - 20, y + 28], fill=(240, 230, 200))
    bx = x + 8
    for f in [0.5, 0.75, 0.58, 0.9, 0.65, 0.8, 0.55]:
        bw = (w - 16) / 7
        bh = h * f * 0.6
        d.rectangle([bx, y + h - bh, bx + bw - 4, y + h], fill=(52, 62, 92))
        for wy in range(int(y + h - bh + 5), int(y + h - 4), 11):
            for wx in range(int(bx + 3), int(bx + bw - 7), 9):
                if (wx * 7 + wy) % 19 < 7:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        bx += bw
    # searchlight beams
    d.polygon([(x + 60, y + h), (x + 40, y + 6), (x + 52, y + 6)], fill=(255, 240, 180))
    d.polygon([(x + 230, y + h), (x + 250, y + 10), (x + 262, y + 10)], fill=(255, 240, 180))
    # drone trails + air-defence flashes
    for sx, ex, yy in [(x + 20, x + 120, 14), (x + 150, x + 260, 20), (x + 90, x + 200, 8)]:
        for t in range(0, 13):
            tt = t / 12
            px = sx + (ex - sx) * tt
            py = y + yy + 8 * math.sin(tt * math.pi)
            if t % 2 == 0:
                d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
    for fx, fy in [(x + 70, y + 18), (x + 210, y + 24), (x + 280, y + 14)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([fx, fy, fx + 12 * math.cos(ang), fy + 12 * math.sin(ang)],
                   fill=(255, 200, 80), width=2)
        d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 170, 40))


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 26, 48))
    for sx, sy in [(16, 12), (80, 8), (150, 14), (220, 10), (280, 16)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w - 72, y + 6, x + w - 50, y + 28], fill=(240, 220, 180))
    # dunes
    d.polygon([(x, y + h), (x, y + h - 18), (x + w * 0.35, y + h - 30),
               (x + w * 0.7, y + h - 16), (x + w, y + h - 24), (x + w, y + h)],
              fill=(196, 150, 80))
    d.polygon([(x, y + h), (x, y + h - 8), (x + w * 0.5, y + h - 14),
               (x + w, y + h - 6), (x + w, y + h)], fill=(170, 125, 60))
    # skyline + minaret
    d.rectangle([x + 20, y + h - 42, x + 34, y + h - 18], fill=(20, 18, 36))
    d.rectangle([x + 42, y + h - 52, x + 52, y + h - 18], fill=(20, 18, 36))
    d.polygon([(x + 42, y + h - 60), (x + 47, y + h - 52), (x + 52, y + h - 60)],
              fill=(20, 18, 36))
    d.rectangle([x + 60, y + h - 36, x + 78, y + h - 18], fill=(20, 18, 36))
    for wx in range(int(x + 24), int(x + 76), 10):
        d.rectangle([wx, y + h - 30, wx + 3, y + h - 26], fill=(255, 214, 120))
    # interception flashes + smoke trails
    for fx, fy in [(x + 130, y + 20), (x + 210, y + 28), (x + 270, y + 18)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([fx, fy, fx + 14 * math.cos(ang), fy + 14 * math.sin(ang)],
                   fill=(255, 140, 40), width=2)
        d.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=(255, 200, 90))
        d.arc([fx - 40, fy - 8, fx + 12, fy + 44], start=300, end=60,
              fill=(220, 220, 220), width=1)


def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    d.polygon([(x, y + h), (x + 50, y + 22), (x + 105, y + h)], fill=(120, 118, 112))
    d.polygon([(x + 70, y + h), (x + 150, y + 10), (x + 235, y + h)], fill=(90, 88, 84))
    d.polygon([(x + 200, y + h), (x + 270, y + 26), (x + w, y + h)], fill=(140, 136, 128))
    d.polygon([(x + 140, y + 10), (x + 150, y + 24), (x + 160, y + 10), (x + 150, y + 2)],
              fill=(255, 255, 255))
    # village houses
    for hx in [x + 18, x + 250]:
        d.rectangle([hx, y + h - 16, hx + 18, y + h - 4], fill=(150, 90, 60))
        d.polygon([(hx - 2, y + h - 16), (hx + 9, y + h - 24), (hx + 20, y + h - 16)],
                  fill=(120, 60, 40))
    # seismic crack + red wave
    cy = y + h * 0.58
    pts = [(x + 6, cy + 8), (x + 40, cy + 8), (x + 52, cy - 14), (x + 66, cy + 14),
           (x + 84, cy - 18), (x + 102, cy + 10), (x + 128, cy - 10), (x + 160, cy + 8),
           (x + 210, cy + 8), (x + 226, cy - 12), (x + 244, cy + 8), (x + w - 6, cy + 8)]
    d.line(pts, fill=RED, width=3)
    d.line([(x + 96, y + h - 6), (x + 112, y + h - 28), (x + 128, y + h - 12)],
           fill=RED, width=2)
    d.text((x + 10, y + 6), "M6.8", font=F(SANS_B, 13), fill=RED)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    d.ellipse([x + 14, y + 8, x + 52, y + 46], fill=(140, 190, 220))
    d.ellipse([x + 24, y + 16, x + 38, y + 28], fill=(120, 190, 120))
    # flags row
    for i, c in enumerate([(200, 50, 40), (29, 53, 87), (201, 162, 39),
                           (46, 125, 50), (14, 124, 123)]):
        fx = x + 70 + i * 16
        d.line([fx, y + 10, fx, y + 30], fill=INK, width=1)
        d.polygon([(fx, y + 10), (fx + 12, y + 14), (fx, y + 18)], fill=c)
    # conference dome building
    d.rectangle([x + 30, y + h - 30, x + w - 30, y + h - 6], fill=(255, 255, 255),
                outline=NAVY, width=1)
    d.pieslice([x + 78, y + 16, x + w - 78, y + h - 18], start=180, end=360,
               fill=(90, 140, 200), outline=NAVY, width=1)
    for i in range(5):
        bx = x + 44 + i * 44
        d.rectangle([bx, y + h - 30, bx + 10, y + h - 6], fill=NAVY)
    # clock past deadline
    d.ellipse([x + w - 56, y + 8, x + w - 16, y + 48], fill=(255, 255, 255),
              outline=RED, width=2)
    d.line([x + w - 36, y + 28, x + w - 36, y + 13], fill=INK, width=2)
    d.line([x + w - 36, y + 28, x + w - 24, y + 33], fill=INK, width=2)


def art_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 20))
    for sx, sy in [(14, 10), (50, 24), (90, 8), (160, 14), (220, 10), (260, 26), (120, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 10, y + 8, x + w - 10, y + h - 8], outline=GOLD, width=1)
    d.ellipse([x + 40, y + 18, x + w - 60, y + h - 18], outline=(150, 130, 80), width=1)
    mx, my = x + w - 52, y + h - 22
    d.ellipse([mx - 18, my - 18, mx + 18, my + 18], fill=(205, 140, 60))
    for cx, cy, r in [(mx - 7, my - 5, 4), (mx + 7, my + 4, 3), (mx + 3, my - 9, 3),
                      (mx - 10, my + 8, 2)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 105, 45))
    sx, sy = x + 78, y + 30
    d.rectangle([sx - 10, sy - 6, sx + 10, sy + 6], fill=(200, 210, 220),
                outline=(255, 255, 255), width=1)
    d.rectangle([sx - 34, sy - 4, sx - 10, sy + 4], fill=(60, 90, 160))
    d.rectangle([sx + 10, sy - 4, sx + 34, sy + 4], fill=(60, 90, 160))
    d.line([sx, sy + 6, sx, sy + 14], fill=(255, 255, 255), width=1)
    d.text((x + 10, y + h - 18), "ESA\u2013JAXA", font=F(SANS_B, 10),
           fill=(255, 255, 255))


def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 18, 34))
    # city lights skyline at bottom
    bx = x + 6
    for f in [0.4, 0.6, 0.45, 0.7, 0.5, 0.65]:
        bw = (w - 12) / 6
        bh = h * f * 0.35
        d.rectangle([bx, y + h - bh, bx + bw - 3, y + h], fill=(40, 44, 70))
        for wy in range(int(y + h - bh + 4), int(y + h - 3), 9):
            for wx in range(int(bx + 3), int(bx + bw - 6), 8):
                if (wx * 5 + wy) % 17 < 6:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 200, 90))
        bx += bw
    # night circuit (rounded track)
    d.rounded_rectangle([x + 20, y + 10, x + w - 20, y + h - 26], radius=18,
                        outline=(255, 220, 60), width=3)
    d.rounded_rectangle([x + 34, y + 20, x + w - 34, y + h - 36], radius=12,
                        outline=(120, 130, 160), width=1)
    # race cars with headlights
    for cx, cy, col in [(x + 90, y + 14, (200, 50, 40)), (x + 210, y + h - 30, (40, 120, 220))]:
        d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=col)
        d.ellipse([cx + 12, cy - 2, cx + 20, cy + 2], fill=(255, 240, 150))
        d.ellipse([cx - 20, cy - 2, cx - 12, cy + 2], fill=(255, 80, 60))
    # chequered flag
    fx, fy = x + w - 46, y + 12
    d.line([fx, fy, fx, fy + 22], fill=(255, 255, 255), width=1)
    for r in range(2):
        for c in range(3):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (0, 0, 0)
            d.rectangle([fx + c * 6, fy + r * 6, fx + c * 6 + 6, fy + r * 6 + 6],
                        fill=col)
    d.text((x + 10, y + h - 18), "P1 \u00b7 RUSSELL", font=F(SANS_B, 10), fill=(255, 220, 60))


HEROES = [
    ("Strikes hit Kyiv; two land in Poland", "Kyiv Post", art_kyiv),
    ("Three Houthi missiles downed over Riyadh", "Reuters", art_riyadh),
    ("M6.8 earthquake shakes central Peru", "USGS", art_peru),
    ("COP31 runs into Saturday with no deal", "AFP", art_cop31),
    ("BepiColombo reaches Mercury orbit", "ESA\u2013JAXA", art_bepi),
    ("Las Vegas GP: Russell on top in practice", "Formula 1", art_f1),
]

REGIONS = [
    ("AMERICAS", NAVY, "globe", [
        "FBI and US farm agency hacked",
        "4.2 quake rocks Los Angeles",
        "CBO: battleships add billions",
    ]),
    ("EUROPE", RED, "star", [
        "NATO chief Rutte visits Warsaw",
        "UK\u2013EU reset pact since Brexit",
        "EU: COP31 draft \"fossil-fuel\"",
    ]),
    ("MIDDLE EAST", GOLD, "crescent", [
        "Three killed in Gaza aid strike",
        "Tanker hit near Strait of Hormuz",
        "Coalition strikes Hodeidah port",
    ]),
    ("EAST & SOUTHEAST ASIA", (14, 124, 123), "torii", [
        "Jet lands after engine-fire alert",
        "Trump\u2013Xi: 3-way summit tested",
        "China backs clean power at COP31",
    ]),
    ("SOUTH & CENTRAL ASIA", (106, 79, 163), "lotus", [
        "ICJ: Myanmar guilty of Rohingya genocide",
        "Rahul 124* puts India on top in Wellington",
        "Banda Sea quake 6.8 near Timor",
    ]),
    ("AFRICA", (46, 125, 50), "africa", [
        "S. Africa: ex-deputy president dies at 71",
        "South Africa: hail warnings in 7 provinces",
        "Port Louis: African rating agency talks",
    ]),
    ("OCEANIA & SCIENCE / SPACE", (70, 90, 110), "orbit", [
        "Cancer pill: tumours gone in 1 in 12",
        "UN: \u2018killer robot\u2019 rules by 2028",
        "S&P falls 3.7% in AI sell-off",
    ]),
]

NUMBERS = [
    ("400+", "DRONES AT UKRAINE"),
    ("110", "MISSILES FIRED"),
    ("2", "LAND IN POLAND"),
    ("3", "MISSILES DOWNED"),
    ("6.8", "PERU QUAKE"),
]

# pins: (lon, lat, number); map box (28,148,700,220), PlateCarree lon -180..180, lat -55..75
PINS = [
    (-115.14, 36.17, "1"),   # Las Vegas
    (-77.04, -12.05, "2"),   # Lima
    (30.52, 50.45, "3"),     # Kyiv
    (21.01, 52.23, "4"),     # Warsaw
    (2.10, 51.20, "5"),      # London / Brussels
    (30.70, 36.90, "6"),     # Antalya
    (46.70, 24.70, "7"),     # Riyadh
    (125.60, 7.07, "8"),     # Davao
]
PIN_LEGEND = ("1 LAS VEGAS \u2014 F1 GP   \u2022   2 LIMA \u2014 M6.8 QUAKE   \u2022   3 KYIV \u2014 STRIKES   \u2022   "
              "4 WARSAW \u2014 RUTTE VISIT   \u2022   5 LONDON / BRUSSELS \u2014 UK-EU RESET",
              "6 ANTALYA \u2014 COP31 OVERTIME   \u2022   7 RIYADH \u2014 MISSILES DOWNED   \u2022   "
              "8 DAVAO \u2014 JET LANDS SAFE   \u2022   ORBIT \u2014 BEPICOLOMBO AT MERCURY")


def region_icon(d, kind, x, y, s, color):
    """16px mini vector icon for a region header."""
    cx, cy = x + s / 2, y + s / 2
    if kind == "globe":
        d.ellipse([x, y, x + s, y + s], outline=color, width=2)
        d.ellipse([x + 3, y + 3, x + 8, y + 7], fill=color)
        d.ellipse([x + 8, y + 9, x + 13, y + 13], fill=color)
    elif kind == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            r = s / 2 if i % 2 == 0 else s / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=color)
    elif kind == "crescent":
        d.ellipse([x, y, x + s, y + s], fill=color)
        d.ellipse([x + 5, y - 1, x + s + 2, y + s - 1], fill=CARD)
    elif kind == "torii":
        d.rectangle([x + 1, y + 2, x + s - 1, y + 5], fill=color)
        d.rectangle([x + 3, y + 7, x + s - 3, y + 9], fill=color)
        d.rectangle([x + 3, y + 2, x + 5, y + s], fill=color)
        d.rectangle([x + s - 5, y + 2, x + s - 3, y + s], fill=color)
    elif kind == "lotus":
        d.polygon([(cx, y), (cx + 3, y + 8), (cx - 3, y + 8)], fill=color)
        d.polygon([(x, y + 6), (cx - 2, y + 10), (x + 2, y + 12)], fill=color)
        d.polygon([(x + s, y + 6), (cx + 2, y + 10), (x + s - 2, y + 12)], fill=color)
        d.arc([x, y + 8, x + s, y + s + 2], start=0, end=180, fill=color, width=2)
    elif kind == "africa":
        d.polygon([(x + 4, y + 1), (x + 12, y + 1), (x + 14, y + 6), (x + 11, y + 12),
                   (x + 8, y + 15), (x + 6, y + 10), (x + 3, y + 6)], fill=color)
    else:  # orbit
        d.ellipse([x + 1, y + 4, x + s - 1, y + 12], outline=color, width=1)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # masthead
    d.text((512, 18), "THE GLOBAL DISPATCH", font=F(SERIF, 46), fill=INK, anchor="mt")
    d.text((512, 72), "S A T U R D A Y ,   2 1   N O V E M B E R   2 0 2 6",
           font=F(SANS_B, 15), fill=INK, anchor="mt")
    d.line([28, 100, W - 28, 100], fill=INK, width=2)
    d.line([28, 104, W - 28, 104], fill=INK, width=1)
    d.text((512, 112), "24-HOUR WORLD BRIEFING  \u2022  27 VERIFIED STORIES  \u2022  7 REGIONS",
           font=F(SANS_B, 11), fill=RED, anchor="mt")

    # map (real Natural Earth land) + right numbers panel
    my = 132
    d.text((28, my), "WHERE IT HAPPENED \u2014 21 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, my), "8 HOTSPOTS", font=F(SANS_B, 12), fill=RED, anchor="rt")
    map_img = Image.open("/tmp/world_map5.png").resize((700, 220), Image.LANCZOS)
    img.paste(map_img, (28, 148))
    d.rectangle([28, 148, 728, 368], outline=INK, width=1)
    for lon, lat, num in PINS:
        cx = 28 + (lon + 180) / 360 * 700
        cy = 148 + (75 - lat) / 130 * 220
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), num, font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
    # orbit icon, well inside the map (Pacific)
    ox, oy = 620, 162
    d.ellipse([ox - 26, oy - 11, ox + 26, oy + 11], outline=GOLD, width=2)
    d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=NAVY)
    d.rectangle([ox + 6, oy - 2, ox + 16, oy + 2], fill=NAVY)
    d.text((ox, oy + 17), "ORBIT \u2014 BEPICOLOMBO", font=F(SANS_B, 9),
           fill=NAVY, anchor="mt")
    # legend
    d.text((512, 374), PIN_LEGEND[0], font=F(SANS_B, 9.5), fill=INK, anchor="mt")
    d.text((512, 388), PIN_LEGEND[1], font=F(SANS_B, 9.5), fill=INK, anchor="mt")
    # right panel: BY THE NUMBERS
    px, py, pw = 740, 148, 256
    d.rectangle([px, py, px + pw, 368], outline=NAVY, width=1)
    d.text((px + 12, py + 10), "BY THE NUMBERS", font=F(SANS_B, 13), fill=NAVY)
    d.line([px + 12, py + 32, px + pw - 12, py + 32], fill=NAVY, width=1)
    for i, (num, lab) in enumerate(NUMBERS):
        yy = py + 38 + i * 34
        d.text((px + 12, yy), num, font=F(SANS_B, 21), fill=RED)
        d.text((px + 12, yy + 24), lab, font=F(SANS_B, 10), fill=INK)

    # hero strip: 6 illustrated top stories, 3 x 2
    hy = 412
    d.text((28, 396), "TOP STORIES \u2014 SIX HEADLINES, SIX DRAWINGS",
           font=F(SANS_B, 12), fill=INK)
    hw = (W - 56 - 2 * 10) // 3
    hh = 140
    for i, (head, src, art) in enumerate(HEROES):
        r, c = divmod(i, 3)
        x = 28 + c * (hw + 10)
        y = hy + r * (hh + 10)
        d.rectangle([x, y, x + hw, y + hh], outline=INK, width=1)
        art(d, x + 1, y + 1, hw - 2, 84)
        block(d, x + 8, y + 90, head, F(SERIF, 14), hw - 16, 16, max_lines=2)
        d.text((x + 8, y + hh - 16), f"({src})", font=F(SANS, 9), fill=GREY)

    # region grid: 3 one-line stories per region, thin-bordered cards
    gy = 712
    d.line([28, gy - 8, W - 28, gy - 8], fill=INK, width=2)
    d.text((28, gy), "SEVEN REGIONS \u2014 THREE STORIES EACH",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, gy), "ALL TIMES UTC", font=F(SANS_B, 12), fill=GREY, anchor="rt")

    def region_block(x, y, w, name, color, icon, items):
        bh = 30 + 3 * 26 + 8
        d.rectangle([x, y, x + w, y + bh], fill=CARD, outline=INK, width=1)
        region_icon(d, icon, x + 8, y + 8, 16, color)
        d.text((x + 30, y + 9), name, font=F(SANS_B, 12.5), fill=color)
        d.line([x + 8, y + 30, x + w - 8, y + 30], fill=INK, width=1)
        iy = y + 38
        for head in items:
            block(d, x + 10, iy, head, F(SANS_B, 10.5), w - 20, 13, max_lines=1)
            iy += 26

    row1_y = gy + 26
    rw = (W - 56 - 3 * 10) / 4
    for i in range(4):
        name, color, icon, items = REGIONS[i]
        region_block(28 + i * (rw + 10), row1_y, rw, name, color, icon, items)
    row2_y = row1_y + 124
    rw2 = (W - 56 - 2 * 10) / 3
    for i in range(4, 7):
        name, color, icon, items = REGIONS[i]
        region_block(28 + (i - 4) * (rw2 + 10), row2_y, rw2, name, color, icon, items)

    # footer colophon
    fy = 986
    d.line([28, fy, W - 28, fy], fill=INK, width=2)
    d.text((512, fy + 8),
           "SATURDAY 21 NOVEMBER 2026  \u2022  COMPILED FROM VERIFIED GLOBAL WIRE REPORTS  \u2022  ALL TIMES UTC",
           font=F(SANS_B, 11), fill=INK, anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size)


if __name__ == "__main__":
    render()
