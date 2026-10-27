"""Google Play graphics: 512 px app icon and the 1024x500 feature graphic (one per listing language).

usage: python tools/make_store_graphics.py store
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from make_icons import art, TEAL  # noqa: E402  (shares the icon drawing)

out = sys.argv[1]
FONTS = "C:/Windows/Fonts/"
TAGLINES = {
    "pl": ("Tankowania, spalanie, serwisy", "i koszty auta w jednym miejscu"),
    "en": ("Fill-ups, fuel economy, service", "and car costs in one place"),
}

art("full", 0.72).convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{out}/icon-512.png")

for lang, (line1, line2) in TAGLINES.items():
    W, H = 1024, 500
    img = Image.new("RGB", (W, H))
    top, bottom = (17, 128, 119), (8, 64, 60)
    for y in range(H):  # vertical gradient
        t = y / H
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    logo = art("rounded", 0.9, (255, 255, 255), TEAL)  # white tile, teal drop
    logo = logo.resize((260, 260), Image.LANCZOS)
    img.paste(logo, (90, (H - 260) // 2), logo)
    d = ImageDraw.Draw(img)
    d.text((400, 150), "Refuelling", font=ImageFont.truetype(FONTS + "segoeuib.ttf", 84), fill="white")
    small = ImageFont.truetype(FONTS + "segoeui.ttf", 36)
    d.text((404, 270), line1, font=small, fill=(213, 240, 236))
    d.text((404, 318), line2, font=small, fill=(213, 240, 236))
    img.save(f"{out}/feature-graphic-{lang}.png")
print("ok")
