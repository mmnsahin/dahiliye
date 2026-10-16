"""Kullanım: python tools/satirlar.py <p1> <p2>  -> GÖRÜNÜR (Tr3 olmayan) metnin paragraf başlarını y (pt) ile listeler; soru başlangıcı bulmaya yardımcı (görselle doğrulanmalı)."""
import sys, pathlib, pymupdf
sys.stdout.reconfigure(encoding='utf-8')
root = pathlib.Path(__file__).resolve().parent.parent
doc = pymupdf.open(root/'kaynak.pdf')
for p in range(int(sys.argv[1]), int(sys.argv[2])+1):
    pg = doc[p-1]; chars = []
    for sp in pg.get_texttrace():
        if sp['type'] == 3 or sp.get('opacity', 1) == 0: continue
        for c, org, gid, bb in sp['chars']:
            if c != 32: chars.append((bb, chr(c), sp.get('flags', 0), sp.get('font', '')))
    lines = []
    for bb, ch, fl, fn in sorted(chars, key=lambda t: ((t[0][1]+t[0][3])/2, t[0][0])):
        ym = (bb[1]+bb[3])/2
        if lines and abs(lines[-1][0]-ym) < 3: lines[-1][2].append((bb[0], bb[2], ch))
        else: lines.append([ym, bb[3]-bb[1], [(bb[0], bb[2], ch)], 'Bold' in fn or fn.endswith('-B')])
    prev = None; n = 0
    print(f'--- s{p}: görünür satır {len(lines)}')
    for ym, h, cs, bold in lines:
        cs.sort(); t = ''
        for k, (x0, x1, ch) in enumerate(cs):
            if k and x0-cs[k-1][1] > h*0.18: t += ' '
            t += ch
        if prev is None or ym-prev > h*1.6:
            print(f'  y{ym-h/2:.0f}{" B" if bold else ""}: {t[:85]}')
        prev = ym
