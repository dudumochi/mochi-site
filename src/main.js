// Mochi Brothers — home. Movimentos reconstruídos a partir dos módulos da referência
// (HomeLoader, HeroParallax, Intro, Title/Batch, BScroll, BleedSlider). Ver .reanimate/mochi-home/spec.md
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { CustomEase } from "gsap/CustomEase";
import { SplitText } from "gsap/SplitText";
import Lenis from "lenis";

gsap.registerPlugin(ScrollTrigger, CustomEase, SplitText);
CustomEase.create("main", "0.44, 0.01, 0, 1");
CustomEase.create("reveal", "0.53, 0.02, 0, 0.99");
CustomEase.create("slow-out", "0.19, 1, 0.22, 1");

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const isMobile = () => innerWidth < 768;
const params = new URLSearchParams(location.search);

/* ---------------- scroll suave (Lenis, mesma config da referência) ---------------- */
const lenis = new Lenis({ duration: 1, easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)), smoothWheel: !reduced, syncTouch: false });
// movimento reduzido: toda transição que ainda rodar fica praticamente instantânea
if (reduced) gsap.globalTimeline.timeScale(40);
// enquanto uma âncora rola a página, a transição do monograma não deve "capturar" a rolagem
let navScrolling = false;
const scrollToEl = (el, opts = {}) => {
  navScrolling = true;
  lenis.scrollTo(el, {
    duration: reduced ? 0 : 1.2, immediate: reduced, force: true, offset: isMobile() ? -65 : 0, ...opts,
    onComplete: () => { navScrolling = false; ScrollTrigger.update(); },
  });
  if (reduced) setTimeout(() => { navScrolling = false; }, 50);
};
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
history.scrollRestoration = "manual";
window.scrollTo(0, 0);
window.__lenis = lenis;

let scrollInited = false;

/* ================= MENU / NAV ================= */
const navItems = [$(".header__brand"), $(".header__mono"), ...$$(".header__nav .pill")];
navItems.forEach((n) => n.setAttribute("data-nav-item", ""));

const menu = $("#menu");
const toggle = $("[data-menu-toggle]");
const menuLinks = $$("[data-menu-link] span");
let menuOpen = false;
const menuTl = gsap.timeline({ paused: true, defaults: { ease: "reveal" } })
  .set(menu, { visibility: "visible" })
  .fromTo(menu, { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: .9 })
  .fromTo(menuLinks, { yPercent: 110 }, { yPercent: 0, duration: 1, stagger: .05, ease: "slow-out" }, .2)
  .fromTo([".menu__langs", ".menu__prefs"], { autoAlpha: 0, yPercent: 50 }, { autoAlpha: 1, yPercent: 0, duration: .8 }, .45);
function setMenu(open) {
  if (!isMobile() && open) return;
  menuOpen = open;
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Fechar menu" : "Mochi Brothers — abrir menu");
  menu.setAttribute("aria-hidden", String(!open));
  menu.toggleAttribute("inert", !open);
  document.body.classList.toggle("menu-open", open);
  if (open) { lenis.stop(); menuTl.timeScale(1).play(0); gsap.delayedCall(.3, () => $("[data-menu-link]").focus()); }
  else { lenis.start(); menuTl.timeScale(1.6).reverse(); }
}
toggle.addEventListener("click", () => setMenu(!menuOpen));
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && menuOpen) { setMenu(false); toggle.focus(); }
  // mantém o foco dentro do menu aberto (toggle + links)
  if (e.key === "Tab" && menuOpen) {
    const f = [toggle, ...$$("a, button", menu)];
    const i = f.indexOf(document.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
  }
});
addEventListener("resize", () => { if (menuOpen && !isMobile()) setMenu(false); });

