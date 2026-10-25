"""Profile picture options, round 4: the CodeNest name written on the picture.

Text is sized to stay legible in Instagram's ~110 px feed circle.

    python branding/make_avatars_v4.py
"""

from PIL import Image, ImageDraw

from make_avatars_v2 import (CREAM, DEEP, HERE, ORANGE, S, YELLOW, finish, font, preview,
                             radial_bg, with_shadow)


def draw_nest(d, cx, rim, scale=1.0, numbers=True):
    """The round-3 nest (three eggs numbered 0 1 2) at any position and size."""
    k = scale
    f = font("mono-bold", int(120 * k))
    for i, (x, dy) in enumerate([(-0.155, 0.02), (0.0, -0.03), (0.155, 0.02)]):
        ex, ey = cx + x * S * k, rim - S * 0.07 * k + dy * S * k
        rx, ry = S * 0.085 * k, S * 0.11 * k
        d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=YELLOW if i == 1 else CREAM,
                  outline=DEEP, width=max(4, int(12 * k)))
        if numbers:
            d.text((ex, ey - S * 0.012 * k), str(i), font=f, fill=DEEP, anchor="mm")
    w, h = S * 0.66 * k, S * 0.36 * k
    box = [cx - w / 2, rim - h / 2, cx + w / 2, rim + h / 2]
    d.chord(box, 0, 180, fill=ORANGE)
    for j in range(6):
        inset = j * S * 0.028 * k
        d.arc([box[0] + inset, box[1] + inset * 0.6, box[2] - inset, box[3] - inset * 0.6],
              8, 172, fill=YELLOW if j % 2 == 0 else DEEP, width=max(5, int(16 * k)))
    d.rounded_rectangle([box[0] - 10 * k, rim - 22 * k, box[2] + 10 * k, rim + 22 * k],
                        radius=int(22 * k), fill=YELLOW)


def two_tone(d, y, size, first="Code", second="Nest", weight="sans-black"):
    """'Code' in cream + 'Nest' in yellow on one line, centred."""
    f = font(weight, size)
    w1, w2 = f.getlength(first), f.getlength(second)
    x = (S - w1 - w2) / 2
    d.text((x, y), first, font=f, fill=CREAM, anchor="lm")
    d.text((x + w1, y), second, font=f, fill=YELLOW, anchor="lm")
    return x, w1 + w2


def nest_and_name():
    """Nest icon on top, CodeNest underneath."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    draw_nest(d, S / 2, S * 0.46, scale=0.78)
    two_tone(d, S * 0.70, 300)
    return finish(with_shadow(base, L))


def stacked_name():
    """CODE / NEST stacked big, the egg trio as a full stop under it."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font("sans-black", 440)
    d.text((S / 2, S * 0.36), "Code", font=f, fill=CREAM, anchor="mm")
    d.text((S / 2, S * 0.60), "Nest", font=f, fill=YELLOW, anchor="mm")
    for i, x in enumerate((-0.09, 0.0, 0.09)):
        cx, cy = S / 2 + x * S, S * 0.78
        rx, ry = S * 0.032, S * 0.042
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=YELLOW if i == 1 else CREAM)
    return finish(with_shadow(base, L))


def egg_o():
    """CodeNest on one line with the 'o' as a yellow egg, and the nest under it."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font("sans-black", 360)
    parts = ["C", "o", "deNest"]
    widths = [f.getlength(p) for p in parts]
    x = (S - sum(widths)) / 2
    y = S * 0.47
    d.text((x, y), "C", font=f, fill=CREAM, anchor="lm")
    ox = x + widths[0] + widths[1] / 2
    rx, ry = widths[1] * 0.42, S * 0.085
    d.ellipse([ox - rx, y - ry + S * 0.035, ox + rx, y + ry + S * 0.02], fill=YELLOW)
    x2 = x + widths[0] + widths[1]
    d.text((x2, y), "de", font=f, fill=CREAM, anchor="lm")
    d.text((x2 + f.getlength("de"), y), "Nest", font=f, fill=YELLOW, anchor="lm")
    # woven underline: the nest rim
    left, right = x, x + sum(widths)
    for j in range(3):
        yy = S * 0.62 + j * S * 0.03
        inset = j * S * 0.04
        d.arc([left + inset, yy - S * 0.08, right - inset, yy + S * 0.08], 10, 170,
              fill=ORANGE if j % 2 else YELLOW, width=26)
    return finish(with_shadow(base, L))


def brace_name():
    """{ CodeNest } in monospace, like a code block."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    fb = font("mono-bold", 700)
    d.text((S * 0.13, S * 0.5), "{", font=fb, fill=ORANGE, anchor="mm")
    d.text((S * 0.87, S * 0.5), "}", font=fb, fill=ORANGE, anchor="mm")
    f = font("sans-black", 330)
    d.text((S / 2, S * 0.40), "Code", font=f, fill=CREAM, anchor="mm")
    d.text((S / 2, S * 0.62), "Nest", font=f, fill=YELLOW, anchor="mm")
    return finish(with_shadow(base, L))


if __name__ == "__main__":
    opts = [("1_nest_and_name", "1  Nest + name", nest_and_name()),
            ("2_stacked_name", "2  Code / Nest", stacked_name()),
            ("3_egg_o", "3  Egg as the 'o'", egg_o()),
            ("4_brace_name", "4  { Code Nest }", brace_name())]
    for name, _, im in opts:
        im.save(HERE / f"v4_avatar_{name}.png")
    preview([o[2] for o in opts], [o[1] for o in opts], HERE / "v4_avatar_options_preview.png")
    print("done")
