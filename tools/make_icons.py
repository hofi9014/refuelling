"""Draws the app logo (fuel drop with a gauge needle, "logo A" in store/logo-proposals.html).

usage: python tools/make_icons.py docs/icons [assets]
The optional second folder gets the 1024 px sources for `npm run icons` (@capacitor/assets -> Android icons and splash).
"""
import math
import sys
from PIL import Image, ImageDraw

S = 1024  # draw large, downscale for smooth edges
GRAPHITE = (23, 25, 28)
PAPER = (242, 238, 229)
AMBER = (226, 154, 23)


def art(bg="rounded", k=0.9, bg_color=GRAPHITE, fg=PAPER):
    """bg: "rounded" tile, "full" square, or None (transparent, gauge cut out of the drop). fg: colour of the drop."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg == "full":
        d.rectangle([0, 0, S, S], fill=bg_color)
    elif bg == "rounded":
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=bg_color)
    c = S / 2
    u = k * S / 96  # the design is on a 96 unit grid

    def P(x, y):
        return (c + (x - 48) * u, c + (y - 48) * u)

    def disc(x, y, r, fill):
        cx, cy = P(x, y)
        d.ellipse([cx - r * u, cy - r * u, cx + r * u, cy + r * u], fill=fill)

    cut = bg_color if bg else (0, 0, 0, 0)  # ImageDraw writes pixels directly, so a transparent fill really cuts
    # drop: circle plus a triangle whose sides are tangent to it
    disc(48, 58.2, 28.2, fg)
    d.polygon([P(48, 9), P(24.9, 42), P(71.1, 42)], fill=fg)
    # gauge arc
    cx, cy = P(49.1, 65.1)
    r = 17.4 * u
    width = 6.6 * u
    d.arc([cx - r - width / 2, cy - r - width / 2, cx + r + width / 2, cy + r + width / 2], 175, 330, fill=cut, width=int(width))
    for a in (175, 330):  # round caps
        ax = 49.1 + 17.4 * math.cos(math.radians(a))
        ay = 65.1 + 17.4 * math.sin(math.radians(a))
        disc(ax, ay, 3.3, cut)
    # needle and hub
    d.line([P(48, 64.8), P(61.2, 47.7)], fill=AMBER, width=int(7.8 * u))
    disc(61.2, 47.7, 3.9, AMBER)
    disc(48, 65.4, 5.7, AMBER)
    return im


def splash(color):
    im = Image.new("RGBA", (2732, 2732), color)
    logo = art(None, 0.9).resize((640, 640), Image.LANCZOS)
    im.alpha_composite(logo, ((2732 - 640) // 2, (2732 - 640) // 2))
    return im


if __name__ == "__main__":
    web = sys.argv[1]
    for name, size, bleed in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                              ("maskable-512.png", 512, True), ("apple-touch-icon.png", 180, True),
                              ("favicon-32.png", 32, False)]:
        img = art("full", 0.72) if bleed else art("rounded", 0.86)  # 0.72 keeps the maskable art in its safe zone
        img.resize((size, size), Image.LANCZOS).save(f"{web}/{name}")

    if len(sys.argv) > 2:
        out = sys.argv[2]
        art("full", 0.72).save(f"{out}/icon-only.png")
        art(None, 0.6).save(f"{out}/icon-foreground.png")  # Android adaptive icons crop to the middle ~66%
        Image.new("RGBA", (S, S), GRAPHITE).save(f"{out}/icon-background.png")
        splash(GRAPHITE).save(f"{out}/splash.png")
        splash(GRAPHITE).save(f"{out}/splash-dark.png")
    print("ok")