// links para outras páginas do site: DefaultLeave da referência (menu sobe, conteúdo some em .3 s) e navega
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href]");
  if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0 || a.target === "_blank") return;
  const url = new URL(a.href, location.href);
  if (url.origin !== location.origin || url.pathname === location.pathname) return;
  e.preventDefault();
  if (menuOpen) setMenu(false);
  try { sessionStorage.setItem("mb-nav", "1"); } catch {}
  if (reduced) { location.href = url.href; return; }
  lenis.stop();
  gsap.timeline({ defaults: { ease: "power1.inOut", duration: .3 }, onComplete: () => { location.href = url.href; } })
    .to(navItems, { yPercent: -300, ease: "reveal", duration: .6 }, 0)
    .to(["main", "footer"], { opacity: 0 }, 0);
});
addEventListener("pageshow", (e) => { if (e.persisted) location.reload(); });

// âncoras com rolagem suave (também fecha o menu)
$$('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => {
  const id = a.getAttribute("href");
  const el = id.length > 1 && $(id);
  if (!el) return;
  e.preventDefault();
  if (menuOpen) setMenu(false);
  scrollToEl(el, id === "#topo" ? { offset: 0 } : {});
  history.replaceState(null, "", id);
}));

/* ================= 01 HERO · LOADER (HomeLoader / SimpleLoader) ================= */
const hero = $("[data-hero]");
const heroMedia = $("[data-hero-media]");
const lines = $$(".hero__line");
const loaderWin = $("[data-loader-win]");
const loaderImgs = $$("img", loaderWin);
const logoA = $("[data-loader-a]");
const logoB = $("[data-loader-b]");

// [data-reveal="left"] começa em translate(105%), "right" em translate(-105%) (CSS inline da referência)
lines.forEach((l) => gsap.set(l, { xPercent: l.dataset.reveal === "left" ? 105 : -105 }));
const navHide = (i, el) => -(el.getBoundingClientRect().bottom + 12);
gsap.set(navItems, { y: navHide });
const heroTitle = $(".hero__title");
gsap.set("[data-hero-grad]", { scaleY: 0 });

function finishLoad() {
  document.body.classList.remove("is-loading");
  lenis.start();
  // divisões de linha (SplitText) só depois da fonte carregada, para quebrar como o layout final
  document.fonts.ready.then(() => { initScroll(); ScrollTrigger.refresh(); });
}

function fullLoader() {
  // janela: 4 passos (largura × altura em vh), 0,7 s cada, ease "main", atraso 0,55 + 0,2
  // y: atraso inicial calibrado pela comparação com a referência (reanimate, .reanimate/motion): logo separa aos ~0,3 s
  const o = 1.4, h = .7, y = .05, OPEN = 3.74;
  let unit = "vh";
  let W = [20 * o, 22 * o, 36.5 * o, 42 * o], H = [14.5 * o, 22 * o, 28 * o, 38 * o];
  if (innerWidth <= 479) { unit = "vw"; H = [14.5 * o, 22 * o, 45 * o, 60 * o]; }
  const vw = innerWidth / 100, vh = innerHeight / 100, U = unit === "vh" ? vh : vw;
  const lastW = W[3] * U, lastH = H[3] * U;
  const insetY = (innerHeight - lastH) / 2, insetX = (innerWidth - lastW) / 2;

  gsap.set([heroMedia, heroTitle], { clipPath: `inset(${insetY}px ${insetX}px)` , autoAlpha: 0 });
  gsap.set(loaderImgs[0], { opacity: 1 });

  // MOCHI. / BROTHERS se separam no eixo Y (bullet -100, proof +100)
  // HomeLoader da referência: no mobile a separação é mais curta (h - .3) e também desloca em x
  const mob = isMobile();
  gsap.to(logoA, { yPercent: mob ? -120 : -100, duration: mob ? h - .3 : h - .1, delay: y + .2, ease: "main" });
  gsap.to(logoB, { yPercent: mob ? 60 : 100, duration: mob ? h - .3 : h - .1, delay: y + .2, ease: "main" });
  gsap.to(logoA, { xPercent: mob ? 100 : 0, duration: h, delay: y + .2, ease: "main" });
  gsap.to(logoB, { xPercent: mob ? -100 : 0, duration: h, delay: y + .2, ease: "main" });

  const tl = gsap.timeline({ onComplete: finishLoad });
  W.forEach((w, i) => {
    tl.to(loaderWin, {
      width: `${w}${unit}`, height: `${H[i]}${unit}`, delay: y + .2, duration: h, ease: "main",
      onStart: () => loaderImgs.forEach((im, k) => im.classList.toggle("is-on", k === i)),
    }, i * h);
  });
  tl.set([heroMedia, heroTitle], { autoAlpha: 1 }, OPEN)
    .to([heroMedia, heroTitle], { clipPath: "inset(0px 0px)", duration: 1.3, ease: "reveal", onStart: () => document.body.classList.remove("is-loading") }, OPEN)
    .to(lines, { xPercent: 0, duration: 1.3, ease: "reveal" }, "<0.1")
    .to(navItems, { y: 0, duration: 1, ease: "reveal" }, "<")
    .to("[data-hero-grad]", { scaleY: 1, duration: 1, ease: "reveal" }, "<")
    .set(".loader", { autoAlpha: 0 })
    .set(heroTitle, { clearProps: "clipPath" });
}

