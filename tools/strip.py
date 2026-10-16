"""Kullanım: python tools/strip.py <sayfa1> <sayfa2> ... [--dpi 60] -> tmp/strip.png (yan yana önizleme)"""
import sys, pathlib, pymupdf
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent; tmp = root/'tmp'
dpi = 60; pgs = []
a = sys.argv[1:]; i = 0
while i < len(a):
    if a[i] == '--dpi': dpi = int(a[i+1]); i += 2
    else: pgs.append(int(a[i])); i += 1
doc = pymupdf.open(root/'kaynak.pdf'); ims = []
for p in pgs:
    px = doc[p-1].get_pixmap(dpi=dpi); ims.append(Image.frombytes('RGB', (px.width, px.height), px.samples))
c = Image.new('RGB', (sum(i.width for i in ims), max(i.height for i in ims)), 'white'); x = 0
for im in ims: c.paste(im, (x, 0)); x += im.width
c.save(tmp/'strip.png'); print(c.size)
