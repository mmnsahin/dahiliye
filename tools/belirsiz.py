"""Kullanım: python tools/belirsiz.py -> data/emin_degil.md üretir: okumalarda [?] ve [OKUNAMADI] geçen her yer (id, sayfa, bağlam). Elle kontrol için."""
import re, pathlib, glob
root = pathlib.Path(__file__).resolve().parent.parent
out = ["# Emin olunamayan yerler (el yazısı/slayt)", "", "Her satır: `id (sayfa)` — işaret — bağlam. İşaretler: `[?]` tahmin/şüpheli okuma, `[OKUNAMADI]` okunamadı. Kontrol edince satırı silebilir ya da okumalar/<id>.md içinde düzeltebilirsin. Dosya `python tools/belirsiz.py` ile yeniden üretilir.", ""]
n = 0
def key(p):
    m = re.match(r'([A-Z])-(\d+)', pathlib.Path(p).stem); return ('NGRHEOI'.find(m.group(1)), int(m.group(2)))
for f in sorted(glob.glob(str(root/'data/okumalar/*.md')), key=key):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    sayfa = re.search(r'^sayfa: (.*)$', t, re.M).group(1)
    for m in re.finditer(r'\[\?\]|\[OKUNAMADI[^\]]*\]', t):
        a = max(0, m.start()-60); b = min(len(t), m.end()+40)
        ctx = t[a:b].replace('\n', ' ')
        out.append(f"- **{pathlib.Path(f).stem}** (s.{sayfa}) {m.group(0)[:14]} — …{ctx}…"); n += 1
(root/'data/emin_degil.md').write_text('\n'.join(out)+'\n', encoding='utf-8')
print(n, 'madde')
