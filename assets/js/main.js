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
    onScroll();
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
                } else {
                    err.hidden = false;
                }
            })
            .catch(function () { err.hidden = false; })
            .finally(function () { btn.disabled = false; });
    });
});