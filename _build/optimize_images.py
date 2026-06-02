#!/usr/bin/env python3
"""
Tesla Boutique Miami — image optimizer.

Turns heavy source photos (JPG/PNG) into the lightest possible web assets:
  - AVIF (smallest) + WebP (fallback), both emitted into assets/img/
  - resized to sensible max widths, metadata stripped

Workflow for the future, as the project grows with many photos:
  1. Drop full-resolution photos into  _build/source_images/  (kept out of git)
  2. Run:  python3 _build/optimize_images.py
  3. Reference them in pages via the <picture> helper (AVIF + WebP + lazy <img>)

Re-running is safe and idempotent. Pair every <img> with loading="lazy"
and decoding="async" (handled by the page generator) so pages stay fast
no matter how many images are added.
"""
import os, sys
from PIL import Image
import pillow_avif  # noqa: F401  (registers the AVIF plugin)

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "img")

# Source folders searched, in order. The first that exists is used.
SOURCE_DIRS = [
    os.path.join(ROOT, "_build", "source_images"),
    ROOT,  # fall back to the original photos sitting in the repo root
]

# Max width per output. Hero/background art can be a little larger; everything
# else is capped tighter because it is only ever shown in cards/galleries.
DEFAULT_MAX_W = 1000
WIDTH_OVERRIDES = {
    "model-s": 1500,          # used as the hero background image
}

WEBP_QUALITY = 70
AVIF_QUALITY = 50             # AVIF quality scale differs; ~50 ≈ visually clean
EXTS = (".jpg", ".jpeg", ".png")


def pick_source_dir():
    for d in SOURCE_DIRS:
        if os.path.isdir(d) and any(f.lower().endswith(EXTS) for f in os.listdir(d)):
            return d
    return None


def optimize():
    src = pick_source_dir()
    if not src:
        print("No source images found. Add photos to _build/source_images/ and re-run.")
        return
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Source: {src}")
    total_in = total_out = 0
    for fname in sorted(os.listdir(src)):
        if not fname.lower().endswith(EXTS):
            continue
        path = os.path.join(src, fname)
        try:
            im = Image.open(path)
            im = im.convert("RGB")
        except Exception as e:
            print(f"  skip {fname}: {e}")
            continue
        stem = os.path.splitext(fname)[0]
        max_w = WIDTH_OVERRIDES.get(stem, DEFAULT_MAX_W)
        w, h = im.size
        if w > max_w:
            im = im.resize((max_w, round(h * max_w / w)), Image.LANCZOS)

        webp = os.path.join(OUT_DIR, stem + ".webp")
        avif = os.path.join(OUT_DIR, stem + ".avif")
        im.save(webp, "webp", quality=WEBP_QUALITY, method=6)
        im.save(avif, "avif", quality=AVIF_QUALITY)

        in_sz = os.path.getsize(path)
        out_sz = os.path.getsize(webp) + os.path.getsize(avif)
        total_in += in_sz
        total_out += out_sz
        print(f"  {fname:42s} {in_sz/1e6:6.2f}MB -> "
              f"webp {os.path.getsize(webp)/1024:5.0f}KB + "
              f"avif {os.path.getsize(avif)/1024:5.0f}KB  {im.size}")
    print(f"\nSource total: {total_in/1e6:.1f} MB  ->  optimized total: {total_out/1024:.0f} KB")


if __name__ == "__main__":
    optimize()
