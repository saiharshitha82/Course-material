"""Episode 01 — Python list indexing (≈31 s).

Run from the engine/ folder:
    python episodes/ep01_list_indexing.py            # full MP4
    python episodes/ep01_list_indexing.py --stills   # key frames as PNG for review
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import (ArrayRow, Brand, Card, CodeBlock, CodeLine, Highlight, Pill,  # noqa: E402
                     Pointer, Scene, Text, Title)

DURATION = 31
OUT = Path(__file__).resolve().parents[2] / "renders"

scene = Scene(DURATION)
scene.add(Brand(handle="@yourhandle", duration=DURATION))

# 0–3.6 s  HOOK ---------------------------------------------------------------
scene.add(Pill(text="DSA in Python  ·  #01", y=280, start=0.0, end=3.6))
scene.add(Title(text="Python list indexing in 30 seconds", y=420, size=96,
                highlight=("indexing",), start=0.15, end=3.6))
scene.add(Text(text="(and the bug every beginner hits)", y=820, size=44,
               color="muted", start=1.2, end=3.6))

# 3.6–23.8 s  MAIN EXPLANATION -----------------------------------------------
END_MAIN = 23.8
scene.add(Text(text="Lists · indexing", y=290, size=50, weight="sans-black",
               start=3.7, end=END_MAIN))

row = ArrayRow(values=[10, 20, 30, 40, 50], y=720, cell=130, start=5.0, end=END_MAIN,
               pos_index_at=6.6, neg_index_at=13.0, fade_in=0.01, slide=0,
               highlights=[Highlight(2, 10.0, 12.6, "primary"),
                           Highlight(4, 16.5, 19.2, "accent")],
               ghost=(5, 20.6, 23.4))
scene.add(row)

scene.add(Pointer(row=row, moves=[(0, 2)], label="i = 2", start=9.6, end=12.6))
scene.add(Pointer(row=row, moves=[(0, 4)], label="i = -1", color="accent",
                  start=16.1, end=19.2))

captions = [
    ("Each item has a position", 5.2, 6.5, "ink"),
    ("Counting starts at 0, not 1", 6.6, 9.4, "primary"),
    ("nums[2] → the 3rd item", 10.0, 12.6, "primary"),
    ("Negative indexes count from the end", 13.0, 16.0, "accent"),
    ("nums[-1] → always the last item", 16.5, 19.2, "accent"),
    ("Only -5 … 4 exist here", 20.6, END_MAIN, "bad"),
]
for txt, s, e, col in captions:
    scene.add(Text(text=txt, y=470, size=50, weight="sans-bold", color=col,
                   start=s, end=e, fade_out=0.15))

scene.add(CodeBlock(y=960, size=36, start=3.8, end=END_MAIN, lines=[
    CodeLine("nums = [10, 20, 30, 40, 50]", at=3.9),
    CodeLine("nums[2]", at=9.0, focus=(9.0, 12.6)),
    CodeLine("30", at=10.0, kind="out"),
    CodeLine("nums[-1]", at=15.5, focus=(15.5, 19.2)),
    CodeLine("50", at=16.5, kind="out"),
    CodeLine("nums[5]", at=19.7, focus=(19.7, END_MAIN)),
    CodeLine("IndexError: list index out of range", at=20.6, kind="err"),
]))

# 24–28.4 s  RECAP ------------------------------------------------------------
scene.add(Card(heading="Recap", y=420, start=24.0, end=28.4, row_stagger=0.7, rows=[
    ("nums[0]", "first item — indexes start at 0"),
    ("nums[-1]", "last item, whatever the length"),
    ("nums[len(nums)]", "IndexError — one past the end"),
]))

# 28.6–31 s  CTA --------------------------------------------------------------
scene.add(Pill(text="Next episode", y=560, start=28.6, color="accent", soft="accent_soft"))
scene.add(Title(text="List slicing: nums[1:4]", y=660, size=84,
                highlight=("slicing",), start=28.8))
scene.add(Text(text="Follow so you don't miss it", y=900, size=44, color="muted",
               start=29.3))

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if "--stills" in sys.argv:
        for t in (1.5, 8.0, 11.5, 17.5, 22.0, 27.0, 30.5):
            scene.still(t, OUT / f"ep01_t{t:04.1f}.png")
        print("stills written to", OUT)
    else:
        scene.render(OUT / "ep01_list_indexing.mp4")
