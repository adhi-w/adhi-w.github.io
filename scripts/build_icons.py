"""Export the existing vector monogram as browser-compatible favicon assets.

Authoring dependencies: Pillow and pymupdf. No runtime dependencies.
"""
from io import BytesIO
from pathlib import Path
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/img/monogram.svg'

with pymupdf.open(stream=SOURCE.read_bytes(), filetype='svg') as vector:
    pixmap = vector[0].get_pixmap(matrix=pymupdf.Matrix(4, 4), alpha=True)
    raster = Image.open(BytesIO(pixmap.tobytes('png'))).convert('RGBA')

for size, name in [(32, 'favicon-32.png'), (192, 'favicon-192.png'), (180, 'apple-touch-icon.png')]:
    raster.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / 'assets/img' / name)
raster.save(ROOT / 'favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
print('Exported PNG icons, Apple touch icon, and multi-resolution favicon.ico.')
