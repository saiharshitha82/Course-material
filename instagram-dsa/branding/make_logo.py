"""Logo: the 0 1 2 nest mark plus the wordmark, in horizontal and stacked layouts.

Outputs (in branding/logo/), for each spelling in NAMES:
    <name>_horizontal_dark.png         on the videos' dark green
    <name>_horizontal_light.png        dark-green text, for white backgrounds
    <name>_horizontal_transparent.png  cream text on transparent (for dark photos/video)
    <name>_stacked_dark.png            square, icon above the name
    <name>_stacked_transparent.png
    icon_transparent.png               the nest alone

    python branding/make_logo.py
"""

from PIL import Image, ImageDraw

from make_avatars_v2 import CREAM, DEEP, HERE, S, YELLOW, font, radial_bg, with_shadow
from make_avatars_v4 import draw_nest

OUT = HERE / "logo"
NAMES = {"codesnest": ("Codes", "Nest"), "codenest": ("Code", "Nest")}
TAGLINE = "Python DSA, made visual"
SS = 2  # supersampling factor


def nest_layer(size, k):
    """Draw the nest centred on a transparent square layer of `size` px (pre-supersampled).
    draw_nest positions eggs relative to S, so draw at S and scale the layer."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_nest(ImageDraw.Draw(L), S / 2, S * 0.56, scale=k)
    box = L.getbbox()
    L = L.crop(box)
    w, h = L.size
    f = size / max(w, h)
    return L.resize((int(w * f), int(h * f)), Image.LANCZOS)


AMBER = (180, 83, 9)  # "Nest" on white: yellow is too faint there


def wordmark(d, x, y, first, second, size, first_col, anchor="lm", second_col=YELLOW):
    f = font("sans-black", size)
    w1 = f.getlength(first)
    if anchor == "mm":
        x -= (w1 + f.getlength(second)) / 2
    d.text((x, y), first, font=f, fill=first_col, anchor="lm")
    d.text((x + w1, y), second, font=f, fill=second_col, anchor="lm")
    return w1 + f.getlength(second)


def horizontal(first, second, bg):
    W_, H_ = 2400 * SS, 800 * SS
    if bg == "dark":
        base = radial_bg().resize((W_, W_)).crop((0, (W_ - H_) // 2, W_, (W_ + H_) // 2))
        canvas = base.convert("RGBA")
        text_col, tag_col = CREAM, (163, 196, 179)
    else:
        canvas = Image.new("RGBA", (W_, H_), (255, 255, 255, 0 if bg == "transparent" else 255))
        text_col = CREAM if bg == "transparent" else DEEP
        tag_col = (163, 196, 179) if bg == "transparent" else (59, 107, 80)
    icon = nest_layer(int(H_ * 0.62), 1.0)
    pad = int(H_ * 0.16)
    canvas.alpha_composite(icon, (pad, (H_ - icon.height) // 2))
    d = ImageDraw.Draw(canvas)
    tx = pad + icon.width + int(H_ * 0.12)
    size = int(H_ * 0.30)
    wordmark(d, tx, H_ * 0.44, first, second, size, text_col,
             second_col=AMBER if bg == "light" else YELLOW)
    d.text((tx + 8, H_ * 0.70), TAGLINE, font=font("sans-semibold", int(H_ * 0.085)),
           fill=tag_col, anchor="lm")
    # trim right-hand empty space so the lockup is tight
    if bg != "dark":
        box = canvas.getbbox()
        canvas = canvas.crop((0, 0, min(W_, box[2] + pad), H_))
    return canvas.resize((canvas.width // SS, canvas.height // SS), Image.LANCZOS)


def stacked(first, second, bg):
    N = 1080 * SS
    if bg == "dark":
        canvas = radial_bg().resize((N, N)).convert("RGBA")
    else:
        canvas = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    icon = nest_layer(int(N * 0.50), 1.0)
    canvas.alpha_composite(icon, ((N - icon.width) // 2, int(N * 0.24)))
    d = ImageDraw.Draw(canvas)
    wordmark(d, N / 2, N * 0.65, first, second, int(N * 0.15), CREAM, anchor="mm")
    d.text((N / 2, N * 0.765), TAGLINE, font=font("sans-semibold", int(N * 0.045)),
           fill=(163, 196, 179), anchor="mm")
    return canvas.resize((N // SS, N // SS), Image.LANCZOS)


def preview(paths, out):
    ims = [Image.open(p) for p in paths]
    w = 1200
    rows = []
    for im in ims:
        f = w / im.width if im.width > im.height else 600 / im.height
        rows.append(im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS))
    H_ = sum(r.height for r in rows) + 40 * (len(rows) + 1)
    sheet = Image.new("RGB", (w + 80, H_), (200, 200, 200))
    # checkerboard behind transparent logos
    d = ImageDraw.Draw(sheet)
    for yy in range(0, H_, 40):
        for xx in range(0, w + 80, 40):
            if (xx // 40 + yy // 40) % 2:
                d.rectangle([xx, yy, xx + 39, yy + 39], fill=(225, 225, 225))
    y = 40
    for r in rows:
        sheet.paste(r, (40 + (w - r.width) // 2, y), r if r.mode == "RGBA" else None)
        y += r.height + 40
    sheet.save(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    nest_layer(1024, 1.0).save(OUT / "icon_transparent.png")
    for key, (first, second) in NAMES.items():
        files = []
        for bg in ("dark", "light", "transparent"):
            p = OUT / f"{key}_horizontal_{bg}.png"
            horizontal(first, second, bg).save(p)
            files.append(p)
        for bg in ("dark", "transparent"):
            p = OUT / f"{key}_stacked_{bg}.png"
            stacked(first, second, bg).save(p)
            files.append(p)
        preview([files[0], files[1], files[3]], OUT / f"{key}_preview.png")
    print("done:", sorted(p.name for p in OUT.iterdir()))
