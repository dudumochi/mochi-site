# Gera /metodo/ (02 / O método · Institucional completo, 355:8639) e /metodo/satori/ (02 / Método Satori, 355:7128).
# Uso: python3 tools/build_metodo.py  (também regenera as páginas de cases via build_pages)
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import head, header, FOOTER, ARROW, ROOT

def u(n): return f'calc({n} * var(--u))'
def pos(l, t, w=None, extra=''):
    s = f'left:{u(l)};top:{u(t)};'
    if w: s += f'width:{u(w)};'
    return s + extra

def btn(label, href, l=None, t=None, cls=''):
    st = f' style="position:absolute;{pos(l, t)}"' if l is not None else ''
    return (f'<a class="btn {cls}" href="{href}"{st} data-batch><span class="btn__label">{label}</span>'
            f'<span class="btn__arrow">{ARROW}</span></a>')

def duo(title, body, size, track, dark=False, title_tag='h2', name=''):
    """linha título | texto (padding 76.563/40.833, gap 91.875; 612.5 + 683.958)"""
    paras = body if isinstance(body, list) else [body]
    ps = ''.join(f'<p class="duo__p" data-split-descr>{x}</p>' for x in paras)
    return (f'<section class="duo{" is-dark" if dark else ""}" aria-label="{name or title}">'
            f'<{title_tag} class="duo__t" style="font-size:{u(size)};letter-spacing:{u(track)}" data-split-lines>{title}</{title_tag}>'
            f'<div class="duo__b">{ps}</div></section>')

def page(title, desc, body, key):
    return f'''{head(title, desc)}
<body data-page="{key}">
  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <main id="conteudo" data-main>
{body}
  </main>
{FOOTER}
  <script type="module" src="/src/pages.js"></script>
</body>
</html>
'''

# ---------------- /metodo/ ----------------
steps = [('01', 'Candidatura', 'Você submete sua marca e conta onde ela quer chegar.', 40.83),
         ('02', 'Avaliação', 'Nosso time analisa afinidade, escopo e potencial de referência.', 530.83),
         ('03', 'Aprovação', 'Havendo encaixe, o diagnóstico é liberado e a jornada começa.', 1020.83)]
jornada = ['Empresa boa', 'Clareza', 'Posicionamento', 'Percepção', 'Autoridade', 'Referência', 'Domínio']
CTA = '/contato/'

