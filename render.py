#!/usr/bin/env python3
"""v2: neater front page modelled on the top entries' look.
1024x1024, 35 stories, 7 regions, coloured pictograms, source tags,
region bar, DATE CHECK footer. Deterministic, no network.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
DARK = (24, 32, 54)
BLUE = (38, 84, 124)
GREY = (96, 96, 92)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
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


def kicker(d, x, y, label):
    f = F(SANS_B, 12)
    tw = d.textlength(label, font=f)
    d.rectangle([x, y, x + tw + 14, y + 19], fill=RED)
    d.text((x + 7, y + 3), label, font=f, fill=(255, 255, 255))


def tag(d, x, y, label, right=None):
    """small status tag; x is left unless right given (right edge)."""
    f = F(SANS_B, 9)
    tw = d.textlength(label, font=f)
    if right is not None:
        x = right - tw - 10
    d.rectangle([x, y, x + tw + 10, y + 14], outline=INK, width=1)
    d.text((x + 5, y + 2), label, font=f, fill=INK)
    return x


# ------------------------------------------------------------- pictograms
def picto(d, key, x, y, w, h):
    """small coloured illustration band inside a tile."""
    cx, cy = x + w / 2, y + h / 2
    if key == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
        d.ellipse([x + 8, y + 4, x + 34, y + h - 4], fill=(90, 140, 200),
                  outline=BLUE, width=1)
        d.ellipse([x + 16, y + 8, x + 26, y + 16], fill=(120, 190, 120))
        d.ellipse([x + 22, y + 16, x + 30, y + 24], fill=(120, 190, 120))
        # thermometer
        d.rectangle([x + 44, y + 6, x + 50, y + h - 8], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([x + 46, y + h - 12, x + 48, y + h - 9], fill=RED)
        d.ellipse([x + 42, y + h - 12, x + 52, y + h - 3], fill=RED)
        # clock
        d.ellipse([x + w - 34, y + 4, x + w - 8, y + h - 4], fill=(255, 255, 255),
                  outline=INK, width=1)
        d.line([x + w - 21, y + h / 2, x + w - 21, y + 9], fill=INK, width=1)
        d.line([x + w - 21, y + h / 2, x + w - 13, y + h / 2 + 3], fill=INK, width=1)
    elif key == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
        pts = [(x + 4, cy + 6), (x + 22, cy + 6), (x + 30, cy - 10), (x + 38, cy + 10),
               (x + 48, cy - 12), (x + 58, cy + 8), (x + 70, cy - 6), (x + 84, cy + 6),
               (x + 110, cy + 6), (x + 122, cy - 8), (x + 134, cy + 6), (x + w - 6, cy + 6)]
        d.line(pts, fill=RED, width=2)
        d.polygon([(x + w - 34, y + h - 4), (x + w - 22, y + 8), (x + w - 10, y + h - 4)],
                  fill=(150, 90, 60))
    elif key == "kyiv":
        d.rectangle([x, y, x + w, y + h], fill=(30, 50, 90))
        d.rectangle([x, y, x + w, y + h / 2], fill=(40, 90, 160))
        d.rectangle([x, y + h / 2, x + w, y + h], fill=(240, 200, 60))
        d.polygon([(cx, y + 5), (cx - 10, y + 22), (cx + 10, y + 22)], fill=(255, 255, 255),
                  outline=RED, width=1)
        d.text((cx, y + 11), "!", font=F(SANS_B, 10), fill=RED, anchor="mt")
    elif key == "court":
        d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210))
        d.polygon([(cx - 34, y + 8), (cx, y + 2), (cx + 34, y + 8)], fill=(120, 100, 70))
        for i in range(4):
            bx = cx - 27 + i * 18
            d.rectangle([bx, y + 10, bx + 6, y + h - 6], fill=(90, 80, 60))
        d.rectangle([cx - 34, y + h - 6, cx + 34, y + h - 3], fill=(120, 100, 70))
    elif key == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.rectangle([cx - 30, cy - 8, cx + 30, cy + 10], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([cx - 4, cy - 5, cx + 4, cy + 7], fill=RED)
        d.rectangle([cx - 10, cy - 1, cx + 10, cy + 3], fill=RED)
        d.line([x + 6, y + h - 3, x + w - 6, y + h - 3], fill=(150, 120, 80), width=2)
    elif key == "hormuz":
        d.rectangle([x, y, x + w, y + h], fill=(70, 130, 180))
        d.polygon([(cx - 40, cy + 2), (cx - 28, cy + 2), (cx - 28, cy - 10),
                   (cx - 20, cy + 2)], fill=(40, 40, 40))
        d.rectangle([cx - 44, cy + 2, cx + 44, cy + 10], fill=(30, 30, 30))
        d.rectangle([cx - 44, cy + 10, cx + 44, cy + 12], fill=RED)
        for wx in range(int(cx - 38), int(cx + 40), 12):
            d.rectangle([wx, cy + 5, wx + 5, cy + 8], fill=(255, 220, 120))
    elif key == "markets":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        pts = [(x + 6, y + 6), (x + 40, y + 10), (x + 70, y + 8), (x + 105, y + 18),
               (x + 140, y + 16), (x + w - 8, y + h - 6)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + w - 16, y + h - 6), (x + w - 4, y + h - 6), (x + w - 8, y + h - 12)],
                  fill=RED)
    elif key == "ukeu":
        d.rectangle([x, y, x + w, y + h], fill=(40, 70, 140))
        for i in range(8):
            a = i * math.pi / 4
            sx, sy = cx - 28 + 10 * math.cos(a), cy + 10 * math.sin(a)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
        d.rectangle([cx + 6, y + 4, cx + 44, y + h - 4], fill=(255, 255, 255))
        d.rectangle([cx + 6, y + 4, cx + 44, y + 9], fill=RED)
        d.rectangle([cx + 6, y + h - 9, cx + 44, y + h - 4], fill=RED)
    elif key == "cyber":
        d.rectangle([x, y, x + w, y + h], fill=(30, 34, 48))
        d.rectangle([cx - 34, y + 5, cx + 34, y + h - 8], fill=(200, 220, 240),
                    outline=(120, 140, 170), width=1)
        d.polygon([(cx, y + 8), (cx - 9, y + 20), (cx + 9, y + 20)], fill=RED)
        d.text((cx - 1, y + 12), "!", font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mt")
    elif key == "bayer":
        d.rectangle([x, y, x + w, y + h], fill=(220, 240, 220))
        d.ellipse([cx - 34, cy - 7, cx + 34, cy + 7], fill=(255, 255, 255),
                  outline=(60, 140, 60), width=2)
        d.rectangle([cx - 2, cy - 7, cx + 2, cy + 7], fill=(60, 140, 60))
        d.text((cx + 42, cy - 6), "$", font=F(SANS_B, 14), fill=(40, 110, 40))
    elif key == "davao":
        d.rectangle([x, y, x + w, y + h], fill=(170, 210, 240))
        d.polygon([(cx - 40, cy), (cx + 34, cy - 4), (cx + 44, cy), (cx + 34, cy + 4),
                   (cx - 40, cy + 2)], fill=(255, 255, 255))
        d.polygon([(cx - 6, cy - 2), (cx + 6, cy - 12), (cx + 10, cy - 2)], fill=(255, 255, 255))
        d.polygon([(cx - 6, cy + 2), (cx + 6, cy + 12), (cx + 10, cy + 2)], fill=(255, 255, 255))
    elif key == "la":
        d.rectangle([x, y, x + w, y + h], fill=(230, 228, 220))
        d.line([(x + 8, y + h - 6), (x + 30, y + 12), (x + 52, y + h - 10),
                (x + 80, y + 8), (x + 110, y + h - 6), (x + w - 8, y + 10)],
               fill=(90, 90, 90), width=2)
        d.rectangle([cx - 26, y + 6, cx - 6, y + 16], fill=(180, 60, 50))
        d.text((cx - 16, y + 8), "4.2", font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mt")


def skyline(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    bx = x + 8
    heights = [0.45, 0.7, 0.55, 0.85, 0.6, 0.75, 0.5]
    for f in heights:
        bw = (w - 16) / len(heights)
        bh = h * f
        d.rectangle([bx, y + h - bh, bx + bw - 3, y + h], fill=(52, 62, 92))
        for wy in range(int(y + h - bh + 6), int(y + h - 4), 12):
            for wx in range(int(bx + 3), int(bx + bw - 6), 9):
                if (wx + wy) % 23 < 9:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        bx += bw
    for sx, sy, ex, ey in [(x + 30, y + 12, x + 130, y + 55),
                           (x + 200, y + 8, x + 300, y + 60),
                           (x + 350, y + 15, x + 430, y + 50)]:
        d.arc([sx, sy, ex, ey + 40], start=200, end=340, fill=(255, 200, 80), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 170, 40))
        for a in range(8):
            ang = a * math.pi / 4
            d.line([ex, ey, ex + 12 * math.cos(ang), ey + 12 * math.sin(ang)],
                   fill=(255, 200, 80), width=2)


def cop31_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    d.ellipse([x + 14, y + 8, x + 78, y + h - 8], fill=(90, 140, 200), outline=BLUE, width=2)
    d.ellipse([x + 30, y + 16, x + 52, y + 32], fill=(120, 190, 120))
    d.ellipse([x + 48, y + 34, x + 66, y + 50], fill=(120, 190, 120))
    d.rectangle([x + 96, y + 10, x + 104, y + h - 14], fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([x + 92, y + h - 20, x + 108, y + h - 4], fill=RED)
    d.rectangle([x + 98, y + h - 26, x + 102, y + h - 12], fill=RED)
    d.ellipse([x + w - 62, y + 8, x + w - 14, y + h - 8], fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + w - 38, y + h / 2, x + w - 38, y + 14], fill=INK, width=2)
    d.line([x + w - 38, y + h / 2, x + w - 24, y + h / 2 + 6], fill=INK, width=2)
    d.text((x + w - 100, y + h - 16), "+1.5\u00b0C", font=F(SANS_B, 12), fill=RED)


def quake_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    cy = y + h / 2
    pts = [(x + 6, cy + 8), (x + 40, cy + 8), (x + 55, cy - 16), (x + 70, cy + 14),
           (x + 88, cy - 18), (x + 106, cy + 10), (x + 130, cy - 8), (x + 160, cy + 8),
           (x + 200, cy + 8), (x + 220, cy - 12), (x + 240, cy + 8), (x + w - 8, cy + 8)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(x + w - 60, y + h - 4), (x + w - 34, y + 12), (x + w - 8, y + h - 4)],
              fill=(150, 90, 60))
    d.text((x + 10, y + 6), "6.7", font=F(SANS_B, 13), fill=RED)


# ------------------------------------------------------------- data
HEROES = [
    ("COP31: OVERTIME", "1 \u00b7 ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
     "Climate summit runs into Saturday with no deal",
     "Nearly 200 nations race to agree a third draft; the last one dropped fossil-fuel mentions. (AFP, CNA)",
     "cop31", "Ongoing \u00b7 AFP, Al Jazeera"),
    ("SAUDI: MISSILES", "2 \u00b7 RIYADH, SAUDI ARABIA \u00b7 WAR",
     "Three Houthi missiles shot down over Riyadh",
     "Second attack on the Saudi capital in days, after its tallest tower was hit on Thursday. No casualties reported. (Reuters)",
     "riyadh", "Coalition says \u00b7 Reuters"),
    ("PERU: QUAKE 6.8", "3 \u00b7 JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
     "Magnitude 6.8 earthquake shakes central Peru",
     "Felt in Lima and on the coast. No deaths, damage or tsunami risk. (USGS, IGP)",
     "quake", "00:09 UTC \u00b7 108 km deep"),
]

TILES = [
    ("4", "KYIV \u00b7 WAR", "Russian strikes kill 12, wound 82",
     "Overnight barrage hits Kryvyi Rih. (Kyiv Post)", "Kyiv Post", "REPORTED", "kyiv"),
    ("5", "ROHINGYA \u00b7 COURT", "UN court: Myanmar guilty of genocide",
     "Historic ICJ ruling for the Rohingya. (ICJ)", "ICJ", "OFFICIAL", "court"),
    ("6", "GAZA \u00b7 AID", "Three killed in strike on aid vehicle",
     "Renewed attacks hit aid supplies. (AFP)", "AFP", "REPORTED", "gaza"),
    ("7", "HORMUZ \u00b7 SEA", "Tanker hit near Strait of Hormuz",
     "Two incidents reported off Oman. (UKMTO)", "UKMTO", "REPORTED", "hormuz"),
    ("8", "MARKETS", "AI sell-off: S&P falls 3.7%",
     "Dow in correction; Anthropic slides. (Exchanges)", "Exchanges", "REPORTED", "markets"),
    ("9", "UK\u2013EU \u00b7 DEAL", "Biggest UK\u2013EU pact since Brexit",
     "Food, carbon, youth mobility deals. (UK govt)", "UK govt", "OFFICIAL", "ukeu"),
    ("10", "CYBER \u00b7 HACKS", "FBI and US farm agency hacked",
     "US outages and hacks continue. (FBI)", "FBI", "REPORTED", "cyber"),
    ("11", "BAYER \u00b7 COURTS", "Bayer pays $7.25bn over Roundup",
     "Settlement ends the claims. (Bayer)", "Bayer", "OFFICIAL", "bayer"),
    ("12", "DAVAO \u00b7 AVIATION", "Jet lands after engine-fire alert",
     "Air Niugini 767: all 146 safe. (AP)", "AP", "OFFICIAL", "davao"),
    ("13", "LA \u00b7 QUAKE", "4.2 quake rocks Los Angeles",
     "No injuries or major damage. (USGS)", "USGS", "OFFICIAL", "la"),
]

INDEX = [
    "Basra power-station fire kills 4",
    "Spain extends bank tax for housing",
    "UN: \u2018killer robot\u2019 rules by 2028",
    "Syria seizes arms bound for Lebanon",
    "Students protest across Europe",
    "Kyiv bridge clear-up \u2018may take a year\u2019",
    "Cargo ship hit by drones off Finland",
    "Trump\u2013Xi: 3-way summit tested",
    "Cancer pill: tumours gone in 1 in 12",
    "N. Korea expands uranium work",
    "Qeshm blast \u2018defence systems\u2019",
    "Kryvyi Rih: 2 killed, 83 hurt",
    "China backs clean power at COP31",
    "Banda Sea quake 6.8 near Timor",
    "Houthi raids cloud Saudi nuclear pact",
    "Shenzhen summit hailed by China",
    "EU: COP31 draft \u2018fossil-fuel summit\u2019",
    "CBO: battleships add billions",
    "COP31 protesters chant \u2018shame\u2019",
    "Hodeidah port struck by coalition",
    "Trump presser after China trip",
    "S. Africa: ex-deputy president dies at 71",
]

NUMBERS = [
    ("400+", "DRONES AT UKRAINE"),
    ("110", "MISSILES FIRED"),
    ("2", "LAND IN POLAND"),
    ("3", "MISSILES DOWNED"),
    ("6.8", "PERU QUAKE"),
    ("146", "SAFE IN DAVAO"),
]

REGIONS = [
    ("Europe", 10, (43, 94, 167)),
    ("Asia", 6, (217, 123, 41)),
    ("Middle East", 8, (178, 34, 34)),
    ("Africa", 1, (46, 125, 50)),
    ("Americas", 5, (14, 124, 123)),
    ("Oceania", 1, (106, 79, 163)),
    ("Global", 5, (119, 119, 119)),
]

CONTINENTS = [
    [(18, 38), (60, 22), (105, 28), (120, 55), (95, 78), (60, 82), (30, 70)],
    [(95, 120), (130, 115), (150, 140), (135, 185), (110, 175), (95, 145)],
    [(215, 30), (250, 22), (265, 45), (245, 60), (220, 52)],
    [(215, 75), (260, 70), (275, 110), (255, 160), (225, 140), (210, 100)],
    [(270, 25), (340, 18), (400, 35), (410, 75), (360, 95), (310, 80), (280, 55)],
    [(360, 160), (395, 155), (405, 180), (375, 190), (355, 175)],
]
DOTS = [(30, 150), (298, 66), (222, 58), (238, 44), (292, 54), (232, 36),
        (272, 34), (268, 24), (375, 75), (120, 50), (385, 55), (302, 72),
        (258, 46), (360, 60), (395, 140), (288, 78), (372, 80), (244, 32),
        (110, 55), (258, 56), (266, 42), (282, 84), (115, 48), (125, 58)]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=RED, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=1)

    # top line
    d.text((28, 20), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
    d.text((W - 28, 20), "35 STORIES  \u2022  7 REGIONS  \u2022  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
           font=F(SANS_B, 10), fill=GREY, anchor="rt")
    d.line([28, 38, W - 28, 38], fill=INK, width=1)
    # masthead
    d.text((512, 44), "Saturday 21 November 2026", font=F(SERIF, 54), fill=INK, anchor="mt")
    d.text((512, 104),
           "COP31 talks run into overtime  \u2022  Three missiles downed over Riyadh  \u2022  Russia strikes Kyiv again",
           font=F(SERIF_I, 15), fill=INK, anchor="mt")
    d.line([28, 126, W - 28, 126], fill=INK, width=2)

    # numbers strip
    y0 = 134
    cw = (W - 56 - 5 * 8) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = 28 + i * (cw + 8)
        d.rectangle([x, y0, x + cw, y0 + 46], outline=INK, width=1)
        d.text((x + cw / 2, y0 + 3), num, font=F(SANS_B, 21), fill=RED, anchor="mt")
        d.text((x + cw / 2, y0 + 27), lab, font=F(SANS_B, 9), fill=INK, anchor="mt")
    # region bar
    ry = 188
    total = sum(c for _, c, _ in REGIONS)
    bx = 28
    bar_w = W - 56
    for name, count, color in REGIONS:
        seg = bar_w * count / total
        d.rectangle([bx, ry, bx + seg, ry + 14], fill=color)
        bx += seg
    lx = 28
    d.text((28, ry + 18), "Europe 9", font=F(SANS_B, 10), fill=(43, 94, 167))
    d.text((150, ry + 18), "Asia 6", font=F(SANS_B, 10), fill=(217, 123, 41))
    d.text((215, ry + 18), "Middle East 8", font=F(SANS_B, 10), fill=(178, 34, 34))
    d.text((330, ry + 18), "Africa 1", font=F(SANS_B, 10), fill=(46, 125, 50))
    d.text((400, ry + 18), "Americas 5", font=F(SANS_B, 10), fill=(14, 124, 123))
    d.text((490, ry + 18), "Oceania 1", font=F(SANS_B, 10), fill=(106, 79, 163))
    d.text((575, ry + 18), "Global 5", font=F(SANS_B, 10), fill=(119, 119, 119))
    d.line([28, ry + 34, W - 28, ry + 34], fill=INK, width=2)

    # heroes
    hy = 230
    hw = (W - 56 - 2 * 12) / 3
    hh = 190
    for i, (kick, sub, head, cap, art, src) in enumerate(HEROES):
        x = 28 + i * (hw + 12)
        d.rectangle([x, hy, x + hw, hy + hh], outline=INK, width=1)
        if art == "cop31":
            cop31_art(d, x + 1, hy + 1, hw - 2, 62)
        elif art == "riyadh":
            skyline(d, x + 1, hy + 1, hw - 2, 62)
        else:
            quake_art(d, x + 1, hy + 1, hw - 2, 62)
        kicker(d, x + 8, hy + 69, kick)
        d.text((x + 8, hy + 92), sub, font=F(SANS_B, 10), fill=GREY)
        block(d, x + 8, hy + 106, head, F(SERIF, 18), hw - 16, 21, max_lines=2)
        block(d, x + 8, hy + 150, cap, F(SANS, 11), hw - 16, 13, color=(60, 60, 60),
              max_lines=2)
        d.text((x + hw - 8, hy + hh - 16), src, font=F(SANS, 9), fill=GREY, anchor="rt")

    # tiles 2 rows x 5
    ty = 430
    tw = (W - 56 - 4 * 8) / 5
    th = 116
    for i, (num, place, head, cap, src, status, key) in enumerate(TILES):
        r, c = divmod(i, 5)
        x = 28 + c * (tw + 8)
        y = ty + r * (th + 8)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        d.text((x + 6, y + 4), f"{num} \u00b7 {place}", font=F(SANS_B, 9.5), fill=INK)
        tag(d, 0, y + 4, status, right=x + tw - 5)
        picto(d, key, x + 1, y + 20, tw - 2, 30)
        block(d, x + 6, y + 54, head, F(SERIF, 12.5), tw - 12, 14, max_lines=2)
        block(d, x + 6, y + 84, cap, F(SANS, 9.5), tw - 12, 11, color=(60, 60, 60),
              max_lines=2)

    # map + index
    my = 678
    d.line([28, my - 6, W - 28, my - 6], fill=INK, width=2)
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 14), fill=INK)
    d.text((W - 28, my), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=F(SANS_B, 14), fill=INK, anchor="rt")
    map_x, map_y, map_w, map_h = 28, my + 24, 420, 190
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(214, 228, 238),
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + int(py * 0.76)) for px, py in poly]
        d.polygon(pts, fill=(236, 214, 170), outline=BLUE)
    for n, (dx, dy) in enumerate(DOTS):
        cx, cy = map_x + dx, map_y + int(dy * 0.76)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(14 + n), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
    ix = 470
    iy = my + 24
    col_w = (W - 28 - ix - 10) / 2
    for n, item in enumerate(INDEX):
        col = 0 if n < 11 else 1
        row = n if n < 11 else n - 11
        x = ix + col * (col_w + 10)
        y = iy + row * 17
        d.text((x, y), f"{14 + n}.", font=F(SANS_B, 11), fill=RED)
        d.text((x + 26, y), item, font=F(SANS, 11), fill=INK)
    d.text((28, my + 220), "1\u201313 above.",
           font=F(SANS, 10), fill=GREY)

    # date check
    dy = 906
    d.rectangle([28, dy, W - 28, dy + 42], outline=RED, width=2)
    block(d, 36, dy + 4,
          "DATE CHECK \u2713  Every story on this page happened, or was first reported, on Saturday 21 November 2026 in at least one time zone. Left out as earlier news: Shenzhen summit (Thu 19 Nov); Kerch Bridge first hit (Mon 16 Nov); Cyclone Akvan landfall (Fri 20 Nov). Claims by one side are marked CLAIM; tolls are as first reported.",
          F(SANS, 10.5), W - 72, 13, color=INK, max_lines=3)
    # sources + footer
    d.text((512, 954), "Sources named beside each story: Reuters \u2022 AP \u2022 AFP \u2022 Al Jazeera \u2022 Kyiv Post \u2022 USGS \u2022 UKMTO \u2022 France 24",
           font=F(SANS, 9.5), fill=GREY, anchor="mt")
    d.rectangle([28, 968, W - 28, 996], fill=RED)
    d.text((512, 975), "SATURDAY 21 NOVEMBER 2026  \u2022  THE WORLD IN ONE DAY",
           font=F(SANS_B, 13), fill=(255, 255, 255), anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size)


if __name__ == "__main__":
    render()
