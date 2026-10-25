# DSA in Python: an Instagram Reels production kit

A complete workflow for a page that teaches Python data structures and algorithms
through short, animated, white-background Reels. It starts at lists and indexing,
not `print()`.

| File | What it is |
|---|---|
| [`reference-analysis.md`](reference-analysis.md) | Status of the reference Reel analysis (**not yet done**, because Instagram was unreachable) and what to send so it can be done |
| [`style-guide.md`](style-guide.md) | Original brand: colours, fonts, safe areas, layout, motion language, pacing |
| [`content-plan.md`](content-plan.md) | 58 episodes across 8 seasons, from lists to graphs, each with a hook, visual and gotcha |
| [`templates/episode-template.md`](templates/episode-template.md) | Fill-in script, storyboard and caption template |
| [`episodes/`](episodes/) | Finished episode scripts |
| [`engine/reelkit.py`](engine/reelkit.py) | Python animation engine (Pillow + ffmpeg) that renders the videos |
| [`samples/`](samples/) | Rendered Episode 01 and its key frames |

## The production workflow (per episode, ~1–2 hours once practised)

```
1. PICK      next row in content-plan.md
2. SCRIPT    copy templates/episode-template.md → episodes/NN-topic.md
             write the code first, then run it in a real REPL and paste exact outputs
3. STORYBOARD fill the timing table: one idea per 2–4 s, visual change == output moment
4. BUILD     copy engine/episodes/ep01_list_indexing.py → epNN_topic.py, edit timings
5. REVIEW    python episodes/epNN_topic.py --stills   → check PNGs for overlap/safe area
6. RENDER    python episodes/epNN_topic.py            → renders/epNN_topic.mp4 (~30 s)
7. AUDIO     (optional) record the voice-over from the script; add it and quiet
             music in CapCut / InShot / Premiere. Add auto-captions if using a VO.
8. PUBLISH   upload, set the hook frame as cover, paste the caption, pin a comment
             with the answer to the quiz question after a few hours
9. LEARN     after 48 h log views, average watch %, saves and shares; adjust hooks
```

## Rendering

Requirements: Python 3.9+, Pillow, ffmpeg, and the Inter and JetBrains Mono fonts. Both
fonts are free under the OFL. If they aren't installed system-wide, drop the `.otf`
and `.ttf` files into `engine/fonts/`.

```bash
pip install pillow
cd instagram-dsa/engine
python episodes/ep01_list_indexing.py --stills   # key frames → ../renders/*.png
python episodes/ep01_list_indexing.py            # full MP4  → ../renders/*.mp4
```

A 31 s episode renders in about 30 s on a laptop. `renders/` is git-ignored, so keep
the finished uploads in `samples/` or your own drive.

### Engine building blocks

| Element | Use |
|---|---|
| `Title`, `Text`, `Pill` | Hook, captions, episode tags (`Title.highlight` adds a coloured, underlined keyword) |
| `CodeBlock` + `CodeLine` | REPL card with a typewriter effect, syntax highlighting, outputs, errors and line focus |
| `ArrayRow` + `Highlight` | List/array cells with pop-in, index labels, highlighted access, and an out-of-range ghost cell |
| `Pointer` | An arrow and label that glide between cells (iterators, two pointers, binary search) |
| `Card` | Recap card |
| `Brand` | Handle and progress bar on every frame |

Every element takes `start` and `end` in seconds and animates in and out by itself, so
an episode file is just a timeline. Later seasons need new primitives: stack tower,
linked-list nodes, tree, graph and bar-chart sorting. Each one is a single class
following the `ArrayRow` pattern.

## Before publishing

1. **Handle:** change `@yourhandle` in each episode file (or make it a constant).
2. **Series name:** "DSA in Python" is a placeholder. Use your page's name.
3. **Reference style:** once you send screenshots or a screen recording of the
   reference Reel, the pacing and motion can be tuned to match its approach.
