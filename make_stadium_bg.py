#!/usr/bin/env python3
"""Generate a painterly stadium-interior background (1920x1080) as a PNG.
Used as the default backdrop when no real venue photo is supplied."""
from PIL import Image, ImageDraw, ImageFilter
import math, random

W, H = 1920, 1080
random.seed(26)

img = Image.new("RGB", (W, H), (8, 11, 17))
d = ImageDraw.Draw(img, "RGBA")

# --- night sky / upper bowl gradient ---
for y in range(H):
    t = y / H
    r = int(10 + 8 * (1 - t))
    g = int(14 + 12 * (1 - t))
    b = int(22 + 20 * (1 - t))
    d.line([(0, y), (W, y)], fill=(r, g, b))

cx, cy = W / 2, H * 1.15  # bowl center far below: we see the far stands

# --- pitch: bright green ellipse at the bottom, perspective ---
pitch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(pitch)
pd.ellipse([W*0.10, H*0.66, W*0.90, H*1.35], fill=(34, 102, 53, 255))
# mowing stripes
stripe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stripe)
for i in range(-2, 14):
    x0 = W*0.10 + i * (W*0.80/12)
    sd.polygon([(x0, H*0.66), (x0 + W*0.80/24, H*0.66),
                (x0 + W*0.80/24*1.6, H*1.3), (x0 - W*0.80/24*0.6, H*1.3)],
               fill=(255, 255, 255, 16 if i % 2 == 0 else 0))
pitch = Image.alpha_composite(pitch, stripe)
img.paste(Image.alpha_composite(img.convert("RGBA"), pitch).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# --- far stands: concentric arcs of "seats" (tiny dots) ---
for ring in range(18):
    ry = 120 + ring * 26
    rx = 760 + ring * 70
    seats = 220 + ring * 16
    base_b = 60 - ring * 2
    for s in range(seats):
        ang = math.pi * (0.04 + 0.92 * s / seats)  # upper arc only
        x = cx + rx * math.cos(ang)
        y = (cy - H * 0.92) + ry * math.sin(ang) * 0.5
        if 0 <= x < W and 0 <= y < H * 0.7:
            jitter = random.randint(-12, 12)
            col = (max(40 + jitter, 0), max(48 + jitter, 0), max(base_b + jitter, 0), 200)
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=col)

# --- floodlight glow patches at top ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for gx in (W*0.20, W*0.50, W*0.80):
    gd.ellipse([gx-260, -180, gx+260, 260], fill=(150, 180, 230, 40))
glow = glow.filter(ImageFilter.GaussianBlur(80))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

# --- atmospheric haze + vignette ---
img = img.filter(ImageFilter.GaussianBlur(1.2))
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-W*0.3, -H*0.3, W*1.3, H*1.3], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(200))
dark = Image.new("RGB", (W, H), (4, 6, 10))
img = Image.composite(img, dark, vig)

_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stadium_bg.png")
img.save(_out, "PNG")
print("stadium_bg.png written")
