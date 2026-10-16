"""Kullanım: python tools/textlayer.py <id> [<id>...]  -> bölgenin GÖRÜNÜR metin katmanını (UTF-8) tmp/tl_<id>.txt'ye yazar.
Soru metni (bolgeler.json 'text') ile cevabı '## Soru' / '## Cevap' diye ayırır. İskelet; görselle doğrulanmalıdır."""
import sys, json, re, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent
tmp = root/'tmp'; tmp.mkdir(exist_ok=True)
E = {e['id']: e for e in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))}
norm = lambda s: re.sub(r'\W+', '', s).lower()
doc = pymupdf.open(root/'kaynak.pdf')
for rid in sys.argv[1:]:
    e = E[rid]; paras = []
    for s in e['segments']:
        pg = doc[s['page']-1]
        for b in pg.get_text('blocks'):
            x0, y0, x1, y1, t = b[:5]
            if b[6] != 0 or not t.strip(): continue
            ym = (y0+y1)/2
            if s['y0'] <= ym < s['y1']:
                paras.append((s['page'], y0, ' '.join(t.split())))
    paras.sort(key=lambda p: (p[0], p[1]))
    q = norm(e['text']); acc = ''; i = 0
    while i < len(paras) and len(acc) < len(q)*0.9:
        acc += norm(paras[i][2]); i += 1
    out = ['## Soru'] + ['[DAKTİLO] '+p[2] if k == 0 else p[2] for k, p in enumerate(paras[:i])] + ['## Cevap'] + [p[2] for p in paras[i:]]
    (tmp/f'tl_{rid}.txt').write_text('\n'.join(out), encoding='utf-8')
    print(rid, len(paras), 'blok; soru blok:', i)
