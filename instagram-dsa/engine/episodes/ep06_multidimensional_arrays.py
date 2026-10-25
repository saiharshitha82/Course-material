"""Episode 06 — Multidimensional arrays, and the [[0] * 3] * 3 bug.

    python episodes/ep06_multidimensional_arrays.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode, recap
from reelkit import CodeBlock, CodeLine, Text
from structures import Grid, RefDiagram
from voice import Narration

NAME = "ep06_multidimensional_arrays"

nar = Narration()
nar.beat("hook", "Two-dimensional arrays.", "Plus the grid bug that catches everyone.",
         pause_after=0.2)
nar.beat("setup", "Give NumPy a list of lists.", pause_after=0.3)
nar.beat("shape", ("grid.shape is two by three:", "grid dot shape, is two by three."),
         "two rows, three columns.", pause_after=0.3)
nar.beat("access", ("grid[1, 2] means row one, column two.",
                    "grid, one comma two, means row one, column two."), pause_after=0.6)
nar.beat("col", ("grid[:, 1] takes a whole column.",
                 "grid, colon comma one, takes a whole column."), pause_after=0.6)
nar.beat("bug", "Now the bug.", "Build a grid from plain lists like this,",
         "then change one cell.", pause_after=0.2)
nar.beat("boom", "Every row changed!", pause_after=0.4)
nar.beat("why", "All three rows are the same list,", "so one change shows up everywhere.",
         pause_after=0.4)
nar.beat("fix", "Use a comprehension instead,", "so each row is a brand new list.",
         pause_after=0.6)
nar.beat("recap", "Recap.", ("grid[r, c] is one cell.", "Grid, r comma c, is one cell."),
         ("grid[:, c] is a column.", "Grid, colon comma c, is a column."),
         "And build plain-list grids with a comprehension.", pause_after=0.6)
nar.beat("cta", "Next up: tuples.", "Follow for the whole series.")

scene, B = new_episode(nar)
hook(scene, B, 6, "2-D arrays, and the grid bug", highlight=("2-D", "bug"),
     sub="that catches everyone")

END_NP = B["bug"].start - 0.15
END_MAIN = B["recap"].start - 0.2
header(scene, "2-D arrays", B["setup"].start, END_NP)
header(scene, "The grid bug", B["bug"].start, END_MAIN)

# NumPy grid ------------------------------------------------------------------
grid = Grid([[1, 2, 3], [4, 5, 6]], y=620, cell=120, start=B["setup"].start + 1.2,
            end=END_NP, labels_at=B["shape"].start + 0.5)
grid.highlight(B["shape"].at(1), B["access"].start, r=0, style="primary")
grid.highlight(B["shape"].at(1) + 0.6, B["access"].start, r=1, style="primary")
a = B["access"].start
grid.highlight(a + 0.8, B["col"].start, r=1, style="primary")
grid.highlight(a + 1.8, B["col"].start, c=2, style="accent")
grid.highlight(a + 2.6, B["col"].start, r=1, c=2, style="good")
grid.highlight(B["col"].start + 0.9, END_NP, c=1, style="primary")
scene.add(grid)

scene.add(CodeBlock(y=905, size=32, start=B["setup"].start, end=END_NP, lines=[
    CodeLine("import numpy as np", at=B["setup"].start),
    CodeLine("grid = np.array([[1, 2, 3],", at=B["setup"].start + 0.6),
    CodeLine("                [4, 5, 6]])", at=B["setup"].start + 1.4, prompt="... "),
    CodeLine("grid.shape", at=B["shape"].start, focus=(B["shape"].start, a)),
    CodeLine("(2, 3)", at=B["shape"].start + 0.8, kind="out"),
    CodeLine("print(grid[1, 2])", at=a, focus=(a, B["col"].start)),
    CodeLine("6", at=a + 2.6, kind="out"),
    CodeLine("grid[:, 1]", at=B["col"].start, focus=(B["col"].start, END_NP)),
    CodeLine("array([2, 5])", at=B["col"].start + 1.0, kind="out"),
]))

# The bug: [[0] * 3] * 3 ------------------------------------------------------
t_set = B["bug"].at(2) + 0.6
END_GRID2 = B["why"].start - 0.1
g2 = Grid([[0] * 3 for _ in range(3)], y=560, cell=110, start=B["bug"].at(1) + 0.8,
          end=END_GRID2, labels_at=B["bug"].at(1) + 1.0)
g2.set(t_set, {(0, 0): 9, (1, 0): 9, (2, 0): 9}, style="bad")
g2.highlight(B["boom"].start, END_GRID2, c=0, style="bad")
scene.add(g2)

# why: three names, one list
END_WHY = B["fix"].start - 0.1
rows_y = [600, 720, 840]
scene.add(RefDiagram(start=B["why"].start, end=END_WHY, links_at=B["why"].start + 0.4,
                     slots=[(250, y, None) for y in rows_y],
                     objects=[(700, 720, "[9, 0, 0]", "one list")],
                     links=[(0, 0), (1, 0), (2, 0)], link_stagger=0.3,
                     link_style={0: "bad", 1: "bad", 2: "bad"}))
for i, y in enumerate(rows_y):
    scene.add(Text(text=f"g[{i}]", x=110, y=y - 20, size=34, weight="mono-bold",
                   color="primary", start=B["why"].start, end=END_WHY))
# fix: three separate lists
scene.add(RefDiagram(start=B["fix"].start, end=END_MAIN, links_at=B["fix"].start + 0.6,
                     slots=[(250, y, None) for y in rows_y],
                     objects=[(700, y, v, None) for y, v in
                              zip(rows_y, ["[9, 0, 0]", "[0, 0, 0]", "[0, 0, 0]"])],
                     links=[(0, 0), (1, 1), (2, 2)], link_stagger=0.3,
                     link_style={0: "good", 1: "good", 2: "good"}))
for i, y in enumerate(rows_y):
    scene.add(Text(text=f"g[{i}]", x=110, y=y - 20, size=34, weight="mono-bold",
                   color="primary", start=B["fix"].start, end=END_MAIN))

scene.add(CodeBlock(y=1000, size=34, start=B["bug"].at(1), end=B["fix"].start, lines=[
    CodeLine("g = [[0] * 3] * 3", at=B["bug"].at(1)),
    CodeLine("g[0][0] = 9", at=B["bug"].at(2), focus=(B["bug"].at(2), B["why"].start)),
    CodeLine("g", at=t_set + 0.2),
    CodeLine("[[9, 0, 0], [9, 0, 0], [9, 0, 0]]", at=B["boom"].start, kind="err"),
]))
scene.add(CodeBlock(y=1000, size=34, start=B["fix"].start, end=END_MAIN, lines=[
    CodeLine("g = [[0] * 3 for _ in range(3)]", at=B["fix"].start),
    CodeLine("g[0][0] = 9", at=B["fix"].start + 1.4),
    CodeLine("g", at=B["fix"].at(1)),
    CodeLine("[[9, 0, 0], [0, 0, 0], [0, 0, 0]]", at=B["fix"].at(1) + 0.4, kind="out"),
]))

headlines(scene, [
    ("A list of lists → a grid", B["setup"].start + 0.4, B["shape"].start, "ink"),
    ("shape = (rows, columns)", B["shape"].start + 0.3, a, "primary"),
    ("grid[row, column]", a + 0.4, B["col"].start, "good"),
    (": means every row", B["col"].start + 0.5, END_NP, "primary"),
    ("Change one cell…", B["bug"].at(2), B["boom"].start, "ink"),
    ("…every row changed!", B["boom"].start, B["why"].start, "bad"),
    ("3 names, 1 list", B["why"].start + 0.2, B["fix"].start, "bad"),
    ("Fix: a new list per row", B["fix"].start + 0.2, END_MAIN, "good"),
])

recap(scene, B, [
    ("grid[r, c]", "one cell: row r, column c"),
    ("grid[:, c]", "a whole column"),
    ("grid.shape", "(rows, columns)"),
    ("[[0]*3 for _ in range(3)]", "a safe grid of plain lists"),
])
cta(scene, B, "Tuples: frozen lists", highlight=("Tuples",))

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 1.5), ("shape", 2.4), ("access", 3.2), ("col", 2.2),
                              ("boom", 0.8), ("why", 2.0), ("fix", 3.5), ("recap", 4.5)])
