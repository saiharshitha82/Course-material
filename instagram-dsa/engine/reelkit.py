"""reelkit — a tiny, dependency-light animation engine for 9:16 teaching Reels.

Renders frames with Pillow and pipes them to ffmpeg. No Manim / Cairo needed.

    from reelkit import *
    scene = Scene(duration=30)
    scene.add(Title("Python Lists", y=330, start=0.2))
    scene.render("out.mp4")

Every element has `start` / `end` (seconds) and animates itself in and out.
Coordinates are in pixels on a 1080x1920 canvas.
"""

from __future__ import annotations

import math
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Brand tokens (see ../style-guide.md). Change these once, every video follows.
# ---------------------------------------------------------------------------

W, H, FPS = 1080, 1920, 30

# Instagram overlays its own UI on Reels; keep content inside this box.
SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT = 250, 1500, 80, 940

COLORS = {
    "bg": (255, 255, 255),
    "ink": (17, 24, 39),          # primary text
    "muted": (107, 114, 128),     # secondary text, index labels
    "line": (209, 213, 219),      # cell borders, dividers
    "card": (244, 245, 247),      # code card background
    "primary": (37, 99, 235),     # focus / highlight (blue)
    "primary_soft": (219, 234, 254),
    "accent": (245, 158, 11),     # second highlight (amber)
    "accent_soft": (254, 243, 199),
    "good": (5, 150, 105),        # output / correct
    "bad": (220, 38, 38),         # errors
    "bad_soft": (254, 226, 226),
    # syntax highlighting (light theme)
    "kw": (124, 58, 237),
    "num": (217, 119, 6),
    "str": (5, 150, 105),
    "com": (156, 163, 175),
    "fn": (37, 99, 235),
}

FONT_DIRS = [
    Path("/usr/share/fonts/opentype/inter"),
    Path("/usr/share/fonts/truetype/jetbrains-mono"),
    Path(__file__).parent / "fonts",
]
FONT_FILES = {
    "sans": "Inter-Medium.otf",
    "sans-semibold": "Inter-SemiBold.otf",
    "sans-bold": "Inter-Bold.otf",
    "sans-black": "Inter-ExtraBold.otf",
    "mono": "JetBrainsMono-Medium.ttf",
    "mono-bold": "JetBrainsMono-Bold.ttf",
}
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    key = (kind, size)
    if key not in _font_cache:
        name = FONT_FILES[kind]
        for d in FONT_DIRS:
            if (d / name).exists():
                _font_cache[key] = ImageFont.truetype(str(d / name), size)
                break
        else:
            raise FileNotFoundError(f"Font {name} not found in {FONT_DIRS}")
    return _font_cache[key]


# ---------------------------------------------------------------------------
# Easing / helpers
# ---------------------------------------------------------------------------

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def ease_in_out(p):
    return 3 * p * p - 2 * p * p * p


def ease_out_back(p, s=1.70158):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def progress(t, start, dur):
    """0 before `start`, 1 after `start + dur`, eased in between."""
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return clamp((t - start) / dur)


def mix(c1, c2, p):
    return tuple(int(a + (b - a) * p) for a, b in zip(c1, c2))


def text_w(txt, f):
    return f.getlength(txt)


# ---------------------------------------------------------------------------
# Element base: handles enter/exit opacity + slide.
# ---------------------------------------------------------------------------

@dataclass
class Element:
    start: float = 0.0
    end: float = math.inf
    fade_in: float = 0.35
    fade_out: float = 0.25
    slide: int = 24  # px the element rises while fading in

    def visible(self, t):
        return self.start <= t < self.end + self.fade_out

    def alpha(self, t):
        a = ease_out_cubic(progress(t, self.start, self.fade_in))
        if t > self.end:
            a *= 1 - progress(t, self.end, self.fade_out)
        return a

    def dy(self, t):
        return (1 - ease_out_cubic(progress(t, self.start, self.fade_in))) * self.slide

    def draw(self, d: ImageDraw.ImageDraw, t: float):  # pragma: no cover
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Text elements
# ---------------------------------------------------------------------------

