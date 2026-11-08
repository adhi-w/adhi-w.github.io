"""Career content shared by the detailed CV, resume pages, and PDF exports."""
from html import escape as esc

IDENTITY = 'Researcher & Engineer | XR and Video Systems'
SUMMARY = ('I develop XR streaming and video systems, combining gaze-adaptive graphics, '
           'neural video compression, and perceptual evaluation. My background in robotics '
           'and immersive telepresence connects software development with sensing and real-world systems.')
CURRENT = {
    'title': 'Doctoral Researcher · Cloud-XR & Gaming',
    'dates': 'November 2023–present',
    'org': 'University of Helsinki · Department of Computer Science, Finland',
    'intro': 'Research alongside PhD studies in Computer Science. My work focuses on remote rendering, foveated streaming, neural video codecs, and visual quality.',
    'bullets': [
        'Implement gaze-adaptive spatial compression in ALVR, connecting server-side HLSL foveation with client-side Vulkan reconstruction, eye tracking, and H.265 video streaming.',
        'Develop latency compensation through gaze prediction, hysteresis-based stabilization, and adaptive foveal sizing, with synchronized parameters across the server and headset.',
        'Build Python workflows for gaze analysis, parameter tuning, and visual-quality evaluation using eye-weighted PSNR and FovVideoVDP.',
        'Investigate foveated neural video compression for VR. This work is ongoing and unpublished.',
        'Develop research software in C++ and Python to support video-system experiments.',
        'Contribute to user studies, undergraduate thesis supervision, and teaching; collaborate with researchers at Aalto University and National Tsing Hua University.'
    ],
    'projects': [
        ('Gaze-adaptive foveation · ACM Multimedia 2025', 'First-author paper comparing three dynamic foveation methods in an end-to-end VR system. The evaluated implementation supported native 72 FPS operation and a complementary 16-participant study.'),
        ('Latency-driven optimization · ACM Multimedia 2026', 'First-author paper reporting 24.04% lower mean gaze error in the evaluated conditions, with significant visual and overall quality gains in a 30-participant study. Conference: 10–14 November 2026.'),
        ('Neural video compression · Ongoing', 'Explore foveated neural video compression for VR through ongoing, unpublished research.')
    ]
}
OULU = {
    'title': 'Researcher · Immersive Telepresence',
    'dates': '2019–October 2023',
    'org': 'University of Oulu · Center for Ubiquitous Computing, Finland',
    'intro': 'Research integrating virtual reality and mobile robotics. The work combined immersive software, sensing, system integration, and studies of user comfort and experience.',
    'bullets': [
        'Developed VR-based robotic telepresence systems, connecting headset rendering, panoramic cameras, robot navigation, and sensing.',
        'Contributed to the design and operation of user studies, analyzed participant experience, and iterated on the immersive system.',
        'Supported teaching in sensing, tracking, and autonomy, and contributed demonstrations and research-unit events.'
    ],
    'projects': [
        ('XR cinema rendering · 2019–2021', 'Developed mesh generation and image-mapping software for panoramic media, working with UV coordinates, shaders, equirectangular and cube-map projections, and interpolation. Rendered 16K still images and 8K video.'),
        ('Headset and streaming integration · 2021–2023', 'Integrated Oculus Rift S, Quest 2, and Varjo headsets with XR cinema and telepresence playback. Worked with eye tracking, video passthrough, and live video to connect immersive applications with different devices.'),
        ('Immersive perception experiments · 2022–2023', 'Adapted rendering software for perceptual experiments, produced panoramic media, and implemented gaze tracking and event handling. Supported VR studies and analysis of user experience.'),
        ('Robotic telepresence · 2021–2022', 'Integrated VR with a mobile robot, environment mapping, navigation, and obstacle avoidance. Supported deployments and user studies to assess comfort and the remote experience.'),
        ('Headset benchmarking · 2019–2020', 'Worked with OptoFidelity engineers on robot-based headset evaluation, including resolution, motion-to-photon latency, field of view, and tracking accuracy. Built Python tools for analysis and visualization.'),
        ('Oulu campus virtual environment · 2020–2021', 'Created building models, PBR materials, lighting, avatars, and animations. Programmed interactive objects, optimized rendering performance, and connected the Unity environment to ROS 2 through TCP/IP.'),
        ('Panoramic media · 2019–2022', 'Captured and processed high-resolution 360-degree images and videos for robotic telepresence and immersive meetings, working on stitching quality and playback integration.'),
        ('Photogrammetry and 3D scanning · 2019–2022', 'Supported scanner development, capture planning, equipment operation, and scan processing. Produced assets for human avatars, virtual museum content, and 3D printing.'),
        ('Inertial sensing · 2019–2020', 'Developed an IMU software library for a mobile robot, integrated it with camera and sensing systems, and tested it in laboratory and field settings.')
    ]
}
EARLIER = [
    ('System Business Analyst', '2016–2018', 'GriyaBinangun · Property consultancy and home development, Indonesia', [
        'Supported, maintained, and improved business processes and business-intelligence workflows.',
        'Analyzed system issues, recommended upgrades, and developed solutions for changing business needs.'
    ]),
    ('Research Student & Project Engineer', '2014–2016', 'Medical Robotic Laboratory · Taiwan Tech, Taiwan', [
        'Designed and manufactured mechanical parts and electronic circuit boards for humanoid robots.',
        'Developed computer vision, robot control, and task-oriented behavior for international competitions.',
        'Built an IMU-based wearable motion-capture system and evaluated quaternion-based sensor fusion.',
        'Collaborated on research projects with industry partners and contributed to hardware/software integration.'
    ]),
    ('Undergraduate robotics research', '', 'Mechatronics Engineering · Sepuluh Nopember Institute of Technology, Indonesia', [
        'Developed a vision-based localization and coordination system for two holonomic soccer robots.',
        'Implemented marker recognition, ball tracking, calibration interfaces, and leader–follower behavior.'
    ]),
    ('Engineering Intern', '2011', 'PT. Djaja Sakti Sari · Indonesia', [
        'Supported CAD design, manufacturing, production management, and machine maintenance.',
        'Worked with engineers and technicians on a machine for recovering material from rejected products.'
    ])
]
EDUCATION = [
    ('PhD studies in Computer Science', 'University of Helsinki · Finland', 'May 2024–present', 'In progress. Cloud-native XR and Gaming Using Neural Processing. Paid research began in November 2023.'),
    ('MSc in Electrical Engineering', 'National Taiwan University of Science and Technology · Taiwan', '', 'Thesis: Wearable Motion Tracking System using Quaternion-based Complementary Filter Algorithm with Inertial Measurement Units.'),
    ('Bachelor of Applied Science in Mechatronics Engineering', 'Sepuluh Nopember Institute of Technology · Indonesia', '', 'Thesis: Localization and Synchronization of Multi-agent Robot Soccer based on Visualization.')
]
SKILLS = [
    ('Graphics & XR', ['C++', 'HLSL / GLSL', 'Vulkan', 'OpenXR', 'SteamVR', 'ALVR', 'Eye tracking']),
    ('Video & learning', ['Python', 'PyTorch', 'CUDA', 'Neural video codecs', 'H.265 / HEVC', 'Foveated streaming']),
    ('Evaluation', ['NumPy / pandas', 'Gaze prediction', 'Latency analysis', 'EWPSNR', 'FovVideoVDP', 'User studies']),
    ('Systems foundation', ['Unity / C#', 'Computer vision', 'ROS 2', 'Sensor fusion', 'MATLAB', 'Blender', 'CAD / CAM'])
]

