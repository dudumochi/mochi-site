// Gera o PDF da proposta no navegador (jsPDF, carregado só no clique). Nada é enviado a servidor.
export async function propostaPDF({ fields = {}, plan, groups, totals }) {
  const { jsPDF } = await import("jspdf");
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  const W = 210, M = 18, CW = W - M * 2;
  const INK = [28, 28, 26], MUTED = [115, 115, 110], BRAND = [128, 64, 56], LINE = [216, 215, 210];
  let y = 0;
  const color = (c) => doc.setTextColor(...c);
  const page = () => { doc.addPage(); y = M; };
  const need = (h) => { if (y + h > 297 - M - 10) page(); };
  const text = (s, x, size, c = INK, opts = {}) => { doc.setFontSize(size); color(c); doc.text(s, x, y, opts); };
  const wrap = (s, size, c = MUTED, w = CW) => {
    doc.setFontSize(size); color(c);
    const lines = doc.splitTextToSize(s, w);
    lines.forEach((l) => { need(size * .45); doc.text(l, M, y); y += size * .45; });
  };
  const rule = () => { doc.setDrawColor(...LINE); doc.setLineWidth(.2); doc.line(M, y, W - M, y); };

  // capa escura
  doc.setFillColor(...INK); doc.rect(0, 0, W, 78, "F");
  doc.setFont("helvetica", "bold"); y = 20; text("MOCHI.BROTHERS", M, 9, [255, 255, 255]);
  doc.setFont("helvetica", "normal"); text("A PROPOSTA QUE CONSTRUÍMOS NESTA CONVERSA", W - M, 7, [200, 200, 195], { align: "right" });
  y = 42; text("UMA MARCA INTEIRA.", M, 24, [255, 255, 255]);
  y = 52; text("UMA OPERAÇÃO DO SEU TAMANHO.", M, 24, [255, 255, 255]);
  y = 68; text(new Date().toLocaleDateString("pt-BR", { day: "2-digit", month: "long", year: "numeric" }), M, 9, [200, 200, 195]);
  if (plan) text(`Ponto de partida: ${plan}`, W - M, 9, [200, 200, 195], { align: "right" });
  y = 92;

  // dados
  const dados = [["Empresa", fields.empresa], ["Contato", fields.contato], ["CNPJ", fields.cnpj], ["Razão social", fields.d0], ["Nome fantasia", fields.d1],
    ["Endereço", fields.d2], ["Telefone", fields.d3], ["E-mail", fields.d4], ["Representantes", (fields.d6 || "").split("\n").filter(Boolean).join(", ")]].filter(([, v]) => v && String(v).trim());
  if (dados.length) {
    text("DADOS", M, 7, MUTED); y += 6;
    dados.forEach(([k, v]) => { need(7); text(k, M, 8, MUTED); doc.setFontSize(10); color(INK); doc.text(doc.splitTextToSize(String(v), CW - 40)[0], M + 40, y); y += 6; });
    y += 6;
  }

  // itens por modalidade
  const section = (title, list, total) => {
    need(20); text(title, M, 14, INK); if (total) text(total, W - M, 14, BRAND, { align: "right" }); y += 4; rule(); y += 6;
    if (!list.length) { text("Nenhum item selecionado.", M, 9, MUTED); y += 10; return; }
    list.forEach((it) => {
      const desc = doc.setFontSize(8).splitTextToSize(it.desc || "", CW - 16);
      need(12 + desc.length * 3.6);
      text(it.code, M, 8, MUTED); text(it.name, M + 16, 10.5, INK); text(it.price, W - M, 9, BRAND, { align: "right" }); y += 4.6;
      doc.setFontSize(8); color(MUTED); desc.slice(0, 4).forEach((l) => { doc.text(l, M + 16, y); y += 3.6; });
      y += 2.4; rule(); y += 5.5;
    });
    y += 4;
  };
  section("Criação · pagamento único", groups.u, totals.u);
  section("Mensalidade · por mês", groups.m, totals.m);
  section("Serviços avulsos · pagamento por execução", groups.x, totals.x);

  // composição
  need(44);
  doc.setFillColor(...INK); doc.rect(M, y, CW, 36, "F");
  const y0 = y; y = y0 + 9; text("SUA COMPOSIÇÃO", M + 7, 7, [255, 255, 255]); text(totals.count, W - M - 7, 8, [200, 200, 195], { align: "right" });
  y = y0 + 18; text("CRIAÇÃO · PAGAMENTO ÚNICO", M + 7, 6.5, [200, 200, 195]); text("MENSALIDADE · POR MÊS", M + CW / 2, 6.5, [200, 200, 195]);
  y = y0 + 28; text(totals.u, M + 7, 17, [255, 255, 255]); text(totals.m, M + CW / 2, 17, [255, 255, 255]);
  y = y0 + 46;
  wrap("Direção, roteiros dentro do volume contratado, atendimento, reunião mensal e Metrificai incluídos na operação. Produção, verba de mídia, deslocamento, diárias e necessidades adicionais são orçados à parte. Valores a partir de variam conforme complexidade e escopo de produção. Referências em validação.", 8);
  y += 3; wrap("Valores do catálogo de referência. Composição e condições ajustáveis na jornada.", 8);

  // rodapé em todas as páginas
  const n = doc.getNumberOfPages();
  for (let i = 1; i <= n; i++) {
    doc.setPage(i); doc.setFontSize(7); color(MUTED);
    doc.text("MOCHI BROTHERS · admin@mochibrothers.com · +55 34 98851-0335", M, 289);
    doc.text(`${i} / ${n}`, W - M, 289, { align: "right" });
  }
  const slug = (fields.empresa || "mochi-brothers").normalize("NFD").replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "-").toLowerCase() || "mochi-brothers";
  doc.save(`proposta-${slug}.pdf`);
}