function simpleLoader() {
  gsap.set([logoA, logoB, loaderWin], { autoAlpha: 0 });
  gsap.timeline({ onComplete: finishLoad })
    .fromTo([heroMedia, heroTitle], { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.3, ease: "reveal", onStart: () => document.body.classList.remove("is-loading") }, .6)
    .to(lines, { xPercent: 0, duration: 1.3, ease: "reveal" }, "<0.1")
    .to(navItems, { y: 0, duration: 1, ease: "reveal" }, "<")
    .to("[data-hero-grad]", { scaleY: 1, duration: 1, ease: "reveal" }, "<");
}



/* ================= ROLAGEM ================= */
function initScroll() {
  if (scrollInited) return; scrollInited = true;
  heroParallax();
  intro();
  descr();
  batch();
  featured();
  work();
  method();
  manifesto();
  footer();
  // header mobile: transparente sobre o hero, claro depois dele
  ScrollTrigger.create({
    trigger: hero, start: "bottom top+=65",
    onEnter: () => $("[data-header]").classList.add("is-solid"),
    onLeaveBack: () => $("[data-header]").classList.remove("is-solid"),
  });
}

// HeroParallax: scrub linear do topo do hero até o início da seção seguinte
function heroParallax() {
  if (reduced) return;
  const mm = gsap.matchMedia();
  mm.add("(min-width: 768px)", () => {
    const tl = gsap.timeline({ defaults: { ease: "none" } });
    tl.to(heroMedia, { y: "40vh", rotate: .01 }, 0)
      .to(lines[0], { x: "15vw" }, 0)
      .to(lines[1], { x: "4vw" }, 0)
      .to(lines[2], { x: "-8vw" }, 0)
      .to(lines[3], { x: "-5vw" }, 0);
    ScrollTrigger.create({ trigger: hero, start: "top top", end: "bottom top", scrub: true, animation: tl });
  });
}

// Intro: linhas sobem por trás da máscara + imagem abre do centro
function intro() {
  const sec = $("[data-intro]");
  const ls = $$("[data-reveal-line]", sec);
  const img = $("[data-intro-img]", sec);
  if (reduced) return;
  gsap.set(ls, { yPercent: 120 });
  gsap.set(img, { clipPath: "inset(50%)" });
  ScrollTrigger.create({
    trigger: sec, start: "top 45%",
    onEnter: () => {
      gsap.to(ls, { yPercent: 0, stagger: .1, duration: .8, ease: "power4.out" });
      gsap.to(img, { clipPath: "inset(0%)", duration: 1, ease: "slow-out" });
    },
  });
  ScrollTrigger.create({
    trigger: sec, start: "top 80%",
    onLeaveBack: () => { gsap.set(ls, { yPercent: 120 }); gsap.set(img, { clipPath: "inset(50%)" }); },
  });
}

