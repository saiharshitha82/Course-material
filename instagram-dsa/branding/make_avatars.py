"""Profile picture options in the Reels' 'board' theme. 1080x1080 PNGs;
Instagram crops to a circle, so everything important sits in the centre ~70%.

    python branding/make_avatars.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
import os  # noqa: E402
os.environ.setdefault("REEL_THEME", "board")
from reelkit import COLORS, font  # noqa: E402

S = 1080
C = COLORS


def canvas():
    return Image.new("RGB", (S, S), C["bg"])


def cell(d, cx, cy, size, text, hl=False, fsize=None):
    h = size / 2
    d.rounded_rectangle([cx - h, cy - h, cx + h, cy + h], radius=int(size * 0.18),
                        fill=C["primary_soft"] if hl else C["surface"],
                        outline=C["primary"] if hl else C["line"], width=max(6, size // 18))
    d.text((cx, cy), text, font=font("sans-black", fsize or int(size * 0.5)),
           fill=C["primary"] if hl else C["ink"], anchor="mm")


def option_a():
    """[0] — the 'counting starts at zero' motif from episode 01."""
    im = canvas()
    d = ImageDraw.Draw(im)
    d.text((S / 2, S / 2 - 20), "[0]", font=font("mono-bold", 360), fill=C["primary"], anchor="mm")
    d.text((S / 2, S / 2 + 230), "DSA in Python", font=font("sans-black", 72),
           fill=C["ink"], anchor="mm")
    return im


def option_b():
    """Three list cells D S A, the middle one highlighted, with the pointer arrow."""
    im = canvas()
    d = ImageDraw.Draw(im)
    size, gap = 230, 26
    for i, ch in enumerate("DSA"):
        cell(d, S / 2 + (i - 1) * (size + gap), S / 2 + 60, size, ch, hl=(i == 1))
    x, y = S / 2, S / 2 - 200
    d.rectangle([x - 14, y - 70, x + 14, y + 20], fill=C["primary"])
    d.polygon([(x - 55, y + 10), (x + 55, y + 10), (x, y + 80)], fill=C["primary"])
    for i in range(3):
        d.text((S / 2 + (i - 1) * (size + gap), S / 2 + 60 + size / 2 + 70), str(i),
               font=font("mono-bold", 56), fill=C["accent"], anchor="mm")
    return im


def option_c():
    """Code-first: a >>> prompt and a blinking caret, like the REPL card."""
    im = canvas()
    d = ImageDraw.Draw(im)
    r = 330
    d.rounded_rectangle([S / 2 - r, S / 2 - 230, S / 2 + r, S / 2 + 230], radius=60,
                        fill=C["card"])
    f = font("mono-bold", 210)
    d.text((S / 2 - 250, S / 2), ">>>", font=f, fill=C["primary"], anchor="lm")
    d.rectangle([S / 2 + 175, S / 2 - 95, S / 2 + 215, S / 2 + 95], fill=C["accent"])
    return im


def circle_preview(ims, path):
    """How each option looks in Instagram's round crop, at feed size and full size."""
    pad, big, small = 40, 420, 110
    out = Image.new("RGB", (pad + len(ims) * (big + pad), big + small + pad * 3), (250, 250, 250))
    mask_big = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask_big).ellipse([0, 0, big, big], fill=255)
    mask_small = Image.new("L", (small, small), 0)
    ImageDraw.Draw(mask_small).ellipse([0, 0, small, small], fill=255)
    for i, im in enumerate(ims):
        x = pad + i * (big + pad)
        out.paste(im.resize((big, big), Image.LANCZOS), (x, pad), mask_big)
        out.paste(im.resize((small, small), Image.LANCZOS),
                  (x + (big - small) // 2, big + pad * 2), mask_small)
    out.save(path)


if __name__ == "__main__":
    opts = {"a_index_zero": option_a(), "b_dsa_cells": option_b(), "c_repl_prompt": option_c()}
    for name, im in opts.items():
        im.save(HERE / f"avatar_{name}.png")
    circle_preview(list(opts.values()), HERE / "avatar_options_preview.png")
    print("wrote", ", ".join(f"avatar_{n}.png" for n in opts), "and avatar_options_preview.png")