inst = f'''    <section class="mhero" data-mhero>
      <div class="mhero__media" data-hero-media><img src="/assets/hero.png" alt="" fetchpriority="high" /></div>
      {header('image', current='metodo')}
      <p class="ly mhero__k" style="{pos(29.6, 193.96)}" data-hero-label>MÉTODO SATORI</p>
      <p class="ly mhero__k" style="{pos(29.6, 229.69)}" data-hero-label>( 000 )</p>
      <h1 class="mhero__title" aria-label="A referência não compete. Ela é a medida.">
        <span class="mk ly" style="{pos(285.83, 428.75)}" aria-hidden="true"><span class="mh-line">A REFERÊNCIA</span></span>
        <span class="mk ly" style="{pos(102.08, 541.04)}" aria-hidden="true"><span class="mh-line">NÃO COMPETE.</span></span>
        <span class="mk ly" style="{pos(1061.67, 541.04)}" aria-hidden="true"><span class="mh-line">ELA É</span></span>
        <span class="mk ly" style="{pos(576.77, 663.54)}" aria-hidden="true"><span class="mh-line is-sm">A MEDIDA.</span></span>
      </h1>
    </section>

    <section class="mintro" aria-label="A arte de construir o natural">
      <h2 class="mintro__title">
        <span class="mk ly" style="{pos(519.84, 234.79)}"><span class="mi-line c-pink">A ARTE DE</span></span>
        <span class="mk ly" style="{pos(243.02, 321.56)}"><span class="mi-line">CONSTRUIR O NATURAL</span></span>
        <span class="mk ly" style="{pos(128.49, 408.33)}"><span class="mi-line">COM A INTELIGÊNCIA DIGITAL.</span></span>
      </h2>
      <div class="ly ly-img is-parallax" style="{pos(553.8, 505.31, 362.396, f'height:{u(248.063)}')}"><img src="/assets/komainu.png" alt="Komainu, guardiões em metal — símbolo Mochi" loading="lazy" /></div>
      <p class="ly mintro__p" style="{pos(285.83, 801.35, 898.333)}" data-split-descr>Construímos marcas para serem referência.</p>
      <p class="ly mintro__p" style="{pos(275.63, 913.65, 918.75)}" data-split-descr>Empresas disputam, referências dominam.</p>
      <p class="ly mintro__s" style="{pos(224.58, 969.79, 1020.833)}" data-batch>only for exclusive brands. only for those who love art.</p>
      {btn('Submeter minha marca', CTA, 622.71, 1039.72)}
    </section>

    {duo('Disputa é ruído.', 'Enquanto uns brigam por atenção, outros já são procurados.', 90, -3.6)}
    {duo('Domínio é silêncio.', 'Quem domina nunca precisa levantar a voz.', 90, -3.6)}
    {duo('Entre o ruído e o silêncio, existe um método.', 'Método Satori.', 77, -3.08)}
    {duo('Aceitamos poucas marcas por ano.', ['Referência não se constrói em escala. Ela exige atenção total, e atenção total não se divide entre muitos. Por isso não temos uma lista de clientes. Temos uma seleção.', 'Aqui, a marca não contrata a Mochi Brothers. Ela se candidata. Você submete seu projeto, nosso time avalia a afinidade e o potencial de dominar a categoria, e só quando faz sentido para os dois lados o diagnóstico é liberado e a jornada começa.'], 97.5, -3.9, dark=True)}

    <section class="mabs is-dark" style="height:{u(530.833)}" aria-label="Como entrar">
      <p class="ly mabs__k" style="{pos(40.83, 40.83)}" data-batch>COMO ENTRAR</p>
      {''.join(f'<h3 class="ly msteps__t" style="{pos(l, 102.08, 408.333)}" data-split-lines>{n}<br>{t}</h3><p class="ly msteps__p" style="{pos(l, 234.79, 387.917)}" data-split-descr>{p}</p>' for n, t, p, l in steps)}
      <p class="ly msteps__note" style="{pos(40.83, 408.33, 1102.5)}" data-split-descr>Nem toda marca é aprovada. E é justamente por isso que ser aprovada já diz muito sobre ela.</p>
      {btn('Submeter minha marca', CTA, 1153.54, 442.53)}
    </section>

    {duo('O sistema que constrói referências.', 'Estratégia, identidade e presença contínua em quatro etapas.', 90, -3.6)}

    <section class="mabs" style="height:{u(449.167)}" aria-label="A jornada da referência" data-jornada>
      <p class="ly mabs__k c-muted" style="{pos(40.83, 30.63)}" data-batch>A JORNADA DA REFERÊNCIA</p>
      <p class="ly mjor__lead" style="{pos(40.83, 86.77, 1327.083)}" data-split-descr>Ninguém vira referência por acaso. Cada estágio prepara o próximo, e nenhum se pula.</p>
      <ol class="mjor__list">{''.join(f'<li class="ly mjor__i" style="{pos(40.83 + i * 199.0625, 224.58, 183.75)}" data-jor-item><span class="mjor__n">{i + 1:02d}</span><span class="mjor__l">{x}</span></li>' for i, x in enumerate(jornada))}</ol>
      <p class="ly mjor__foot" style="{pos(40.83, 362.4, 1327.083)}" data-split-descr>Quatro movimentos. O sistema que transforma empresas boas nas marcas mais desejadas e dominantes de cada mercado.</p>
    </section>

    {duo('DESPERTAR', 'Diagnóstico e estratégia para definir a direção da marca.', 88.5, -3.54, title_tag='h3')}
    {duo('REVELAÇÃO', 'Identidade verbal e visual para expressar sua marca.', 88.5, -3.54, title_tag='h3')}
    {duo('MANIFESTAÇÃO', 'Site, canais e lançamento para colocar a marca no mundo.', 88.5, -3.54, title_tag='h3')}
    {duo('PERMANÊNCIA', 'Conteúdo e acompanhamento para manter a marca em movimento.', 88.5, -3.54, title_tag='h3')}

    <section class="mabs" style="height:{u(224.583)}" aria-label="Continuidade">
      <p class="ly mcont__p" style="{pos(40.83, 45.94, 1122.917)}" data-split-descr>Quatro movimentos. Nenhum pulado. Porque referência não se improvisa, se constrói.</p>
      {btn('Conheça o Método Satori', '/metodo/satori/', 1133.13, 141.38)}
    </section>

    {duo('Transformar estratégia em domínio.', 'É onde a estratégia sai do documento e vira algo que o mercado sente na pele. Cada detalhe existe para confirmar, de novo e de novo, que aquela marca é a referência da categoria.', 90, -3.6, dark=True)}
    <section class="mabs is-dark" style="height:{u(265.417)}" aria-label="Indicadores">
      {''.join(f'<p class="ly mind__t" style="{pos(l, 56.15, 408.333)}" data-split-lines>{a}<br>{b}</p>' for l, a, b in [(40.83, 'HORAS DEDICADAS', 'A PROJETOS'), (530.83, 'TOKENS DE', 'INTELIGÊNCIA APLICADA'), (1020.83, 'AGENTES DE IA', 'CRIADOS SOB MEDIDA')])}
    </section>

    <section class="duo" aria-label="Cases"><h2 class="duo__t" style="font-size:{u(131.5)};letter-spacing:{u(-5.26)}" data-split-lines><a href="/cases/">CASES</a></h2><div class="duo__b"><p class="duo__p" data-split-descr>Empresas não crescem só porque são boas. Crescem quando são percebidas como a principal referência do que fazem. A Mochi Brothers existe para construir essa percepção.</p></div></section>

    <section class="mabs is-dark mko" style="height:{u(877.917)}" aria-label="Case em destaque: Koyfer">
      <a class="mko__link" href="/cases/koyfer/" aria-label="Ver case Koyfer"></a>
      <p class="ly mko__ko" style="{pos(76.56, 40.83)}" aria-hidden="true" data-ko>KO</p>
      <p class="ly mko__k" style="{pos(42.88, 35.73)}" data-batch>PERSONA</p>
      <h3 class="ly mko__name" style="{pos(40.83, 597.19)}" data-split-lines>KOYFER</h3>
      <p class="ly mko__p" style="{pos(775.83, 602.29, 643.125)}" data-split-descr>Koyfer transforma técnica em autoridade e barbeiros em empresários. Uma marca de atitude, precisão e visão para quem quer liderar o próprio futuro.</p>
      <p class="ly mabs__k" style="{pos(40.83, 816.67)}" data-batch>01 / 04</p>
      {btn('Ver os 4 cases', '/cases/', 1194.38, 799.82)}
    </section>

    <section class="mabs mmarcas" style="height:{u(673.75)}" aria-label="Marcas Mochi">
      <a class="ly ly-img is-parallax" href="/cases/azevedo-beauty/" style="{pos(0, 0, 719.688, f'height:{u(449.167)}')}"><img src="/media/poster-azevedo-beauty.webp" alt="Azevedo Beauty" loading="lazy" /></a>
      <a class="ly ly-img is-parallax" href="/cases/turbo-tintas/" style="{pos(750.31, 0, 719.688, f'height:{u(449.167)}')}"><img src="/media/poster-turbo-tintas.webp" alt="Turbo Tintas" loading="lazy" /></a>
      <a class="ly mmar__n" href="/cases/azevedo-beauty/" style="{pos(30.63, 474.69)}" data-split-lines>AZEVEDO BEAUTY</a>
      <a class="ly mmar__n" href="/cases/turbo-tintas/" style="{pos(780.94, 474.69)}" data-split-lines>TURBO TINTAS</a>
      <a class="ly mmar__n is-lg" href="/cases/criativi-concept/" style="{pos(30.63, 571.67)}" data-split-lines>CRIATIVI CONCEPT</a>
      <p class="ly mabs__k c-muted" style="{pos(974.9, 617.6)}" data-batch>BRANDING · ESTRATÉGIA · IDENTIDADE</p>
    </section>

    {duo('Notas sobre percepção, posicionamento e domínio de mercado.', 'O QUE APRENDEMOS CONSTRUINDO REFERÊNCIAS, REGISTRADO DIRETO AO PONTO. OS PRIMEIROS ESTÃO A CAMINHO.', 82.5, -3.3)}
    {duo('As perguntas que todo founder faz antes de entrar.', 'AS PERGUNTAS ESTÃO SENDO PUBLICADAS.', 82.5, -3.3)}
    {duo('Sua empresa já é boa. Agora ela vai dominar.', 'Você chegou até aqui porque sabe que sua marca vale mais do que o mercado enxerga hoje. O próximo passo é submeter sua marca. Nosso time avalia, e havendo encaixe o diagnóstico abre e a jornada começa. Nem toda candidatura é aprovada, e tudo começa por afinidade.', 94, -3.76, dark=True)}
    <section class="mabs is-dark" style="height:{u(265.417)}" aria-label="Comece pela candidatura">
      <p class="ly mcand__t" style="{pos(40.83, 30.63, 714.583)}" data-split-lines>Comece pela candidatura.</p>
      {btn('Submeter minha marca', CTA, 40.83, 151.59)}
      <a class="ly mcand__l" style="{pos(520.63, 166.4)}" href="https://wa.me/5534988510335" target="_blank" rel="noopener" data-batch>Falar com o time ↗</a>
      <a class="ly mcand__l" style="{pos(1020.83, 166.4)}" href="https://wa.me/5534988510335" target="_blank" rel="noopener" data-batch>Agendar consultoria ↗</a>
    </section>'''

