"""Voice-over + burned-in captions for reelkit.

The narration drives the timeline: each beat is synthesised first, and the
visuals are scheduled against the real start/end of what is being said.

    nar = Narration()
    nar.beat("hook", "Python list indexing in 30 seconds.",
             ("nums[2] is 30.", "nums of two is thirty."))   # (shown, spoken)
    nar.layout(lead_in=0.4)
    nar["hook"].start, nar["hook"].end, nar["hook"].sentences[1].start
    scene.add(nar.subtitles())
    scene.render("out.mp4", audio=nar.write_wav("out.wav", scene.duration))

TTS: Kokoro-82M (Apache-2.0) via kokoro-onnx, fully offline once the model files
are in engine/models/ (see README). Audio is cached per sentence, so re-rendering
after a visual tweak doesn't re-synthesise anything.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import soundfile as sf

from reelkit import (COLORS, SAFE_LEFT, SAFE_RIGHT, W, Element, ease_out_back,
                     ease_out_cubic, font, mix, progress, text_w)

ENGINE = Path(__file__).resolve().parent
MODEL = ENGINE / "models" / "kokoro-v1.0.fp16.onnx"
VOICES = ENGINE / "models" / "voices-v1.0.bin"
CACHE = ENGINE.parent / "renders" / ".tts-cache"
SR = 24000

_kokoro = None


def _tts(text: str, voice: str, speed: float) -> np.ndarray:
    key = hashlib.sha1(f"{voice}|{speed}|{text}".encode()).hexdigest()[:16]
    path = CACHE / f"{key}.wav"
    if path.exists():
        audio, _ = sf.read(path, dtype="float32")
        return audio
    global _kokoro
    if _kokoro is None:
        if not MODEL.exists():
            raise FileNotFoundError(
                f"Kokoro model missing: {MODEL}\nDownload it with: python voice.py --download")
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(str(MODEL), str(VOICES))
    audio, sr = _kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    assert sr == SR
    audio = _trim(audio)
    CACHE.mkdir(parents=True, exist_ok=True)
    sf.write(path, audio, SR)
    return audio


def _trim(a: np.ndarray, thresh=0.01, keep=0.04) -> np.ndarray:
    """Strip leading/trailing silence so sentence timings are tight."""
    loud = np.nonzero(np.abs(a) > thresh)[0]
    if len(loud) == 0:
        return a
    k = int(keep * SR)
    return a[max(0, loud[0] - k): loud[-1] + k]


@dataclass
class Sentence:
    shown: str          # what the caption displays (may contain code: nums[2])
    spoken: str         # what the voice says ("nums of two")
    audio: np.ndarray | None = None
    start: float = 0.0

    @property
    def dur(self):
        return len(self.audio) / SR

    @property
    def end(self):
        return self.start + self.dur


@dataclass
class Beat:
    name: str
    sentences: list[Sentence]
    pause_after: float
    min_dur: float

    @property
    def start(self):
        return self.sentences[0].start

    @property
    def end(self):
        return self.sentences[-1].end

    def at(self, i: int) -> float:
        """Start time of the i-th sentence of this beat."""
        return self.sentences[i].start


class Narration:
    def __init__(self, voice: str = "af_heart", speed: float = 1.05,
                 sentence_gap: float = 0.22, beat_gap: float = 0.35):
        self.voice, self.speed = voice, speed
        self.sentence_gap, self.beat_gap = sentence_gap, beat_gap
        self.beats: dict[str, Beat] = {}

    def beat(self, name: str, *sentences, pause_after: float = 0.0, min_dur: float = 0.0):
        """Each sentence is a string, or a (shown, spoken) pair when code
        should be read aloud differently from how it's displayed."""
        ss = [Sentence(s, s) if isinstance(s, str) else Sentence(*s) for s in sentences]
        self.beats[name] = Beat(name, ss, pause_after, min_dur)

    def __getitem__(self, name) -> Beat:
        return self.beats[name]

    def layout(self, lead_in: float = 0.4) -> float:
        """Synthesise every sentence and place them back to back. Returns end time."""
        t = lead_in
        for b in self.beats.values():
            b_start = t
            for i, s in enumerate(b.sentences):
                s.audio = _tts(s.spoken, self.voice, self.speed)
                s.start = t
                t = s.end + (self.sentence_gap if i < len(b.sentences) - 1 else 0)
            t = max(t, b_start + b.min_dur) + b.pause_after + self.beat_gap
        self.total = t
        return t

    def write_wav(self, path: str | Path, duration: float) -> Path:
        mixdown = np.zeros(int(duration * SR) + SR, dtype=np.float32)
        for b in self.beats.values():
            for s in b.sentences:
                i = int(s.start * SR)
                mixdown[i:i + len(s.audio)] += s.audio
        mixdown = mixdown[: int(duration * SR)]
        peak = np.max(np.abs(mixdown)) or 1
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(path, mixdown * (0.89 / peak), SR)
        return path

    def write_srt(self, path: str | Path) -> Path:
        """Caption file for CapCut / YouTube Shorts re-uploads."""
        def ts(x):
            ms = int(round(x * 1000))
            return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
        rows = []
        for n, (s, e, words) in enumerate(_chunks(self), 1):
            rows.append(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(w for w, _, _ in words)}\n")
        Path(path).write_text("\n".join(rows))
        return Path(path)

    def subtitles(self, **kw) -> "Subtitles":
        return Subtitles(chunks=_chunks(self), **kw)