def bullets(items):
    return '<ul>' + ''.join(f'<li>{esc(item)}</li>' for item in items) + '</ul>'

def role_html(role):
    projects = ''.join(f'<div class="experience-project"><h4>{esc(title)}</h4><p>{esc(copy)}</p></div>' for title, copy in role['projects'])
    return f'<article class="timeline-item"><p class="date">{esc(role["dates"])}</p><h3>{esc(role["title"])}</h3><p class="org">{esc(role["org"])}</p><p class="role-intro">{esc(role["intro"])}</p>{bullets(role["bullets"])}<div class="experience-projects"><h4 class="project-group-label">Selected project responsibilities</h4>{projects}</div></article>'

def cv_body(intro, tags):
    extra = '<div class="actions no-print"><a class="button" href="#resume-options">Choose a one-page résumé ↓</a><button class="button secondary" type="button" data-print data-enhanced hidden>Print full CV</button></div><div class="print-only">Adhi Widagdo · adhi-w.github.io · linkedin.com/in/adhi-w</div>'
    body = '<div class="wrap full-cv">' + intro('Curriculum vitae', 'Research depth.<br>Engineering range.', SUMMARY, extra)
    body += '''<section class="resume-options no-print" id="resume-options" aria-label="One-page resumes"><div><span class="eyebrow">For job applications</span><h2>Choose your résumé.</h2><p>The full CV below preserves the detail. These one-page versions select the experience most relevant to a role.</p></div><div class="resume-choice"><h3>XR &amp; video systems</h3><p>Recent focus, with selected work from 2022 onward and a brief telepresence foundation.</p><a href="resume-xr.html">Preview &amp; print →</a><a href="assets/documents/adhi-widagdo-resume-xr.pdf" download>Download one-page PDF ↓</a></div><div class="resume-choice"><h3>Research &amp; engineering</h3><p>A broader view of the 2019–present research period, including VR, robotics, and systems integration.</p><a href="resume-research.html">Preview &amp; print →</a><a href="assets/documents/adhi-widagdo-resume-research.pdf" download>Download one-page PDF ↓</a></div></section>'''
    body += '<div class="split"><aside class="sidebar" aria-label="CV sections and skills"><h2>On this page</h2><ul><li><a href="#experience">Experience</a></li><li><a href="#earlier">Earlier engineering</a></li><li><a href="#education">Education &amp; research training</a></li><li><a href="#skills">Technical toolkit</a></li><li><a href="#recognition">Publications &amp; recognition</a></li></ul><h2>Current focus</h2><p>Cloud-XR &amp; gaming<br>Foveated streaming<br>Neural video compression<br>Perceptual quality</p><a href="projects.html">Explore project evidence →</a><a href="https://www.linkedin.com/in/adhi-w/">LinkedIn ↗</a></aside><div>'
    body += '<section class="cv-section" id="experience"><h2>Research experience</h2>' + role_html(CURRENT) + role_html(OULU) + '</section>'
    body += '<section class="cv-section" id="earlier"><h2>Earlier engineering experience</h2>'
    for title, dates, org, items in EARLIER:
        date = f'<p class="date">{esc(dates)}</p>' if dates else ''
        body += f'<article class="timeline-item">{date}<h3>{esc(title)}</h3><p class="org">{esc(org)}</p>{bullets(items)}</article>'
    body += '</section><section class="cv-section" id="education"><h2>Education &amp; research training</h2>'
    for title, org, dates, note in EDUCATION:
        date = f'<p class="date">{esc(dates)}</p>' if dates else ''
        body += f'<article class="timeline-item">{date}<h3>{esc(title)}</h3><p class="org">{esc(org)}</p><p class="org">{esc(note)}</p></article>'
    body += '</section><section class="cv-section" id="skills"><h2>Technical toolkit</h2><div class="subroles">'
    body += ''.join(f'<div><h4>{esc(title)}</h4>{tags(items)}</div>' for title,items in SKILLS)
    body += '</div></section><section class="cv-section" id="recognition"><h2>Publications &amp; recognition</h2>'
    body += bullets(['First author: Gaze-Adaptive Foveation for Remote Rendered VR · ACM Multimedia 2025.', 'First author: Latency-Driven Optimization for Foveation in Remote Rendered VR · ACM Multimedia 2026 (forthcoming).', 'Co-author: viewpoint-height perception in immersive 360° video · IEEE Telepresence 2024.', 'Best Student Conference Paper · CACS 2015.', 'Earlier team awards include RoboCup 2015 Teen-size Technical Challenge, KORINDO 2010, and KOMURINDO 2011.'])
    return body + '<a class="text-link" href="research.html">Selected publications, preprints &amp; awards →</a></section></div></div></div>'

