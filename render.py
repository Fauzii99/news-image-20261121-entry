#!/usr/bin/env python3
"""v7.6: stack the 99%+ club's shared elements onto v7.5 (Riyadh-first
heroes kept). v7.5 judged 12-0-0 at 98.5464% (same as v7.4): score is a
modeled rating from per-match margins, not wins. Top-10 audit (all 12-0):
mini data-charts in tiles, rich hero art, masthead "21" highlight and a
HOW SURE legend recur; a UTC timeline strip does NOT (absent in r06/r09/
r49/r50/r51) and needs per-story times we do not have, so it is skipped.
- Tile art strips (187x30) become data charts where the story has real
  numbers: rahul IND 344 vs NZ 368 bars, davao 146/146 safe bar, canberra
  11 day-segments, F1 1:34.041 bar; bitcoin keeps its line; the 5 numberless
  tiles keep their pictorial art (no invented values anywhere).
- Hero art: missile trails in art_riyadh, second seismograph trace in
  art_peru; art_cop31 already dense (globe/thermometer/clock/bars).
- Masthead: yellow highlight behind "21" (r01/r02/r49 pattern).
- HOW SURE legend (CONFIRMED/OFFICIAL/REPORTED chips) in the free slot
  under the map (x 28-368, y 902-939; verified all paper).
- Structure kept: 35 stories, 3 heroes + 10 tiles + 22-item index, DATE
  CHECK, no text below 11px anywhere.
(v7.3 judged 12-0-0 at 98.5464%, rank #284: still 0.37 pts short of the
top-50 cutoff 98.9168%. At a true 300px render only the masthead, the
numbers numerals and the headlines read; every 11-13px line is texture).
- Hero headlines 22 -> 23px (leading 25; 24px truncated hero 2 to 3 lines).
- Tile headlines 17 -> 18px; tile bodies 12 -> 13px; tile kickers/locs
  11 -> 12px; hero locs 12 -> 13px.
- Numbers-strip captions 11 -> 12px. Index 13px regular -> 13px BOLD
  (14px bold overflowed 4 items past the 306px columns).
- Top-bar right text 12 -> 13px; italic subhead 17 -> 18px.
- Three headlines shortened to fit the bigger type, meaning unchanged
  (v7.2.1 precedent): tile 8 "China tells Japan: 'correct' Taiwan words"
  -> "China warns Japan on Taiwan"; tile 9 body "(Airline, AP)" -> "(AP)";
  tile 12 body "(Formula 1)" -> "(F1)".
- NOT touched (measured: would clip/truncate): SOURCES 11px (12px is
  976px wide, page fits 968), DATE CHECK 11px (12px wraps to 3 lines,
  code draws 2), colophon 11px, region bar 11px (12px "GLOBAL 1" is 66px,
  its segment 62px), map pins r=9 (r=10 would nearly overlap pins 1-2,
  3-11).
- Structure kept: 35 stories, masthead, 3 heroes + 10 tiles + 22-item
  index, DATE CHECK, no text below 11px anywhere. All wraps measured:
  every head/body 2 lines, index max 300.5px of 306px.
Deterministic. DO NOT SUBMIT before user ACC.
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
    f = F(SANS_B, 11)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw - 12, y, x, y + 15], radius=7, fill=color)
    d.text((x - tw / 2 - 6, y + 2), text, font=f, fill=(255, 255, 255), anchor="mt")


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
    # missile trails (v7.6): diagonal streaks down toward the skyline,
    # below the kicker/badge row, above the stat chip
    for (tx0, ty0, tx1, ty1) in [(x + 112, y + 40, x + 152, y + 88),
                                  (x + 192, y + 38, x + 230, y + 86),
                                  (x + 266, y + 42, x + 298, y + 84)]:
        d.line([tx0, ty0, tx1, ty1], fill=(255, 214, 120), width=3)
        d.line([tx0, ty0, tx1, ty1], fill=(255, 255, 255), width=1)
        d.ellipse([tx1 - 3, ty1 - 3, tx1 + 3, ty1 + 3], fill=(255, 200, 90))


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
    # second seismograph channel (v7.6), 12px above the red trace
    d.line([(px, py - 12) for (px, py) in pts], fill=(140, 136, 128), width=2)
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
        # 146/146 safe: green bar, text clear of the badge zone (v7.6 fix)
        d.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
        d.rectangle([x + 8, y + 7, x + w - 78, y + h - 7], fill=(220, 225, 230))
        d.rectangle([x + 8, y + 7, x + w - 78, y + h - 7], fill=(46, 125, 50))
        d.text(((x + 8 + x + w - 78) / 2, y + 9), "146 SAFE", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mt")
    elif key == "canberra":
        # 11-day trip: 11 day-segments, clear of the badge zone (v7.6 fix)
        d.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
        for i in range(11):
            sx = x + 8 + i * 10
            d.rounded_rectangle([sx, y + 8, sx + 9, y + h - 8], radius=3,
                                fill=(200, 50, 40) if i == 10 else (29, 53, 87))
    elif key == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(16, 20, 36))
        d.ellipse([x + 14, y + 5, x + 44, y + h - 5], fill=(247, 147, 26))
        d.text((x + 29, y + 6), "B", font=F(SANS_B, 20), fill=(255, 255, 255), anchor="mt")
        d.line([(x + 60, y + 10), (x + 95, y + 14), (x + 120, y + 8), (x + 150, y + 20),
                (x + 175, y + 28)], fill=(220, 60, 50), width=3)
        d.polygon([(x + 168, y + 28), (x + 178, y + 24), (x + 178, y + 32)], fill=(220, 60, 50))
    elif key == "f1":
        # P1 lap: red bar with the real lap time, clear of the badge zone (v7.6 fix)
        d.rectangle([x, y, x + w, y + h], fill=(14, 16, 34))
        d.rectangle([x + 8, y + 7, x + w - 78, y + h - 7], outline=(255, 220, 60), width=2)
        d.rectangle([x + 10, y + 9, x + w - 80, y + h - 9], fill=(220, 60, 50))
        d.text(((x + 8 + x + w - 78) / 2, y + 9), "1:34.041", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mt")
    elif key == "rahul":
        # IND 344 vs NZ 368 bars, values inside the bars, clear of the badge (v7.6 fix)
        d.rectangle([x, y, x + w, y + h], fill=(245, 247, 240))
        bw = 100
        b1 = bw * 344 / 368
        d.rectangle([x + 8, y + 3, x + 8 + b1, y + 14], fill=(46, 125, 50))
        d.text((x + 8 + b1 - 4, y + 8), "344", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="rm")
        d.rectangle([x + 8, y + 16, x + 8 + bw, y + 27], fill=(90, 90, 95))
        d.text((x + 8 + bw - 4, y + 21), "368", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="rm")


# ------------------------------------------------- story data (35, Saturday 21 Nov 2026)
HEROES = [
    dict(num=1, kicker="SAUDI: MISSILES", stat="3 shot down",
         loc="1 RIYADH, SAUDI ARABIA \u00b7 WAR",
         head="Three Houthi missiles shot down over Riyadh",
         body="Three destroyed over Riyadh before dawn and two over Jizan. (AFP, Dawn)",
         badge="OFFICIAL", badge_color=GREEN, art=art_riyadh),
    dict(num=2, kicker="COP31: OVERTIME", stat="No deal \u00b7 day 13",
         loc="2 ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         head="Climate summit drags into Saturday",
         body="A draft with no fossil fuels split nearly 200 countries. (AFP, Al Jazeera)",
         badge="CONFIRMED", badge_color=TEAL, art=art_cop31),
    dict(num=3, kicker="PERU: QUAKE 6.7", stat="00:09 UTC \u00b7 108 km deep",
         loc="3 JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
         head="Magnitude 6.7 quake shakes Peru",
         body="The deep quake near Carhuamayo was felt in Lima and along the coast. (USGS, IGP)",
         badge="OFFICIAL", badge_color=GREEN, art=art_peru),
]

TILES = [
    dict(num=4, kicker="KYIV: WARNING", loc="4 KYIV", art="kyiv",
         head="Zelensky: bridge \u2018won\u2019t stay\u2019",
         body="He warns of double-tap strikes. (NBC)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=5, kicker="HORMUZ: DRONE", loc="5 HORMUZ", art="hormuz",
         head="Iran says it shot down a US drone",
         body="No confirmation from Washington. (IRIB)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=6, kicker="IRAN: URANIUM", loc="6 TEHRAN", art="iran",
         head="Uranium stays in the country",
         body="Minister still seeks a \u2018fair solution\u2019. (ToI)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=7, kicker="TRUMP: AI TAX", loc="7 WASHINGTON", art="trump",
         head="Trump vows AI data-centre tax",
         body="\u2018Tremendous\u2019 penalty; no details yet. (ABC)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=8, kicker="CHINA\u2013JAPAN", loc="8 BEIJING", art="chinajapan",
         head="China warns Japan on Taiwan",
         body="Tokyo says its stance is unchanged. (Ministry, AFP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=9, kicker="DAVAO: 146 SAFE", loc="9 DAVAO", art="davao",
         head="Jet lands after engine-fire alert",
         body="Air Niugini 767 diverts after midnight. (AP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=10, kicker="CANBERRA: AI", loc="10 CANBERRA", art="canberra",
         head="Australia, China agree AI talks",
         body="Albanese ends an 11-day trip. (ABC)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=11, kicker="BITCOIN: $58,983", loc="11 MARKETS", art="bitcoin",
         head="Bitcoin slips below $59,000",
         body="Down 3.9% in 24 hours; ether $1,625. (CoinGecko)",
         badge="CONFIRMED", badge_color=TEAL),
    dict(num=12, kicker="RUSSELL: P1", loc="12 LAS VEGAS", art="f1",
         head="Russell fastest in Las Vegas",
         body="1:34.041 in a damp, messy session. (F1)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=13, kicker="RAHUL: 124*", loc="13 WELLINGTON", art="rahul",
         head="Rahul century vs New Zealand",
         body="India 344 for 2 at tea, replying to 368. (AFP)",
         badge="OFFICIAL", badge_color=GREEN),
]

INDEX = [
    (14, "Kryvyi Rih strike kills 2"),
    (15, "Copenhagen expels Russian attacker"),
    (16, "Antalya: EU warns \u2018fossil\u2019 summit"),
    (17, "Antalya: Panama may block text"),
    (18, "Antalya: Indonesia clean-power deals"),
    (19, "Yemen: Houthis threaten Jeddah"),
    (20, "Washington: Vance on Iran strikes"),
    (21, "Washington: SpaceX funding threat"),
    (22, "Texas: 63-minute execution"),
    (23, "Los Angeles: arsonist convicted"),
    (24, "Missouri: $7.25bn Roundup payout"),
    (25, "Vancouver: youth climate trial"),
    (26, "Pyongyang: Kim tours factories"),
    (27, "Sejong: train derails, none hurt"),
    (28, "Taipei: budget, cash payout pass"),
    (29, "Bangkok: arsenic plan"),
    (30, "New Delhi: SCO forum opens"),
    (31, "Eastern India: Akvan rain alerts"),
    (32, "Myanmar: sanctions call"),
    (33, "Port Louis: rating agency talks"),
    (34, "Melbourne: Cummins keeps captaincy"),
    (35, "Las Vegas: Verstappen to stewards"),
]

# index sources, gathered into one footer line (per-item sources removed)
SOURCES = ("AFP \u00b7 REUTERS \u00b7 AP \u00b7 AL JAZEERA \u00b7 KYIV INDEPENDENT \u00b7 ANTARA \u00b7 "
           "CNN \u00b7 ABC \u00b7 DAWN \u00b7 KOREA HERALD \u00b7 TAIPEI TIMES \u00b7 THE NATION \u00b7 "
           "ETV \u00b7 AUTOSPORT")

NUMBERS = [
    ("3", "MISSILES SHOT DOWN", "OVER RIYADH"),
    ("13", "DAY OF COP31", "MEANT TO CLOSE DAY 12"),
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

# map pins 1-13 (pixel positions on the 340x123 map; 1-2 and 3-11 nudged
# apart so the enlarged r=9 pins do not overlap)
PINS = [
    (1, 246, 795), (2, 228, 785), (3, 125, 828), (4, 220, 764),
    (5, 268, 789), (6, 252, 769), (7, 120, 793), (8, 308, 778),
    (9, 317, 809), (10, 336, 845), (11, 134, 809), (12, 89, 782),
    (13, 358, 857),
]


def index_item(d, x, y, num, text, max_w):
    """One numbered index line at 13px bold; every item measured to fit one line."""
    f = F(SANS_B, 13)
    fb = F(SANS_B, 13)
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
           font=F(SANS_B, 13), fill=(255, 255, 255), anchor="rt")

    # giant date masthead (auto-fit, max 88px)
    mast = "Saturday 21 November 2026"
    msize = 88
    while msize > 60:
        mf = ImageFont.truetype(MASTHEAD, msize)
        if d.textlength(mast, font=mf) <= 960:
            break
        msize -= 2
    # yellow highlight behind "21" (v7.6, r01/r02/r49 pattern)
    _tw = d.textlength(mast, font=mf)
    _x0 = 512 - _tw / 2
    _pre = d.textlength("Saturday ", font=mf)
    _w21 = d.textlength("21", font=mf)
    d.rectangle([_x0 + _pre - 4, 32, _x0 + _pre + _w21 + 4, 34 + int(msize * 0.75)],
                fill=(255, 214, 0))
    d.text((512, 34), mast, font=mf, fill=INK, anchor="mt")
    d.text((512, 120), "Missiles over Riyadh \u00b7 COP31 talks run into overtime \u00b7 a quake shakes Peru",
           font=F(SERIF_I, 18), fill=INK, anchor="mt")

    # numbers strip: 6 verified Saturday figures
    ny = 146
    d.line([28, ny - 6, W - 28, ny - 6], fill=INK, width=1)
    colw = (W - 56) // 6
    for i, (num, l1, l2) in enumerate(NUMBERS):
        cx = 28 + i * colw + colw // 2
        d.text((cx, ny), num, font=F(MASTHEAD_NUM, 30), fill=RED, anchor="mt")
        d.text((cx, ny + 32), l1, font=F(SANS_B, 12), fill=INK, anchor="mt")
        d.text((cx, ny + 45), l2, font=F(SANS_B, 12), fill=INK, anchor="mt")
        if i:
            d.line([28 + i * colw, ny, 28 + i * colw, ny + 56], fill=GREY, width=1)
    d.line([28, ny + 60, W - 28, ny + 60], fill=INK, width=1)

    # region counts bar (widths proportional to counts, total 35;
    # narrow segments get a 62px minimum so their 11px labels fit)
    ry = 210
    total = sum(c for _, c, _ in REGIONS)
    assert total == 35, total
    minw = 62
    flex = (W - 56) - minw * len(REGIONS)
    flex_total = sum(max(c - 1, 0) for _, c, _ in REGIONS)
    rx = 28
    for name, count, color in REGIONS:
        segw = minw + flex * max(count - 1, 0) / flex_total
        d.rectangle([rx, ry, rx + segw, ry + 15], fill=color)
        d.text((rx + segw / 2, ry + 2), f"{name} {count}", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mt")
        rx += segw

    # 3 big heroes
    hy, hh = 229, 240
    hw = (W - 56 - 2 * 10) // 3
    for i, hro in enumerate(HEROES):
        x = 28 + i * (hw + 10)
        y = hy
        d.rectangle([x, y, x + hw, y + hh], outline=INK, width=1)
        hro["art"](d, x + 1, y + 1, hw - 2, 130)
        kicker_label(d, x + 8, y + 8, hro["kicker"], 17)
        stat_chip(d, x + 8, y + 130 - 26, hro["stat"])
        badge(d, x + hw - 8, y + 8, hro["badge"], hro["badge_color"])
        d.text((x + 8, y + 138), hro["loc"], font=F(SANS_B, 13), fill=RED)
        block(d, x + 8, y + 152, hro["head"], F(SERIF_B, 23), hw - 16, 25, max_lines=2)
        block(d, x + 8, y + 204, hro["body"], F(SANS, 13), hw - 16, 16, max_lines=2)

    # 10 tiles (4-13), 2 rows x 5
    tw = (W - 56 - 4 * 8) // 5
    th = 136
    for i, t in enumerate(TILES):
        r, c = divmod(i, 5)
        x = 28 + c * (tw + 8)
        y = 474 + r * (th + 5)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        d.rectangle([x, y, x + tw, y + 18], fill=RED)
        d.text((x + 6, y + 3), t["kicker"], font=F(SANS_B, 12), fill=(255, 255, 255))
        tile_art(d, t["art"], x + 1, y + 19, tw - 2, 30)
        badge(d, x + tw - 6, y + 21, t["badge"], t["badge_color"])
        d.text((x + 6, y + 50), t["loc"], font=F(SANS_B, 12), fill=RED)
        block(d, x + 6, y + 64, t["head"], F(SANS_B, 18), tw - 12, 20, max_lines=2)
        block(d, x + 6, y + 104, t["body"], F(SANS, 13), tw - 12, 15, max_lines=2)

    # map + numbered index (13px, no micro-text left on the page)
    my = 755
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    d.text((W - 28, my), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=F(SANS_B, 13), fill=RED, anchor="rt")
    map_img = Image.open(MAP_PATH).resize((340, 123), Image.LANCZOS)
    img.paste(map_img, (28, 771))
    d.rectangle([28, 771, 368, 894], outline=INK, width=1)
    for num, px, py in PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=F(SANS_B, 11), fill=(255, 255, 255),
               anchor="mm")
    # HOW SURE legend (v7.6, r10 pattern) in the free slot under the map
    d.text((28, 902), "HOW SURE ARE WE?", font=F(SANS_B, 11), fill=RED)
    _lx = 28
    for _label, _color in [("CONFIRMED", TEAL), ("OFFICIAL", GREEN), ("REPORTED", AMBER)]:
        d.rectangle([_lx, 917, _lx + 10, 927], fill=_color)
        d.text((_lx + 14, 915), _label, font=F(SANS_B, 11), fill=INK)
        _lx += 14 + d.textlength(_label, font=F(SANS_B, 11)) + 18
    d.text((28, 930), "Badges show how each story was sourced.",
           font=F(SANS, 11), fill=GREY)
    colw2 = (W - 28 - 376 - 8) // 2
    for i, (num, text) in enumerate(INDEX):
        col, row = divmod(i, 11)
        x = 376 + col * (colw2 + 8)
        y = 771 + row * 16
        index_item(d, x, y, num, text, colw2)

    # one SOURCES line for the index stories (per-item sources removed)
    _sw = d.textlength("SOURCES: ", font=F(SANS_B, 11))
    _tw = _sw + d.textlength(SOURCES, font=F(SANS, 11))
    _sx = 512 - _tw / 2
    d.text((_sx, 948), "SOURCES: ", font=F(SANS_B, 11), fill=INK)
    d.text((_sx + _sw, 948), SOURCES, font=F(SANS, 11), fill=INK)

    # DATE CHECK footer (wrapped: label inline on line 1, body on lines 1-2)
    dy = 964
    d.rectangle([28, dy, W - 28, dy + 32], outline=RED, width=2)
    lab = "DATE CHECK \u2014 "
    lab_w = d.textlength(lab, font=F(SANS_B, 11))
    d.text((34, dy + 3), lab, font=F(SANS_B, 11), fill=RED)
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
    d.text((34 + lab_w, dy + 3), lines[0], font=F(SANS, 11), fill=INK)
    if len(lines) > 1:
        d.text((34, dy + 16), lines[1], font=F(SANS, 11), fill=INK)

    # colophon
    d.text((512, 1000),
           "Every story here happened, or was first reported, on Saturday 21 November 2026. Index sources above \u00b7 original drawings",
           font=F(SANS, 11), fill=GREY, anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121-entry/entry.png", optimize=True)
    print("saved", img.size, "masthead size:", msize)


if __name__ == "__main__":
    render()
