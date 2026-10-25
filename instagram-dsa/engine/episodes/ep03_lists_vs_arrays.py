"""Episode 03 — Lists vs arrays: references vs packed values.

    python episodes/ep03_lists_vs_arrays.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode, recap
from reelkit import CodeBlock, CodeLine, Text
from structures import ListAnim, RefDiagram
from voice import Narration

NAME = "ep03_lists_vs_arrays"

nar = Narration()
nar.beat("hook", "Python lists are not arrays.", "Here's what's really in memory.", pause_after=0.2)
nar.beat("setup", "A list can mix types, like this.", pause_after=0.2)
nar.beat("refs", "That's because a list doesn't store the values.",
         "It stores references: arrows to objects somewhere else in memory.", pause_after=0.4)
nar.beat("cost", "Each object is a separate box, with its own overhead.", pause_after=0.3)
nar.beat("array", "An array stores the raw values themselves,", "packed side by side.",
         pause_after=0.3)
nar.beat("same", "Every item has the same type, and the same size.",
         "Here, four bytes each.", pause_after=0.3)
nar.beat("jump", "So the computer finds any item with simple maths:",
         "start, plus index, times size.", pause_after=0.8)
nar.beat("recap", "Recap.", "Lists hold references, so they're flexible.",
         "Arrays hold raw values, so they're compact and fast.", pause_after=0.6)
nar.beat("cta", "Next up: Python's array module.", "Follow for the whole series.")

scene, B = new_episode(nar)
hook(scene, B, "Lists are not arrays", highlight=("not",),
     sub="here's what's really in memory")

END_A = B["array"].start - 0.15
END_MAIN = B["recap"].start - 0.2
header(scene, "Lists vs arrays", B["setup"].start, END_MAIN)

# Part A: a list of references ------------------------------------------------
slot_x = [315, 465, 615, 765]
scene.add(RefDiagram(
    start=B["setup"].start + 1.0, end=END_A, links_at=B["refs"].at(1) + 0.2,
    slots=[(x, 610, str(i)) for i, x in enumerate(slot_x)],
    objects=[(250, 815, "1", "int"), (760, 915, '"hi"', "str"),
             (460, 910, "3.5", "float"), (820, 790, "True", "bool")],
    links=[(0, 0), (1, 1), (2, 2), (3, 3)],
    memory_box=(100, 690, 940, 975, "memory"),
))
scene.add(CodeBlock(y=1000, size=34, start=B["setup"].start, end=END_A, lines=[
    CodeLine('mixed = [1, "hi", 3.5, True]', at=B["setup"].start + 0.1),
]))

# Part B: an array of packed values -------------------------------------------
strip = ListAnim([1, 2, 3, 4], y=640, cell=150, start=B["array"].start + 0.6, end=END_MAIN,
                 joined=True, labels="address", label_at=B["same"].start,
                 byte_ticks=True, itemsize=4, tag="array('i')", tag_color="primary")
strip.highlight(B["same"].at(1), B["jump"].start, [0, 1, 2, 3], "accent")
t_jump = B["jump"].at(1)
strip.highlight(t_jump, END_MAIN, [2], "primary")
scene.add(strip)
scene.add(Text(text="1000 + 2 × 4 = 1008", y=880, size=44, weight="mono-bold",
               color="primary", start=t_jump + 0.4, end=END_MAIN))
scene.add(Text(text="(addresses are illustrative)", y=945, size=28, color="muted",
               start=B["same"].start + 0.3, end=END_MAIN))
scene.add(CodeBlock(y=1000, size=34, start=B["array"].start, end=END_MAIN, lines=[
    CodeLine("from array import array", at=B["array"].start),
    CodeLine("a = array('i', [1, 2, 3, 4])", at=B["array"].start + 1.1),
    CodeLine("a.itemsize", at=B["same"].at(1) - 0.4),
    CodeLine("4", at=B["same"].at(1), kind="out"),
    CodeLine("a[2]", at=t_jump, focus=(t_jump, END_MAIN)),
    CodeLine("3", at=t_jump + 0.6, kind="out"),
]))

headlines(scene, [
    ("A list can mix types", B["setup"].start + 0.4, B["refs"].start, "ink"),
    ("Lists store references", B["refs"].start, B["cost"].start, "primary"),
    ("One object per item", B["cost"].start, END_A, "accent"),
    ("Arrays store raw values", B["array"].start + 0.3, B["same"].start, "primary"),
    ("Same type, same size", B["same"].start, B["jump"].start, "accent"),
    ("start + index × size", B["jump"].start + 0.3, END_MAIN, "primary"),
])

recap(scene, B, [
    ("list", "references to objects: any type, flexible"),
    ("array", "raw values packed together: one type"),
    ("a[i]", "found by maths: start + i × size"),
])
cta(scene, B, "Python's array module", highlight=("array",))

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 1.5), ("refs", 4.5), ("same", 2.5), ("jump", 3.5),
                              ("recap", 4.0)])
