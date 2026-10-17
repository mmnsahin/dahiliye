"""Kullanım: python tools/kalin.py <p1> <p2> -> görünür metinde kalın (bold) satır başlarını yazar: sayfa y metin (sayfa boyutu pt)"""
import sys, pymupdf, pathlib
doc = pymupdf.open(pathlib.Path(__file__).resolve().parent.parent/'kaynak.pdf')
for p in range(int(sys.argv[1]), int(sys.argv[2])+1):
    pg = doc[p-1]; prev = None
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            bold = all((s['flags'] & 16) or 'Bold' in s['font'] or 'bold' in s['font'] for s in sp)
            y = round(l['bbox'][1], 1)
            t = ''.join(s['text'] for s in sp).strip()
            if bold and (prev is None or y-prev > 14): print(f"s{p} y{y} [{pg.rect.height:.0f}] {t[:100]}")
            prev = y if bold else None
