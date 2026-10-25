"""Animated data-structure primitives for reelkit, beyond the static ArrayRow.

ListAnim     a list/array whose contents change over time (append, insert, pop,
             set, extend, reject) with items gliding to their new positions
RowPointer   arrow that follows cells of a ListAnim
Bracket      span marker under a slice, with an optional excluded "stop" cell
Hops         arcs hopping between cells (slice step, iteration)
FlyCells     copies of cells flying from one row into another (slicing → new list)
RefDiagram   slots with arrows to objects elsewhere in memory (references)
Grid         2-D array with row/column labels, cell/row/column highlights
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from reelkit import (COLORS, SAFE_LEFT, SAFE_RIGHT, W, Element, _dashed_rect, clamp,
                     ease_in_out, ease_out_back, ease_out_cubic, font, mix, progress, text_w)

SOFT = {"primary": "primary_soft", "accent": "accent_soft", "bad": "bad_soft",
        "good": "primary_soft"}


def lerp(a, b, p):
    return a + (b - a) * p


def draw_cell(d, cx, cy, cs, text, style=None, strength=1.0, scale=1.0, dim=False,
              square=False, mono=False, font_scale=0.36):
    """One list/array cell. `style` is a highlight colour key, blended by `strength`."""
    if scale <= 0.02:
        return
    half = cs / 2 * scale
    fill, border, txt = COLORS["surface"], COLORS["line"], COLORS["ink"]
    if dim:
        border, txt = mix(COLORS["line"], COLORS["surface"], 0.4), COLORS["line"]
    if style:
        fill = mix(fill, COLORS[SOFT[style]], strength)
        border = mix(border, COLORS[style], strength)
        txt = mix(txt, COLORS[style], strength)
    box = [cx - half, cy - half, cx + half, cy + half]
    if square:
        d.rectangle(box, fill=fill, outline=border, width=4)
    else:
        d.rounded_rectangle(box, radius=int(cs * 0.17 * scale), fill=fill,
                            outline=border, width=5)
    if scale > 0.55:
        text = str(text)
        fs = int(cs * font_scale * min(1, scale))
        f = font("mono-bold" if mono else "sans-bold", fs)
        while text_w(text, f) > cs * 0.86 and fs > 14:  # shrink long values to fit
            fs -= 2
            f = font("mono-bold" if mono else "sans-bold", fs)
        d.text((cx, cy), text, font=f, fill=txt, anchor="mm")


# ---------------------------------------------------------------------------
# ListAnim
# ---------------------------------------------------------------------------

@dataclass
class _Snap:
    t: float
    ids: list
    vals: dict
    changed: set = field(default_factory=set)
    change_style: str = "accent"


class ListAnim(Element):
    """A row of cells whose contents change over time.

        row = ListAnim([10, 20, 30], y=700, start=2.0)
        row.append(5.0, 40)          # new cell drops in at the end
        row.insert(7.0, 0, 5)        # everything glides right, 5 drops in
        row.pop(9.0)                 # last cell flies out
        row.highlight(3, 4, [1], "primary")

    Operations must be added in time order. Cell size shrinks automatically
    when the list grows too wide for the safe area.
    """

    def __init__(self, values, y, start, end=math.inf, cell=130, gap=14,
                 max_width=SAFE_RIGHT - SAFE_LEFT, labels="index", label_at=None,
                 label_color="primary", addr_base=1000, itemsize=4, byte_ticks=False,
                 joined=False, stagger=0.12, pop=True, dur=0.5, mono=False, tag=None,
                 tag_color="muted", x_center=W / 2):
        self.start, self.end = start, end
        self.fade_in, self.fade_out, self.slide = 0.01, 0.25, 0
        self.y, self.cell, self.gap, self.max_width = y, cell, gap, max_width
        self.labels, self.label_at, self.label_color = labels, label_at, label_color
        self.addr_base, self.itemsize, self.byte_ticks = addr_base, itemsize, byte_ticks
        self.joined, self.stagger, self.pop_in, self.dur = joined, stagger, pop, dur
        self.mono, self.x_center = mono, x_center
        self.tags = [(start, tag, tag_color)] if tag else []
        self._next_id = 0
        ids = [self._new_id() for _ in values]
        self.snaps = [_Snap(start, ids, dict(zip(ids, values)))]
        self.highlights = []   # (t0, t1, indices, style, dim)
        self.rejects = []      # (t0, t1, value)

    # ---- building the timeline ----
    def _new_id(self):
        self._next_id += 1
        return self._next_id

    def _push(self, t, ids, vals, changed=(), style="accent"):
        assert t >= self.snaps[-1].t, "ListAnim operations must be added in time order"
        self.snaps.append(_Snap(t, ids, vals, set(changed), style))
        return self

    @property
    def values(self):
        s = self.snaps[-1]
        return [s.vals[i] for i in s.ids]

    def append(self, t, v):
        return self.insert(t, len(self.snaps[-1].ids), v)

    def insert(self, t, i, v):
        s = self.snaps[-1]
        nid = self._new_id()
        ids = s.ids[:i] + [nid] + s.ids[i:]
        return self._push(t, ids, {**s.vals, nid: v})

    def extend(self, t, values):
        s = self.snaps[-1]
        new = [self._new_id() for _ in values]
        return self._push(t, s.ids + new, {**s.vals, **dict(zip(new, values))})

    def pop(self, t, i=-1):
        s = self.snaps[-1]
        ids = list(s.ids)
        ids.pop(i)
        return self._push(t, ids, dict(s.vals))

    def set(self, t, i, v, style="accent"):
        s = self.snaps[-1]
        return self._push(t, list(s.ids), {**s.vals, s.ids[i]: v}, [s.ids[i]], style)

    def set_all(self, t, values, style="accent"):
        s = self.snaps[-1]
        return self._push(t, list(s.ids), {**s.vals, **dict(zip(s.ids, values))},
                          s.ids, style)

    def reset(self, t, values):
        """Replace the contents instantly (cross-fade-free swap to a new list)."""
        ids = [self._new_id() for _ in values]
        snap = _Snap(t, ids, dict(zip(ids, values)))
        snap.instant = True
        self.snaps.append(snap)
        return self

    def highlight(self, t0, t1, indices, style="primary", dim=False):
        self.highlights.append((t0, t1, set(indices), style, dim))
        return self

    def reject(self, t0, t1, value):
        """A dashed red cell tries to join the end and shakes: invalid append."""
        self.rejects.append((t0, t1, value))
        return self

    def retag(self, t, text, color="muted"):
        self.tags.append((t, text, color))
        return self

    # ---- geometry ----
    def _cs(self, n):
        if n == 0:
            return self.cell
        g = 0 if self.joined else self.gap
        return min(self.cell, (self.max_width - g * (n - 1)) / n)

    def _xc(self, n, i):
        cs = self._cs(n)
        g = 0 if self.joined else self.gap
        total = n * cs + (n - 1) * g
        return self.x_center - total / 2 + i * (cs + g) + cs / 2

    def _snap_at(self, t):
        k = 0
        for j, s in enumerate(self.snaps):
            if s.t <= t:
                k = j
        return k

    def center(self, i, t):
        s = self.snaps[self._snap_at(t)]
        n = len(s.ids)
        i = i % n if n and i < 0 else i
        return self._xc(n, i), self.y + self._cs(n) / 2

    def cell_size(self, t):
        return self._cs(len(self.snaps[self._snap_at(t)].ids))

    # ---- drawing ----
    def draw(self, d, t):
        k = self._snap_at(t)
        cur = self.snaps[k]
        prev = self.snaps[k - 1] if k > 0 and not getattr(cur, "instant", False) else None
        p = ease_in_out(progress(t, cur.t, self.dur)) if prev else 1.0
        n, pn = len(cur.ids), len(prev.ids) if prev else 0
        cs = lerp(self._cs(pn), self._cs(n), p) if prev else self._cs(n)

        hl = {}
        dim_on = False
        for t0, t1, idx, style, dim in self.highlights:
            if t0 <= t < t1:
                strength = ease_out_cubic(progress(t, t0, 0.25))
                for i in idx:
                    hl[i % n if n else i] = (style, strength)
                dim_on = dim_on or dim

        # tag (e.g. "list" / "np.array") above the row, left aligned
        tag = None
        for tt, text, color in self.tags:
            if tt <= t:
                tag = (tt, text, color)
        if tag and n:
            tp = ease_out_cubic(progress(t, tag[0], 0.3))
            left = self._xc(n, 0) - cs / 2
            ty = self.y - (118 if self.labels == "index" else 60)
            f = font("mono-bold", 30)
            tw = text_w(tag[1], f)
            d.rounded_rectangle([left, ty, left + tw + 32, ty + 46], radius=12,
                                fill=mix(COLORS["bg"], COLORS["card"], tp))
            d.text((left + 16, ty + 7), tag[1], font=f,
                   fill=mix(COLORS["bg"], COLORS[tag[2]], tp))

        # items leaving (fly up and shrink)
        if prev:
            for j, iid in enumerate(prev.ids):
                if iid in cur.vals and iid in cur.ids:
                    continue
                q = progress(t, cur.t, self.dur)
                x = self._xc(pn, j)
                cy = self.y + cs / 2 - ease_in_out(q) * 110
                draw_cell(d, x, cy, cs, prev.vals[iid], "bad", 1.0, 1 - q, mono=self.mono)

        for i, iid in enumerate(cur.ids):
            x_cur = self._xc(n, i)
            scale, dy = 1.0, 0.0
            if prev and iid in prev.ids:
                x = lerp(self._xc(pn, prev.ids.index(iid)), x_cur, p)
            elif prev:  # inserted: drop in from above
                q = progress(t, cur.t, self.dur)
                x, scale = x_cur, ease_out_back(q)
                dy = -(1 - ease_out_cubic(q)) * 90
            else:  # initial build
                q = progress(t, cur.t + i * self.stagger, 0.4)
                if q <= 0:
                    continue
                x = x_cur
                scale = ease_out_back(q) if self.pop_in else 1.0
            style, strength = hl.get(i, (None, 0))
            if iid in cur.changed:
                f_ = progress(t, cur.t, 0.9)
                if not style:
                    style, strength = cur.change_style, 1 - ease_in_out(clamp((f_ - 0.4) / 0.6))
                scale *= 1 + 0.14 * math.sin(math.pi * clamp(f_ / 0.45))
            dim = dim_on and i not in hl
            lift = -16 * strength if style and i in hl else 0
            cy = self.y + cs / 2 + dy + lift
            draw_cell(d, x, cy, cs, cur.vals[iid], style, strength, scale, dim,
                      square=self.joined, mono=self.mono)
            if self.byte_ticks and scale > 0.9:
                for b in range(1, self.itemsize):
                    bx = x - cs / 2 + cs * b / self.itemsize
                    d.line([bx, self.y + cs - 18, bx, self.y + cs - 4],
                           fill=COLORS["line"], width=3)
            self._draw_label(d, t, i, x, cs, n)

        for t0, t1, value in self.rejects:
            if t0 <= t < t1:
                q = ease_out_cubic(progress(t, t0, 0.3))
                shake = math.sin((t - t0) * 40) * 12 * (1 - progress(t, t0, 0.7))
                x = self._xc(n, n) + shake if not self.joined else \
                    self._xc(n, n - 1) + cs + shake
                col = mix(COLORS["bg"], COLORS["bad"], q)
                _dashed_rect(d, x - cs / 2, self.y, x + cs / 2, self.y + cs, col, width=5)
                f = font("sans-bold", int(cs * 0.3))
                d.text((x, self.y + cs / 2), str(value), font=f, fill=col, anchor="mm")

    def _draw_label(self, d, t, i, x, cs, n):
        if not self.labels:
            return
        at = self.start if self.label_at is None else self.label_at
        q = ease_out_cubic(progress(t, at + i * 0.06, 0.3))
        if q <= 0:
            return
        if self.labels == "index":
            d.text((x, self.y - 26 - 10 * (1 - q)), str(i), font=font("mono-bold", 32),
                   fill=mix(COLORS["bg"], COLORS[self.label_color], q), anchor="ms")
        elif self.labels == "address":
            d.text((x, self.y + cs + 44 + 10 * (1 - q)),
                   str(self.addr_base + i * self.itemsize), font=font("mono-bold", 26),
                   fill=mix(COLORS["bg"], COLORS["muted"], q), anchor="ms")


# ---------------------------------------------------------------------------
# Markers on top of a ListAnim
# ---------------------------------------------------------------------------

@dataclass
class RowPointer(Element):
    """Arrow above a ListAnim cell. moves: [(time, index, label)]"""
    row: ListAnim | None = None
    moves: list = field(default_factory=list)
    color: str = "primary"
    move_dur: float = 0.35

    def draw(self, d, t):
        x, label = None, ""
        for mt, mi, ml in self.moves:
            target = self.row.center(mi, t)[0]
            if x is None:
                x, label = target, ml
            elif t >= mt:
                x = lerp(x, target, ease_in_out(progress(t, mt, self.move_dur)))
                label = ml
        y = self.row.y - 150 + math.sin(t * 5) * 5 + self.dy(t)
        col = COLORS[self.color]
        d.polygon([(x - 22, y + 40), (x + 22, y + 40), (x, y + 72)], fill=col)
        d.rectangle([x - 5, y, x + 5, y + 42], fill=col)
        if label:
            d.text((x, y - 12), label, font=font("mono-bold", 34), fill=col, anchor="ms")


@dataclass
class Bracket(Element):
    """Square bracket under cells i0..i1 (inclusive), label underneath.
    `excluded` marks a cell with a dashed red outline (the slice's stop index)."""
    row: ListAnim | None = None
    i0: int = 0
    i1: int = 0
    text: str = ""
    color: str = "primary"
    excluded: int | None = None

    def draw(self, d, t):
        cs = self.row.cell_size(t)
        x0 = self.row.center(self.i0, t)[0] - cs / 2
        x1 = self.row.center(self.i1, t)[0] + cs / 2
        y = self.row.y + cs + 26 + self.dy(t)
        p = ease_out_cubic(progress(t, self.start, 0.45))
        mid = (x0 + x1) / 2
        col = COLORS[self.color]
        a, b = lerp(mid, x0, p), lerp(mid, x1, p)
        d.line([a, y + 18, b, y + 18], fill=col, width=6)
        d.line([a, y, a, y + 18], fill=col, width=6)
        d.line([b, y, b, y + 18], fill=col, width=6)
        if self.text:
            d.text((mid, y + 70), self.text, font=font("mono-bold", 34),
                   fill=mix(COLORS["bg"], col, p), anchor="ms")
        if self.excluded is not None:
            ex = self.row.center(self.excluded, t)[0]
            q = ease_out_cubic(progress(t, self.start + 0.4, 0.3))
            _dashed_rect(d, ex - cs / 2 - 8, self.row.y - 8, ex + cs / 2 + 8,
                         self.row.y + cs + 8, mix(COLORS["bg"], COLORS["bad"], q), width=4)


@dataclass
class Hops(Element):
    """Arcs hopping across cells in order — shows a step or an iteration path."""
    row: ListAnim | None = None
    indices: list = field(default_factory=list)
    hop_dur: float = 0.35
    color: str = "accent"
    text: str = ""

    def draw(self, d, t):
        col = COLORS[self.color]
        cs = self.row.cell_size(t)
        top = self.row.y - 56
        for k in range(len(self.indices) - 1):
            p = progress(t, self.start + k * self.hop_dur, self.hop_dur)
            if p <= 0:
                continue
            xa = self.row.center(self.indices[k], t)[0]
            xb = self.row.center(self.indices[k + 1], t)[0]
            span = abs(xb - xa)
            h = min(72, span * 0.3)
            box = [min(xa, xb), top - h, max(xa, xb), top + h]
            # arc grows in the direction of travel
            if xb >= xa:
                d.arc(box, 180, 180 + 180 * ease_in_out(p), fill=col, width=6)
            else:
                d.arc(box, 360 - 180 * ease_in_out(p), 360, fill=col, width=6)
            if p >= 1:
                d.polygon([(xb - 12, top - 14), (xb + 12, top - 14), (xb, top + 6)], fill=col)
        if self.text:
            q = ease_out_cubic(progress(t, self.start, 0.3))
            d.text((W / 2, top - 130), self.text, font=font("mono-bold", 34),
                   fill=mix(COLORS["bg"], col, q), anchor="ms")


@dataclass
class FlyCells(Element):
    """Copies of src cells fly into dst row positions (dst should start, without
    pop, at `start + dur` with the same stagger)."""
    src: ListAnim | None = None
    src_indices: list = field(default_factory=list)
    dst: ListAnim | None = None
    stagger: float = 0.12
    dur: float = 0.5
    style: str = "primary"
    fade_in: float = 0.01
    slide: int = 0

    def draw(self, d, t):
        src_vals = self.src.values if self.src.snaps[-1].t <= self.start else \
            [self.src.snaps[self.src._snap_at(self.start)].vals[i]
             for i in self.src.snaps[self.src._snap_at(self.start)].ids]
        cs0 = self.src.cell_size(self.start)
        cs1 = self.dst.cell_size(self.dst.start)
        for k, si in enumerate(self.src_indices):
            tk = self.start + k * self.stagger
            q = progress(t, tk, self.dur)
            if q <= 0 or q >= 1:
                continue
            e = ease_in_out(q)
            x0, y0 = self.src.center(si, self.start)
            x1, y1 = self.dst.center(k, self.dst.start)
            # slight arc so cells don't slide flat over each other
            x, y = lerp(x0, x1, e), lerp(y0, y1, e) - math.sin(math.pi * e) * 40
            draw_cell(d, x, y, lerp(cs0, cs1, e), src_vals[si], self.style, 1.0,
                      mono=self.src.mono)


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------

@dataclass
class RefDiagram(Element):
    """Slots holding arrows to objects stored elsewhere.

    slots:   [(x, y, label)]               small boxes that hold a reference
    objects: [(x, y, text, type_label)]    boxes in "memory"
    links:   [(slot_index, object_index)]
    """
    slots: list = field(default_factory=list)
    objects: list = field(default_factory=list)
    links: list = field(default_factory=list)
    slot_size: int = 96
    link_stagger: float = 0.35
    links_at: float | None = None
    memory_box: tuple | None = None   # (x0, y0, x1, y1, label)
    link_style: dict = field(default_factory=dict)  # link index -> colour key

    def draw(self, d, t):
        ss = self.slot_size
        la = self.start + 0.5 if self.links_at is None else self.links_at
        if self.memory_box:
            x0, y0, x1, y1, label = self.memory_box
            q = ease_out_cubic(progress(t, la - 0.2, 0.4))
            if q > 0:
                _dashed_rect(d, x0, y0, x1, y1, mix(COLORS["bg"], COLORS["line"], q), width=3)
                d.text((x0 + 20, y0 + 16), label, font=font("sans-semibold", 28),
                       fill=mix(COLORS["bg"], COLORS["muted"], q))
        for i, (x, y, label) in enumerate(self.slots):
            q = progress(t, self.start + i * 0.1, 0.4)
            if q <= 0:
                continue
            s = ease_out_back(q)
            d.rounded_rectangle([x - ss / 2 * s, y - ss / 2 * s, x + ss / 2 * s, y + ss / 2 * s],
                                radius=int(16 * s), fill=COLORS["surface"], outline=COLORS["line"],
                                width=5)
            d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=COLORS["ink"])
            if label:
                d.text((x, y - ss / 2 - 18), label, font=font("mono-bold", 30),
                       fill=COLORS["primary"], anchor="ms")
        obj_shown = set()
        for k, (si, oi) in enumerate(self.links):
            p = ease_in_out(progress(t, la + k * self.link_stagger, 0.4))
            if p <= 0:
                continue
            sx, sy = self.slots[si][0], self.slots[si][1]
            ox, oy, otext, _ = self.objects[oi]
            ow, oh = self._obj_size(otext)
            # aim at the nearest edge of the object box
            tx, ty = ox, oy - oh / 2 if oy > sy else oy + oh / 2
            if abs(oy - sy) < oh:
                tx, ty = (ox - ow / 2, oy) if ox > sx else (ox + ow / 2, oy)
            ex, ey = lerp(sx, tx, p), lerp(sy, ty, p)
            col = COLORS[self.link_style.get(k, "ink")]
            d.line([sx, sy, ex, ey], fill=col, width=5)
            ang = math.atan2(ey - sy, ex - sx)
            if p > 0.2:
                hx, hy = ex, ey
                d.polygon([(hx, hy),
                           (hx - 24 * math.cos(ang - 0.45), hy - 24 * math.sin(ang - 0.45)),
                           (hx - 24 * math.cos(ang + 0.45), hy - 24 * math.sin(ang + 0.45))],
                          fill=col)
            if p >= 0.85:
                obj_shown.add(oi)
        for oi, (ox, oy, otext, otype) in enumerate(self.objects):
            if oi not in obj_shown:
                continue
            first = min(k for k, (_, o) in enumerate(self.links) if o == oi)
            q = progress(t, la + first * self.link_stagger + 0.34, 0.35)
            s = ease_out_back(q)
            ow, oh = self._obj_size(otext)
            d.rounded_rectangle([ox - ow / 2 * s, oy - oh / 2 * s, ox + ow / 2 * s, oy + oh / 2 * s],
                                radius=18, fill=COLORS["accent_soft"], outline=COLORS["accent"],
                                width=4)
            if s > 0.6:
                d.text((ox, oy), otext, font=font("mono-bold", 38), fill=COLORS["ink"],
                       anchor="mm")
                if otype:
                    d.text((ox, oy - oh / 2 - 12), otype, font=font("sans-semibold", 26),
                           fill=COLORS["muted"], anchor="ms")

    @staticmethod
    def _obj_size(text):
        return max(110, text_w(text, font("mono-bold", 38)) + 44), 80


