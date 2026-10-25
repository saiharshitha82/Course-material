# Episode 05: NumPy arrays

- **Status:** rendered. Source: [`engine/episodes/ep05_numpy_arrays.py`](../engine/episodes/ep05_numpy_arrays.py)
- **Length:** 38.1 s
- **Learning goal:** the viewer understands vectorised operations (`a * 2` works on every element) and doesn't confuse them with `list * 2`, which repeats the list.

## Voice-over and storyboard

| Beat | Time | Voice-over *(spoken form, if different)* | On screen |
|---|---|---|---|
| hook | 0.4–4.2 | "Why does everyone use NumPy? Watch what happens when we double a list." | Title "Why everyone uses **NumPy**" |
| setup | 4.7–6.1 | "Here's a plain Python list." | `nums = [1, 2, 3, 4]`, tagged `list` |
| loop | 6.7–10.1 | "To double it, Python visits each item, one at a time." | `[x * 2 for x in nums]`: an amber `x` pointer steps along and each cell doubles in turn; `[2, 4, 6, 8]` |
| np | 11.0–12.3 | "Now the NumPy way." | `import numpy as np`, `a = np.array(nums)`; tag `np.array · dtype int64` |
| vec | 12.9–18.7 | "a * 2 doubles every item at once. The loop runs inside NumPy's fast, compiled code." *(a times two)* | All four cells pulse together to 2, 4, 6, 8, with "× 2"; `array([2, 4, 6, 8])` |
| gotcha | 19.5–24.4 | "Careful: nums * 2 on a plain list doesn't do maths. It repeats the list!" *(nums times two)* | The list row grows to 8 cells; the copies are red; `[1, 2, 3, 4, 1, 2, 3, 4]` |
| recap | 25.5–32.4 | "Recap. NumPy does maths on the whole array at once. Every item shares one type. And a list times two just repeats." | Three-row recap card |
| cta | 33.4–37.0 | "Next up: multidimensional arrays. Follow for the whole series." | "Next episode: **Multidimensional** arrays" |

Accuracy note: `dtype` shows `int64` on NumPy 2.x, which is what was used to verify
this. On NumPy 1.x under Windows it was `int32`. The video says "one type" in the
voice-over and shows int64 only in the tag.

## Instagram caption

```
Same numbers. Very different results 👀

nums = [1, 2, 3, 4]
a = np.array(nums)

a * 2     → array([2, 4, 6, 8])         maths on every item at once ⚡
nums * 2  → [1, 2, 3, 4, 1, 2, 3, 4]    just repeats the list 😅

NumPy runs the loop in compiled code, and every item shares one dtype.

Quick check 👇 What does np.array([1, 2, 3]) + 10 give?

Ep 05 of "DSA in Python". Next up: multidimensional arrays.

#python #numpy #datascience #datastructures #dsa #learnpython #machinelearning
#computerscience #codinginterview #csstudent #programmingtips
```

Quiz answer: `array([11, 12, 13])`.

## Checks before you publish

- [x] Every code line was run in Python (NumPy 2.5), and the outputs match what's on screen
- [ ] Watch it once on a phone at full speed
- [ ] Set the hook frame as the cover
