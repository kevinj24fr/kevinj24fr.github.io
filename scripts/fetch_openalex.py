#!/usr/bin/env python3
"""Refresh scripts/openalex.json: per-DOI authorships with institutions and citation counts, from OpenAlex."""
import json, urllib.request, urllib.parse, time, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pubs=json.load(open('publications.json'))
H={'User-Agent':'kj-site-builder (mailto:kevin.joseph@uniklinik-freiburg.de)'}
out={}
for p in pubs:
    url='https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(p['doi'],safe='')+'?mailto=kevin.joseph@uniklinik-freiburg.de'
    try:
        w=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30))
    except Exception as e:
        print('MISS',p['doi'],str(e)[:50]); continue
    out[p['doi']]={'cited_by_count':w.get('cited_by_count'),'authorships':[{'name':a['author'].get('display_name'),'orcid':a['author'].get('orcid'),
        'institutions':[{'name':i.get('display_name'),'country':i.get('country_code'),'ror':i.get('ror')} for i in a.get('institutions',[])]} for a in w.get('authorships',[])]}
    time.sleep(0.15)
a=json.load(urllib.request.urlopen(urllib.request.Request('https://api.openalex.org/authors?filter=orcid:0000-0001-6317-8736&mailto=kevin.joseph@uniklinik-freiburg.de',headers=H),timeout=30))
me=a['results'][0] if a['results'] else {}
out['_author']={'works_count':me.get('works_count'),'cited_by_count':me.get('cited_by_count'),'h_index':(me.get('summary_stats') or {}).get('h_index'),'i10':(me.get('summary_stats') or {}).get('i10_index'),'openalex_id':me.get('id')}
json.dump(out,open('scripts/openalex.json','w'),indent=1,ensure_ascii=False)
print(len(out)-1,'works resolved;',out['_author'])
