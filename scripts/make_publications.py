#!/usr/bin/env python3
"""Rebuild publications.json from a Google Scholar CSV export, resolving DOIs through Crossref.

usage: python3 -I scripts/make_publications.py /path/to/citations.csv
Keeps peer-reviewed papers and preprints from 2018 on; drops conference abstracts, posters, the
thesis, and preprints that duplicate a journal paper. Prefers the journal DOI over bioRxiv, SSRN
and Research Square. Preserves the `selected` field from the existing publications.json by title.
Review the printed table before committing; anything marked NO DOI needs a manual fix.
"""
import csv, re, json, sys, os, time, difflib, urllib.request, urllib.parse
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src=sys.argv[1]
H={'User-Agent':'kj-site-builder (mailto:kevin.joseph@uniklinik-freiburg.de)'}
PRE=('10.1101/','10.64898/','10.21203/','10.2139/')
old={p['title']:p for p in json.load(open('publications.json'))} if os.path.exists('publications.json') else {}
rows=list(csv.DictReader(open(src, encoding='utf-8-sig')))
abstract_pat=re.compile(r'^(P\d+\.|OS\d+\.|EXTH-|CNSC-|TAMI-|IMMU-|TMOD-|TMIC-|Poster:)', re.I)
SKIP_PREFIX=('Hypoxia shapes tumor immune microenvironment','Spatial analysis reveals the evolving organization of low-grade','Iron-Associated Mesenchymal Plasticity')  # abstracts or duplicate preprints
keep=[]
for r in rows:
    y=int(r['Year'] or 0); t=r['Title'].strip(); pub=r['Publication'].strip()
    if y<2018 or abstract_pat.match(t) or pub=='' or 'Tagungswoche' in pub or t.startswith(SKIP_PREFIX): continue
    if pub in ('GLIA','NEURO-ONCOLOGY','PREPRINT','EUROPEAN JOURNAL OF NEUROLOGY') or 'Albert-Ludwigs' in r['Publisher']: continue
    if pub=='Cancer Research' and t.endswith('.'): continue
    keep.append(dict(year=y,title=t,authors=[a.strip() for a in r['Authors'].split(';') if a.strip()],journal=pub,preprint=pub.lower()=='biorxiv',doi=old.get(t,{}).get('doi'),selected=old.get(t,{}).get('selected')))
norm=lambda s: re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def lookup(k):
    q=urllib.parse.urlencode({'query.bibliographic':k['title'],'query.container-title':k['journal'],'rows':6,'select':'DOI,title,container-title,author'})
    items=json.load(urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works?'+q,headers=H),timeout=30))['message']['items']
    best=None
    for it in items:
        ct=(it.get('title') or [''])[0]
        if difflib.SequenceMatcher(None,norm(ct),norm(k['title'])).ratio()<0.85: continue
        if 'Joseph' not in ' '.join((a.get('family') or '') for a in it.get('author',[])): continue
        if k['preprint']==it['DOI'].startswith(PRE): return it['DOI']
        best=best or it['DOI']
    return best
for k in keep:
    if k['doi'] and (k['preprint'] or not k['doi'].startswith(PRE)): continue
    try: k['doi']=lookup(k) or k['doi']
    except Exception as e: print('ERR',k['title'][:60],e)
    time.sleep(0.3)
    print(k['year'],'|',k['doi'] or 'NO DOI','|',k['title'][:70])
keep.sort(key=lambda k:(-k['year'],k['preprint'],k['title']))
json.dump(keep,open('publications.json','w'),indent=1,ensure_ascii=False)
print(len(keep),'entries;',sum(1 for k in keep if not k['doi']),'without DOI')