# ---------------------------------------------------------------------------
# 2-D grid
# ---------------------------------------------------------------------------

class Grid(Element):
    """rows × cols cells with index labels. highlight() a cell, row or column
    (pass r or c as None for a whole column / row); set() changes cells."""

    def __init__(self, values, y, start, end=math.inf, cell=120, gap=12,
                 labels_at=None, stagger=0.06, x_center=W / 2):
        self.start, self.end = start, end
        self.fade_in, self.fade_out, self.slide = 0.01, 0.25, 0
        self.values = [list(r) for r in values]
        self.y, self.cell, self.gap, self.labels_at = y, cell, gap, labels_at
        self.stagger, self.x_center = stagger, x_center
        self.highlights = []  # (t0, t1, r, c, style)
        self.changes = []     # (t, {(r, c): v}, style)

    def highlight(self, t0, t1, r=None, c=None, style="primary"):
        self.highlights.append((t0, t1, r, c, style))
        return self

    def set(self, t, cells: dict, style="bad"):
        self.changes.append((t, cells, style))
        return self

    def center(self, r, c):
        rows, cols = len(self.values), len(self.values[0])
        step = self.cell + self.gap
        x0 = self.x_center - (cols * step - self.gap) / 2
        return x0 + c * step + self.cell / 2, self.y + r * step + self.cell / 2

    def draw(self, d, t):
        rows, cols = len(self.values), len(self.values[0])
        vals = [list(r) for r in self.values]
        flash = {}
        for ct, cells, style in self.changes:
            if t >= ct:
                for (r, c), v in cells.items():
                    vals[r][c] = v
                    f_ = progress(t, ct, 1.2)
                    flash[(r, c)] = (style, 1 - ease_in_out(clamp((f_ - 0.5) / 0.5)), f_)
        for r in range(rows):
            for c in range(cols):
                q = progress(t, self.start + (r * cols + c) * self.stagger, 0.4)
                if q <= 0:
                    continue
                cx, cy = self.center(r, c)
                style, strength, scale = None, 0.0, ease_out_back(q)
                for t0, t1, hr, hc, hs in self.highlights:
                    if t0 <= t < t1 and (hr is None or hr == r) and (hc is None or hc == c):
                        style, strength = hs, ease_out_cubic(progress(t, t0, 0.25))
                if (r, c) in flash:
                    fs, fstr, f_ = flash[(r, c)]
                    if not style:
                        style, strength = fs, fstr
                    scale *= 1 + 0.14 * math.sin(math.pi * clamp(f_ / 0.4))
                draw_cell(d, cx, cy, self.cell, vals[r][c], style, strength, scale)
        if self.labels_at is not None:
            q = ease_out_cubic(progress(t, self.labels_at, 0.35))
            if q > 0:
                f = font("mono-bold", 32)
                for c in range(cols):
                    cx, cy = self.center(0, c)
                    d.text((cx, cy - self.cell / 2 - 24), str(c), font=f,
                           fill=mix(COLORS["bg"], COLORS["accent"], q), anchor="ms")
                for r in range(rows):
                    cx, cy = self.center(r, 0)
                    d.text((cx - self.cell / 2 - 34, cy), str(r), font=f,
                           fill=mix(COLORS["bg"], COLORS["primary"], q), anchor="mm")


