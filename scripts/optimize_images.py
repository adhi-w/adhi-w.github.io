"""Make responsive WebP copies. Originals are never changed or upscaled."""
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/img/optimized'
OUT.mkdir(parents=True, exist_ok=True)
paths = sorted((ROOT / 'assets/img/portfolio').iterdir())
paths += [ROOT / 'assets/img/ProfilePicture.jpg']
manifest = {}
for path in paths:
    if path.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
        continue
    with Image.open(path) as opened:
        im = ImageOps.exif_transpose(opened).convert('RGB')
        variants = {}
        for label, limit, quality in [('thumb', 144, 76), ('card', 640, 84), ('full', 1400, 88)]:
            target = OUT / f'{path.stem.lower()}-{label}.webp'
            copy = im.copy()
            copy.thumbnail((limit, limit), Image.Resampling.LANCZOS)
            if not target.exists() or target.stat().st_mtime < path.stat().st_mtime:
                copy.save(target, 'WEBP', quality=quality, method=6)
            variants[label] = {'src': target.relative_to(ROOT).as_posix(), 'width': copy.width, 'height': copy.height}
        manifest[path.relative_to(ROOT).as_posix()] = variants
(ROOT / 'assets/content/images.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(f'Prepared {len(manifest)} original images in three responsive sizes.')
print(f'Originals: {sum(p.stat().st_size for p in paths):,} bytes. Full-size WebP copies: {sum(p.stat().st_size for p in OUT.glob("*-full.webp")):,} bytes.')
