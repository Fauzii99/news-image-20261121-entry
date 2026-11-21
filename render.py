#!/usr/bin/env python3
"""v3: THE GLOBAL DISPATCH — Swiss-modernist broadsheet.
1024x1024, 35 verified 21 Nov 2026 stories in 7 regions, centrepiece
world map with pins + leader lines. Deterministic, no network.
Note: prompt said COP31 in Belem — COP31 is in Antalya, Turkiye
(COP30 was Belem). Generic filler items from the prompt were replaced
with verified 21 Nov stories.
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
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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


# simplified minimalist continents (968 x 200 map area)
CONTINENTS = [
    # North America
    [(55, 28), (150, 14), (260, 18), (315, 40), (330, 70), (290, 95), (250, 118),
     (190, 122), (140, 100), (80, 88), (45, 60)],
    # South America
    [(300, 128), (355, 122), (385, 150), (370, 195), (335, 208), (305, 175)],
    # Europe
    [(468, 28), (530, 20), (562, 38), (555, 62), (520, 78), (478, 66), (462, 45)],
    # Africa
    [(480, 92), (545, 84), (575, 108), (565, 155), (535, 198), (500, 168), (478, 128)],
    # Asia
    [(575, 26), (700, 14), (830, 18), (915, 40), (930, 75), (890, 105), (820, 118),
     (720, 122), (640, 108), (580, 80), (568, 50)],
    # Oceania
    [(815, 150), (880, 144), (915, 162), (885, 182), (830, 178)],
]

PINS = [
    # (x, y, number)
    (180, 68, "1"),   # Las Vegas
    (325, 168, "2"),  # Lima
    (545, 44, "3"),   # Kyiv
    (522, 38, "4"),   # Warsaw
    (480, 34, "5"),   # London/Brussels
    (562, 62, "6"),   # Antalya
    (602, 96, "7"),   # Riyadh
    (832, 106, "8"),  # Davao
]
PIN_LEGEND = ("1 LAS VEGAS \u2014 F1 GP   \u2022   2 LIMA \u2014 M6.7 QUAKE   \u2022   3 KYIV \u2014 STRIKES   \u2022   "
              "4 WARSAW \u2014 RUTTE VISIT   \u2022   5 LONDON / BRUSSELS \u2014 UK-EU RESET",
              "6 ANTALYA \u2014 COP31 OVERTIME   \u2022   7 RIYADH \u2014 MISSILES DOWNED   \u2022   "
              "8 DAVAO \u2014 JET LANDS SAFE   \u2022   ORBIT \u2014 BEPICOLOMBO AT MERCURY")

REGIONS = [
    ("AMERICAS", NAVY, "circle", [
        ("Peru M6.7 quake shakes central Peru", "USGS"),
        ("Las Vegas GP: Russell fastest in practice", "Formula 1"),
        ("FBI and US farm agency hacked", "FBI"),
        ("4.2 quake rocks Los Angeles", "USGS"),
        ("CBO: Trump-class battleships add billions", "CBO"),
    ]),
    ("EUROPE", RED, "square", [
        ("COP31 talks run into Saturday, no deal", "AFP"),
        ("Russia strikes Kyiv: 400 drones, 110 missiles", "Kyiv Post"),
        ("NATO chief Rutte visits Warsaw", "NATO"),
        ("UK\u2013EU reset: biggest pact since Brexit", "UK govt"),
        ("EU: COP31 draft a \u2018fossil-fuel summit\u2019", "EU"),
    ]),
    ("MIDDLE EAST", GOLD, "triangle", [
        ("Three Houthi missiles downed over Riyadh", "Reuters"),
        ("Three killed in strike on Gaza aid vehicle", "AFP"),
        ("Tanker hit near Strait of Hormuz", "UKMTO"),
        ("Hodeidah port struck by coalition", "Coalition"),
        ("Syria seizes arms bound for Lebanon", "SANA"),
    ]),
    ("EAST & SOUTHEAST ASIA", (14, 124, 123), "diamond", [
        ("Jet lands safely after engine-fire alert", "AP"),
        ("Trump\u2013Xi: 3-way summit tested", "Xinhua"),
        ("China backs clean power at COP31", "China"),
        ("N. Korea expands uranium work at Yongbyon", "IAEA"),
        ("Shenzhen summit hailed by China", "Xinhua"),
    ]),
    ("SOUTH & CENTRAL ASIA", (106, 79, 163), "circle", [
        ("ICJ: Myanmar guilty of Rohingya genocide", "ICJ"),
        ("Rahul 124* puts India on top in Wellington", "AP"),
        ("Banda Sea quake 6.8 near Timor", "USGS"),
        ("Taipei: 2,700 China-linked accounts flagged", "Meta"),
        ("Bangkok: arsenic plan for two rivers", "The Nation"),
    ]),
    ("AFRICA", (46, 125, 50), "square", [
        ("S. Africa: ex-deputy president dies at 71", "Ramaphosa"),
        ("South Africa: hail warnings in 7 provinces", "SAWS"),
        ("Port Louis: African rating agency talks", "AU"),
        ("Bayelsa: search on after funeral barge sank", "Nigeria"),
        ("Nairobi: teachers join state payroll", "Kenya"),
    ]),
    ("OCEANIA & SCIENCE / SPACE", (70, 90, 110), "triangle", [
        ("BepiColombo reaches Mercury orbit", "ESA\u2013JAXA"),
        ("Cancer pill: tumours gone in 1 in 12", "Trial"),
        ("UN: \u2018killer robot\u2019 rules by 2028", "UN"),
        ("S&P falls 3.7% in AI sell-off", "Exchanges"),
        ("Canberra: Australia, China agree AI talks", "ABC"),
    ]),
]

NUMBERS = ["COP31 OVERTIME TALKS", "PERU M6.7 QUAKE", "BEPICOLOMBO AT MERCURY",
           "LAS VEGAS GP", "UK-EU RESET"]


def glyph(d, shape, cx, cy, r, color):
    if shape == "circle":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif shape == "square":
        d.rectangle([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif shape == "triangle":
        d.polygon([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)], fill=color)
    else:  # diamond
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=color)


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
    # edition badge
    d.text((512, 112), "24-HOUR WORLD BRIEFING  \u2022  35 VERIFIED STORIES  \u2022  7 REGIONS",
           font=F(SANS_B, 11), fill=RED, anchor="mt")

    # by the numbers strip
    y0 = 134
    cw = (W - 56 - 4 * 8) / 5
    for i, lab in enumerate(NUMBERS):
        x = 28 + i * (cw + 8)
        d.rectangle([x, y0, x + cw, y0 + 34], outline=NAVY, width=1)
        lines = wrap(d, lab, F(SANS_B, 11), cw - 12)
        ly = y0 + (34 - len(lines) * 13) / 2
        for ln in lines:
            d.text((x + cw / 2, ly), ln, font=F(SANS_B, 11), fill=NAVY, anchor="mt")
            ly += 13

    # map centrepiece
    my = 196
    d.text((28, my), "WHERE IT HAPPENED \u2014 21 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, my), "8 HOTSPOTS", font=F(SANS_B, 12), fill=RED, anchor="rt")
    map_x, map_y, map_h = 28, my + 20, 200
    d.rectangle([map_x, map_y, map_x + 968, map_y + map_h], outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + py) for px, py in poly]
        d.polygon(pts, fill=(232, 222, 190), outline=NAVY, width=1)
    # orbit icon top-right
    ox, oy = map_x + 930, map_y + 22
    d.ellipse([ox - 26, oy - 12, ox + 26, oy + 12], outline=GOLD, width=2)
    d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=NAVY)
    d.rectangle([ox + 6, oy - 2, ox + 16, oy + 2], fill=NAVY)
    d.text((ox - 30, oy + 16), "ORBIT \u2014 BEPICOLOMBO", font=F(SANS_B, 9),
           fill=NAVY, anchor="mt")
    for px, py, num in PINS:
        cx, cy = map_x + px, map_y + py
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), num, font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
    d.text((512, map_y + map_h + 6), PIN_LEGEND[0], font=F(SANS_B, 9.5), fill=INK, anchor="mt")
    d.text((512, map_y + map_h + 20), PIN_LEGEND[1], font=F(SANS_B, 9.5), fill=INK, anchor="mt")

    # region grid
    gy = 452
    d.line([28, gy - 8, W - 28, gy - 8], fill=INK, width=2)
    d.text((28, gy), "SEVEN REGIONS \u2014 FIVE STORIES EACH",
           font=F(SANS_B, 12), fill=INK)
    d.text((W - 28, gy), "ALL TIMES UTC", font=F(SANS_B, 12), fill=GREY, anchor="rt")

    def region_block(x, y, w, name, color, shape, items):
        d.rectangle([x, y, x + w, y + 4], fill=color)
        d.text((x, y + 10), name, font=F(SANS_B, 13), fill=color)
        d.line([x, y + 30, x + w, y + 30], fill=INK, width=1)
        iy = y + 38
        for head, src in items:
            glyph(d, shape, x + 6, iy + 6, 5, color)
            block(d, x + 18, iy, head, F(SANS_B, 11.5), w - 18, 13, max_lines=2)
            nlines = len(wrap(d, head, F(SANS_B, 11.5), w - 18))
            d.text((x + 18, iy + min(nlines, 2) * 13 + 1), f"({src})",
                   font=F(SANS, 9), fill=GREY)
            iy += 40

    row1_y = gy + 26
    rw = (W - 56 - 3 * 10) / 4
    for i in range(4):
        name, color, shape, items = REGIONS[i]
        region_block(28 + i * (rw + 10), row1_y, rw, name, color, shape, items)
    row2_y = row1_y + 236
    rw2 = (W - 56 - 2 * 10) / 3
    for i in range(4, 7):
        name, color, shape, items = REGIONS[i]
        region_block(28 + (i - 4) * (rw2 + 10), row2_y, rw2, name, color, shape, items)

    # footer colophon
    fy = 936
    d.line([28, fy, W - 28, fy], fill=INK, width=2)
    d.text((512, fy + 8),
           "SATURDAY 21 NOVEMBER 2026  \u2022  COMPILED FROM VERIFIED GLOBAL WIRE REPORTS  \u2022  ALL TIMES UTC",
           font=F(SANS_B, 11), fill=INK, anchor="mt")
    d.text((512, fy + 26), "Sources: Reuters \u2022 AP \u2022 AFP \u2022 Al Jazeera \u2022 Kyiv Post \u2022 USGS \u2022 UKMTO \u2022 France 24 \u2022 ESA",
           font=F(SANS, 9.5), fill=GREY, anchor="mt")
    d.rectangle([28, 976, W - 28, 1000], fill=RED)
    d.text((512, 982), "THE GLOBAL DISPATCH", font=F(SANS_B, 13),
           fill=(255, 255, 255), anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size)


if __name__ == "__main__":
    render()
