#!/usr/bin/env python3
"""Generate the Kuromi icon set from nine square reference images."""

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
    parser.add_argument("source_dir", type=Path, help="Folder containing nine IMG_*.JPG files")
    parser.add_argument(
        "--icons-js",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets/icons/icons.js",
    )
    args = parser.parse_args()

    files = sorted(args.source_dir.glob("IMG_*.JPG"))
    if len(files) < len(MODULE_ORDER):
        raise SystemExit(f"Expected {len(MODULE_ORDER)} IMG_*.JPG files in {args.source_dir}, found {len(files)}")
    files = files[: len(MODULE_ORDER)]

    raw = args.icons_js.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"const ICON_IMGS=(.*);", raw)
    if not match:
        raise SystemExit(f"Cannot parse icon map: {args.icons_js}")
    icon_map = json.loads(match.group(1))

    kuromi = {key: image_data(path) for key, path in zip(MODULE_ORDER, files)}
    kuromi["brand"] = image_data(files[0])
    icon_map["kuromi"] = kuromi
    args.icons_js.write_text(
        "const ICON_IMGS=" + json.dumps(icon_map, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(f"saved Kuromi icons to {args.icons_js} ({len(files)} source images)")


if __name__ == "__main__":
    main()
