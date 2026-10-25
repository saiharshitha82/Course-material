# Episode 01: Python list indexing

- **Status:** rendered. Source: [`engine/episodes/ep01_list_indexing.py`](../engine/episodes/ep01_list_indexing.py)
- **Length:** 31 s
- **Learning goal:** the viewer can predict the result of `nums[i]` for positive,
  negative and out-of-range `i`.

## Storyboard and timing

| Time | On screen | Voice-over (optional) |
|---|---|---|
| 0.0–3.6 | Pill "DSA in Python · #01". Title "Python list **indexing** in 30 seconds". Sub: "(and the bug every beginner hits)" | "Python list indexing in thirty seconds, plus the bug every beginner hits." |
| 3.7–6.5 | Header "Lists · indexing". Types `nums = [10, 20, 30, 40, 50]`. Five cells pop in. | "Here's a list of five numbers. Each item has a position." |
| 6.6–9.4 | Blue labels 0–4 above the cells. Caption "Counting starts at 0, not 1". | "Positions start at zero, not one." |
| 9.0–12.6 | Types `nums[2]`. Arrow glides to cell 2, which lifts blue. Output `30`. | "So nums of two is the third item: thirty." |
| 13.0–16.0 | Amber labels −5…−1 below. Caption "Negative indexes count from the end". | "Negative indexes count backwards from the end." |
| 15.5–19.2 | Types `nums[-1]`. Amber arrow on cell 4. Output `50`. | "Minus one is always the last item, whatever the length." |
| 19.7–23.8 | Types `nums[5]`. A dashed red "?" box shakes at position 5. `IndexError: list index out of range`. | "But nums of five? There is no position five. Valid indexes run from minus five to four." |
| 24.0–28.4 | Recap card with three rows | "Recap: zero is first, minus one is last, and length is one past the end." |
| 28.6–31.0 | "Next episode: List **slicing**: nums[1:4]". "Follow so you don't miss it" | "Next up: slicing. Follow so you don't miss it." |

## Instagram caption

```
Python lists start counting at 0 🧠

nums = [10, 20, 30, 40, 50]
nums[2]  → 30   (3rd item)
nums[-1] → 50   (always the last)
nums[5]  → IndexError 💥

Valid indexes for a list of length n: -n … n-1

Quick check 👇 What does nums[-5] return?

Ep 01 of "DSA in Python". Save it for revision and follow for Ep 02: slicing.

#python #datastructures #algorithms #dsa #pythonprogramming #codinginterview
#computerscience #learnpython #csstudent #softwaredeveloper #programmingtips
```

## Checks before you publish

- [ ] Every code line runs in a real Python REPL and prints exactly what's shown
- [ ] No text in the bottom 420 px or the right 140 px (preview on a phone)
- [ ] The cover frame (hook) is exported
- [ ] The quiz question in the caption has one correct answer (`10`)
