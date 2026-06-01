"""Text detection — RapidOCR DBNet with recognition disabled.

Returns only the vertical extent (height in px) of each detected text line.
Recognition is off (use_rec=False), so there is no text content or script
information to act on — just line-box heights. Identical on macOS/Linux/Windows.
"""

from __future__ import annotations

from pathlib import Path


def detect_line_heights(image_path: Path) -> list[float]:
    """Detect text lines and return each line-box's vertical extent in pixels.

    Detection only (no recognition), so the result is a flat list of heights with
    no text and no ordering guarantees. Empty when nothing text-like is found.
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

    heights: list[float] = []
    for box in result:
        try:
            ys = [float(point[1]) for point in box]
        except (TypeError, IndexError, ValueError):
            continue
        height = max(ys) - min(ys)
        if height > 0:
            heights.append(height)
    return heights
