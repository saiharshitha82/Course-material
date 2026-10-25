"""Logo round 2: no nest or eggs. Three code / data-structure marks, each shown as an
icon and as a horizontal lockup with the wordmark.

    python branding/make_logo_v2.py
"""

from PIL import Image, ImageDraw

from make_avatars_v2 import CREAM, DEEP, HERE, MID, ORANGE, YELLOW, font, radial_bg

OUT = HERE / "logo_v2"
FIRST, SECOND = "Codes", "Nest"
TAGLINE = "Python DSA, made visual"
SS = 2
MUTED = (163, 196, 179)


def icon_cells(d, cx, cy, u):
    """C and N as two list cells, indices 0 and 1 above, N lit as the current item."""
    cell, gap = 1.0 * u, 0.12 * u
    x0 = cx - cell - gap / 2
    for i, (ch, lit) in enumerate([("C", False), ("N", True)]):
        x = x0 + i * (cell + gap)
        box = [x, cy - cell / 2, x + cell, cy + cell / 2]
        d.rounded_rectangle(box, radius=int(cell * 0.18), fill=YELLOW if lit else MID,
                            outline=YELLOW, width=max(4, int(u * 0.07)))
        d.text((x + cell / 2, cy + u * 0.02), ch, font=font("sans-black", int(cell * 0.62)),
               fill=DEEP if lit else CREAM, anchor="mm")
        d.text((x + cell / 2, cy - cell / 2 - u * 0.12), str(i),
               font=font("mono-bold", int(u * 0.26)), fill=ORANGE, anchor="ms")


def icon_braces(d, cx, cy, u):
    """{CN} — a code block holding the initials."""
    fb = font("mono-bold", int(u * 2.0))
    d.text((cx - u * 1.05, cy), "{", font=fb, fill=ORANGE, anchor="mm")
    d.text((cx + u * 1.05, cy), "}", font=fb, fill=ORANGE, anchor="mm")
    f = font("sans-black", int(u * 1.0))
    wc = f.getlength("C")
    wn = f.getlength("N")
    x = cx - (wc + wn) / 2
    d.text((x, cy + u * 0.04), "C", font=f, fill=CREAM, anchor="lm")
    d.text((x + wc, cy + u * 0.04), "N", font=f, fill=YELLOW, anchor="lm")


def icon_graph_n(d, cx, cy, u):
    """The letter N drawn as a graph: four nodes joined by three edges."""
    h, w = 1.5 * u, 1.1 * u
    pts = [(cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2),
           (cx + w / 2, cy + h / 2), (cx + w / 2, cy - h / 2)]
    lw = max(6, int(u * 0.16))
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=CREAM, width=lw)
    r = u * 0.2
    for i, (x, y) in enumerate(pts):
        lit = i == len(pts) - 1
        d.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if lit else DEEP,
                  outline=YELLOW, width=max(4, int(u * 0.08)))


# (key, label, draw function, half-width of the icon in units of u)
ICONS = [("cells", "1  [C][N] list cells", icon_cells, 1.06),
         ("braces", "2  {CN} code block", icon_braces, 1.55),
         ("graph", "3  N as a graph", icon_graph_n, 0.75)]


def square_icon(draw_fn, n=1080):
    N = n * SS
    im = radial_bg().resize((N, N)).convert("RGBA")
    draw_fn(ImageDraw.Draw(im), N / 2, N / 2, N * 0.26)
    return im.resize((n, n), Image.LANCZOS)


def lockup(draw_fn, half_w, bg="dark"):
    W_, H_ = 2400 * SS, 800 * SS
    if bg == "dark":
        im = radial_bg().resize((W_, W_)).crop((0, (W_ - H_) // 2, W_, (W_ + H_) // 2)).convert("RGBA")
        first_col, second_col, tag_col = CREAM, YELLOW, MUTED
    else:
        im = Image.new("RGBA", (W_, H_), (255, 255, 255, 255))
        first_col, second_col, tag_col = DEEP, (180, 83, 9), (59, 107, 80)
    d = ImageDraw.Draw(im)
    u = H_ * 0.26
    icx = H_ * 0.18 + half_w * u
    draw_fn(d, icx, H_ / 2, u)
    tx = icx + half_w * u + u * 0.55
    f = font("sans-black", int(H_ * 0.30))
    w1 = f.getlength(FIRST)
    d.text((tx, H_ * 0.44), FIRST, font=f, fill=first_col, anchor="lm")
    d.text((tx + w1, H_ * 0.44), SECOND, font=f, fill=second_col, anchor="lm")
    d.text((tx + 8, H_ * 0.70), TAGLINE, font=font("sans-semibold", int(H_ * 0.085)),
           fill=tag_col, anchor="lm")
    return im.resize((W_ // SS, H_ // SS), Image.LANCZOS)


def preview(rows, out):
    """rows: [(label, icon_img, lockup_img)]"""
    ih, lw = 300, 900
    pad = 30
    sheet = Image.new("RGB", (pad * 3 + ih + lw, len(rows) * (ih + pad + 50) + pad),
                      (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    y = pad
    for label, icon, lock in rows:
        d.text((pad, y), label, font=font("sans-bold", 30), fill=(30, 30, 30))
        y += 46
        m = Image.new("L", (ih, ih), 0)
        ImageDraw.Draw(m).ellipse([0, 0, ih, ih], fill=255)
        sheet.paste(icon.resize((ih, ih), Image.LANCZOS), (pad, y), m)
        lk = lock.resize((lw, lw // 3), Image.LANCZOS)
        sheet.paste(lk, (pad * 2 + ih, y + (ih - lk.height) // 2))
        y += ih + pad
    sheet.save(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    rows = []
    for key, label, fn, half_w in ICONS:
        icon = square_icon(fn)
        icon.save(OUT / f"{key}_icon.png")
        dark = lockup(fn, half_w, "dark")
        dark.save(OUT / f"{key}_horizontal_dark.png")
        lockup(fn, half_w, "light").save(OUT / f"{key}_horizontal_light.png")
        rows.append((label, icon, dark))
    preview(rows, OUT / "preview.png")
    print("done")
