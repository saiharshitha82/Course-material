# Episode 03: Lists vs arrays

- **Status:** rendered. Source: [`engine/episodes/ep03_lists_vs_arrays.py`](../engine/episodes/ep03_lists_vs_arrays.py)
- **Length:** 43.8 s
- **Learning goal:** the viewer can explain that a list stores references to objects anywhere in memory, while an array packs same-typed raw values contiguously, and why that makes `a[i]` simple address arithmetic.

## Voice-over and storyboard

| Beat | Time | Voice-over | On screen |
|---|---|---|---|
| hook | 0.4–3.7 | "Python lists are not arrays. Here's what's really in memory." | Title "Lists are **not** arrays" |
| setup | 4.2–5.8 | "A list can mix types, like this." | `mixed = [1, "hi", 3.5, True]`; 4 slots pop in |
| refs | 6.3–12.1 | "That's because a list doesn't store the values. It stores references: arrows to objects somewhere else in memory." | A dashed "memory" area; arrows grow from each slot to scattered objects labelled int, str, float, bool |
| cost | 12.8–15.8 | "Each object is a separate box, with its own overhead." | Headline "One object per item" |
| array | 16.5–20.0 | "An array stores the raw values themselves, packed side by side." | `array('i', [1, 2, 3, 4])`: a joined memory strip |
| same | 20.7–25.1 | "Every item has the same type, and the same size. Here, four bytes each." | Byte ticks inside each cell; addresses 1000, 1004, 1008, 1012; `a.itemsize` → `4` |
| jump | 25.8–30.6 | "So the computer finds any item with simple maths: start, plus index, times size." | Cell 2 lifts; `1000 + 2 × 4 = 1008`; `a[2]` → `3` |
| recap | 31.7–38.1 | "Recap. Lists hold references, so they're flexible. Arrays hold raw values, so they're compact and fast." | Three-row recap card |
| cta | 39.0–42.6 | "Next up: Python's array module. Follow for the whole series." | "Next episode: Python's **array** module" |

Accuracy notes: the memory addresses are labelled "illustrative" on screen. Lists
storing references (pointers) to objects describes CPython, the standard
interpreter. `itemsize` for `'i'` is 4 on mainstream platforms; the docs only
guarantee at least 2.

## Instagram caption

```
A Python list is NOT an array 🧠

list  → a row of references (arrows) to objects anywhere in memory
         so it can mix types: [1, "hi", 3.5, True]
array → the raw values themselves, packed side by side
         one type, same size → item i lives at start + i × size

Flexible vs compact. Know which one you're using.

Quick check 👇 If an array starts at address 2000 and each item is 8 bytes, where is a[3]?

Ep 03 of "DSA in Python". Next up: Python's array module.

#python #datastructures #arrays #memory #dsa #computerscience #learnpython
#codinginterview #csstudent #softwaredeveloper #programmingtips
```

Quiz answer: 2000 + 3 × 8 = **2024**.

## Checks before you publish

- [x] Every code line was run in Python, and the outputs match what's on screen
- [ ] Watch it once on a phone at full speed
- [ ] Set the hook frame as the cover