// Title.descrAnimation: parágrafos divididos em linhas, opacity + yPercent 20, stagger .3, 1.2 s power2.inOut
function descr() {
  const items = $$("[data-split-descr]");
  if (reduced) return;
  const m = isMobile();
  items.forEach((el) => {
    const split = new SplitText(el, { type: "lines", linesClass: "descr-line" });
    const tl = gsap.timeline({ paused: true, defaults: { duration: m ? .6 : 1.2, ease: "power2.inOut", stagger: m ? .15 : .3 } })
      .fromTo(split.lines, { opacity: 0, yPercent: 20 }, { opacity: 1, yPercent: 0 });
    ScrollTrigger.create({ trigger: el, start: "top 80%", onEnter: () => tl.play() });
    ScrollTrigger.create({ trigger: el, start: "top bottom", onLeaveBack: () => tl.time(0).pause() });
  });
}

// Batch: opacity 0 → 1, .6 s power1, top 85%; volta a 0 quando sai por baixo
function batch() {
  const els = $$("[data-batch]");
  if (reduced) return;
  gsap.set(els, { opacity: 0 });
  els.forEach((el) => {
    ScrollTrigger.create({
      trigger: el, start: "top 85%",
      onEnter: () => gsap.to(el, { opacity: 1, duration: .6, ease: "power1" }),
    });
    ScrollTrigger.create({ trigger: el, start: "top bottom", onLeaveBack: () => gsap.set(el, { opacity: 0 }) });
  });
}

/* ================= 01.a MONOGRAMA → 03 CASES EM DESTAQUE (BScroll + BleedSlider) ================= */
function featured() {
  // Cases em destaque: o slider aparece direto (a transição do monograma M foi retirada a pedido)
  const sec = $("[data-featured]");
  const bs = bleedSlider();
  if (reduced) { bs.open(); return; } // sem troca automática
  ScrollTrigger.create({ trigger: sec, start: "top 70%", once: true, onEnter: () => { bs.open(); bs.start(); } });
}

