"""Kullanım: python tools/dogrula.py [önek]  -> bolgeler.json geçerli mi; her kayıt için okuma dosyası var mı; front-matter ve ## Soru/## Cevap tamam mı; [?]/[OKUNAMADI] sayıları."""
import sys, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
E = json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))
pre = sys.argv[1] if len(sys.argv) > 1 else ''
miss = []; bad = []; q = o = n = 0
for e in E:
    if not e['id'].startswith(pre): continue
    p = root/f"data/okumalar/{e['id']}.md"
    if not p.exists(): miss.append(e['id']); continue
    t = p.read_text(encoding='utf-8'); n += 1
    if not re.match(r"---\nid: %s\nkonu: .+\nhoca: .+\nsayfa: .+\norijinal_no: .+\n---\n## Soru\n" % re.escape(e['id']), t) or t.count('## Cevap\n') != 1 or t.count('## Soru\n') != 1:
        bad.append(e['id'])
    q += t.count('[?]'); o += t.count('[OKUNAMADI]')
print(f'json geçerli, {len(E)} kayıt; okuması olan {n}; eksik {miss[:15]}{"..." if len(miss)>15 else ""} ({len(miss)}); bozuk {bad}; [?]={q} [OKUNAMADI]={o}')
