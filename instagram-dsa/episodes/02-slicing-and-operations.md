# Episode 02: List slicing and list operations

- **Status:** rendered. Source: [`engine/episodes/ep02_slicing_and_operations.py`](../engine/episodes/ep02_slicing_and_operations.py)
- **Length:** 50.7 s
- **Learning goal:** the viewer can predict `nums[a:b]`, `nums[::step]` and `nums[::-1]`, and knows that `append` is cheap while `insert(0, x)` shifts every item.

## Voice-over and storyboard

| Beat | Time | Voice-over *(spoken form, if different)* | On screen |
|---|---|---|---|
| hook | 0.4–4.0 | "Slicing and list operations. Four moves you'll use every day." | Title "**Slice** it, grow it, shrink it" |
| setup | 4.5–5.9 | "Same list as last time." | `nums = [10, 20, 30, 40, 50]`, cells with indices |
| slice | 6.3–11.4 | "nums[1:4] takes a slice. It starts at index one, and stops before index four." *(nums, one to four…)* | Cells 1–3 highlighted, others dimmed; a bracket labelled `[1:4]`; a dashed red box on index 4; copies fly down into `[20, 30, 40]` |
| rule | 12.0–14.0 | "The stop index is never included." | Headline in red |
| step | 14.6–17.7 | "nums[::2] takes every second item." *(colon colon two)* | Amber arcs hop 0 → 2 → 4; copies fly into `[10, 30, 50]` |
| rev | 18.5–21.4 | "And nums[::-1] reverses it." *(colon colon minus one)* | Cells fly in reverse order into `[50, 40, 30, 20, 10]` |
| copy | 22.3–25.6 | "Every slice is a new list. The original never changes." | Original row untouched |
| append | 26.2–28.0 | "append adds an item to the end." | 60 drops in at the end |
| insert | 28.8–33.7 | "insert(0, 5) puts a value at the front, so every other item has to shift right." | Every cell glides right (amber) and 5 drops in at index 0 |
| pop | 34.5–37.0 | "pop removes the last item, and returns it." | 60 flies out; the REPL prints `60` |
| recap | 37.8–45.1 | "Recap. Slices are copies, and stop is excluded. append is fast. Inserting at the front is slow on big lists." | Four-row recap card |
| cta | 46.0–49.5 | "Next up: lists versus arrays. Follow for the whole series." | "Next episode: Lists vs **arrays**" |

## Instagram caption

```
Slicing never touches your original list ✂️

nums = [10, 20, 30, 40, 50]
nums[1:4]   → [20, 30, 40]   stop is NOT included
nums[::2]   → [10, 30, 50]
nums[::-1]  → [50, 40, 30, 20, 10]

nums.append(60)   → fast, adds to the end
nums.insert(0, 5) → shifts EVERY item right 🐢
nums.pop()        → removes + returns the last item

Quick check 👇 What is nums[1:1]?

Ep 02 of "DSA in Python". Next up: lists vs arrays.

#python #datastructures #algorithms #dsa #pythonlists #slicing #learnpython
#codinginterview #computerscience #csstudent #programmingtips
```

Quiz answer (pin it as a comment later): `[]`, an empty list, because start = stop.

## Checks before you publish

- [x] Every code line was run in Python, and the outputs match what's on screen
- [ ] Watch it once on a phone at full speed
- [ ] Set the hook frame as the cover
