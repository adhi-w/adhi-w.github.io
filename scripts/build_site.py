"""Generate buildless GitHub Pages HTML from editable content. Python 3 only."""
from pathlib import Path
from html import escape
import json
import re
from profile_content import cv_body, resume_body

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'assets/content/projects.json').read_text(encoding='utf-8'))
IMAGES = json.loads((ROOT / 'assets/content/images.json').read_text(encoding='utf-8'))
BASE = 'https://adhi-w.github.io/'
FEATURED = [project for project in PROJECTS if project.get('featured')]

def esc(text):
    return escape(str(text), quote=True)

def image(path, alt, size='card', eager=False, sizes='(max-width: 420px) 92vw, (max-width: 760px) 45vw, 370px'):
    item = IMAGES[path][size]
    variants = {v['width']: v['src'] for k,v in IMAGES[path].items() if k != 'thumb'}
    srcset = ', '.join(f'{url} {width}w' for width,url in sorted(variants.items()))
    return f'<img src="{item["src"]}" srcset="{srcset}" sizes="{sizes}" width="{item["width"]}" height="{item["height"]}" alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"{chr(32)+"fetchpriority=\"high\"" if eager else ""}>'

def tags(values):
    return '<div class="skills-list">' + ''.join(f'<span class="tag">{esc(value)}</span>' for value in values) + '</div>'

def closing():
    return '<section class="wrap closing"><div><h2>Have a role in mind?</h2><p>Let’s talk about XR, video compression, and graphics systems.</p></div><a class="button" href="contact.html">Get in touch <span aria-hidden="true">↗</span></a></section>'

