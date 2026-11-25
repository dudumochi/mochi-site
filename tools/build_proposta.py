# Gera /proposta/ (05 planos → 06.A–D, 06.X → 08 resumo, diálogos do 09) e /contato/ (07).
# Uso: python3 tools/build_proposta.py
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import head, header, FOOTER, ARROW, ROOT
from proposta_data import PLANS, STAGES

E = html.escape
def btn(label, attrs='', cls=''):
    return f'<button type="button" class="btn {cls}" {attrs}><span class="btn__label">{label}</span><span class="btn__arrow">{ARROW}</span></button>'

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

TABS = '''<nav class="stabs" aria-label="Seções">
      <a class="pill pill--paper" href="/metodo/satori/"><span class="pill__t">O método</span></a>
      <a class="pill pill--paper" href="/cases/"><span class="pill__t">Cases</span></a>
      <a class="pill pill--paper is-current" aria-current="page" href="/proposta/"><span class="pill__t">Sua proposta</span></a>
    </nav>'''

SUMMARY = f'''<aside class="psum" aria-label="Sua composição" data-psum>
          <p class="psum__k">SUA COMPOSIÇÃO</p>
          <p class="psum__t">Uma operação<br>do seu tamanho.</p>
          <p class="psum__n" data-sum-count>3 itens essenciais</p>
          <hr class="psum__hr" />
          <p class="psum__k">CRIAÇÃO · PAGAMENTO ÚNICO</p>
          <p class="psum__v" data-sum-u>R$ 2.580,00</p>
          <p class="psum__k">MENSALIDADE · POR MÊS</p>
          <p class="psum__v" data-sum-m>R$ 1.350,00</p>
          <p class="psum__x" data-sum-x>Avulsos · R$ 0,00</p>
          {btn('Salvar proposta', 'data-save')}
          <p class="psum__st" data-sum-state>Rascunho não salvo<br>Alterações não publicadas</p>
        </aside>'''

def stage_nav(cur):
    return ''.join(f'<button type="button" class="pstage{" is-on" if k == cur else ""}" data-go="{k}">{L}&nbsp;&nbsp;{n}</button>' for k, L, n, *_ in STAGES)

def rows(st):
    k, L, n, title, sub, kind, items = st
    out = []
    for code, name, price, val, desc, req in items:
        out.append(f'''<div class="psrv{" is-req is-on" if req else ""}" data-srv="{code}" data-kind="{kind}" data-val="{'' if val is None else val}">
            <button type="button" class="psrv__row" aria-pressed="{'true' if req else 'false'}"{' aria-disabled="true"' if req else ''}>
              <span class="psrv__c">{code}</span><span class="psrv__n">{E(name)}</span><span class="psrv__p">{E(price)}</span><span class="psrv__i" aria-hidden="true">{'✓' if req else '+'}</span>
            </button>
            <div class="psrv__d"><p>{E(desc)}</p>{'<p class="psrv__tag">OBRIGATÓRIO · 1 UNIDADE</p>' if req else ''}</div>
          </div>''')
    return '\n          '.join(out)

views = []
# 05 planos
plans = ''.join(f'''<article class="pplan" data-plan="{E(a)}">
        <p class="pplan__k">COMPOSIÇÃO</p><h3 class="pplan__t">{a}</h3><p class="pplan__s">{b}</p>
        <p class="pplan__v" data-money>{c}</p><p class="pplan__m" data-money>{d}</p><p class="pplan__h">Ajuste a composição na jornada.</p>
        <button type="button" class="pill pill--paper pplan__b" data-choose="{E(a)}"><span class="pill__t">ESCOLHER</span></button>
      </article>''' for a, b, c, d in PLANS)
