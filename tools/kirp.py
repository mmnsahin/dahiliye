"""Her kayıt bölgesini PDF'ten yüksek çözünürlükte (170 dpi, değiştirilmemiş) kırpar -> docs/img/<id>.webp
Kullanım: python3 tools/kirp.py kaynak.pdf [--ids N-1,N-2] [--dpi 170] ; var olan dosyaların üstüne yazmaz (--zorla ile yazar)."""
import json, subprocess, sys, pathlib, os, concurrent.futures as cf
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent
pdf = sys.argv[1]
dpi = 170
ids = None; zorla = '--zorla' in sys.argv
for i, a in enumerate(sys.argv):
    if a == '--dpi': dpi = int(sys.argv[i+1])
    if a == '--ids': ids = set(sys.argv[i+1].split(','))
S = dpi/72.0
tmp = root/'tmp_pages'; out = root/'docs/img'; tmp.mkdir(exist_ok=True); out.mkdir(parents=True, exist_ok=True)
recs = [r for r in json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))
        if (root/'data/okumalar'/f"{r['id']}.md").exists() and (ids is None or r['id'] in ids)]
recs = [r for r in recs if zorla or not (out/f"{r['id']}.webp").exists()]
pages = sorted({s['page'] for r in recs for s in r['segments']})
def render(p):
    f = tmp/f"p{p}.png"
    if not f.exists():
        subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(p),'-l',str(p),'-png','-singlefile',pdf,str(tmp/f"p{p}")],check=True)
    return p
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(render, pages))
def crop(r):
    parts = []
    for s in r['segments']:
        im = Image.open(tmp/f"p{s['page']}.png").convert('RGB')
        y0 = max(0, int(s['y0']*S)); y1 = min(im.height, int(s['y1']*S+1))
        if y1 <= y0: continue
        parts.append(im.crop((0, y0, im.width, y1)))
    if not parts: return r['id'], 0
    W = max(p.width for p in parts); H = sum(p.height for p in parts)
    canvas = Image.new('RGB', (W, H), 'white'); y = 0
    for p in parts: canvas.paste(p, (0, y)); y += p.height
    canvas.save(out/f"{r['id']}.webp", 'WEBP', quality=78, method=4)
    return r['id'], canvas.size
with cf.ThreadPoolExecutor(4) as ex: n = sum(1 for _ in ex.map(crop, recs))
print('kırpıldı:', n)
