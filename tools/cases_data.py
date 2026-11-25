# Dados das páginas de case, extraídos do Figma (MB.Rebranding-mochibrothers).
# Coordenadas em px do frame desktop de 1470 px; o gerador converte para var(--u).
# Camadas:  img(name, url, x, y, w, h, crop=None, fit='cover', pos=None, rotate=None)
#           text(html, x, y, size, cls, w=None, extra='')
F = 'https://www.figma.com/api/mcp/asset/'

def img(name, uid, x, y, w, h, crop=None, pos=None, rotate=None):
    return dict(t='img', name=name, url=F + uid + '.png', x=x, y=y, w=w, h=h, crop=crop, pos=pos, rotate=rotate)

def text(html, x, y, size, cls='', w=None, style=''):
    return dict(t='text', html=html, x=x, y=y, size=size, cls=cls, w=w, style=style)

def box(x, y, w, h, bg, layers, border=None, style=''):
    return dict(t='box', x=x, y=y, w=w, h=h, bg=bg, layers=layers, border=border, style=style)

G = 867.708  # altura das seções de galeria

CASES = [
  dict(
    slug='koyfer', name='KOYFER', no='01', category='PERSONA', filter='persona',
    tag=['Técnica em', 'autoridade.'],
    hero=dict(bg='#804038', layers=[
        img('koyfer-hero-v2', '35f3985a-cb09-4543-9162-169c254f4acb', -13, 0, 1495, 1952),
        text('KOYFER', 29.6, 428.75, 216, 'c-ghost', w=1429.167, style='letter-spacing:calc(-8.64*var(--u));line-height:1'),
      ], label=(29.6, 250.1), title=dict(x=29.6, y=301.15, size=87, lh=1.09, ls=-3.48, w=1020.833, lines=['Técnica em', 'autoridade.'])),
    context='Koyfer transforma técnica em autoridade e barbeiros em empresários. Uma marca de atitude, precisão e visão para quem quer liderar o próprio futuro.',
    materials='SÍNTESE DO PROJETO',
    sections=[
      dict(h=G, bg='#000', layers=[
        text('Na Koyfer, tudo segue um princípio claro', 174, 296.87, 51.084, 'f-tiro c-white', w=794.991),
        text('o barbeiro entra para evoluir<br>e permanece por anos dentro do sistema.', 174, 449.32, 23.946, 'f-inter c-white', style='white-space:nowrap'),
      ]),
      dict(h=G, layers=[img('koyfer-01', '1a53674f-f7da-4ad3-abde-8a5cedbac86d', -72, -0.25, 1542, 868)]),
      dict(h=G, layers=[img('koyfer-02', '301f16de-79dd-42f9-aae4-312c25f0c201', -60, -14.25, 1590, 895)]),
      dict(h=G, layers=[img('koyfer-03', '09a68aac-6de3-44a4-8dfb-616d3a6d7b9a', -60, 0.04, 1590, 895)]),
      dict(h=G, layers=[img('koyfer-04', '8ab1a18f-e2b7-48d4-9416-6f31dd53054f', -89, -29.67, 1648, 927)]),
      dict(h=G, layers=[img('koyfer-05-v2', 'f8c60319-ff6c-44cc-83fe-a40e576e3728', -69, -0.08, 1544, 868)]),
      dict(h=G, layers=[img('koyfer-06', '680f77af-e1d5-4984-b637-8068e7b0b8db', -67, -0.08, 1565, 881)]),
      dict(h=G, layers=[img('koyfer-07', 'a2dc223d-8106-4c10-a9dd-c3a8b40ce1d6', 0, -264.5, 1805, 2707)]),
      dict(h=G, layers=[img('koyfer-08', 'a7e919ea-da69-41d8-90c6-dfb0ca928dd7', -31, -0.21, 1579, 888)]),
      dict(h=G, layers=[img('koyfer-09', 'cbb36b8d-b8b3-4cfa-b9e5-016aa7655e34', -199, 0.08, 1868, 1051)]),
      dict(h=G, layers=[img('koyfer-10', '4999b2f0-d0f6-4a3c-b364-d0a1dc83b471', -565, -732.63, 2731, 4096)]),
      dict(h=G, bg='#000', layers=[img('koyfer-11', 'fba05b8e-0d00-4335-83d1-b26108ccc81d', 197, 130.67, 1076, 605)]),
      dict(h=G, layers=[img('koyfer-12', '08ab068d-e106-45ef-af8f-0ea973fd60e0', -36, -108.04, 1541, 2311)]),
      dict(h=G, bg='#000', layers=[img('koyfer-13', '8dfdf434-7c68-410f-b451-d65c5e872aa4', 79, 65.25, 1311, 738)]),
      dict(h=G, bg='#000', layers=[img('koyfer-14', '10da4b1f-bba0-43f1-8752-7a89f002afa1', -794, -1748.46, 2731, 4096)]),
      dict(h=G, bg='#000', layers=[img('koyfer-15', 'ee3f3263-0167-4255-a287-4806077c8f65', 74, 124.83, 1321, 743)]),
    ],
  ),
  dict(
    slug='criativi-concept', name='CRIATIVI CONCEPT', no='02', category='CONSTRUÇÃO CIVIL', filter='construcao',
    tag=['Um jeito', 'de viver.'], bold_header=True,
    hero=dict(bg='#804038', layers=[
        img('criativi-hero', '5ea7d0b2-ecdf-4483-9b89-ea4bcba68efe', -202, -56, 1722, 969),
        text('CRIATIVI CONCEPT', 29.6, 428.75, 169, 'c-ghost w-700', w=1429.167, style='letter-spacing:calc(-6.76*var(--u));line-height:1'),
      ], label=(30, 188), label_bold=True, title=dict(x=30, y=239.04, size=87, lh=1.09, ls=-3.48, w=1020.833, lines=['Um jeito', 'de viver.'])),
    context='A Criativi dá forma ao jeito de viver de cada cliente. Móveis sob medida, ambientes com identidade e uma relação que continua depois da entrega.',
    materials='SÍNTESE DO PROJETO',
    sections=[
      dict(h=829, w=1459, layers=[img('criativi-01', '48389860-4454-4f85-b838-1c8580f7b0d0', 0, 0, 1459, 829)]),
      dict(h=G, layers=[
        box(-62, 0.46, 1679.758, 867, '#000', []),
        text('Você dorme em obra.<br>Acorda em casa pronta.', 128.72, 284.79, 55.992, 'f-tiro c-white', style='white-space:nowrap'),
        text('Fala só com a Criativi e recebe a chave. Sem poeira, sem pendência, sem ninguém além de nós pra você cobrar. Contrata uma vez — a obra inteira sai da sua lista.', 128.72, 492.14, 26.246, 'f-inter c-white', w=934.365),
      ]),
      dict(h=G, layers=[img('criativi-02', 'ce04847c-cfd3-4e17-9283-a118d9d7d06a', -228, -108.25, 1925, 1083)]),
      dict(h=G, layers=[img('criativi-03', 'bb16b527-1cfa-4b81-b917-af9ef172a58f', 88.91, 185.31, 1291.992, 563.555)]),
      dict(h=G, layers=[text('Do início ao fim com a criativi', 308, 374.33, 64, 'f-tiro c-black', style='white-space:nowrap')]),
      dict(h=G, bg='#fff', layers=[img('criativi-04', 'ae436471-8f24-4c37-ba5d-ff6e704e273f', 165, 37.91, 1177, 739)]),
      dict(h=G, layers=[box(0, -0.08, 1605, 902.782, '#e9e8e4', [
          img('criativi-05', '97214a55-5d36-4e42-be1e-2106e42d0624', 185.78, 66.03, 616.486, 770.207),
          img('criativi-06', '96804549-d297-4292-a25d-f6f32c7e6a9c', 891.91, 181.34, 431.874, 539.561),
        ], border=0.164)]),
      dict(h=G, layers=[box(-51, 0.21, 1521.48, 855.803, '#e9e8e4', [
          img('criativi-07', '2e90e2bd-5a7a-41a1-86f7-e300e2eb8ad0', -271.25, -579.72, 2745.601, 2384.555),
          dict(t='grad', x=-17.28, y=-28.96, w=1538.608, h=884.61, css='linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,.22))'),
          dict(t='svg', name='criativi-logo', url=F + '0239ce1a-70d2-4956-accd-174c581dc59b.svg', x=613.3, y=754.6, w=295.2, h=46.6),
          text('FALE APENAS', 0, 40.02, 46.714, 'f-inter c-white t-center', w=1521.48, style='line-height:1.5;letter-spacing:calc(-1.0744*var(--u))'),
          text('COM A', 0, 400.93, 46.714, 'f-inter c-white t-center', w=1521.48, style='line-height:1.5;letter-spacing:calc(-1.0744*var(--u))'),
          text('Você não recebe um ambiente pronto pra montar. Recebe um ambiente pronto pra usar', 545.5, 230.52, 18.686, 'f-inter w-500 c-white t-center', w=431.016, style='line-height:1.05;letter-spacing:calc(-.4298*var(--u))'),
          text('Você acorda no primeiro dia já com fogão ligado pro seu café da manhã.', 579.4, 591.43, 18.686, 'f-inter w-500 c-white t-center', w=362.969, style='line-height:1.14;letter-spacing:calc(-.4298*var(--u))'),
        ], border=0.156)]),
      dict(h=G, bg='#fff', layers=[img('criativi-08', '66d38503-69f8-4b2f-9700-b000580cdf26', 193, 36.5, 1084, 793)]),
      dict(h=G, layers=[img('criativi-09', '87858ef8-b00a-4098-b838-4db48ee63bdb', -125, -0.21, 1594.812, 1025.819)]),
    ],
  ),
  dict(
    slug='azevedo-beauty', name='AZEVEDO BEAUTY', no='03', category='VAREJO', filter='varejo',
    tag=['Cuidado de', 'alto padrão.'],
    hero=dict(bg='#1c1c1a', layers=[img('azevedo-hero', 'e1b217dd-049a-4ec9-bee9-f2bbb70a6d95', -422, -45, 1892, 1051)],
      label=(29.6, 250.1), title=dict(x=17.35, y=292.98, size=105, lh=.95, ls=-4.2, w=488.979, lines=['Cuidado de alto padrão.'], diff=True)),
    context='Azevedo Beauty. O cuidado de alto padrão mais perto de quem quer se sentir bem todos os dias.',
    materials='BRANDING E MATERIAIS',
    sections=[
      dict(h=G, layers=[img('azevedo-abertura', 'cad83cf4-6ca8-483c-ab79-a1e93f6b788f', 23.48, 0, 1423.042, 800.333)]),
      dict(h=1327.083, layers=[
        img('azevedo-ed-1', '9c12c497-fd4a-4010-a598-5e5c01d1b1d0', 23.48, 0, 1423.042, 663.542),
        img('azevedo-ed-2', '3cdf22be-9a64-44aa-98a0-f9ed3400fe9e', 23.48, 694.17, 1423.042, 592.083),
      ]),
    ],
    gallery=[(f'azevedo-{n}', u, h) for n, u, h in [
      ('05', 'b53fbae6-ca98-42e9-a711-7d90fe59e8ad', 899.354), ('06', 'b6033de1-5943-4e3c-a1bc-18f934ead389', 882),
      ('07', '49c2add9-708f-4ae4-8c78-07239b3755fe', 1043.292), ('08', '3ab852aa-8d6a-44ba-9887-f11e7d676ff3', 829.938),
      ('09', '91adbd84-f3ca-4b70-a040-58c7917ddaed', 906.5), ('10', '453fddbf-f962-4161-a2b9-d64c8f5580ef', 882),
      ('12', 'b4ab06cc-a30e-4823-824b-1475e6654927', 940.188), ('13', 'b4e17d21-9f29-402f-b7ba-59b407f549b3', 692.125),
      ('14', '92b4b6c2-d8a8-428a-8740-5f844c787967', 789.104), ('15', '2e2b0b8a-8eef-491a-b2cc-2863fb63b50e', 826.875),
      ('16', '8d7e1102-2e2c-43ab-9beb-9c9de97f4478', 826.875), ('17', '07180976-871b-4640-af5d-5f2c71d9d958', 826.875),
      ('18', 'c5b869ca-0ba9-40fa-9463-e70fe58fa275', 826.875), ('19', '3f5cdf67-7701-43d8-8378-8e5e0b04ccee', 826.875),
      ('20', 'caeea15f-c176-4fd3-b0cf-ace5284276cc', 826.875), ('21', 'a7786e9c-1015-4f7b-ab09-62e9a52b5f79', 826.875),
      ('22', 'b03481bf-8d60-4e50-8e29-694193e7733b', 815.646), ('23', '0cd2ff17-c38f-4436-bdb7-7a28844a79d6', 815.646)]],
  ),
  dict(
    slug='turbo-tintas', name='TURBO TINTAS', no_next=True, no='04', category='CONSTRUÇÃO CIVIL', filter='construcao',
    tag=['Toda conquista', 'merece uma cor.'],
    hero=dict(bg='#1c1c1a', layers=[
        img('turbo-hero-v2', '28065927-0bc5-4c97-b656-4901e51bae1c', -56, 0, 1956, 1101),
        text('TURBO<br>TINTAS', 20, 455, 169, 'c-ghost w-700', w=1429.167, style='letter-spacing:calc(-6.76*var(--u));line-height:1'),
      ], label=(29.6, 250.1), title=dict(x=29.6, y=301.15, size=87, lh=.88, ls=-3.48, w=1020.833, lines=['Toda conquista', 'merece uma cor.'], diff=True)),
    context='Toda conquista merece uma cor. A Turbo Tintas faz parte de quem constrói, renova e dá vida ao próximo capítulo.',
    materials='BRANDING E MATERIAIS',
    sections=[
      dict(h=G, layers=[img('turbo-abertura', '51884441-6eac-4124-853e-908314a4f5e7', -6, 37.458, 1476, 830)]),
    ],
    gallery_gap=-54,
    gallery=[('turbo-v4-capa', 'local', 801), ('turbo-identidade', 'svg', 914.833, 1626.794)] + [(f'turbo-v3-{n}', 'local', h) for n, h in [
      ('15', 832), ('09', 826.875), ('07', 826), ('16', 826.875), ('10', 826.875), ('11', 846.271), ('12', 826.875), ('17', 826.875)]],
  ),
]