views.append(f'''<section class="pview is-on" data-view="planos" aria-label="Planos e dados">
      <div class="pab"><p class="pk">AGORA, A EXTENSÃO DO SEU PROJETO</p><h1 class="pab__t" data-split-lines>VAMOS DESENHAR<br>SUA PROPOSTA.</h1></div>
      <div class="pdata">
        <label class="pfield"><span>CNPJ (opcional)</span><input name="cnpj" inputmode="numeric" placeholder="Digite o CNPJ" data-store /></label>
        <label class="pfield"><span>Empresa</span><input name="empresa" placeholder="Nome da empresa" data-store /></label>
        <label class="pfield"><span>Contato</span><input name="contato" placeholder="Nome do contato" data-store /></label>
        <button type="button" class="pill pill--paper pdata__b" data-open="dados"><span class="pill__t">DADOS COMPLETOS</span></button>
      </div>
      <div class="pplans">{plans}</div>
      <button type="button" class="ptoggle" data-toggle-money aria-pressed="true">Mostrar investimento <span aria-hidden="true">◉</span></button>
      <p class="pnote">Valores do catálogo de referência. Composição e condições ajustáveis na jornada.</p>
    </section>''')
for st in STAGES:
    k, L, n, title, sub, kind, items = st
    views.append(f'''<section class="pview" data-view="{k}" aria-label="{n}">
      <div class="phd"><p class="pk">COMPONHA SUA JORNADA / {L}</p><h1 class="phd__t">{title}</h1><p class="phd__s">{sub}</p>
        <div class="pstages" role="group" aria-label="Etapas">{stage_nav(k)}</div></div>
      <div class="pbody">
        <div class="pcat">
          {rows(st)}
        </div>
        {SUMMARY}
      </div>
    </section>''')
views.append(f'''<section class="pview" data-view="resumo" aria-label="Resumo">
      <div class="pab"><p class="pk">A PROPOSTA QUE CONSTRUÍMOS NESTA CONVERSA</p><h1 class="pab__t is-sm">UMA MARCA INTEIRA.<br>UMA OPERAÇÃO<br>DO SEU TAMANHO.</h1></div>
      <div class="pbody">
        <div class="pres">
          <h2 class="pres__h">Criação · pagamento único</h2><div data-res="u"></div>
          <h2 class="pres__h">Mensalidade · por mês</h2><div data-res="m"></div>
          <h2 class="pres__h is-sm">Serviços avulsos · pagamento por execução</h2><div data-res="x"></div>
          <p class="pres__note">Direção, roteiros dentro do volume contratado, atendimento, reunião mensal e Metrificai incluídos na operação. Produção, verba de mídia, deslocamento, diárias e necessidades adicionais são orçados à parte. Valores a partir de variam conforme complexidade e escopo de produção. Referências em validação.</p>
          <div class="pres__pdf">{btn('Baixar PDF da proposta', 'data-pdf')}</div>
        </div>
        {SUMMARY}
      </div>
    </section>''')

FIELDS = ['Razão social', 'Nome fantasia', 'Endereço', 'Telefone', 'E-mail', 'Contato', 'Representantes (um nome por linha)']
dialogs = f'''<dialog class="pdlg is-tall" data-dlg="dados" aria-labelledby="dlg-dados">
      <p class="pk">DADOS COMPLETOS</p><h2 class="pdlg__t" id="dlg-dados">Confira os dados.</h2><p class="pdlg__p">Contato e representantes são escolhidos por você.</p>
      <form method="dialog" data-dados>{''.join(f'<label class="pfield"><span>{f}</span>{"<textarea" if "Repres" in f else "<input"} name="d{i}" placeholder="Preencher" data-store>{"</textarea>" if "Repres" in f else ""}</label>' for i, f in enumerate(FIELDS))}
        <div class="pdlg__a"><button class="pill pill--paper" value="cancel"><span class="pill__t">CANCELAR</span></button>{btn('Salvar dados', 'type="submit" value="ok"').replace('type="button" ', '')}</div></form>
    </dialog>
    <dialog class="pdlg" data-dlg="salva" aria-labelledby="dlg-salva"><p class="pk">PROPOSTA / VERSÃO SALVA</p><h2 class="pdlg__t is-xl" id="dlg-salva">PROPOSTA<br>SALVA.</h2><p class="pdlg__p">Sua composição está pronta para compartilhar.</p><div class="pdlg__a">{btn('Copiar link público', 'data-copy')}{btn('Baixar PDF', 'data-pdf')}</div><button type="button" class="pdlg__x" data-close aria-label="Fechar">×</button></dialog>
    <dialog class="pdlg" data-dlg="falha" aria-labelledby="dlg-falha"><p class="pk">NÃO FOI POSSÍVEL SALVAR</p><h2 class="pdlg__t" id="dlg-falha">Tente novamente.</h2><p class="pdlg__p">Sua composição continua nesta tela.</p>{btn('Tentar novamente', 'data-save')}<button type="button" class="pdlg__x" data-close aria-label="Fechar">×</button></dialog>
    <dialog class="pdlg" data-dlg="copiado" aria-labelledby="dlg-cop"><h2 class="pdlg__t" id="dlg-cop">Link copiado.</h2><p class="pdlg__p">Quem receber pode abrir a versão salva da proposta.</p><button type="button" class="pill pill--paper" data-close><span class="pill__t">VOLTAR À PROPOSTA</span></button></dialog>'''

