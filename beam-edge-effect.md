# `.beam-edge` — Rotating "flashlight" glass-edge glow (reusable card effect)

A slow, brand-colored light that sweeps around a card's border, as if someone behind a
pane of glass were circling a flashlight against the edge. It fades in once with a
cinematic ease, ~2 s after the card scrolls into view, then loops forever.

- **Self-contained**: drop the CSS + JS into any project, add one class to any card.
- **Performant**: animates only a custom angle property and opacity → GPU compositor, no layout/paint thrash.
- **Accessible**: fully disabled under `prefers-reduced-motion: reduce`.
- **Tunable per card** via CSS custom properties (speed, thickness, fade, colors) and a `data-beam-delay` attribute.

Browser support: needs CSS `@property` (Chrome/Edge 85+, Safari 16.4+, Firefox 128+) for the
sweep to animate. In older browsers the light shows as a soft static glow that still fades in
(graceful degradation). Mask requires the `-webkit-` prefixes included below.

---

## 1) CSS

```css
/* ========================================================================
   THEME: "Linterna" — rotating brand-colored glass-edge beam (reusable)
   Add class="beam-edge" to ANY card to opt in. A slow light sweeps the
   border, fading in once the card scrolls into view (JS adds .beam-on after
   data-beam-delay ms, default 2000), then loops. GPU-only (angle + opacity);
   honors prefers-reduced-motion.
   Per-card knobs (set inline style or in a rule):
     --beam-thickness  edge width    (default 1.5px)
     --beam-spin       sec / rev     (default 15s, very slow)
     --beam-fade       fade-in time  (default 1.8s)
     --beam-c1/c2/c3   arc colors    (brand indigo -> periwinkle)
   Start immediately with data-beam-delay="0".
   ======================================================================== */
@property --beam-angle { syntax: "<angle>"; initial-value: 0deg; inherits: false; }

.beam-edge {
    position: relative;
    isolation: isolate;
    --beam-thickness: 1.5px;
    --beam-spin: 15s;
    --beam-fade: 1.8s;
    --beam-c1: #2B3990;   /* arc edges  (brand indigo)     */
    --beam-c2: #6f80e0;   /* mid                            */
    --beam-c3: #93a2ec;   /* brightest point (periwinkle)   */
}
.beam-edge::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: var(--beam-thickness);
    background: conic-gradient(from var(--beam-angle),
        transparent 0deg,
        transparent 205deg,
        rgba(43, 57, 144, 0) 230deg,
        var(--beam-c1) 262deg,
        var(--beam-c2) 296deg,
        var(--beam-c3) 312deg,
        var(--beam-c2) 328deg,
        var(--beam-c1) 352deg,
        transparent 360deg);
    /* show only the border ring: outer box minus inner content box */
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    /* soft halo bleeding from the lit arc (the "flashlight" glow) */
    filter: drop-shadow(0 0 5px rgba(111, 128, 224, 0.45))
            drop-shadow(0 0 11px rgba(43, 57, 144, 0.35));
    opacity: 0;                 /* hidden until JS adds .beam-on */
    pointer-events: none;
    z-index: 0;
}
.beam-edge > * { position: relative; z-index: 1; }  /* keep content above the glow */

@media (prefers-reduced-motion: no-preference) {
    .beam-edge.beam-on::before {
        animation: beamFade var(--beam-fade) ease-out forwards,
                   beamSpin var(--beam-spin) linear infinite;
    }
}
@keyframes beamFade { from { opacity: 0; } to { opacity: 1; } }
@keyframes beamSpin { to { --beam-angle: 360deg; } }
```

---

## 2) JavaScript

```javascript
/* "Linterna" beam: one-shot trigger when a card scrolls into view.
   Any element with class .beam-edge gets the sweep, starting data-beam-delay ms
   after entering view (default 2000), once, then looping. */
(function () {
    var cards = document.querySelectorAll('.beam-edge');
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
```

---

## 3) HTML usage

Add the class to any card. The card should have a `border-radius` (the ring inherits it)
and benefits from a solid/dark background so the lit edge reads clearly.

```html
<!-- default: 15s/rev, 2s delay, brand colors -->
<div class="card beam-edge">…</div>

<!-- custom: slower, thicker, starts immediately, lighter peak color -->
<div class="card beam-edge"
     style="--beam-spin:22s; --beam-thickness:2px; --beam-c3:#b9c4f5;"
     data-beam-delay="0">…</div>
```

### Knobs
| Property / attr      | Default   | Effect                                        |
|----------------------|-----------|-----------------------------------------------|
| `--beam-spin`        | `15s`     | Seconds per full revolution (higher = slower) |
| `--beam-thickness`   | `1.5px`   | Width of the lit glass edge                   |
| `--beam-fade`        | `1.8s`    | Cinematic fade-in duration                    |
| `--beam-c1`          | `#2B3990` | Arc edge color (brand indigo)                 |
| `--beam-c2`          | `#6f80e0` | Arc mid color                                 |
| `--beam-c3`          | `#93a2ec` | Arc brightest point (brand periwinkle)        |
| `data-beam-delay`    | `2000`    | Milliseconds after in-view before it starts   |

---

## Notes for another AI agent integrating this

- The effect lives entirely in a `::before` pseudo-element masked to the border ring, so it
  never blocks clicks (`pointer-events:none`) and sits under the card content (`z-index`).
- Colors are the only brand-specific values. Swap `--beam-c1/c2/c3` (and the
  `rgba(43,57,144,…)` values inside the `conic-gradient` transparent stop and the
  `drop-shadow`) to match a different palette. Keep `c1` and `c3` as the same hue family for
  the "single light source" look.
- The bright arc spans roughly 205°→360° of the gradient; widen/narrow that window to make
  the flashlight beam broader or tighter.
- The 2-second delay and "trigger once on scroll-in" behavior are handled in JS, not CSS, so
  the animation starts when the user actually reaches the card.
- Always keep it subtle: only one ~90° arc is lit at a time, which is what makes it read as a
  moving light rather than a glowing border.
```
```
