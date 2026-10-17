"""Kullanım: python tools/ekle.py <spec.json> [--son sayfa y]
spec.json: [{"id":"G-1","orijinal_no":"2","hoca":"—","page":95,"y":77.4,"text_src":"D","text":"..."(ops.)}, ...] yazılış sırasıyla.
Her kaydın bitişi bir sonrakinin başlangıcı; son kaydın bitişi --son (varsayılan: o sayfanın sonu). Segmentler: ilk sayfada y-3.9'dan, sonraki sayfalarda 0'dan; bitiş sayfasında y-3.9'a kadar.
bolgeler.json'a ekler (aynı id varsa değiştirir). 'text' verilmezse görünür metin katmanındaki ilk paragraf alınır."""
import sys, json, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent
P = root/'data/bolgeler.json'; H = 866.7
spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
son = (spec[-1]['page'], H)
if '--son' in sys.argv: i = sys.argv.index('--son'); son = (int(sys.argv[i+1]), float(sys.argv[i+2]))
E = json.loads(P.read_text(encoding='utf-8')); doc = pymupdf.open(root/'kaynak.pdf')
konu = {'N': 'Nefroloji', 'G': 'Gastroenteroloji', 'R': 'Romatoloji', 'H': 'Hematoloji', 'E': 'Endokrinoloji', 'O': 'Onkoloji', 'I': 'İmmünoloji-Alerji'}
def vis_text(page, y):
    pg = doc[page-1]; chars = []
    for sp in pg.get_texttrace():
        if sp['type'] == 3 or sp.get('opacity', 1) == 0: continue
        for c, org, gid, bb in sp['chars']:
            if c != 32 and (bb[1]+bb[3])/2 >= y-1: chars.append((bb, chr(c)))
    lines = []
    for bb, ch in sorted(chars, key=lambda t: ((t[0][1]+t[0][3])/2, t[0][0])):
        ym = (bb[1]+bb[3])/2
        if lines and abs(lines[-1][0]-ym) < 3: lines[-1][2].append((bb[0], bb[2], ch))
        else: lines.append([ym, bb[3]-bb[1], [(bb[0], bb[2], ch)]])
    out = []; prev = None
    for ym, h, cs in lines:
        cs.sort(); t = ''
        for k, (x0, x1, ch) in enumerate(cs):
            if k and x0-cs[k-1][1] > h*0.18: t += ' '
            t += ch
        if prev is not None and ym-prev > h*1.6: break
        out.append(t); prev = ym
    return ' '.join(out)
ids = {e['id']: i for i, e in enumerate(E)}
for k, s in enumerate(spec):
    nxt = (spec[k+1]['page'], spec[k+1]['y']) if k+1 < len(spec) else son
    p0, y0 = s['page'], s['y']; p1, y1 = nxt
    segs = []
    for pg in range(p0, p1+1):
        a = max(y0-3.9, 0) if pg == p0 else 0.0
        b = max(y1-3.9, a) if pg == p1 else H
        if pg == p1 and p1 > p0 and y1 <= 5: continue
        segs.append({'page': pg, 'y0': round(a, 1), 'y1': round(b, 1)})
    pre = s['id'].split('-')[0]; no = int(''.join(c for c in s['id'].split('-')[1] if c.isdigit()))
    text = s.get('text') or vis_text(p0, y0)
    rec = {'no': no, 'page': p0, 'y': y0, 'dup': 1, 'seq': no, 'text': text, 'text_src': s.get('text_src', 'D'),
           'hoca': s.get('hoca', '—'), 'end': {'page': p1, 'y': y1}, 'segments': segs, 'pages': [p0, segs[-1]['page']],
           'start_src': s.get('start_src', 'DAKTİLO'), 'konu': konu[pre], 'id': s['id'], 'orijinal_no': s.get('orijinal_no')}
    if s['id'] in ids: E[ids[s['id']]] = rec
    else: E.append(rec); ids[s['id']] = len(E)-1
P.write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(spec), 'kayıt eklendi/güncellendi; toplam', len(E))
