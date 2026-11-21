#!/usr/bin/env python3
"""Render the 21 Nov 2026 front page: 1024x1024, 35 stories, 7 regions.
Deterministic: no randomness, no network, fixed fonts.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
DARK = (24, 32, 54)
BLUE = (38, 84, 124)
GREY = (90, 90, 88)
LIGHT = (232, 226, 208)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, max_w, leading, color=INK, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


def kicker(draw, x, y, label, w):
    f = F(SANS_B, 13)
    tw = draw.textlength(label, font=f)
    bw = tw + 16
    draw.rectangle([x, y, x + bw, y + 20], fill=RED)
    draw.text((x + 8, y + 3), label, font=f, fill=(255, 255, 255))
    return y + 20


# ---------------------------------------------------------------- stories
HEROES = [
    ("UKRAINE  •  POLAND",
     "400 drones, 110 missiles \u2014 two land in Poland",
     "Russia\u2019s biggest overnight barrage hits Kyiv and three Dnipro bridges; Warsaw calls the Polish landings a deliberate provocation.",
     "kyiv"),
    ("RIYADH  •  YEMEN",
     "Three Houthi missiles downed over Riyadh",
     "Saudi-led coalition intercepts all three on a third straight night of alerts; Houthis warn airlines after strikes on Hodeidah.",
     "riyadh"),
]

TILES = [
    ("COP31 OVERTIME", "Climate talks run past deadline in Antalya",
     "Nearly 200 nations deadlocked on fossil fuels; the draft drops the wording."),
    ("PERU QUAKE", "6.8 quake shakes the Andes",
     "Tremors felt in Lima; no deaths reported at once."),
    ("ROHINGYA RULING", "UN court: Myanmar guilty of genocide",
     "Historic ICJ ruling for the Rohingya people."),
    ("GAZA AID", "Three killed in strike on aid vehicle",
     "Renewed attacks hit humanitarian supplies."),
    ("HORMUZ TANKER", "Tanker hit near Strait of Hormuz",
     "UK maritime agency reports two incidents off Oman."),
    ("MARKETS ROUT", "AI sell-off: S&P falls 3.7%",
     "Dow enters correction; Anthropic slides a second day."),
    ("UK\u2013EU DEAL", "Biggest UK\u2013EU pact since Brexit",
     "Food, carbon and youth mobility deals signed."),
    ("CYBERATTACKS", "FBI and US farm agency hacked",
     "US computer outages and hacks continue."),
    ("BAYER PAYOUT", "Bayer pays $7.25bn over Roundup",
     "Settlement ends long-running weedkiller claims."),
]

INDEX = [
    "LA quake 4.2, no injuries",
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
    "Russian strikes kill 12 in a day",
    "Hodeidah port struck by coalition",
    "Trump presser after China trip",
    "Anthropic shares close $88.91",
]

NUMBERS = [
    ("400+", "DRONES AT UKRAINE"),
    ("110", "MISSILES FIRED"),
    ("2", "LAND IN POLAND"),
    ("3", "MISSILES DOWNED"),
    ("6.8", "PERU QUAKE"),
    ("3.7%", "S&P FALLS"),
]

# rough continent blobs (x, y, w, h) on a 430x250 map
CONTINENTS = [
    [(18, 38), (60, 22), (105, 28), (120, 55), (95, 78), (60, 82), (30, 70)],   # N America
    [(95, 120), (130, 115), (150, 140), (135, 185), (110, 175), (95, 145)],    # S America
    [(215, 30), (250, 22), (265, 45), (245, 60), (220, 52)],                    # Europe
    [(215, 75), (260, 70), (275, 110), (255, 160), (225, 140), (210, 100)],    # Africa
    [(270, 25), (340, 18), (400, 35), (410, 75), (360, 95), (310, 80), (280, 55)],  # Asia
    [(360, 160), (395, 155), (405, 180), (375, 190), (355, 175)],              # Australia
]
# (map x, y) per index item 12..35 -- spread, small dots
DOTS = [(30, 150), (298, 66), (222, 58), (238, 44), (292, 54), (232, 36),
        (272, 34), (268, 24), (375, 75), (120, 50), (385, 55), (302, 72),
        (258, 46), (360, 60), (395, 140), (288, 78), (372, 80), (244, 32),
        (110, 55), (258, 56), (266, 42), (282, 84), (115, 48), (125, 58)]


def draw_skyline(draw, x, y, w, h, kind):
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    # buildings
    bx = x + 8
    heights = [0.45, 0.7, 0.55, 0.85, 0.6, 0.75, 0.5] if kind == "kyiv" else [0.6, 0.8, 0.5, 0.9, 0.65, 0.55, 0.75]
    for i, f in enumerate(heights):
        bw = (w - 16) / len(heights)
        bh = h * f
        draw.rectangle([bx, y + h - bh, bx + bw - 3, y + h], fill=(52, 62, 92))
        # lit windows
        for wy in range(int(y + h - bh + 6), int(y + h - 4), 12):
            for wx in range(int(bx + 3), int(bx + bw - 6), 9):
                if (wx + wy) % 23 < 9:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        bx += bw
    # missile arcs + bursts
    for i, (sx, sy, ex, ey) in enumerate([(x + 30, y + 12, x + 130, y + 55),
                                          (x + 200, y + 8, x + 300, y + 60),
                                          (x + 350, y + 15, x + 430, y + 50)]):
        draw.arc([sx, sy, ex, ey + 40], start=200, end=340, fill=(255, 200, 80), width=2)
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 170, 40))
        for a in range(8):
            import math
            ang = a * math.pi / 4
            draw.line([ex, ey, ex + 12 * math.cos(ang), ey + 12 * math.sin(ang)],
                      fill=(255, 200, 80), width=2)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=RED, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=1)

    # masthead
    d.text((512, 26), "THE WORLD IN ONE PAGE", font=F(SERIF, 46), fill=INK, anchor="mt")
    d.text((512, 76), "SATURDAY  21  NOVEMBER  2026", font=F(SANS_B, 20),
           fill=RED, anchor="mt")
    d.line([28, 104, W - 28, 104], fill=INK, width=2)
    d.text((512, 110), "35 STORIES  \u2022  7 REGIONS  \u2022  ONE DAY",
           font=F(SANS_B, 14), fill=GREY, anchor="mt")

    # numbers strip
    y0 = 138
    cw = (W - 56 - 5 * 8) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = 28 + i * (cw + 8)
        d.rectangle([x, y0, x + cw, y0 + 52], outline=INK, width=1)
        d.text((x + cw / 2, y0 + 4), num, font=F(SANS_B, 22), fill=RED, anchor="mt")
        d.text((x + cw / 2, y0 + 30), lab, font=F(SANS_B, 10), fill=INK, anchor="mt")
    d.line([28, y0 + 62, W - 28, y0 + 62], fill=INK, width=2)

    # heroes
    hy = 210
    hw = (W - 56 - 12) / 2
    hh = 190
    for i, (kick, head, cap, kind) in enumerate(HEROES):
        x = 28 + i * (hw + 12)
        d.rectangle([x, hy, x + hw, hy + hh], outline=INK, width=1)
        draw_skyline(d, x + 1, hy + 1, hw - 2, 62, kind)
        kicker(d, x + 8, hy + 70, kick, hw)
        text_block(d, x + 8, hy + 96, head, F(SERIF, 21), hw - 16, 24, max_lines=2)
        text_block(d, x + 8, hy + 146, cap, F(SANS, 12), hw - 16, 15, color=(60, 60, 60),
                   max_lines=3)

    # tiles 3x3
    ty = 414
    tw = (W - 56 - 2 * 10) / 3
    th = 88
    for i, (kick, head, cap) in enumerate(TILES):
        r, c = divmod(i, 3)
        x = 28 + c * (tw + 10)
        y = ty + r * (th + 8)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        kicker(d, x + 6, y + 6, kick, tw)
        text_block(d, x + 6, y + 30, head, F(SERIF, 14.5), tw - 12, 17, max_lines=2)
        text_block(d, x + 6, y + 65, cap, F(SANS, 10.5), tw - 12, 12, color=(60, 60, 60),
                   max_lines=2)

    # map + index
    my = 710
    mh = 252
    d.line([28, my - 6, W - 28, my - 6], fill=INK, width=2)
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 15), fill=INK)
    d.text((W - 28, my), "THE DAY IN 35 STORIES", font=F(SANS_B, 15), fill=INK, anchor="rt")
    map_x, map_y, map_w, map_h = 28, my + 26, 420, 190
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(214, 228, 238),
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + int(py * 0.76)) for px, py in poly]
        d.polygon(pts, fill=(236, 214, 170), outline=BLUE)
    for n, (dx, dy) in enumerate(DOTS):
        cx, cy = map_x + dx, map_y + int(dy * 0.76)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(12 + n), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
    # index, two columns
    ix = 470
    iy = my + 26
    col_w = (W - 28 - ix - 10) / 2
    f_idx = F(SANS, 12)
    f_num = F(SANS_B, 12)
    for n, item in enumerate(INDEX):
        col = 0 if n < 12 else 1
        row = n if n < 12 else n - 12
        x = ix + col * (col_w + 10)
        y = iy + row * 17
        d.text((x, y), f"{12 + n}.", font=f_num, fill=RED)
        d.text((x + 26, y), item, font=f_idx, fill=INK)
    d.text((28, my + 220), "1\u201311 above.",
           font=F(SANS, 11), fill=GREY)

    # footer
    fy = 956
    d.rectangle([28, fy, W - 28, fy + 30], fill=RED)
    d.text((512, fy + 7), "SATURDAY 21 NOVEMBER 2026  \u2022  THE WORLD IN ONE PAGE",
           font=F(SANS_B, 14), fill=(255, 255, 255), anchor="mt")
    d.text((512, fy + 36), "SOURCES: REUTERS \u2022 AP \u2022 BBC \u2022 UN \u2022 UKMTO \u2022 GFZ",
           font=F(SANS, 10), fill=GREY, anchor="mt")

    img.save("/home/hatch/workspace/makefun/news-image-20261121/entry.png",
             optimize=True)
    print("saved", img.size)


if __name__ == "__main__":
    render()