def _chunks(nar: Narration, max_chars: int = 24):
    """Split each sentence into caption chunks of a few words, with per-word
    times estimated from character length (good enough at sentence level,
    since every sentence is synthesised and timed separately)."""
    out = []
    for b in nar.beats.values():
        for s in b.sentences:
            words = s.shown.split()
            weights = [len(w) + 1.5 for w in words]  # +1.5 ≈ inter-word time
            total = sum(weights)
            t, timed = s.start, []
            for w, wt in zip(words, weights):
                d = s.dur * wt / total
                timed.append((w, t, t + d))
                t += d
            # as few chunks as fit max_chars (with a little slack so short
            # sentences stay on one line), split as evenly as possible so a
            # sentence never ends on a lonely one-word caption
            n = max(1, -(-(len(s.shown) - 4) // max_chars))
            for group in _balanced(timed, min(n, len(timed))):
                out.append((group[0][1], group[-1][2], group))
    # hold each chunk on screen until the next one starts (no flicker in short gaps)
    held = []
    for i, (s, e, words) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else e + 0.6
        held.append((s, min(nxt, e + 0.6), words))
    return held


def _balanced(items, n):
    """Split items into n contiguous groups minimising the longest group's text."""
    def length(group):
        return len(" ".join(w for w, _, _ in group))
    if n <= 1:
        return [items]
    best = None
    for cut in range(1, len(items) - n + 2):
        rest = _balanced(items[cut:], n - 1)
        worst = max(length(items[:cut]), *(length(g) for g in rest))
        if best is None or worst < best[0]:
            best = (worst, [items[:cut]] + rest)
    return best[1]


@dataclass
class Subtitles(Element):
    """Burned-in captions: a short phrase, the word being spoken in brand blue."""
    chunks: list = field(default_factory=list)
    y: float = 1478
    size: int = 50
    fade_in: float = 0.0
    slide: int = 0

    def draw(self, d, t):
        cur = next((c for c in self.chunks if c[0] <= t < c[1]), None)
        if not cur:
            return
        c_start, _, words = cur
        f = font("sans-black", self.size)
        space = text_w(" ", f)
        widths = [text_w(w, f) for w, _, _ in words]
        total = sum(widths) + space * (len(words) - 1)
        scale_p = ease_out_back(progress(t, c_start, 0.18))
        x = (W - total) / 2
        x = max(SAFE_LEFT, min(x, SAFE_RIGHT - total))
        y = self.y + (1 - scale_p) * 10
        for (w, ws, we), ww in zip(words, widths):
            speaking = ws <= t < we
            spoken = t >= ws
            if speaking:
                p = ease_out_cubic(progress(t, ws, 0.08))
                d.rounded_rectangle([x - 10, y - 6, x + ww + 10, y + self.size * 1.12],
                                    radius=12, fill=mix(COLORS["bg"], COLORS["primary"], p))
                col = COLORS["bg"]
            else:
                col = COLORS["ink"] if spoken else COLORS["muted"]
            d.text((x, y), w, font=f, fill=col)
            x += ww + space


if __name__ == "__main__":
    import sys
    import urllib.request
    if "--download" in sys.argv:
        base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
        MODEL.parent.mkdir(exist_ok=True)
        for p in (MODEL, VOICES):
            if not p.exists():
                print("downloading", p.name)
                urllib.request.urlretrieve(base + p.name, p)
        print("models ready in", MODEL.parent)
