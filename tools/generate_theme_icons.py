#!/usr/bin/env python3
"""Generate a theme's icon files and runtime map.

Examples:
  python3 tools/generate_theme_icons.py popmart "/path/to/POP MART" --brand-index 9
  python3 tools/generate_theme_icons.py kuromi /path/to/Kuromi

The first nine images are assigned to the workbench modules in MODULE_ORDER.
The optimized 120px PNGs are kept in assets/icons for visual inspection, while
the same images are also written as data URIs to icons.js so every dist/*.html
file remains a self-contained offline page.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


MODULE_ORDER = ["home", "todo", "create", "media", "ledger", "health", "diary", "finance", "ai"]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def make_icon(path: Path, size: int = 120) -> Image.Image:
    """Fit an image into a consistent transparent circular PNG."""
    image = Image.open(path).convert("RGBA")
    image = ImageOps.fit(
        image,
        (size, size),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    output = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    output.paste(image, (0, 0), mask)
    return output


def image_data(image: Image.Image) -> str:
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode("ascii")


def source_images(source_dir: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in source_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES and not path.name.startswith(".")
        ),
        key=lambda path: path.name.lower(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme", help="Theme ID used in ICON_IMGS, for example popmart or kuromi")
    parser.add_argument("source_dir", type=Path, help="Folder containing at least nine image files")
    parser.add_argument("--brand-index", type=int, default=0, help="Source image index for the brand avatar")
    parser.add_argument(
        "--icons-js",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets/icons/icons.js",
        help="Runtime icon map to update",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets/icons",
        help="Directory for optimized PNG inspection files",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9-]+", args.theme):
        raise SystemExit("theme must contain only lowercase letters, digits, and hyphens")
    if not args.source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {args.source_dir}")

    files = source_images(args.source_dir)
    if len(files) < len(MODULE_ORDER):
        raise SystemExit(f"Expected at least {len(MODULE_ORDER)} image files, found {len(files)}")
    if not 0 <= args.brand_index < len(files):
        raise SystemExit(f"brand index must be between 0 and {len(files) - 1}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    optimized = {}
    for index, (key, source) in enumerate(zip(MODULE_ORDER, files[: len(MODULE_ORDER)]), start=1):
        icon = make_icon(source)
        target = args.output_dir / f"{args.theme}_{index:02d}.png"
        icon.save(target, format="PNG", optimize=True)
        optimized[key] = image_data(icon)

    brand = make_icon(files[args.brand_index])
    brand_path = args.output_dir / f"{args.theme}_brand.png"
    brand.save(brand_path, format="PNG", optimize=True)
    optimized["brand"] = image_data(brand)

    raw = args.icons_js.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"const ICON_IMGS=(.*);", raw)
    if not match:
        raise SystemExit(f"Cannot parse icon map: {args.icons_js}")
    icon_map = json.loads(match.group(1))
    icon_map[args.theme] = optimized
    args.icons_js.write_text(
        "const ICON_IMGS=" + json.dumps(icon_map, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(f"saved {args.theme}: {len(MODULE_ORDER)} module icons + brand")
    print(f"  preview PNGs: {args.output_dir}")
    print(f"  runtime map:  {args.icons_js}")


if __name__ == "__main__":
    main()