# ---------------- /metodo/satori/ ----------------
rows = [('Quatro etapas.<br>Uma direção.', 'Da estratégia à presença contínua.'),
        ('01 / Despertar', 'Diagnóstico e estratégia para definir a direção da marca.'),
        ('02 / Revelação', 'Identidade verbal e visual para expressar sua marca.'),
        ('03 / Manifestação', 'Site, canais e lançamento para colocar a marca no mundo.'),
        ('04 / Permanência', 'Conteúdo e acompanhamento para manter a marca em movimento.')]
sat = f'''    <div class="pbar">{header('light', current='metodo')}</div>
    <section class="sab" aria-label="Método Satori" data-sab>
      <p class="ly sab__k" style="{pos(40.83, 51.04)}" data-hero-label>MOCHI BROTHERS / MÉTODO SATORI</p>
      <h1 class="ly sab__t" style="{pos(40.83, 153.13, 1357.708)}">
        <span class="mk"><span class="sab-line">MÉTODO</span></span>
        <span class="mk"><span class="sab-line sab__satori">SATORI.</span></span>
      </h1>
      <p class="ly sab__p" style="{pos(40.83, 811.56)}" data-split-descr>Estratégia, criação e presença contínua.</p>
    </section>
    <nav class="stabs" aria-label="Seções">
      <a class="pill pill--paper is-current" aria-current="page" href="/metodo/satori/" style="{pos(40.83, 25.52)}"><span class="pill__t">O método</span></a>
      <a class="pill pill--paper" href="/cases/" style="{pos(224.58, 25.52)}"><span class="pill__t">Cases</span></a>
      <a class="pill pill--paper" href="/proposta/" style="{pos(362.4, 25.52)}"><span class="pill__t">Sua proposta</span></a>
    </nav>
    <section class="sess" aria-label="As quatro etapas">
      {''.join(f'<div class="sess__row"><h2 class="sess__t" data-split-lines>{a}</h2><p class="sess__p" data-split-descr>{b}</p></div>' for a, b in rows)}
    </section>
    <section class="snext" aria-label="Próximo passo">
      <h2 class="ly snext__t" style="{pos(40.83, 45.94)}" data-split-lines>SUA MARCA,<br>A PARTIR DAQUI.</h2>
      <a class="btn btn--solid" href="/proposta/" style="position:absolute;{pos(40.83, 290.94)}" data-batch><span class="btn__label">Ver cases e compor proposta</span><span class="btn__arrow">{ARROW}</span></a>
    </section>'''

for path, html_ in [('metodo', page('O método · Mochi Brothers', 'Método Satori: o sistema da Mochi Brothers que transforma empresas boas em referências de mercado.', inst, 'metodo')),
                    ('metodo/satori', page('Método Satori · Mochi Brothers', 'Método Satori: Despertar, Revelação, Manifestação e Permanência.', sat, 'satori'))]:
    d = os.path.join(ROOT, path); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html_)
print('ok metodo')
