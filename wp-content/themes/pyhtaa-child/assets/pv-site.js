/* Pyhtää Water Cooperative – front-end behaviours for the Elementor blocks:
   menu drawer, scroll-to-top, quick-link cycling, scroll reveal and stagger. */
(function () {
  'use strict';
  var doc = document, body = doc.body, html = doc.documentElement;
  if (body.classList.contains('elementor-editor-active') || window.elementorFrontend && window.elementorFrontend.isEditMode && window.elementorFrontend.isEditMode()) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  html.classList.add('pv-js');

  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }
  function kids(el) {
    var inner = el.querySelector(':scope > .e-con-inner');
    return Array.prototype.slice.call((inner || el).children);
  }

  /* ---- Menu drawer ---- */
  var toggles = $$('.pv-menu-toggle .elementor-button');
  toggles.forEach(function (btn) {
    if (!btn.querySelector('.pv-burger')) {
      var b = doc.createElement('span');
      b.className = 'pv-burger'; b.setAttribute('aria-hidden', 'true');
      b.innerHTML = '<i></i><i></i><i></i>';
      (btn.querySelector('.elementor-button-content-wrapper') || btn).appendChild(b);
    }
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-expanded', 'false');
  });
  var drawer = doc.querySelector('.pv-drawer');
  if (drawer) { drawer.setAttribute('aria-label', 'Main menu'); drawer.setAttribute('aria-hidden', 'true'); }
  function setMenu(open) {
    body.classList.toggle('pv-menu-open', open);
    body.style.overflow = open ? 'hidden' : '';
    if (drawer) drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    toggles.forEach(function (btn) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var t = btn.querySelector('.elementor-button-text');
      if (t) { if (!t.dataset.pvLabel) t.dataset.pvLabel = t.textContent; t.textContent = open ? 'Close' : t.dataset.pvLabel; }
    });
    // staggered menu items: .15s + i*.05s when opening
    $$('.pv-drawer .hfe-nav-menu > li').forEach(function (li, i) {
      li.style.transitionDelay = open ? (0.15 + i * 0.05) + 's' : '0s';
    });
  }
  doc.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('.pv-menu-toggle .elementor-button')) { e.preventDefault(); setMenu(!body.classList.contains('pv-menu-open')); return; }
    if (t.closest('.pv-menu-close .elementor-button') || t.closest('.pv-overlay')) { e.preventDefault(); setMenu(false); return; }
    if (t.closest('.pv-drawer a[href]')) { setMenu(false); }
    if (t.closest('.pv-top-btn .elementor-button, .pv-totop-float .elementor-button')) { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && body.classList.contains('pv-menu-open')) setMenu(false); });

  /* ---- Floating scroll-to-top ---- */
  function onScroll() { body.classList.toggle('pv-show-top', window.scrollY > 500); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---- Quick links: cycle the active card every 2.2s, hover/focus takes over ---- */
  $$('.pv-quick-group').forEach(function (group) {
    var cards = $$('.pv-quick', group), active = 0, hovering = false;
    if (!cards.length) return;
    function paint() { cards.forEach(function (c, i) { c.classList.toggle('is-active', i === active); }); }
    cards.forEach(function (c, i) {
      function enter() { hovering = true; active = i; paint(); }
      function leave() { hovering = false; }
      c.addEventListener('mouseenter', enter); c.addEventListener('focusin', enter);
      c.addEventListener('mouseleave', leave); c.addEventListener('focusout', leave);
    });
    paint();
    if (!reduce) setInterval(function () { if (!hovering) { active = (active + 1) % cards.length; paint(); } }, 2200);
  });

  if (reduce || !('IntersectionObserver' in window)) return;

  /* ---- Stagger groups: children rise in one after another ---- */
  var so = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var items = kids(e.target);
      items.forEach(function (c) { c.style.opacity = '1'; c.style.transform = ''; });
      so.unobserve(e.target);
      setTimeout(function () { items.forEach(function (c) { c.style.transition = ''; c.style.transitionDelay = ''; c.style.opacity = ''; }); }, 2000);
    });
  }, { threshold: 0.3 });
  $$('.pv-stagger').forEach(function (g) {
    kids(g).forEach(function (c, i) {
      c.style.opacity = '0'; c.style.transform = 'translateY(40px) scale(.94)';
      c.style.transition = 'opacity .6s ease, transform .7s cubic-bezier(.2,.8,.2,1.2)';
      c.style.transitionDelay = (i * 0.18) + 's';
    });
    so.observe(g);
  });

  /* ---- Reveal: sections below the fold fade up once ---- */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.remove('pv-pre');
      io.unobserve(e.target);
    });
  }, { threshold: 0.12 });
  $$('.pv-reveal').forEach(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight * 0.9) return;
    el.classList.add('pv-pre');
    void el.offsetWidth;
    el.classList.add('pv-anim');
    io.observe(el);
  });
})();
