// Configurador da proposta (05 → 06.A–D/X → 08) e candidatura (07). Estados e diálogos do frame 09.
// Tudo roda no navegador: a composição fica no localStorage deste visitante; nada é enviado a servidor.
import { gsap } from "gsap";
import { propostaPDF } from "./proposta-pdf.js";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const KEY = "mb-proposta";
const brl = (n) => n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }).replace(/ /g, " ");
const store = {
  get() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } },
  set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); return true; } catch { return false; } },
};

export function proposta() {
  const root = $("[data-proposta]");
  const order = ["planos", "a", "b", "c", "d", "x", "resumo"];
  const live = $("[data-live]");
  let st = Object.assign({ sel: [], fields: {}, money: true, view: "planos", plan: null }, store.get());
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const dirty = () => $$("[data-sum-state]").forEach((p) => (p.innerHTML = "Rascunho não salvo<br>Alterações não publicadas"));
  const persist = () => store.set({ ...st, saved: undefined });

  // seleção de serviços
  const items = $$("[data-srv]");
  items.forEach((it) => {
    const code = it.dataset.srv;
    if (!it.classList.contains("is-req") && st.sel.includes(code)) setOn(it, true);
    $(".psrv__row", it).addEventListener("click", () => {
      if (it.classList.contains("is-req")) return;
      const on = !it.classList.contains("is-on");
      setOn(it, on);
      st.sel = on ? [...new Set([...st.sel, code])] : st.sel.filter((c) => c !== code);
      persist(); dirty(); totals();
      live.textContent = `${code} ${on ? "adicionado" : "removido"}.`;
    });
  });
  function setOn(it, on) {
    it.classList.toggle("is-on", on);
    $(".psrv__row", it).setAttribute("aria-pressed", String(on));
    $(".psrv__i", it).textContent = on ? "✓" : "+";
  }
  function chosen() {
    const seen = new Set();
    return items.filter((it) => it.classList.contains("is-on") && !seen.has(it.dataset.srv) && seen.add(it.dataset.srv));
  }
  function totals() {
    const ch = chosen();
    const sum = (k) => ch.filter((i) => i.dataset.kind === k).reduce((a, i) => a + (+i.dataset.val || 0), 0);
    const req = ch.filter((i) => i.classList.contains("is-req")).length;
    const extra = ch.length - req;
    const tbd = ch.some((i) => i.dataset.val === "");
    $$("[data-sum-count]").forEach((e) => (e.textContent = `${req} itens essenciais${extra ? ` + ${extra} escolhido${extra > 1 ? "s" : ""}` : ""}`));
    $$("[data-sum-u]").forEach((e) => (e.textContent = brl(sum("u"))));
    $$("[data-sum-m]").forEach((e) => (e.textContent = brl(sum("m"))));
    $$("[data-sum-x]").forEach((e) => (e.textContent = `Avulsos · ${brl(sum("x"))}${tbd ? " + a definir" : ""}`));
    // 08 resumo por modalidade
    ["u", "m", "x"].forEach((k) => {
      const box = $(`[data-res="${k}"]`);
      const list = ch.filter((i) => i.dataset.kind === k);
      box.innerHTML = list.length ? list.map((i) => {
        const p = $(".psrv__p", i).textContent;
        return `<div class="pres__r"><span class="psrv__c">${i.dataset.srv}</span><span class="psrv__n">${$(".psrv__n", i).textContent}</span><span class="psrv__p">${p}${k === "m" && !/mês/.test(p) ? "" : ""}</span><span class="psrv__i">✓</span></div>`;
      }).join("") : `<p class="pres__empty">Nenhum item selecionado.</p>`;
    });
  }

  // navegação entre etapas
  function go(v, focus = true) {
    if (!order.includes(v)) v = "planos";
    const cur = $(".pview.is-on", root), next = $(`[data-view="${v}"]`, root);
    if (cur !== next) {
      cur?.classList.remove("is-on"); next.classList.add("is-on");
      if (!reduced) gsap.fromTo(next.children, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .8, stagger: .06, ease: "reveal" });
    }
    st.view = v; persist();
    history.replaceState(null, "", `#${v}`);
    $("[data-prev]").hidden = v === "planos";
    $("[data-pdf-flow]").hidden = v !== "resumo";
    $("[data-next] .pill__t").textContent = v === "resumo" ? "SALVAR PROPOSTA" : v === "x" ? "VER RESUMO →" : "PRÓXIMO →";
    if (focus) { window.__lenis?.scrollTo(root.offsetTop - 0, { immediate: reduced }); $("h1", next)?.setAttribute("tabindex", "-1"); $("h1", next)?.focus({ preventScroll: true }); }
  }
  $$("[data-go]").forEach((b) => b.addEventListener("click", () => go(b.dataset.go)));
  $("[data-prev]").addEventListener("click", () => go(order[order.indexOf(st.view) - 1]));
  $("[data-next]").addEventListener("click", () => st.view === "resumo" ? save() : go(order[order.indexOf(st.view) + 1]));
  $$("[data-choose]").forEach((b) => b.addEventListener("click", () => {
    st.plan = b.dataset.choose; $$(".pplan").forEach((p) => p.classList.toggle("is-on", p.dataset.plan === st.plan)); go("a");
  }));
  if (st.plan) $$(".pplan").forEach((p) => p.classList.toggle("is-on", p.dataset.plan === st.plan));

  // mostrar / ocultar investimento (09 · Valores ocultos)
  const tg = $("[data-toggle-money]");
  const money = () => {
    tg.setAttribute("aria-pressed", String(st.money)); $("span", tg).textContent = st.money ? "◉" : "◯";
    $$("[data-money]").forEach((e) => { e.dataset.orig ??= e.textContent; e.textContent = st.money ? e.dataset.orig : "Sob consulta"; });
  };
  tg.addEventListener("click", () => { st.money = !st.money; persist(); money(); });
  money();

  // campos (dados rápidos e completos)
  $$("[data-store]").forEach((f) => {
    if (st.fields[f.name]) f.value = st.fields[f.name];
    f.addEventListener("input", () => { st.fields[f.name] = f.value; persist(); dirty(); });
  });
  const cnpj = $('input[name="cnpj"]');
  cnpj.addEventListener("input", () => {
    const d = cnpj.value.replace(/\D/g, "").slice(0, 14);
    cnpj.value = d.replace(/^(\d{2})(\d)/, "$1.$2").replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3").replace(/\.(\d{3})(\d)/, ".$1/$2").replace(/(\d{4})(\d)/, "$1-$2");
  });

  // diálogos
  const dlg = (n) => $(`[data-dlg="${n}"]`);
  const open = (n) => { $$("dialog[open]").forEach((d) => d.close()); dlg(n).showModal(); };
  $$("[data-open]").forEach((b) => b.addEventListener("click", () => open(b.dataset.open)));
  $$("[data-close]").forEach((b) => b.addEventListener("click", () => b.closest("dialog").close()));
  $$("dialog").forEach((d) => d.addEventListener("click", (e) => { if (e.target === d) d.close(); }));
  function save() {
    const data = { ...st, savedAt: new Date().toISOString() };
    if (!store.set(data)) return open("falha");
    $$("[data-sum-state]").forEach((p) => (p.innerHTML = `Versão salva neste navegador<br>${new Date().toLocaleString("pt-BR")}`));
    open("salva");
  }
  $$("[data-save]").forEach((b) => b.addEventListener("click", save));
  $("[data-copy]").addEventListener("click", async () => {
    const url = `${location.origin}${location.pathname}#resumo`;
    try { await navigator.clipboard.writeText(url); open("copiado"); } catch { open("falha"); }
  });

  // PDF da proposta (08 · resumo)
  $$("[data-pdf]").forEach((b) => b.addEventListener("click", async () => {
    const ch = chosen();
    const pick = (k) => ch.filter((i) => i.dataset.kind === k).map((i) => ({
      code: i.dataset.srv, name: $(".psrv__n", i).textContent, price: $(".psrv__p", i).textContent, desc: $(".psrv__d p", i)?.textContent || "" }));
    const t = (sel) => $(`.pview.is-on ${sel}`)?.textContent || $(sel).textContent;
    b.setAttribute("aria-busy", "true");
    try {
      await propostaPDF({ fields: st.fields, plan: st.plan, groups: { u: pick("u"), m: pick("m"), x: pick("x") },
        totals: { u: t("[data-sum-u]"), m: t("[data-sum-m]"), x: t("[data-sum-x]").replace(/^Avulsos · /, ""), count: t("[data-sum-count]") } });
      live.textContent = "PDF da proposta gerado.";
    } catch (e) { console.error(e); open("falha"); }
    b.removeAttribute("aria-busy");
  }));

  totals();
  go(location.hash.slice(1) || st.view, false);
}

export function contato() {
  const f = $("[data-cand]"), err = $("[data-err]", f);
  f.addEventListener("submit", (e) => {
    e.preventDefault();
    const bad = [...f.elements].filter((el) => el.willValidate && !el.checkValidity());
    $$(".pfield", f).forEach((l) => l.classList.toggle("is-bad", bad.includes($("input,textarea", l))));
    if (bad.length) { err.textContent = "Confira os campos destacados."; bad[0].focus(); return; }
    err.textContent = "";
    // Sem destino configurado: a candidatura não é enviada a lugar nenhum ainda.
    $('[data-dlg="recebida"]').showModal();
  });
}
