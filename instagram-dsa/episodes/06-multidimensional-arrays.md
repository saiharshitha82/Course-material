# Episode 06: Multidimensional arrays

- **Status:** rendered. Source: [`engine/episodes/ep06_multidimensional_arrays.py`](../engine/episodes/ep06_multidimensional_arrays.py)
- **Length:** 46.5 s
- **Learning goal:** the viewer can read `shape`, index `grid[r, c]`, select a column with `grid[:, c]`, and avoid the `[[0] * 3] * 3` aliasing bug.

## Voice-over and storyboard

| Beat | Time | Voice-over *(spoken form, if different)* | On screen |
|---|---|---|---|
| hook | 0.4–4.0 | "Two-dimensional arrays. Plus the grid bug that catches everyone." | Title "**2-D** arrays, and the grid **bug**" |
| setup | 4.6–6.2 | "Give NumPy a list of lists." | `grid = np.array([[1, 2, 3], [4, 5, 6]])`; a 2 × 3 grid pops in |
| shape | 6.8–10.5 | "grid.shape is two by three: two rows, three columns." | Row labels (blue) and column labels (amber); rows light up one after another; `(2, 3)` |
| access | 11.1–13.9 | "grid[1, 2] means row one, column two." | Row 1 lights blue, column 2 amber, and the crossing cell green; `print(grid[1, 2])` → `6` |
| col | 14.8–17.3 | "grid[:, 1] takes a whole column." | Column 1 highlighted; `array([2, 5])` |
| bug | 18.3–22.4 | "Now the bug. Build a grid from plain lists like this, then change one cell." | `g = [[0] * 3] * 3`; a 3 × 3 grid of zeros; `g[0][0] = 9` |
| boom | 23.0–24.1 | "Every row changed!" | All of column 0 flips to 9 in red; `[[9, 0, 0], [9, 0, 0], [9, 0, 0]]` |
| why | 24.9–28.6 | "All three rows are the same list, so one change shows up everywhere." | `g[0]`, `g[1]`, `g[2]` with red arrows to one single `[9, 0, 0]` |
| fix | 29.3–32.9 | "Use a comprehension instead, so each row is a brand new list." | `g = [[0] * 3 for _ in range(3)]`; green arrows to three separate lists; `[[9, 0, 0], [0, 0, 0], [0, 0, 0]]` |
| recap | 33.9–41.6 | "Recap. grid[r, c] is one cell. grid[:, c] is a column. And build plain-list grids with a comprehension." | Four-row recap card |
| cta | 42.6–45.3 | "Next up: tuples. Follow for the whole series." | "Next episode: **Tuples**: frozen lists" |

Accuracy note: in NumPy 2, the REPL shows `grid[1, 2]` as `np.int64(6)`, so the video
uses `print(grid[1, 2])`, which prints `6`.

## Instagram caption

```
This one-liner breaks your grid 🐛

g = [[0] * 3] * 3
g[0][0] = 9
g → [[9, 0, 0], [9, 0, 0], [9, 0, 0]]   😱 every row changed

All 3 rows are the SAME list. Fix:
g = [[0] * 3 for _ in range(3)]

NumPy 2-D basics:
grid.shape   → (rows, columns)
grid[1, 2]   → row 1, column 2
grid[:, 1]   → a whole column

Quick check 👇 For grid = np.array([[1, 2, 3], [4, 5, 6]]), what is grid[0, :]?

Ep 06 on @codenest. Next up: tuples.

#python #numpy #2darray #matrix #datastructures #dsa #learnpython #pythonbug
#codinginterview #computerscience #csstudent #programmingtips
```

Quiz answer: `array([1, 2, 3])`.

## Checks before you publish

- [x] Every code line was run in Python (NumPy 2.5), and the outputs match what's on screen
- [ ] Watch it once on a phone at full speed
- [ ] Set the hook frame as the cover
