"""Kullanım: python tools/renumber.py <ön ek, örn. R> -> bolgeler.json'daki o ön ekli kayıtları (page,y) sırasına göre ön ek-1.. yeniden numaralar; okumalar dosyalarını ve front-matter id'sini günceller."""
import sys, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
pre = sys.argv[1]; P = root/'data/bolgeler.json'
E = json.loads(P.read_text(encoding='utf-8'))
mine = sorted([e for e in E if e['id'].startswith(pre+'-')], key=lambda e: (e['page'], e['y']))
mp = {e['id']: f'{pre}-{i+1}' for i, e in enumerate(mine)}
d = root/'data/okumalar'; tmpd = {}
for old, new in mp.items():
    f = d/f'{old}.md'
    if f.exists(): tmpd[new] = f.read_text(encoding='utf-8'); f.unlink()
for new, txt in tmpd.items():
    old = [o for o, n in mp.items() if n == new][0]
    txt = re.sub(r'^id: .*$', f'id: {new}', txt, count=1, flags=re.M)
    (d/f'{new}.md').write_text(txt, encoding='utf-8')
for i, e in enumerate(mine):
    e['id'] = mp[e['id']]; e['no'] = i+1; e['seq'] = i+1
rest = [e for e in E if not e['id'].startswith(pre+'-') or e in mine]
# aynı sırayı koru: ön ek kayıtlarını (page,y) sırasına koy
others = [e for e in E if e not in mine]
P.write_text(json.dumps(others + mine, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(mine), 'kayıt yeniden numaralandı; değişen:', sum(1 for o, n in mp.items() if o != n))
