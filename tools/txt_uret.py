"""data/okumalar + data/kumeler.txt -> dahiliye_okumalar.txt (tüm okumalar, konu ve küme başlığıyla)."""
import re, glob, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
kon = {}; cur = None
for l in (root/'data/kumeler.txt').read_text(encoding='utf-8').splitlines():
    if l.startswith('## '): cur = re.match(r'## (.+?)\s*\[', l).group(1)
    elif l.startswith('- '):
        t, ids = l[2:].split(' :: ')
        for i in ids.split(','): kon[i.strip()] = (cur, t.strip())
order = {'N':0,'G':1,'R':2,'H':3,'E':4,'O':5,'I':6}
def key(f):
    m = re.match(r'([A-Z])-(\d+)([ab]?)', f.stem); return (order.get(m.group(1), 9), int(m.group(2)), m.group(3))
out = ['DAHİLİYE SÖZLÜ ÇIKMIŞ SORULAR – OKUMALAR', 'Etiketler: [DAKTİLO] metin katmanı, [SLAYT] slayt/görsel, [EL YAZISI] el yazısı (okunan), [OKUNAMADI], [?] okuması şüpheli.', '='*78, '']
n = 0
for f in sorted((root/'data/okumalar').glob('*.md'), key=key):
    t = f.read_text(encoding='utf-8')
    m = re.match(r'---\n(.*?)\n---\n## Soru\n(.*?)\n## Cevap\n?(.*)', t, re.S)
    fm = dict(l.split(': ', 1) for l in m.group(1).split('\n') if ': ' in l)
    konu, kume = kon.get(fm['id'], ('?', '?')); n += 1
    out += [f"[{fm['id']}] Ders: {fm['konu']} | Konu: {konu} | Küme: {kume}",
            f"Hoca: {fm.get('hoca','—')} | Sayfa: {fm.get('sayfa','')} | Orijinal no: {fm.get('orijinal_no','null')}",
            'SORU:', m.group(2).strip(), 'CEVAP:', m.group(3).strip() or '(cevap yok)', '', '-'*78, '']
(root/'dahiliye_okumalar.txt').write_text('\n'.join(out), encoding='utf-8')
print(n, 'kayıt yazıldı')
