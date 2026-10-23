# Adhi Widagdo — CV & portfolio

A static, multi-page personal website for GitHub Pages. HTML is committed directly, so deployment does not require Node, a framework, or a build service. Visitors load only the pages they choose.

## Pages

- `index.html`: introduction and three selected projects.
- `cv.html`: selected experience, education, skills, and browser print/PDF layout.
- `projects.html`: all 25 projects, with category filters and search.
- `research.html`: publications, awards, research support, and posters.
- `contact.html`: professional contact route.
- `portfolio-details-*.html`: individual case studies at the existing URLs.

All 144 original portfolio images appear in their corresponding project galleries. Galleries advance only through explicit input: thumbnail selection, buttons, arrow keys, or touch gestures. Without JavaScript, the pages remain readable and every thumbnail links to its original image.

## Editing content

Project copy, order, metadata, and image lists live in `assets/content/projects.json`. Shared templates and the CV/research/contact text live in `scripts/build_site.py`. Edit these sources, then regenerate the checked-in HTML:

```sh
python scripts/build_site.py
python scripts/check_site.py
```

The generator uses Python 3.12 or newer and the standard library. Normal content edits do not need image processing.

### Images

Original files in `assets/img/portfolio/` remain unchanged. The image utility creates thumbnail, card, and large WebP copies plus `assets/content/images.json`:

```sh
python -m pip install -r requirements.txt
python scripts/optimize_images.py
python scripts/build_site.py
python scripts/check_site.py
```

Images are resized only downward. No AI reconstruction or invented technical details are used. Compression and appropriate display sizes improve delivery; they cannot recover detail missing from a blurry original. Replace originals with higher-resolution source files when available, keeping filenames stable, and rerun the commands. All filenames in generated pages use exact casing for GitHub Pages.

### Local preview

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. Check desktop and mobile layouts, project search/filters, gallery controls, and the CV print preview before publishing.

Optional DOM integration tests use Node.js and jsdom 26, installed separately from the deployable site:

```sh
node scripts/check_interactions.cjs /path/to/node_modules/jsdom
```

These exercise every gallery image, manual navigation, keyboard and touch events, search, category filters, the empty state, menu focus behavior, and the print action. They do not replace visual layout testing. The redesign passed these tests and `check_site.py`; visual browser QA was blocked by the connected Computer Use tool's browser URL-policy limitation.

## Content update notes

The redesign uses the existing portfolio information. Work from November 2023 through October 2026 has not been added. The CV explicitly describes selected work through 2023, without asserting a current employer or an unconfirmed employment end date.

Confirm these items during the next content update:

- Current role, location, preferred job titles, and updated employment dates.
- New projects, contributions, publications, and measurable outcomes since November 2023.
- Motion-capture project date: its old detail page says 2019–2021, while its description identifies it as the master's research completed in 2016. The conflicting date is omitted.
- Humanoid robot height: the old detail page says 82 mm; this uncertain dimension is omitted.
- HuroCup All Round result: the original homepage and project page disagree (third versus second). That category is omitted pending confirmation.
- XR cinema spans 2019–2023 when its later integration work is included; virtual campus work uses the 2020–2021 dates from the experience section.

The public phone number, placeholder social links, arbitrary skill percentages, creativity-test score, unrelated renovation entry, and third-party reference contact information have been removed. The existing email is retained as a clear recruiting contact route.

## Performance & accessibility

No third-party scripts, web fonts, analytics, or runtime libraries are loaded. Shared CSS and JavaScript are about 19 KB combined before HTTP compression. Non-hero images load lazily, responsive image sources reduce transfer size, and project detail pages load only their own galleries. Original image downloads happen when explicitly opened.

Navigation, filters, and gallery controls use native links and buttons. Pages include a skip link, visible keyboard focus, reduced-motion styles, image dimensions, accessible labels, and a print stylesheet. Original legacy vendor files remain in the repository but are not requested by the rebuilt pages.
