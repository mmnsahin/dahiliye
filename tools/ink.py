"""Kullanım: python tools/ink.py <önek> <n1> <n2> -> bölgelerde vektör çizim (el yazısı/çizgi) yoğunluğu: id sayfa:çizim_sayısı"""
import sys, json, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent
E = {e['id']: e for e in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))}
doc = pymupdf.open(root/'kaynak.pdf'); cache = {}
pre, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for i in range(a, b+1):
    k = f'{pre}-{i}'
    if k not in E: continue
    tot = []
    for s in E[k]['segments']:
        if s['page'] not in cache: cache[s['page']] = doc[s['page']-1].get_drawings()
        n = 0
        for d in cache[s['page']]:
            r = d['rect']
            if r.y1 > s['y0'] and r.y0 < s['y1'] and d.get('type') in ('s','fs','f') and r.width < 400:
                col = d.get('color') or d.get('fill')
                if col and any(abs(c - col[0]) > 0.15 for c in col): n += 1   # renkli
                elif d.get('type') == 's': n += 1
        tot.append(f"{s['page']}:{n}")
    print(k, ' '.join(tot))
