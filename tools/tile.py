"""Kullanım: python tools/tile.py <sayfa> <y0> <y1> <dpi> <satır> <sütun> [x0 x1]
Sayfanın [y0,y1] pt aralığını dpi'da satır x sütun parçaya böler (%8 bindirmeli) -> tmp/t<sayfa>_<r>_<c>.png (kâğıt fotoğrafı/yoğun sayfalar için)."""
import sys, pathlib, pymupdf
root = pathlib.Path(__file__).resolve().parent.parent; tmp = root/'tmp'; tmp.mkdir(exist_ok=True)
pg, y0, y1, dpi, R, C = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
x0, x1 = (float(sys.argv[7]), float(sys.argv[8])) if len(sys.argv) > 8 else (0, 612)
doc = pymupdf.open(root/'kaynak.pdf'); page = doc[pg-1]
h = (y1-y0)/R; w = (x1-x0)/C; ov = 0.08
for r in range(R):
    for c in range(C):
        rect = pymupdf.Rect(max(x0, x0+c*w-w*ov), max(y0, y0+r*h-h*ov), min(x1, x0+(c+1)*w+w*ov), min(y1, y0+(r+1)*h+h*ov))
        o = tmp/f't{pg}_{r+1}_{c+1}.png'; page.get_pixmap(dpi=dpi, clip=rect).save(o); print(o.name, f'y{rect.y0:.0f}-{rect.y1:.0f} x{rect.x0:.0f}-{rect.x1:.0f}')
