"""Kullanım: python tools/yaz_daktilo.py <id>...  -> tmp/tl_<id>.txt (textlayer.py çıktısı) + bolgeler.json'dan data/okumalar/<id>.md iskeleti.
Yalnızca saf DAKTİLO bölgeler için; görselle doğrulandıktan sonra kullanılır."""
import sys, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
E = {e['id']: e for e in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))}
(root/'data/okumalar').mkdir(exist_ok=True)
for rid in sys.argv[1:]:
    e = E[rid]; lines = (root/f'tmp/tl_{rid}.txt').read_text(encoding='utf-8').split('\n')
    i = lines.index('## Cevap'); q, a = lines[1:i], lines[i+1:]
    a = ['[DAKTİLO] '+l for l in a] or ['(cevap yok)']
    p0, p1 = e['pages']; sayfa = str(p0) if p0 == p1 else f'{p0}-{p1}'
    on = e.get('orijinal_no')
    md = ['---', f"id: {rid}", f"konu: {e['konu']}", f"hoca: {e.get('hoca') or '—'}", f'sayfa: {sayfa}',
          f"orijinal_no: {on if on is not None else 'null'}", '---', '## Soru', *q, '## Cevap', *a, '']
    (root/f'data/okumalar/{rid}.md').write_text('\n'.join(md), encoding='utf-8')
    print(rid, 'yazıldı')