def page(file, title, description, body, active, close=True):
    nav = [('index.html','Overview'),('cv.html','CV'),('projects.html','Projects'),('research.html','Research'),('contact.html','Contact')]
    links = ''.join(f'<a href="{url}"{(" aria-current=\"page\"" if label == active else "")}{(" class=\"contact-link\"" if label == "Contact" else "")}>{label}</a>' for url,label in nav)
    meteors = '<i class="meteor"></i>' * 12
    full_title = 'Adhi Widagdo — Researcher & Engineer | XR & Video Systems' if file == 'index.html' else f'{title} — Adhi Widagdo'
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{'<base href="/">' if file == '404.html' else ''}
<title>{esc(full_title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#0b1220">
<link rel="canonical" href="{BASE}{file if file != 'index.html' else ''}">
<link rel="icon" href="favicon.ico" type="image/x-icon" sizes="16x16 32x32 48x48">
<link rel="icon" href="assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="assets/img/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png" sizes="180x180">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE}{file if file != 'index.html' else ''}"><meta property="og:image" content="{BASE}assets/img/portfolio/gaze-adaptive-streaming-concept.png"><meta property="og:image:alt" content="Gaze-adaptive VR streaming: rendered, foveated, and reconstructed frames"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/css/site.css"><script src="assets/js/site.js" defer></script></head>
<body><div class="ambient" aria-hidden="true"><span></span><span></span>{meteors}</div><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Adhi Widagdo, overview"><span class="brand-mark" aria-hidden="true">AW</span>Adhi Widagdo.</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Menu</button><nav class="nav" id="site-nav" aria-label="Main navigation">{links}</nav></div></header>
<main id="main">{body}</main>{closing() if close else ''}
<footer class="site-footer"><div class="wrap footer-inner"><span>© Adhi Widagdo · XR &amp; video systems research</span><div><a href="cv.html">Curriculum vitae</a><a href="https://github.com/adhi-w">GitHub ↗</a><a href="https://www.linkedin.com/in/adhi-w/">LinkedIn ↗</a><a href="contact.html">Contact</a><button type="button" class="motion-toggle" data-motion-toggle data-enhanced hidden aria-pressed="false">Background motion</button></div></div></footer></body></html>'''
    (ROOT / file).write_text(html + '\n', encoding='utf-8')

def card(project):
    search = ' '.join([project['title'],project['category'],project['summary'],*project['tags']]).lower()
    return f'''<article class="project-card" data-project data-category="{esc(project['category'])}" data-search="{esc(search)}"><a href="{project['file']}"><div class="project-cover">{image(project['cover'],project['title']+' — project photograph or illustration')}</div><div class="meta"><span>{esc(project['category'])}</span><span>{esc(project['date'])}</span></div><h3>{esc(project['title'])}<span aria-hidden="true">↗</span></h3><p>{esc(project['summary'])}</p></a></article>'''

def intro(label, title, text, extra=''):
    return f'<div class="page-intro"><span class="eyebrow">{label}</span><h1>{title}</h1><p>{text}</p>{extra}</div>'

def overview():
    photo = image('assets/img/ProfilePicture.jpg','Portrait of Adhi Widagdo','full',True,'(max-width: 760px) 260px, 290px')
    body = f'''<div class="wrap"><section class="hero profile-hero"><div><span class="eyebrow">Researcher &amp; Engineer / Helsinki, Finland</span><h1>XR experiences.<br><em>Built with depth.</em></h1><p class="intro">I’m Adhi. I build systems for immersive video, gaze-adaptive VR streaming, and neural video compression. My work connects graphics engineering with research into what people see and experience.</p><div class="actions"><a class="button" href="projects.html">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="cv.html#resume-options">Get my résumé →</a></div><div class="profile-links"><a href="https://www.linkedin.com/in/adhi-w/">LinkedIn ↗</a><a href="https://github.com/adhi-w">GitHub ↗</a><a href="contact.html">Get in touch ↗</a></div></div><figure class="profile-card">{photo}<svg class="portrait-neon" viewBox="0 0 300 460" preserveAspectRatio="none" aria-hidden="true" focusable="false"><rect class="neon-base" x="3" y="3" width="294" height="454" rx="15" vector-effect="non-scaling-stroke"/><rect class="neon-run" x="3" y="3" width="294" height="454" rx="15" pathLength="100" vector-effect="non-scaling-stroke"/><rect class="neon-run neon-run-second" x="3" y="3" width="294" height="454" rx="15" pathLength="100" vector-effect="non-scaling-stroke"/></svg><figcaption><strong>Adhi Widagdo</strong><span>XR &amp; video systems</span><span>University of Helsinki</span><span class="photo-credit">Photo: Heikki Nenonen</span></figcaption></figure></section><div class="expertise-strip"><strong>From research to working systems</strong><span>Foveated streaming</span><span>Neural video codecs</span><span>Perceptual evaluation</span></div><section class="section"><div class="section-heading"><div><span class="eyebrow">Selected work</span><h2>Built. Measured. Explored.</h2></div><a class="text-link" href="projects.html">All {len(PROJECTS)} projects ↗</a></div><div class="project-grid featured-grid">{''.join(card(p) for p in FEATURED)}</div></section></div>
<section class="about-band"><div class="wrap about-grid"><div><span class="eyebrow">A connected engineering background</span><h2>Robotics foundations.<br>Immersive systems.<br>Smarter video.</h2></div><div><p>My path started with robotics: computer vision, sensing, control, and making hardware and software work together. At the University of Oulu, I brought those skills into VR-based robotic telepresence and immersive media.</p><p>Since November 2023, my research at the University of Helsinki has focused on Cloud-XR and gaming. I develop gaze-adaptive streaming and latency compensation, and investigate neural video compression. I combine C++, GPU shaders, Python, and PyTorch with objective quality measurements and user studies.</p><p>I’m pursuing a PhD in Computer Science and looking for research and engineering opportunities in XR, video systems, and visual computing.</p><a class="text-link" href="cv.html">Explore my experience →</a></div></div></section>'''
    page('index.html','Overview','Adhi Widagdo, researcher and engineer in XR streaming, neural video compression, graphics, and perceptual quality.',body,'Overview')

def projects():
    filters = ''.join(f'<button class="filter" type="button" data-filter="{esc(value)}" aria-pressed="{str(value=="all").lower()}">{label}</button>' for value,label in [('all','All work'),('VR & XR','VR & XR'),('Robotics','Earlier robotics'),('Engineering & design','Engineering & design')])
    body = '<div class="wrap">' + intro('Project portfolio','Research that runs<br>on real systems.','My current work connects gaze-adaptive VR streaming, latency optimization, and neural video compression. Explore the published research and ongoing experiments, alongside earlier work in robotics and engineering.') + f'<div class="toolbar" data-enhanced hidden><div class="filters" role="group" aria-label="Filter projects">{filters}</div><label class="search"><span class="sr-only">Search projects by title, skill, or topic</span><input id="project-search" type="search" placeholder="Search projects or skills…"></label></div><p class="result-count" id="project-count" role="status" aria-live="polite">{len(PROJECTS)} projects</p><div class="project-grid">'+''.join(card(p) for p in PROJECTS)+'</div><p class="empty" id="no-results" hidden>No projects match. Try another search or choose “All work”.</p><div class="section"></div></div>'
    page('projects.html','Projects',f'Explore {len(PROJECTS)} projects, covering XR streaming, neural video compression, and earlier engineering work.',body,'Projects')

def cv():
    page('cv.html','CV','Detailed experience, doctoral research, education, and skills of Adhi Widagdo, with one-page resumes for XR and engineering roles.',cv_body(intro,tags),'CV')

def resumes():
    for kind in ('xr','research'):
        page(f'resume-{kind}.html','One-page resume','One-page resume of Adhi Widagdo: XR streaming, neural video codecs, and systems engineering.',resume_body(kind),'CV',False)

def research():
    publications = [
      ('2026','Latency-Driven Optimization for Foveation in Remote Rendered VR','Adhi Widagdo, Teemu Kämäräinen, Sam Kondori, Yuan-Chun Sun, Matti Siekkinen & Cheng-Hsin Hsu','34th ACM International Conference on Multimedia (MM ’26), Rio de Janeiro, Brazil · Forthcoming, 10–14 November 2026','10.1145/3767308.3835889'),
      ('2025','Gaze-Adaptive Foveation for Remote Rendered VR','Adhi Widagdo, Teemu Kämäräinen, Ahmad Alhilal, Matti Siekkinen & Cheng-Hsin Hsu','33rd ACM International Conference on Multimedia (MM ’25), Dublin, Ireland','10.1145/3746027.3755620'),
      ('2024','Investigating a simple technique to alter viewpoint height in immersive 360° video','Evan G. Center, Adhi Widagdo, Matti Pouke, Markku Suomalainen, Katherine J. Mimnaugh, Abdulsatar Aboud, Timo Ojala & Steven M. LaValle','2024 IEEE Conference on Telepresence, pp. 131–138','10.1109/Telepresence63209.2024.10841573'),
      ('2022','Unwinding Rotations Improves User Comfort with Immersive Telepresence Robots','M. Suomalainen, B. Sakcak, A. Widagdo, J. Kalliokoski, K. J. Mimnaugh, A. P. Chambers, T. Ojala & S. M. LaValle','ACM/IEEE International Conference on Human-Robot Interaction (HRI)',''),
      ('2017','Limb motion tracking with inertial measurement units','P. A. C. Widagdo, H. H. Lee & C. H. Kuo','IEEE International Conference on Systems, Man, and Cybernetics (SMC), pp. 1551–1556','10.1109/SMC.2017.8122818'),
      ('2015','Development of a Biped Teen-Size Humanoid Robot for Participating in RoboCup 2015 Competition','I. W. D. Pranata, A. C. Widagdo, A. P. Yudha & C. H. Kuo','CACS International Automatic Control Conference, pp. 232–236','10.1109/CACS.2015.7393872'),
    ]
    rows = ''
    for year,title,authors,venue,doi in publications:
        link = f'<a href="https://doi.org/{doi}">Read publication ↗</a>' if doi else ''
        rows += f'<article class="research-row"><span class="date">{year}</span><div><h3>{esc(title)}</h3><p>{esc(authors)}</p><p>{esc(venue)}</p>{link}</div></article>'
    body = '<div class="wrap">' + intro('Research & recognition','Gaze, latency,<br>and visual experience.','My research connects gaze-adaptive graphics, video compression, and perceptual evaluation. Published work explores foveation and latency in streamed VR; ongoing work investigates how these ideas extend to neural video codecs.') + '''<div class="split"><aside class="sidebar" aria-label="Research sections"><h2>On this page</h2><ul><li><a href="#publications">Selected publications</a></li><li><a href="#ongoing">Ongoing research</a></li><li><a href="#preprints">Preprints</a></li><li><a href="#awards">Earlier awards</a></li><li><a href="#support">Research support</a></li><li><a href="#posters">Posters</a></li></ul><h2>Research interests</h2><p>Remote XR rendering<br>Neural video compression<br>Foveated streaming<br>Quality of experience</p><h2>Research software</h2><a href="https://github.com/adhi-w/Dyna-ALVR">Dyna-ALVR repository ↗</a></aside><div><section class="cv-section" id="publications"><h2>Selected publications</h2>''' + rows + '''</section>
<section class="cv-section" id="ongoing"><h2>Ongoing research</h2><article class="research-row"><span class="date">In progress</span><div><h3>Foveated neural video compression</h3><p>Combining gaze-adaptive sampling with learned video codecs, and evaluating the trade-offs between visual quality, bitrate, and processing time.</p><p>Unpublished research · GPU experiments and codec integration.</p><a href="portfolio-details-foveated-neural-video.html">Explore the project ↗</a></div></article></section>
<section class="cv-section" id="preprints"><h2>Preprints</h2><article class="research-row"><span class="date">2022</span><div><h3>A Study of Preference and Comfort for Users Immersed in a Telepresence Robot</h3><p>Adhi Widagdo, Markku Suomalainen, Basak Sakcak, Katherine J. Mimnaugh, Juho Kalliokoski, Alexis P. Chambers, Timo Ojala &amp; Steven M. LaValle</p><p>arXiv preprint · arXiv:2203.02699</p><a href="https://doi.org/10.48550/arXiv.2203.02699">Read preprint ↗</a></div></article></section>
<section class="cv-section" id="awards"><h2>Selected awards</h2><ul class="awards"><li><strong>Best Student Conference Paper · 2015</strong>CACS International Automatic Control Conference.</li><li><strong>RoboCup · 2015</strong>Team awards: first place in the Teen-size Technical Challenge and second place in Teen-size Soccer.</li><li><strong>HuroCup · 2015</strong>Team awards: first place in Adult-size Sprint; second place in Marathon and Obstacle Run.</li><li><strong>PIMNAS XXVI · 2013</strong>National Presenter Award.</li><li><strong>EEPIS Final Project Competition · 2013</strong>Third place.</li><li><strong>National rocket competitions · 2010 &amp; 2011</strong>Team: first place at KORINDO 2010 and KOMURINDO 2011.</li></ul></section>
<section class="cv-section" id="support"><h2>Research support</h2><p>The current foveation research is supported by the Research Council of Finland (grant 355577). The LDO work also acknowledges partial support from Taiwan’s NSTC (112-2221-E-007-090-MY3).</p><p>Earlier research and project support included UniOGS Infotech, the 6G Flagship program, Taiwan NSC and Ministry of Education, MRL industry collaboration, DIKTI, and EEPIS. Scholarship support included a Taiwan Tech master’s student award.</p></section>
<section class="cv-section" id="posters"><h2>Research posters</h2><article class="research-row"><span class="date">2026</span><div><h3>Latency-Driven Optimization for Foveation in Remote Rendered VR</h3><p>ACM Multimedia 2026 · Gaze-adaptive streaming, latency compensation, and experimental results.</p><a href="assets/documents/ldo-acm-mm2026-poster.pdf">View poster (PDF, 1.4 MB) ↗</a></div></article><article class="research-row"><span class="date">Earlier XR</span><div><h3>Challenges in Wireless XR</h3><p>Adhi Widagdo &amp; Steve LaValle · 6G Flagship</p><a href="assets/img/poster-6g-flagship.jpg">View poster image ↗</a></div></article><article class="research-row"><span class="date">Robotics</span><div><h3>Sistem Koordinasi &amp; Kecerdasan Buatan untuk Strategi Bertanding pada Robot Soccer</h3><p>Adhi Widagdo, Renita Urrosyda, Ermita Rachmawati &amp; Indra Adji · PIMNAS XXVI DIKTI</p><a href="assets/img/poster-pkmp.jpg">View poster image ↗</a></div></article></section></div></div></div>'''
    page('research.html','Research','Selected publications and ongoing research in gaze-adaptive VR streaming, neural video compression, and perceptual quality.',body,'Research')

def contact():
    body = '<div class="wrap">' + intro('Contact','Let’s build<br>better XR experiences.','I’m interested in research and engineering roles in XR, neural video compression, real-time graphics, and visual computing.') + '''<div class="contact-layout"><section class="contact-main"><span class="eyebrow">Start a conversation</span><h2>Have an opportunity<br>in mind?</h2><p>Send me a little about the role, the team, and the problem you’re working on. I’d be glad to hear more.</p><p class="email" id="email-address">adhi [dot] cwidagdo [at] gmail [dot] com</p><div class="actions"><a class="button secondary" href="#email-address" data-email-link data-enhanced hidden>Open email app <span aria-hidden="true">↗</span></a></div></section><aside class="contact-aside"><h2>Connect on LinkedIn</h2><p>For professional updates, research, and opportunities.</p><a class="text-link" href="https://www.linkedin.com/in/adhi-w/">linkedin.com/in/adhi-w ↗</a><h2 class="contact-subheading">Explore my work</h2><p>My current work combines gaze-adaptive graphics, neural video compression, and perceptual evaluation, from VR streaming systems to experimental codec pipelines. Explore the recent research projects or read an overview of my experience.</p><a class="text-link" href="cv.html">Read my CV →</a><br><a class="text-link" href="projects.html">Explore the project portfolio →</a><br><a class="text-link" href="https://github.com/adhi-w">Find me on GitHub ↗</a></aside></div></div>'''
    page('contact.html','Contact','Contact Adhi Widagdo about research and engineering opportunities in XR, real-time graphics, and video streaming.',body,'Contact',False)

def caption(path, project):
    if path in project.get('image_captions', {}):
        return project['image_captions'][path]
    name = Path(path).stem
    for prefix in ['6g-flagship-','immersive-','telepresence-robot-','simulation-robot-','xr-cinematech-','3d-scanner-','huro-mech-','huro-vision-','oulucampus-','panoramic-']:
        if name.startswith(prefix): name = name[len(prefix):]; break
    else:
        if name.startswith(project['slug']+'-'): name = name[len(project['slug'])+1:]
    words = re.sub(r'(\D)(\d+)$',r'\1 \2',name).replace('-',' ').replace('_',' ')
    words = re.sub(r'\b(gui|bom|io|hs|id)\b',lambda m:m[0].upper(),words)
    return words[:1].upper() + words[1:]

def detail(project, index):
    items=[]
    for path in project['images']:
        variants=IMAGES[path]; full=variants['full']; widths={v['width']:v['src'] for k,v in variants.items() if k!='thumb'}
        items.append({**full,'original':path,'srcset':', '.join(f'{url} {w}w' for w,url in sorted(widths.items())),'caption':caption(path,project)})
    first=project['images'][0]
    thumbs=''.join(f'<a href="{path}" data-slide="{i}" aria-current="{str(i==0).lower()}" aria-label="View image {i+1}: {esc(items[i]["caption"])}"><img src="{IMAGES[path]["thumb"]["src"]}" width="{IMAGES[path]["thumb"]["width"]}" height="{IMAGES[path]["thumb"]["height"]}" alt="" loading="lazy" decoding="async"></a>' for i,path in enumerate(project['images']))
    meta = [('Discipline',project['category']),('Context',project['context'])]
    if project['date']:meta.append((project.get('date_label','Period'),project['date']))
    if project['funding']:meta.append(('Support',project['funding']))
    facts=''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in meta)
    contributions = ''
    if project.get('contributions'):
        contributions = '<h3>Project contributions &amp; outcomes</h3><ul>' + ''.join(f'<li>{esc(c)}</li>' for c in project['contributions']) + '</ul>'
    gallery_json=json.dumps(items,ensure_ascii=False).replace('<','\\u003c')
    body=f'''<div class="wrap"><div class="breadcrumb"><a href="projects.html">Projects</a><span aria-hidden="true"> / </span>{esc(project['category'])}</div><div class="page-intro project-intro"><span class="eyebrow">Project notes</span><h1>{esc(project['title'])}</h1><p>{esc(project['summary'])}</p></div><dl class="project-facts">{facts}</dl><div class="case-grid"><section class="gallery" data-gallery aria-label="{esc(project['title'])} image gallery"><div class="gallery-stage"><a href="{first}" aria-label="Open displayed image at original resolution">{image(first,items[0]['caption'],'full',True,'(max-width: 760px) 92vw, 680px')}</a></div><div class="gallery-bar"><div class="gallery-controls" data-enhanced hidden><button type="button" data-previous aria-label="Previous image" disabled>←</button><span class="gallery-count" aria-live="polite">1 / {len(items)}</span><button type="button" data-next aria-label="Next image">→</button></div><a class="original-link" href="{first}">View original image ↗</a></div><p class="gallery-caption" aria-live="polite">{esc(items[0]['caption'])}</p><div class="gallery-thumbs" aria-label="All project images">{thumbs}</div><p class="gallery-help">{len(items)} images · Select a thumbnail to explore. Original project photographs and illustrations.</p><noscript><p class="gallery-help">Select any thumbnail to open its original image.</p></noscript><script type="application/json" id="gallery-data">{gallery_json}</script></section><div class="case-copy"><h2>The work</h2><p>{esc(project['overview'])}</p>{contributions}<h3>Tools &amp; focus</h3>{tags(project['tags'])}</div></div>'''
    if project.get('results'):
        results = ''.join(f'<li>{esc(result)}</li>' for result in project['results'])
        links = ''.join(f'<a href="{esc(link["url"])}">{esc(link["label"])} ↗</a>' for link in project.get('links', []))
        body += f'<section class="case-evidence" aria-label="Evaluation and publication"><div><span class="eyebrow">Evidence &amp; evaluation</span><h2>What the study found</h2></div><div><ul>{results}</ul><p class="note">{esc(project["evaluation"])}</p><h3>Publication &amp; collaboration</h3><p>{esc(project["collaboration"])}</p><div class="research-links">{links}</div></div></section>'
    if project.get('project_notes'):
        body += f'<section class="cv-section"><h2>Research status</h2><p>{esc(project["project_notes"])}</p></section>'
    if project.get('links') and not project.get('results'):
        links = ''.join(f'<a href="{esc(link["url"])}">{esc(link["label"])} ↗</a>' for link in project['links'])
        body += f'<section class="cv-section"><h2>Related documents</h2><div class="research-links">{links}</div></section>'
    previous=PROJECTS[(index-1)%len(PROJECTS)];following=PROJECTS[(index+1)%len(PROJECTS)]
    body+=f'<nav class="project-nav" aria-label="Adjacent projects"><a href="{previous["file"]}">← {esc(previous["title"])}</a><a href="{following["file"]}">{esc(following["title"])} →</a></nav></div>'
    page(project['file'],project['title'],project['summary'],body,'Projects')

if __name__ == '__main__':
    overview(); cv(); resumes(); projects(); research(); contact()
    for i,project in enumerate(PROJECTS): detail(project,i)
    page('404.html','Page not found','This page could not be found. Explore Adhi Widagdo’s portfolio.', '<div class="wrap">'+intro('404 · Page not found','Let’s get you<br>back on track.','The page may have moved. You can find the full portfolio and CV using the navigation above.','<div class="actions"><a class="button" href="index.html">Back to overview →</a></div>')+'</div>','',False)
    files=['','cv.html','resume-xr.html','resume-research.html','projects.html','research.html','contact.html']+[p['file'] for p in PROJECTS]
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{file}</loc></url>' for file in files)+'</urlset>\n',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    (ROOT/'.nojekyll').touch()
    print(f'Generated {len(PROJECTS)+8} pages and sitemap.')
