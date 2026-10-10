#!/usr/bin/env python3
"""Render inspection pages and contact sheets; report text and page-size checks."""
from pathlib import Path
import json, subprocess, argparse, shutil
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
import pdfplumber

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('pdf', nargs='?', default=str(ROOT/'release/paper.pdf'))
a=p.parse_args()
pdf=Path(a.pdf).resolve()
qa=ROOT/'tmp'/'pdf-qa'/pdf.stem
qa.mkdir(parents=True,exist_ok=True)
renderer=shutil.which('pdftoppm')
if not renderer:
    raise SystemExit('pdftoppm is required on PATH for visual QA')
# Remove prior generated previews so a shorter revision has no stale pages.
for pattern in ['page-*.png', 'contact-*.jpg']:
    for previous in qa.glob(pattern):
        previous.unlink()
subprocess.run([renderer,'-scale-to','1400','-png',str(pdf),str(qa/'page')],check=True)
paths=sorted(qa.glob('page-*.png'))
for group_start in range(0,len(paths),6):
    items=paths[group_start:group_start+6]
    canvas=Image.new('RGB',(1200,1740),'#ddd')
    d=ImageDraw.Draw(canvas)
    for i,f in enumerate(items):
        im=Image.open(f).convert('RGB');im.thumbnail((388,820))
        x=(i%3)*400+(400-im.width)//2;y=(i//3)*870+30
        canvas.paste(im,(x,y));d.text(((i%3)*400+15,(i//3)*870+10),f.name,fill='black')
    canvas.save(qa/f'contact-{group_start//6+1}.jpg')
reader=PdfReader(pdf)
with pdfplumber.open(pdf) as doc:
    clips=[]
    for page_no,page in enumerate(doc.pages,1):
        for word in page.extract_words():
            if word['x0']<20 or word['x1']>float(page.width)-20 or word['top']<15 or word['bottom']>float(page.height)-15:
                clips.append({'page':page_no,'text':word['text'],'box':[word['x0'],word['top'],word['x1'],word['bottom']]})
    result={'pdf':str(pdf),'pages':len(reader.pages),'bytes':pdf.stat().st_size,'text_words':sum(len((p.extract_text()or'').split()) for p in reader.pages),'page_sizes':sorted(set((float(p.mediabox.width),float(p.mediabox.height))for p in reader.pages)),'edge_text':clips,'blank_pages':[i for i,p in enumerate(reader.pages,1)if not (p.extract_text()or'').strip()],'contact_sheets':[str(f)for f in sorted(qa.glob('contact-*.jpg'))]}
(qa/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