/* ---------------- BleedSlider ---------------- */
function bleedSlider() {
  const wrap = $("[data-slider]");
  const slides = $$("[data-slide]", wrap);
  const dots = $$(".dot", wrap);
  const clients = $("[data-clients]", wrap);
  const activeNr = $("[data-slide-active]", wrap);
  const cta = $("[data-slider-cta]", wrap);
  const destinations = ["/cases/azevedo-beauty/", "/cases/koyfer/", "/cases/turbo-tintas/", "/cases/criativi-concept/"];
  let current = 0, z = 2, timer = null, changing = false, allow = false, running = false;
  let inTl = gsap.timeline(), outTl = gsap.timeline();

  // letras: começam deslocadas ±21vw no desktop e ±35vw no mobile (--x / --mob-x da referência)
  const LS = () => (isMobile() ? ".Lm" : ".L");
  const scatter = (slide) => {
    const L = $$(LS(), slide);
    const d = isMobile() ? 35 : 21;
    return L.map((el, i) => {
      if (i === 0) return `-${d}vw`;
      if (i === L.length - 1) return `${d}vw`;
      return gsap.utils.random([`-${d}vw`, `${d}vw`]);
    });
  };
  const lettersTo = (slide, open) => {
    const xs = scatter(slide);
    $$(LS(), slide).forEach((el, i) => gsap.to(el, { x: open ? 0 : xs[i], duration: .8, ease: "slow-out", overwrite: "auto" }));
  };
  // só o slide visível fica disponível para leitores de tela e teclado
  const a11y = (active) => slides.forEach((s) => { const on = s === active; s.toggleAttribute("inert", !on); s.setAttribute("aria-hidden", String(!on)); });

  slides[0].classList.add("is-active");
  a11y(slides[0]);
  if (!reduced) slides.forEach((s) => $$(LS(), s).forEach((el, i) => gsap.set(el, { x: scatter(s)[i] })));

  const animateOut = (el) => {
    outTl.kill();
    const xs = scatter(el);
    outTl = gsap.timeline()
      .add(() => $$(LS(), el).forEach((l, i) => gsap.to(l, { x: xs[i], duration: .8, ease: "slow-out" })), 0)
      .to($("img", el), { xPercent: -25, duration: 1.2, ease: "slow-out" }, 0)
      .set(el, { clearProps: "zIndex" }, 1.2)
      .call(() => { el.classList.remove("is-active", "is-out"); gsap.set($("img", el), { xPercent: 0 }); }, null, 1.2);
    el.classList.add("is-out");
  };
  const animateIn = (el) => {
    inTl.kill();
    const tags = $$(".slide__tag span, .slide__m-desc", el);
    inTl = gsap.timeline({ onStart: () => { el.classList.add("is-in"); }, onComplete: () => { el.classList.remove("is-in"); el.classList.add("is-active"); } })
      .set(el, { zIndex: ++z }, 0)
      .fromTo(el, { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.2, ease: "slow-out" }, 0)
      .fromTo($("img", el), { xPercent: 20 }, { xPercent: 0, duration: 1.2, ease: "slow-out" }, "<")
      .add(() => lettersTo(el, true), "<+=0.45")
      .call(() => { changing = false; }, null, "<+=0.8")
      .fromTo(tags, { yPercent: 25, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, stagger: { each: .1, from: "end" }, duration: .5 }, 0.65);
  };

  function change(i) {
    const prev = slides[current], next = slides[i];
    if (prev === next || changing) return;
    changing = true; current = i; resetTimer();
    dots.forEach((d, k) => { d.classList.toggle("is-active", k === i); d.setAttribute("aria-selected", String(k === i)); });
    activeNr.textContent = i + 1;
    cta.setAttribute("href", destinations[i]);
    a11y(next);
    animateOut(prev); animateIn(next);
    gsap.to(clients, { yPercent: -i * 25, duration: 1, ease: "slow-out" });
  }
  const nextSlide = () => { if (allow && !changing) change((current + 1) % slides.length); };
  function resetTimer() { clearInterval(timer); if (running) timer = setInterval(nextSlide, 4000); }

  dots.forEach((d, i) => d.addEventListener("click", () => change(i)));
  wrap.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") change((current + 1) % slides.length);
    if (e.key === "ArrowLeft") change((current - 1 + slides.length) % slides.length);
  });
  // pausa enquanto o cursor está no CTA (como a referência)
  cta.addEventListener("mouseenter", () => { allow = false; });
  cta.addEventListener("mouseleave", () => { allow = running; });
  // arrastar / swipe: limiar de 25 px (também sobre o link do slide no mobile; um toque continua sendo clique)
  let sx = null, swiped = false;
  wrap.addEventListener("pointerdown", (e) => { if (!e.target.closest("button")) { sx = e.clientX; swiped = false; } });
  addEventListener("pointerup", (e) => {
    if (sx === null) return;
    const d = sx - e.clientX; sx = null;
    if (Math.abs(d) > 25) swiped = true;
    if (d > 25) change((current + 1) % slides.length);
    else if (d < -25) change((current - 1 + slides.length) % slides.length);
  });
  wrap.addEventListener("click", (e) => { if (swiped) { e.preventDefault(); e.stopPropagation(); swiped = false; } }, true);
  // só roda quando visível
  const io = new IntersectionObserver(([en]) => { if (running) allow = en.isIntersecting; }, { threshold: .3 });
  io.observe(wrap);
  if (!reduced) { running = true; resetTimer(); running = false; }

  return {
    open: () => lettersTo(slides[current], true),
    close: () => lettersTo(slides[current], false),
    // como na referência: o intervalo de 4 s já corre desde a criação; a revelação só libera a troca no próximo tique
    start: () => { running = true; allow = true; if (!timer) resetTimer(); },
    stop: () => { running = false; allow = false; clearInterval(timer); timer = null; },
    reset: () => {},
  };
}

