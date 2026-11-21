#!/usr/bin/env python3
"""v4: THE GLOBAL DISPATCH — real Natural Earth world map (cartopy),
5 illustrated hero cards, 7-region grid with vignettes.
1024x1024. Deterministic, no network at render time (map pre-rendered
from Natural Earth 110m land via cartopy, /tmp/world_map.png).
DO NOT SUBMIT before user review + ACC.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 244, 235)
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


def glyph(d, shape, cx, cy, r, color):
    if shape == "circle":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif shape == "square":
        d.rectangle([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif shape == "triangle":
        d.polygon([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)], fill=color)
    else:
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=color)


# ------------------------------------------------- hero illustrations
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    for sx, sy in [(20, 10), (60, 22), (110, 8), (150, 18), (175, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    bx = x + 6
    for f in [0.45, 0.7, 0.55, 0.85, 0.6, 0.75]:
        bw = (w - 12) / 6
        bh = h * f * 0.62
        d.rectangle([bx, y + h - bh, bx + bw - 3, y + h], fill=(52, 62, 92))
        for wy in range(int(y + h - bh + 4), int(y + h - 3), 10):
            for wx in range(int(bx + 3), int(bx + bw - 5), 8):
                if (wx * 7 + wy) % 19 < 7:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 214, 120))
        bx += bw
    # drone trails (dashed arcs) + air-defence flashes
    for sx, ex in [(x + 14, x + 80), (x + 90, x + 160)]:
        for t in range(0, 11):
            tt = t / 10
            px = sx + (ex - sx) * tt
            py = y + 12 + 10 * math.sin(tt * math.pi)
            if t % 2 == 0:
                d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
    for fx, fy in [(x + 40, y + 16), (x + 130, y + 22)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([fx, fy, fx + 11 * math.cos(ang), fy + 11 * math.sin(ang)],
                   fill=(255, 200, 80), width=2)
        d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 170, 40))


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 26, 48))
    for sx, sy in [(16, 12), (70, 8), (120, 16), (165, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + 6, x + w - 16, y + 24], fill=(240, 220, 180))
    # desert dune
    d.polygon([(x, y + h), (x, y + h - 14), (x + w * 0.4, y + h - 22),
               (x + w, y + h - 10), (x + w, y + h)], fill=(196, 150, 80))
    # city silhouette
    d.rectangle([x + 14, y + h - 30, x + 26, y + h - 14], fill=(20, 18, 36))
    d.rectangle([x + 34, y + h - 38, x + 44, y + h - 14], fill=(20, 18, 36))
    d.rectangle([x + 52, y + h - 26, x + 66, y + h - 14], fill=(20, 18, 36))
    # interception flashes + smoke trails
    for fx, fy in [(x + 90, y + 18), (x + 140, y + 26)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([fx, fy, fx + 13 * math.cos(ang), fy + 13 * math.sin(ang)],
                   fill=(255, 140, 40), width=2)
        d.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=(255, 200, 90))
        d.arc([fx - 30, fy - 6, fx + 10, fy + 34], start=300, end=60,
              fill=(220, 220, 220), width=1)


def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    # Andes silhouette
    d.polygon([(x, y + h), (x + 30, y + 18), (x + 62, y + h)], fill=(120, 118, 112))
    d.polygon([(x + 40, y + h), (x + 90, y + 8), (x + 140, y + h)], fill=(90, 88, 84))
    d.polygon([(x + 120, y + h), (x + 165, y + 22), (x + w, y + h)], fill=(140, 136, 128))
    d.polygon([(x + 82, y + 8), (x + 90, y + 18), (x + 98, y + 8), (x + 90, y + 2)],
              fill=(255, 255, 255))
    # seismic crack + red wave
    cy = y + h * 0.55
    pts = [(x + 4, cy + 6), (x + 24, cy + 6), (x + 32, cy - 10), (x + 42, cy + 10),
           (x + 54, cy - 12), (x + 66, cy + 8), (x + 82, cy - 6), (x + 100, cy + 6),
           (x + 130, cy + 6), (x + 142, cy - 8), (x + 154, cy + 6), (x + w - 4, cy + 6)]
    d.line(pts, fill=RED, width=3)
    d.line([(x + 60, y + h - 6), (x + 74, y + h - 22), (x + 88, y + h - 10)],
           fill=RED, width=2)
    d.text((x + 8, y + 4), "M6.8", font=F(SANS_B, 12), fill=RED)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    # conference dome building
    d.rectangle([x + 18, y + h - 22, x + w - 18, y + h - 4], fill=(255, 255, 255),
                outline=NAVY, width=1)
    d.pieslice([x + 42, y + 12, x + w - 42, y + h - 14], start=180, end=360,
               fill=(90, 140, 200), outline=NAVY, width=1)
    for i in range(4):
        bx = x + 30 + i * 34
        d.rectangle([bx, y + h - 22, bx + 8, y + h - 4], fill=NAVY)
    # clock past deadline
    d.ellipse([x + w - 46, y + 6, x + w - 14, y + 38], fill=(255, 255, 255),
              outline=RED, width=2)
    d.line([x + w - 30, y + 22, x + w - 30, y + 10], fill=INK, width=2)
    d.line([x + w - 30, y + 22, x + w - 20, y + 26], fill=INK, width=2)
    d.text((x + 10, y + 6), "DAY 13", font=F(SANS_B, 11), fill=RED)
    d.text((x + 10, y + 22), "NO DEAL", font=F(SANS_B, 9), fill=NAVY)


def art_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 20))
    for sx, sy in [(14, 10), (40, 22), (70, 8), (120, 14), (160, 8), (100, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # orbit ellipse
    d.ellipse([x + 8, y + 6, x + w - 8, y + h - 6], outline=GOLD, width=1)
    # Mercury
    mx, my = x + w - 42, y + h - 18
    d.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(205, 140, 60))
    for cx, cy, r in [(mx - 5, my - 4, 3), (mx + 5, my + 3, 2), (mx + 2, my - 7, 2)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 105, 45))
    # spacecraft
    sx, sy = x + 52, y + 22
    d.rectangle([sx - 8, sy - 5, sx + 8, sy + 5], fill=(200, 210, 220), outline=(255, 255, 255), width=1)
    d.rectangle([sx - 26, sy - 3, sx - 8, sy + 3], fill=(60, 90, 160))
    d.rectangle([sx + 8, sy - 3, sx + 26, sy + 3], fill=(60, 90, 160))
    d.text((x + 10, y + h - 16), "ESA\u2013JAXA", font=F(SANS_B, 9), fill=(255, 255, 255))


HEROES = [
    ("Strikes hit Kyiv; two land in Poland", "Kyiv Post", art_kyiv),
    ("Three Houthi missiles downed over Riyadh", "Reuters", art_riyadh),
    ("M6.8 earthquake shakes central Peru", "USGS", art_peru),
    ("COP31 runs into Saturday with no deal", "AFP", art_cop31),
    ("BepiColombo reaches Mercury orbit", "ESA\u2013JAXA", art_bepi),
]

REGIONS = [
    ("AMERICAS", NAVY, "circle", [
        ("Peru M6.7 quake shakes central Peru", "USGS", None),
        ("Las Vegas GP: Russell fastest in practice", "Formula 1", None),
        ("FBI and US farm agency hacked", "FBI", None),
        ("4.2 quake rocks Los Angeles", "USGS", None),
        ("CBO: Trump-class battleships add billions", "CBO", None),
    ]),
    ("EUROPE", RED, "square", [
        ("COP31 talks run into Saturday, no deal", "AFP", None),
        ("Russia strikes Kyiv: 400 drones, 110 missiles", "Kyiv Post", None),
        ("NATO chief Rutte visits Warsaw", "NATO", None),
        ("UK\u2013EU reset: biggest pact since Brexit", "UK govt", "ukeu"),
        ("EU: COP31 draft a \u2018fossil-fuel summit\u2019", "EU", None),
    ]),
    ("MIDDLE EAST", GOLD, "triangle", [
        ("Three Houthi missiles downed over Riyadh", "Reuters", None),
        ("Three killed in strike on Gaza aid vehicle", "AFP", None),
        ("Tanker hit near Strait of Hormuz", "UKMTO", None),
        ("Hodeidah port struck by coalition", "Coalition", None),
        ("Syria seizes arms bound for Lebanon", "SANA", None),
    ]),
    ("EAST & SOUTHEAST ASIA", (14, 124, 123), "diamond", [
        ("Jet lands safely after engine-fire alert", "AP", None),
        ("Trump\u2013Xi: 3-way summit tested", "Xinhua", None),
        ("China backs clean power at COP31", "China", None),
        ("N. Korea expands uranium work at Yongbyon", "IAEA", None),
        ("Shenzhen summit hailed by China", "Xinhua", None),
    ]),
    ("SOUTH & CENTRAL ASIA", (106, 79, 163), "circle", [
        ("ICJ: Myanmar guilty of Rohingya genocide", "ICJ", "court"),
        ("Rahul 124* puts India on top in Wellington", "AP", None),
        ("Banda Sea quake 6.8 near Timor", "USGS", None),
        ("Taipei: 2,700 China-linked accounts flagged", "Meta", None),
        ("Bangkok: arsenic plan for two rivers", "The Nation", None),
    ]),
    ("AFRICA", (46, 125, 50), "square", [
        ("S. Africa: ex-deputy president dies at 71", "Ramaphosa", None),
        ("South Africa: hail warnings in 7 provinces", "SAWS", None),
        ("Port Louis: African rating agency talks", "AU", None),
        ("Bayelsa: search on after funeral barge sank", "Nigeria", None),
        ("Nairobi: teachers join state payroll", "Kenya", None),
    ]),
    ("OCEANIA & SCIENCE / SPACE", (70, 90, 110), "triangle", [
        ("BepiColombo reaches Mercury orbit", "ESA\u2013JAXA", None),
        ("Cancer pill: tumours gone in 1 in 12", "Trial", None),
        ("UN: \u2018killer robot\u2019 rules by 2028", "UN", None),
        ("S&P falls 3.7% in AI sell-off", "Exchanges", "markets"),
        ("Canberra: Australia, China agree AI talks", "ABC", None),
    ]),
]

NUMBERS = [
    ("400+", "DRONES AT UKRAINE"),
    ("110", "MISSILES FIRED"),
    ("2", "LAND IN POLAND"),
    ("3", "MISSILES DOWNED"),
    ("6.8", "PERU QUAKE"),
]

# pins: (lon, lat, number) — lon/lat -> map pixels, map box (28,148,700,260),
# PlateCarree extent lon -180..180, lat -58..84
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
PIN_LEGEND = ("1 LAS VEGAS \u2014 F1 GP   \u2022   2 LIMA \u2014 M6.7 QUAKE   \u2022   3 KYIV \u2014 STRIKES   \u2022   "
              "4 WARSAW \u2014 RUTTE VISIT   \u2022   5 LONDON / BRUSSELS \u2014 UK-EU RESET",
              "6 ANTALYA \u2014 COP31 OVERTIME   \u2022   7 RIYADH \u2014 MISSILES DOWNED   \u2022   "
              "8 DAVAO \u2014 JET LANDS SAFE   \u2022   ORBIT \u2014 BEPICOLOMBO AT MERCURY")


def vignette(d, key, x, y, s):
    """small 20px editorial vignette for Markets / UK-EU / Rohingya."""
    if key == "markets":
        d.rectangle([x, y, x + s, y + s], fill=(255, 255, 255), outline=INK, width=1)
        pts = [(x + 2, y + 4), (x + 7, y + 7), (x + 11, y + 6), (x + 15, y + 13),
               (x + 18, y + 16)]
        d.line(pts, fill=RED, width=2)
        d.polygon([(x + 18, y + 16), (x + 14, y + 16), (x + 18, y + 12)], fill=RED)
    elif key == "ukeu":
        d.rectangle([x, y, x + s, y + s], fill=(40, 70, 140))
        for i in range(8):
            a = i * math.pi / 4
            sx, sy = x + 6 + 4 * math.cos(a), y + 10 + 4 * math.sin(a)
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 220, 60))
        d.rectangle([x + 11, y + 3, x + 18, y + s - 3], fill=(255, 255, 255))
        d.rectangle([x + 11, y + 3, x + 18, y + 6], fill=RED)
        d.rectangle([x + 11, y + s - 6, x + 18, y + s - 3], fill=RED)
    elif key == "court":
        d.rectangle([x, y, x + s, y + s], fill=(238, 230, 210), outline=INK, width=1)
        d.polygon([(x + 4, y + 5), (x + 10, y + 2), (x + 16, y + 5)], fill=(120, 100, 70))
        for i in range(3):
            bx = x + 5 + i * 5
            d.rectangle([bx, y + 6, bx + 2, y + 15], fill=(90, 80, 60))
        d.rectangle([x + 3, y + 16, x + 17, y + 18], fill=(120, 100, 70))


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
    d.text((512, 112), "24-HOUR WORLD BRIEFING  \u2022  35 VERIFIED STORIES  \u2022  7 REGIONS",
           font=F(SANS_B, 11), fill=RED, anchor="mt")

    # map (real Natural Earth land) + right numbers panel
    my = 132
    d.text((28, my), "WHERE IT HAPPENED \u2014 21 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, my), "8 HOTSPOTS", font=F(SANS_B, 12), fill=RED, anchor="rt")
    map_img = Image.open("/tmp/world_map.png").resize((700, 260), Image.LANCZOS)
    img.paste(map_img, (28, 148))
    d.rectangle([28, 148, 728, 408], outline=INK, width=1)
    # pins from lon/lat
    for lon, lat, num in PINS:
        cx = 28 + (lon + 180) / 360 * 700
        cy = 148 + (84 - lat) / 142 * 260
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), num, font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
    # orbit icon over the Pacific (empty ocean, top right of map)
    ox, oy = 650, 165
    d.ellipse([ox - 26, oy - 11, ox + 26, oy + 11], outline=GOLD, width=2)
    d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=NAVY)
    d.rectangle([ox + 6, oy - 2, ox + 16, oy + 2], fill=NAVY)
    d.text((ox, oy + 17), "ORBIT \u2014 BEPICOLOMBO", font=F(SANS_B, 9),
           fill=NAVY, anchor="mt")
    # legend
    d.text((512, 414), PIN_LEGEND[0], font=F(SANS_B, 9.5), fill=INK, anchor="mt")
    d.text((512, 428), PIN_LEGEND[1], font=F(SANS_B, 9.5), fill=INK, anchor="mt")
    # right panel: BY THE NUMBERS
    px, py, pw = 740, 148, 256
    d.rectangle([px, py, px + pw, 408], outline=NAVY, width=1)
    d.text((px + 12, py + 10), "BY THE NUMBERS", font=F(SANS_B, 13), fill=NAVY)
    d.line([px + 12, py + 32, px + pw - 12, py + 32], fill=NAVY, width=1)
    for i, (num, lab) in enumerate(NUMBERS):
        yy = py + 40 + i * 46
        d.text((px + 12, yy), num, font=F(SANS_B, 22), fill=RED)
        d.text((px + 12, yy + 25), lab, font=F(SANS_B, 10), fill=INK)

    # hero strip: 5 illustrated top stories
    hy = 462
    d.text((28, 446), "TOP STORIES \u2014 FIVE HEADLINES, FIVE DRAWINGS",
           font=F(SANS_B, 12), fill=INK)
    hw = (W - 56 - 4 * 8) / 5
    hh = 120
    for i, (head, src, art) in enumerate(HEROES):
        x = 28 + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], outline=INK, width=1)
        art(d, x + 1, hy + 1, hw - 2, 60)
        block(d, x + 7, hy + 67, head, F(SERIF, 13), hw - 14, 15, max_lines=2)
        d.text((x + 7, hy + hh - 16), f"({src})", font=F(SANS, 9), fill=GREY)

    # region grid
    gy = 590
    d.line([28, gy - 8, W - 28, gy - 8], fill=INK, width=2)
    d.text((28, gy), "SEVEN REGIONS \u2014 FIVE STORIES EACH",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, gy), "ALL TIMES UTC", font=F(SANS_B, 12), fill=GREY, anchor="rt")

    def region_block(x, y, w, name, color, shape, items):
        d.rectangle([x, y, x + w, y + 4], fill=color)
        d.text((x, y + 10), name, font=F(SANS_B, 13), fill=color)
        d.line([x, y + 30, x + w, y + 30], fill=INK, width=1)
        iy = y + 38
        for head, src, vig in items:
            if vig:
                vignette(d, vig, x + 1, iy + 1, 20)
            else:
                glyph(d, shape, x + 8, iy + 9, 5, color)
            block(d, x + 26, iy, f"{head} ({src})", F(SANS_B, 11), w - 26, 13,
                  max_lines=2)
            iy += 30

    row1_y = gy + 26
    rw = (W - 56 - 3 * 10) / 4
    for i in range(4):
        name, color, shape, items = REGIONS[i]
        region_block(28 + i * (rw + 10), row1_y, rw, name, color, shape, items)
    row2_y = row1_y + 186
    rw2 = (W - 56 - 2 * 10) / 3
    for i in range(4, 7):
        name, color, shape, items = REGIONS[i]
        region_block(28 + (i - 4) * (rw2 + 10), row2_y, rw2, name, color, shape, items)

    # footer colophon
    fy = 992
    d.line([28, fy, W - 28, fy], fill=INK, width=2)
    d.text((512, fy + 8),
           "SATURDAY 21 NOVEMBER 2026  \u2022  COMPILED FROM VERIFIED GLOBAL WIRE REPORTS  \u2022  ALL TIMES UTC",
           font=F(SANS_B, 11), fill=INK, anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size)


if __name__ == "__main__":
    render()
