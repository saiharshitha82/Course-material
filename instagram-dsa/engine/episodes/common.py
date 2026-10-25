"""Shared scaffolding for episodes: hook, section header, headlines, recap, CTA, render."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import Brand, Card, Pill, Scene, Text, Title  # noqa: E402
from voice import Narration  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "renders"
HANDLE = "@codenest"
SERIES = "DSA in Python"


def new_episode(nar: Narration, tail: float = 0.8):
    """Lay out the narration and create the scene sized to it."""
    duration = round(nar.layout(lead_in=0.4) + tail, 1)
    scene = Scene(duration)
    scene.add(Brand(handle=HANDLE))
    return scene, nar.beats


def hook(scene, B, number, title, highlight=(), sub=None, next_beat="setup", size=92):
    end = B[next_beat].start - 0.15
    scene.add(Pill(text=f"{SERIES}  ·  #{number:02}", y=280, start=0.0, end=end))
    scene.add(Title(text=title, y=420, size=size, highlight=highlight, start=0.15, end=end))
    if sub:
        hb = B["hook"]
        scene.add(Text(text=sub, y=820, size=44, color="muted",
                       start=hb.at(len(hb.sentences) - 1), end=end))


def header(scene, text, start, end):
    scene.add(Text(text=text, y=290, size=50, weight="sans-black", start=start, end=end))


def headlines(scene, items, y=420):
    """items: [(text, start, end, colour)] — one-line 'what is happening now'."""
    for txt, s, e, col in items:
        scene.add(Text(text=txt, y=y, size=50, weight="sans-bold", color=col,
                       start=s, end=e, fade_out=0.15))


def recap(scene, B, rows, y=420):
    """Recap card; rows appear spread across the recap beat's sentences."""
    rc = B["recap"]
    n = len(rows)
    stagger = (rc.end - rc.start - 0.6) / max(1, n - 1) if n > 1 else 0.5
    scene.add(Card(heading="Recap", y=y, start=rc.start - 0.3, end=B["cta"].start - 0.2,
                   row_stagger=min(stagger, 1.4), rows=rows))


def cta(scene, B, title, highlight=()):
    cs = B["cta"].start
    scene.add(Pill(text="Next episode", y=560, start=cs - 0.1, color="accent", soft="accent_soft"))
    scene.add(Title(text=title, y=660, size=84, highlight=highlight, start=cs))
    scene.add(Text(text="Follow so you don't miss it", y=900, size=44, color="muted",
                   start=B["cta"].at(len(B["cta"].sentences) - 1)))


def finish(scene, nar, name, stills):
    """Add captions, then render (or write stills with --stills).
    stills: [(beat_name, seconds_after_beat_start)]"""
    scene.add(nar.subtitles())
    OUT.mkdir(exist_ok=True)
    B = nar.beats
    print(f"{name}: {scene.duration}s;",
          ", ".join(f"{b.name} {b.start:.1f}-{b.end:.1f}" for b in B.values()))
    if "--stills" in sys.argv:
        for beat, dt in stills:
            scene.still(B[beat].start + dt, OUT / f"{name}_{beat}.png")
    else:
        wav = nar.write_wav(OUT / f"{name}.wav", scene.duration)
        nar.write_srt(OUT / f"{name}.srt")
        scene.render(OUT / f"{name}.mp4", audio=wav)
