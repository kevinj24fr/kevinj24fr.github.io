#!/usr/bin/env python3
"""Build every page of kevinj24fr.github.io from scripts/pages/*.html + publications.json."""
import json, html, re, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
V='2026-10-23j'
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

# ---------- trajectory strip ----------
traj=json.load(open('scripts/trajectory.json'))
TOPIC_ORDER=['neurotransmission & stimulation','neural implants & interface','human tissue models','glioma microenvironment','spatial & single-cell','neurodegeneration','meningioma','neurosurgery & diagnostics']
YEARS=list(range(2014,2027))
def trajectory_svg():
    from collections import Counter
    cnt=Counter((i['topic'],i['year']) for i in traj)
    papers=Counter((i['topic'],i['year']) for i in traj if i['kind']=='paper')
    left,top,cw,rh=250,34,46,30
    W=left+cw*len(YEARS)+20; Hh=top+rh*len(TOPIC_ORDER)+30
    s=[f'<svg class="traj" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="traj-t traj-d" xmlns="http://www.w3.org/2000/svg">',
       '<title id="traj-t">Publications by topic and year, 2014 to 2026</title>',
       '<desc id="traj-d">Each dot is scaled by the number of papers and conference abstracts on that topic in that year. The work moves from neurotransmission and stimulation, through neural implants, into the glioma microenvironment, spatial genomics, meningioma, and diagnostics.</desc>']
    for j,y in enumerate(YEARS):
        x=left+cw*j+cw/2
        s.append(f'<text class="yr" x="{x}" y="{top-12}" text-anchor="middle">{str(y)[2:]}</text>')
        s.append(f'<line class="grid" x1="{x}" y1="{top-4}" x2="{x}" y2="{top+rh*len(TOPIC_ORDER)-8}"/>')
    for i,t in enumerate(TOPIC_ORDER):
        y=top+rh*i+rh/2
        s.append(f'<text class="lbl" x="{left-14}" y="{y+4}" text-anchor="end">{html.escape(t)}</text>')
        for j,yr in enumerate(YEARS):
            n=cnt[(t,yr)]
            if not n: continue
            x=left+cw*j+cw/2; r=4+2.6*(n**0.5)
            p=papers[(t,yr)]
            cls='dot' if p else 'dot abs'
            s.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r:.1f}"><title>{html.escape(t)}, {yr}: {n} item{"s" if n>1 else ""} ({p} paper{"s" if p!=1 else ""})</title></circle>')
    s.append(f'<text class="cap" x="{left}" y="{Hh-6}">dot area ∝ papers + conference abstracts that year · hollow = abstracts only · 20 = 2020</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- collaborators ----------
oa=json.load(open('scripts/openalex.json'))
HOME={'university of freiburg','university medical center freiburg','deutsches konsortium für translationale krebsforschung','german cancer research center'}
ALIAS={'city of hope':'City of Hope','city of hope national medical center':'City of Hope','beckman research institute':'City of Hope',
       'robert h. lurie comprehensive cancer center of northwestern university':'Northwestern University','university hospital zurich':'University of Zurich',
       'university hospital bonn':'University of Bonn','inserm':'Inserm','centre national de la recherche scientifique':'CNRS'}
COUNTRY={'DE':'Germany','FR':'France','CH':'Switzerland','US':'United States','IL':'Israel','LT':'Lithuania','NO':'Norway','FI':'Finland','GB':'United Kingdom','AT':'Austria','NL':'Netherlands','IT':'Italy','ES':'Spain','SE':'Sweden','DK':'Denmark','BE':'Belgium','CA':'Canada','AU':'Australia','IN':'India','CN':'China','JP':'Japan','PL':'Poland','CZ':'Czechia','PT':'Portugal','IE':'Ireland','LU':'Luxembourg','HU':'Hungary','GR':'Greece','TR':'Türkiye','KR':'South Korea'}
def collab_html():
    from collections import Counter, defaultdict
    inst=Counter(); ictry={}; coauth=Counter()
    for doi,w in oa.items():
        if doi.startswith('_'): continue
        seen=set()
        for a in w['authorships']:
            nm=a['name'] or ''
            if 'Joseph' in nm and 'Kevin' in nm: continue
            if nm: coauth[nm]+=1
            for i in a['institutions']:
                if not i['name']: continue
                key=i['name'].strip().lower()
                if key in HOME: continue
                name=ALIAS.get(key,i['name'].strip())
                if name in seen: continue
                seen.add(name); inst[name]+=1
                if i['country'] and name not in ictry: ictry[name]=i['country']
                if name=='City of Hope': ictry[name]='US'
                if name=='Northwestern University': ictry[name]='US'
    top=[(n,k) for n,k in sorted(inst.items(), key=lambda kv:(-kv[1],kv[0])) if k>=3]
    names=[f'{html.escape(n)} ({COUNTRY.get(ictry.get(n,""),ictry.get(n,""))})' for n,k in top]
    line='<p class="after">Closest partners, three or more shared papers: '+', '.join(names)+'. Hover a country for its count.</p>'
    out=[line]
    return map_svg()+'\n'+'\n'.join(out)

# ---------- world map ----------
world=json.load(open('scripts/world.json'))
def collab_counts():
    from collections import Counter
    ctry=Counter()
    for doi,w in oa.items():
        if doi.startswith('_'): continue
        cs=set()
        for a in w['authorships']:
            nm=a['name'] or ''
            if 'Joseph' in nm and 'Kevin' in nm: continue
            for i in a['institutions']:
                if not i['name'] or i['name'].strip().lower() in HOME: continue
                c=i['country'] or ({'City of Hope':'US','Northwestern University':'US'}.get(ALIAS.get(i['name'].strip().lower(),i['name'].strip())))
                if c: cs.add(c)
        for c in cs: ctry[c]+=1
    return ctry
def map_svg():
    ctry=collab_counts()
    mx=max(ctry.values()) if ctry else 1
    W,H=world['w'],world['h']
    s=[f'<svg class="wmap" viewBox="0 0 {W} {H}" role="img" aria-labelledby="wm-t wm-d" xmlns="http://www.w3.org/2000/svg">',
       '<title id="wm-t">Countries of collaborating institutions</title>',
       '<desc id="wm-d">World map with the home country, Germany, and each country of a co-author institution shaded by the number of shared papers.</desc>']
    def style(code):
        if code=='DE': return 'home','Germany, home'
        if code in ctry:
            n=ctry[code]; lvl=1+int(3*(n-1)/max(1,mx-1)) if mx>1 else 1
            return f'c c{min(lvl,4)}', f'{COUNTRY.get(code,code)}: {n} shared paper{"s" if n!=1 else ""}'
        return 'land',''
    def path(code,d):
        cls,t=style(code)
        return f'<path class="{cls}" d="{d}">'+(f'<title>{html.escape(t)}</title>' if t else '')+'</path>'
    for code,d in world['countries'].items(): s.append(path(code,d))
    # Europe inset: own copy of the outlines whose bounding box touches the inset window
    e=world['europe']; iw=170; ih=round(iw*e['h']/e['w']); ix,iy=40,H-ih-30
    def bbox(d):
        nums=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',d)]
        xs=nums[0::2]; ys=nums[1::2]; return min(xs),min(ys),max(xs),max(ys)
    s.append(f'<rect class="inset-bg" x="{ix-1}" y="{iy-1}" width="{iw+2}" height="{ih+2}"/>')
    s.append(f'<svg x="{ix}" y="{iy}" width="{iw}" height="{ih}" viewBox="{e["x"]} {e["y"]} {e["w"]} {e["h"]}" preserveAspectRatio="xMidYMid slice">')
    for code,d in world['countries'].items():
        x0,y0,x1,y1=bbox(d)
        if x1<e['x'] or x0>e['x']+e['w'] or y1<e['y'] or y0>e['y']+e['h']: continue
        s.append(path(code,d))
    s.append('</svg>')
    s.append(f'<text class="inset-lbl" x="{ix+6}" y="{iy+14}">europe</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- conference abstracts line ----------
def abstracts_line():
    from collections import Counter
    ab=[i for i in traj if i['kind']=='abstract']
    return f'{len(ab)} conference abstracts are not listed: most in the EANO and SNO meeting supplements of <i>Neuro-Oncology</i>, the rest in <i>GLIA</i>, <i>Cancer Research</i>, the <i>European Journal of Neurology</i>, and the DGNC sections meeting.'

# ---------- structured data ----------
PERSON={"@context":"https://schema.org","@type":"Person","name":"Kevin Joseph","honorificPrefix":"Dr.-Ing.","jobTitle":"Research Group Leader, Laboratory for NeuroEngineering",
  "affiliation":{"@type":"Organization","name":"Department of Neurosurgery, Medical Center – University of Freiburg","url":"https://www.uniklinik-freiburg.de/neurochirurgie.html"},
  "email":"mailto:kevin.joseph@uniklinik-freiburg.de","url":"https://kevinj24fr.github.io/","image":"https://kevinj24fr.github.io/assets/img/kevin-joseph.jpg",
  "sameAs":["https://orcid.org/0000-0001-6317-8736","https://scholar.google.de/citations?user=s10D-HEAAAAJ","https://github.com/kevinj24fr","https://www.linkedin.com/in/josephkevin","https://openalex.org/A5035795519"],
  "knowsAbout":["glial signalling","spatial transcriptomics","single-cell genomics","human organotypic brain slice culture","neural implants","glioblastoma","neurotechnology","bioinformatics"]}
def papers_jsonld():
    items=[]
    for i,p in enumerate(pubs,1):
        items.append({"@type":"ListItem","position":i,"item":{"@type":"ScholarlyArticle","headline":p['title'],"url":"https://doi.org/"+p['doi'],"sameAs":"https://doi.org/"+p['doi'],
            "datePublished":str(p['year']),"isPartOf":{"@type":"Periodical","name":jname.get(p['journal'],p['journal'])},
            "author":[{"@type":"Person","name":initials(a)} for a in p['authors']]}})
    return {"@context":"https://schema.org","@type":"ItemList","name":"Publications of Kevin Joseph","numberOfItems":len(pubs),"itemListElement":items}
def jsonld_tag(obj): return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>'

NAV=[('/','home'),('/research/','research'),('/papers/','papers'),('/tools/','tools'),('/about/','about')]
def layout(path,title,desc,body,jsonld=''):
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
  <meta property="og:site_name" content="Kevin Joseph">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="https://kevinj24fr.github.io{path}">
  <meta property="og:image" content="https://kevinj24fr.github.io/assets/img/card.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Kevin Joseph, NeuroEngineering, Freiburg: three perturbations, one glial response, three readouts">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://kevinj24fr.github.io/assets/img/card.png">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%2314213d'/%3E%3Ctext x='32' y='44' font-family='Menlo,monospace' font-size='28' font-weight='700' fill='%23f6f4ef' text-anchor='middle'%3Ekj%3C/text%3E%3C/svg%3E">
  <meta name="theme-color" content="#f6f4ef" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f1a2e" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="/assets/css/style.css?v={V}">
  {jsonld}
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
    <p>© <span id="year">2026</span> Kevin Joseph · <a href="https://github.com/kevinj24fr/kevinj24fr.github.io" target="_blank" rel="noopener noreferrer">source</a></p>
  </div>
</footer>
<script src="/assets/js/main.js?v={V}"></script>
</body>
</html>
'''
PAGES=[('/','index.html','Kevin Joseph – NeuroEngineering, Neurosurgery Freiburg','Kevin Joseph, Dr.-Ing., leads the Laboratory for NeuroEngineering at the Department of Neurosurgery, Medical Center – University of Freiburg: glial signalling in living human brain tissue, spatial genomics, neural implants, Rust tools.'),
       ('/research/','research/index.html','Research: glial signalling in human brain tissue – Kevin Joseph, Freiburg','Human brain slice cultures, spatial and single-cell genomics, electrophysiology, and machine learning to ask how glial cells respond to tumours, implants, and amyloid. Lab of Kevin Joseph, Neurosurgery Freiburg.'),
       ('/papers/','papers/index.html','Papers – Kevin Joseph, Neurosurgery Freiburg','Peer-reviewed papers and preprints by Kevin Joseph with DOIs: Cancer Cell, Nature Communications, iScience, Neuro-Oncology, Biomaterials, Life Science Alliance. Glioblastoma, meningioma, neural implants, human tissue models.'),
       ('/tools/','tools/index.html','Tools: karna, h5utils, peek-series, atman, mpx2nwb – Kevin Joseph','Open-source Rust tools for bioinformatics by Kevin Joseph: karna transcriptomics engine, h5utils for h5ad files, peek-series format inspectors, atman proteomics, mpx2nwb electrophysiology conversion.'),
       ('/about/','about/index.html','About Kevin Joseph – Dr.-Ing., Research Group Leader, Freiburg','Career, lab, collaborators, teaching, and contact for Kevin Joseph, biomedical engineer and neuroscientist leading the Laboratory for NeuroEngineering at the Department of Neurosurgery, University of Freiburg.')]
for path,out,title,desc in PAGES:
    name='home' if path=='/' else path.strip('/')
    body=open('scripts/pages/%s.html'%name).read()
    body=body.replace('{{LEAD}}',lead_html).replace('{{ALL}}',all_html).replace('{{N_ALL}}',str(len(pubs)))
    body=body.replace('{{TRAJECTORY}}',trajectory_svg()).replace('{{COLLAB}}',collab_html()).replace('{{ABSTRACTS}}',abstracts_line())
    jl=jsonld_tag(PERSON) if name in ('home','about') else (jsonld_tag(papers_jsonld()) if name=='papers' else '')
    body=re.sub(r'\{\{L:([^|]+)\|([^}]+)\}\}',lambda m:L(m.group(1),m.group(2)),body)
    os.makedirs(os.path.dirname(out) or '.',exist_ok=True)
    page=layout(path,title,desc,body,jl)
    import html.parser; hp=html.parser.HTMLParser(); hp.feed(page)
    open(out,'w').write(page); print('wrote',out)

# ---------- sitemap and robots ----------
LASTMOD='2026-10-23'
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path,_,_,_ in PAGES: sm.append(f'  <url><loc>https://kevinj24fr.github.io{path}</loc><lastmod>{LASTMOD}</lastmod></url>')
sm.append('</urlset>'); open('sitemap.xml','w').write('\n'.join(sm)+'\n')
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://kevinj24fr.github.io/sitemap.xml\n')
print('wrote sitemap.xml robots.txt')
