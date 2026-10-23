"""Check deployable pages, exact-case URLs, and complete gallery coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
FILES = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts}
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.h1s = 0
        self.title = False
        self.description = False
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids: errors.append(f'{self.path.name}: duplicate ID {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1s += 1
        if tag == 'title': self.title = True
        if tag == 'meta' and attrs.get('name') == 'description': self.description = bool(attrs.get('content'))
        if tag == 'img':
            for key in ('alt','width','height','loading'):
                if key not in attrs: errors.append(f'{self.path.name}: image lacks {key}')
        for key in ('src','href'):
            if key in attrs: self.links.append(attrs[key])
        if 'srcset' in attrs:
            self.links += [variant.strip().split()[0] for variant in attrs['srcset'].split(',')]
        if tag in ('script','link'):
            url=attrs.get('src',attrs.get('href',''))
            if url.startswith('https://') and attrs.get('rel') != 'canonical':
                errors.append(f'{self.path.name}: external runtime dependency {url}')

pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
for name,page in pages.items():
    if page.h1s != 1 or not page.title or not page.description:
        errors.append(f'{name}: missing or duplicate heading/title/description')
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc: continue
        path=unquote(url.path).lstrip('/') or name
        if path not in FILES:
            errors.append(f'{name}: missing or incorrectly cased URL {link}')
        if url.fragment and path in pages and url.fragment not in pages[path].ids:
            errors.append(f'{name}: missing anchor {link}')

projects=json.loads((ROOT/'assets/content/projects.json').read_text(encoding='utf-8'))
images=json.loads((ROOT/'assets/content/images.json').read_text(encoding='utf-8'))
all_project_images={p.relative_to(ROOT).as_posix() for p in (ROOT/'assets/img/portfolio').iterdir() if p.suffix.lower() in ('.jpg','.png','.jpeg')}
gallery_images=set()
for project in projects:
    source=(ROOT/project['file']).read_text(encoding='utf-8')
    for image in project['images']:
        gallery_images.add(image)
        if image not in images or image not in source: errors.append(f'{project["file"]}: image omitted {image}')
        for variant in images[image].values():
            if variant['src'] not in FILES: errors.append(f'Missing optimized asset: {variant["src"]}')
    if source.count('data-slide=') != len(project['images']): errors.append(f'{project["file"]}: incomplete thumbnail list')
    if project['file'] not in (ROOT/'projects.html').read_text(encoding='utf-8'): errors.append(f'Unlisted project {project["file"]}')
if gallery_images != all_project_images: errors.append(f'Gallery coverage mismatch: {gallery_images ^ all_project_images}')
script=(ROOT/'assets/js/site.js').read_text(encoding='utf-8')
for forbidden in ('setInterval','autoplay','setTimeout'):
    if forbidden in script: errors.append(f'Unexpected automatic behavior: {forbidden}')
for name in pages:
    source=(ROOT/name).read_text(encoding='utf-8')
    if 'assets/vendor/' in source or 'fonts.googleapis.com' in source: errors.append(f'{name}: legacy runtime dependency')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; all local links and anchors resolve with exact casing.')
print(f'PASS: {len(projects)} project pages cover all {len(gallery_images)} original project images.')
print('PASS: metadata, image dimensions, alt attributes, and dependency-free manual galleries.')
