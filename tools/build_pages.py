# Gera as páginas internas (HTML estático) a partir dos dados do Figma.
# Uso: python3 tools/build_pages.py   → cases/index.html e cases/<slug>/index.html
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from cases_data import CASES, POSTERS, GRID_ALL, GRID_SLOTS, FILTERS

ROOT = os.path.join(os.path.dirname(__file__), '..')
U = lambda n: f'calc({round(n, 3)} * var(--u))'
ARROW = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4.16667 15.8333L15.8333 4.16667M15.8333 15.8333V4.16667H4.16667" stroke-width="1.5" stroke="currentColor"/></svg>'

# rodapé: o mesmo da Home, com os links apontando para as rotas
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
FOOTER = re.search(r'  <!-- FOOTER -->.*?</footer>', home, re.S).group(0)
FOOTER = (FOOTER.replace('href="#topo">HOME', 'href="/">HOME').replace('href="#metodo">MÉTODO', 'href="/metodo/">MÉTODO')
          .replace('href="#cases">CASES', 'href="/cases/">CASES').replace('href="#proposta">PROPOSTA', 'href="/proposta/">PROPOSTA'))

def head(title, desc):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="stylesheet" href="/src/style.css" />
  <link rel="stylesheet" href="/src/pages.css" />
</head>'''

def header(variant, bold=False, current='cases'):
    wm = '/assets/wordmark-dark.svg' if variant == 'light' else '/assets/wordmark-header.svg'
    wh = 'width="162" height="13"' if variant == 'light' else 'width="126" height="8"'
    pills = ''.join(
        f'<a class="pill pill--paper{" is-current" if key == current else ""}" href="{href}"{" aria-current=page" if key == current else ""}><span class="pill__t">{label}</span></a>'
        for key, label, href in [('metodo', 'MÉTODO', '/metodo/'), ('cases', 'CASES', '/cases/'), ('proposta', 'PROPOSTA', '/proposta/')])
    return f'''<header class="pheader pheader--{variant}{' is-bold' if bold else ''}" data-pheader>
      <a class="pheader__brand" href="/" aria-label="Mochi Brothers — início" data-nav-item><img src="{wm}" {wh} alt="" /></a>
      <nav class="pheader__nav" aria-label="Navegação">{pills}</nav>
    </header>'''

def box_style(l):
    s = f'left:{U(l["x"])};top:{U(l["y"])};width:{U(l["w"])};height:{U(l["h"])}'
    return s

def layer(l, parallax=False):
    t = l['t']
    if t == 'img':
        alt = ''
        if l.get('crop'):
            cx, cy, cw, ch = l['crop']
            inner = f'<img src="/media/{l["name"]}.webp" alt="{alt}" loading="lazy" decoding="async" style="position:absolute;left:{cx}%;top:{cy}%;width:{cw}%;height:{ch}%" />'
        else:
            pos = f';object-position:{l["pos"]}' if l.get('pos') else ''
            inner = f'<img src="/media/{l["name"]}.webp" alt="{alt}" loading="lazy" decoding="async" style="width:100%;height:100%;object-fit:cover{pos}" />'
        rot = f';transform:rotate({l["rotate"]}deg)' if l.get('rotate') else ''
        clip = ';overflow:hidden' if l.get('crop') else ''
        return f'<div class="ly ly-img{" is-parallax" if parallax else ""}" style="{box_style(l)}{rot}{clip}">{inner}</div>'
    if t == 'svg':
        return f'<img class="ly" src="/media/{l["name"]}.svg" alt="" style="{box_style(l)}" />'
    if t == 'grad':
        return f'<div class="ly" style="{box_style(l)};background:{l["css"]}"></div>'
    if t == 'box':
        b = f';border:calc({l["border"]} * var(--u)) solid #000' if l.get('border') else ''
        inner = ''.join(layer(x) for x in l['layers'])
        return f'<div class="ly" style="{box_style(l)};background:{l["bg"]};overflow:hidden{b}">{inner}</div>'
    if t == 'text':
        w = f';width:{U(l["w"])}' if l.get('w') else ''
        return (f'<p class="ly ly-text {l["cls"]}" data-split-lines style="left:{U(l["x"])};top:{U(l["y"])};'
                f'font-size:{U(l["size"])}{w};{l["style"]}">{l["html"]}</p>')
    raise ValueError(t)

def poster(c, i):
    slug = c['slug']
    x, y, w, h = GRID_ALL[slug]
    p = POSTERS[slug]
    if p.get('crop'):
        cx, cy, cw, ch = p['crop']
        im = f'<img src="/media/poster-{slug}.webp" alt="" style="position:absolute;left:{cx}%;top:{cy}%;width:{cw}%;height:{ch}%" />'
    else:
        im = f'<img src="/media/poster-{slug}.webp" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{p.get("pos") or "center"}" />'
    # Criativi tem textos em outra posição no Figma
    off = dict(nx=29.04, ny=42, tr=519.04, tx=27, ty=552.41) if slug == 'criativi-concept' else dict(nx=20.42, ny=20.42, tr=510.42, tx=18.38, ty=530.83)
    lines = c['name'].split(' ') if ' ' in c['name'] else [c['name']]
    tag = ''.join(f'<span>{t}</span>' for t in c['tag'])
    ttl = ''.join(f'<span class="pt-mask"><span class="pt-line">{t}</span></span>' for t in lines)
    bg = '#000' if slug == 'criativi-concept' else 'var(--brand)'
    return f'''<a class="poster" href="/cases/{slug}/" data-poster data-filter="{c["filter"]}" data-slug="{slug}"
         style="--x:{x};--y:{y};--w:{w};--h:{h};--bg:{bg};--nx:{off["nx"]};--ny:{off["ny"]};--tr:{off["tr"]};--tx:{off["tx"]};--ty:{off["ty"]}" aria-label="{c["name"].title()} — ver case">
        <span class="poster__img" data-poster-img>{im}</span>
        <span class="poster__no" data-poster-details>NO. {c["no"]}</span>
        <span class="poster__tag" data-poster-details>{tag}</span>
        <span class="poster__title" data-poster-title>{ttl}</span>
      </a>'''

def cases_index():
    posters = '\n      '.join(poster(c, i) for i, c in enumerate(CASES))
    pills = ''.join(f'<button class="pill pill--paper fpill{" is-active" if k == "todos" else ""}" type="button" data-filter-btn="{k}" aria-pressed="{"true" if k == "todos" else "false"}"><span class="pill__t">{l}</span></button>' for k, l in FILTERS)
    slots = ';'.join(f'{x},{y},{w},{h}' for x, y, w, h in GRID_SLOTS)
    return f'''{head('Cases · Mochi Brothers', 'A prova: os cases da Mochi Brothers — Koyfer, Criativi Concept, Azevedo Beauty e Turbo Tintas.')}
