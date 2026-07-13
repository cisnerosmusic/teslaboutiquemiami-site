/* Tesla Boutique Miami — cookie consent + Meta Pixel.
   INACTIVE until you set PIXEL_ID below. When set, a consent banner appears and the
   Meta Pixel loads ONLY after the visitor accepts. window.tbmTrack(event) fires
   events only with consent. Bilingual (reads <html lang>). */
(function () {
  'use strict';

  /* === PASO 1: pega aquí tu Meta Pixel ID para activar (ej: '1234567890123456'). === */
  var PIXEL_ID = '';
  if (!PIXEL_ID) return; // sin ID: no hay banner ni seguimiento.

  var KEY = 'tbm_consent';
  var ES = (document.documentElement.lang || 'en').toLowerCase().indexOf('es') === 0;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  function loadPixel() {
    if (window._tbmPixel) return; window._tbmPixel = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  /* Global helper: fires an event only if the visitor granted consent. */
  window.tbmTrack = function (ev, params) {
    if (store.get(KEY) === 'granted' && window.fbq) { try { window.fbq('track', ev, params || {}); } catch (e) {} }
  };

  /* Track phone / email clicks as "Contact" (no-op until consent is granted). */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
    if (a) window.tbmTrack('Contact');
  }, true);

  var choice = store.get(KEY);
  if (choice === 'granted') { loadPixel(); return; }
  if (choice === 'denied') { return; }

  /* No choice yet: show the consent banner. */
  function decide(v) {
    store.set(KEY, v);
    if (v === 'granted') loadPixel();
    var b = document.getElementById('tbm-consent');
    if (b) b.parentNode.removeChild(b);
  }

  function render() {
    var css = '#tbm-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:99999;max-width:720px;margin:0 auto;background:#111;border:1px solid #232323;border-radius:12px;padding:15px 18px;display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;box-shadow:0 12px 44px rgba(0,0,0,.55);font-family:inherit}#tbm-consent p{margin:0;flex:1 1 240px;color:#cfd2da;font-size:.82rem;line-height:1.5}#tbm-consent a{color:#6f80e0;text-decoration:underline}#tbm-consent .tbm-b{display:flex;gap:10px;flex:0 0 auto}#tbm-consent button{cursor:pointer;border-radius:6px;padding:9px 16px;font:600 .78rem/1 inherit;letter-spacing:.02em;border:1px solid transparent}#tbm-consent .tbm-a{background:#2B3990;color:#fff}#tbm-consent .tbm-a:hover{background:#233079}#tbm-consent .tbm-d{background:transparent;color:#cfd2da;border-color:#333}#tbm-consent .tbm-d:hover{border-color:#666}';
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var priv = ES ? '/es/legal.html' : '/legal.html';
    var txt = ES
      ? 'Usamos cookies y el pixel de Meta para medir y mejorar nuestra publicidad. '
      : 'We use cookies and the Meta pixel to measure and improve our advertising. ';
    var el = document.createElement('div');
    el.id = 'tbm-consent';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', ES ? 'Consentimiento de cookies' : 'Cookie consent');
    el.innerHTML = '<p>' + txt + '<a href="' + priv + '">' + (ES ? 'Privacidad' : 'Privacy') + '</a></p>' +
      '<div class="tbm-b">' +
      '<button type="button" class="tbm-d">' + (ES ? 'Rechazar' : 'Decline') + '</button>' +
      '<button type="button" class="tbm-a">' + (ES ? 'Aceptar' : 'Accept') + '</button>' +
      '</div>';
    document.body.appendChild(el);
    el.querySelector('.tbm-a').addEventListener('click', function () { decide('granted'); });
    el.querySelector('.tbm-d').addEventListener('click', function () { decide('denied'); });
  }

  if (document.body) render();
  else window.addEventListener('DOMContentLoaded', render);
})();