# Grade de cases (03 / Cases · Desktop): pôster de cada case (imagem + recorte do Figma)
POSTERS = {
  'koyfer': dict(url=F + '841b3c9b-6a0c-4a01-8df5-2d6d7562a75a.png', crop=None, pos='bottom'),
  'criativi-concept': dict(url=F + '970519e3-e64e-4e80-9979-23864c86072f.png', crop=(-58.36 * 556 / 537 + (867 - 882) / 537 * 100, (-3.75 * 744 / 740) + (350.17 - 354.17) / 740 * 100, 181.66 * 556 / 537, 181.01 * 744 / 740)),
  'azevedo-beauty': dict(url=F + '30a2d215-e153-4e62-8705-0d3f988ce5e4.png', crop=(0, -4.78, 319.2, 131.17)),
  'turbo-tintas': dict(url=F + 'fb3d8da0-b881-4d81-bc56-6d909a79edb4.png', crop=(-62.41, -0.02, 247.16, 100)),
}
# posições (x, y, w, h) na grade "Todos" e nas grades filtradas (duas posições)
GRID_ALL = {'koyfer': (330, 130.17, 537, 729), 'criativi-concept': (882, 354.17, 537, 740),
            'azevedo-beauty': (330, 1090.17, 537, 734), 'turbo-tintas': (904, 1310, 537, 740)}
GRID_SLOTS = [(330.75, 130.67, 536.958, 735), (904.46, 351.17, 536.958, 735)]
FILTERS = [('todos', 'Todos'), ('persona', 'Persona'), ('construcao', 'Construção Civil'), ('varejo', 'Varejo')]
