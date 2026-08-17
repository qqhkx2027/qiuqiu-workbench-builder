#!/usr/bin/env python3
"""Inline a nine-image theme into assets/icons/icons.js.

Examples:
  python3 tools/generate_theme_icons.py popmart "/path/to/POP MART" --brand-index 9
  python3 tools/generate_theme_icons.py kuromi /path/to/Kuromi

Only optimized 120px JPEG data URIs are stored in the repository; source photos
can remain outside the skill folder.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps


MODULE_ORDER = ["home", "todo", "create", "media", "ledger", "health", "diary", "finance", "ai"]


def image_data(path: Path, size: int = 120) -> str:
    image = Image.open(path).convert("RGB")
    image = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    output = BytesIO()
    image.save(output, format="JPEG", quality=84, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme", help="Theme ID used in ICON_IMGS, for example popmart or kuromi")
    parser.add_argument("source_dir", type=Path, help="Folder containing at least nine IMG_*.JPG files")
    parser.add_argument("--brand-index", type=int, default=0, help="Source image index to use for the brand avatar")
    parser.add_argument(
        "--icons-js",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets/icons/icons.js",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9-]+", args.theme):
        raise SystemExit("theme must contain only lowercase letters, digits, and hyphens")
    files = sorted(args.source_dir.glob("IMG_*.JPG"))
    if len(files) < len(MODULE_ORDER):
        raise SystemExit(f"Expected at least {len(MODULE_ORDER)} IMG_*.JPG files, found {len(files)}")
    if not 0 <= args.brand_index < len(files):
        raise SystemExit(f"brand index must be between 0 and {len(files) - 1}")

    raw = args.icons_js.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"const ICON_IMGS=(.*);", raw)
    if not match:
        raise SystemExit(f"Cannot parse icon map: {args.icons_js}")
    icon_map = json.loads(match.group(1))
    icon_map[args.theme] = {
        **{key: image_data(path) for key, path in zip(MODULE_ORDER, files[: len(MODULE_ORDER)])},
        "brand": image_data(files[args.brand_index]),
    }
    args.icons_js.write_text(
        "const ICON_IMGS=" + json.dumps(icon_map, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(f"saved {args.theme} icons to {args.icons_js} ({len(files)} source images)")


if __name__ == "__main__":
    main()