# ---------------------------------------------------------------------------
# Intro / overview primitives
# ---------------------------------------------------------------------------

@dataclass
class Gather(Element):
    """Values scattered across the screen fly into a ListAnim's cells
    (dst should start, without pop, at `start + dur` with the same stagger)."""
    values: list = field(default_factory=list)
    origins: list = field(default_factory=list)  # [(x, y)] scattered positions
    dst: ListAnim | None = None
    gather_at: float = 0.0
    stagger: float = 0.1
    dur: float = 0.6
    fade_in: float = 0.01
    slide: int = 0

    def draw(self, d, t):
        cs = self.dst.cell_size(self.dst.start)
        for k, (v, (ox, oy)) in enumerate(zip(self.values, self.origins)):
            appear = progress(t, self.start + k * 0.08, 0.35)
            if appear <= 0:
                continue
            tk = self.gather_at + k * self.stagger
            q = ease_in_out(progress(t, tk, self.dur))
            if q >= 1:
                continue
            x1, y1 = self.dst.center(k, self.dst.start)
            wob = math.sin(t * 3 + k) * 8 * (1 - q)  # idle drift while scattered
            draw_cell(d, lerp(ox, x1, q), lerp(oy, y1, q) + wob, cs, v,
                      scale=ease_out_back(appear), mono=self.dst.mono)


