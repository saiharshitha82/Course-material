"""Episode 01 — Python list indexing.

The voice-over drives the timing: beats are synthesised first, then every
visual is scheduled against when its sentence is spoken.

Run from the engine/ folder:
    python episodes/ep01_list_indexing.py            # MP4 with voice + captions
    python episodes/ep01_list_indexing.py --stills   # key frames as PNG for review
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import (ArrayRow, Brand, Card, CodeBlock, CodeLine, Highlight, Pill,  # noqa: E402
                     Pointer, Scene, Text, Title)
from voice import Narration  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "renders"
NAME = "ep01_list_indexing"

# ---------------------------------------------------------------------------
# Script. (shown, spoken) pairs let code read naturally: "nums of two".
# ---------------------------------------------------------------------------
nar = Narration(voice="af_heart", speed=1.05)
nar.beat("hook", ("Python list indexing in 40 seconds.",
                  "Python list indexing, in forty seconds."),
         "Plus the bug every beginner hits.", pause_after=0.2)
nar.beat("setup", "Here's a list of five numbers.", "Each item has a position.")
nar.beat("rule", "And positions start at zero, not one.", pause_after=0.3)
nar.beat("ex1", ("So nums[2] is the third item:", "So, nums of two, is the third item."),
         ("30.", "Thirty."), pause_after=0.4)
nar.beat("neg", "Negative indexes count from the end.", pause_after=0.2)
nar.beat("ex2", ("nums[-1] is always the last item,", "Nums of minus one, is always the last item,"),
         "whatever the length.", pause_after=0.4)
nar.beat("gotcha", ("But nums[5]?", "But nums of five?"),
         "There is no position five.",
         ("Python raises an IndexError.", "Python raises an index error."), pause_after=0.6)
nar.beat("recap", ("Recap: 0 is first,", "Recap. Zero is first."),
         ("-1 is last,", "Minus one is last."),
         ("and len(nums) is one past the end.", "And the length, is one past the end."),
         pause_after=0.6)
nar.beat("cta", "Next up: slicing.", "Follow so you don't miss it.")
END = nar.layout(lead_in=0.4)
DURATION = round(END + 0.8, 1)
B = nar.beats

scene = Scene(DURATION)
scene.add(Brand(handle="@codenest"))

# HOOK -----------------------------------------------------------------------
hook_end = B["setup"].start - 0.15
scene.add(Pill(text="DSA in Python  ·  #01", y=280, start=0.0, end=hook_end))
scene.add(Title(text="Python list indexing in 40 seconds", y=420, size=96,
                highlight=("indexing",), start=0.15, end=hook_end))
scene.add(Text(text="(and the bug every beginner hits)", y=820, size=44,
               color="muted", start=B["hook"].at(1), end=hook_end))

# MAIN -----------------------------------------------------------------------
t_ex1_out = B["ex1"].at(1)
t_ex2_out = B["ex2"].start + 1.3   # roughly when "last item" is said
t_err = B["gotcha"].at(1)
END_MAIN = B["recap"].start - 0.2

scene.add(Text(text="Lists · indexing", y=290, size=50, weight="sans-black",
               start=B["setup"].start, end=END_MAIN))

row = ArrayRow(values=[10, 20, 30, 40, 50], y=720, cell=130,
               start=B["setup"].start + 0.8, end=END_MAIN,
               pos_index_at=B["rule"].start + 0.6, neg_index_at=B["neg"].start + 0.4,
               fade_in=0.01, slide=0,
               highlights=[Highlight(2, B["ex1"].start + 0.6, B["neg"].start, "primary"),
                           Highlight(4, B["ex2"].start + 0.6, B["gotcha"].start, "accent")],
               ghost=(5, t_err, END_MAIN))
scene.add(row)

scene.add(Pointer(row=row, moves=[(0, 2)], label="i = 2",
                  start=B["ex1"].start + 0.4, end=B["neg"].start))
scene.add(Pointer(row=row, moves=[(0, 4)], label="i = -1", color="accent",
                  start=B["ex2"].start + 0.4, end=B["gotcha"].start))

headlines = [
    ("Each item has a position", B["setup"].at(1), B["rule"].start, "ink"),
    ("Counting starts at 0, not 1", B["rule"].start, B["ex1"].start, "primary"),
    ("nums[2] → the 3rd item", B["ex1"].start + 0.6, B["neg"].start, "primary"),
    ("Negative indexes count from the end", B["neg"].start, B["ex2"].start, "accent"),
    ("nums[-1] → always the last item", B["ex2"].start + 0.6, B["gotcha"].start, "accent"),
    ("Only -5 … 4 exist here", t_err, END_MAIN, "bad"),
]
for txt, s, e, col in headlines:
    scene.add(Text(text=txt, y=420, size=50, weight="sans-bold", color=col,
                   start=s, end=e, fade_out=0.15))

scene.add(CodeBlock(y=960, size=36, start=B["setup"].start, end=END_MAIN, lines=[
    CodeLine("nums = [10, 20, 30, 40, 50]", at=B["setup"].start + 0.1),
    CodeLine("nums[2]", at=B["ex1"].start, focus=(B["ex1"].start, B["neg"].start)),
    CodeLine("30", at=t_ex1_out, kind="out"),
    CodeLine("nums[-1]", at=B["ex2"].start, focus=(B["ex2"].start, B["gotcha"].start)),
    CodeLine("50", at=t_ex2_out, kind="out"),
    CodeLine("nums[5]", at=B["gotcha"].start, focus=(B["gotcha"].start, END_MAIN)),
    CodeLine("IndexError: list index out of range", at=t_err, kind="err"),
]))

# RECAP — each row appears as it is spoken ------------------------------------
# Card reveals row i at start + 0.3 + i * row_stagger, so row 0 lands on "Recap".
rc = B["recap"]
scene.add(Card(heading="Recap", y=420, start=rc.start - 0.3, end=B["cta"].start - 0.2,
               row_stagger=(rc.at(2) - rc.start) / 2, rows=[
                   ("nums[0]", "first item — indexes start at 0"),
                   ("nums[-1]", "last item, whatever the length"),
                   ("nums[len(nums)]", "IndexError — one past the end"),
               ]))

# CTA ------------------------------------------------------------------------
cs = B["cta"].start
scene.add(Pill(text="Next episode", y=560, start=cs - 0.1, color="accent", soft="accent_soft"))
scene.add(Title(text="List slicing: nums[1:4]", y=660, size=84,
                highlight=("slicing",), start=cs))
scene.add(Text(text="Follow so you don't miss it", y=900, size=44, color="muted",
               start=B["cta"].at(1)))

# CAPTIONS (burned in, synced word-by-word) ----------------------------------
scene.add(nar.subtitles())

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    print(f"duration {DURATION}s; beats:",
          ", ".join(f"{b.name} {b.start:.1f}-{b.end:.1f}" for b in B.values()))
    if "--stills" in sys.argv:
        for name, dt in (("hook", 1.5), ("ex1", 2.0), ("ex2", 2.4), ("gotcha", 2.5),
                         ("recap", 3.5), ("cta", 1.5)):
            scene.still(B[name].start + dt, OUT / f"{NAME}_{name}.png")
        print("stills written to", OUT)
    else:
        wav = nar.write_wav(OUT / f"{NAME}.wav", DURATION)
        nar.write_srt(OUT / f"{NAME}.srt")
        scene.render(OUT / f"{NAME}.mp4", audio=wav)
