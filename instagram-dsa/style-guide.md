# Visual style guide

This is an original visual system for a dark-green-background Reels page that teaches data
structures and algorithms in Python. Every value here is defined once in
[`engine/reelkit.py`](engine/reelkit.py) (`COLORS`, `FONT_FILES`, `SAFE_*`), so changing
the brand there updates every video.

## 1. Canvas and safe areas

| Property | Value |
|---|---|
| Resolution | 1080 × 1920 (9:16), 30 fps, H.264, yuv420p |
| Length | 25–45 s. One concept per Reel. |
| Safe content box | x 80–940, y 250–1500 |
| Top 250 px | Reserved for Instagram's header. Only the handle goes here. |
| Bottom 420 px | Reserved for the caption, audio label and buttons. Nothing important goes here. |
| Right 140 px | The like, comment and share buttons sit here (mostly below y≈1100). Keep code and text out. |

Run `Scene(..., debug_safe_area=True)` to draw the box while you lay out a scene.

## 2. Colour themes

Every video uses one theme, set by the `REEL_THEME` environment variable. The
default is **board**, a dark chalkboard green. See [`samples/theme-options.png`](samples/theme-options.png)
for the same frames in each theme.

```bash
python episodes/ep01_list_indexing.py                     # board: dark green (default)
REEL_THEME=green python episodes/ep01_list_indexing.py    # light green
REEL_THEME=white python episodes/ep01_list_indexing.py    # original white
```

| Token | green | board (default) | white | Use |
|---|---|---|---|---|
| `bg` | `#C3EBCF` | `#123A2B` | `#FFFFFF` | Canvas |
| `surface` | `#FFFFFF` | `#1B4A38` | `#FFFFFF` | Cells, slots, recap card: the data sits on this |
| `ink` | `#0B2316` | `#F1F6F3` | `#111827` | Headings, values |
| `muted` | `#3B6B50` | `#A3C4B3` | `#6B7280` | Secondary text, the handle |
| `card` | `#F3FBF5` | `#0C2C20` | `#F4F5F7` | Code card |
| `primary` | `#1D4ED8` | `#FDE047` | `#2563EB` | **The thing to look at now** |
| `accent` | `#C2410C` | `#FB923C` | `#F59E0B` | A second concept on screen |
| `good` / `bad` | `#047857` / `#B91C1C` | `#4ADE80` / `#F87171` | `#059669` / `#DC2626` | Output / errors |

The board theme uses light text with yellow as the focus colour, which reads like
chalk on a board. The light green theme uses darker blue, orange and red than the
white theme, so headline text keeps enough contrast. To add your own theme, copy an
entry in `THEMES` in `engine/reelkit.py` and change its values.

Rules:
- **At most two highlight colours on screen at once.** `primary` means focus;
  `accent` means "the other one".
- Highlight colours always mean the same thing within an episode.
- Colour is never the only signal. Pair it with a lift, an arrow or a label.

## 3. Typography

Both fonts are free under the SIL Open Font License, so they're safe for commercial use.

| Role | Font | Size (px at 1080 wide) |
|---|---|---|
| Hook title | Inter ExtraBold | 84–96 |
| Section header | Inter ExtraBold | 50 |
| Headline, "what's happening now" | Inter Bold | 50 |
| Voice-over captions | Inter ExtraBold, spoken word on a blue pill | 50 |
| Supporting text | Inter Medium | 36–44 |
| Code | JetBrains Mono Medium | 36–42 (never below 34) |
| Index labels, pointers | JetBrains Mono Bold | 34 |

- Keep headlines to **one line and about 35 characters or fewer**. If one needs two
  lines, split it into two beats.
- Voice-over captions are split automatically into balanced chunks of up to about 24
  characters, so there are never lonely one-word captions.
- Code lines should fit in **about 36 monospace characters** at 36 px. Shorten variable
  names rather than shrinking the font.

## 4. Layout template, top to bottom

```
 y 100   @codenest (left)
 y 290   Section header           ("Lists · indexing")
 y 420   Headline / current idea  (changes with each beat)
 y 600–950  VISUAL ZONE           (array cells, nodes, tree, graph)
 y 960–1440 CODE ZONE             (REPL card, grows line by line)
 y 1478  CAPTIONS                 (voice-over subtitles, current word in blue)
```

The visual sits above the code because viewers look at the picture first, then read
the code that produced it. Keep that order in every episode, so the page has a
recognisable layout.

## 5. Motion language

| Motion | Meaning | Engine |
|---|---|---|
| Pop with a slight overshoot (`ease_out_back`), staggered 0.12 s | Data is created | `ArrayRow` |
| Fade and rise 24 px over 0.35 s | Text arrives | Every `Element` |
| Typewriter at 28 chars/s with a blue caret | Code is being written | `CodeBlock` |
| Cell lifts 18 px and fills with colour | This element is being accessed | `Highlight` |
| Arrow glides between cells (0.4 s ease-in-out) and bobs gently | A pointer or iterator moves | `Pointer` |
| Dashed red box plus a shake | An invalid position or error | `ArrayRow.ghost` |
| Orange underline swipes under a keyword | The key term of the episode | `Title.highlight` |

- **One movement at a time.** Start a new animation only after the previous one has
  settled, about 0.4 s later.
- Show the visual change **at the same moment** the output appears in the code card,
  so cause and effect line up.

## 6. Pacing (voice-first; ~35–40 s with narration)

The narration sets the clock (Kokoro `af_heart` at speed 1.05, with 0.22 s between
sentences and 0.35 s between beats). Use `pause_after` on a beat to give viewers
time to read an output. The proportions below still apply.

| Beat | Time | Content |
|---|---|---|
| Hook | 0–3.5 s | A question or promise, plus the episode tag. No code yet. |
| Setup | 3.5–7 s | Type the data, build the visual |
| Rule | 7–10 s | One sentence, e.g. "counting starts at 0" |
| Example 1 | 10–13 s | Code, highlight, output |
| Example 2 / twist | 13–19 s | A second rule or the counter-intuitive case |
| Gotcha | 19–24 s | The common mistake or error |
| Recap | 24–28 s | Three rows, code on the left and meaning below |
| CTA | 28–31 s | "Next episode: …". This drives follows and series binge-watching. |

## 7. Branding

- The handle **@codenest** appears on every frame, top left. There's no progress bar. Set the handle in `HANDLE` in `engine/episodes/common.py`.
- **Voice:** one consistent narrator across the series (`af_heart` by default). Read
  code as words ("nums of two", "minus one"), not symbols.
- No episode tag or series name on screen: the hook opens with the title alone.
- Cover image: export the hook frame (`scene.still(1.5, ...)`) and use it as the Reel
  cover, so the grid looks consistent.
