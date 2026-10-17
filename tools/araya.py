"""Kullanım: python tools/araya.py <yeni_id> <sayfa> <y> "<soru metni>" [orijinal_no]
Mevcut bir kaydın içine yeni bir soru başlangıcı ekler: önceki kaydın bitişi ve yeni kaydın segmentleri yeniden hesaplanır.
Yeni id geçicidir (ör. E-9001); işlem sonunda `python tools/renumber.py E` ile (sayfa,y) sırasına göre yeniden numaralanır."""
import sys, json, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent
P = root/'data/bolgeler.json'; H = 866.7
nid, page, y, text = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
onr = sys.argv[5] if len(sys.argv) > 5 else None
E = json.loads(P.read_text(encoding='utf-8')); doc = pymupdf.open(root/'kaynak.pdf')
pre = nid.split('-')[0]
konu = {'N': 'Nefroloji', 'G': 'Gastroenteroloji', 'R': 'Romatoloji', 'H': 'Hematoloji', 'E': 'Endokrinoloji', 'O': 'Onkoloji', 'I': 'İmmünoloji-Alerji'}
sec = sorted([e for e in E if e['id'].split('-')[0] == pre and e['id'] != nid], key=lambda e: (e['page'], e['y']))
prev = [e for e in sec if (e['page'], e['y']) < (page, y)][-1]
nxt = [e for e in sec if (e['page'], e['y']) > (page, y)]
nxt = nxt[0] if nxt else None
end_of_prev = prev['end']
def height(pg): return round(doc[pg-1].rect.height, 1) if pg >= 368 else H
def segs(p0, y0, p1, y1):
    out = []
    for pg in range(p0, p1+1):
        a = max(y0-3.9, 0) if pg == p0 else 0.0
        b = max(y1-3.9, a) if pg == p1 else height(pg)
        if pg == p1 and p1 > p0 and y1 <= 5: continue
        out.append({'page': pg, 'y0': round(a, 1), 'y1': round(b, 1)})
    return out
prev['end'] = {'page': page, 'y': y}; prev['segments'] = segs(prev['page'], prev['y'], page, y); prev['pages'] = [prev['page'], prev['segments'][-1]['page']]
ep, ey = (end_of_prev['page'], end_of_prev['y'])
sg = segs(page, y, ep, ey)
rec = {'no': 0, 'page': page, 'y': y, 'dup': 1, 'seq': 0, 'text': text, 'text_src': 'D', 'hoca': '—', 'end': {'page': ep, 'y': ey}, 'segments': sg,
       'pages': [page, sg[-1]['page']], 'start_src': 'DAKTİLO', 'konu': konu[pre], 'id': nid, 'orijinal_no': onr}
E = [e for e in E if e['id'] != nid]; E.append(rec)
P.write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding='utf-8')
print('eklendi', nid, page, y, 'önceki:', prev['id'], '->', prev['end'], '| yeni bitiş:', rec['end'])