/* ================= 04 CASES E JORNADA (Work) ================= */
function work() {
  const sec = $("[data-work]");
  const items = $$("[data-work-item]", sec);
  const poster = $("[data-work-poster]", sec);
  const base = $("[data-poster-img]", poster);
  // um <img> por pôster distinto, empilhados; troca instantânea como na referência
  const imgs = {};
  items.forEach((it) => {
    const src = it.dataset.poster;
    if (imgs[src]) return;
    let im = base;
    if (src !== base.getAttribute("src")) {
      im = base.cloneNode();
      im.src = src;
      im.setAttribute("data-poster-img", "clone");
      poster.insertBefore(im, base.nextSibling);
    }
    imgs[src] = im;
  });
  const showPoster = (src) => {
    Object.entries(imgs).forEach(([k, im]) => { im.style.opacity = k === src ? 1 : 0; });
    poster.style.visibility = src ? "visible" : "hidden";
  };
  const setActive = (it) => {
    items.forEach((x) => x.classList.toggle("is-active", x === it));
    showPoster(it ? it.dataset.poster : null);
    // cases com foto própria (Koyfer, Criativi, Azevedo, Turbo Tintas): só a imagem, sem o símbolo
    $(".work__poster-mono", poster).style.display = it && it.hasAttribute("data-no-mono") ? "none" : "";
  };
  setActive(null);
  if (reduced) { setActive(items[5]); return; }

  items.forEach((it, i) => {
    // cada linha deriva ±5 % na horizontal com a rolagem (scrub)
    gsap.fromTo($("[data-work-inner]", it), { xPercent: 0 }, {
      xPercent: (i % 2 === 0 ? -1 : 1) * (isMobile() ? 2 : 5), ease: "none",
      scrollTrigger: { trigger: it, start: "top bottom", end: "bottom top", scrub: true },
    });
    // a linha que cruza 48 % da tela fica ativa
    const next = items[i + 1];
    ScrollTrigger.create({
      trigger: it, start: "top 48%",
      end: () => `+=${next ? next.offsetTop - it.offsetTop : it.offsetHeight}`,
      onEnter: () => setActive(it), onEnterBack: () => setActive(it),
    });
    $("a", it).addEventListener("focus", () => setActive(it));
  });
  ScrollTrigger.create({ trigger: items[0], start: "top 48%", onLeaveBack: () => setActive(null) });
  ScrollTrigger.create({
    trigger: items[items.length - 1], start: "bottom 48%",
    onLeave: () => setActive(null), onEnterBack: () => setActive(items[items.length - 1]),
  });
}

/* ================= 05 MÉTODO (títulos em máscara + carrossel arrastável) ================= */
function method() {
  const sec = $("[data-method]");
  const t = $$(".mt", sec);
  const car = $("[data-carousel]", sec);
  const track = $("[data-carousel-track]", sec);
  const cards = $$("[data-card]", sec);
  if (!reduced) {
    // Title split-lines: yPercent 110 → 0, stagger .1, 1.2 s "reveal", top 80%
    gsap.set(t, { yPercent: 110 });
    ScrollTrigger.create({ trigger: sec, start: "top 80%", once: true, onEnter: () => gsap.to(t, { yPercent: 0, stagger: .1, duration: 1.2, ease: "reveal" }) });
    // cartões: Batch (opacity .6 s power1, top 85%, stagger .1)
    gsap.set(cards, { opacity: 0 });
    ScrollTrigger.create({ trigger: car, start: "top 85%", onEnter: () => gsap.to(cards, { opacity: 1, stagger: .1, duration: .6, ease: "power1" }) });
    ScrollTrigger.create({ trigger: car, start: "top bottom", onLeaveBack: () => gsap.set(cards, { opacity: 0 }) });
  }

  // SmoothSlider: arrasto com inércia (lerp .1), trackpad horizontal e setas do teclado
  let target = 0, cur = 0, max = 0, down = false, sx = 0, st = 0, moved = 0;
  const clamp = (v) => Math.min(max, Math.max(0, v));
  const measure = () => { max = Math.max(0, track.scrollWidth + track.offsetLeft * 2 - car.clientWidth); target = clamp(target); };
  measure(); addEventListener("resize", measure);
  gsap.ticker.add(() => {
    cur += (target - cur) * .1;
    if (Math.abs(target - cur) < .05) cur = target;
    track.style.transform = `translate3d(${-cur}px,0,0)`;
  });
  car.addEventListener("pointerdown", (e) => { down = true; moved = 0; sx = e.clientX; st = target; car.classList.add("is-drag"); });
  addEventListener("pointermove", (e) => {
    if (!down) return;
    const d = sx - e.clientX;
    moved = Math.max(moved, Math.abs(d));
    target = clamp(st + d * (e.pointerType === "touch" ? 1.5 : 1));
  });
  addEventListener("pointerup", () => { down = false; car.classList.remove("is-drag"); });
  car.addEventListener("click", (e) => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  car.addEventListener("wheel", (e) => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); target = clamp(target + e.deltaX); }
  }, { passive: false });
  car.addEventListener("keydown", (e) => {
    const step = cards[0].offsetWidth + 20;
    if (e.key === "ArrowRight") { target = clamp(target + step); e.preventDefault(); }
    if (e.key === "ArrowLeft") { target = clamp(target - step); e.preventDefault(); }
  });
  cards.forEach((c) => c.addEventListener("focus", () => { target = clamp(c.offsetLeft - track.offsetLeft); }));
}