<body data-page="cases">
  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <main id="conteudo" data-main>
    <div class="pbar">{header('light')}</div>
    <section class="cgrid" data-cgrid data-slots="{slots}" aria-label="Cases">
      <h1 class="cgrid__title" data-cgrid-title><span>A PROVA</span></h1>
      <a class="cgrid__all" href="#todos-os-projetos" data-scroll-to>TODOS OS CASES ↓</a>
      {posters}
    </section>
    <section class="cfilters" id="todos-os-projetos" data-filters>
      <h2 class="cfilters__title" data-filter-title><span>TODOS OS PROJETOS</span></h2>
      <div class="cfilters__pills" role="group" aria-label="Filtrar cases">{pills}</div>
      <p class="sr-only" aria-live="polite" data-filter-status></p>
    </section>
  </main>
{FOOTER}
  <script type="module" src="/src/pages.js"></script>
</body>
</html>
'''

def case_page(c, idx):
    hero = c['hero']
    ly = ''.join(layer(l) for l in hero['layers'])
    lx, lyy = hero['label']
    t = hero['title']
    diff = ' is-diff' if t.get('diff') else ''
    title_lines = ''.join(f'<span class="mask-l"><span class="ch-line">{x}</span></span>' for x in t['lines'])
    sections = []
    for s in c['sections']:
        single = len(s['layers']) == 1 and s['layers'][0]['t'] == 'img'
        inner = ''.join(layer(l, parallax=single) for l in s['layers'])
        w = f'width:{U(s["w"])};' if s.get('w') else ''
        bg = f'background:{s["bg"]};' if s.get('bg') else ''
        sections.append(f'<section class="cs-sec" style="{w}{bg}height:{U(s["h"])}">{inner}</section>')
    gallery = ''
    if c.get('gallery'):
        def gitem(g):
            n, u, h = g[0], g[1], g[2]
            if u == 'svg':  # composição vetorial (pode ser mais larga que a página; a galeria recorta)
                return f'<div class="cs-gal__item" style="height:{U(h)}"><img src="/media/{n}.svg" alt="" loading="lazy" style="width:{U(g[3])};height:100%;max-width:none" /></div>'
            return f'<div class="cs-gal__item" style="height:{U(h)}"><img src="/media/{n}.webp" alt="" loading="lazy" decoding="async" data-gal-img /></div>'
        items = ''.join(gitem(g) for g in c['gallery'])
        gap = c.get('gallery_gap')
        gst = f' style="gap:0;--gg:{U(gap)}"' if gap is not None else ''
        gallery = f'<section class="cs-gal"{gst} aria-label="Galeria integral">{items}</section>'
    nxt = CASES[(idx + 1) % len(CASES)]
    nextblk = '' if c.get('no_next') else f'''<nav class="cs-next" aria-label="Próximo case">
      <a href="/cases/{nxt['slug']}/" class="cs-next__link" data-next-case>
        <span class="cs-next__k">Próximo projeto…</span>
        <span class="cs-next__name">{nxt['name']}</span>
      </a>
    </nav>'''
    meta = ''.join(f'<p class="cm-k" style="top:{U(y)}" data-batch>{k}</p><p class="cm-v" style="top:{U(y + 30.63)}" data-batch>{v}</p>'
                   for k, v, y in [('PROJETO', c['name'], 102.08), ('CLIENTE', c['name'], 219.48), ('MATERIAIS', c['materials'], 336.88)])
    label_cls = ' w-700' if hero.get('label_bold') else ''
    return f'''{head(f"{c['name'].title()} · Mochi Brothers", c['context'])}
