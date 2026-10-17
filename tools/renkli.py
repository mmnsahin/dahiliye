"""Kullanım: python tools/renkli.py <p1> <p2> -> görünür metinde siyah olmayan renkli satırlar (soru başlığı ipucu): sayfa y renk metin"""
import sys, pymupdf
doc = pymupdf.open(__import__('pathlib').Path(__file__).resolve().parent.parent/'kaynak.pdf')
for p in range(int(sys.argv[1]), int(sys.argv[2])+1):
    pg = doc[p-1]; rows = {}
    for sp in pg.get_texttrace():
        if sp['type'] == 3 or sp.get('opacity', 1) == 0: continue
        col = sp['color']
        if isinstance(col, (tuple, list)): c = tuple(round(x, 1) for x in col)
        else: c = (round(((col>>16)&255)/255,1), round(((col>>8)&255)/255,1), round((col&255)/255,1)) if isinstance(col,int) else col
        for ch in sp['chars']:
            y = round((ch[3][1]+ch[3][3])/2/3)*3
            rows.setdefault((y, c), []).append((ch[3][0], chr(ch[0])))
    for (y, c), cs in sorted(rows.items()):
        if c in ((0.0,0.0,0.0), (0,0,0), 0): continue
        cs.sort(); print(f"s{p} y{y} {c} {''.join(x[1] for x in cs)[:90]}")
