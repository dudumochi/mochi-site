// Páginas internas (Cases e Case). Movimentos reconstruídos dos módulos da referência:
// WorkLoader, ScrollDelays, FilterTitle, Filters, WorkPosterToCase, DefaultEnter/Leave, Title, Batch,
// ParallaxImages e Footer. Valores e curvas medidos em .reanimate/ (mesmos da Home).
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { CustomEase } from "gsap/CustomEase";
import { SplitText } from "gsap/SplitText";
import { Flip } from "gsap/Flip";
import Lenis from "lenis";
import { proposta, contato } from "./proposta.js";

gsap.registerPlugin(ScrollTrigger, CustomEase, SplitText, Flip);
CustomEase.create("main", "0.44, 0.01, 0, 1");
CustomEase.create("reveal", "0.53, 0.02, 0, 0.99");
CustomEase.create("slow-out", "0.19, 1, 0.22, 1");

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const isMobile = () => innerWidth < 768;
const page = document.body.dataset.page;
// chegou por uma transição interna? (a referência só anima a entrada nesse caso; no acesso direto a página já aparece pronta)
let fromNav = false;
try { fromNav = sessionStorage.getItem("mb-nav") === "1"; sessionStorage.removeItem("mb-nav"); } catch {}
if (reduced) gsap.globalTimeline.timeScale(40);

/* ---------------- rolagem suave ---------------- */
const lenis = new Lenis({ duration: 1, easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)), smoothWheel: !reduced });
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
history.scrollRestoration = "manual";
window.__lenis = lenis;

/* ---------------- transições entre páginas (DefaultLeave / DefaultEnter) ---------------- */
const main = $("[data-main]");
const navItems = $$("[data-pheader] .pheader__brand, [data-pheader] .pill");
const overlay = Object.assign(document.createElement("div"), { className: "ptrans" });
document.body.appendChild(overlay);

const sameSite = (a) => a.origin === location.origin && !a.hash && a.target !== "_blank" && !a.hasAttribute("download");
function leave(href, tl) {
  lenis.stop();
  try { sessionStorage.setItem("mb-nav", "1"); } catch {}
  const t = tl || gsap.timeline({ defaults: { ease: "power1.inOut", duration: .3 } })
    .to(navItems, { yPercent: -300, ease: "reveal", duration: .6 }, 0)       // HideNav
    .to([main, "footer"], { opacity: 0 }, 0);                                 // container opacity .3 s
  // ?medir: roda a transição sem navegar (usado na comparação de movimento do reanimate)
  t.eventCallback("onComplete", () => { if (!new URLSearchParams(location.search).has("medir")) location.href = href; });
  if (reduced) location.href = href;
}
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href]");
  if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
  const url = new URL(a.href, location.href);
  if (url.pathname === location.pathname && url.hash) { // âncora na mesma página
    const el = $(url.hash);
    if (el) { e.preventDefault(); lenis.scrollTo(el, { duration: reduced ? 0 : 1.2, immediate: reduced }); }
    return;
  }
  if (!sameSite(url) && !(url.origin === location.origin && url.hash)) return;
  if (a.hasAttribute("data-poster")) return; // transição própria do pôster
  e.preventDefault();
  leave(url.href);
});
addEventListener("pageshow", (e) => { if (e.persisted) location.reload(); }); // voltar pelo histórico

function enter() {
  if (!fromNav) return;
  // DefaultEnter: container opacity 0 → 1 (.3 s power1.inOut) e o menu desce (yPercent 0, "reveal")
  gsap.fromTo(main, { opacity: 0 }, { opacity: 1, duration: .3, ease: "power1.inOut" });
  gsap.fromTo(navItems, { yPercent: -300 }, { yPercent: 0, duration: 1, ease: "reveal", delay: .1 });
}

