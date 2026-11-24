"""Bersihkan export Roboflow test set custom -> test_custom_clean.json (file asli tidak diubah).

Langkah (semua tercatat di laporan):
1. buang kelas permukaan (dinding/lantai/plafon) + kelas di luar dataset asli -> dikecualikan dari evaluasi
2. buang serpihan mask < 0.01% luas foto (sisa auto-label)
3. gabungkan potongan satu objek yang terbelah oklusi menjadi satu instance (daftar MERGE, dicek visual)
4. hapus label salah yang sudah dicek visual (daftar REMOVE)

Opsi --keep-surface (untuk ANALISIS SENSITIVITAS, bukan hasil utama): kelas permukaan TIDAK dibuang,
dan 'ceiling' (nama dari Roboflow) diganti 'ceiling-merged' agar sama dengan nama kelas dataset asli.
  python3 clean_custom.py _annotations.coco.json test_custom_surface_clean.json --keep-surface
"""
import json, re, sys, collections

args = [a for a in sys.argv[1:] if not a.startswith('--')]
KEEP_SURFACE = '--keep-surface' in sys.argv
SRC = args[0] if len(args) > 0 else '_annotations.coco.json'
DST = args[1] if len(args) > 1 else 'test_custom_clean.json'
RENAME = {'ceiling': 'ceiling-merged'} if KEEP_SURFACE else {}

SURFACE = {'wall', 'wall-brick', 'wall-other-merged', 'wall-stone', 'wall-tile', 'wall-wood',
           'floor-other-merged', 'floor-wood', 'ceiling-merged', 'ceiling', 'st-'}
NOT_IN_DATASET = {'cat'}
MIN_AREA_FRAC = 1e-4
MERGE = {('IMG_8804', 'dining table'), ('F08214DF-EE44-4F71-88CD-48E9212A07E6', 'table-merged'),
         ('1A205BFE-355B-4727-B360-BC5F92EF089F', 'table-merged')}
REMOVE = {('IMG_1651', 'bed')}   # matras di lantai, bukan kasur

d = json.load(open(SRC))
for c in d['categories']:
    c['name'] = RENAME.get(c['name'], c['name'])
if KEEP_SURFACE: SURFACE = set()
cats = {c['id']: c['name'] for c in d['categories']}
stem = {i['id']: re.sub(r'_jpg\.rf\..*', '', i['file_name']) for i in d['images']}
area = {i['id']: i['width'] * i['height'] for i in d['images']}
log = collections.Counter()

keep, groups = [], collections.defaultdict(list)
for a in d['annotations']:
    name, key = cats[a['category_id']], (stem[a['image_id']], cats[a['category_id']])
    segs = [s for s in a.get('segmentation') or [] if len(s) >= 6]
    if name in SURFACE: log['kelas permukaan'] += 1; continue
    if name in NOT_IN_DATASET: log['kelas di luar dataset'] += 1; continue
    if not segs: log['tanpa polygon valid'] += 1; continue
    if a['area'] / area[a['image_id']] < MIN_AREA_FRAC: log['serpihan kecil'] += 1; continue
    if key in REMOVE: log['label salah (REMOVE)'] += 1; continue
    a = dict(a, segmentation=segs, iscrowd=0)
    (groups[key] if key in MERGE else keep).append(a)

for key, parts in groups.items():
    x0 = min(p['bbox'][0] for p in parts); y0 = min(p['bbox'][1] for p in parts)
    x1 = max(p['bbox'][0] + p['bbox'][2] for p in parts); y1 = max(p['bbox'][1] + p['bbox'][3] for p in parts)
    m = dict(parts[0], segmentation=[s for p in parts for s in p['segmentation']],
             area=sum(p['area'] for p in parts), bbox=[x0, y0, x1 - x0, y1 - y0])
    keep.append(m); log[f'digabung {key[0][:8]}:{key[1]}'] = len(parts)

for k, a in enumerate(keep, 1): a['id'] = k
used = {a['category_id'] for a in keep}
d['annotations'] = keep
d['categories'] = [c for c in d['categories'] if c['id'] in used]
json.dump(d, open(DST, 'w'))

print(f"{len(d['images'])} foto, {len(keep)} instance, {len(used)} kelas -> {DST}")
for k, v in log.items(): print(f"  {k}: {v}")
