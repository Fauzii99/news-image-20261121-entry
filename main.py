#!/usr/bin/env python3
"""news-image-20261121 entry: copy the bundled front page to /output/entry.png.

The image is drawn by render.py (same directory) with PIL: a 1024x1024
newspaper front page, "THE WORLD IN ONE PAGE", Saturday 21 November 2026,
35 verified stories across 7 regions, a day-in-numbers strip, two hero
stories (Russia's 400-drone / 110-missile barrage and two missiles landing
in Poland; three Houthi missiles downed over Riyadh), a 9-tile grid, and a
world map with a numbered index of all 35 stories.

Standard library only. No network. Deterministic: the same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
