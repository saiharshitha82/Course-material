# DSA in Python: an Instagram Reels production kit

A complete workflow for a page that teaches Python data structures and algorithms
through short, animated Reels on a dark chalkboard-green background (light-green and
white themes also included). It starts at lists and indexing,
not `print()`.

| File | What it is |
|---|---|
| [`reference-analysis.md`](reference-analysis.md) | Status of the reference Reel analysis (**not yet done**, because Instagram was unreachable) and what to send so it can be done |
| [`style-guide.md`](style-guide.md) | Original brand: colour themes (dark green default), fonts, safe areas, layout, motion language, pacing |
| [`content-plan.md`](content-plan.md) | 51 episodes across 8 seasons, from lists to graphs, each with a hook, visual and gotcha |
| [`templates/episode-template.md`](templates/episode-template.md) | Fill-in script, storyboard and caption template |
| [`episodes/`](episodes/) | Episode scripts 01–06: voice-over, storyboard, Instagram caption, quiz |
| [`engine/`](engine/) | Python animation engine (Pillow + ffmpeg + Kokoro TTS) and one script per episode |
| [`samples/`](samples/) | Rendered Episodes 01–06 (MP4 with voice-over and captions), their `.srt` files, and key frames |

## The production workflow (per episode, ~1–2 hours once practised)

```
1. PICK      next row in content-plan.md
2. SCRIPT    copy templates/episode-template.md → episodes/NN-topic.md
             write the code first, then run it in a real REPL and paste exact outputs
3. STORYBOARD write the voice-over as beats; one idea per beat, visual change == the spoken word
4. BUILD     copy the closest engine/episodes/epNN_*.py → epNN_topic.py, edit beats + visuals
5. REVIEW    python episodes/epNN_topic.py --stills   → check PNGs for overlap/safe area
6. RENDER    python episodes/epNN_topic.py            → renders/epNN_topic.mp4 (~30 s)
7. AUDIO     voice-over + burned-in captions are generated automatically (see below);
             optionally add quiet music in the Instagram app or CapCut
8. PUBLISH   upload, set the hook frame as cover, paste the caption, pin a comment
             with the answer to the quiz question after a few hours
9. LEARN     after 48 h log views, average watch %, saves and shares; adjust hooks
```

## Rendering

Requirements: Python 3.9+, ffmpeg, and the Inter and JetBrains Mono fonts. Both
fonts are free under the OFL. If they aren't installed system-wide, drop the `.otf`
and `.ttf` files into `engine/fonts/`.

```bash
pip install pillow kokoro-onnx soundfile
cd instagram-dsa/engine
python voice.py --download                       # one-time: ~200 MB voice model → engine/models/
python episodes/ep01_list_indexing.py --stills   # key frames → ../renders/*.png
python episodes/ep01_list_indexing.py            # MP4 with voice + captions → ../renders/
```

Set `REEL_THEME=green` (light green) or `REEL_THEME=white` before the command to render in a
different colour theme (see the style guide).

Each render writes three files to `renders/`:

| File | Use |
|---|---|
| `epNN_*.mp4` | Upload this. Voice-over muxed in at about -14 LUFS, captions burned in. |
| `epNN_*.wav` | Voice-over alone, if you want to remix it with music in an editor |
| `epNN_*.srt` | Caption file for CapCut, YouTube Shorts or TikTok re-uploads |

A 38 s episode renders in about 40 s on a laptop. The first render also synthesises
the voice, which takes a few seconds per sentence. After that the audio is cached per
sentence, so changing visuals doesn't re-synthesise anything.

### Voice-over and captions

- **Voice:** [Kokoro-82M](https://github.com/thewh1teagle/kokoro-onnx), an open TTS
  model licensed Apache-2.0, so commercial use is fine. It runs offline. The default
  voice is `af_heart`. Others include `am_michael`, `bf_emma` and `bm_george`; set
  `Narration(voice=..., speed=...)`. To use your own voice instead, record each
  sentence and swap the cached WAVs, or replace the audio track in an editor using
  the `.srt` timings.
- **Timing is voice-first:** an episode lists its narration as named *beats*.
  `nar.layout()` synthesises them and places them back to back, and the visuals are
  scheduled from `B["beat"].start` / `.at(i)`. Edit a sentence and the whole video
  re-times itself.
- **Code read aloud:** give a `(shown, spoken)` pair, e.g.
  `("nums[2] is 30.", "nums of two is thirty.")`. The caption shows the code and the
  voice says the words.
- **Captions:** short phrases of up to about 24 characters at the bottom of the safe
  area. The word being spoken is highlighted in the theme's focus colour (yellow on dark green).
- **Music:** add it in the Instagram app (licensed library) or in your editor, at
  about 10–15% volume under the voice.

`renders/` is git-ignored, so keep the finished uploads in `samples/` or your own drive.

### Engine building blocks

| Element | Use |
|---|---|
| `Title`, `Text`, `Pill` | Hook, captions, episode tags (`Title.highlight` adds a coloured, underlined keyword) |
| `CodeBlock` + `CodeLine` | REPL card with a typewriter effect, syntax highlighting, outputs, errors and line focus |
| `ArrayRow` + `Highlight` | List/array cells with pop-in, index labels, highlighted access, and an out-of-range ghost cell |
| `Pointer` | An arrow and label that glide between cells (iterators, two pointers, binary search) |
| `Card` | Recap card |
| `Brand` | The @codenest handle, top left on every frame |
| `Narration`, `Subtitles` (`voice.py`) | Voice-over beats, audio mixdown, `.srt`, burned-in word-highlight captions |
| `ListAnim` (`structures.py`) | A list/array that changes over time: `append`, `insert`, `pop`, `set`, `set_all`, `extend`, `reject`, and highlights; can also render as a joined memory strip with addresses and byte ticks |
| `RowPointer`, `Bracket`, `Hops`, `FlyCells` | Pointers, slice brackets with an excluded stop, step arcs, and cells copying into a new list |
| `RefDiagram` | Slots with arrows to objects in memory (references, aliasing) |
| `Grid` | 2-D array with row/column labels, cell/row/column highlights, and value changes |

Episodes share their hook, header, recap, CTA and render steps through
`engine/episodes/common.py`, so a new episode file only contains its own script and
visuals.

Every element takes `start` and `end` in seconds and animates in and out by itself, so
an episode file is just a timeline. Later seasons need new primitives: stack tower,
linked-list nodes, tree, graph and bar-chart sorting. Each one is a single class
following the `ListAnim` / `Grid` pattern.

Render all of Season 1:

```bash
for f in episodes/ep0*.py; do python "$f"; done
```

## Before publishing

1. **Handle:** `@codenest` is set once in `engine/episodes/common.py` (`HANDLE`); Episode 01 sets it in its own file.
2. **Reference style:** once you send screenshots or a screen recording of the
   reference Reel, the pacing and motion can be tuned to match its approach.
