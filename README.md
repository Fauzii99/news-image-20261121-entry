# Saturday 21 November 2026: the world in one page

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Fauzii99/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Fauzii99/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up Saturday 21 November 2026 in one image:
**27 verified stories across 7 regions** — Russia's 400-drone, 110-missile
barrage on Ukraine with two missiles landing in Poland; three Houthi
missiles intercepted over Riyadh; COP31 running into overtime in Antalya;
a 6.8 quake in Peru; the UN court finding Myanmar guilty of genocide
against the Rohingya; a tanker hit near Hormuz; the AI stock rout; and the
biggest UK–EU pact since Brexit — plus a day-in-numbers strip and a world
map with a numbered index of all 8 hotspots.

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
