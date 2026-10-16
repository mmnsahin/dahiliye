"""Ortak yazıcı: python içinden `from yaz import *` (exec ile). tl(id): textlayer cevap satırları; w(...): okuma dosyası yazar; D(lines, ekler): DAKTİLO satırlarını ekleri araya koyarak birleştirir."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
E = {e['id']: e for e in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))}
def rt(i):
    return (root/f'tmp/tl_N-{i}.txt' if not str(i).startswith(('G','R','H','E','O','I','N')) else root/f'tmp/tl_{i}.txt')
def _read(i):
    i = str(i); p = root/f'tmp/tl_{i}.txt' if i[:2] in ('N-','G-','R-','H-','E-','O-','I-') else root/f'tmp/tl_N-{i}.txt'
    return p.read_text(encoding='utf-8').replace('ﬂ', 'fl').replace('', '•').replace('', 'Ø').replace('', '▪')
def tlq(i): return _read(i).split('## Cevap')[0].split('\n', 1)[1].strip()
def tl(i):
    t = _read(i)
    sep = '## Cevap' + chr(10)
    return [l for l in t.split(sep, 1)[1].split(chr(10)) if l.strip()] if sep in t else []
def D(lines, ek=None):
    """ek: {satır_başı_öneki: eklenecek_metin} -> o satırdan SONRA eklenir; None anahtarı başa eklenir."""
    out = []; ek = ek or {}
    if None in ek: out.append(ek[None])
    for l in lines:
        out.append('[DAKTİLO] ' + l)
        for k, v in ek.items():
            if k is not None and l.startswith(k): out.append(v)
    return '\n'.join(out)
def w(i, cevap, soru=None, hoca=None, sayfa=None, onr='null'):
    e = E[f'N-{i}'] if f'N-{i}' in E else E[i]; rid = e['id']
    h = hoca if hoca is not None else (e.get('hoca') or '—')
    p0, p1 = e['pages']; sy = sayfa or (str(p0) if p0 == p1 else f'{p0}-{p1}')
    s = soru if soru is not None else tlq(rid)
    (root/f'data/okumalar/{rid}.md').write_text(f"---\nid: {rid}\nkonu: {e['konu']}\nhoca: {h}\nsayfa: {sy}\norijinal_no: {onr}\n---\n## Soru\n{s}\n## Cevap\n{cevap.strip() or '(cevap yok)'}\n", encoding='utf-8')