def resume_data(kind):
    focused = kind == 'xr'
    return {
        'label': 'XR & video systems' if focused else 'Research & engineering',
        'summary': ('Researcher and engineer developing gaze-adaptive VR streaming and neural video compression. Combines C++, GPU shaders, Python, and PyTorch with systems integration and perceptual evaluation.' if focused else 'Researcher and engineer connecting XR software, video systems, and robotics. Experience spans immersive rendering, telepresence, sensing, and user studies; current research focuses on foveated streaming and neural video compression.'),
        'current': ([
            'Implemented gaze-adaptive foveation in ALVR using HLSL/Vulkan, eye tracking, and H.265 streaming; evaluated system supported native 72 FPS.',
            'Developed gaze prediction and latency compensation; reported 24.04% lower mean gaze error in tested conditions, with a collaborative 30-participant study.',
            'Evaluated dynamic foveation using objective quality measures and a 16-participant study; dynamic methods generally improved visual quality over static foveation.',
            'Research foveated neural video compression for VR. Ongoing, unpublished work.',
            'Build C++/Python research software for gaze analysis, parameter tuning, and visual-quality evaluation.',
            'Collaborate with researchers at Aalto University and National Tsing Hua University; contribute to teaching and undergraduate thesis supervision.'
        ] if focused else [
            'Develop gaze-adaptive VR streaming in ALVR, integrating HLSL/Vulkan shaders, eye tracking, H.265, and synchronized server/headset reconstruction.',
            'Build latency compensation, gaze-analysis tools, and perceptual evaluation workflows; contribute to user studies and thesis supervision.',
            'Published foveation work includes a native 72 FPS implementation and collaborative studies with 16 and 30 participants.',
            'Investigate neural video compression for VR. Ongoing, unpublished work.'
        ]),
        'oulu': ([
            'Integrated headset playback, gaze tracking, and event handling for immersive perception studies in 2022–2023; supported user-experience analysis.',
            'Earlier work included rendering 16K panoramic images and 8K video, with Oculus and Varjo headset integration for immersive telepresence.',
            'Supported robot-based headset benchmarking and Python analysis of latency, field of view, and tracking accuracy.'
        ] if focused else [
            'Built immersive rendering for 16K panoramic images and 8K video; integrated Oculus and Varjo headsets, eye tracking, and live media.',
            'Connected VR applications with mobile robotics, ROS 2, navigation, cameras, and inertial sensing; supported deployments and user studies.',
            'Supported robot-based headset benchmarking and Python analysis of motion-to-photon latency, field of view, and tracking accuracy.',
            'Created interactive Unity environments, optimized rendering, and contributed to photogrammetry capture and 3D asset processing.'
        ]),
        'skills': 'C++ · Python · PyTorch · HLSL / GLSL · Vulkan · GPU programming · Systems integration · Perceptual evaluation' if focused else 'C++ · Python · PyTorch · Unity / C# · HLSL / Vulkan · ROS 2 · Computer vision · Sensor fusion · User studies',
        'publications': [
            ('Gaze-Adaptive Foveation for Remote Rendered VR', 'First author · ACM Multimedia 2025', 'https://doi.org/10.1145/3746027.3755620'),
            ('Latency-Driven Optimization for Foveation in Remote Rendered VR', 'First author · ACM Multimedia 2026 (forthcoming)', 'https://doi.org/10.1145/3767308.3835889'),
            ('Investigating a simple technique to alter viewpoint height in immersive 360° video', 'Co-author · IEEE Conference on Telepresence 2024', 'https://doi.org/10.1109/Telepresence63209.2024.10841573')
        ],
        'recognition': 'Best Student Conference Paper, CACS 2015. Team: first place, RoboCup 2015 Teen-size Technical Challenge; second place, Teen-size Soccer.',
        'education': [
            'University of Helsinki · PhD studies in Computer Science, May 2024–present. In progress.',
            'MSc Electrical Engineering · National Taiwan University of Science and Technology (Taiwan Tech).',
            'BASc Mechatronics Engineering · Sepuluh Nopember Institute of Technology, Indonesia.'
        ]
    }