@dataclass
class NodeGraph(Element):
    """Circles joined by lines: trees and graphs. nodes: [(x, y, label)],
    edges: [(i, j)]. Nodes pop in staggered; each edge draws once both ends exist."""
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    radius: int = 34
    stagger: float = 0.1
    highlight: dict = field(default_factory=dict)  # node index -> colour key
    fade_in: float = 0.01
    slide: int = 0

    def _node_t(self, i):
        return self.start + i * self.stagger

    def draw(self, d, t):
        for i, j in self.edges:
            te = max(self._node_t(i), self._node_t(j)) + 0.2
            p = ease_in_out(progress(t, te, 0.35))
            if p <= 0:
                continue
            (x0, y0, _), (x1, y1, _) = self.nodes[i], self.nodes[j]
            d.line([x0, y0, lerp(x0, x1, p), lerp(y0, y1, p)], fill=COLORS["line"], width=5)
        f = font("sans-bold", int(self.radius * 0.9))
        for i, (x, y, label) in enumerate(self.nodes):
            q = progress(t, self._node_t(i), 0.35)
            if q <= 0:
                continue
            r = self.radius * ease_out_back(q)
            style = self.highlight.get(i)
            fill = COLORS[SOFT[style]] if style else COLORS["surface"]
            border = COLORS[style] if style else COLORS["line"]
            d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=border, width=5)
            if label and q > 0.6:
                d.text((x, y), str(label), font=f,
                       fill=COLORS[style] if style else COLORS["ink"], anchor="mm")


