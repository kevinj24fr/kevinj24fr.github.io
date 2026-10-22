#!/usr/bin/env python3
"""Build every page of kevinj24fr.github.io from scripts/pages/*.html + publications.json."""
import json, html, re, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
V='2026-10-22j'
pubs=json.load(open('publications.json'))
SPLIT=re.compile(r'[\s\-]+')
def initials(a):
    if ',' in a:
        last,first=[x.strip() for x in a.split(',',1)]
        return last+' '+''.join(w[0] for w in SPLIT.split(first) if w)
    return a
def authors_html(auths):
    names=[initials(a) for a in auths]
    fmt=lambda n: ('<b>'+html.escape(n)+'</b>') if n.startswith('Joseph') else html.escape(n)
    if len(names)<=5: return ', '.join(fmt(n) for n in names)
    ji=next((i for i,n in enumerate(names) if n.startswith('Joseph')),None)
    parts=[fmt(names[0]),fmt(names[1])]
    if ji is not None and 1<ji<len(names)-1: parts+=['…',fmt(names[ji])]
    parts+=['…',fmt(names[-1])]
    return ', '.join(parts).replace(', …, ',' … ').replace(', …',' …')
jname={'Iscience':'iScience','Plos one':'PLOS ONE','PLoS One':'PLOS ONE','Nature cell biology':'Nature Cell Biology','Nature communications':'Nature Communications','Nature neuroscience':'Nature Neuroscience','Cell death & disease':'Cell Death & Disease','Communications biology':'Communications Biology','Cancer cell':'Cancer Cell','Life science alliance':'Life Science Alliance','Scientific reports':'Scientific Reports','Journal of neural engineering':'Journal of Neural Engineering','EMBO molecular medicine':'EMBO Molecular Medicine','STAR protocols':'STAR Protocols','BioRxiv':'bioRxiv','2023 IEEE BioSensors Conference (BioSensors)':'IEEE BioSensors Conference'}
def find(prefix):
    p=next((p for p in pubs if p['title'].lower().startswith(prefix.lower())),None)
    if p is None: sys.exit('no publication starts with: '+prefix)
    return p
def entry(p,year=False,role=None):
    j=jname.get(p['journal'],p['journal'])+((' '+str(p['year'])) if year else '')
    tag=' <span class="tag">preprint</span>' if p['preprint'] else ''
    r=(' <span class="tag role">'+html.escape(role)+'</span>') if role else ''
    return ('<li><a href="https://doi.org/'+html.escape(p["doi"])+'" target="_blank" rel="noopener noreferrer">'+html.escape(p["title"])+'</a>'+tag+r
            +'<span class="meta">'+authors_html(p["authors"])+' · <i>'+html.escape(j)+'</i></span></li>')
def L(prefix,label):
    """inline link to a paper by title prefix, labelled e.g. 'Cancer Cell 2022'"""
    p=find(prefix); return '<a href="https://doi.org/'+html.escape(p['doi'])+'" target="_blank" rel="noopener noreferrer"><i>'+label+'</i></a>'
years=sorted({p['year'] for p in pubs},reverse=True)
def yearblock(y): return '<div class="yr"><div class="yr-label mono">'+str(y)+'</div><ol>'+''.join(entry(p) for p in pubs if p['year']==y)+'</ol></div>'
LEAD=[('Human organotypic brain slice culture','shared first author'),
      ('Human brain slice cultures: translational','first author'),
      ('Transcriptional characterization of the glial response','first author'),
      ('Inhibition of metabotropic glutamate receptor III','last & corresponding author'),
      ('MicroFace maps microglial morphology','last author')]
lead_html='<div class="yr"><div class="yr-label mono">lead</div><ol>'+''.join(entry(find(t),True,r) for t,r in LEAD)+'</ol></div>'
all_html=''.join(yearblock(y) for y in years)
NAV=[('/','home'),('/research/','research'),('/papers/','papers'),('/tools/','tools'),('/about/','about')]
def layout(path,title,desc,body):
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if h==path else '',n) for h,n in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="author" content="Kevin Joseph">
  <link rel="canonical" href="https://kevinj24fr.github.io{path}">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="https://kevinj24fr.github.io{path}">
  <meta property="og:image" content="https://kevinj24fr.github.io/assets/img/kevin-joseph.jpg">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:image" content="https://kevinj24fr.github.io/assets/img/kevin-joseph.jpg">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%2314213d'/%3E%3Ctext x='32' y='44' font-family='Menlo,monospace' font-size='28' font-weight='700' fill='%23f6f4ef' text-anchor='middle'%3Ekj%3C/text%3E%3C/svg%3E">
  <meta name="theme-color" content="#f6f4ef" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f1a2e" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="/assets/css/style.css?v={V}">
  <script>(function(){{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}})();</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand mono" href="/">kevin joseph</a>
    <nav aria-label="Pages" class="mono">{nav}</nav>
    <button id="theme-toggle" class="toggle mono" type="button" aria-label="Toggle dark mode" title="Toggle dark mode"><span class="t-light">dark</span><span class="t-dark">light</span></button>
  </div>
  <nav aria-label="Pages, small screens" class="mono nav-small">{nav}</nav>
</header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="foot mono">
  <div class="wrap">
    <p>static html · one css file · 20 lines of js · no analytics · no cookies · <a href="https://github.com/kevinj24fr/kevinj24fr.github.io" target="_blank" rel="noopener noreferrer">source</a></p>
    <p>© <span id="year">2026</span> Kevin Joseph · last updated 2026-10-22</p>
  </div>
</footer>
<script src="/assets/js/main.js?v={V}"></script>
</body>
</html>
'''
PAGES=[('/','index.html','Kevin Joseph — NeuroEngineering, Freiburg','Kevin Joseph leads the NeuroEngineering lab at the Department of Neurosurgery, Medical Center – University of Freiburg. Glial signalling in intact human brain tissue, measured with electrophysiology, spatial genomics, and machine learning.'),
       ('/research/','research/index.html','Research — Kevin Joseph','How glial cells receive, integrate, and transmit signals in intact human brain tissue: platforms, findings, and the programme ahead.'),
       ('/papers/','papers/index.html','Papers — Kevin Joseph','Peer-reviewed papers and preprints by Kevin Joseph, with DOIs.'),
       ('/tools/','tools/index.html','Tools — Kevin Joseph','Open-source Rust, R, and Python tools for transcriptomics, proteomics, imaging, and electrophysiology.'),
       ('/about/','about/index.html','About — Kevin Joseph','Career, education, funding, teaching, and service.')]
for path,out,title,desc in PAGES:
    name='home' if path=='/' else path.strip('/')
    body=open('scripts/pages/%s.html'%name).read()
    body=body.replace('{{LEAD}}',lead_html).replace('{{ALL}}',all_html).replace('{{N_ALL}}',str(len(pubs)))
    body=re.sub(r'\{\{L:([^|]+)\|([^}]+)\}\}',lambda m:L(m.group(1),m.group(2)),body)
    os.makedirs(os.path.dirname(out) or '.',exist_ok=True)
    page=layout(path,title,desc,body)
    import html.parser; hp=html.parser.HTMLParser(); hp.feed(page)
    open(out,'w').write(page); print('wrote',out)
