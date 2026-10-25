"""Profile picture options, round 2: logo-style marks with depth.

Drawn at 2x and downsampled for smooth edges. Instagram crops to a circle,
so each mark sits inside the centre ~70%.

    python branding/make_avatars_v2.py
"""

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
from reelkit import font  # noqa: E402

S = 1080 * 2  # supersampled
YELLOW = (253, 224, 71)
ORANGE = (251, 146, 60)
CREAM = (241, 246, 243)
DEEP = (12, 44, 32)
MID = (30, 92, 67)


def radial_bg(inner=MID, outer=DEEP):
    y, x = np.mgrid[0:S, 0:S]
    r = np.sqrt((x - S / 2) ** 2 + (y - S / 2.3) ** 2) / (S * 0.72)
    r = np.clip(r, 0, 1)[..., None]
    arr = np.array(inner) * (1 - r) + np.array(outer) * r
    return Image.fromarray(arr.astype("uint8"), "RGB")


def with_shadow(base, layer, offset=(0, 28), blur=36, alpha=0.55):
    """Composite an RGBA layer over base with a soft drop shadow."""
    a = layer.split()[3]
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: int(v * alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = base.convert("RGBA")
    out.alpha_composite(sh, offset)
    out.alpha_composite(layer)
    return out.convert("RGB")


def finish(im):
    return im.resize((S // 2, S // 2), Image.LANCZOS)


def snake():
    """A python made of linked-list nodes: Python + data structures in one mark."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    # tail on the left, head on the right facing right; nodes grow toward the head
    pts = []
    n = 7
    for i in range(n):
        t = i / (n - 1)
        x = S * (0.18 + 0.56 * t)
        y = S * 0.52 + math.sin(t * math.pi * 1.5 - 0.4) * S * 0.12
        pts.append((x, y, 58 + 50 * t))
    for (x0, y0, _), (x1, y1, _) in zip(pts, pts[1:]):
        d.line([x0, y0, x1, y1], fill=YELLOW, width=34)
    for i, (x, y, r) in enumerate(pts):
        head = i == len(pts) - 1
        col = YELLOW if head else CREAM
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=YELLOW, width=18)
        if not head:
            d.ellipse([x - r * 0.28, y - r * 0.28, x + r * 0.28, y + r * 0.28], fill=DEEP)
    hx, hy, hr = pts[-1]
    # eye and forked tongue
    d.ellipse([hx + hr * 0.1, hy - hr * 0.5, hx + hr * 0.5, hy - hr * 0.1], fill=DEEP)
    tx = hx + hr
    d.line([tx - 10, hy + 10, tx + 90, hy + 10], fill=ORANGE, width=16)
    d.line([tx + 90, hy + 10, tx + 130, hy - 20], fill=ORANGE, width=14)
    d.line([tx + 90, hy + 10, tx + 130, hy + 40], fill=ORANGE, width=14)
    return finish(with_shadow(base, L))


def tree():
    """A binary tree, the classic algorithms icon, with the root lit up."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    levels = [[(0.5, 0.30)], [(0.34, 0.52), (0.66, 0.52)],
              [(0.25, 0.73), (0.43, 0.73), (0.57, 0.73), (0.75, 0.73)]]
    for li in range(2):
        for pi, (px, py) in enumerate(levels[li]):
            for cx, cy in levels[li + 1][pi * 2: pi * 2 + 2]:
                d.line([px * S, py * S, cx * S, cy * S], fill=CREAM, width=30)
    radii = [150, 118, 92]
    for li, lvl in enumerate(levels):
        for x, y in lvl:
            r = radii[li]
            fill = YELLOW if li == 0 else (CREAM if li == 1 else MID)
            d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=fill,
                      outline=YELLOW if li else DEEP, width=20 if li else 0)
    d.text((0.5 * S, 0.30 * S), "Py", font=font("sans-black", 150), fill=DEEP, anchor="mm")
    return finish(with_shadow(base, L))


def wordmark():
    """A typographic mark: dsa.py, like a file name."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font("mono-bold", 400)
    w1 = f.getlength("dsa")
    w2 = f.getlength(".py")
    x = (S - w1 - w2) / 2
    d.text((x, S * 0.47), "dsa", font=f, fill=CREAM, anchor="lm")
    d.text((x + w1, S * 0.47), ".py", font=f, fill=YELLOW, anchor="lm")
    # underline caret, like the REPL card
    d.rounded_rectangle([x, S * 0.6, x + w1 + w2, S * 0.6 + 34], radius=17, fill=ORANGE)
    return finish(with_shadow(base, L))


def stack():
    """Three stacked blocks with the top one lifting off: push/pop as a logo."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    w, h, gap = S * 0.46, S * 0.12, S * 0.035
    x0 = (S - w) / 2
    y = S * 0.70
    for i, col in enumerate([MID, CREAM, YELLOW]):
        lift = S * 0.05 if i == 2 else 0
        top = y - i * (h + gap) - lift - h
        d.rounded_rectangle([x0, top, x0 + w, top + h], radius=int(h * 0.3),
                            fill=col, outline=YELLOW if i < 2 else None, width=16)
    ax = S / 2
    d.polygon([(ax - 60, S * 0.205), (ax + 60, S * 0.205), (ax, S * 0.145)], fill=ORANGE)
    d.rectangle([ax - 16, S * 0.2, ax + 16, S * 0.245], fill=ORANGE)
    return finish(with_shadow(base, L))


def preview(ims, labels, path):
    pad, big, small = 40, 360, 110
    out = Image.new("RGB", (pad + len(ims) * (big + pad), big + small + pad * 3 + 50),
                    (248, 248, 248))
    d = ImageDraw.Draw(out)
    for i, (im, label) in enumerate(zip(ims, labels)):
        x = pad + i * (big + pad)
        for size, y in ((big, pad), (small, big + pad * 2)):
            m = Image.new("L", (size, size), 0)
            ImageDraw.Draw(m).ellipse([0, 0, size, size], fill=255)
            out.paste(im.resize((size, size), Image.LANCZOS),
                      (x + (big - size) // 2, y), m)
        d.text((x + big / 2, big + small + pad * 3 + 10), label,
               font=font("sans-bold", 30), fill=(30, 30, 30), anchor="mm")
    out.save(path)


if __name__ == "__main__":
    opts = [("1_snake_nodes", "1  Node snake", snake()),
            ("2_binary_tree", "2  Binary tree", tree()),
            ("3_wordmark", "3  dsa.py", wordmark()),
            ("4_stack", "4  Stack", stack())]
    for name, _, im in opts:
        im.save(HERE / f"v2_avatar_{name}.png")
    preview([o[2] for o in opts], [o[1] for o in opts], HERE / "v2_avatar_options_preview.png")
    print("done")