/* ---------------- genéricos: Title (linhas), Batch, Parallax, Footer ---------------- */
function splitLines() {
  $$("[data-split-descr]").forEach((el) => {
    const split = new SplitText(el, { type: "lines", linesClass: "descr-line" });
    const tl = gsap.timeline({ paused: true, defaults: { duration: 1.2, ease: "power2.inOut", stagger: .3 } })
      .fromTo(split.lines, { opacity: 0, yPercent: 20 }, { opacity: 1, yPercent: 0 });
    ScrollTrigger.create({ trigger: el, start: "top 80%", onEnter: () => tl.play() });
    ScrollTrigger.create({ trigger: el, start: "top bottom", onLeaveBack: () => tl.time(0).pause() });
  });
  // textos das galerias: linhas em máscara (Title split-lines: yPercent 110 → 0, stagger .1, 1.2 s "reveal")
  $$("[data-split-lines]").forEach((el) => {
    const split = new SplitText(el, { type: "lines", linesClass: "sl-line", mask: "lines" });
    gsap.set(split.lines, { yPercent: 110 });
    ScrollTrigger.create({ trigger: el, start: "top 80%", once: true, onEnter: () => gsap.to(split.lines, { yPercent: 0, stagger: .1, duration: 1.2, ease: "reveal" }) });
  });
}
function batch() {
  const els = $$("[data-batch]");
  gsap.set(els, { opacity: 0 });
  els.forEach((el) => {
    ScrollTrigger.create({ trigger: el, start: "top 85%", onEnter: () => gsap.to(el, { opacity: 1, duration: .6, ease: "power1" }) });
    ScrollTrigger.create({ trigger: el, start: "top bottom", onLeaveBack: () => gsap.set(el, { opacity: 0 }) });
  });
}
function parallaxImages() {
  // ParallaxImages: yPercent -10 → 0 com scale 1.1, scrub 1, do "top bottom" ao "bottom top"
  const imgs = [...$$(".ly-img.is-parallax img"), ...$$("[data-gal-img]")];
  imgs.forEach((im) => {
    gsap.fromTo(im, { yPercent: -10, scale: 1.1, transformOrigin: "top center" }, {
      yPercent: 0, ease: "none",
      scrollTrigger: { trigger: im.parentElement, start: "top bottom", end: "bottom top", scrub: 1 },
    });
  });
}
function footer() {
  const f = $("[data-footer]");
  if (!f) return;
  gsap.matchMedia().add("(min-width: 768px)", () => {
    gsap.fromTo("[data-footer-inner]", { y: "-25vw" }, { y: 0, ease: "none", scrollTrigger: { trigger: f, start: "top bottom", end: "bottom bottom", scrub: true } });
    const tl = gsap.timeline()
      .fromTo("[data-f-left]", { xPercent: 51 }, { xPercent: 0, duration: 5, ease: "power1.out" }, 0)
      .fromTo("[data-f-right]", { xPercent: -50 }, { xPercent: 0, duration: 5, ease: "power1.out" }, 0)
      .fromTo("[data-f-tag]", { yPercent: 100, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 3, ease: "power1.out" }, 1);
    ScrollTrigger.create({ trigger: f, start: "top 70%", end: "bottom bottom", scrub: true, animation: tl });
  });
}

