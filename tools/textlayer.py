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
        # SADECE görünür metin: get_texttrace type 3 = render mode 3 (görünmez/gizli OCR) -> atlanır
        chars = []
        for sp in pg.get_texttrace():
            if sp['type'] == 3 or sp.get('opacity', 1) == 0: continue
            for c, org, gid, bb in sp['chars']:
                if c != 32 and s['y0'] <= (bb[1]+bb[3])/2 < s['y1']: chars.append((bb, chr(c)))
        lines = []  # (ymid, h, [(x0, ch)])
        for bb, ch in sorted(chars, key=lambda t: ((t[0][1]+t[0][3])/2, t[0][0])):
            ym = (bb[1]+bb[3])/2
            if lines and abs(lines[-1][0]-ym) < 3: lines[-1][2].append((bb[0], bb[2], ch))
            else: lines.append([ym, bb[3]-bb[1], [(bb[0], bb[2], ch)]])
        prev = None; cur = []
        for ym, h, cs in lines:
            cs.sort(); t = ''
            for k, (x0, x1, ch) in enumerate(cs):
                if k and x0 - cs[k-1][1] > h*0.18: t += ' '
                t += ch
            if prev is not None and ym - prev > h*1.6 and cur:
                paras.append((s['page'], cur[0], ' '.join(cur[1:]))); cur = []
            if not cur: cur = [ym - h/2]
            cur.append(t); prev = ym
        if cur: paras.append((s['page'], cur[0], ' '.join(cur[1:])))
    paras.sort(key=lambda p: (p[0], p[1]))
    q = norm(e['text']); acc = ''; i = 0
    while i < len(paras) and len(acc) < len(q)*0.9:
        acc += norm(paras[i][2]); i += 1
    out = ['## Soru'] + ['[DAKTİLO] '+p[2] if k == 0 else p[2] for k, p in enumerate(paras[:i])] + ['## Cevap'] + [p[2] for p in paras[i:]]
    (tmp/f'tl_{rid}.txt').write_text('\n'.join(out), encoding='utf-8')
    import json as _j
    (tmp/f'ty_{rid}.json').write_text(_j.dumps([{'p':a,'y':b,'t':c} for a,b,c in paras[i:]], ensure_ascii=False), encoding='utf-8')
    print(rid, len(paras), 'blok; soru blok:', i)
