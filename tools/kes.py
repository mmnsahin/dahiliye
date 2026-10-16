"""Kullanım: python tools/kes.py <png> <parça sayısı> -> tmp/<ad>_k1.png ... (üst üste biner, yüksek dpi bölgelerde okumak için)"""
import sys, pathlib
from PIL import Image
f = pathlib.Path(sys.argv[1]); n = int(sys.argv[2]); im = Image.open(f); h = im.height; step = h/n
for i in range(n):
    y0 = max(0, int(i*step-40)); y1 = min(h, int((i+1)*step+40))
    o = f.with_name(f'{f.stem}_k{i+1}.png'); im.crop((0, y0, im.width, y1)).save(o); print(o, im.size[0], y1-y0)
