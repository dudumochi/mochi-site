# Verifica se as imagens do site ainda correspondem às imagens-fonte do Figma (hash perceptual dHash).
# Uso: python3 tools/check_swaps.py <urls.json>   (json: {"grupo": ["url", ...]})
import io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
MEDIA = os.path.join(os.path.dirname(__file__), '..', 'public', 'media')

def dhash(im, n=16):
    g = im.convert('L').resize((n + 1, n), Image.LANCZOS)
    px = list(g.getdata())
    return sum(1 << i for i in range(n * n) if px[(i // n) * (n + 1) + i % n] > px[(i // n) * (n + 1) + i % n + 1])

def fetch(u):
    for _ in range(10):
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'curl/8.5.0'}), timeout=120)
        d = r.read()
        if r.status == 200 and d:
            return dhash(Image.open(io.BytesIO(d)))
    return None

groups = json.load(open(sys.argv[1]))
used = set(json.load(open(sys.argv[2]))) if len(sys.argv) > 2 else None
for prefix, urls in groups.items():
    with ThreadPoolExecutor(6) as ex:
        raw = [h for h in ex.map(fetch, urls) if h is not None]
    site = sorted(f for f in os.listdir(MEDIA) if f.startswith(prefix) and f.endswith('.webp') and (used is None or f[:-5] in used))
    print(f'== {prefix}: {len(site)} imagens no site, {len(raw)} fontes no Figma')
    for f in site:
        h = dhash(Image.open(os.path.join(MEDIA, f)))
        d = min(bin(h ^ r).count('1') for r in raw) if raw else 999
        print(f'  {"ok   " if d <= 40 else "MUDOU?"} {f}  distância {d}')