/* ================= 03 / CASES ================= */
function casesPage() {
  const grid = $("[data-cgrid]");
  const posters = $$("[data-poster]", grid);
  const title = $("[data-cgrid-title]");

  // WorkLoader: pôsteres opacity 0 → 1 com stagger .1; o título entra 0,2 s depois
  if (!reduced && fromNav) {
    gsap.timeline({ delay: .15 })
      .fromTo(posters, { opacity: 0 }, { opacity: 1, stagger: .1, duration: .5 })
      .fromTo(title, { opacity: 0 }, { opacity: 1, duration: .5 }, "<0.2");
  }

  // ScrollDelays: cada pôster atrasa conforme a velocidade da rolagem (±250 px), volta a 0 após 150 ms
  if (!reduced && !isMobile()) {
    const quicks = posters.map((p, i) => gsap.quickTo(p, "y", { duration: .2 * parseFloat(`1.${i}`), ease: "power1" }));
    let settle;
    lenis.on("scroll", (l) => {
      const v = gsap.utils.clamp(-250, 250, l.velocity * 1.1);
      quicks.forEach((q) => q(v));
      clearTimeout(settle);
      settle = setTimeout(() => quicks.forEach((q) => q(0)), 150);
    });
  }

  // FilterTitle: letras de "TODOS OS PROJETOS" ganham espaço conforme a rolagem (scrub)
  const ft = $("[data-filter-title] span");
  if (ft && !reduced) {
    document.fonts.ready.then(() => {
      const split = new SplitText(ft, { type: "chars" });
      const steps = [0, 0, .24, 0, 0, .1, .32, 0, .22, .26, 0];
      const tl = gsap.timeline({ defaults: { ease: "none" } });
      split.chars.forEach((c, i) => tl.fromTo(c, { marginLeft: "0em" }, { marginLeft: `${steps[i % steps.length]}em` }, 0));
      ScrollTrigger.create({ trigger: ft, start: "top bottom", end: "center center-=20%", scrub: true, animation: tl });
    });
  }

  // Filtros: reorganiza a grade com Flip (posições dos frames 03.1–03.3 do Figma)
  const slots = grid.dataset.slots.split(";").map((s) => s.split(",").map(Number));
  const all = posters.map((p) => ({ x: +p.style.getPropertyValue("--x"), y: +p.style.getPropertyValue("--y"), w: +p.style.getPropertyValue("--w"), h: +p.style.getPropertyValue("--h") }));
  const btns = $$("[data-filter-btn]");
  const status = $("[data-filter-status]");
  function applyFilter(key) {
    btns.forEach((b) => { const on = b.dataset.filterBtn === key; b.classList.toggle("is-active", on); b.setAttribute("aria-pressed", String(on)); });
    const state = Flip.getState(posters, { props: "opacity" });
    let k = 0;
    posters.forEach((p, i) => {
      const show = key === "todos" || p.dataset.filter === key;
      p.classList.toggle("is-hidden", !show);
      p.toggleAttribute("inert", !show);
      const r = key === "todos" ? all[i] : (show ? (() => { const s = slots[k++]; return { x: s[0], y: s[1], w: s[2], h: s[3] }; })() : all[i]);
      p.style.setProperty("--x", r.x); p.style.setProperty("--y", r.y); p.style.setProperty("--w", r.w); p.style.setProperty("--h", r.h);
    });
    grid.classList.toggle("is-filtered", key !== "todos");
    const n = posters.filter((p) => !p.classList.contains("is-hidden")).length;
    status.textContent = `${n} ${n === 1 ? "case" : "cases"}`;
    Flip.from(state, { duration: 1, ease: "reveal", absolute: true, scale: false, onEnter: (els) => gsap.fromTo(els, { opacity: 0 }, { opacity: 1, duration: .6, stagger: .1 }), onLeave: (els) => gsap.to(els, { opacity: 0, duration: .3 }) });
    ScrollTrigger.refresh();
    lenis.scrollTo(grid, { duration: reduced ? 0 : 1.2, immediate: reduced });
  }
  btns.forEach((b) => b.addEventListener("click", () => applyFilter(b.dataset.filterBtn)));

  // WorkPosterToCase: os outros pôsteres saem para os lados, o título cresce e as letras sobem
  posters.forEach((p) => p.addEventListener("click", (e) => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    e.preventDefault();
    if (reduced) { location.href = p.href; return; }
    lenis.stop();
    const visible = posters.filter((x) => !x.classList.contains("is-hidden"));
    const others = visible.filter((x) => x !== p);
    // par/ímpar pela posição original na grade (como a referência: índice par → -200 %, ímpar → +150 %)
    const odd = visible.filter((x, i) => x !== p && i % 2 === 0), even = visible.filter((x, i) => x !== p && i % 2 === 1);
    const tr = title.getBoundingClientRect();
    const tl = gsap.timeline({ defaults: { ease: "reveal", duration: 1 } })
      .to([...others, ".cgrid__all", "[data-filters]", "footer"], { opacity: 0, duration: .4 }, 0)
      .to(odd, { xPercent: -200, duration: .75 }, 0)
      .to(even, { xPercent: 150, duration: .75 }, 0)
      .to(title, { x: -tr.right }, .01) // o título sai inteiro pela esquerda, sem desbotar
      .to($$("[data-poster-details]", p), { yPercent: 50, autoAlpha: 0, duration: .6 }, .01)
      .to($$(".pt-line", p), { yPercent: () => gsap.utils.random([-120, 120]), duration: .8 }, .01)
      .to($("[data-poster-img]", p), { scale: 1.15, duration: 1 }, 0)
      .to(navItems, { yPercent: -300, duration: .6 }, 0)
      .to(overlay, { opacity: 1, duration: .35, ease: "power1.inOut" }, .75);
    leave(p.href, tl);
  }));
  $("[data-scroll-to]")?.addEventListener("click", (e) => { e.preventDefault(); lenis.scrollTo($("#todos-os-projetos"), { duration: 1.2, offset: -40 }); });
}

