"""Episode 04 — Python's array module.

    python episodes/ep04_array_module.py [--stills]
"""

from common import cta, finish, header, headlines, hook, new_episode, recap
from reelkit import Card, CodeBlock, CodeLine
from structures import ListAnim
from voice import Narration

NAME = "ep04_array_module"

nar = Narration()
nar.beat("hook", "Python has a built-in array type.", "Most people never use it.", pause_after=0.2)
nar.beat("setup", "Import it from the array module.", pause_after=0.3)
nar.beat("code", ("The first argument, 'i', is the type code.",
                  "The first argument, i, is the type code."),
         "It means every item is a signed integer.", pause_after=0.3)
nar.beat("size", ("a.itemsize says each item takes four bytes.",
                  "a dot item size, says each item takes four bytes."), pause_after=0.3)
nar.beat("append", "It works like a list, so you can append.", pause_after=0.4)
nar.beat("gotcha", ("But try appending 2.5.", "But try appending two point five."),
         "The array refuses.", "It only holds integers.", pause_after=0.6)
nar.beat("codes", "So pick the type code for your data.",
         ("'b' for tiny integers, 'i' for integers, 'd' for decimals.",
          "b for tiny integers. i for integers. d for decimals."), pause_after=0.8)
nar.beat("recap", "Recap.", "An array stores one type, packed tightly.",
         "The type code sets that type.", "And the wrong type raises a TypeError.",
         pause_after=0.6)
nar.beat("cta", "Next up: NumPy arrays.", "Follow for the whole series.")

scene, B = new_episode(nar)
hook(scene, B, "Python's built-in array", highlight=("array",),
     sub="most people never use it")

END_MAIN = B["codes"].start - 0.15
header(scene, "The array module", B["setup"].start, END_MAIN)

strip = ListAnim([1, 2, 3, 4], y=640, cell=130, start=B["setup"].start + 1.6, end=END_MAIN,
                 joined=True, labels="address", label_at=B["size"].start + 0.6,
                 byte_ticks=True, itemsize=4, tag="array('i')", tag_color="primary")
strip.retag(B["code"].start + 0.4, "'i' → signed int", "primary")
strip.highlight(B["size"].start + 0.6, B["append"].start, [0, 1, 2, 3], "accent")
t_app = B["append"].start + 1.3
strip.append(t_app, 5)
t_rej = B["gotcha"].at(1)
strip.reject(t_rej, END_MAIN, "2.5")
scene.add(strip)

scene.add(CodeBlock(y=950, size=34, start=B["setup"].start, end=END_MAIN, lines=[
    CodeLine("from array import array", at=B["setup"].start),
    CodeLine("a = array('i', [1, 2, 3, 4])", at=B["setup"].start + 0.9,
             focus=(B["code"].start, B["size"].start)),
    CodeLine("a.itemsize", at=B["size"].start, focus=(B["size"].start, B["append"].start)),
    CodeLine("4", at=B["size"].start + 0.7, kind="out"),
    CodeLine("a.append(5)", at=B["append"].start + 0.6),
    CodeLine("a.append(2.5)", at=B["gotcha"].start, focus=(B["gotcha"].start, END_MAIN)),
    CodeLine("TypeError: 'float' object cannot be interpreted as an integer",
             at=t_rej, kind="err"),
]))

headlines(scene, [
    ("One type, packed tightly", B["setup"].start + 1.6, B["code"].start, "ink"),
    ("'i' = type code", B["code"].start + 0.3, B["size"].start, "primary"),
    ("4 bytes per item", B["size"].start + 0.6, B["append"].start, "accent"),
    ("Works like a list", B["append"].start + 0.3, B["gotcha"].start, "primary"),
    ("Wrong type → TypeError", t_rej, END_MAIN, "bad"),
])

# Type-code table -------------------------------------------------------------
scene.add(Card(heading="Type codes", y=420, start=B["codes"].start - 0.1,
               end=B["recap"].start - 0.2, row_stagger=0.9, rows=[
                   ("'b'", "tiny int, 1 byte (-128 to 127)"),
                   ("'i'", "int, usually 4 bytes"),
                   ("'d'", "float (decimal), 8 bytes"),
               ]))

recap(scene, B, [
    ("array('i', [...])", "one type, packed tightly"),
    ("type code", "'b', 'i', 'd' … sets the item type"),
    ("a.append(2.5)", "TypeError: wrong type is refused"),
])
cta(scene, B, "NumPy arrays", highlight=("NumPy",))

if __name__ == "__main__":
    finish(scene, nar, NAME, [("hook", 1.5), ("code", 2.0), ("size", 2.0), ("gotcha", 3.0),
                              ("codes", 3.5), ("recap", 4.0)])