<body data-page="case" data-slug="{c['slug']}">
  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <main id="conteudo" data-main>
    <section class="cs-hero" style="background:{hero['bg']}" data-case-hero>
      <div class="cs-hero__media" data-hero-media>{ly}</div>
      {header('image', c.get('bold_header', False))}
      <p class="cs-hero__label{label_cls}" style="left:{U(lx)};top:{U(lyy)}" data-hero-label>{c['name']}</p>
      <h1 class="cs-hero__title{diff}" style="left:{U(t['x'])};top:{U(t['y'])};width:{U(t['w'])};font-size:{U(t['size'])};line-height:{t['lh']};letter-spacing:{U(t['ls'])}" data-hero-title>{title_lines}</h1>
    </section>
    <section class="cs-ctx" aria-label="Contexto">
      <p class="cm-k" style="left:{U(23.48)};top:{U(102.08)}" data-batch>{c['category']}</p>
      <p class="cs-ctx__text" data-split-descr>{c['context']}</p>
      <div class="cs-ctx__meta">{meta}</div>
    </section>
    {''.join(sections)}
    {gallery}
    {nextblk}
  </main>
{FOOTER}
  <script type="module" src="/src/pages.js"></script>
</body>
</html>
'''

os.makedirs(os.path.join(ROOT, 'cases'), exist_ok=True)
open(os.path.join(ROOT, 'cases', 'index.html'), 'w', encoding='utf-8').write(cases_index())
for i, c in enumerate(CASES):
    d = os.path.join(ROOT, 'cases', c['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(case_page(c, i))
print('ok', len(CASES) + 1, 'páginas')
