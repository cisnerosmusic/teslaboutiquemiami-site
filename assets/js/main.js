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

/* Location map: copy buttons, directions zoom effect, tile fallback */
(function () {
  document.querySelectorAll('.map-copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-copy');
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(v).then(function () {
        var o = b.textContent;
        b.textContent = b.getAttribute('data-done') || 'Copied';
        b.classList.add('done');
        setTimeout(function () { b.textContent = o; b.classList.remove('done'); }, 1400);
      });
    });
  });
  var dir = document.querySelector('[data-directions]');
  if (dir) {
    dir.addEventListener('click', function () {
      var s = document.querySelector('.map-stage');
      if (s) { s.classList.add('zoom'); setTimeout(function () { s.classList.remove('zoom'); }, 1300); }
      window.open(dir.getAttribute('data-directions'), '_blank', 'noopener');
    });
  }
  var mi = document.querySelector('.map-img');
  if (mi) { mi.addEventListener('error', function () { mi.classList.add('failed'); }); }
})();
