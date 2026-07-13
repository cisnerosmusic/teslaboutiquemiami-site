/* Tesla Boutique Miami, shared interactions. Minimal JS for INP. */
(function () {
  'use strict';

  // Header background on scroll
  var header = document.getElementById('header');
  if (header) {
    var onScroll = function () {
      if (window.pageYOffset > 50) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
    };
    requestAnimationFrame(onScroll);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Smooth scroll for same-page anchors only
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      if (id.length < 2) return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (nav && nav.classList.contains('open')) nav.classList.remove('open');
      }
    });
  });

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.setAttribute('aria-expanded', 'false');
    q.addEventListener('click', function () {
      var item = q.closest('.faq-item');
      var isOpen = item.classList.toggle('open');
      q.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });

  // Reveal on scroll
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    if ('IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
      revealEls.forEach(function (el) { obs.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add('in'); });
    }
  }
})();

/* ========== CONTACT FORM ========== */
document.querySelectorAll('.cform').forEach(function (form) {
    var tsField = form.querySelector('input[name="ts"]');
    if (tsField) tsField.value = Date.now();

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var btn = form.querySelector('.cform-btn');
        var ok = form.querySelector('.cform-ok');
        var err = form.querySelector('.cform-err');
        ok.hidden = true;
        err.hidden = true;

        var phone = form.querySelector('input[name="phone"]').value.trim();
        var email = form.querySelector('input[name="email"]').value.trim();
        if (!phone && !email) {
            err.hidden = false;
            return;
        }

        btn.disabled = true;
        var datos = new URLSearchParams(new FormData(form));
        fetch(form.action, { method: 'POST', body: datos })
            .then(function (r) { return r.json(); })
            .then(function (d) {
                if (d && d.ok) {
                    form.reset();
                    if (tsField) tsField.value = Date.now();
                    ok.hidden = false;
                    if (window.tbmTrack) window.tbmTrack('Lead');
                } else {
                    err.hidden = false;
                }
            })
            .catch(function () { err.hidden = false; })
            .finally(function () { btn.disabled = false; });
    });
});
/* ========== HERO SLIDESHOW (crossfade) ========== */
(function () {
    var slides = document.querySelectorAll('.hero .hero-bg-image');
    if (slides.length < 2) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    // Hydrate deferred slide backgrounds only after first paint, so the LCP
    // (first slide) is not starved of bandwidth by the other slides.
    var hydrate = function () {
        slides.forEach(function (s) {
            if (s.dataset && s.dataset.bg) {
                s.setAttribute('style', s.dataset.bg);
                s.removeAttribute('data-bg');
            }
        });
    };
    if (document.readyState === 'complete') hydrate();
    else window.addEventListener('load', hydrate);
    var i = 0;
    setInterval(function () {
        slides[i].classList.remove('is-active');
        i = (i + 1) % slides.length;
        slides[i].classList.add('is-active');
    }, 7000);
})();
/* ========== "Linterna" beam theme: one-shot trigger when a card scrolls into view ========== */
/* Any element with class .beam-edge (and the contact card .cform-wrap) gets a slow,
   brand-colored light sweeping its border. Starts data-beam-delay ms after entering
   view (default 2000), once, then loops. */
(function () {
    var cards = document.querySelectorAll('.beam-edge, .cform-wrap');
    if (!cards.length) return;
    var light = function (el) {
        var d = parseInt(el.getAttribute('data-beam-delay'), 10);
        if (isNaN(d)) d = 2000;
        setTimeout(function () { el.classList.add('beam-on'); }, d);
    };
    if (!('IntersectionObserver' in window)) { cards.forEach(light); return; }
    var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) { obs.unobserve(entry.target); light(entry.target); }
        });
    }, { threshold: 0.35 });
    cards.forEach(function (el) { obs.observe(el); });
})();
