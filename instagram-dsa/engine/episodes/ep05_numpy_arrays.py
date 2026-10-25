"""Episode 05 — NumPy arrays: vectorised maths vs Python loops.

    python episodes/ep05_numpy_arrays.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode, recap
from reelkit import CodeBlock, CodeLine, Text
from structures import ListAnim, RowPointer
from voice import Narration

NAME = "ep05_numpy_arrays"

nar = Narration()
nar.beat("hook", "Why does everyone use NumPy?", "Watch what happens when we double a list.",
         pause_after=0.2)
nar.beat("setup", "Here's a plain Python list.", pause_after=0.2)
nar.beat("loop", "To double it, Python visits each item,", "one at a time.", pause_after=0.6)
nar.beat("np", "Now the NumPy way.", pause_after=0.3)
nar.beat("vec", ("a * 2 doubles every item at once.", "a times two, doubles every item at once."),
         "The loop runs inside NumPy's fast, compiled code.", pause_after=0.5)
nar.beat("gotcha", ("Careful: nums * 2 on a plain list", "Careful. nums times two, on a plain list,"),
         "doesn't do maths.", "It repeats the list!", pause_after=0.7)
nar.beat("recap", "Recap.", "NumPy does maths on the whole array at once.",
         "Every item shares one type.", "And a list times two just repeats.", pause_after=0.6)
nar.beat("cta", "Next up: multidimensional arrays.", "Follow for the whole series.")

scene, B = new_episode(nar)
hook(scene, B, 5, "Why everyone uses NumPy", highlight=("NumPy",),
     sub="watch what happens when we double a list")

END_MAIN = B["recap"].start - 0.2
header(scene, "NumPy arrays", B["setup"].start, END_MAIN)

row = ListAnim([1, 2, 3, 4], y=660, cell=130, start=B["setup"].start + 0.6, end=END_MAIN,
               tag="list", tag_color="muted")

# Python loop: one item at a time
lp = B["loop"]
steps = [lp.start + 0.9 + k * 0.7 for k in range(4)]
for k, t in enumerate(steps):
    row.set(t, k, (k + 1) * 2, style="accent")
scene.add(RowPointer(row=row, moves=[(steps[0] - 0.4, 0, "x")] +
                     [(t - 0.35, k, "x") for k, t in enumerate(steps)][1:],
                     color="accent", start=steps[0] - 0.4, end=steps[-1] + 0.6))

# NumPy: all at once
t_np = B["np"].start + 1.2
row.reset(t_np, [1, 2, 3, 4])
row.retag(t_np, "np.array  ·  dtype int64", "primary")
t_vec = B["vec"].start + 1.0
row.set_all(t_vec, [2, 4, 6, 8], style="primary")
scene.add(Text(text="× 2", x=838, y=692, size=60, weight="sans-black", color="primary",
               start=t_vec - 0.3, end=t_vec + 1.0, fade_out=0.3))

# list * 2 repeats
t_list = B["gotcha"].start + 0.2
row.reset(t_list, [1, 2, 3, 4])
row.retag(t_list, "list", "muted")
t_rep = B["gotcha"].at(2)
row.extend(t_rep, [1, 2, 3, 4])
row.highlight(t_rep + 0.2, END_MAIN, [4, 5, 6, 7], "bad")
scene.add(row)

headlines(scene, [
    ("A plain Python list", B["setup"].start + 0.3, lp.start, "ink"),
    ("Loop: one item at a time", lp.start + 0.3, B["np"].start, "accent"),
    ("Same data, as a NumPy array", B["np"].start + 0.6, B["vec"].start, "primary"),
    ("Every item at once", t_vec, B["gotcha"].start, "primary"),
    ("list * 2 doesn't do maths", t_list + 0.3, t_rep, "bad"),
    ("It repeats the list!", t_rep, END_MAIN, "bad"),
])

scene.add(CodeBlock(y=1000, size=34, start=B["setup"].start, end=B["gotcha"].start, lines=[
    CodeLine("nums = [1, 2, 3, 4]", at=B["setup"].start + 0.1),
    CodeLine("[x * 2 for x in nums]", at=lp.start, focus=(lp.start, B["np"].start)),
    CodeLine("[2, 4, 6, 8]", at=steps[-1] + 0.5, kind="out"),
    CodeLine("import numpy as np", at=B["np"].start),
    CodeLine("a = np.array(nums)", at=B["np"].start + 0.7),
    CodeLine("a * 2", at=B["vec"].start, focus=(B["vec"].start, B["gotcha"].start)),
    CodeLine("array([2, 4, 6, 8])", at=t_vec + 0.2, kind="out"),
]))
scene.add(CodeBlock(y=1000, size=34, start=B["gotcha"].start, end=END_MAIN, lines=[
    CodeLine("nums * 2", at=B["gotcha"].start, focus=(B["gotcha"].start, END_MAIN)),
    CodeLine("[1, 2, 3, 4, 1, 2, 3, 4]", at=t_rep + 0.2, kind="err"),
]))

recap(scene, B, [
    ("a * 2", "maths on every item at once"),
    ("a.dtype", "one type for every item (int64)"),
    ("nums * 2", "plain list: repeats, no maths!"),
])
cta(scene, B, "Multidimensional arrays", highlight=("Multidimensional",))

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 1.5), ("loop", 2.6), ("vec", 1.6), ("gotcha", 3.5),
                              ("recap", 4.0)])