prop = f'''    <div class="pbar">{header('light', current='proposta')}</div>
    {TABS}
    <div class="pviews" data-proposta>
    {chr(10).join(views)}
    <nav class="pflow" aria-label="Avançar na proposta"><button type="button" class="pill pill--paper" data-prev><span class="pill__t">← ANTERIOR</span></button><button type="button" class="pill pill--paper" data-next><span class="pill__t">PRÓXIMO →</span></button><button type="button" class="pill pill--paper" data-pdf data-pdf-flow hidden><span class="pill__t">BAIXAR PDF</span></button></nav>
    </div>
    <p class="sr-only" aria-live="polite" data-live></p>
    {dialogs}'''

contato = f'''    <div class="pbar">{header('light', current='')}</div>
    <section class="cconv" aria-label="Convite"><p class="pk c-white">CONTATO / CANDIDATURA</p><h1 class="cconv__t" data-split-lines>SUA EMPRESA<br>JÁ É BOA. AGORA<br>ELA VAI DOMINAR.</h1></section>
    <section class="cform">
      <h2 class="cform__t" data-split-lines>Comece pela candidatura.</h2>
      <p class="cform__p" data-split-descr>Você chegou até aqui porque sabe que sua marca vale mais do que o mercado enxerga hoje. Nosso time avalia, e havendo encaixe o diagnóstico abre e a jornada começa.</p>
      <a class="pill pill--paper cform__l" href="https://wa.me/5534988510335" target="_blank" rel="noopener"><span class="pill__t">FALAR COM O TIME</span></a>
      <a class="pill pill--paper cform__l is-2" href="https://wa.me/5534988510335" target="_blank" rel="noopener"><span class="pill__t">AGENDAR CONSULTORIA</span></a>
      <form class="cform__f" novalidate data-cand>
        <label class="pfield"><span>Nome</span><input name="nome" required autocomplete="name" placeholder="Seu nome" /></label>
        <label class="pfield"><span>Empresa</span><input name="empresa" required autocomplete="organization" placeholder="Nome da marca" /></label>
        <label class="pfield"><span>E-mail</span><input name="email" type="email" required autocomplete="email" placeholder="voce@empresa.com" /></label>
        <label class="pfield"><span>Onde sua marca quer chegar?</span><textarea name="msg" required rows="2" placeholder="Conte um pouco do seu momento"></textarea></label>
        <p class="cform__err" data-err aria-live="polite"></p>
        <button type="submit" class="btn"><span class="btn__label">Submeter minha marca</span><span class="btn__arrow">{ARROW}</span></button>
      </form>
    </section>
    <dialog class="pdlg" data-dlg="recebida" aria-labelledby="dlg-rec"><p class="pk">CANDIDATURA RECEBIDA</p><h2 class="pdlg__t" id="dlg-rec">Sua marca já está<br>no nosso radar.</h2><p class="pdlg__p">Nosso time vai avaliar afinidade e escopo para conversar sobre os próximos passos.</p><a class="pill pill--paper" href="/"><span class="pill__t">VOLTAR AO INÍCIO</span></a></dialog>'''

for path, h in [('proposta', page('Sua proposta · Mochi Brothers', 'Componha sua jornada com a Mochi Brothers: Despertar, Revelação, Manifestação, Permanência e serviços avulsos.', prop, 'proposta')),
                ('contato', page('Candidatura · Mochi Brothers', 'Submeta sua marca à Mochi Brothers.', contato, 'contato'))]:
    d = os.path.join(ROOT, path); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
print('ok proposta')