/* ================= 04 / CASE ================= */
function casePage() {
  const hero = $("[data-case-hero]");
  const lines = $$(".ch-line", hero);
  const label = $("[data-hero-label]", hero);
  const media = $("[data-hero-media]", hero);
  if (!reduced) {
    // entrada: a imagem assenta (scale 1.1 → 1) e o título sobe por trás da máscara (Title split-lines)
    gsap.fromTo(media, { scale: 1.1 }, { scale: 1, duration: 1.6, ease: "slow-out" });
    gsap.fromTo(label, { yPercent: 110, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 1, ease: "reveal", delay: .2 });
    gsap.fromTo(lines, { yPercent: 110 }, { yPercent: 0, stagger: .1, duration: 1.2, ease: "reveal", delay: .3 });
    // hero: a imagem desce mais devagar que a página (parallax do HeroParallax, 40vh de amplitude)
    gsap.to(media, { y: "30vh", ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
  }
  // próximo case: o nome se abre ao entrar na tela
  const nx = $(".cs-next__name");
  if (nx && !reduced) {
    const split = new SplitText(nx, { type: "chars" });
    gsap.from(split.chars, { yPercent: () => gsap.utils.random([-120, 120]), opacity: 0, stagger: .02, duration: 1, ease: "reveal", scrollTrigger: { trigger: nx, start: "top 85%", once: true } });
  }
}

/* ================= 02 / MÉTODO e MÉTODO SATORI ================= */
function metodoPage() {
  if (reduced) return;
  // entrada: Title split-lines (yPercent 110 → 0, stagger .1, 1.2 s "reveal") + rótulos e imagem assentando
  gsap.fromTo($$(".mh-line, .sab-line"), { yPercent: 110 }, { yPercent: 0, stagger: .1, duration: 1.2, ease: "reveal", delay: .3 });
  gsap.fromTo("[data-hero-label]", { yPercent: 110, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 1, ease: "reveal", delay: .2 });
  const media = $("[data-hero-media]");
  if (media) {
    gsap.fromTo(media, { scale: 1.1 }, { scale: 1, duration: 1.6, ease: "slow-out" });
    gsap.to(media, { y: "30vh", ease: "none", scrollTrigger: { trigger: "[data-mhero]", start: "top top", end: "bottom top", scrub: true } });
  }
  // introdução: linhas em máscara ao entrar (igual à Home)
  const il = $$(".mi-line");
  if (il.length) {
    gsap.set(il, { yPercent: 110 });
    ScrollTrigger.create({ trigger: ".mintro", start: "top 60%", once: true, onEnter: () => gsap.to(il, { yPercent: 0, stagger: .1, duration: 1.2, ease: "reveal" }) });
  }
  // jornada: os 7 estágios em sequência
  const ji = $$("[data-jor-item]");
  if (ji.length) {
    gsap.set(ji, { opacity: 0, yPercent: 30 });
    ScrollTrigger.create({ trigger: "[data-jornada]", start: "top 70%", once: true, onEnter: () => gsap.to(ji, { opacity: 1, yPercent: 0, stagger: .08, duration: 1, ease: "reveal" }) });
  }
  // KO gigante: deriva lateral com o scroll
  const ko = $("[data-ko]");
  if (ko) gsap.fromTo(ko, { xPercent: -8 }, { xPercent: 4, ease: "none", scrollTrigger: { trigger: ko.parentElement, start: "top bottom", end: "bottom top", scrub: 1 } });
}

/* ---------------- boot ---------------- */
document.fonts.ready.then(() => {
  enter();
  if (!reduced) { splitLines(); batch(); parallaxImages(); footer(); }
  if (page === "cases") casesPage();
  if (page === "case") casePage();
  if (page === "metodo" || page === "satori") metodoPage();
  if (page === "proposta") proposta();
  if (page === "contato") contato();
  ScrollTrigger.refresh();
});
