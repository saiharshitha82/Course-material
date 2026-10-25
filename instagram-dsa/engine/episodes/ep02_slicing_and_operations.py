"""Episode 02 — List slicing and list operations.

    python episodes/ep02_slicing_and_operations.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode, recap
from reelkit import CodeBlock, CodeLine
from structures import Bracket, FlyCells, Hops, ListAnim
from voice import Narration

NAME = "ep02_slicing_and_operations"

nar = Narration()
nar.beat("hook", "Slicing and list operations.", "Four moves you'll use every day.",
         pause_after=0.2)
nar.beat("setup", "Same list as last time.")
nar.beat("slice", ("nums[1:4] takes a slice.", "nums, one to four, takes a slice."),
         "It starts at index one, and stops before index four.", pause_after=0.3)
nar.beat("rule", "The stop index is never included.", pause_after=0.3)
nar.beat("step", ("nums[::2] takes every second item.",
                  "nums, colon colon two, takes every second item."), pause_after=0.5)
nar.beat("rev", ("And nums[::-1] reverses it.", "And nums, colon colon minus one, reverses it."),
         pause_after=0.6)
nar.beat("copy", "Every slice is a new list.", "The original never changes.", pause_after=0.3)
nar.beat("append", ("append adds an item to the end.", "Append adds an item to the end."),
         pause_after=0.4)
nar.beat("insert", ("insert(0, 5) puts a value at the front,", "Insert zero, five, puts a value at the front,"),
         "so every other item has to shift right.", pause_after=0.4)
nar.beat("pop", ("pop removes the last item, and returns it.", "Pop removes the last item, and returns it."),
         pause_after=0.5)
nar.beat("recap", "Recap.", "Slices are copies, and stop is excluded.",
         ("append is fast.", "Append is fast."),
         "Inserting at the front is slow on big lists.", pause_after=0.6)
nar.beat("cta", "Next up: lists versus arrays.", "Follow for the whole series.")

scene, B = new_episode(nar)
hook(scene, B, "Slice it, grow it, shrink it", highlight=("Slice",),
     sub="4 list moves you'll use every day")

END_SLICE = B["append"].start - 0.15
END_MAIN = B["recap"].start - 0.2
header(scene, "Lists · slicing", B["setup"].start, END_SLICE)
header(scene, "Lists · operations", B["append"].start, END_MAIN)

# Source list -----------------------------------------------------------------
ROW_Y, RES_Y = 640, 860
row = ListAnim([10, 20, 30, 40, 50], y=ROW_Y, cell=120, start=B["setup"].start + 0.3,
               end=END_MAIN, label_at=B["setup"].start + 0.9)
row.highlight(B["slice"].at(1), B["step"].start, [1, 2, 3], "primary", dim=True)
row.highlight(B["step"].start + 0.5, B["rev"].start, [0, 2, 4], "accent", dim=True)
row.highlight(B["rev"].start + 0.4, B["copy"].start + 0.2, [0, 1, 2, 3, 4], "primary")

# nums[1:4] ------------------------------------------------------------------
t_fly1 = B["slice"].at(1) + 1.6
scene.add(Bracket(row=row, i0=1, i1=3, text="[1:4]", excluded=4,
                  start=B["slice"].at(1), end=B["step"].start))
res1 = ListAnim([20, 30, 40], y=RES_Y, cell=96, start=t_fly1 + 0.5, end=B["step"].start,
                labels=None, pop=False, stagger=0.12)
scene.add(FlyCells(src=row, src_indices=[1, 2, 3], dst=res1, start=t_fly1,
                   end=t_fly1 + 1.0))
scene.add(res1)

# nums[::2] ------------------------------------------------------------------
t_hops = B["step"].start + 0.5
scene.add(Hops(row=row, indices=[0, 2, 4], start=t_hops, end=B["rev"].start))
t_fly2 = t_hops + 0.9
res2 = ListAnim([10, 30, 50], y=RES_Y, cell=96, start=t_fly2 + 0.5, end=B["rev"].start,
                labels=None, pop=False)
scene.add(FlyCells(src=row, src_indices=[0, 2, 4], dst=res2, start=t_fly2,
                   end=t_fly2 + 1.0, style="accent"))
scene.add(res2)

# nums[::-1] -----------------------------------------------------------------
t_fly3 = B["rev"].start + 0.8
res3 = ListAnim([50, 40, 30, 20, 10], y=RES_Y, cell=96, start=t_fly3 + 0.5,
                end=END_SLICE, labels=None, pop=False, stagger=0.1)
scene.add(FlyCells(src=row, src_indices=[4, 3, 2, 1, 0], dst=res3, start=t_fly3,
                   end=t_fly3 + 1.0, stagger=0.1))
scene.add(res3)

# Operations ------------------------------------------------------------------
t_app = B["append"].start + 0.9
t_ins = B["insert"].start + 1.2
t_pop = B["pop"].start + 1.0
row.append(t_app, 60)
row.insert(t_ins, 0, 5)
row.highlight(t_ins + 0.1, B["pop"].start, [1, 2, 3, 4, 5, 6], "accent")
row.highlight(t_ins + 0.1, B["pop"].start, [0], "primary")
row.pop(t_pop)
scene.add(row)

headlines(scene, [
    ("Start at 1, stop before 4", B["slice"].at(1), B["rule"].start, "primary"),
    ("Stop is never included", B["rule"].start, B["step"].start, "bad"),
    ("Step 2: every second item", B["step"].start + 0.5, B["rev"].start, "accent"),
    ("Step -1: reversed", B["rev"].start + 0.4, B["copy"].start, "primary"),
    ("Slices are new lists", B["copy"].start, END_SLICE, "ink"),
    ("append → add to the end", B["append"].start + 0.5, B["insert"].start, "primary"),
    ("insert(0, x) → everything shifts", B["insert"].start + 0.5, B["pop"].start, "accent"),
    ("pop() → remove + return last", B["pop"].start + 0.4, END_MAIN, "bad"),
])

scene.add(CodeBlock(y=1000, size=34, start=B["setup"].start, end=END_SLICE, lines=[
    CodeLine("nums = [10, 20, 30, 40, 50]", at=B["setup"].start + 0.1),
    CodeLine("nums[1:4]", at=B["slice"].start, focus=(B["slice"].start, B["step"].start)),
    CodeLine("[20, 30, 40]", at=t_fly1 + 0.8, kind="out"),
    CodeLine("nums[::2]", at=B["step"].start, focus=(B["step"].start, B["rev"].start)),
    CodeLine("[10, 30, 50]", at=t_fly2 + 0.8, kind="out"),
    CodeLine("nums[::-1]", at=B["rev"].start, focus=(B["rev"].start, B["copy"].start)),
    CodeLine("[50, 40, 30, 20, 10]", at=t_fly3 + 0.9, kind="out"),
]))
scene.add(CodeBlock(y=1000, size=34, start=B["append"].start, end=END_MAIN, lines=[
    CodeLine("nums.append(60)", at=B["append"].start, focus=(B["append"].start, B["insert"].start)),
    CodeLine("nums.insert(0, 5)", at=B["insert"].start, focus=(B["insert"].start, B["pop"].start)),
    CodeLine("nums", at=B["insert"].at(1)),
    CodeLine("[5, 10, 20, 30, 40, 50, 60]", at=B["insert"].at(1) + 0.4, kind="out"),
    CodeLine("nums.pop()", at=B["pop"].start, focus=(B["pop"].start, END_MAIN)),
    CodeLine("60", at=t_pop + 0.3, kind="out"),
]))

recap(scene, B, [
    ("nums[1:4]", "index 1 up to, not including, 4"),
    ("nums[::-1]", "a reversed copy; nums is unchanged"),
    ("nums.append(x)", "add to the end: fast"),
    ("nums.insert(0, x)", "shifts every item: slow on big lists"),
])
cta(scene, B, "Lists vs arrays", highlight=("arrays",))

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 1.5), ("slice", 4.2), ("step", 2.2), ("rev", 2.4),
                              ("insert", 2.6), ("pop", 2.0), ("recap", 4.0)])