@dataclass
class Chips(Element):
    """Topic tags that wrap across lines and pop in one by one (a roadmap)."""
    labels: list = field(default_factory=list)
    y: float = 560
    stagger: float = 0.15
    size: int = 38
    highlight: dict = field(default_factory=dict)  # label index -> colour key
    fade_in: float = 0.01
    slide: int = 0

    def _layout(self):
        f = font("sans-bold", self.size)
        padx, gap, row_h = 26, 16, self.size + 52
        rows, cur, cur_w = [], [], 0
        for i, lab in enumerate(self.labels):
            w = text_w(lab, f) + 2 * padx
            if cur and cur_w + gap + w > SAFE_RIGHT - SAFE_LEFT:
                rows.append((cur, cur_w))
                cur, cur_w = [], 0
            cur_w += (gap if cur else 0) + w
            cur.append((i, lab, w))
        if cur:
            rows.append((cur, cur_w))
        out = []
        for r, (items, total) in enumerate(rows):
            x = (W - total) / 2
            for i, lab, w in items:
                out.append((i, lab, x, self.y + r * row_h, w))
                x += w + gap
        return out, f

    def draw(self, d, t):
        items, f = self._layout()
        h = self.size + 32
        for i, lab, x, y, w in items:
            q = progress(t, self.start + i * self.stagger, 0.35)
            if q <= 0:
                continue
            s = ease_out_back(q)
            style = self.highlight.get(i)
            fill = COLORS[SOFT[style]] if style else COLORS["surface"]
            border = COLORS[style] if style else COLORS["line"]
            cx, cy = x + w / 2, y + h / 2
            d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s],
                                radius=int(h / 2 * s), fill=fill, outline=border, width=4)
            if s > 0.7:
                d.text((cx, cy), lab, font=f,
                       fill=COLORS[style] if style else COLORS["ink"], anchor="mm")


