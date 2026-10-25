# Episode 01: Python list indexing

- **Status:** rendered. Source: [`engine/episodes/ep01_list_indexing.py`](../engine/episodes/ep01_list_indexing.py)
- **Length:** 37.8 s (set by the narration)
- **Learning goal:** the viewer can predict the result of `nums[i]` for positive,
  negative and out-of-range `i`.
- **Audio:** Kokoro `af_heart` voice-over, with captions burned in and synced word by word

## Voice-over script and storyboard

The times are what the renderer produced. They come from the narration, so if you
edit a line, the visuals re-time themselves.

| Beat | Time | Voice-over (caption text; spoken form in brackets if different) | On screen |
|---|---|---|---|
| hook | 0.4–4.8 | "Python list indexing in 40 seconds. Plus the bug every beginner hits." | Title with **indexing** underlined, sub-line |
| setup | 5.4–8.5 | "Here's a list of five numbers. Each item has a position." | `nums = [10, 20, 30, 40, 50]` types out, five cells pop in |
| rule | 8.9–10.9 | "And positions start at zero, not one." | Blue indices 0–4 above the cells |
| ex1 | 11.6–14.5 | "So nums[2] is the third item: 30." *(nums of two… thirty)* | Arrow to cell 2, which lifts blue; `30` appears as "thirty" is said |
| neg | 15.2–17.2 | "Negative indexes count from the end." | Amber −5…−1 below the cells |
| ex2 | 17.8–21.6 | "nums[-1] is always the last item, whatever the length." *(nums of minus one…)* | Amber arrow to cell 4, output `50` |
| gotcha | 22.3–27.0 | "But nums[5]? There is no position five. Python raises an IndexError." | A dashed red "?" box shakes, then `IndexError: list index out of range` |
| recap | 27.9–32.9 | "Recap: 0 is first, -1 is last, and len(nums) is one past the end." | Recap card; each row appears as it is spoken |
| cta | 33.9–36.7 | "Next up: slicing. Follow so you don't miss it." | "Next episode: List **slicing**: nums[1:4]" |

## Instagram caption

```
Python lists start counting at 0 🧠

nums = [10, 20, 30, 40, 50]
nums[2]  → 30   (3rd item)
nums[-1] → 50   (always the last)
nums[5]  → IndexError 💥

Valid indexes for a list of length n: -n … n-1

Quick check 👇 What does nums[-5] return?

Ep 01 on @codenest. Save it for revision and follow for Ep 02: slicing.

#python #datastructures #algorithms #dsa #pythonprogramming #codinginterview
#computerscience #learnpython #csstudent #softwaredeveloper #programmingtips
```

## Checks before you publish

- [ ] Every code line runs in a real Python REPL and prints exactly what's shown
- [ ] No text in the bottom 420 px or the right 140 px (preview on a phone)
- [ ] The cover frame (hook) is exported
- [ ] The quiz question in the caption has one correct answer (`10`)
