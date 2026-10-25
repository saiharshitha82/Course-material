"""Logo round 3: code-first marks (no nest, no eggs).

Four options, each an icon tile plus a monospace wordmark:
    A  {cn}        braces monogram
    B  >>> _       the Python REPL prompt, as in every Reel's code card
    C  [c|n]       array cells with an index pointer, the Reels' visual language
    D  </>         the classic code glyph, slash in yellow

Outputs go to branding/logo_v3/: <option>_icon.png (1080 square, dark),
<option>_<name>_horizontal_dark.png / _light.png, and a preview sheet per spelling.

    python branding/make_logo_v3.py
"""

from PIL import Image, ImageDraw

from make_avatars_v2 import CREAM, DEEP, HERE, MID, ORANGE, S, YELLOW, font, radial_bg, with_shadow

OUT = HERE / "logo_v3"
NAMES = {"codenest": ("code", "nest"), "codesnest": ("codes", "nest")}
TAGLINE = "Python DSA, made visual"
MUTED = (163, 196, 179)
AMBER = (180, 83, 9)
INK_LIGHT = DEEP
SS = 2


# ---------------------------------------------------------------------------
# Icon marks, drawn on a transparent S × S layer
# ---------------------------------------------------------------------------

def tile(d, fill=MID, outline=YELLOW):
    m = S * 0.12
    d.rounded_rectangle([m, m, S - m, S - m], radius=int(S * 0.2), fill=fill,
                        outline=outline, width=int(S * 0.018))


def mark_braces(d):
    tile(d)
    fb = font("mono-bold", int(S * 0.34))
    d.text((S * 0.27, S * 0.49), "{", font=fb, fill=ORANGE, anchor="mm")
    d.text((S * 0.73, S * 0.49), "}", font=fb, fill=ORANGE, anchor="mm")
    f = font("mono-bold", int(S * 0.22))
    d.text((S * 0.435, S * 0.50), "c", font=f, fill=CREAM, anchor="mm")
    d.text((S * 0.565, S * 0.50), "n", font=f, fill=YELLOW, anchor="mm")


def mark_repl(d):
    tile(d, fill=DEEP)
    # editor dots, as on the Reels' code card
    for i in range(3):
        cx = S * (0.27 + i * 0.07)
        r = S * 0.022
        d.ellipse([cx - r, S * 0.25 - r, cx + r, S * 0.25 + r], fill=(75, 122, 102))
    f = font("mono-bold", int(S * 0.24))
    d.text((S * 0.24, S * 0.56), ">>>", font=f, fill=YELLOW, anchor="lm")
    w = f.getlength(">>>")
    x = S * 0.24 + w + S * 0.05
    d.rounded_rectangle([x, S * 0.47, x + S * 0.075, S * 0.66], radius=8, fill=CREAM)


def mark_cells(d):
    # two joined array cells "c" "n", pointer on "n", indices below
    cs = S * 0.30
    x0 = (S - 2 * cs) / 2
    y0 = S * 0.36
    f = font("mono-bold", int(cs * 0.62))
    for i, (ch, col) in enumerate((("c", CREAM), ("n", YELLOW))):
        x = x0 + i * cs
        fill = MID if i == 0 else (77, 83, 35)
        d.rectangle([x, y0, x + cs, y0 + cs], fill=fill, outline=CREAM if i == 0 else YELLOW,
                    width=int(S * 0.016))
        d.text((x + cs / 2, y0 + cs / 2), ch, font=f, fill=col, anchor="mm")
        d.text((x + cs / 2, y0 + cs + S * 0.09), str(i), font=font("mono-bold", int(S * 0.08)),
               fill=MUTED if i == 0 else YELLOW, anchor="mm")
    # pointer arrow above "n"
    ax = x0 + cs * 1.5
    d.rectangle([ax - S * 0.014, S * 0.17, ax + S * 0.014, S * 0.27], fill=ORANGE)
    d.polygon([(ax - S * 0.05, S * 0.26), (ax + S * 0.05, S * 0.26), (ax, S * 0.32)], fill=ORANGE)


def mark_glyph(d):
    tile(d)
    f = font("mono-bold", int(S * 0.40))
    d.text((S * 0.29, S * 0.50), "<", font=f, fill=CREAM, anchor="mm")
    d.text((S * 0.50, S * 0.50), "/", font=f, fill=YELLOW, anchor="mm")
    d.text((S * 0.71, S * 0.50), ">", font=f, fill=CREAM, anchor="mm")


