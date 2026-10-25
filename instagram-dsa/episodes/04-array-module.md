# Episode 04: Python's `array` module

- **Status:** rendered. Source: [`engine/episodes/ep04_array_module.py`](../engine/episodes/ep04_array_module.py)
- **Length:** 43.4 s
- **Learning goal:** the viewer can create an `array.array` with a type code, read `itemsize`, append to it, and predict the `TypeError` for a value of the wrong type.

## Voice-over and storyboard

| Beat | Time | Voice-over *(spoken form, if different)* | On screen |
|---|---|---|---|
| hook | 0.4–3.8 | "Python has a built-in array type. Most people never use it." | Title "Python's built-in **array**" |
| setup | 4.3–5.9 | "Import it from the array module." | `from array import array`, `a = array('i', [1, 2, 3, 4])`; the strip builds |
| code | 6.6–11.3 | "The first argument, 'i', is the type code. It means every item is a signed integer." *(i)* | Tag changes to `'i' → signed int` |
| size | 12.0–15.1 | "a.itemsize says each item takes four bytes." *(a dot item size)* | Byte ticks; addresses step by 4; `4` |
| append | 15.7–17.7 | "It works like a list, so you can append." | `a.append(5)`: 5 joins the strip |
| gotcha | 18.4–23.2 | "But try appending 2.5. The array refuses. It only holds integers." *(two point five)* | A dashed red 2.5 shakes at the end; `TypeError: 'float' object cannot be interpreted as an integer` |
| codes | 24.1–30.0 | "So pick the type code for your data. 'b' for tiny integers, 'i' for integers, 'd' for decimals." | "Type codes" card: `'b'` 1 byte (−128 to 127), `'i'` usually 4 bytes, `'d'` 8-byte float |
| recap | 31.2–37.9 | "Recap. An array stores one type, packed tightly. The type code sets that type. And the wrong type raises a TypeError." | Three-row recap card |
| cta | 38.9–42.2 | "Next up: NumPy arrays. Follow for the whole series." | "Next episode: **NumPy** arrays" |

## Instagram caption

```
Python has a built-in array, no install needed 📦

from array import array
a = array('i', [1, 2, 3, 4])   # 'i' = signed int
a.itemsize      → 4 (bytes per item)
a.append(5)     ✅
a.append(2.5)   ❌ TypeError

Type codes: 'b' tiny int (1 byte) · 'i' int · 'd' float (8 bytes)

Quick check 👇 What does array('d', [1.5, 2.5]).itemsize return?

Ep 04 of "DSA in Python". Next up: NumPy arrays.

#python #datastructures #arrays #pythontips #dsa #learnpython #computerscience
#codinginterview #csstudent #softwaredeveloper #programming
```

Quiz answer: **8** (verified).

## Checks before you publish

- [x] Every code line was run in Python, and the outputs match what's on screen, including the exact `TypeError` text
- [ ] Watch it once on a phone at full speed
- [ ] Set the hook frame as the cover
