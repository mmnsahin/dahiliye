"""data/ -> site/index.html. Kullanım: python3 build_site.py [--todo]
Girdi: data/okumalar/*.md (kayıt okumaları), data/kumeler.txt (konu/küme), data/birlesik/<küme_id>.md (birleşik cevaplar; küme_id = kümenin ilk kayıt id'si).
Çıktı: docs/index.html (metin gömülü; sayfa görüntüleri docs/img/<id>.webp olarak yanında; GitHub Pages: main /docs)."""
import re, json, pathlib, sys, collections
root = pathlib.Path(__file__).parent
rows = {}
for f in sorted((root/'data/okumalar').glob('*.md')):
    t = f.read_text(encoding='utf-8')
    m = re.match(r'---\n(.*?)\n---\n## Soru\n(.*?)\n## Cevap\n?(.*)', t, re.S)
    if not m: print('okunamadı:', f.name); sys.exit(1)
    fm = dict(l.split(': ', 1) for l in m.group(1).split('\n') if ': ' in l)
    rows[fm['id']] = {'id': fm['id'], 'ders': fm.get('konu', ''), 'hoca': fm.get('hoca', '—'), 'sayfa': fm.get('sayfa', ''),
                      'no': None if fm.get('orijinal_no', 'null') in ('null', '') else fm['orijinal_no'],
                      'q': m.group(2).strip(), 'a': m.group(3).strip()}
konular, cur, errors, seen = [], None, [], collections.Counter()
for line in (root/'data/kumeler.txt').read_text(encoding='utf-8').splitlines():
    if line.startswith('## '):
        mm = re.match(r'## (.+?)\s*\[(.+?)\]\s*$', line)
        cur = {'id': 't%02d' % (len(konular)+1), 'title': mm.group(1), 'ders': mm.group(2), 'clusters': []}; konular.append(cur)
    elif line.startswith('- '):
        title, ids = line[2:].split(' :: ')
        ids = [x.strip() for x in ids.split(',')]
        for i in ids:
            seen[i] += 1
            if i not in rows: errors.append(f'{title}: bilinmeyen kayıt {i}')
        cur['clusters'].append({'id': 'c-' + ids[0], 'title': title.strip(), 'rows': ids, 'merged': None})
for i in rows:
    if seen[i] != 1: errors.append(f'{i}: {seen[i]} kümede (1 olmalı)')
mdir = root/'data/birlesik'; allc = {c['id']: c for k in konular for c in k['clusters']}
SRC = re.compile(r'\[([A-Z](?:\s*,\s*[A-Z])*)(?:\s*[·,]\s*el yazısı)?\]')
done = multi = 0
for cid, c in allc.items():
    f = mdir/f'{cid}.md'
    if len(set(re.sub(r'^(N-\d+)[ab]$', r'\1', r) for r in c['rows'])) > 1: multi += 1
    if f.exists():
        txt = f.read_text(encoding='utf-8').strip(); allowed = {chr(65+i) for i in range(len(c['rows']))}
        for grp in SRC.findall(txt):
            bad = set(re.split(r'\s*,\s*', grp)) - allowed
            if bad: errors.append(f'{cid}: kaynak harfi yok {sorted(bad)} (izinli {"".join(sorted(allowed))})')
        c['merged'] = txt; done += 1
adir = root/'data/ai'
if adir.exists():
    for f in adir.glob('*.md'):
        if f.stem in allc: allc[f.stem]['ai'] = f.read_text(encoding='utf-8').strip()
        else: errors.append(f'data/ai/{f.name}: böyle bir küme yok')
if mdir.exists():
    for f in mdir.glob('*.md'):
        if f.stem not in allc: errors.append(f'data/birlesik/{f.name}: böyle bir küme yok')
if '--todo' in sys.argv:
    for cid, c in allc.items():
        n = len(set(re.sub(r'^(N-\d+)[ab]$', r'\1', r) for r in c['rows']))
        if n > 1 and not c['merged']: print(f'{cid:<10} {n}x  {c["title"]}  {c["rows"]}')
    sys.exit(0)
if errors: print('\n'.join(errors)); sys.exit(1)
konular = [k for k in konular if k['clusters']]
data = json.dumps({'konular': konular, 'rows': rows}, ensure_ascii=False).replace('</', '<\\/')
html = (root/'site/template.html').read_text(encoding='utf-8').replace('__DATA__', data)
(root/'docs').mkdir(exist_ok=True); (root/'docs/index.html').write_text(html, encoding='utf-8'); (root/'docs/.nojekyll').write_text('')
print(f"docs/index.html yazıldı: {len(rows)} kayıt, {sum(len(k['clusters']) for k in konular)} küme, {len(konular)} konu; birleşik cevap {done}/{multi} çok kaynaklı küme.")
