"""Episode 00 — Intro: what DSA is, why it matters, and what @codenest teaches.

    python episodes/ep00_intro_to_dsa.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode
from reelkit import Card, CodeBlock, CodeLine, Text
from structures import Chips, CompareBars, Gather, Grid, ListAnim, NodeGraph, RowPointer
from voice import Narration

NAME = "ep00_intro_to_dsa"

nar = Narration()
nar.beat("hook", "What are data structures and algorithms?",
         "And why does every coding interview ask about them?", pause_after=0.2)
nar.beat("setup", "A data structure is a way to organise data,",
         "so your code can use it quickly.", pause_after=0.3)
nar.beat("types", "Lists.", "Grids.", "Trees.", "Graphs.",
         "Each one organises data in its own way.", pause_after=0.3)
nar.beat("algo", "An algorithm is a step-by-step recipe for solving a problem.",
         "Like searching a list: check each item, until you find the one you want.",
         pause_after=0.5)
nar.beat("why", "With a million sorted items, checking one by one can take a million steps.",
         "Binary search needs just twenty.", pause_after=0.5)
nar.beat("interview", "That's why coding interviews are full of DSA.", pause_after=0.3)
nar.beat("learn", "Here, you'll learn it all in Python, visually.",
         "From lists and arrays, to stacks, linked lists, trees, graphs, searching, and sorting.",
         pause_after=0.5)
nar.beat("format", "One idea per reel, in under a minute.",
         "With real code, and a quiz in every caption.", pause_after=0.6)
nar.beat("cta", "Start with episode one: list indexing.", "Follow, and let's master DSA together.")

scene, B = new_episode(nar)
hook(scene, B, "What is DSA, and why learn it?", highlight=("DSA",),
     sub="the skill behind every coding interview")

# DATA STRUCTURES --------------------------------------------------------------
END_DS = B["algo"].start - 0.15
header(scene, "Data structures", B["setup"].start, END_DS)
t_gather = B["setup"].at(1) - 0.2
row = ListAnim([7, 2, 9, 4, 5], y=650, cell=120, start=t_gather + 0.6,
               end=B["types"].start - 0.1, labels=None, pop=False, stagger=0.1)
scene.add(Gather(values=[7, 2, 9, 4, 5],
                 origins=[(210, 600), (820, 560), (470, 880), (700, 930), (300, 830)],
                 dst=row, start=B["setup"].start + 0.2, end=t_gather + 1.2,
                 gather_at=t_gather))
scene.add(row)

# montage: one structure per word
ty = B["types"]
END_TYPES = END_DS
mini = ListAnim([3, 1, 4, 1], y=600, cell=72, gap=8, x_center=300, start=ty.at(0),
                end=END_TYPES, labels=None, stagger=0.06)
scene.add(mini)
scene.add(Grid([[1, 2, 3], [4, 5, 6]], y=576, cell=58, gap=8, x_center=780,
               start=ty.at(1), end=END_TYPES, stagger=0.04))
scene.add(NodeGraph(start=ty.at(2), end=END_TYPES, radius=24, stagger=0.06,
                    nodes=[(300, 820, ""), (225, 890, ""), (375, 890, ""), (185, 960, ""),
                           (265, 960, ""), (335, 960, ""), (415, 960, "")],
                    edges=[(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)],
                    highlight={0: "primary"}))
scene.add(NodeGraph(start=ty.at(3), end=END_TYPES, radius=24, stagger=0.06,
                    nodes=[(690, 830, ""), (860, 810, ""), (650, 950, ""), (800, 965, ""),
                           (900, 905, "")],
                    edges=[(0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (3, 4)],
                    highlight={3: "accent"}))
for txt, x, y, beat_i in (("list", 300, 735, 0), ("grid", 780, 735, 1),
                          ("tree", 300, 1035, 2), ("graph", 780, 1035, 3)):
    scene.add(Text(text=txt, x=x, y=y, size=36, weight="mono-bold", color="muted",
                   anchor="ma", start=ty.at(beat_i) + 0.2, end=END_TYPES))

# ALGORITHMS -------------------------------------------------------------------
al = B["algo"]
END_ALGO = B["why"].start - 0.15
header(scene, "Algorithms", al.start, END_ALGO)
srch = ListAnim([10, 20, 30, 40, 50], y=700, cell=120, start=al.start + 0.3, end=END_ALGO,
                label_at=al.start + 0.5)
steps = [al.at(1) + 1.4 + k * 0.55 for k in range(4)]
for k, t in enumerate(steps[:-1]):
    srch.highlight(t, steps[k + 1], [k], "accent")
srch.highlight(steps[-1], END_ALGO, [3], "good")
scene.add(srch)
scene.add(RowPointer(row=srch, moves=[(steps[0], 0, "40?")] +
                     [(t - 0.3, k, "40?") for k, t in enumerate(steps)][1:],
                     color="accent", start=steps[0] - 0.2, end=END_ALGO))
scene.add(CodeBlock(y=1000, size=34, start=al.start, end=END_ALGO, lines=[
    CodeLine("nums = [10, 20, 30, 40, 50]", at=al.start + 0.2),
    CodeLine("nums.index(40)", at=al.at(1), focus=(al.at(1), END_ALGO)),
    CodeLine("3", at=steps[-1] + 0.2, kind="out"),
]))

# WHY IT MATTERS ----------------------------------------------------------------
wy = B["why"]
END_WHY = B["learn"].start - 0.15
header(scene, "Why it matters", wy.start, END_WHY)
scene.add(CompareBars(y=560, start=wy.start + 0.4, end=END_WHY,
                      row_stagger=wy.at(1) - wy.start - 0.3, rows=[
                          ("Check every item", "1,000,000 steps", 1.0, "bad"),
                          ("Binary search (sorted data)", "20 steps", 20 / 1_000_000, "good"),
                      ]))
scene.add(Text(text="Coding interviews test exactly this", y=1060, size=44,
               weight="sans-bold", color="primary", start=B["interview"].start, end=END_WHY))

# WHAT YOU'LL LEARN -------------------------------------------------------------
ln = B["learn"]
END_LEARN = B["format"].start - 0.15
header(scene, "On @codenest", ln.start, END_LEARN)
scene.add(Chips(y=520, start=ln.at(1) - 0.2, end=END_LEARN, stagger=0.28,
                labels=["Lists", "Arrays", "NumPy", "Tuples", "Sets", "Dictionaries",
                        "Stacks", "Queues", "Linked lists", "Hash tables", "Big-O",
                        "Searching", "Sorting", "Trees", "Graphs"],
                highlight={0: "primary"}))

# FORMAT ------------------------------------------------------------------------
scene.add(Card(heading="Every reel", y=420, start=B["format"].start - 0.2,
               end=B["cta"].start - 0.2, row_stagger=1.1, rows=[
                   ("1 idea", "explained visually, in under a minute"),
                   ("real code", "run in Python; outputs are exact"),
                   ("1 quiz", "in the caption, answer pinned"),
               ]))

headlines(scene, [
    ("A way to organise data", B["setup"].start + 0.3, B["types"].start, "primary"),
    ("Different shapes for different jobs", B["types"].at(4), END_DS, "ink"),
    ("A step-by-step recipe", al.start + 0.3, al.at(1), "primary"),
    ("Linear search: find 40", al.at(1), END_ALGO, "accent"),
    ("1,000,000 sorted items", wy.start + 0.2, END_WHY, "ink"),
    ("Python DSA, step by step", ln.start + 0.2, END_LEARN, "primary"),
])

cta(scene, B, "Ep 01: List indexing", highlight=("indexing",), label="Start here")

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 2.0), ("setup", 3.6), ("types", 4.0),
                              ("algo", 6.6), ("why", 5.5), ("learn", 6.5), ("format", 3.0),
                              ("cta", 2.0)])