@dataclass
class Text(Element):
    text: str = ""
    x: float | None = None  # None = centered
    y: float = 0
    size: int = 48
    weight: str = "sans"
    color: str = "ink"
    anchor: str = "la"  # Pillow anchor; "ma" = middle/top

    def draw(self, d, t):
        f = font(self.weight, self.size)
        x = W / 2 if self.x is None else self.x
        anchor = "ma" if self.x is None else self.anchor
        d.text((x, self.y + self.dy(t)), self.text, font=f,
               fill=COLORS[self.color], anchor=anchor)


@dataclass
class Title(Element):
    """Big hook text. `highlight` words get the primary colour + underline swipe."""
    text: str = ""
    y: float = 300
    size: int = 84
    highlight: tuple[str, ...] = ()
    max_width: int = SAFE_RIGHT - SAFE_LEFT

    def draw(self, d, t):
        f = font("sans-black", self.size)
        words = self.text.split()
        lines, cur = [], []
        for w in words:
            trial = " ".join(cur + [w])
            if cur and text_w(trial, f) > self.max_width:
                lines.append(cur)
                cur = [w]
            else:
                cur.append(w)
        lines.append(cur)
        space = text_w(" ", f)
        y = self.y + self.dy(t)
        underline_p = ease_in_out(progress(t, self.start + 0.35, 0.45))
        for line in lines:
            total = sum(text_w(w, f) for w in line) + space * (len(line) - 1)
            x = (W - total) / 2
            for w in line:
                ww = text_w(w, f)
                hl = w.strip(".,:?!") in self.highlight
                if hl and underline_p > 0:
                    uy = y + self.size * 0.98
                    d.rounded_rectangle([x, uy, x + ww * underline_p, uy + 14],
                                        radius=7, fill=COLORS["accent"])
                d.text((x, y), w, font=f,
                       fill=COLORS["primary" if hl else "ink"])
                x += ww + space
            y += self.size * 1.18


