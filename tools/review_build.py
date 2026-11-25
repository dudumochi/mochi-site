# Prepara o build para revisão como Artifact (caminhos relativos, sem servidor).
# Uso: npx vite build --base ./ --outDir dist-review --emptyOutDir && python3 tools/review_build.py
import os, re, glob, json
D = os.path.join(os.path.dirname(__file__), '..', 'dist-review')

def rel(prefix, path):
    path = path.lstrip('/')
    if path == '' or path.startswith('#'):
        return prefix + 'index.html' + path
    m = re.match(r'([^#?]*)([#?].*)?$', path)
    p, rest = m.group(1), m.group(2) or ''
    if p.endswith('/') or p == '':
        p += 'index.html'
    return prefix + p + rest

for f in glob.glob(os.path.join(D, '**', '*.html'), recursive=True):
    depth = os.path.relpath(f, D).count(os.sep)
    prefix = '../' * depth
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'(href|src|data-poster)="(/[^"]*)"', lambda m: f'{m.group(1)}="{rel(prefix, m.group(2))}"', s)
    open(f, 'w', encoding='utf-8').write(s)

# rotas escritas no JS da Home (slider): relativas à raiz
for f in glob.glob(os.path.join(D, 'assets', '*.js')):
    s = open(f, encoding='utf-8').read()
    s2 = re.sub(r'"/cases/([a-z-]*)/?"', lambda m: f'"cases/{m.group(1) + "/" if m.group(1) else ""}index.html"', s)
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2)

# página principal do Artifact: a Home sem o esqueleto do documento
s = open(os.path.join(D, 'index.html'), encoding='utf-8').read()
head = re.search(r'<head>(.*?)</head>', s, re.S).group(1)
body = re.search(r'<body[^>]*>(.*)</body>', s, re.S).group(1)
head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*|<title>.*?</title>', '', head)
open(os.path.join(D, 'page.html'), 'w', encoding='utf-8').write('<title>Mochi Brothers Site</title>\n' + head + '\n<script>document.body.classList.add("is-loading")</script>\n' + body)

files = sorted(os.path.relpath(p, D) for p in glob.glob(os.path.join(D, '**', '*'), recursive=True) if os.path.isfile(p) and not p.endswith('page.html'))
json.dump(files, open(os.path.join(D, '..', 'tools', 'review_files.json'), 'w'), indent=0)
print(len(files), 'arquivos')
