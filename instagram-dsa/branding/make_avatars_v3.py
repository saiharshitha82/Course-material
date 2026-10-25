"""Profile picture options, round 3: marks built around the CodeNest name.

Reuses the round-2 helpers (radial background, soft shadow, 2x supersampling).

    python branding/make_avatars_v3.py
"""

from PIL import Image, ImageDraw

from make_avatars_v2 import (CREAM, DEEP, HERE, MID, ORANGE, S, YELLOW, finish, font,
                             preview, radial_bg, with_shadow)


def brace_nest():
    """{ } as a nest holding three eggs: code + nest in one shape."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font("mono-bold", 820)
    d.text((S * 0.27, S * 0.5), "{", font=f, fill=CREAM, anchor="mm")
    d.text((S * 0.73, S * 0.5), "}", font=f, fill=CREAM, anchor="mm")
    # three eggs, the middle one lit like the "current item" in the Reels
    for i, (x, col) in enumerate([(0.385, CREAM), (0.5, YELLOW), (0.615, CREAM)]):
        cx, cy = x * S, S * (0.56 if i != 1 else 0.52)
        rx, ry = S * 0.046, S * 0.064
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col,
                  outline=YELLOW, width=14 if col == CREAM else 0)
    return finish(with_shadow(base, L))


def woven_nest():
    """A woven nest holding three eggs numbered like list indices: 0, 1, 2."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    cx, rim = S / 2, S * 0.54
    # eggs first, so the nest's front rim overlaps them
    f = font("mono-bold", 120)
    for i, (x, dy) in enumerate([(-0.155, 0.02), (0.0, -0.03), (0.155, 0.02)]):
        ex, ey = cx + x * S, rim - S * 0.07 + dy * S
        rx, ry = S * 0.085, S * 0.11
        d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=YELLOW if i == 1 else CREAM,
                  outline=DEEP, width=12)
        d.text((ex, ey - S * 0.012), str(i), font=f, fill=DEEP, anchor="mm")
    # bowl: a filled half-ellipse, then woven strands across it
    w, h = S * 0.66, S * 0.36
    box = [cx - w / 2, rim - h / 2, cx + w / 2, rim + h / 2]
    d.chord(box, 0, 180, fill=ORANGE)
    for k in range(6):
        inset = k * S * 0.028
        d.arc([box[0] + inset, box[1] + inset * 0.6, box[2] - inset, box[3] - inset * 0.6],
              8, 172, fill=YELLOW if k % 2 == 0 else DEEP, width=16)
    d.rounded_rectangle([box[0] - 10, rim - 22, box[2] + 10, rim + 22], radius=22, fill=YELLOW)
    return finish(with_shadow(base, L))


def nested_squares():
    """[[[ ]]]: nested arrays shrinking to a yellow core. 'Nest' as in nesting."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    sizes = [0.56, 0.42, 0.28]
    for i, sz in enumerate(sizes):
        half = S * sz / 2
        r = int(half * 0.22)
        d.rounded_rectangle([S / 2 - half, S / 2 - half, S / 2 + half, S / 2 + half],
                            radius=r, fill=MID if i % 2 == 0 else DEEP,
                            outline=CREAM if i < 2 else YELLOW, width=26)
    half = S * 0.075
    d.rounded_rectangle([S / 2 - half, S / 2 - half, S / 2 + half, S / 2 + half],
                        radius=int(half * 0.3), fill=YELLOW)
    return finish(with_shadow(base, L))


def wordmark():
    """CodeNest as a two-line mark; reads at small sizes thanks to the heavy weight."""
    base = radial_bg()
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = font("sans-black", 330)
    d.text((S / 2, S * 0.40), "code", font=f, fill=CREAM, anchor="mm")
    d.text((S / 2, S * 0.62), "nest", font=f, fill=YELLOW, anchor="mm")
    w = f.getlength("nest")
    d.rounded_rectangle([S / 2 - w / 2, S * 0.71, S / 2 + w / 2, S * 0.71 + 30],
                        radius=15, fill=ORANGE)
    return finish(with_shadow(base, L))


if __name__ == "__main__":
    opts = [("1_brace_nest", "1  { nest }", brace_nest()),
            ("2_woven_nest", "2  Nest of 0 1 2", woven_nest()),
            ("3_nested_squares", "3  Nested arrays", nested_squares()),
            ("4_wordmark", "4  code / nest", wordmark())]
    for name, _, im in opts:
        im.save(HERE / f"v3_avatar_{name}.png")
    preview([o[2] for o in opts], [o[1] for o in opts], HERE / "v3_avatar_options_preview.png")
    print("done")
