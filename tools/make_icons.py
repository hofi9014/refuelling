"""Draws the app icon (fuel drop with a lightning bolt).

usage: python tools/make_icons.py docs/icons [assets]
The optional second folder gets the 1024 px sources for `npm run icons` (@capacitor/assets -> Android icons and splash).
"""
import sys
from PIL import Image, ImageDraw

S = 1024  # draw large, downscale for smooth edges
TEAL = (15, 118, 110)
DARK = (13, 20, 25)


def art(bg="rounded", k=0.9, bg_color=TEAL):
    """bg: "rounded" tile, "full" square, or None (transparent, bolt cut out)."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg == "full":
        d.rectangle([0, 0, S, S], fill=bg_color)
    elif bg == "rounded":
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=bg_color)
    c = S / 2

    def P(x, y):  # coordinates in a 0..1000 design grid, scaled around the centre
        return (c + (x - 500) * k * S / 1000, c + (y - 500) * k * S / 1000)

    # fuel drop
    d.ellipse([*P(270, 400), *P(730, 860)], fill="white")
    d.polygon([P(500, 130), P(296, 524), P(704, 524)], fill="white")  # sides tangent to the circle
    # lightning bolt cut out of the drop (ImageDraw writes pixels directly, so a transparent fill really cuts)
    d.polygon([P(540, 420), P(420, 660), P(505, 660), P(465, 800), P(590, 570), P(505, 570)],
              fill=bg_color if bg else (0, 0, 0, 0))
    return im


def splash(color):
    im = Image.new("RGBA", (2732, 2732), color)
    logo = art(None, 0.9).resize((640, 640), Image.LANCZOS)  # white drop, bolt shows the background
    im.alpha_composite(logo, ((2732 - 640) // 2, (2732 - 640) // 2))
    return im


web = sys.argv[1]
for name, size, bleed in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                          ("maskable-512.png", 512, True), ("apple-touch-icon.png", 180, True),
                          ("favicon-32.png", 32, False)]:
    img = art("full", 0.72) if bleed else art("rounded", 0.9)  # 0.72 keeps the maskable art in its safe zone
    img.resize((size, size), Image.LANCZOS).save(f"{web}/{name}")

if len(sys.argv) > 2:
    out = sys.argv[2]
    art("full", 0.72).save(f"{out}/icon-only.png")
    art(None, 0.6).save(f"{out}/icon-foreground.png")  # Android adaptive icons crop to the middle ~66%
    Image.new("RGBA", (S, S), TEAL).save(f"{out}/icon-background.png")
    splash(TEAL).save(f"{out}/splash.png")
    splash(DARK).save(f"{out}/splash-dark.png")
print("ok")