@dataclass
class Pill(Element):
    """Small rounded tag, e.g. episode number or topic."""
    text: str = ""
    y: float = 260
    size: int = 34
    color: str = "primary"
    soft: str = "primary_soft"

    def draw(self, d, t):
        f = font("sans-bold", self.size)
        tw = text_w(self.text, f)
        padx, pady = 28, 14
        x0 = (W - tw) / 2 - padx
        y0 = self.y + self.dy(t)
        d.rounded_rectangle([x0, y0, x0 + tw + 2 * padx, y0 + self.size + 2 * pady],
                            radius=(self.size + 2 * pady) // 2, fill=COLORS[self.soft])
        d.text((x0 + padx, y0 + pady - 2), self.text, font=f, fill=COLORS[self.color])


# ---------------------------------------------------------------------------
# Code block with typewriter effect and light-theme syntax highlighting.
# ---------------------------------------------------------------------------

PY_KEYWORDS = {
    "def", "return", "for", "in", "if", "else", "elif", "while", "import", "from",
    "as", "class", "None", "True", "False", "and", "or", "not", "is", "lambda",
    "try", "except", "with", "yield", "pass", "break", "continue",
}
PY_BUILTINS = {"print", "len", "range", "list", "dict", "set", "tuple", "sorted",
               "append", "pop", "insert", "array", "enumerate", "zip"}
TOKEN_RE = re.compile(
    r"(#.*)|('[^']*'|\"[^\"]*\")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+)|(.)")


def highlight_py(line: str):
    """Yield (text, colour_key) pairs."""
    for m in TOKEN_RE.finditer(line):
        com, s, num, ident, ws, other = m.groups()
        if com:
            yield com, "com"
        elif s:
            yield s, "str"
        elif num:
            yield num, "num"
        elif ident:
            yield ident, ("kw" if ident in PY_KEYWORDS
                          else "fn" if ident in PY_BUILTINS else "ink")
        else:
            yield (ws or other), "ink"


@dataclass
class CodeLine:
    text: str
    at: float               # when typing starts
    kind: str = "code"      # code | out | err
    cps: float = 28         # characters per second while typing
    focus: tuple[float, float] | None = None  # time window to emphasise this line


@dataclass
class CodeBlock(Element):
    lines: list[CodeLine] = field(default_factory=list)
    x: float = SAFE_LEFT
    y: float = 900
    width: float = SAFE_RIGHT - SAFE_LEFT
    size: int = 42
    line_gap: float = 1.55
    show_prompt: bool = True  # draw ">>>" for code lines (REPL style)

    def draw(self, d, t):
        f = font("mono", self.size)
        fb = font("mono-bold", self.size)
        lh = self.size * self.line_gap
        pad = 40
        y0 = self.y + self.dy(t)
        shown = [ln for ln in self.lines if t >= ln.at]
        h = pad * 2 + max(1, len(shown)) * lh - (lh - self.size * 1.2)
        # card grows smoothly as lines are added
        d.rounded_rectangle([self.x, y0, self.x + self.width, y0 + h],
                            radius=28, fill=COLORS["card"])
        # three "window" dots — a generic editor hint, not a specific brand
        for i, c in enumerate(("line", "line", "line")):
            d.ellipse([self.x + self.width - 120 + i * 30, y0 + 22,
                       self.x + self.width - 104 + i * 30, y0 + 38], fill=COLORS[c])
        y = y0 + pad
        prompt = ">>> " if self.show_prompt else ""
        for ln in shown:
            n_chars = len(ln.text) if ln.kind != "code" else int((t - ln.at) * ln.cps)
            visible = ln.text[:n_chars]
            if ln.focus and ln.focus[0] <= t < ln.focus[1]:
                p = ease_out_cubic(progress(t, ln.focus[0], 0.25))
                d.rounded_rectangle([self.x + 14, y - 10,
                                     self.x + 14 + (self.width - 28) * p, y + self.size * 1.2],
                                    radius=12, fill=COLORS["primary_soft"])
            x = self.x + pad
            if ln.kind == "code":
                if prompt:
                    d.text((x, y), prompt, font=f, fill=COLORS["com"])
                    x += text_w(prompt, f)
                for tok, ck in highlight_py(visible):
                    d.text((x, y), tok, font=f, fill=COLORS[ck])
                    x += text_w(tok, f)
                typing = n_chars < len(ln.text)
                if typing or (t - ln.at) < len(ln.text) / ln.cps + 0.6:
                    if int(t * 2.5) % 2 == 0 or typing:  # blinking caret
                        d.rectangle([x + 2, y + 4, x + 6, y + self.size * 1.1],
                                    fill=COLORS["primary"])
            else:
                # outputs pop in with a quick fade toward their colour
                p = ease_out_cubic(progress(t, ln.at, 0.3))
                col = COLORS["good"] if ln.kind == "out" else COLORS["bad"]
                d.text((x, y), visible, font=fb, fill=mix(COLORS["card"], col, p))
            y += lh


# ---------------------------------------------------------------------------
# Array / list visualisation
# ---------------------------------------------------------------------------

@dataclass
class Highlight:
    index: int
    start: float
    end: float
    style: str = "primary"  # primary | accent | bad


@dataclass
class ArrayRow(Element):
    values: list = field(default_factory=list)
    y: float = 620
    cell: int = 150
    gap: int = 14
    stagger: float = 0.12        # delay between cells popping in
    pos_index_at: float | None = None   # when to reveal 0..n-1 labels
    neg_index_at: float | None = None   # when to reveal -n..-1 labels
    highlights: list[Highlight] = field(default_factory=list)
    ghost: tuple[int, float, float] | None = None  # (index, start, end) dashed "missing" cell

    def cell_x(self, i):
        n = len(self.values)
        total = n * self.cell + (n - 1) * self.gap
        return (W - total) / 2 + i * (self.cell + self.gap)

    def draw(self, d, t):
        fv = font("sans-bold", int(self.cell * 0.36))
        fi = font("mono-bold", 34)
        n = len(self.values)
        y0 = self.y
        for i, v in enumerate(self.values):
            p = progress(t, self.start + i * self.stagger, 0.4)
            if p <= 0:
                continue
            s = ease_out_back(p)
            x = self.cell_x(i)
            cx, cy = x + self.cell / 2, y0 + self.cell / 2
            half = self.cell / 2 * s
            fill, border, txt = COLORS["bg"], COLORS["line"], COLORS["ink"]
            lift = 0
            for hl in self.highlights:
                if hl.index == i and hl.start <= t < hl.end:
                    hp = ease_out_cubic(progress(t, hl.start, 0.25))
                    soft = {"primary": "primary_soft", "accent": "accent_soft",
                            "bad": "bad_soft"}[hl.style]
                    fill = mix(COLORS["bg"], COLORS[soft], hp)
                    border = mix(COLORS["line"], COLORS[hl.style], hp)
                    txt = mix(COLORS["ink"], COLORS[hl.style], hp)
                    lift = -18 * hp
            d.rounded_rectangle([cx - half, cy - half + lift, cx + half, cy + half + lift],
                                radius=int(22 * s), fill=fill, outline=border, width=5)
            if s > 0.6:
                d.text((cx, cy + lift), str(v), font=fv, fill=txt, anchor="mm")
            # index labels
            if self.pos_index_at is not None:
                ip = ease_out_cubic(progress(t, self.pos_index_at + i * 0.08, 0.3))
                if ip > 0:
                    d.text((cx, y0 - 30 - 12 * (1 - ip)), str(i), font=fi,
                           fill=mix(COLORS["bg"], COLORS["primary"], ip), anchor="ms")
            if self.neg_index_at is not None:
                ip = ease_out_cubic(progress(t, self.neg_index_at + (n - 1 - i) * 0.08, 0.3))
                if ip > 0:
                    d.text((cx, y0 + self.cell + 62 + 12 * (1 - ip)), str(i - n), font=fi,
                           fill=mix(COLORS["bg"], COLORS["accent"], ip), anchor="ms")
        if self.ghost:
            gi, gs, ge = self.ghost
            if gs <= t < ge:
                gp = ease_out_cubic(progress(t, gs, 0.3))
                # shake left/right to signal "not allowed"
                shake = math.sin((t - gs) * 40) * 10 * (1 - progress(t, gs, 0.6))
                x = self.cell_x(gi) + shake
                col = mix(COLORS["bg"], COLORS["bad"], gp)
                _dashed_rect(d, x, y0, x + self.cell, y0 + self.cell, col, width=5)
                d.text((x + self.cell / 2, y0 + self.cell / 2), "?", font=fv,
                       fill=col, anchor="mm")
                d.text((x + self.cell / 2, y0 - 30), str(gi), font=fi, fill=col, anchor="ms")


def _dashed_rect(d, x0, y0, x1, y1, col, width=4, dash=18):
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1),
                             (x1, y1, x0, y1), (x0, y1, x0, y0)):
        length = math.hypot(bx - ax, by - ay)
        steps = int(length // (dash * 2)) + 1
        for k in range(steps):
            s0 = k * 2 * dash / length
            s1 = min(1, (k * 2 * dash + dash) / length)
            d.line([ax + (bx - ax) * s0, ay + (by - ay) * s0,
                    ax + (bx - ax) * s1, ay + (by - ay) * s1], fill=col, width=width)


@dataclass
class Pointer(Element):
    """Down-pointing arrow + label that glides between array cells."""
    row: ArrayRow | None = None
    moves: list[tuple[float, int]] = field(default_factory=list)  # (time, index)
    label: str = ""
    color: str = "primary"

    def draw(self, d, t):
        idx_x = None
        for k, (mt, mi) in enumerate(self.moves):
            target = self.row.cell_x(mi) + self.row.cell / 2
            if idx_x is None:
                idx_x = target
            elif t >= mt:
                prev = idx_x
                idx_x = prev + (target - prev) * ease_in_out(progress(t, mt, 0.4))
        bob = math.sin(t * 5) * 5
        y = self.row.y - 150 + bob + self.dy(t)
        col = COLORS[self.color]
        d.polygon([(idx_x - 22, y + 40), (idx_x + 22, y + 40), (idx_x, y + 72)], fill=col)
        d.rectangle([idx_x - 5, y, idx_x + 5, y + 42], fill=col)
        if self.label:
            d.text((idx_x, y - 12), self.label, font=font("mono-bold", 34),
                   fill=col, anchor="ms")


@dataclass
class Card(Element):
    """Summary / recap card with bullet rows."""
    heading: str = ""
    rows: list[tuple[str, str]] = field(default_factory=list)  # (code, explanation)
    y: float = 560
    row_stagger: float = 0.5

    def draw(self, d, t):
        x0, x1 = SAFE_LEFT, SAFE_RIGHT
        y0 = self.y + self.dy(t)
        h = 130 + len(self.rows) * 150
        d.rounded_rectangle([x0, y0, x1, y0 + h], radius=32,
                            fill=COLORS["bg"], outline=COLORS["line"], width=4)
        d.rounded_rectangle([x0, y0, x0 + 16, y0 + h], radius=8, fill=COLORS["primary"])
        d.text((x0 + 56, y0 + 44), self.heading, font=font("sans-black", 52),
               fill=COLORS["ink"])
        for i, (code, expl) in enumerate(self.rows):
            p = ease_out_cubic(progress(t, self.start + 0.3 + i * self.row_stagger, 0.35))
            if p <= 0:
                continue
            ry = y0 + 140 + i * 150 + (1 - p) * 20
            d.text((x0 + 56, ry), code, font=font("mono-bold", 44),
                   fill=mix(COLORS["bg"], COLORS["primary"], p))
            d.text((x0 + 56, ry + 62), expl, font=font("sans", 36),
                   fill=mix(COLORS["bg"], COLORS["muted"], p))


@dataclass
class Brand(Element):
    """Persistent handle + progress bar at the bottom of the safe area."""
    handle: str = "@yourhandle"
    duration: float = 30
    fade_in: float = 0.0
    slide: int = 0

    def draw(self, d, t):
        y = SAFE_BOTTOM - 10
        d.text((W / 2, y), self.handle, font=font("sans-semibold", 32),
               fill=COLORS["muted"], anchor="ms")
        # thin progress bar — gives viewers a sense of how long is left
        bar_y = 70
        d.rounded_rectangle([SAFE_LEFT, bar_y, SAFE_RIGHT, bar_y + 8], radius=4,
                            fill=COLORS["card"])
        d.rounded_rectangle([SAFE_LEFT, bar_y,
                             SAFE_LEFT + (SAFE_RIGHT - SAFE_LEFT) * clamp(t / self.duration),
                             bar_y + 8], radius=4, fill=COLORS["primary"])


# ---------------------------------------------------------------------------
# Scene + renderer
# ---------------------------------------------------------------------------

class Scene:
    def __init__(self, duration: float, fps: int = FPS, debug_safe_area: bool = False):
        self.duration = duration
        self.fps = fps
        self.elements: list[Element] = []
        self.debug_safe_area = debug_safe_area

    def add(self, *els: Element):
        self.elements.extend(els)
        return els[0] if len(els) == 1 else els

    def frame(self, t: float) -> Image.Image:
        base = Image.new("RGB", (W, H), COLORS["bg"])
        for el in self.elements:
            if not el.visible(t):
                continue
            a = el.alpha(t)
            if a <= 0.01:
                continue
            if a >= 0.99:
                el.draw(ImageDraw.Draw(base), t)
            else:
                # draw on a white copy, then blend — cheap opacity on a white canvas
                layer = base.copy()
                el.draw(ImageDraw.Draw(layer), t)
                base = Image.blend(base, layer, a)
        if self.debug_safe_area:
            d = ImageDraw.Draw(base)
            d.rectangle([SAFE_LEFT, SAFE_TOP, SAFE_RIGHT, SAFE_BOTTOM],
                        outline=(255, 0, 255), width=3)
        return base

    def still(self, t: float, path: str | Path):
        self.frame(t).save(path)

    def render(self, path: str | Path, start: float = 0, end: float | None = None):
        end = self.duration if end is None else end
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-loglevel", "error",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(self.fps), "-i", "-",
               "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        n = int((end - start) * self.fps)
        for k in range(n):
            t = start + k / self.fps
            proc.stdin.write(self.frame(t).tobytes())
            if k % self.fps == 0:
                print(f"\r  rendering {t:5.1f}s / {end:.1f}s", end="", flush=True)
        proc.stdin.close()
        proc.wait()
        print(f"\r  wrote {path} ({n} frames)          ")
