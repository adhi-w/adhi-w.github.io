"""Build two fixed, one-page A4 resumes from the shared career content.

Authoring only: python -m pip install reportlab pymupdf
The public site has no PDF-generation runtime dependency.
"""
from pathlib import Path
from html import escape
import unicodedata
import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from profile_content import IDENTITY, CURRENT, OULU, resume_data

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/documents'
INK = colors.HexColor('#18232e')
ACCENT = colors.HexColor('#174b60')
MUTED = colors.HexColor('#44515b')

def clean(value):
    for old, new in [('–', '-'), ('—', '-'), ('·', '|'), ('’', "'")]:
        value = value.replace(old, new)
    return escape(unicodedata.normalize('NFKC', value))

def build(kind):
    data = resume_data(kind)
    styles = {
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.7, leading=13.2, textColor=INK, spaceAfter=5),
        'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=27, leading=30, textColor=INK, spaceAfter=6),
        'identity': ParagraphStyle('identity', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=ACCENT, spaceAfter=6),
        'contact': ParagraphStyle('contact', fontName='Helvetica', fontSize=8, leading=12, textColor=MUTED, spaceAfter=13),
        'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=ACCENT, spaceBefore=10, spaceAfter=5),
        'role': ParagraphStyle('role', fontName='Helvetica-Bold', fontSize=10.2, leading=14, textColor=INK, spaceBefore=6, spaceAfter=2),
        'meta': ParagraphStyle('meta', fontName='Helvetica', fontSize=8.7, leading=12, textColor=MUTED, spaceAfter=5),
        'small': ParagraphStyle('small', fontName='Helvetica', fontSize=9, leading=12, textColor=INK, spaceAfter=4),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.7, leading=13.2, textColor=INK, leftIndent=10, firstLineIndent=-8, spaceAfter=4)
    }
    story=[]
    def para(text, style='body', markup=False):
        story.append(Paragraph(text if markup else clean(text), styles[style]))
    def section(title):
        para(title.upper(), 'section')
        story.append(HRFlowable(width='100%', thickness=.5, color=colors.HexColor('#cad5dc'), spaceAfter=5))
    para('Adhi Widagdo','name')
    para(IDENTITY,'identity')
    para('<link href="https://adhi-w.github.io/" color="#174b60">adhi-w.github.io</link> | <link href="https://www.linkedin.com/in/adhi-w/" color="#174b60">linkedin.com/in/adhi-w</link><br/>adhi [dot] cwidagdo [at] gmail [dot] com', 'contact', True)
    para(data['summary'])
    section('Experience')
    for role, company, key in [(CURRENT,'University of Helsinki','current'),(OULU,'University of Oulu','oulu')]:
        para(role['title'],'role')
        para(company+' | '+role['dates'],'meta')
        for item in data[key]: para('- '+item,'bullet')
    section('Selected publications')
    for title,note,url in data['publications']:
        para(f'<link href="{url}" color="#174b60"><b>{clean(title)}</b></link><br/>{clean(note)}','small',True)
    section('Education & research training')
    for item in data['education']: para(item,'small')
    section('Selected recognition')
    para(data['recognition'],'small')
    section('Technical skills')
    para(data['skills'],'small')
    target=OUT/f'adhi-widagdo-resume-{kind}.pdf'
    SimpleDocTemplate(str(target),pagesize=A4,rightMargin=43,leftMargin=43,topMargin=37,bottomMargin=32,
                      title=f'Adhi Widagdo - {data["label"]} resume',author='Adhi Widagdo').build(story)
    with pymupdf.open(target) as pdf:
        assert len(pdf)==1, f'{target.name}: expected one page, got {len(pdf)}'
        text=pdf[0].get_text()
        assert clean(OULU['title']) in text
        assert 'Technical skills'.upper() in text
    print(f'PASS: {target.name}: one A4 page, {target.stat().st_size:,} bytes.')

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for kind in ('xr','research'): build(kind)
