"""Simple helper to list the most common colors in an image.

Usage:
    python get_colors.py path/to/image.png [--top N]
"""

from pathlib import Path
from collections import Counter

import numpy as np

try:
    from PIL import Image
except ImportError:  # pragma: no cover - pillow may not be installed
    raise ImportError("pillow is required: pip install Pillow")


def extract_top_colors(path: Path, top: int = 10):
    """Return the `top` most common RGB tuples from the given image."""
    img = Image.open(path)
    arr = np.array(img)
    # drop alpha channel if present
    if arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[arr[:, :, 3] > 0][:, :3]
    pixels = arr.reshape(-1, arr.shape[-1])
    common = Counter([tuple(c) for c in pixels]).most_common(top)
    return common


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Find most common colors in an image.")
    parser.add_argument("image", type=Path, help="path to an image file")
    parser.add_argument("--top", "-n", type=int, default=10, help="how many colors to show")
    args = parser.parse_args()
    common = extract_top_colors(args.image, args.top)
    for color, count in common:
        print(f"{color} – {count} pixels")


if __name__ == "__main__":
    main()