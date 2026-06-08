# Tesla Boutique Miami

Static marketing site for Tesla Boutique Miami (a service by Unlimited Wraps), an
XPEL exclusive dealer specializing in Tesla paint protection film, ceramic coating
and window tint in Doral and Miami, FL.

Built with an SEO + AEO ("answer engine optimization") architecture: one page per
Tesla model, per service, and per model+service combination, a bilingual (EN/ES)
mirror, an Updates/blog section, and structured data so search engines and AI
assistants can read and cite the business.

## Structure

```
index.html                 Home (EN)
legal.html                 Legal & trademark notice (hand-maintained, self-styled)
es/index.html              Home (ES) (hand-maintained)
models/                    Per-model pages (Model 3, Y, S, X, Cybertruck) + SEO combo page
services/                  Per-service pages (PPF, Colored PPF, Ceramic, Tint, Windshield, Correction)
news/                      Updates: index + article pages (EN)
es/                         Spanish mirror of models/, services/, news/
assets/css/style.css       Shared design system (colors, type, layout)
assets/js/main.js          Minimal JS (header scroll, mobile nav, FAQ accordion, scroll reveal)
assets/img/                Optimized images (.avif + .webp)
assets/img/cars/<model>/   Per-model car photo sets used by hero + model galleries
sitemap.xml robots.txt llms.txt humans.txt   Technical + AEO layer

_build/                    Generators + content (not part of the served site)
  site.py                  Builds all EN pages (home, models, services, projects, news + articles)
  build_es.py              Builds the ES sub-pages (imports site.py helpers)
  posts/<slug>.<lang>.html Article bodies, shared by the generator and the live pages
  optimize_images.py       Re-encode photos to AVIF + WebP
  serve.ps1                Local static preview server (Windows; no Node/Python needed)
```

Notes:
- `es/index.html` and `legal.html` are hand-maintained, not generated. Every other
  page is produced by the generators.
- News/blog articles are defined as metadata in the `POSTS` (site.py) and `POSTS_ES`
  (build_es.py) dicts; their body lives once in `_build/posts/<slug>.en.html` and
  `<slug>.es.html` and is read by both languages. Articles get a `BlogPosting` +
  `BreadcrumbList` JSON-LD and hreflang links automatically.
- Per-model car galleries and heroes read from `assets/img/cars/<model>/`; logos and
  shared/legacy photos stay in `assets/img/`.

## Development

```bash
python3 _build/site.py             # regenerate all EN pages
python3 _build/build_es.py         # regenerate all ES sub-pages
python3 _build/optimize_images.py  # re-encode photos to AVIF + WebP
```

Add new full-resolution photos to `_build/source_images/`, run the optimizer, then
reference them through the generator's `<picture>` / `bg_style` helpers (AVIF + WebP +
lazy-loaded `<img>`), so the site stays fast as the photo library grows. Image `alt`
text is generated automatically by `img_alt()` (unique per photo, EN/ES).

To add a new Updates article: drop `_build/posts/<slug>.en.html` and `<slug>.es.html`
(the body), add a metadata entry to `POSTS` / `POSTS_ES`, then rebuild. The Updates
index card, the article pages and the hreflang links are produced from there. Add the
two URLs to `sitemap.xml` (hand-maintained).

House style: no em/en dashes anywhere; relative links; no inline prices.

## Local preview (Windows, no toolchain)

`.claude/launch.json` + `_build/serve.ps1` run a static server on port 8099 for quick
visual checks when Node/Python are not installed.

## Deploy

Plain static site, runs from the repo root with relative links, so it works both on
GitHub Pages and standard hosting. Canonical, hreflang and Open Graph URLs point to
the production domain `https://teslaboutiquemiami.com`.
