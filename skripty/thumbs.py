import pymupdf, pathlib
root = pathlib.Path('.')
out = root / 'prehlad-img'
out.mkdir(exist_ok=True)
n = 0
for p in sorted(root.glob('KECY znacky/**/*.pdf')) + sorted(root.glob('KECY mapy/*.pdf')):
    d = pymupdf.open(p)
    pg = d[0]
    r = pg.rect
    z = 700 / max(r.width, r.height)
    name = p.relative_to(root).as_posix().replace('/', '__').replace(' ', '_')[:-4] + '.png'
    pg.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(out / name)
    n += 1
    if n < 4 or len(d) > 1:
        print(ascii(name), round(r.width), round(r.height), len(d))
print(n)
