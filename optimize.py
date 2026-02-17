"""Utility script for simple project optimizations.

Usage:
    python optimize.py --minify
    python optimize.py --images

The script will produce minified versions of CSS/JS and convert JPEG/PNG files to WebP.
It also prints a summary of savings.
"""
import re
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None


def minify_css(source: Path, dest: Path) -> None:
    text = source.read_text(encoding="utf-8")
    # remove comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # remove whitespace around symbols
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ?([{},;:>]) ?", r"\1", text)
    dest.write_text(text.strip(), encoding="utf-8")
    print(f"CSS minified: {source.name} -> {dest.name} ({len(text)} bytes)")


def minify_js(source: Path, dest: Path) -> None:
    text = source.read_text(encoding="utf-8")
    # strip comments (// and /* */) and extra whitespace
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text)
    dest.write_text(text.strip(), encoding="utf-8")
    print(f"JS minified: {source.name} -> {dest.name} ({len(text)} bytes)")


def convert_images(folder: Path) -> None:
    if Image is None:
        print("Pillow not installed; cannot convert images. Use `pip install Pillow`.")
        return
    for path in folder.rglob("*.jpg") + folder.rglob("*.png"):
        out = path.with_suffix(".webp")
        try:
            img = Image.open(path)
            img.save(out, "WEBP", quality=75)
            print(f"converted {path.name} -> {out.name}")
        except Exception as e:
            print(f"failed to convert {path.name}: {e}")


def main():
    base = Path(__file__).parent
    if "--minify" in sys.argv:
        css = base / "style.css"
        js = base / "app.js"
        minify_css(css, base / "style.min.css")
        minify_js(js, base / "app.min.js")
    if "--images" in sys.argv:
        convert_images(base / "image")


if __name__ == "__main__":
    main()