def resume_body(kind):
    data = resume_data(kind)
    return f'''<div class="wrap resume-wrap"><div class="resume-toolbar no-print"><div><span class="eyebrow">One-page résumé · {esc(data['label'])}</span><p>Print at A4, 100% scale, with browser headers and footers off. The PDF download has a fixed one-page layout.</p></div><div class="actions"><a class="button" href="assets/documents/adhi-widagdo-resume-{kind}.pdf" download>Download PDF ↓</a><button class="button secondary" data-print data-enhanced hidden type="button">Print / save as PDF</button><a href="cv.html">Full CV →</a></div></div><article class="resume-sheet"><header><h1>Adhi Widagdo</h1><p class="resume-identity">{esc(IDENTITY)}</p><p class="resume-contact"><a href="https://adhi-w.github.io/">adhi-w.github.io</a> · <a href="https://www.linkedin.com/in/adhi-w/">linkedin.com/in/adhi-w</a> · adhi [dot] cwidagdo [at] gmail [dot] com</p></header><p class="resume-summary">{esc(data['summary'])}</p><section><h2>Experience</h2><h3>{esc(CURRENT['title'])}</h3><p class="resume-meta">University of Helsinki · {esc(CURRENT['dates'])}</p>{bullets(data['current'])}<h3>{esc(OULU['title'])}</h3><p class="resume-meta">University of Oulu · {esc(OULU['dates'])}</p>{bullets(data['oulu'])}</section><section><h2>Selected publications</h2>{''.join(f'<p class="resume-publication"><a href="{url}">{esc(title)}</a><br><span>{esc(note)}</span></p>' for title,note,url in data['publications'])}</section><section><h2>Education &amp; research training</h2>{''.join(f'<p class="resume-education">{esc(row)}</p>' for row in data['education'])}</section><section><h2>Selected recognition</h2><p class="resume-education">{esc(data['recognition'])}</p></section><section><h2>Technical skills</h2><p>{esc(data['skills'])}</p></section></article></div>'''
