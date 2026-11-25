# Baixa as imagens das páginas de case do Figma e grava em public/media/*.webp,
# redimensionadas para 2x a largura exibida no frame de 1470 px (máx. 2600 px), WebP q=80.
# Uso: python3 tools/fetch_assets.py
import io, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from cases_data import CASES, POSTERS

OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'media')
os.makedirs(OUT, exist_ok=True)
jobs = []  # (name, url, display_width_px)

def walk(layers):
    for l in layers:
        if l['t'] == 'img':
            w = l['w'] * ((l['crop'][2] / 100) if l.get('crop') else 1)
            jobs.append((l['name'], l['url'], w))
        elif l['t'] == 'svg':
            jobs.append((l['name'], l['url'], None))
        elif l['t'] == 'box':
            walk(l['layers'])

for c in CASES:
    walk(c['hero']['layers'])
    for s in c['sections']:
        walk(s['layers'])
    for g in c.get('gallery', []):
        name, uid = g[0], g[1]
        if uid not in ('svg', 'local'):  # itens vetoriais ou já salvos localmente
            jobs.append((name, 'https://www.figma.com/api/mcp/asset/' + uid + '.png', 1470))
for slug, p in POSTERS.items():
    w = 537 * ((p['crop'][2] / 100) if p.get('crop') else 1)
    jobs.append((f'poster-{slug}', p['url'], w))

def run(job):
    name, url, w = job
    if w is None:
        dst = os.path.join(OUT, name + '.svg')
        if not os.path.exists(dst):
            for attempt in range(20):
                r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'curl/8.5.0', 'Accept': '*/*'}), timeout=120); d = r.read()
                if r.status == 200 and d:
                    open(dst, 'wb').write(d); break
                time.sleep(3)
        return f'{name}.svg'
    dst = os.path.join(OUT, name + '.webp')
    if os.path.exists(dst):
        return f'{name}.webp (cache)'
    data = b''
    for attempt in range(20):  # o Figma responde 202 enquanto renderiza o asset
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'curl/8.5.0', 'Accept': '*/*'}), timeout=120)
        data = r.read()
        if r.status == 200 and data:
            break
        time.sleep(3)
    try:
        im = Image.open(io.BytesIO(data))
    except Exception:
        return f'FALHOU {name}: {len(data)} bytes, início {data[:60]!r}'
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    target = int(min(im.width, max(800, min(2600, round(w * 2)))))
    if im.width > target:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=80, method=5)
    return f'{name}.webp {im.width}x{im.height} {os.path.getsize(dst)//1024}KB'

with ThreadPoolExecutor(6) as ex:
    for r in ex.map(run, jobs):
        print(r)
print('total', len(jobs))
