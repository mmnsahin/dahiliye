"""Kullanım: python tools/imgs.py <id>... -> bölge segmentlerindeki görsellerin (y0-y1, x0-x1) listesi; yazı katmanı dışı içerik nerede?"""
import sys, json, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent
E = {e['id']: e for e in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))}
doc = pymupdf.open(root/'kaynak.pdf')
for rid in sys.argv[1:]:
    e = E[rid]; out = []
    for s in e['segments']:
        for im in doc[s['page']-1].get_image_info():
            x0, y0, x1, y1 = im['bbox']
            if y1 > s['y0'] and y0 < s['y1'] and (y1-y0) > 25 and (x1-x0) > 25:
                out.append(f"s{s['page']} y{max(y0,s['y0']):.0f}-{min(y1,s['y1']):.0f} x{x0:.0f}-{x1:.0f}")
    print(rid, '|', '; '.join(out) if out else 'görsel yok')
