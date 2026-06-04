"""Content-addressed cache for shrunk images.

The cache key combines the source bytes with the pipeline version and the
output-affecting settings, so the same image under the same settings reuses a
prior result while any change (new file, new floor, new pipeline) misses. The
WebP itself is written atomically by the shrink step; this module owns the key,
the file paths, and the sidecar metadata.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def cache_key(
    file_bytes: bytes,
    *,
    pipeline_version: str,
    outlier_percentile: int,
    floor_char_height_px: int,
) -> str:
    """Return `<content>_<settings>`: 16 hex of the file's sha256 plus 8 hex of
    the settings' sha256. Only output-affecting settings enter the key."""
    content = hashlib.sha256(file_bytes).hexdigest()[:16]
    settings = hashlib.sha256(
        f"v={pipeline_version};op={outlier_percentile};floor={floor_char_height_px}".encode()
    ).hexdigest()[:8]
    return f"{content}_{settings}"


def paths_for(cache_dir: Path, key: str) -> tuple[Path, Path]:
    """Return (webp_path, meta_path) for a cache key."""
    webp_path = cache_dir / f"{key}.webp"
    return webp_path, webp_path.with_suffix(".json")


def write_meta(meta_path: Path, meta: dict[str, Any]) -> None:
    """Best-effort sidecar write; failures are non-fatal (metadata is advisory)."""
    try:
        meta_path.write_text(json.dumps(meta))
    except OSError:
        pass
