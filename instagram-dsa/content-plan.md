# Content plan: DSA in Python

**Audience:** computer science students and aspiring software developers who already
know basic Python syntax.
**Promise:** "One data structure or algorithm idea, visualised, in about 30 seconds."
**Cadence (suggested):** 4 Reels a week, plus 1 carousel recap at the end of each
season. Each season runs 2–3 weeks.

Each episode teaches **one** idea. If the outline needs the word "and", split it
into two episodes.

## Season 1: Lists and arrays

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 01 | List indexing in 30 s ✅ *(rendered)* | Cells with positive and negative indices | `IndexError` one past the end |
| 02 | List slicing `nums[1:4]` | Two brackets sliding over the cells, end excluded | The end index is *exclusive* |
| 03 | Slicing with a step, `[::2]` and `[::-1]` | A pointer hopping by step | `[::-1]` makes a copy, `reverse()` doesn't |
| 04 | `append` vs `insert(0, x)` | Every cell shifts right on insert | `insert(0)` is O(n) |
| 05 | `pop()` vs `pop(0)` | Shift-left animation | Use `deque` for queues (teaser for S3) |
| 06 | Copy vs reference: `b = a` | Two names, arrows to one list | `a[:]` / `copy()` |
| 07 | Shallow vs deep copy | A nested list sharing an inner box | `copy.deepcopy` |
| 08 | List comprehensions, visualised | A conveyor belt: filter, then map | Readability limit |
| 09 | Lists vs arrays | Boxes holding pointers vs packed bytes | A list holds references |
| 10 | Python's `array` module | Typecode `'i'` and a fixed-width memory strip | `TypeError` on a mixed type |
| 11 | NumPy arrays | A vectorised op lighting up all cells at once | Fixed dtype, broadcasting |
| 12 | 2-D arrays and `shape` | A grid with row/column indices | `[[0]*3]*3` aliasing bug |
| 13 | Row-major memory layout | A 2-D grid unrolling into 1-D memory | Why the loop order matters |

## Season 2: Built-in collections

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 14 | Tuples: frozen lists | A lock icon on the cells | `(1)` vs `(1,)` |
| 15 | Tuple unpacking and swaps | Values flying into variables | `a, b = b, a` |
| 16 | Sets: why `in` is fast | Values dropping into hash buckets | No order, no duplicates |
| 17 | Set operations | Animated Venn diagram for `|`, `&`, `-`, `^` | |
| 18 | Dictionaries: key → value | Key cards with arrows to values | Keys must be hashable |
| 19 | `get`, `setdefault`, `defaultdict` | A missing key, `KeyError` vs a default | |
| 20 | Counting with `Counter` | A tally bar chart growing | |

## Season 3: Linear structures

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 21 | Stack (LIFO) with a list | A vertical tower, push and pop | Peek on an empty stack |
| 22 | Stack use case: balanced brackets | Characters pushed and popped | |
| 23 | Queue (FIFO) with `deque` | A horizontal lane, enqueue and dequeue | Why not `list.pop(0)` |
| 24 | Linked list: nodes and pointers | Node boxes with `next` arrows | No indexing, O(n) access |
| 25 | Insert / delete in a linked list | An arrow re-pointing | Losing the rest of the list |
| 26 | Reverse a linked list | Three pointers, prev/curr/next | Classic interview question |
| 27 | Doubly linked lists | Two-way arrows | |

## Season 4: Hashing

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 28 | What is a hash function? | A key going through a "blender" to a bucket number | Same input gives the same output |
| 29 | Collisions and chaining | Two keys landing in one bucket | |
| 30 | Open addressing | Probing to the next slot | |
| 31 | Load factor and resizing | A table doubling and rehashing | Amortised O(1) |

## Season 5: Complexity (placed before trees, so later episodes can quote Big-O)

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 32 | Big-O in 30 s | Curves racing as n grows | Constants are dropped |
| 33 | O(1) vs O(n) vs O(n²) with real code | Counting operations | |
| 34 | O(log n): halving | A list being chopped in half | |
| 35 | Space complexity | A memory bar growing | Recursion stack |
| 36 | Big-O of Python built-ins | A cheat-sheet card | `x in list` vs `x in set` |

## Season 6: Searching and sorting

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 37 | Linear search | A pointer walking | |
| 38 | Binary search | lo/mid/hi pointers | The list must be sorted; off-by-one |
| 39 | `bisect` module | | |
| 40 | Bubble sort | Neighbouring bars swapping | O(n²) |
| 41 | Selection sort | Min-finder sweep | |
| 42 | Insertion sort | A card-hand animation | Fast on nearly sorted data |
| 43 | Merge sort | Split tree, then merge | O(n log n), extra space |
| 44 | Quick sort | Pivot partition | Worst case O(n²) |
| 45 | `sorted()` and `key=` | | Timsort, stable |

## Season 7: Trees

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 46 | Tree vocabulary | Root, leaves, height, depth | |
| 47 | Binary tree in Python | `Node(left, right)` | |
| 48 | DFS traversals: pre/in/post | A visit-order path | |
| 49 | BFS / level order | Wave by wave, with a queue | |
| 50 | Binary search tree insert | A value sliding down left/right | |
| 51 | BST search and why balance matters | A degenerate "stick" tree | O(n) worst case |
| 52 | Heaps and `heapq` | An array ↔ tree mapping | Min-heap only |

## Season 8: Graphs

| # | Title / hook | Key visual | Gotcha / twist |
|---|---|---|---|
| 53 | Graph basics | Nodes and edges, directed/undirected | |
| 54 | Adjacency list vs matrix | The same graph in two forms | Space trade-off |
| 55 | BFS on a graph | A frontier expanding | `visited` set |
| 56 | DFS on a graph | Going deep, then backtracking | Recursion limit |
| 57 | Shortest path (Dijkstra) | Distance labels updating | No negative weights |
| 58 | Topological sort | A dependency order | Cycles break it |

## Later seasons (backlog)

Recursion and the call stack · two pointers · sliding window · prefix sums ·
dynamic programming (Fibonacci memo, coin change, knapsack) · greedy algorithms ·
tries · union-find · bit manipulation · LRU cache.

## Non-Reel formats

- **Carousel** at the end of each season: recap cards built from each episode's
  `Card` frame.
- **Quiz Reel** after every 3 episodes: "What does this print?" Show the code, pause
  3 s, then reveal. Comment-bait like this tends to drive engagement.
- **Stories:** a poll on the next topic, plus a "this or that" question (list vs
  tuple).
