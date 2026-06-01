"""Downscale an image so its smallest non-outlier text line stays readable.

Pipeline: detect line heights (ocr) → take the (outlier_percentile)-th percentile
height as the smallest non-outlier line → scale = floor / that height → resize once
with Lanczos → save lossless WebP atomically.

Terminology: detection yields line-level boxes, so the measured heights are
line-box heights, not single glyphs. The public name `floor_char_height_px` is
kept for config compatibility but means the minimum line-box height (px) to keep.

Content-blind by design: it always tries to shrink and the caller decides when to
invoke it. With no detectable text the result is `status="no_text"` and the
original is preserved.
"""

import json
import os
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detect import detect_line_heights  # noqa: E402

DEFAULT_FLOOR_CHAR_HEIGHT_PX = 18


def percentile_height(heights_px: list[float], percentile: int) -> float:
    """Lower-rank ("drop-bottom-p%") percentile: drop the shortest `percentile`%
    of lines and return the smallest survivor. idx = floor(n * percentile / 100),
    so p=5 on n=200 drops the 10 shortest and returns the 11th. Not numpy's
    interpolated percentile; for n < 100/percentile nothing is dropped (idx=0)."""
    n = len(heights_px)
    if n == 0:
        return 0.0
    ordered = sorted(heights_px)
    return ordered[max(0, min(n - 1, (n * percentile) // 100))]


def compute_scale(
    heights_px: list[float], floor_px: int, outlier_percentile: int
) -> tuple[float, float]:
    """Return (scale, measured_height) for the given line heights.

    `scale` is clamped to <= 1.0 (1.0 means the text already sits at/above the
    floor — nothing to do). `measured_height` is the percentile line-box height,
    or 0.0 when there are no heights.
    """
    measured = percentile_height(heights_px, outlier_percentile)
    if measured <= 0:
        return 1.0, measured
    return min(1.0, floor_px / measured), measured


def downscale(img: Image.Image, scale: float) -> Image.Image:
    w, h = img.size
    new_size = (max(1, round(w * scale)), max(1, round(h * scale)))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def save_webp_atomic(img: Image.Image, path: str | Path) -> None:
    """Save lossless WebP atomically: write to a temp file in the same directory,
    then os.replace() it into place so a concurrent reader never sees a partial
    file. method=6 maximizes compression (a few hundred ms, fine here)."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".glyphfit-tmp-", suffix=".webp")
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        img.save(tmp_path, format="WEBP", lossless=True, method=6)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


@dataclass
class ShrinkResult:
    status: str  # "ok" | "no_text" | "no_action"
    scale: float
    original_size: tuple[int, int]
    output_size: tuple[int, int]
    pixel_reduction: float
    output_path: str
    outlier_percentile: int
    measured_char_height: float  # the percentile line-box height, in px
    floor_char_height_px: int    # the floor applied (min line-box height), in px
    fragments: int
    elapsed_sec: float

    @classmethod
    def unchanged(
        cls,
        status: str,
        *,
        size: tuple[int, int],
        output_path: str | Path,
        outlier_percentile: int,
        measured_char_height: float,
        floor_char_height_px: int,
        fragments: int,
        started_at: float,
    ) -> "ShrinkResult":
        """Build a passthrough result (no resize): `no_text` or `no_action`,
        scale 1.0, output identical to input."""
        return cls(
            status=status,
            scale=1.0,
            original_size=size,
            output_size=size,
            pixel_reduction=0.0,
            output_path=str(output_path),
            outlier_percentile=outlier_percentile,
            measured_char_height=measured_char_height,
            floor_char_height_px=floor_char_height_px,
            fragments=fragments,
            elapsed_sec=time.monotonic() - started_at,
        )


def shrink_to_min_readable(
    src: str | Path,
    out_path: str | Path | None = None,
    outlier_percentile: int = 5,
    floor_char_height_px: int = DEFAULT_FLOOR_CHAR_HEIGHT_PX,
    verbose: bool = False,
) -> ShrinkResult:
    """Resize `src` once so its (outlier_percentile)-th percentile line-box height
    sits at or above `floor_char_height_px`. Values <= 0 fall back to the default.
    (Per-script auto-detect is intentionally unavailable: detection runs without
    recognition, so there is no script to key a floor on.)"""
    started = time.monotonic()
    src_path = Path(src)
    floor = floor_char_height_px if floor_char_height_px > 0 else DEFAULT_FLOOR_CHAR_HEIGHT_PX

    with Image.open(src_path) as img:
        size = img.size
        heights = detect_line_heights(src_path)

        if not heights:
            return ShrinkResult.unchanged(
                "no_text", size=size, output_path=src_path,
                outlier_percentile=outlier_percentile, measured_char_height=0.0,
                floor_char_height_px=floor, fragments=0, started_at=started,
            )

        scale, measured = compute_scale(heights, floor, outlier_percentile)
        if verbose:
            sys.stderr.write(
                f"  fragments={len(heights)}, p{outlier_percentile} "
                f"height={measured:.1f}px, floor={floor}px, scale={scale:.4f}\n"
            )

        if scale >= 1.0:
            return ShrinkResult.unchanged(
                "no_action", size=size, output_path=src_path,
                outlier_percentile=outlier_percentile, measured_char_height=measured,
                floor_char_height_px=floor, fragments=len(heights), started_at=started,
            )

        final = downscale(img, scale)

    out = Path(out_path) if out_path is not None else src_path.with_name(f"{src_path.stem}.shrunk.webp")
    save_webp_atomic(final, out)

    (ow, oh), (fw, fh) = size, final.size
    return ShrinkResult(
        status="ok",
        scale=scale,
        original_size=size,
        output_size=(fw, fh),
        pixel_reduction=1.0 - (fw * fh) / (ow * oh),
        output_path=str(out),
        outlier_percentile=outlier_percentile,
        measured_char_height=measured,
        floor_char_height_px=floor,
        fragments=len(heights),
        elapsed_sec=time.monotonic() - started,
    )


def _main(argv: list[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Shrink an image based on detected text-line heights")
    p.add_argument("src")
    p.add_argument("-o", "--out", default=None)
    p.add_argument("--outlier-percentile", type=int, default=5,
                   help="Drop bottom N%% of line heights as outliers (1–50, default 5)")
    p.add_argument("--floor-char-height-px", type=int, default=DEFAULT_FLOOR_CHAR_HEIGHT_PX,
                   help="Minimum line-box height in the output (px, default 18). "
                        "Recommended: 12 (latin), 18 (hangul/kana), 24 (CJK).")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    res = shrink_to_min_readable(
        args.src,
        out_path=args.out,
        outlier_percentile=args.outlier_percentile,
        floor_char_height_px=args.floor_char_height_px,
        verbose=args.verbose,
    )
    print(json.dumps(asdict(res), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
