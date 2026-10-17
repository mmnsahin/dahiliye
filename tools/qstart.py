"""Kullanım: python tools/qstart.py <p1> <p2> -> görünür metinde mavi/mor (soru rengi) veya 'N)' numaralı satırların paragraf başları: sayfa y renk metin"""
import sys, re, pymupdf, pathlib
doc = pymupdf.open(pathlib.Path(__file__).resolve().parent.parent/'kaynak.pdf')
QC = {(0.0,0.1,0.4),(0.4,0.2,0.6),(0.2,0.5,0.7),(0.0,0.4,0.8),(0.1,0.2,0.4)}
for p in range(int(sys.argv[1]), int(sys.argv[2])+1):
    pg = doc[p-1]; rows = {}
    for sp in pg.get_texttrace():
        if sp['type']==3 or sp.get('opacity',1)==0: continue
        col = sp['color']
        c = tuple(round(x,1) for x in col) if isinstance(col,(tuple,list)) else (round(((col>>16)&255)/255,1),round(((col>>8)&255)/255,1),round((col&255)/255,1))
        for ch in sp['chars']:
            y = round((ch[3][1]+ch[3][3])/2/3)*3
            rows.setdefault(y, []).append((ch[3][0], chr(ch[0]), c))
    prev = None
    for y in sorted(rows):
        cs = sorted(rows[y]); t = ''.join(x[1] for x in cs).strip()
        if len(t) < 8: continue
        cols = {x[2] for x in cs if x[1].strip()}
        isq = bool(cols & QC) or re.match(r'^\(?\d{1,3}\s*[\)\.\-:]', t)
        if isq and (prev is None or y-prev > 22): print(f"s{p} y{y} {''.join(x[1] for x in cs)[:110]}")
        prev = y if isq else None
