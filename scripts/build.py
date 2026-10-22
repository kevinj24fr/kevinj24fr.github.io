import json, html, re
pubs=json.load(open('publications.json'))
SPLIT=re.compile(r'[\s\-]+')
def initials(a):
    if ',' in a:
        last,first=[x.strip() for x in a.split(',',1)]
        ini=''.join(w[0] for w in SPLIT.split(first) if w)
        return last+' '+ini
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
def entry(p):
    j=jname.get(p['journal'],p['journal'])
    tag=' <span class="tag">preprint</span>' if p['preprint'] else ''
    return ('<li><a href="https://doi.org/'+html.escape(p["doi"])+'" target="_blank" rel="noopener noreferrer">'+html.escape(p["title"])+'</a>'+tag
            +'<span class="meta">'+authors_html(p["authors"])+' · <i>'+html.escape(j)+'</i></span></li>')
years=sorted({p['year'] for p in pubs},reverse=True)
def yearblock(y): return '<div class="yr"><div class="yr-label mono">'+str(y)+'</div><ol>'+''.join(entry(p) for p in pubs if p['year']==y)+'</ol></div>'
recent=''.join(yearblock(y) for y in years if y>=2024)
older=''.join(yearblock(y) for y in years if y<2024)
n_old=sum(1 for p in pubs if p['year']<2024); n_all=len(pubs)
tpl=open('scripts/template.html').read()
page=tpl.replace('{{RECENT}}',recent).replace('{{OLDER}}',older).replace('{{N_OLD}}',str(n_old)).replace('{{N_ALL}}',str(n_all))
open('index.html','w').write(page)
import html.parser; p=html.parser.HTMLParser(); p.feed(page); print('html ok', page.count('<li><a href="https://doi.org/'),'pubs')
