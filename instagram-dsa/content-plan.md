# Content plan: DSA in Python

**Audience:** computer science students and aspiring software developers who already
know basic Python syntax.
**Promise:** "One data structure or algorithm idea, visualised, in about 30 seconds."
**Cadence (suggested):** 4 Reels a week, plus 1 carousel recap at the end of each
season. Each season runs 2–3 weeks.

Each episode teaches **one** idea. If the outline needs the word "and", split it
into two episodes.

## Season 1: Lists and arrays ✅ (all rendered)

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 00 | Intro: what is DSA, and why learn it? ✅ *(pin first)* | Scattered values snap into a list; list/grid/tree/graph montage; a million vs 20 steps; topic roadmap | Binary search: at most 20 steps for 1,000,000 sorted items |
| 01 | List indexing ✅ | Cells with positive and negative indices | `IndexError` one past the end |
| 02 | Slicing and list operations ✅ | Bracket over `[1:4]`, step hops, cells flying into new lists; append/insert/pop | Stop is excluded; `insert(0)` shifts every item |
| 03 | Lists vs arrays ✅ | References to scattered objects vs a packed memory strip | Address = start + i × size |
| 04 | Python's `array` module ✅ | Typed memory strip with byte ticks | `TypeError` on a float in an `'i'` array |
| 05 | NumPy arrays ✅ | Loop pointer one by one vs all cells at once | `list * 2` repeats instead of doing maths |
| 06 | Multidimensional arrays ✅ | 2-D grid with row/column highlights | `[[0] * 3] * 3` aliasing bug |

## Season 2: Built-in collections

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 07 | Tuples: frozen lists | A lock icon on the cells | `(1)` vs `(1,)` |
| 08 | Tuple unpacking and swaps | Values flying into variables | `a, b = b, a` |
| 09 | Sets: why `in` is fast | Values dropping into hash buckets | No order, no duplicates |
| 10 | Set operations | Animated Venn diagram for `|`, `&`, `-`, `^` | |
| 11 | Dictionaries: key → value | Key cards with arrows to values | Keys must be hashable |
| 12 | `get`, `setdefault`, `defaultdict` | A missing key, `KeyError` vs a default | |
| 13 | Counting with `Counter` | A tally bar chart growing | |

## Season 3: Linear structures

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 14 | Stack (LIFO) with a list | A vertical tower, push and pop | Peek on an empty stack |
| 15 | Stack use case: balanced brackets | Characters pushed and popped | |
| 16 | Queue (FIFO) with `deque` | A horizontal lane, enqueue and dequeue | Why not `list.pop(0)` |
| 17 | Linked list: nodes and pointers | Node boxes with `next` arrows | No indexing, O(n) access |
| 18 | Insert / delete in a linked list | An arrow re-pointing | Losing the rest of the list |
| 19 | Reverse a linked list | Three pointers, prev/curr/next | Classic interview question |
| 20 | Doubly linked lists | Two-way arrows | |

## Season 4: Hashing

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 21 | What is a hash function? | A key going through a "blender" to a bucket number | Same input gives the same output |
| 22 | Collisions and chaining | Two keys landing in one bucket | |
| 23 | Open addressing | Probing to the next slot | |
| 24 | Load factor and resizing | A table doubling and rehashing | Amortised O(1) |

## Season 5: Complexity (placed before trees, so later episodes can quote Big-O)

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 25 | Big-O in 30 s | Curves racing as n grows | Constants are dropped |
| 26 | O(1) vs O(n) vs O(n²) with real code | Counting operations | |
| 27 | O(log n): halving | A list being chopped in half | |
| 28 | Space complexity | A memory bar growing | Recursion stack |
| 29 | Big-O of Python built-ins | A cheat-sheet card | `x in list` vs `x in set` |

## Season 6: Searching and sorting

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 30 | Linear search | A pointer walking | |
| 31 | Binary search | lo/mid/hi pointers | The list must be sorted; off-by-one |
| 32 | `bisect` module | | |
| 33 | Bubble sort | Neighbouring bars swapping | O(n²) |
| 34 | Selection sort | Min-finder sweep | |
| 35 | Insertion sort | A card-hand animation | Fast on nearly sorted data |
| 36 | Merge sort | Split tree, then merge | O(n log n), extra space |
| 37 | Quick sort | Pivot partition | Worst case O(n²) |
| 38 | `sorted()` and `key=` | | Timsort, stable |

## Season 7: Trees

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 39 | Tree vocabulary | Root, leaves, height, depth | |
| 40 | Binary tree in Python | `Node(left, right)` | |
| 41 | DFS traversals: pre/in/post | A visit-order path | |
| 42 | BFS / level order | Wave by wave, with a queue | |
| 43 | Binary search tree insert | A value sliding down left/right | |
| 44 | BST search and why balance matters | A degenerate "stick" tree | O(n) worst case |
| 45 | Heaps and `heapq` | An array ↔ tree mapping | Min-heap only |

## Season 8: Graphs

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 46 | Graph basics | Nodes and edges, directed/undirected | |
| 47 | Adjacency list vs matrix | The same graph in two forms | Space trade-off |
| 48 | BFS on a graph | A frontier expanding | `visited` set |
| 49 | DFS on a graph | Going deep, then backtracking | Recursion limit |
| 50 | Shortest path (Dijkstra) | Distance labels updating | No negative weights |
| 51 | Topological sort | A dependency order | Cycles break it |

## Later seasons (backlog)

Copy vs reference (`b = a`) · shallow vs deep copy · list comprehensions visualised · row-major memory layout · recursion and the call stack · two pointers · sliding window · prefix sums ·
dynamic programming (Fibonacci memo, coin change, knapsack) · greedy algorithms ·
tries · union-find · bit manipulation · LRU cache.

## Non-Reel formats

- **Carousel** at the end of each season: recap cards built from each episode's
  `Card` frame.
- **Quiz Reel** after every 3 episodes: "What does this print?" Show the code, pause
  3 s, then reveal. Comment-bait like this tends to drive engagement.
- **Stories:** a poll on the next topic, plus a "this or that" question (list vs
  tuple).
