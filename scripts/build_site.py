"""Generate buildless GitHub Pages HTML from editable content. Python 3 only."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'assets/content/projects.json').read_text(encoding='utf-8'))
IMAGES = json.loads((ROOT / 'assets/content/images.json').read_text(encoding='utf-8'))
BASE = 'https://adhi-w.github.io/'

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
    return '<section class="wrap closing"><div><h2>Have a role in mind?</h2><p>Let’s talk about robotics, immersive technology, and the work ahead.</p></div><a class="button" href="contact.html">Get in touch <span aria-hidden="true">↗</span></a></section>'

def page(file, title, description, body, active, close=True):
    nav = [('index.html','Overview'),('cv.html','CV'),('projects.html','Projects'),('research.html','Research'),('contact.html','Contact')]
    links = ''.join(f'<a href="{url}"{(" aria-current=\"page\"" if label == active else "")}{(" class=\"contact-link\"" if label == "Contact" else "")}>{label}</a>' for url,label in nav)
    full_title = 'Adhi Widagdo — Robotics & VR/XR Engineer' if file == 'index.html' else f'{title} — Adhi Widagdo'
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{'<base href="/">' if file == '404.html' else ''}
<title>{esc(full_title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#182e33">
<link rel="canonical" href="{BASE}{file if file != 'index.html' else ''}"><link rel="icon" href="assets/img/monogram.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE}{file if file != 'index.html' else ''}"><meta property="og:image" content="{BASE}assets/img/portfolio/6g-flagship-3d-scanner.jpg"><meta property="og:image:alt" content="Adhi Widagdo working with a 3D scanning setup"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/css/site.css"><script src="assets/js/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Adhi Widagdo, overview"><span class="brand-mark" aria-hidden="true">AW</span>Adhi Widagdo.</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Menu</button><nav class="nav" id="site-nav" aria-label="Main navigation">{links}</nav></div></header>
<main id="main">{body}</main>{closing() if close else ''}
<footer class="site-footer"><div class="wrap footer-inner"><span>© Adhi Widagdo · Robotics &amp; immersive technology</span><div><a href="cv.html">Curriculum vitae</a><a href="https://github.com/adhi-w">GitHub ↗</a><a href="contact.html">Contact</a></div></div></footer></body></html>'''
    (ROOT / file).write_text(html + '\n', encoding='utf-8')

def card(project):
    search = ' '.join([project['title'],project['category'],project['summary'],*project['tags']]).lower()
    return f'''<article class="project-card" data-project data-category="{esc(project['category'])}" data-search="{esc(search)}"><a href="{project['file']}"><div class="project-cover">{image(project['cover'],project['title']+' — project photograph or illustration')}</div><div class="meta"><span>{esc(project['category'])}</span><span>{esc(project['date'])}</span></div><h3>{esc(project['title'])}<span aria-hidden="true">↗</span></h3><p>{esc(project['summary'])}</p></a></article>'''

def intro(label, title, text, extra=''):
    return f'<div class="page-intro"><span class="eyebrow">{label}</span><h1>{title}</h1><p>{text}</p>{extra}</div>'

def overview():
    photo = image('assets/img/portfolio/6g-flagship-3d-scanner.jpg','Adhi Widagdo at a 3D scanning setup, with a captured model on screen','full',True,'(max-width: 760px) 92vw, 505px')
    body = f'''<div class="wrap"><section class="hero"><div><span class="eyebrow">Robotics &amp; VR/XR engineer</span><h1>Engineering the<br>connection between<br><em>physical &amp; virtual.</em></h1><p class="intro">I’m Adhi. I build robotic systems and immersive experiences, bringing together software, hardware, and a hands-on approach to research.</p><div class="actions"><a class="button" href="projects.html">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="cv.html">View my CV →</a></div></div><figure class="hero-figure">{photo}<figcaption><div><span>From the lab</span>3D capture for immersive environments</div><a href="portfolio-details-3d-scanner.html" aria-label="Explore the 3D scanning project">↗</a></figcaption></figure></section><div class="expertise-strip"><strong>From prototype to experience</strong><span>Robotic systems</span><span>Virtual &amp; extended reality</span><span>Human-centered research</span></div><section class="section"><div class="section-heading"><div><span class="eyebrow">Selected projects</span><h2>A closer look at my work.</h2></div><a class="text-link" href="projects.html">All 25 projects ↗</a></div><div class="project-grid">{''.join(card(p) for p in PROJECTS[:3])}</div></section></div>
<section class="about-band"><div class="wrap about-grid"><div><span class="eyebrow">An interdisciplinary perspective</span><h2>Comfortable with code.<br>At home in the workshop.</h2></div><div><p>My background spans mechatronics, electrical engineering, and immersive technology. I’ve worked on humanoid robots, wearable motion tracking, and VR telepresence—from designing components to integrating systems and studying how people use them.</p><p>I enjoy the point where disciplines meet: making a mechanism work, connecting it to software, and turning it into something people can experience.</p><a class="text-link" href="cv.html">Explore my experience →</a></div></div></section>'''
    page('index.html','Overview','Adhi Widagdo’s engineering portfolio: robotics, virtual and extended reality, motion tracking, and human-centered research.',body,'Overview')

def projects():
    filters = ''.join(f'<button class="filter" type="button" data-filter="{esc(value)}" aria-pressed="{str(value=="all").lower()}">{label}</button>' for value,label in [('all','All work'),('Robotics','Robotics'),('VR & XR','VR & XR'),('Engineering & design','Engineering & design')])
    body = '<div class="wrap">' + intro('Project portfolio','Ideas, built and tested.','A collection of research, engineering, and design work. Explore the systems, the process, and the details behind each project.') + f'<div class="toolbar" data-enhanced hidden><div class="filters" role="group" aria-label="Filter projects">{filters}</div><label class="search"><span class="sr-only">Search projects by title, skill, or topic</span><input id="project-search" type="search" placeholder="Search projects or skills…"></label></div><p class="result-count" id="project-count" role="status" aria-live="polite">25 projects</p><div class="project-grid">'+''.join(card(p) for p in PROJECTS)+'</div><p class="empty" id="no-results" hidden>No projects match. Try another search or choose “All work”.</p><div class="section"></div></div>'
    page('projects.html','Projects','Explore 25 projects in robotics, VR/XR, wearable sensing, mechanical design, and engineering.',body,'Projects')

def cv():
    body = '''<div class="wrap">''' + intro('Curriculum vitae','A practical, connected<br>approach to engineering.','Robotics and VR/XR engineer with a background in mechatronics and electrical engineering. My work connects physical systems, immersive software, and experimental research.','<div class="actions no-print"><button class="button" type="button" data-print data-enhanced hidden>Print / save as PDF <span aria-hidden="true">↗</span></button><a class="text-link" href="contact.html">Contact me →</a></div><div class="print-only">Adhi Widagdo · adhi.cwidagdo@gmail.com · adhi-w.github.io</div>') + '''
<div class="split"><aside class="sidebar" aria-label="CV sections and skills"><h2>On this page</h2><ul><li><a href="#experience">Experience</a></li><li><a href="#education">Education</a></li><li><a href="#skills">Technical toolkit</a></li><li><a href="#recognition">Recognition</a></li></ul><h2>Areas of focus</h2><p>Robotic systems<br>VR &amp; XR development<br>Motion tracking<br>Research prototyping</p><h2>Selected work</h2><a href="portfolio-details-telepresence-robot.html">Immersive telepresence →</a><a href="portfolio-details-xr-cinematech.html">XR cinema technology →</a><a href="portfolio-details-mocap.html">Wearable motion capture →</a></aside><div>
<p class="note">Selected experience and project work through 2023.</p>
<section class="cv-section" id="experience"><h2>Experience</h2>
<article class="timeline-item"><p class="date">Selected project work · 2019–2023</p><h3>Research &amp; engineering in robotics and XR</h3><p class="org">Center for Ubiquitous Computing · University of Oulu, Finland</p><ul><li>Developed VR-based robot telepresence systems and supported user studies on comfort and the remote experience.</li><li>Built immersive rendering software for 16K panoramic images and 8K video, integrating Oculus and Varjo headsets.</li><li>Connected Unity applications with ROS 2, robot navigation, camera systems, and inertial sensors.</li><li>Supported teaching in sensing, tracking, and autonomy; contributed to research demonstrations and unit events.</li></ul><div class="subroles"><div><h4>XR software &amp; perception · 2019–2023</h4><p>Mesh generation, projection mapping, gaze tracking, video passthrough, immersive video production, and study support.</p></div><div><h4>Telepresence engineering · 2021–2022</h4><p>Robot deployment, environment mapping, motion planning, and integration with VR.</p></div><div><h4>Virtual environments · 2020–2021</h4><p>Campus modeling, PBR materials, lighting, animated avatars, and performance optimization.</p></div><div><h4>Research infrastructure · 2019–2022</h4><p>Photogrammetry and 3D asset processing, headset benchmarking, and IMU integration.</p></div></div></article>
<article class="timeline-item"><p class="date">2016–2018</p><h3>System Business Analyst</h3><p class="org">GriyaBinangun · Indonesia</p><ul><li>Supported and improved business processes for a property consultancy and home developer.</li><li>Analyzed system issues, recommended upgrades, and developed solutions for new business needs.</li><li>Maintained and improved business intelligence processes.</li></ul></article>
<article class="timeline-item"><p class="date">2014–2016</p><h3>Research Student &amp; Project Engineer</h3><p class="org">Medical Robotic Laboratory · Taiwan Tech, Taiwan</p><ul><li>Designed and manufactured mechanical parts and electronic circuit boards for humanoid robots.</li><li>Developed computer vision, control, and task-oriented behavior for robot competitions.</li><li>Built an IMU-based wearable motion capture system and evaluated sensor-fusion methods.</li><li>Contributed to joint research projects with industry partners.</li></ul></article>
<article class="timeline-item"><p class="date">2011</p><h3>Engineering Intern</h3><p class="org">PT. Djaja Sakti Sari · Indonesia</p><ul><li>Supported CAD design, manufacturing, production management, and machine maintenance.</li><li>Worked with engineers and technicians on a machine for recovering material from rejected products.</li></ul></article></section>
<section class="cv-section" id="education"><h2>Education</h2><article class="timeline-item"><p class="date">2014–2016</p><h3>MSc in Electrical Engineering</h3><p class="org">National Taiwan University of Science and Technology · Taipei, Taiwan</p><p class="org">GPA: 3.97 / 4.0</p><p class="org">Thesis: Wearable Motion Tracking System using Quaternion-based Complementary Filter Algorithm with Inertial Measurement Units.</p></article><article class="timeline-item"><p class="date">2009–2013</p><h3>Bachelor of Applied Science in Mechatronics Engineering</h3><p class="org">Sepuluh Nopember Institute of Technology · Surabaya, Indonesia</p><p class="org">GPA: 3.50 / 4.0</p><p class="org">Thesis: Design and Construction of Multi-agent Robot Soccer: Localization and Synchronization of Multi-agent Robot Soccer based on Visualization.</p></article></section>
<section class="cv-section" id="skills"><h2>Technical toolkit</h2><div class="subroles"><div><h4>Software &amp; programming</h4>''' + tags(['C / C++','C#','Python','Java','Visual Basic','MATLAB','HTML / CSS / JavaScript']) + '''</div><div><h4>Robotics &amp; sensing</h4>''' + tags(['ROS 2','Motion planning','Computer vision','IMUs','Sensor fusion','TCP/IP']) + '''</div><div><h4>Immersive development</h4>''' + tags(['Unity','VR / XR','Shaders','360° video','Blender','Photogrammetry']) + '''</div><div><h4>Design &amp; research</h4>''' + tags(['CAD / CAM','PCB design','Manufacturing','Prototyping','User studies','Data analysis']) + '''</div></div></section>
<section class="cv-section" id="recognition"><h2>Selected recognition</h2><ul><li>Best Student Conference Paper · CACS 2015.</li><li>Team: first place, Teen-size Technical Challenge; second place, Teen-size Soccer · RoboCup 2015.</li><li>Team: first place at KORINDO 2010 and KOMURINDO 2011.</li></ul><a class="text-link" href="research.html">Publications, awards &amp; research support →</a></section></div></div></div>'''
    page('cv.html','CV','Experience, education, and technical skills of Adhi Widagdo, robotics and VR/XR engineer.',body,'CV')

def research():
    publications = [
      ('2022','Unwinding Rotations Improves User Comfort with Immersive Telepresence Robots','M. Suomalainen, B. Sakcak, A. Widagdo, J. Kalliokoski, K. J. Mimnaugh, A. P. Chambers, T. Ojala & S. M. LaValle','ACM/IEEE International Conference on Human-Robot Interaction (HRI)',''),
      ('2017','Limb motion tracking with inertial measurement units','P. A. C. Widagdo, H. H. Lee & C. H. Kuo','IEEE International Conference on Systems, Man, and Cybernetics (SMC), pp. 1551–1556','10.1109/SMC.2017.8122818'),
      ('2015','Development of a Biped Teen-Size Humanoid Robot for Participating in RoboCup 2015 Competition','I. W. D. Pranata, A. C. Widagdo, A. P. Yudha & C. H. Kuo','CACS International Automatic Control Conference, pp. 232–236','10.1109/CACS.2015.7393872'),
      ('2015','Team Description Paper: HuroEvolutionTN Humanoid Robot for RoboCup 2015 Humanoid League','C. H. Kuo, A. P. Yudha, A. C. Widagdo, S. W. Prakosa & I. W. D. Pranata','RoboCup Humanoid League, Hefei, China, pp. 1–8',''),
      ('2014','Dynamic movement of multi-agent robot soccer based on visualization','I. A. Sulistijono, P. A. C. Wicaksono & E. S. Ningrum','10th France-Japan / 8th Europe-Asia Congress on Mechatronics, pp. 1–6','10.1109/MECATRONICS.2014.7018356'),
      ('2013','Sistem Koordinasi dan Kecerdasan Buatan untuk Strategi Bertanding pada Robot Soccer','P. A. C. Widagdo, E. D. Rachmawati, R. Chulafaurrosyda & I. A. Sulistijono','Artikel DIKTI PKM-P','')]
    rows = ''
    for year,title,authors,venue,doi in publications:
        link = f'<a href="https://doi.org/{doi}">Read publication ↗</a>' if doi else ''
        rows += f'<article class="research-row"><span class="date">{year}</span><div><h3>{esc(title)}</h3><p>{esc(authors)}</p><p>{esc(venue)}</p>{link}</div></article>'
    body = '<div class="wrap">' + intro('Research & recognition','Building. Testing.<br>Sharing what we learn.','Publications and recognition from work in immersive telepresence, motion tracking, and robotic systems.') + '''<div class="split"><aside class="sidebar" aria-label="Research sections"><h2>On this page</h2><ul><li><a href="#publications">Publications</a></li><li><a href="#awards">Selected awards</a></li><li><a href="#support">Research support</a></li><li><a href="#posters">Posters</a></li></ul><h2>Research interests</h2><p>Immersive telepresence<br>Human–robot interaction<br>Motion tracking<br>Robot perception</p></aside><div><section class="cv-section" id="publications"><h2>Publications</h2>''' + rows + '''</section>
<section class="cv-section" id="awards"><h2>Selected awards</h2><ul class="awards"><li><strong>Best Student Conference Paper · 2015</strong>CACS International Automatic Control Conference.</li><li><strong>RoboCup · 2015</strong>Team awards: first place in the Teen-size Technical Challenge and second place in Teen-size Soccer.</li><li><strong>HuroCup · 2015</strong>Team awards: first place in Adult-size Sprint; second place in Marathon and Obstacle Run.</li><li><strong>PIMNAS XXVI · 2013</strong>National Presenter Award.</li><li><strong>EEPIS Final Project Competition · 2013</strong>Third place.</li><li><strong>National rocket competitions · 2010 &amp; 2011</strong>Team: first place at KORINDO 2010 and KOMURINDO 2011.</li></ul></section>
<section class="cv-section" id="support"><h2>Research support</h2><p>Research and project work supported by UniOGS Infotech, the 6G Flagship program, Taiwan NSC and Ministry of Education, MRL industry collaboration, DIKTI, and EEPIS.</p><p>Scholarship support included a Taiwan Tech master’s student award (2014–2016).</p></section>
<section class="cv-section" id="posters"><h2>Research posters</h2><article class="research-row"><span class="date">XR</span><div><h3>Challenges in Wireless XR</h3><p>Adhi Widagdo &amp; Steve LaValle · 6G Flagship</p><a href="assets/img/poster-6g-flagship.jpg">View poster image ↗</a></div></article><article class="research-row"><span class="date">Robotics</span><div><h3>Sistem Koordinasi &amp; Kecerdasan Buatan untuk Strategi Bertanding pada Robot Soccer</h3><p>Adhi Widagdo, Renita Urrosyda, Ermita Rachmawati &amp; Indra Adji · PIMNAS XXVI DIKTI</p><a href="assets/img/poster-pkmp.jpg">View poster image ↗</a></div></article></section></div></div></div>'''
    page('research.html','Research','Publications, research posters, and awards in immersive telepresence, motion tracking, and robotics.',body,'Research')

def contact():
    body = '<div class="wrap">' + intro('Contact','Let’s build<br>something useful.','I’m interested in engineering and research roles where robotics, immersive technology, and practical problem-solving come together.') + '''<div class="contact-layout"><section class="contact-main"><span class="eyebrow">Start a conversation</span><h2>Have an opportunity<br>in mind?</h2><p>Send me a little about the role, the team, and the problem you’re working on. I’d be glad to hear more.</p><a class="email" href="mailto:adhi.cwidagdo@gmail.com">adhi.cwidagdo@gmail.com ↗</a></section><aside class="contact-aside"><h2>A good starting point</h2><p>My portfolio covers robotic systems, VR/XR software, sensor integration, and research prototypes. You can explore specific projects or read a concise overview of my experience.</p><a class="text-link" href="cv.html">Read my CV →</a><br><a class="text-link" href="projects.html">Explore the project portfolio →</a><br><a class="text-link" href="https://github.com/adhi-w">Find me on GitHub ↗</a></aside></div></div>'''
    page('contact.html','Contact','Contact Adhi Widagdo about engineering and research opportunities in robotics and VR/XR.',body,'Contact',False)

def caption(path, project):
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
    if project['date']:meta.append(('Period',project['date']))
    if project['funding']:meta.append(('Support',project['funding']))
    facts=''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in meta)
    gallery_json=json.dumps(items,ensure_ascii=False).replace('<','\\u003c')
    body=f'''<div class="wrap"><div class="breadcrumb"><a href="projects.html">Projects</a><span aria-hidden="true"> / </span>{esc(project['category'])}</div><div class="page-intro project-intro"><span class="eyebrow">Project notes</span><h1>{esc(project['title'])}</h1><p>{esc(project['summary'])}</p></div><dl class="project-facts">{facts}</dl><div class="case-grid"><section class="gallery" data-gallery aria-label="{esc(project['title'])} image gallery"><div class="gallery-stage"><a href="{first}" aria-label="Open displayed image at original resolution">{image(first,items[0]['caption'],'full',True,'(max-width: 760px) 92vw, 680px')}</a></div><div class="gallery-bar"><div class="gallery-controls" data-enhanced hidden><button type="button" data-previous aria-label="Previous image" disabled>←</button><span class="gallery-count" aria-live="polite">1 / {len(items)}</span><button type="button" data-next aria-label="Next image">→</button></div><a class="original-link" href="{first}">View original image ↗</a></div><p class="gallery-caption" aria-live="polite">{esc(items[0]['caption'])}</p><div class="gallery-thumbs" aria-label="All project images">{thumbs}</div><p class="gallery-help">{len(items)} images · Select a thumbnail to explore. Original project photographs and illustrations.</p><noscript><p class="gallery-help">Select any thumbnail to open its original image.</p></noscript><script type="application/json" id="gallery-data">{gallery_json}</script></section><div class="case-copy"><h2>The work</h2><p>{esc(project['overview'])}</p><h3>Project contributions &amp; outcomes</h3><ul>{''.join(f'<li>{esc(c)}</li>' for c in project['contributions'])}</ul><h3>Tools &amp; focus</h3>{tags(project['tags'])}</div></div>'''
    previous=PROJECTS[(index-1)%len(PROJECTS)];following=PROJECTS[(index+1)%len(PROJECTS)]
    body+=f'<nav class="project-nav" aria-label="Adjacent projects"><a href="{previous["file"]}">← {esc(previous["title"])}</a><a href="{following["file"]}">{esc(following["title"])} →</a></nav></div>'
    page(project['file'],project['title'],project['summary'],body,'Projects')

if __name__ == '__main__':
    overview(); cv(); projects(); research(); contact()
    for i,project in enumerate(PROJECTS): detail(project,i)
    page('404.html','Page not found','This page could not be found. Explore Adhi Widagdo’s portfolio.', '<div class="wrap">'+intro('404 · Page not found','Let’s get you<br>back on track.','The page may have moved. You can find the full portfolio and CV using the navigation above.','<div class="actions"><a class="button" href="index.html">Back to overview →</a></div>')+'</div>','',False)
    files=['','cv.html','projects.html','research.html','contact.html']+[p['file'] for p in PROJECTS]
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{file}</loc></url>' for file in files)+'</urlset>\n',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    (ROOT/'.nojekyll').touch()
    print(f'Generated {len(PROJECTS)+6} pages and sitemap.')
