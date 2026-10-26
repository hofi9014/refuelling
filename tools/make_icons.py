import sys
from PIL import Image, ImageDraw

out = sys.argv[1]
S = 1024  # draw large, downscale for smooth edges
TEAL = (15, 118, 110)


def art(full_bleed):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=TEAL)
        k = 0.72  # keep artwork inside the maskable safe zone
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=TEAL)
        k = 0.9
    c = S / 2

    def P(x, y):  # coordinates in a 0..1000 design grid, scaled around the centre
        return (c + (x - 500) * k * S / 1000, c + (y - 500) * k * S / 1000)

    # fuel drop
    d.ellipse([*P(270, 400), *P(730, 860)], fill="white")
    d.polygon([P(500, 130), P(296, 524), P(704, 524)], fill="white")  # sides tangent to the circle
    # lightning bolt cut out of the drop
    d.polygon([P(540, 420), P(420, 660), P(505, 660), P(465, 800), P(590, 570), P(505, 570)], fill=TEAL)
    return im


for name, size, bleed in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                          ("maskable-512.png", 512, True), ("apple-touch-icon.png", 180, True),
                          ("favicon-32.png", 32, False)]:
    art(bleed).resize((size, size), Image.LANCZOS).save(f"{out}/{name}")
print("ok")
