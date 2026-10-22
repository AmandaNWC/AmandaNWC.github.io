"""Build the academic CV: python cv/build_cv.py [output.pdf]. Requires reportlab."""
from pathlib import Path
import json, sys
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'cv' / 'cv.json').read_text(encoding='utf-8-sig'))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'NaiWen_Chi_CV.pdf'
NAVY = colors.HexColor('#183548')
GRAY = colors.HexColor('#53616A')
WIDTH = A4[0] - 96
styles = {
 'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=10.1, leading=12.8, spaceAfter=3.6),
 'small': ParagraphStyle('small', fontName='Times-Roman', fontSize=9.25, leading=11.5, spaceAfter=3),
 'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=10, leading=12.6, textColor=NAVY),
 'org': ParagraphStyle('org', fontName='Times-Italic', fontSize=10, leading=12.5, textColor=GRAY, spaceAfter=3),
 'date': ParagraphStyle('date', fontName='Helvetica', fontSize=8.9, leading=12.6, alignment=TA_RIGHT, textColor=GRAY),
 'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=10.2, leading=14, textColor=NAVY, spaceBefore=10, spaceAfter=6),
 'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=25, leading=29, textColor=NAVY, spaceAfter=6),
 'contact': ParagraphStyle('contact', fontName='Helvetica', fontSize=9, leading=12, textColor=GRAY, spaceAfter=3)
}
def p(t, style='body'):
    return Paragraph(t, styles[style])
def sec(t):
    return p(t.upper(), 'section')
def entry(item, bullets=True):
    row = Table([[p(escape(item['title']), 'title'),p(item['date'], 'date')]], colWidths=[WIDTH-119,119])
    row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    result=[row,p(escape(item['org']),'org')]
    if bullets:
        for text in item['bullets']:
            result.append(Paragraph(escape(text), ParagraphStyle('bullet',parent=styles['body'],leftIndent=10,firstLineIndent=-8),bulletText='-'))
    else:
        result.append(p(escape(item['detail']),'small'))
    result.append(Spacer(1,4))
    return KeepTogether(result)

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#D7DFE3'))
    canvas.line(48,40,A4[0]-48,40)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(GRAY)
    canvas.drawString(48,28,'Nai-Wen Chi | Academic CV | '+DATA['updated'])
    canvas.drawRightString(A4[0]-48,28,str(doc.page))
    if doc.page > 1:
        canvas.setFont('Helvetica-Bold',9)
        canvas.drawString(48,A4[1]-33,'NAI-WEN CHI')
        canvas.setFont('Helvetica',8)
        canvas.drawRightString(A4[0]-48,A4[1]-33,'RESEARCH & ACADEMIC CV')

story=[p(DATA['name'],'name'),p(DATA['location']+' | <link href="mailto:'+DATA['email']+'">'+DATA['email']+'</link>','contact'),p('<link href="https://amandanwc.github.io/">Research portfolio</link> | <link href="https://scholar.google.com/citations?user=US6jRQwAAAAJ">Google Scholar</link> | <link href="https://orcid.org/0009-0006-4289-9191">ORCID: 0009-0006-4289-9191</link> | <link href="https://www.linkedin.com/in/nai-wen-chi-4a9478124/">LinkedIn</link>','contact'),sec('Research interests'),p(DATA['interests']),sec('Education')]
story += [entry(e,False) for e in DATA['education']]
story.append(sec('Research & translational experience'))
story += [entry(e) for e in DATA['research']]
story += [PageBreak(),sec('Peer-reviewed publications')]
for i, pub in enumerate(DATA['publications'],1):
    story.append(KeepTogether([p(f"<b>{i}.</b> {pub['authors']} {pub['title']} <i>{pub['journal']}</i>. {pub['citation']}. <link href='https://doi.org/{pub['doi']}'>doi:{pub['doi']}</link>"),Spacer(1,3)]))
story += [sec('Patents & published applications | Co-inventor')]
for patent in DATA['patents']:
    story.append(KeepTogether([p('<b>'+escape(patent['title'])+'.</b> '+patent['detail'],'small'),Spacer(1,2)]))
story += [sec('Regulatory experience')]
story += [entry(e) for e in DATA['regulatory']]
story += [sec('Research methods')]
for label, content in DATA['skills']:
    story.append(p('<b>'+escape(label)+':</b> '+escape(content),'small'))
story += [sec('Additional experience & professional development')]
for text in DATA['additional']:
    story.append(p(text,'small'))
OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=A4,rightMargin=48,leftMargin=48,topMargin=48,bottomMargin=51,title='Nai-Wen Chi | Academic CV',author=DATA['name'],subject='Research experience, publications, patents and academic background').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