/* ================= 06 MANIFESTO (Locations) ================= */
function manifesto() {
  const sec = $("[data-manifesto]");
  const rows = isMobile() ? $("[data-manifesto-rows-m]", sec) : $("[data-manifesto-rows]", sec);
  const media = $("[data-manifesto-media]", sec);
  if (!reduced) {
    // parallax vertical em scrub linear; texto e foto em sentidos opostos (amplitude adaptada à altura da seção)
    const tl = gsap.timeline({ defaults: { ease: "none" } })
      .fromTo(rows, { y: "-8vw" }, { y: "8vw" }, 0)
      .fromTo(media, { y: "6vw" }, { y: "-6vw" }, 0);
    ScrollTrigger.create({ trigger: sec, start: "top bottom", end: "bottom top", scrub: true, animation: tl });
  }
  // hover: as outras linhas esmaecem (desktop)
  if (matchMedia("(hover: hover)").matches) {
    $$(".mr", rows).forEach((r) => {
      r.addEventListener("mouseenter", () => { rows.classList.add("has-hover"); r.classList.add("is-hover"); });
      r.addEventListener("mouseleave", () => { rows.classList.remove("has-hover"); r.classList.remove("is-hover"); });
    });
  }
}

/* ================= FOOTER ================= */
function footer() {
  const f = $("[data-footer]");
  if (reduced) return;
  const mm = gsap.matchMedia();
  mm.add("(min-width: 768px)", () => {
    // o conteúdo sobe por baixo da seção anterior (scrub linear)
    gsap.fromTo("[data-footer-inner]", { y: "-25vw" }, { y: 0, ease: "none", scrollTrigger: { trigger: f, start: "top bottom", end: "bottom bottom", scrub: true } });
    // MOCHI / BROTHERS se afastam até a composição do Figma; a frase sobe
    const tl = gsap.timeline()
      .fromTo("[data-f-left]", { xPercent: 51 }, { xPercent: 0, duration: 5, ease: "power1.out" }, 0)
      .fromTo("[data-f-right]", { xPercent: -50 }, { xPercent: 0, duration: 5, ease: "power1.out" }, 0)
      .fromTo("[data-f-tag]", { yPercent: 100, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 3, ease: "power1.out" }, 1);
    ScrollTrigger.create({ trigger: f, start: "top 70%", end: "bottom bottom", scrub: true, animation: tl });
  });
}

/* ---------------- boot ---------------- */
function boot() {
lenis.stop();
const seen = document.cookie.includes("mb_loaded=1");
document.cookie = `mb_loaded=1; max-age=${2 * 86400}; path=/`;
if (reduced || params.has("noloader")) {
  gsap.set(lines, { xPercent: 0 }); gsap.set(navItems, { y: 0 }); gsap.set("[data-hero-grad]", { scaleY: 1 });
  finishLoad();
} else if (seen && !params.has("fullloader")) simpleLoader();
else fullLoader();
}
boot();
