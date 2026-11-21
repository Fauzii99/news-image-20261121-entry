#!/usr/bin/env python3
"""v7 FINAL: the Top-10 winning skeleton (all 12-0) rebuilt for 21 Nov 2026.
- Giant date masthead (~84px condensed serif): Saturday 21 November 2026.
- 35 verified Saturday stories: 3 big heroes + 10 tiles (4-13) + 22-item
  numbered index (14-35). 6-figure numbers strip + 7-region counts bar.
- Numbered map pins 1-13 matching the illustrated stories.
- DATE CHECK footer: Friday 20 Nov news explicitly excluded + unconfirmed
  items (BepiColombo orbit, final COP31 text).
- Verification badges OFFICIAL / CONFIRMED / REPORTED + sources on every
  main story. Masthead in Noto Serif ExtraCondensed Bold (auto-fit to 82px).
  Hero headlines at 20px so all three fit two lines whole. Deterministic.
  DO NOT SUBMIT before user ACC.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 244, 235)
CARD = (250, 247, 240)
INK = (17, 19, 23)
RED = (200, 50, 40)
CRIMSON = (184, 32, 24)
NAVY = (29, 53, 87)
GOLD = (201, 162, 39)
GREY = (110, 110, 105)
GREEN = (46, 125, 50)
TEAL = (14, 124, 123)
AMBER = (183, 121, 31)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MASTHEAD = "/usr/share/fonts/truetype/noto/NotoSerif-ExtraCondensedBold.ttf"
MASTHEAD_NUM = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
MAP_PATH = "world_map5.png"  # committed in this repo; Natural Earth 110m land


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


def badge(d, x, y, text, color):
    """Small verification pill, right-aligned at x (x = right edge)."""
    f = F(SANS_B, 9)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw - 10, y, x, y + 13], radius=6, fill=color)
    d.text((x - tw / 2 - 5, y + 1), text, font=f, fill=(255, 255, 255), anchor="mt")


def kicker_label(d, x, y, text, size=17):
    """Red kicker label inside an illustration (top-left)."""
    f = F(SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 16, y + size + 10], fill=RED)
    d.text((x + 8, y + 4), text, font=f, fill=(255, 255, 255))


def stat_chip(d, x, y, text):
    """White stat chip inside an illustration (bottom-left)."""
    f = F(SANS_B, 12)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 12, y + 20], fill=(255, 255, 255))
    d.text((x + 6, y + 3), text, font=f, fill=INK)


# ------------------------------------------------- hero illustrations (316x140)
def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 224))
    # globe, thermometer and clock sit BELOW the kicker/badge row (y+40..)
    d.ellipse([x + 14, y + 44, x + 62, y + 92], fill=(140, 190, 220))
    d.ellipse([x + 24, y + 54, x + 40, y + 68], fill=(110, 185, 110))
    d.ellipse([x + 42, y + 70, x + 54, y + 80], fill=(110, 185, 110))
    d.rectangle([x + 74, y + 50, x + 84, y + 86], fill=(220, 220, 220), outline=INK, width=1)
    d.rectangle([x + 76, y + 56, x + 82, y + 82], fill=(200, 50, 40))
    d.ellipse([x + 72, y + 82, x + 86, y + 96], fill=(200, 50, 40))
    d.ellipse([x + w - 64, y + 44, x + w - 16, y + 92], fill=(255, 255, 255),
              outline=RED, width=3)
    d.line([x + w - 40, y + 68, x + w - 40, y + 50], fill=INK, width=3)
    d.line([x + w - 40, y + 68, x + w - 26, y + 74], fill=INK, width=3)
    d.ellipse([x + w - 42, y + 66, x + w - 38, y + 70], fill=RED)
    d.rectangle([x + 30, y + h - 44, x + w - 30, y + h - 8], fill=(255, 255, 255),
                outline=NAVY, width=2)
    d.pieslice([x + 110, y + 52, x + w - 110, y + h - 28], start=180, end=360,
               fill=(90, 140, 200), outline=NAVY, width=2)
    for i in range(5):
        bx = x + 52 + i * 46
        d.rectangle([bx, y + h - 44, bx + 12, y + h - 8], fill=NAVY)
    for i in range(4):
        d.rectangle([x + 76 + i * 46, y + h - 36, x + 86 + i * 46, y + h - 16],
                    fill=(180, 210, 240))


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 24, 50))
    for sx, sy in [(16, 14), (80, 10), (150, 16), (220, 12), (280, 18), (120, 30),
                   (200, 34), (40, 48)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x + w - 102, y + 8, x + w - 74, y + 36], fill=(250, 228, 180))
    d.polygon([(x, y + h), (x, y + h - 30), (x + w * 0.35, y + h - 46),
               (x + w * 0.7, y + h - 26), (x + w, y + h - 38), (x + w, y + h)],
              fill=(206, 158, 84))
    d.polygon([(x, y + h), (x, y + h - 14), (x + w * 0.5, y + h - 22),
               (x + w, y + h - 10), (x + w, y + h)], fill=(178, 132, 64))
    d.rectangle([x + 24, y + h - 64, x + 40, y + h - 26], fill=(16, 14, 34))
    d.rectangle([x + 50, y + h - 78, x + 62, y + h - 26], fill=(16, 14, 34))
    d.polygon([(x + 50, y + h - 88), (x + 56, y + h - 78), (x + 62, y + h - 88)],
              fill=(16, 14, 34))
    d.rectangle([x + 72, y + h - 56, x + 94, y + h - 26], fill=(16, 14, 34))
    for wx in range(int(x + 28), int(x + 90), 10):
        d.rectangle([wx, y + h - 48, wx + 4, y + h - 42], fill=(255, 214, 120))
    for fx, fy in [(x + 140, y + 28), (x + 220, y + 36), (x + 280, y + 24)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([fx, fy, fx + 18 * math.cos(ang), fy + 18 * math.sin(ang)],
                   fill=(255, 130, 30), width=3)
        d.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=(255, 200, 90))
        d.arc([fx - 46, fy - 10, fx + 14, fy + 50], start=300, end=60,
              fill=(235, 235, 235), width=2)


def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    d.polygon([(x, y + h), (x + 55, y + 30), (x + 115, y + h)], fill=(118, 116, 110))
    d.polygon([(x + 80, y + h), (x + 165, y + 14), (x + 255, y + h)], fill=(86, 84, 80))
    d.polygon([(x + 220, y + h), (x + 285, y + 34), (x + w, y + h)], fill=(140, 136, 128))
    d.polygon([(x + 153, y + 14), (x + 165, y + 32), (x + 177, y + 14), (x + 165, y + 6)],
              fill=(255, 255, 255))
    d.polygon([(x + 272, y + 34), (x + 285, y + 48), (x + 298, y + 34), (x + 285, y + 28)],
              fill=(255, 255, 255))
    for hx in [x + 22, x + 268]:
        d.rectangle([hx, y + h - 22, hx + 22, y + h - 6], fill=(150, 90, 60))
        d.polygon([(hx - 2, y + h - 22), (hx + 11, y + h - 32), (hx + 24, y + h - 22)],
                  fill=(120, 60, 40))
    cy = y + h * 0.62
    pts = [(x + 8, cy + 10), (x + 44, cy + 10), (x + 58, cy - 18), (x + 74, cy + 18),
           (x + 94, cy - 22), (x + 114, cy + 12), (x + 142, cy - 12), (x + 176, cy + 10),
           (x + 228, cy + 10), (x + 246, cy - 14), (x + 264, cy + 10), (x + w - 8, cy + 10)]
    d.line(pts, fill=RED, width=4)
    d.line([(x + 104, y + h - 8), (x + 122, y + h - 38), (x + 140, y + h - 14)],
           fill=RED, width=3)


# ------------------------------------------------- tile art strips (187x36)
def tile_art(d, key, x, y, w, h):
    if key == "kyiv":
        d.rectangle([x, y, x + w, y + h], fill=(58, 110, 190))
        d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(240, 200, 40))
        d.polygon([(x + 20, y + h), (x + 60, y + 6), (x + 100, y + h)], fill=(30, 30, 40))
        d.polygon([(x + 90, y + h), (x + 130, y + 10), (x + 170, y + h)], fill=(30, 30, 40))
        d.polygon([(x + w - 26, y + 4), (x + w - 16, y + 20), (x + w - 36, y + 20)],
                  fill=(255, 200, 0), outline=INK)
        d.text((x + w - 26, y + 8), "!", font=F(SANS_B, 12), fill=INK, anchor="mt")
    elif key == "hormuz":
        d.rectangle([x, y, x + w, y + h], fill=(24, 60, 110))
        d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(16, 40, 80))
        d.ellipse([x + 70, y + 6, x + 110, y + 18], fill=(180, 180, 190))
        d.line([x + 60, y + 12, x + 120, y + 12], fill=(220, 220, 220), width=2)
        d.rectangle([x + 130, y + h - 12, x + 165, y + h - 4], fill=(120, 120, 130))
        d.line([x + 140, y + h - 12, x + 140, y + h - 20], fill=(120, 120, 130), width=2)
    elif key == "iran":
        d.rectangle([x, y, x + w, y + h], fill=(240, 236, 220))
        d.ellipse([x + 40, y + 6, x + w - 40, y + h - 6], fill=(255, 255, 255),
                  outline=INK, width=2)
        d.ellipse([x + w / 2 - 11, y + h / 2 - 11, x + w / 2 + 11, y + h / 2 + 11],
                  fill=(200, 50, 40))
        d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4], fill=INK)
    elif key == "trump":
        d.rectangle([x, y, x + w, y + h], fill=(20, 30, 70))
        for i in range(5):
            d.rectangle([x + i * 38, y, x + i * 38 + 19, y + h], fill=(200, 50, 40))
        d.text((x + w / 2, y + 2), "%", font=F(SANS_B, 28), fill=(255, 255, 255),
               anchor="mt")
    elif key == "chinajapan":
        d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
        d.rectangle([x + 30, y + 6, x + 85, y + h - 6], fill=(222, 41, 16))
        for sx, sy in [(38, 12), (52, 10), (46, 20), (60, 18), (66, 12)]:
            d.polygon([(x + sx, y + sy - 3), (x + sx + 1, y + sy + 1),
                       (x + sx + 4, y + sy + 1), (x + sx + 2, y + sy + 3),
                       (x + sx + 3, y + sy + 6), (x + sx, y + sy + 4),
                       (x + sx - 3, y + sy + 6), (x + sx - 2, y + sy + 3),
                       (x + sx - 4, y + sy + 1), (x + sx - 1, y + sy + 1)],
                      fill=(255, 222, 0))
        d.rectangle([x + 105, y + 6, x + 160, y + h - 6], fill=(255, 255, 255),
                    outline=(200, 200, 200), width=1)
        d.ellipse([x + 122, y + 12, x + 143, y + h - 12], fill=(188, 0, 45))
    elif key == "davao":
        d.rectangle([x, y, x + w, y + h], fill=(150, 200, 235))
        d.ellipse([x + 20, y + 4, x + 60, y + 12], fill=(255, 255, 255))
        d.ellipse([x + 120, y + 8, x + 150, y + 14], fill=(255, 255, 255))
        d.polygon([(x + 55, y + 22), (x + 130, y + 22), (x + 145, y + 28),
                   (x + 55, y + 28)], fill=(255, 255, 255))
        d.polygon([(x + 130, y + 22), (x + 150, y + 14), (x + 155, y + 22)], fill=(255, 255, 255))
        d.polygon([(x + 70, y + 28), (x + 78, y + 34), (x + 66, y + 34)], fill=(255, 255, 255))
        d.rectangle([x, y + h - 4, x + w, y + h], fill=(90, 90, 95))
    elif key == "canberra":
        d.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
        d.rounded_rectangle([x + 20, y + 5, x + 85, y + 22], radius=8, fill=(200, 50, 40))
        d.rounded_rectangle([x + 100, y + 14, x + 165, y + 31], radius=8, fill=(29, 53, 87))
        d.polygon([(x + 30, y + 22), (x + 36, y + 28), (x + 38, y + 22)], fill=(200, 50, 40))
        d.polygon([(x + 150, y + 31), (x + 156, y + 34), (x + 158, y + 31)], fill=(29, 53, 87))
    elif key == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(16, 20, 36))
        d.ellipse([x + 14, y + 5, x + 44, y + h - 5], fill=(247, 147, 26))
        d.text((x + 29, y + 6), "B", font=F(SANS_B, 20), fill=(255, 255, 255), anchor="mt")
        d.line([(x + 60, y + 10), (x + 95, y + 14), (x + 120, y + 8), (x + 150, y + 20),
                (x + 175, y + 28)], fill=(220, 60, 50), width=3)
        d.polygon([(x + 168, y + 28), (x + 178, y + 24), (x + 178, y + 32)], fill=(220, 60, 50))
    elif key == "f1":
        d.rectangle([x, y, x + w, y + h], fill=(14, 16, 34))
        d.rounded_rectangle([x + 12, y + 5, x + w - 12, y + h - 5], radius=10,
                            outline=(255, 220, 60), width=3)
        d.rectangle([x + 60, y + 13, x + 90, y + 21], fill=(220, 60, 50),
                    outline=(255, 255, 255), width=1)
        d.rectangle([x + 120, y + 13, x + 150, y + 21], fill=(50, 130, 230),
                    outline=(255, 255, 255), width=1)
    elif key == "rahul":
        d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
        d.rectangle([x + 30, y + 8, x + 38, y + h - 8], fill=(240, 220, 160))
        d.rectangle([x + 30, y + 8, x + 38, y + 14], fill=(120, 60, 40))
        d.ellipse([x + 120, y + 10, x + 134, y + 24], fill=(200, 50, 40))
        d.rectangle([x + 150, y + 6, x + 154, y + 26], fill=(240, 220, 160))
        d.rectangle([x + 162, y + 6, x + 166, y + 26], fill=(240, 220, 160))
        d.rectangle([x + 174, y + 6, x + 178, y + 26], fill=(240, 220, 160))


# ------------------------------------------------- story data (35, Saturday 21 Nov 2026)
HEROES = [
    dict(num=1, kicker="COP31: OVERTIME", stat="No deal \u00b7 day 13",
         loc="1 ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         head="Climate summit runs into Saturday with no deal",
         body="A draft with no fossil fuels split nearly 200 countries. (AFP, Al Jazeera)",
         badge="CONFIRMED", badge_color=TEAL, art=art_cop31),
    dict(num=2, kicker="SAUDI: MISSILES", stat="3 shot down",
         loc="2 RIYADH, SAUDI ARABIA \u00b7 WAR",
         head="Three Houthi missiles shot down over Riyadh",
         body="Three destroyed over Riyadh before dawn and two over Jizan. (AFP, Dawn)",
         badge="OFFICIAL", badge_color=GREEN, art=art_riyadh),
    dict(num=3, kicker="PERU: QUAKE 6.7", stat="00:09 UTC \u00b7 108 km deep",
         loc="3 JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake near Carhuamayo was felt in Lima and along the coast. (USGS, IGP)",
         badge="OFFICIAL", badge_color=GREEN, art=art_peru),
]

TILES = [
    dict(num=4, kicker="KYIV: WARNING", loc="4 KYIV \u00b7 WAR", art="kyiv",
         head="Zelensky: Crimea bridge \u2018will not stay\u2019",
         body="He warns of double-tap strikes. (NBC)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=5, kicker="HORMUZ: DRONE", loc="5 HORMUZ \u00b7 WAR", art="hormuz",
         head="Iran says it shot down a US drone",
         body="No confirmation from Washington. (IRIB)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=6, kicker="IRAN: URANIUM", loc="6 TEHRAN \u00b7 IRAN", art="iran",
         head="Iran: uranium stock stays in the country",
         body="Minister still seeks a \u2018fair solution\u2019. (ToI)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=7, kicker="TRUMP: AI TAX", loc="7 WASHINGTON", art="trump",
         head="Trump vows tax on data centres abroad",
         body="\u2018Tremendous\u2019 penalty; no details yet. (ABC)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=8, kicker="CHINA\u2013JAPAN", loc="8 BEIJING \u00b7 CHINA", art="chinajapan",
         head="China tells Japan: \u2018correct\u2019 Taiwan words",
         body="Tokyo says its stance is unchanged. (Ministry, AFP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=9, kicker="DAVAO: 146 SAFE", loc="9 DAVAO \u00b7 AVIATION", art="davao",
         head="Jet lands safely after engine fire alert",
         body="Air Niugini 767 diverts after midnight. (Airline, AP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=10, kicker="CANBERRA: AI", loc="10 CANBERRA \u00b7 AI", art="canberra",
         head="Australia and China agree to AI talks",
         body="Albanese ends an 11-day trip. (ABC)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=11, kicker="BITCOIN: $58,983", loc="11 MARKETS", art="bitcoin",
         head="Bitcoin slips below $59,000 Saturday",
         body="Down 3.9% in 24 hours; ether $1,625. (CoinGecko)",
         badge="CONFIRMED", badge_color=TEAL),
    dict(num=12, kicker="RUSSELL: P1", loc="12 LAS VEGAS \u00b7 F1", art="f1",
         head="Russell fastest in Las Vegas practice",
         body="1:34.041 in a damp, messy session. (Formula 1)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=13, kicker="RAHUL: 124*", loc="13 WELLINGTON \u00b7 NZ", art="rahul",
         head="Rahul hits a century vs New Zealand",
         body="India 344 for 2 at tea, replying to 368. (AFP)",
         badge="OFFICIAL", badge_color=GREEN),
]

INDEX = [
    (14, "Kryvyi Rih: Strike kills 2, injures 42 (Kyiv Ind.)"),
    (15, "Copenhagen: Russian attack expelled (Al Jazeera)"),
    (16, "Antalya: EU warns COP31 risks a \u2018fossil\u2019 summit (AFP)"),
    (17, "Antalya: Panama may block climate text (Al Jazeera)"),
    (18, "Antalya: Indonesia signs clean-power deals (Antara)"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea (Al Jazeera)"),
    (20, "Washington: Vance: Iran strikes were Trump\u2019s call (Reuters)"),
    (21, "Washington: Lawmaker threatens SpaceX\u2019s funding (CNN)"),
    (22, "Texas: Execution of a man of 70 takes 63 minutes (ABC)"),
    (23, "Los Angeles: Jury convicts man of starting Palisades fire (ABC)"),
    (24, "Missouri: Judge approves $7.25bn Roundup settlement (AFP)"),
    (25, "Vancouver: Canada rests defence in youth climate trial (AFP)"),
    (26, "Pyongyang: Kim tours factories after no Trump meeting (AFP)"),
    (27, "Sejong: Freight train derails; no one hurt (Korea Herald)"),
    (28, "Taipei: Budget and a cash payout are passed (Taipei Times)"),
    (29, "Bangkok: Six-point plan on arsenic in two rivers (The Nation)"),
    (30, "New Delhi: Pakistani minister joins SCO forum in India (Dawn)"),
    (31, "Eastern India: Rain alerts as Akvan\u2019s remnants move inland (ETV)"),
    (32, "Myanmar: Rights groups urge sanctions after court ruling (AP)"),
    (33, "Port Louis: African rating agency talks to 15 states (Al Jazeera)"),
    (34, "Melbourne: Cummins keeps the Australian captaincy (ABC)"),
    (35, "Las Vegas: Verstappen sent to stewards after contact (Autosport)"),
]

NUMBERS = [
    ("13", "DAY OF COP31", "MEANT TO CLOSE DAY 12"),
    ("3", "MISSILES SHOT DOWN", "OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE", "PERU QUAKE"),
    ("146", "PEOPLE SAFE AFTER", "A JET EMERGENCY LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY", "DOWN 3.9% IN A DAY"),
    ("124*", "K L RAHUL\u2019S SCORE", "AT TEA IN WELLINGTON"),
]

# region counts, must sum to 35 (matches the story list above)
REGIONS = [
    ("EUROPE", 6, (46, 90, 172)),
    ("ASIA", 10, (194, 94, 0)),
    ("MIDDLE EAST", 4, (200, 50, 40)),
    ("AFRICA", 1, (123, 75, 166)),
    ("AMERICAS", 10, (14, 124, 107)),
    ("OCEANIA", 3, (74, 144, 194)),
    ("GLOBAL", 1, (107, 107, 107)),
]

# map pins 1-13 (pixel positions on the 340x123 map, nudged to avoid overlap)
PINS = [
    (1, 236, 822), (2, 242, 826), (3, 127, 859), (4, 220, 797),
    (5, 268, 822), (6, 252, 802), (7, 120, 826), (8, 308, 811),
    (9, 317, 842), (10, 336, 878), (11, 134, 842), (12, 89, 815),
    (13, 358, 890),
]


def index_item(d, x, y, num, text, max_w):
    """One numbered index line; shrinks the font until it fits one line."""
    for size in (10, 9.5, 9):
        f = F(SANS, size)
        fb = F(SANS_B, size)
        w = d.textlength(f"{num} ", font=fb) + d.textlength(text, font=f)
        if w <= max_w:
            break
    d.text((x, y), f"{num} ", font=fb, fill=RED)
    d.text((x + d.textlength(f"{num} ", font=fb), y), text, font=f, fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # top bar
    d.rectangle([28, 10, W - 28, 30], fill=CRIMSON)
    d.text((34, 13), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=(255, 255, 255))
    d.text((W - 34, 13), "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=(255, 255, 255), anchor="rt")

    # giant date masthead (auto-fit, max 88px)
    mast = "Saturday 21 November 2026"
    msize = 88
    while msize > 60:
        mf = ImageFont.truetype(MASTHEAD, msize)
        if d.textlength(mast, font=mf) <= 960:
            break
        msize -= 2
    d.text((512, 34), mast, font=mf, fill=INK, anchor="mt")
    d.text((512, 120), "COP31 talks run into overtime \u00b7 missiles over Riyadh \u00b7 a quake shakes Peru",
           font=F(SERIF_I, 17), fill=INK, anchor="mt")

    # numbers strip: 6 verified Saturday figures
    ny = 146
    d.line([28, ny - 6, W - 28, ny - 6], fill=INK, width=1)
    colw = (W - 56) // 6
    for i, (num, l1, l2) in enumerate(NUMBERS):
        cx = 28 + i * colw + colw // 2
        d.text((cx, ny), num, font=F(MASTHEAD_NUM, 30), fill=RED, anchor="mt")
        d.text((cx, ny + 32), l1, font=F(SANS_B, 11), fill=INK, anchor="mt")
        d.text((cx, ny + 45), l2, font=F(SANS_B, 11), fill=INK, anchor="mt")
        if i:
            d.line([28 + i * colw, ny, 28 + i * colw, ny + 56], fill=GREY, width=1)
    d.line([28, ny + 60, W - 28, ny + 60], fill=INK, width=1)

    # region counts bar (widths proportional to counts, total 35;
    # narrow segments get a 56px minimum so their labels fit)
    ry = 212
    total = sum(c for _, c, _ in REGIONS)
    assert total == 35, total
    minw = 56
    flex = (W - 56) - minw * len(REGIONS)
    flex_total = sum(max(c - 1, 0) for _, c, _ in REGIONS)
    rx = 28
    for name, count, color in REGIONS:
        segw = minw + flex * max(count - 1, 0) / flex_total
        d.rectangle([rx, ry, rx + segw, ry + 16], fill=color)
        d.text((rx + segw / 2, ry + 3), f"{name} {count}", font=F(SANS_B, 10),
               fill=(255, 255, 255), anchor="mt")
        rx += segw

    # 3 big heroes
    hy, hh = 234, 250
    hw = (W - 56 - 2 * 10) // 3
    for i, hro in enumerate(HEROES):
        x = 28 + i * (hw + 10)
        y = hy
        d.rectangle([x, y, x + hw, y + hh], outline=INK, width=1)
        hro["art"](d, x + 1, y + 1, hw - 2, 140)
        kicker_label(d, x + 8, y + 8, hro["kicker"], 17)
        stat_chip(d, x + 8, y + 140 - 26, hro["stat"])
        badge(d, x + hw - 8, y + 8, hro["badge"], hro["badge_color"])
        d.text((x + 8, y + 148), hro["loc"], font=F(SANS_B, 12), fill=RED)
        block(d, x + 8, y + 166, hro["head"], F(SERIF_B, 20), hw - 16, 22, max_lines=2)
        block(d, x + 8, y + 214, hro["body"], F(SANS, 13), hw - 16, 16, max_lines=2)

    # 10 tiles (4-13), 2 rows x 5
    tw = (W - 56 - 4 * 8) // 5
    th = 140
    for i, t in enumerate(TILES):
        r, c = divmod(i, 5)
        x = 28 + c * (tw + 8)
        y = 492 + r * (th + 8)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        d.rectangle([x, y, x + tw, y + 18], fill=RED)
        d.text((x + 6, y + 3), t["kicker"], font=F(SANS_B, 11), fill=(255, 255, 255))
        tile_art(d, t["art"], x + 1, y + 19, tw - 2, 36)
        d.text((x + 6, y + 58), t["loc"], font=F(SANS_B, 10), fill=RED)
        badge(d, x + tw - 6, y + 58, t["badge"], t["badge_color"])
        block(d, x + 6, y + 74, t["head"], F(SANS_B, 15), tw - 12, 17, max_lines=2)
        block(d, x + 6, y + 110, t["body"], F(SANS, 11), tw - 12, 13, max_lines=2)

    # map + numbered index
    my = 788
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    d.text((W - 28, my), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=F(SANS_B, 13), fill=RED, anchor="rt")
    map_img = Image.open(MAP_PATH).resize((340, 123), Image.LANCZOS)
    img.paste(map_img, (28, 804))
    d.rectangle([28, 804, 368, 927], outline=INK, width=1)
    for num, px, py in PINS:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=F(SANS_B, 9), fill=(255, 255, 255),
               anchor="mm")
    d.text((28, 930), "Red numbers mark stories 1\u201313. Each number is the story",
           font=F(SANS, 10), fill=INK)
    d.text((28, 942), "with that number on this page.",
           font=F(SANS, 10), fill=INK)
    d.text((28, 952), "HOW WE CHECKED: CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on the record",
           font=F(SANS_B, 9), fill=GREY)
    colw2 = (W - 28 - 376 - 8) // 2
    for i, (num, text) in enumerate(INDEX):
        col, row = divmod(i, 11)
        x = 376 + col * (colw2 + 8)
        y = 804 + row * 14
        index_item(d, x, y, num, text, colw2)

    # DATE CHECK footer (wrapped: label inline on line 1, body on lines 1-2)
    dy = 962
    d.rectangle([28, dy, W - 28, dy + 34], outline=RED, width=2)
    lab = "DATE CHECK \u2014 "
    lab_w = d.textlength(lab, font=F(SANS_B, 11))
    d.text((34, dy + 4), lab, font=F(SANS_B, 11), fill=RED)
    dc = ("Left out as Friday 20 November\u2019s news: Wall Street\u2019s fall into a correction, "
          "the Russian barrage that hit Kyiv\u2019s bridges, the missile that landed in Poland, "
          "the UK\u2013EU deal and Cyclone Akvan\u2019s landfall. Not confirmed when drawn, so not "
          "shown: BepiColombo in Mercury orbit, a final COP31 text.")
    words = dc.split()
    lines, cur, first = [], "", True
    for wd in words:
        maxw = (990 - 34 - lab_w) if first else (990 - 34)
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=F(SANS, 11)) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
            first = False
    if cur:
        lines.append(cur)
    d.text((34 + lab_w, dy + 4), lines[0], font=F(SANS, 11), fill=INK)
    if len(lines) > 1:
        d.text((34, dy + 18), lines[1], font=F(SANS, 11), fill=INK)

    # colophon
    d.text((512, 1000),
           "Every story here happened, or was first reported, on Saturday 21 November 2026. Sources named beside each story \u00b7 original drawings",
           font=F(SANS, 10), fill=GREY, anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size, "masthead size:", msize)


if __name__ == "__main__":
    render()
