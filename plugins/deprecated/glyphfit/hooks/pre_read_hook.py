#!/usr/bin/env python3
"""PreToolUse hook for Read: opt-in, text-aware image downscaling.

When `file_path` contains the `shrink:` marker, the hook downscales the image so its
smallest text line stays readable, caches the result, and rewrites `file_path` to
the cached copy via `updatedInput`. Other shrink: cases (non-image, disabled, too
small, no text, failure) pass through with the original path.

For a plain (non-`shrink:`) Read of an image, the hook stays out of the way but, on
the first such read in a session, injects a one-time note telling Claude when to
opt into `shrink:` — so the plugin guides its own usage without shipping a skill.
"""

import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cache  # noqa: E402

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif"}
SHRINK_PREFIX = "shrink:"
# Bump when the shrink pipeline changes in a way that invalidates cached outputs.
PIPELINE_VERSION = "1"

SHRINK_HINT = (
    "glyphfit is active, and you just read this image at full size. If you only needed "
    "the text in it, re-read it with a `shrink:` prefix (e.g. `shrink:/path/to/image.png`) "
    "to downscale it — cutting vision tokens while keeping text legible. From here on, add "
    "`shrink:` when the goal is reading text (screenshots, docs, logs, terminal/UI captures), "
    "and skip it (read the bare path) when pixel accuracy matters (design/layout review, "
    "visual diffs, photos, icons, diagrams). The choice is per-Read for every image this "
    "session; drop the prefix whenever you need full resolution."
)

DISABLED_HINT = (
    "glyphfit is disabled (its `enabled` option is off), so this `shrink:` was ignored "
    "— the prefix is stripped and the original image is returned at full size. Just read "
    "without the prefix; it has no effect while glyphfit is off. (If downscaling is "
    "wanted, the user can re-enable glyphfit via `/plugin config glyphfit`.)"
)


def _bool_env(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() not in ("0", "false", "no", "off")


def _int_env(name: str, default: int) -> int:
    try:
        return int(float(os.environ.get(name, "") or default))
    except (ValueError, OverflowError):
        return default


@dataclass(frozen=True)
class Config:
    enabled: bool
    outlier_percentile: int
    floor_char_height_px: int
    min_pixels: int

    @classmethod
    def from_env(cls) -> "Config":
        """Load options from CLAUDE_PLUGIN_OPTION_* env vars, clamped to sane
        ranges so a stray value can't crash the pipeline or yield a 1x1 image."""
        return cls(
            enabled=_bool_env("CLAUDE_PLUGIN_OPTION_ENABLED", True),
            outlier_percentile=max(1, min(50, _int_env("CLAUDE_PLUGIN_OPTION_OUTLIER_PERCENTILE", 5))),
            floor_char_height_px=max(1, _int_env("CLAUDE_PLUGIN_OPTION_FLOOR_CHAR_HEIGHT_PX", 18)),
            min_pixels=max(0, _int_env("CLAUDE_PLUGIN_OPTION_MIN_PIXELS_FOR_ACTION", 200_000)),
        )


def passthrough() -> NoReturn:
    """Emit nothing: Read proceeds with its original input."""
    sys.exit(0)


def emit_rewrite(new_path: str | Path, additional_context: str | None = None) -> NoReturn:
    """Allow the Read but rewrite its file_path to `new_path`."""
    spec: dict[str, Any] = {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {"file_path": str(new_path)},
    }
    if additional_context:
        spec["additionalContext"] = additional_context
    sys.stdout.write(json.dumps({"hookSpecificOutput": spec}))
    sys.stdout.flush()
    sys.exit(0)


def emit_context(text: str) -> NoReturn:
    """Inject additionalContext for Claude without touching the tool input — the
    Read runs unchanged, with the note added to the model's context."""
    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}
    }))
    sys.stdout.flush()
    sys.exit(0)


def read_event() -> dict[str, Any]:
    """Read and validate the Read event from stdin; pass through otherwise."""
    raw = sys.stdin.read()
    if not raw.strip():
        passthrough()
    try:
        event: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        passthrough()
    if event.get("tool_name") != "Read":
        passthrough()
    return event


def _hint_flag(session_id: str, kind: str) -> Path:
    # Session-scoped, throwaway markers → the temp dir (same home as the image
    # cache), not the persistent plugin-data dir.
    base = Path(tempfile.gettempdir()) / "glyphfit-hints"
    return base / f"{session_id.replace('/', '_')}.{kind}"


def _claim_once(session_id: str, kind: str) -> bool:
    """Claim the one-shot flag for (session, kind): True the first time, False if
    already claimed or the session/flag can't be tracked. Flags live in the temp
    dir and are left for the OS to reap, same as the image cache."""
    if not session_id:
        return False
    flag = _hint_flag(session_id, kind)
    if flag.exists():
        return False
    try:
        flag.parent.mkdir(parents=True, exist_ok=True)
        flag.touch()
    except OSError:
        return False
    return True


def maybe_hint(file_path: str, session_id: str) -> NoReturn:
    """Plain Read: on the first image of the session, inject one-time `shrink:`
    guidance; otherwise pass through untouched."""
    if Path(file_path).suffix.lower() in IMAGE_EXTS and _claim_once(session_id, "enabled"):
        emit_context(SHRINK_HINT)
    passthrough()


