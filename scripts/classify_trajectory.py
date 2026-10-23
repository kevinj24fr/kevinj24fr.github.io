#!/usr/bin/env python3
"""Rebuild scripts/trajectory.json from a Google Scholar CSV export.

usage: python3 -I scripts/classify_trajectory.py /path/to/citations.csv
Every row is kept (papers, abstracts, thesis) and given a kind and one topic. The topic rules are
title regexes; the precedence list decides ties. Prints the unclassified rows so the rules can be
extended; the build expects none.
"""
import csv, re, json, sys, os, collections
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src=sys.argv[1]
rows=list(csv.DictReader(open(src, encoding='utf-8-sig')))
abstract_pat=re.compile(r'^(P\d+\.|OS\d+\.|EXTH-|CNSC-|TAMI-|IMMU-|TMOD-|TMIC-|Poster:)', re.I)
def kind(r):
    t=r['Title']; pub=r['Publication'].strip()
    if abstract_pat.match(t) or pub.upper() in ('GLIA','NEURO-ONCOLOGY') or 'Tagungswoche' in pub or (pub=='Cancer Research' and t.endswith('.')) or pub.upper()=='EUROPEAN JOURNAL OF NEUROLOGY': return 'abstract'
    if 'Albert-Ludwigs' in r['Publisher']: return 'thesis'
    if pub=='' and r['Year']=='2018' and 'tomographic' in t: return 'abstract'
    if pub=='': return 'other'
    return 'paper'
TOPICS=[('neurotransmission & stimulation',r'glutamate|gaba|serotonin|5-ht|dopamine|leptin|high frequency stimulation|deep brain stimulation|hfs|nucleus accumbens|caudate|neurotransmitter|epileptic|pyramidal|waveform|blanking|spike train|seizure'),
        ('neural implants & interface',r'implant|probe|electrode|microprobe|brain-probe|material-tissue|neural interface|microfluidic|electrochemical sensor|old wires|capri|neural implant|nwb|microinjury|microface|flexible'),
        ('glioma microenvironment',r'glioblastoma|gbm|glioma|astrocytoma|astrocyte|microglia|myeloid|t cell|t-cell|immune|il-10|interleukin|chitinase|zbtb18|smac|lymphoid|myeloiden|tumor-host|tumour'),
        ('spatial & single-cell',r'spatial|single-cell|scrna|single cell|transcriptom|sptcr|sequencing|atlas|developmental trajectory|niche'),
        ('human tissue models',r'slice|organotypic|ex vivo|ex-vivo|cerebellum|cryogel|tumoroid|organoid|cortical slice|brain slice|human2human|autografted|cultures'),
        ('meningioma',r'meningioma'),
        ('neurosurgery & diagnostics',r'dura|platelet|fibrin|sellar|biopsy|shunt|csf|cerebrospinal|hypotension|ftir|spectroscop|quantum|diamond|respiration|microsensor|proteomic|intracranial'),
        ('neurodegeneration',r'amyloid|aβ|alzheimer|senescence')]
PRECEDENCE=['meningioma','neurodegeneration','neural implants & interface','human tissue models','neurosurgery & diagnostics','neurotransmission & stimulation','spatial & single-cell','glioma microenvironment']
def topic(t):
    tl=t.lower(); hits=[n for n,rx in TOPICS if re.search(rx,tl)]
    for p in PRECEDENCE:
        if p in hits: return p
    return 'other'
items=[{'year':int(r['Year'] or 0),'kind':kind(r),'topic':topic(r['Title']),'title':r['Title'].strip(),'venue':r['Publication'].strip()} for r in rows]
json.dump(items,open('scripts/trajectory.json','w'),indent=1,ensure_ascii=False)
print(collections.Counter(i['kind'] for i in items))
un=[i for i in items if i['topic']=='other']
print(len(un),'unclassified'); [print(' ',i['year'],i['title'][:90]) for i in un]
