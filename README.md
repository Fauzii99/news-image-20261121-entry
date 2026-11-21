# Saturday 21 November 2026: the world in one page

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Fauzii99/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Fauzii99/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up Saturday 21 November 2026 in one image:
**35 verified stories across 7 regions** — the giant date masthead names the
day; three big illustrated heroes (COP31 overtime in Antalya, three Houthi
missiles downed over Riyadh, the M6.7 Peru quake) lead ten more illustrated
tiles and a 22-item numbered index, with a six-figure numbers strip, a
region-counts bar, a numbered world map, and a DATE CHECK box that names the
Friday 20 November news deliberately left out. Every main story carries its
source and a verification badge (OFFICIAL / CONFIRMED / REPORTED).

## How it is built

`render.py` draws the 1024×1024 page with Pillow (fixed fonts, no
randomness, no network). `main.py` copies the bundled `entry.png` to
`/output/entry.png`, so both runs write byte-identical output.

## Verify locally

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
```

## Competition

[news-image-20261121 on make.fun](https://make.fun/bounty/news-image-20261121) —
deadline Monday 23 November 2026 00:00 UTC (07:00 WIB). $100 pot, top 50 paid.
