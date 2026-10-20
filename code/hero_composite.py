"""Composite the headline figure onto the hero illustration.
Figure text is the verified share of active STR licenses that are their
holder's only license, from stats.json - typed once here and checked
against stats.json by assertion before compositing.
"""
import json
from PIL import Image, ImageDraw, ImageFont

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
SRC = f"{PKG}/hero_source/media-generation-hero-illustration-0-0fc55aec-c0cc-4b74-b791-28183f733d5f.webp"
S = json.load(open(f"{PKG}/stats.json"))
share = S["concentration_active"]["share_whose_holder_has_exactly_1_pct"]
only = S["concentration_active"]["licenses_whose_holder_has_exactly_1"]
total = S["concentration_active"]["licenses"]
holders = S["concentration_active"]["distinct_holders"]
assert share == 99.71 and only == 2077 and total == 2083 and holders == 2080, (share, only, total, holders)

img = Image.open(SRC).convert("RGB")
W, H = img.size
# soft dark gradient scrim across the top for text legibility
scrim = Image.new("L", (1, H))
for y in range(H):
    scrim.putpixel((0, y), int(220 * max(0.0, 1 - y / (H * 0.55))))
scrim = scrim.resize((W, H))
black = Image.new("RGB", (W, H), (5, 6, 7))
img = Image.composite(black, img, scrim.point(lambda v: v // 2))

d = ImageDraw.Draw(img)
FD = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17/.venv/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"
f_kick = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 44)
f_big = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 168)
f_sub = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 47)
AMBER, FG, MUT = (245, 168, 0), (232, 230, 225), (190, 196, 201)

x = 96
d.text((x, 84), "DENVER SHORT-TERM RENTAL LICENSES, 2026", font=f_kick, fill=AMBER)
d.text((x, 150), "99.7%", font=f_big, fill=FG)
d.text((x, 368), "of active STR licenses are their holder's only license:", font=f_sub, fill=MUT)
d.text((x, 428), f"{only:,} of {total:,} licenses, held by {holders:,} licensees", font=f_sub, fill=MUT)
img.save(f"{PKG}/hero.png")
print("hero.png written", img.size)