MARKS = {
    "A_braces": ("A  {cn} braces", mark_braces),
    "B_repl": ("B  >>> prompt", mark_repl),
    "C_cells": ("C  array cells", mark_cells),
    "D_glyph": ("D  </> glyph", mark_glyph),
}


def icon_layer(fn):
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    fn(ImageDraw.Draw(L))
    return L


def icon_square(fn):
    """1080 × 1080 on the dark radial background, with a soft shadow (profile-picture ready)."""
    return with_shadow(radial_bg(), icon_layer(fn)).resize((S // 2, S // 2), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Horizontal lockup: icon + monospace wordmark with a caret
# ---------------------------------------------------------------------------

def horizontal(fn, first, second, bg):
    W_, H_ = 2400 * SS, 800 * SS
    if bg == "dark":
        canvas = radial_bg().resize((W_, W_)).crop((0, (W_ - H_) // 2, W_, (W_ + H_) // 2)).convert("RGBA")
        c1, c2, tag = CREAM, YELLOW, MUTED
    else:
        canvas = Image.new("RGBA", (W_, H_), (255, 255, 255, 255))
        c1, c2, tag = INK_LIGHT, AMBER, (59, 107, 80)
    L = icon_layer(fn)
    box = L.getbbox()
    L = L.crop(box)
    f_ = (H_ * 0.66) / max(L.size)
    L = L.resize((int(L.width * f_), int(L.height * f_)), Image.LANCZOS)
    pad = int(H_ * 0.16)
    canvas.alpha_composite(L, (pad, (H_ - L.height) // 2))
    d = ImageDraw.Draw(canvas)
    tx = pad + L.width + int(H_ * 0.11)
    f = font("mono-bold", int(H_ * 0.27))
    w1 = f.getlength(first)
    y = H_ * 0.44
    d.text((tx, y), first, font=f, fill=c1, anchor="lm")
    d.text((tx + w1, y), second, font=f, fill=c2, anchor="lm")
    cx = tx + w1 + f.getlength(second) + H_ * 0.03
    d.rectangle([cx, y - H_ * 0.13, cx + H_ * 0.05, y + H_ * 0.12], fill=ORANGE)
    d.text((tx + 6, H_ * 0.71), TAGLINE, font=font("sans-semibold", int(H_ * 0.085)),
           fill=tag, anchor="lm")
    return canvas.resize((W_ // SS, H_ // SS), Image.LANCZOS)


def preview(rows, labels, out):
    w = 1640
    pad = 30
    thumbs = []
    for (hz, ic), lab in zip(rows, labels):
        hz_t = hz.resize((1000, int(hz.height * 1000 / hz.width)), Image.LANCZOS)
        size = hz_t.height
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).ellipse([0, 0, size, size], fill=255)
        ic_t = ic.resize((size, size), Image.LANCZOS)
        thumbs.append((hz_t, ic_t, m, lab))
    H_ = sum(t[0].height + 70 for t in thumbs) + pad
    sheet = Image.new("RGB", (w, H_), (246, 246, 246))
    d = ImageDraw.Draw(sheet)
    y = pad
    for hz_t, ic_t, m, lab in thumbs:
        d.text((pad, y), lab, font=font("sans-bold", 30), fill=(30, 30, 30))
        y += 40
        sheet.paste(hz_t.convert("RGB"), (pad, y))
        sheet.paste(ic_t, (pad + 1000 + 40, y), m)
        small = ic_t.resize((110, 110), Image.LANCZOS)
        ms = m.resize((110, 110))
        sheet.paste(small, (pad + 1000 + 40 + ic_t.width + 30, y + (ic_t.height - 110) // 2), ms)
        y += hz_t.height + 30
    sheet.save(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    icons = {}
    for key, (label, fn) in MARKS.items():
        icons[key] = icon_square(fn)
        icons[key].save(OUT / f"{key}_icon.png")
    for name, (first, second) in NAMES.items():
        rows = []
        for key, (label, fn) in MARKS.items():
            dark = horizontal(fn, first, second, "dark")
            dark.save(OUT / f"{key}_{name}_horizontal_dark.png")
            horizontal(fn, first, second, "light").save(OUT / f"{key}_{name}_horizontal_light.png")
            rows.append((dark, icons[key]))
        preview(rows, [m[0] for m in MARKS.values()], OUT / f"preview_{name}.png")
    print("done")
