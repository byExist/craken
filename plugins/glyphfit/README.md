<h1 align="center">glyphfit</h1>

<p align="center">
  On-demand image downscaling for Claude vision — prefix <code>Read</code> with <code>shrink:</code> to shed pixels while keeping text legible.
</p>

<p align="center">
  A Claude Code plugin · macOS · Linux · Windows
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why glyphfit?

Claude downsizes every image before billing — to a long edge of ~1568px and ~1.15 megapixels at most — then charges roughly:

```
tokens ≈ (resized width × height) / 750   # capped at ~1,600 tokens / image
```

So a 3680×2382 screenshot doesn't cost ~11,700 tokens: Claude first shrinks it under the cap, to about **~1,530 tokens**. But that built-in resize is **content-blind** — it scales by raw pixels with no idea how small the text is. An image that already fits under the cap, or one you read many times, still carries pixels you don't need to read the text.

glyphfit downscales with text in mind: it measures where the smallest text line sits and resizes so that line still lands at a readable floor. When the output stays **under Claude's ~1568px / 1.15MP cap**, token cost drops in proportion to the pixels shed — e.g. a 1024×768 text screenshot at floor 18 lands near 635×476, roughly **−60% tokens** in that case, with no visible loss of legibility.

**Where it helps:** mid-size screenshots already at or under the cap (pixel savings pass straight to tokens), and images read repeatedly (the shrink is cached). **Where it won't:** a huge screenshot still above the cap *after* shrinking — Claude was going to resize it to ~1.15MP regardless, so there's nothing to save until glyphfit's output drops below that envelope.

## Installation

glyphfit runs its image pipeline through [uv](https://docs.astral.sh/uv/), so uv must be installed and on your `PATH`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux — see the uv docs for Windows
```

Then add and install the plugin:

```bash
/plugin marketplace add byExist/plugins
/plugin install glyphfit@plugins
```

On first session, uv provisions the dependencies (Pillow, RapidOCR) into a local virtualenv; the text-detection model (~50 MB) is downloaded once on the first `shrink:` read.

## Usage

Once installed, there's nothing to do. Read images with Claude as usual, and Claude picks based on the task — it reads a downscaled copy when the goal is reading text, and the original when design or pixel accuracy matters.

That choice comes from a hook, not a separate skill. The first time Claude reads an image in a session, glyphfit injects a one-time note ("shrink text, keep design at full size") into Claude's context, so the right call usually happens without you asking.

To steer it yourself:

- **Force a downscale** — say something like "read it shrunk" and Claude reads the reduced copy.
- **Force the original** — say "read it at full resolution," or tell Claude pixel accuracy matters.
- **Turn it off** — disable `enabled` via `/plugin config glyphfit`, and every `Read` passes through untouched.

## How it works

When it intercepts a `shrink:`-prefixed `Read`, glyphfit doesn't scale by a fixed ratio — it shrinks **only until the smallest glyph reaches the readable floor**:

1. **Detect text lines** — RapidOCR (DBNet) locates text lines. It doesn't *recognize* the characters (recognition is off → ~70% less cost), only measures each line box's height in px.
2. **Pick the basis height** — the bottom `outlier_percentile`% of heights (default 5%) are dropped as specks/noise; the next-smallest line's height becomes the basis.
3. **Compute the scale** — `scale = floor / basis` (capped at 1.0): the ratio that lands the smallest non-noise line at `floor_char_height_px` (default 18px). If it's already larger, nothing shrinks.
4. **Resize once** — a single Lanczos downscale, saved as lossless WebP in the cache. The next read of the same image + settings is a cache hit (~100 ms).

If no text is detected (photos, icons, diagrams), the original is returned unchanged. Because recognition is off, the script (hangul, Han, etc.) can't be known, so the per-script `floor_char_height_px` is set in configuration.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `floor_char_height_px` | `18` | Minimum line height (px) for the smallest non-outlier glyph in the output. Recommended: **12** (latin only), **18** (hangul/kana, default), **24** (simplified CJK), **32** (traditional CJK). |
| `outlier_percentile` | `5` | Bottom N% of detected char heights are discarded as outliers. |
| `min_pixels_for_action` | `200000` | Images smaller than this are passed through unchanged even with `shrink:`. |
| `enabled` | `true` | Toggle the whole pipeline. When off, `shrink:` is stripped but the original is returned. |

Set via `/plugin config glyphfit`.

## Trade-offs

- **Set `floor_char_height_px` to match your content's script.** Korean/Japanese needs ~18, Chinese characters need ~24. Default is safe for Korean.
- **First-run cost, in two parts.** On the first session, `uv sync` installs the dependencies (Pillow, ONNX Runtime, RapidOCR — tens of MB, slower on a cold cache). On the first `shrink:` read, RapidOCR fetches its ~50 MB detection model once. Both are one-time; cached reads after that are ~100 ms.
- **`shrink:` can be a no-op.** The original is returned unchanged when the image has no detectable text (photos, icons, diagrams), is already small (under ~200k px), or its text already sits at or above the floor.
- **Cache hits are nearly free.** Same image + same settings hits the cache in ~100 ms.

## License

MIT.
