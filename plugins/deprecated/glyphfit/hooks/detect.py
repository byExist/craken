"""Text detection — RapidOCR DBNet with recognition disabled.

Returns the short side (the smaller of width and height, in px) of each detected
text-line box. For horizontal text the short side is the line's height; for
vertical text (e.g. Japanese) the box is tall and narrow, so its height is the
column length and the *width* is the short side — either way the short side
tracks glyph size rather than line length. RapidOCR normalizes every box to an
axis-aligned TL→TR→BR→BL quad and exposes no writing-direction signal (cls is
0°/180° only), so the short side is the only orientation-agnostic size estimate
available.

Recognition is off (use_rec=False), so there is no text content or script to act
on — just box geometry. Identical on macOS/Linux/Windows.
"""

from __future__ import annotations

from pathlib import Path


def detect_line_heights(image_path: Path) -> list[float]:
    """Detect text lines and return each box's short side (min width/height) in px.

    The short side approximates glyph size even for vertical text, where a line
    box's height is the column length, not the character size. Detection only (no
    recognition), so the result is a flat list with no text and no ordering
    guarantees. Empty when nothing text-like is found.

    Kept named `..._heights` for caller compatibility: for the common horizontal
    case the short side is exactly the line height.
    """
    from rapidocr_onnxruntime import RapidOCR  # type: ignore[PylancereportMissingTypeStubs]

    engine = RapidOCR()
    # use_rec=False → detection only. Each entry is a 4-point polygon
    # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] in absolute pixels.
    result, _elapsed = engine(
        str(image_path), use_det=True, use_cls=False, use_rec=False
    )
    if not result:
        return []

    sizes: list[float] = []
    for box in result:
        try:
            xs = [float(point[0]) for point in box]
            ys = [float(point[1]) for point in box]
        except (TypeError, IndexError, ValueError):
            continue
        # Short side = min(width, height): for vertical text the height is the
        # column length, so the width is what tracks glyph size.
        size = min(max(xs) - min(xs), max(ys) - min(ys))
        if size > 0:
            sizes.append(size)
    return sizes
