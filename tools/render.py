"""Kullanım:
  python3 tools/render.py page <sayfa> [dpi=110] [--grid]   -> tmp/p<sayfa>.png (--grid: her 50 pt'de cetvel çizgisi, y değerleri pt cinsinden)
  python3 tools/render.py region <kayıt-id> [dpi=160]       -> tmp/<id>_<sayfa>.png (bolgeler.json'daki segmentler, kesilmiş)
Kaynak PDF: kaynak.pdf (repo kökü)."""
import sys, json, subprocess, pathlib
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent
tmp = root/'tmp'; tmp.mkdir(exist_ok=True)
pdf = str(root/'kaynak.pdf')
def render(p, dpi):
    out = tmp/f'_r{p}'
    subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(p),'-l',str(p),'-png',pdf,str(out)],check=True)
    f = next(tmp.glob(f'_r{p}-*.png')); im = Image.open(f).convert('RGB'); f.unlink(); return im
mode = sys.argv[1]
if mode == 'page':
    p = int(sys.argv[2]); dpi = int(next((a for a in sys.argv[3:] if a.isdigit()), 110))
    im = render(p, dpi)
    if '--grid' in sys.argv:
        d = ImageDraw.Draw(im); s = dpi/72
        for y in range(0, int(im.height/s)+1, 50):
            d.line([(0,y*s),(im.width,y*s)], fill=(255,0,0), width=1); d.text((3,y*s+1), f'y={y}', fill=(255,0,0))
    im.save(tmp/f'p{p}.png'); print(tmp/f'p{p}.png', im.size)
else:
    rid = sys.argv[2]; dpi = int(sys.argv[3]) if len(sys.argv)>3 else 160
    E = json.loads((root/'data/bolgeler.json').read_text(encoding='utf-8'))
    e = next(x for x in E if x['id']==rid)
    for s in e['segments']:
        im = render(s['page'], dpi); k = dpi/72
        im = im.crop((0,int(s['y0']*k),im.width,min(im.height,int(s['y1']*k))))
        o = tmp/f"{rid}_{s['page']}.png"; im.save(o); print(o, im.size)
