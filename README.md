# Tesla Boutique Miami

Static marketing site for Tesla Boutique Miami (a service by Unlimited Wraps), an
XPEL exclusive dealer specializing in Tesla paint protection film, ceramic coating
and window tint in Doral and Miami, FL.

Built by [Index01](https://index01.net) with an SEO + AEO ("answer engine
optimization") architecture: one page per Tesla model, per service, and per
model+service combination, plus structured data so search engines and AI
assistants can read and cite the business.

## Structure

```
index.html                 Home (EN)
es/index.html              Home (ES)
models/                    Per-model pages (Model 3, Y, S, X, Cybertruck) + SEO combo pages
services/                  Per-service pages (PPF, Colored PPF, Ceramic, Tint, Windshield, Correction)
projects/                  Project archive + individual project pages
news/                      Tesla Boutique Updates
assets/css/style.css       Shared design system (colors, type, layout)
assets/js/main.js          Minimal JS (nav, FAQ accordion, scroll reveal)
assets/img/                Optimized images (.avif + .webp)
sitemap.xml robots.txt llms.txt humans.txt   Technical + AEO layer
_build/                    Dev tools (not part of the served site)
```

## Development

The HTML pages are generated from a single source of truth so the header, footer
and navigation stay identical everywhere and contain no em/en dashes.

```bash
python3 _build/site.py            # regenerate all HTML pages
python3 _build/optimize_images.py # re-encode photos to AVIF + WebP
```

Add new full-resolution photos to `_build/source_images/`, run the optimizer,
then reference them through the generator's `<picture>` helper (AVIF + WebP +
lazy-loaded `<img>`), so the site stays fast as the photo library grows.

## Deploy

This is a plain static site. It runs from the repo root with relative links, so it
works both on GitHub Pages (project subpath) and on standard hosting such as GoDaddy.
Canonical, hreflang and Open Graph URLs point to the production domain
`https://teslaboutiquemiami.com`.
