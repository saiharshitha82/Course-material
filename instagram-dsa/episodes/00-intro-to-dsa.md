# Episode 00: Intro to DSA (pin this first)

- **Status:** rendered. Source: [`engine/episodes/ep00_intro_to_dsa.py`](../engine/episodes/ep00_intro_to_dsa.py)
- **Length:** 55.8 s
- **Purpose:** the page's welcome Reel. It explains what data structures and
  algorithms are, why they matter (speed and interviews), and what @codenest will
  teach, then sends viewers to Episode 01. **Pin it as the first Reel on the grid.**

## Voice-over and storyboard

| Beat | Time | Voice-over | On screen |
|---|---|---|---|
| hook | 0.4–5.1 | "What are data structures and algorithms? And why does every coding interview ask about them?" | Title "What is **DSA**, and why learn it?", sub "the skill behind every coding interview" |
| setup | 5.7–10.2 | "A data structure is a way to organise data, so your code can use it quickly." | Five scattered values drift, then snap into a neat list |
| types | 10.9–16.6 | "Lists. Grids. Trees. Graphs. Each one organises data in its own way." | A list, a grid, a tree and a graph pop in, one per word |
| algo | 17.3–25.1 | "An algorithm is a step-by-step recipe for solving a problem. Like searching a list: check each item, until you find the one you want." | Pointer "40?" checks 10, 20, 30 (amber), then 40 turns green; `nums.index(40)` → `3` |
| why | 25.9–32.0 | "With a million sorted items, checking one by one can take a million steps. Binary search needs just twenty." | Two bars: a full red "1,000,000 steps" against a green sliver, "20 steps" |
| interview | 32.8–35.3 | "That's why coding interviews are full of DSA." | "Coding interviews test exactly this" |
| learn | 36.0–43.1 | "Here, you'll learn it all in Python, visually. From lists and arrays, to stacks, linked lists, trees, graphs, searching, and sorting." | Roadmap of 15 topic chips popping in, with "Lists" highlighted as the start |
| format | 43.9–48.8 | "One idea per reel, in under a minute. With real code, and a quiz in every caption." | "Every reel" card |
| cta | 49.7–54.6 | "Start with episode one: list indexing. Follow, and let's master DSA together." | "Start here: Ep 01: List **indexing**" |

Accuracy notes:
- `list.index` scans from the start, so it's a linear search (verified: `nums.index(40)` → `3`).
- Binary search on 1,000,000 sorted items needs at most 20 comparisons, because
  log₂(1,000,000) ≈ 19.9. A test run in Python found 20 for the worst case.
- "Under a minute": every Season 1 episode runs 38–51 s.

## Instagram caption (paste-ready)

```
New here? Start with this 👋

DSA = Data Structures + Algorithms 🧠

📦 Data structure → how you organise data (lists, grids, trees, graphs)
⚙️ Algorithm → the step-by-step recipe that works on it

Why care? Searching 1,000,000 sorted items:
❌ one by one: up to 1,000,000 steps
✅ binary search: just 20 steps

That's why every coding interview tests DSA.

On @codenest you'll learn it all in Python, visually:
lists → arrays → stacks → linked lists → hash tables → trees → graphs → sorting & searching

🎬 One idea per reel, under a minute
💻 Real code with exact outputs
❓ A quiz in every caption

Start with Ep 01: list indexing 👉 Follow so you don't miss a step!

#python #dsa #datastructures #algorithms #learnpython #codinginterview #computerscience #csstudent #softwaredeveloper #programming #coding
```

**Pinned comment:**

```
Which topic are you most excited for? Lists, trees, graphs or sorting? 👇
```

## Checks before you publish

- [x] Every claim was checked in Python (`list.index`, binary-search step count)
- [ ] Post it first and **pin** it to the top of the grid
- [ ] Set the hook frame as the cover