def disabled_hint(session_id: str) -> str | None:
    """One-time note (per session) that `shrink:` is a no-op while the plugin is
    off — attached via emit_rewrite on a shrink: call; None after the first."""
    return DISABLED_HINT if _claim_once(session_id, "disabled") else None


def shrink_source(file_path: str) -> Path:
    """Extract the real path after the `shrink:` marker; hand back the bare path
    for a non-image. The marker may appear mid-path, not only as a prefix, so
    locate it anywhere and take everything after it as the real path."""
    marker = file_path.find(SHRINK_PREFIX)
    stripped = file_path[marker + len(SHRINK_PREFIX):].strip() if marker != -1 else ""
    if not stripped:
        passthrough()
    src = Path(stripped)
    if src.suffix.lower() not in IMAGE_EXTS or not src.is_file():
        emit_rewrite(src)  # shrink: on a non-image → hand back the bare path
    return src


def image_pixel_count(src: Path) -> int:
    """Open the image only to read its dimensions; emit the original on failure."""
    try:
        from PIL import Image
    except Exception as e:
        sys.stderr.write(f"[glyphfit] Pillow unavailable: {e}\n")
        emit_rewrite(src, "glyphfit: Pillow unavailable — returning the original (unshrunk) image.")
    try:
        with Image.open(src) as probe:
            w, h = probe.size
    except Exception as e:
        sys.stderr.write(f"[glyphfit] cannot open {src}: {e}\n")
        emit_rewrite(src, "glyphfit: cannot open image — returning the original.")
    return w * h


def cache_dir() -> Path:
    directory = Path(
        os.environ.get("GLYPHFIT_CACHE_DIR")
        or (Path(tempfile.gettempdir()) / "glyphfit-cache")
    )
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def populate_cache(src: Path, webp_path: Path, meta_path: Path, config: Config) -> None:
    """Run the shrink into `webp_path` and write its metadata sidecar. Emits the
    original (with context on errors) for any failure or intentional no-op."""
    try:
        from shrink import shrink_to_min_readable
    except Exception as e:
        sys.stderr.write(f"[glyphfit] cannot import shrink: {e}\n")
        emit_rewrite(src, "glyphfit: shrink module unavailable — returning the original (unshrunk) image.")

    try:
        result = shrink_to_min_readable(
            src,
            out_path=webp_path,
            outlier_percentile=config.outlier_percentile,
            floor_char_height_px=config.floor_char_height_px,
            verbose=False,
        )
    except Exception as e:
        sys.stderr.write(f"[glyphfit] shrink failed: {e}\n")
        emit_rewrite(src, "glyphfit: shrink failed — returning the original (unshrunk) image.")

    # No detectable text or already small enough → honor the request with the original.
    if result.status != "ok" or not webp_path.exists():
        emit_rewrite(src)

    ow, oh = result.original_size
    nw, nh = result.output_size
    cache.write_meta(meta_path, {
        "name": src.name,
        "original_size": [ow, oh],
        "output_size": [nw, nh],
        "scale": result.scale,
        "outlier_percentile": result.outlier_percentile,
        "measured_char_height": result.measured_char_height,
        "floor_char_height_px": result.floor_char_height_px,
        "pixel_reduction": result.pixel_reduction,
    })
    sys.stderr.write(
        f"[glyphfit] {src.name}: {ow}x{oh} → {nw}x{nh} "
        f"(scale={result.scale:.3f}, p{result.outlier_percentile}={result.measured_char_height:.1f}px, "
        f"floor={result.floor_char_height_px}px, "
        f"-{result.pixel_reduction * 100:.1f}% pixels, {result.elapsed_sec:.1f}s)\n"
    )


def main() -> None:
    event = read_event()
    tool_input: dict[str, Any] = event.get("tool_input") or {}
    file_path = str(tool_input.get("file_path") or "")
    config = Config.from_env()

    # Disabled: behave as if the plugin weren't installed. A plain Read passes
    # through untouched; a shrink: Read only has its prefix stripped so the path
    # still resolves — no detection, no hint, no rewrite to a cached copy.
    if not config.enabled:
        if SHRINK_PREFIX in file_path:
            src = shrink_source(file_path)
            emit_rewrite(src, disabled_hint(str(event.get("session_id") or "")))
        passthrough()

    if SHRINK_PREFIX not in file_path:
        # Plain Read: nudge once per session on the first image.
        maybe_hint(file_path, str(event.get("session_id") or ""))

    src = shrink_source(file_path)

    if image_pixel_count(src) < config.min_pixels:
        emit_rewrite(src)

    try:
        file_bytes = src.read_bytes()
    except OSError as e:
        sys.stderr.write(f"[glyphfit] cannot read {src}: {e}\n")
        emit_rewrite(src, "glyphfit: cannot read image — returning the original.")

    key = cache.cache_key(
        file_bytes,
        pipeline_version=PIPELINE_VERSION,
        outlier_percentile=config.outlier_percentile,
        floor_char_height_px=config.floor_char_height_px,
    )
    webp_path, meta_path = cache.paths_for(cache_dir(), key)

    if not webp_path.exists():
        populate_cache(src, webp_path, meta_path, config)

    emit_rewrite(webp_path)


if __name__ == "__main__":
    main()
