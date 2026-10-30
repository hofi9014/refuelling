"""Google Play graphics: 512 px app icon and the 1024x500 feature graphic (one per listing language).

usage: python tools/make_store_graphics.py store
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from make_icons import art, AMBER, GRAPHITE, PAPER  # noqa: E402  (shares the logo drawing)

out = sys.argv[1]
NAME = "TANKVIA"
FONTS = "C:/Windows/Fonts/"
TAGLINES = {
    "pl": ("Tankowania, spalanie, serwisy", "i koszty auta w jednym miejscu"),
    "en": ("Fill-ups, fuel economy, service", "and car costs in one place"),
}

art("full", 0.72).convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{out}/icon-512.png")

for lang, (line1, line2) in TAGLINES.items():
    W, H = 1024, 500
    img = Image.new("RGB", (W, H), GRAPHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 10, W, H], fill=AMBER)  # the amber edge of the app's header
    for x in range(404, W - 60, 46):  # road marking
        d.rectangle([x, 372, x + 26, 377], fill=(70, 74, 79))
    logo = art(None, 0.95).resize((300, 300), Image.LANCZOS)
    img.paste(logo, (70, (H - 300) // 2 - 6), logo)
    d.text((400, 120), NAME, font=ImageFont.truetype(FONTS + "segoeuib.ttf", 72), fill=PAPER)
    small = ImageFont.truetype(FONTS + "segoeui.ttf", 34)
    d.text((404, 240), line1, font=small, fill=(200, 196, 188))
    d.text((404, 286), line2, font=small, fill=(200, 196, 188))
    img.save(f"{out}/feature-graphic-{lang}.png")
print("ok")