@dataclass
class CompareBars(Element):
    """Horizontal bars growing to compare sizes. rows: [(label, value_text, fraction, colour)]."""
    rows: list = field(default_factory=list)
    y: float = 600
    row_gap: float = 190
    row_stagger: float = 1.0
    grow: float = 1.2

    def draw(self, d, t):
        x0, full = SAFE_LEFT, SAFE_RIGHT - SAFE_LEFT
        for k, (label, value, frac, col) in enumerate(self.rows):
            ts = self.start + k * self.row_stagger
            q = progress(t, ts, 0.3)
            if q <= 0:
                continue
            y = self.y + k * self.row_gap + self.dy(t)
            d.text((x0, y), label, font=font("sans-bold", 40),
                   fill=mix(COLORS["bg"], COLORS["ink"], ease_out_cubic(q)))
            p = ease_out_cubic(progress(t, ts + 0.2, self.grow))
            bw = max(14, full * frac * p)  # a sliver stays visible for tiny values
            d.rounded_rectangle([x0, y + 62, x0 + full, y + 110], radius=24, fill=COLORS["card"])
            d.rounded_rectangle([x0, y + 62, x0 + bw, y + 110], radius=24, fill=COLORS[col])
            if p > 0.05:
                d.text((x0, y + 128), value, font=font("mono-bold", 38),
                       fill=mix(COLORS["bg"], COLORS[col], min(1, p * 2)))
