#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tesla Boutique Miami — static page generator (single source of truth).

Holds the shared chrome (head, header, footer, CTA) once and emits clean,
static HTML for every page. No em/en dashes anywhere. Every <img> is lazy +
async and served as AVIF with WebP fallback via <picture>.

Run:  python3 _build/site.py
Output: static .html files written into the site root (committed to git).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://teslaboutiquemiami.com"
PHONE_TEL = "7865056162"
PHONE_DISP = "(786) 505-6162"

# ---------------------------------------------------------------- icons
IC = {
    "ppf": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>',
    "color": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>',
    "ceramic": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>',
    "tint": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>',
    "windshield": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>',
    "correction": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>',
    "check": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>',
    "phone": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>',
}

def svg(path, cls="", w=None, h=None):
    attrs = f' class="{cls}"' if cls else ""
    wh = f' width="{w}" height="{h}"' if w else ""
    return f'<svg{attrs}{wh} fill="none" stroke="currentColor" viewBox="0 0 24 24">{path}</svg>'

# ---------------------------------------------------------------- nav data
MODELS_NAV = [
    ("model-3", "Model 3"), ("model-y", "Model Y"), ("model-s", "Model S"),
    ("model-x", "Model X"), ("cybertruck", "Cybertruck"),
]
SERVICES_NAV = [
    ("paint-protection-film", "Paint Protection Film"),
    ("colored-ppf", "Colored PPF"),
    ("ceramic-coating", "Ceramic Coating"),
    ("window-tint", "Window Tint"),
    ("windshield-protection", "Windshield Protection"),
    ("paint-correction", "Paint Correction"),
]

# ---------------------------------------------------------------- helpers
def pic(prefix, name, alt, w, h, eager=False):
    avif = f"{prefix}assets/img/{name}.avif"
    webp = f"{prefix}assets/img/{name}.webp"
    extra = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return (f'<picture><source srcset="{avif}" type="image/avif">'
            f'<source srcset="{webp}" type="image/webp">'
            f'<img src="{webp}" alt="{alt}" width="{w}" height="{h}" decoding="async"{extra}></picture>')

def bg_style(prefix, name):
    avif = f"{prefix}assets/img/{name}.avif"
    webp = f"{prefix}assets/img/{name}.webp"
    return (f"background-image:url('{webp}');"
            f"background-image:image-set(url('{avif}') type('image/avif'), url('{webp}') type('image/webp'));")

def chip(href, label):
    return f'<a class="link-chip" href="{href}">{label}</a>'

def faq_block(items):
    rows = "".join(
        f'<div class="faq-item"><button class="faq-q">{q}</button>'
        f'<div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in items)
    return (f'<section class="section section-alt"><div class="container">'
            f'<div class="section-header"><span class="section-tag">FAQ</span>'
            f'<h2 class="section-title">Common questions</h2></div>'
            f'<div class="faq-list">{rows}</div></div></section>')

def faq_ld(items):
    import json
    main = [{"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": main}, ensure_ascii=False)

def breadcrumb_ld(prefix, trail):
    import json
    items = []
    for i, (name, url) in enumerate(trail, 1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items}, ensure_ascii=False)

def packages_block(tag, title, desc, cards):
    out = []
    for c in cards:
        feats = "".join(f'<li>{svg(IC["check"])} {f}</li>' for f in c["items"])
        feat_cls = " featured" if c.get("featured") else ""
        btn = "btn-primary" if c.get("featured") else "btn-outline"
        out.append(
            f'<div class="package-card{feat_cls} reveal"><span class="package-badge">{c["badge"]}</span>'
            f'<h3>{c["name"]}</h3><p class="package-price"><strong>{c["price"]}</strong></p>'
            f'<ul>{feats}</ul><a href="tel:{PHONE_TEL}" class="btn {btn}">Get quote</a></div>')
    return (f'<section class="section" id="packages"><div class="container">'
            f'<div class="section-header"><span class="section-tag">{tag}</span>'
            f'<h2 class="section-title">{title}</h2><p class="section-desc">{desc}</p></div>'
            f'<div class="packages-grid">{"".join(out)}</div></div></section>')

def service_cards_block(tag, title, prefix, keys):
    from_cards = []
    for k in keys:
        sc = SERVICE_CARDS[k]
        from_cards.append(
            f'<div class="service-card reveal"><div class="service-icon">{svg(sc["icon"])}</div>'
            f'<h3>{sc["title"]}</h3><p>{sc["blurb"]}</p>'
            f'<a class="card-link" href="{prefix}services/{k}.html">{sc["cta"]} &rarr;</a></div>')
    return (f'<section class="section section-alt"><div class="container">'
            f'<div class="section-header"><span class="section-tag">{tag}</span>'
            f'<h2 class="section-title">{title}</h2></div>'
            f'<div class="services-grid">{"".join(from_cards)}</div></div></section>')

def spec_block(title, rows):
    trs = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows)
    return (f'<section class="section section-alt"><div class="container"><div class="prose">'
            f'<h2>{title}</h2><table class="spec-table">{trs}</table></div></div></section>')

def cta_block(title, desc):
    return (f'<section class="cta-section"><div class="container"><div class="cta-content">'
            f'<h2 class="cta-title">{title}</h2><p class="cta-desc">{desc}</p>'
            f'<div class="cta-buttons">'
            f'<a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{PHONE_DISP}</a>'
            f'<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Book via Unlimited Wraps</a>'
            f'</div></div></div></section>')

def related_block(tag, chips):
    return (f'<section class="section"><div class="container">'
            f'<div class="section-header left"><span class="section-tag">{tag}</span>'
            f'<h2 class="section-title">Keep exploring</h2></div>'
            f'<div class="link-cloud">{"".join(chips)}</div></div></section>')

def breadcrumbs_html(prefix, items):
    lis = []
    for label, href in items:
        if href:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{label}</li>')
    return (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>')

def page_hero(prefix, img, title_html, lead, ctas_html, crumbs_html=""):
    return (f'<section class="page-hero"><div class="page-hero-bg" style="{bg_style(prefix, img)}"></div>'
            f'<div class="container">{crumbs_html}<div class="page-hero-content">'
            f'<h1 class="page-title">{title_html}</h1><p class="page-lead">{lead}</p>'
            f'{ctas_html}</div></div></section>')

# ---------------------------------------------------------------- chrome
LOGO = ('<span class="logo-main"><span class="logo-tesla">Tesla</span> '
        '<span class="logo-boutique">Boutique</span> <span class="logo-miami">Miami</span></span>'
        '<span class="logo-sub">Powered by <strong>UnlimitedWraps</strong></span>'
        '<span class="logo-sub logo-xpel">XPEL Exclusive Dealer</span>')

def header(prefix, active=""):
    models_dd = "".join(
        f'<li><a href="{prefix}models/{s}.html">{l}</a></li>' for s, l in MODELS_NAV)
    services_dd = "".join(
        f'<li><a href="{prefix}services/{s}.html">{l}</a></li>' for s, l in SERVICES_NAV)
    def cur(key):
        return ' aria-current="page"' if active == key else ""
    return f'''<header class="header" id="header">
  <div class="container"><div class="header-inner">
    <a href="{prefix}index.html" class="logo" aria-label="Tesla Boutique Miami home">{LOGO}</a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      {svg('<path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>')}
    </button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary">
      <ul class="main-nav-links">
        <li class="has-dropdown"><a href="{prefix}index.html#models"{cur('models')}>Tesla Models</a>
          <ul class="dropdown">{models_dd}</ul></li>
        <li class="has-dropdown"><a href="{prefix}index.html#services"{cur('services')}>Services</a>
          <ul class="dropdown">{services_dd}</ul></li>
        <li><a href="{prefix}projects/index.html"{cur('projects')}>Projects</a></li>
        <li><a href="{prefix}news/index.html"{cur('news')}>Updates</a></li>
        <li><a href="{prefix}index.html#contact">Contact</a></li>
      </ul>
      <div class="lang-switch" aria-label="Language"><a href="#" aria-current="true">EN</a><a href="{prefix}es/index.html">ES</a></div>
    </nav>
    <div class="header-cta">
      <a href="tel:{PHONE_TEL}" class="header-phone">{svg(IC['phone'])}<span>{PHONE_DISP}</span></a>
      <a href="{prefix}index.html#contact" class="btn btn-primary">Book Now</a>
    </div>
  </div></div>
</header>'''

SOCIALS = (
    '<a href="https://www.instagram.com/unlimitedwraps" target="_blank" rel="noopener" class="footer-social" aria-label="Instagram"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>'
    '<a href="https://www.facebook.com/UnlimitedWraps" target="_blank" rel="noopener" class="footer-social" aria-label="Facebook"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/></svg></a>'
    '<a href="https://www.youtube.com/user/UnlimitedWraps" target="_blank" rel="noopener" class="footer-social" aria-label="YouTube"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg></a>'
)

def footer(prefix):
    models_li = "".join(f'<li><a href="{prefix}models/{s}.html">{l}</a></li>' for s, l in MODELS_NAV)
    services_li = "".join(f'<li><a href="{prefix}services/{s}.html">{l}</a></li>' for s, l in SERVICES_NAV[:5])
    return f'''<footer class="footer"><div class="container">
  <div class="footer-main">
    <div class="footer-brand">
      <div class="footer-logo"><span class="logo-tesla">Tesla</span> <span class="logo-boutique">Boutique</span> <span class="logo-miami">Miami</span></div>
      <p>Tesla only paint protection, ceramic coating and window tint in Doral and Miami. XPEL exclusive dealer.</p>
      <div class="footer-powered"><span>A service powered by </span><a href="https://www.unlimitedwraps.com" target="_blank" rel="noopener">Unlimited Wraps</a></div>
    </div>
    <div class="footer-links"><h3>Tesla Models</h3><ul>{models_li}</ul></div>
    <div class="footer-links"><h3>Services</h3><ul>{services_li}</ul></div>
    <div class="footer-links"><h3>Hours</h3><div class="footer-hours">
      <div class="footer-hours-row"><span class="footer-hours-day">Mon to Fri</span><span class="footer-hours-time">9:00 to 5:30</span></div>
      <div class="footer-hours-row"><span class="footer-hours-day">Saturday</span><span class="footer-hours-time">Closed</span></div>
      <div class="footer-hours-row"><span class="footer-hours-day">Sunday</span><span class="footer-hours-time">Closed</span></div>
    </div></div>
  </div>
  <div class="footer-bottom">
    <p class="footer-copyright">&copy; 2026 Tesla Boutique Miami, a service by Unlimited Wraps, Inc. &middot; <a href="{prefix}legal.html" class="footer-legal-link">Legal &amp; Trademark Notice</a></p>
    <div class="footer-socials">{SOCIALS}</div>
  </div>
</div></footer>'''

def doc(path, title, desc, body, active="", preload=None, extra_ld=None, depth=None):
    if depth is None:
        depth = path.count("/")
    prefix = "../" * depth
    canonical = DOMAIN + "/" + ("" if path == "index.html" else path)
    es_path = "es/" + path
    es_url = DOMAIN + "/" + ("es/" if path == "index.html" else es_path)
    preload_tag = ""
    if preload:
        preload_tag = (f'<link rel="preload" as="image" href="{prefix}assets/img/{preload}.webp" fetchpriority="high">')
    ld = ""
    for block in (extra_ld or []):
        ld += f'<script type="application/ld+json">{block}</script>\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="es" href="{es_url}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/{preload or 'model-s'}.webp">
<meta property="og:site_name" content="Tesla Boutique Miami">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
{preload_tag}
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{ld}</head>
<body>
{header(prefix, active)}
<main>
{body}
</main>
{footer(prefix)}
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>'''

# ---------------------------------------------------------------- service cards (reused on models + home)
SERVICE_CARDS = {
    "paint-protection-film": {"icon": IC["ppf"], "title": "Paint Protection Film",
        "blurb": "Invisible self-healing XPEL film against rock chips, scratches and road debris. Full-front, track and full-body coverage.", "cta": "Explore PPF"},
    "colored-ppf": {"icon": IC["color"], "title": "Colored PPF",
        "blurb": "Change your Tesla's color and protect the paint underneath, in gloss, satin and stealth finishes. Fully reversible.", "cta": "Explore Colored PPF"},
    "ceramic-coating": {"icon": IC["ceramic"], "title": "Ceramic Coating",
        "blurb": "XPEL Fusion Plus hydrophobic ceramic that deepens gloss and makes your Tesla far easier to keep clean.", "cta": "Explore Ceramic"},
    "window-tint": {"icon": IC["tint"], "title": "Window Tint",
        "blurb": "XPEL Prime XR Plus ceramic tint, up to 98% infrared heat rejection without changing your Tesla's look.", "cta": "Explore Tint"},
    "windshield-protection": {"icon": IC["windshield"], "title": "Windshield Protection",
        "blurb": "An optically clear film that helps shield Tesla's costly windshield from cracks and pitting.", "cta": "Explore Windshield"},
    "paint-correction": {"icon": IC["correction"], "title": "Paint Correction",
        "blurb": "Multi-stage polishing that removes swirls and restores a flawless finish before coating or film.", "cta": "Explore Correction"},
}

PKG = lambda badge, name, price, items, featured=False: {
    "badge": badge, "name": name, "price": price, "items": items, "featured": featured}

# ---------------------------------------------------------------- MODELS data
MODELS = {
  "model-3": {
    "name": "Model 3", "img": "tesla-model-3-ppf-doral",
    "lead": "The Model 3 is the Tesla that lives on the highway, which is exactly why its front end takes the most punishment. Here is how we keep a daily-driven Model 3 looking new in Miami.",
    "intro": ["As the most-driven Tesla on South Florida roads, the Model 3 racks up highway miles fast, and with them come rock chips on the hood and bumper plus a hot cabin under the Miami sun. The fix is targeted: paint protection film where impacts happen, ceramic window tint for heat, and an optional ceramic coating for gloss and easy washing.",
              "We use model-specific XPEL patterns cut for the Model 3, so coverage is precise with no lifted edges, and every install is registered to your VIN."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "packages": [
      PKG("Essential", "Front Protection", "Full-front PPF",
          ["Full hood &amp; fenders", "Front bumper &amp; mirrors", "Self-healing XPEL film", "10-year warranty"]),
      PKG("Most popular", "Daily Driver", "Full-front PPF + ceramic tint",
          ["Everything in Front Protection", "Ceramic tint, all glass", "Cooler cabin", "Cleaner look"], featured=True),
      PKG("Maximum", "Full Armor", "Full-body PPF + tint + coating",
          ["Every painted panel filmed", "Ceramic tint", "Fusion Plus coating", "Best resale protection"]),
    ],
    "specs": [("Best entry service", "Full-front PPF (hood, fenders, mirrors, bumper)"),
              ("Heat &amp; glare", "Ceramic window tint, all glass"),
              ("Gloss &amp; easy cleaning", "XPEL Fusion Plus ceramic coating"),
              ("Film", "Genuine XPEL, model-specific patterns, warranty to VIN"),
              ("Location", "Doral, FL, serving all of Miami-Dade")],
    "faqs": [("How much does it cost to protect a Tesla Model 3 in Miami?",
              "It depends on coverage. Full-front PPF, ceramic tint and ceramic coating are separate services you can combine. Call (786) 505-6162 for a Model 3 quote."),
             ("Is PPF worth it on a Model 3?",
              "Yes. The Model 3 spends most of its life on the highway where rock chips happen, and its factory paint is thin. Full-front PPF protects the areas that take the most impacts."),
             ("Can you tint a Model 3 in Miami?",
              "Yes, with XPEL Prime XR Plus ceramic film that rejects up to 98% of infrared heat, a big comfort upgrade in the Miami sun.")],
  },
  "model-y": {
    "name": "Model Y", "img": "tesla-model-y-window-tinting",
    "lead": "The Model Y is the Tesla we protect most. Here is exactly how we shield its paint, glass roof and finish from Miami roads, sun and resale wear.",
    "intro": ["The Tesla Model Y spends its life on I-95, the Palmetto and the Turnpike, exactly where sand and gravel chip a soft factory clear coat. Add relentless UV and afternoon heat, and an unprotected Model Y starts showing chips on the hood, swirls in the paint, and a hot cabin under the panoramic glass roof.",
              "Our approach: paint protection film where impacts happen, ceramic coating for gloss and easy cleaning, and ceramic window tint to keep the heat out. Every service uses model-specific XPEL patterns cut for the Model Y."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "packages": [
      PKG("Essential", "Front Protection", "Full-front PPF",
          ["Full hood &amp; fenders", "Front bumper &amp; mirrors", "Self-healing XPEL film", "10-year warranty"]),
      PKG("Most popular", "Complete Comfort", "Full-front PPF + tint + coating",
          ["Everything in Front Protection", "Ceramic tint incl. glass roof", "Fusion Plus ceramic coating", "Cooler cabin, easy upkeep"], featured=True),
      PKG("Maximum", "Full Armor", "Full-body PPF + tint + coating",
          ["Every painted panel filmed", "Gloss or stealth finish", "Ceramic tint + coating", "Best resale protection"]),
    ],
    "specs": [("Best entry service", "Full-front PPF (hood, fenders, mirrors, bumper)"),
              ("Heat &amp; glare", "Ceramic window tint, including the panoramic glass roof"),
              ("Gloss &amp; easy cleaning", "XPEL Fusion Plus ceramic coating"),
              ("Color change", "Colored PPF in gloss, satin or stealth"),
              ("Film", "Genuine XPEL, model-specific patterns, warranty to VIN"),
              ("Location", "Doral, FL, serving all of Miami-Dade")],
    "faqs": [("How much does it cost to protect a Tesla Model Y in Miami?",
              "Pricing depends on coverage. Full-front PPF, ceramic window tint and ceramic coating are each separate services you can combine. Call (786) 505-6162 for a Model Y quote."),
             ("Which PPF coverage is best for a Model Y?",
              "For most owners we recommend at least a full-front package (full hood, fenders, mirrors and front bumper). For maximum resale protection, full-body PPF covers every painted panel."),
             ("Can you tint the Model Y glass roof?",
              "Yes. The panoramic glass roof can receive XPEL ceramic film to cut infrared heat and UV without changing the look."),
             ("Do you use genuine XPEL film on the Model Y?",
              "Always. As an XPEL exclusive dealer we install only genuine XPEL film and coatings, registered to your Model Y's VIN.")],
    "combo": ("tesla-model-y-ppf-miami.html", "Model Y PPF in Miami"),
  },
  "model-s": {
    "name": "Model S", "img": "tesla-model-s-ceramic-coating",
    "lead": "The Model S is Tesla's flagship, and it deserves flagship protection. Full-body film, ceramic coating and tint that keep a premium sedan immaculate.",
    "intro": ["A Model S owner is protecting a significant investment, so coverage tends to go deeper: full-body paint protection film to keep every panel flawless, a Fusion Plus ceramic coating for a liquid-gloss finish, and ceramic tint for comfort and UV protection.",
              "We treat the Model S like the flagship it is, with meticulous edge wraps and genuine XPEL materials registered to your VIN."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "packages": [
      PKG("Essential", "Front Protection", "Full-front PPF",
          ["Full hood &amp; fenders", "Front bumper &amp; mirrors", "Self-healing XPEL film", "10-year warranty"]),
      PKG("Most popular", "Flagship", "Full-front PPF + coating + tint",
          ["Full-front XPEL film", "Fusion Plus ceramic coating", "Ceramic tint, all glass", "Liquid-gloss finish"], featured=True),
      PKG("Maximum", "Full Armor", "Full-body PPF + coating + tint",
          ["Every painted panel filmed", "Ceramic coating over film", "Ceramic tint", "Best resale protection"]),
    ],
    "specs": [("Best for flagship owners", "Full-body PPF + ceramic coating"),
              ("Gloss", "XPEL Fusion Plus over paint and film"),
              ("Heat &amp; glare", "Ceramic window tint, all glass"),
              ("Film", "Genuine XPEL, warranty to VIN"),
              ("Location", "Doral, FL, serving all of Miami-Dade")],
    "faqs": [("Should I get full-body PPF on a Model S?",
              "For a flagship you plan to keep, yes. Full-body film keeps every panel chip-free and protects resale value far beyond the cost of repainting."),
             ("Can you ceramic coat a Model S over PPF?",
              "Yes. A Fusion Plus ceramic coating goes over both paint and film for a uniform, easy-clean, high-gloss finish."),
             ("How much to protect a Model S in Miami?",
              "It depends on coverage. Call (786) 505-6162 and we will build a package around how you use the car.")],
  },
  "model-x": {
    "name": "Model X", "img": "tesla-model-x-full-body-ppf",
    "lead": "Big surfaces, falcon-wing doors and a panoramic windshield. The Model X has more to protect, and we cover all of it with genuine XPEL.",
    "intro": ["The Model X has large body panels and unique falcon-wing doors, which means more painted surface exposed to chips and more edges to wrap correctly. Full-body or extended-front PPF is popular here, paired with ceramic tint for the big glass area and a ceramic coating for gloss.",
              "We pattern the Model X precisely, including the door edges most installers rush, and register every install to your VIN."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "packages": [
      PKG("Essential", "Front Protection", "Full-front PPF",
          ["Full hood &amp; fenders", "Front bumper &amp; mirrors", "Self-healing XPEL film", "10-year warranty"]),
      PKG("Most popular", "Family SUV", "Extended-front PPF + tint + coating",
          ["Full-front plus rocker panels", "Ceramic tint, large glass", "Fusion Plus coating", "Cooler cabin"], featured=True),
      PKG("Maximum", "Full Armor", "Full-body PPF + tint + coating",
          ["Every painted panel filmed", "Falcon-wing door edges", "Ceramic tint + coating", "Best resale protection"]),
    ],
    "specs": [("Best for big surfaces", "Extended-front or full-body PPF"),
              ("Heat &amp; glare", "Ceramic window tint, large glass area"),
              ("Gloss &amp; easy cleaning", "XPEL Fusion Plus ceramic coating"),
              ("Film", "Genuine XPEL, warranty to VIN"),
              ("Location", "Doral, FL, serving all of Miami-Dade")],
    "faqs": [("Do the falcon-wing doors need special PPF?",
              "Yes, the door edges and seams need careful pattern work so the film wraps cleanly and does not interfere with the door mechanism. We pattern them precisely."),
             ("Is full-body PPF worth it on a Model X?",
              "On a large, premium SUV that holds value, full-body film is a popular choice. It keeps every panel chip-free and protects resale."),
             ("Can you tint the large Model X glass?",
              "Yes, with XPEL Prime XR Plus ceramic film to cut heat and UV across the big glass area.")],
  },
  "cybertruck": {
    "name": "Cybertruck", "img": "tesla-cybertruck-ppf-miami",
    "lead": "Stainless steel, not paint. The Cybertruck needs a different playbook, and we have it: PPF to protect the finish and colored PPF to actually change it.",
    "intro": ["The Cybertruck is unlike any other Tesla because its body is bare stainless steel, not painted. That changes everything: there is no clear coat to chip, but the stainless scratches, smudges and shows fine marks. Paint protection film over the stainless keeps it pristine and far easier to clean, while colored PPF is the way to give a Cybertruck real color with full protection underneath.",
              "We film the Cybertruck's large flat panels with genuine XPEL, including satin and stealth options that suit its angular design."],
    "services": ["paint-protection-film", "colored-ppf", "window-tint"],
    "packages": [
      PKG("Essential", "Stainless Guard", "Full-front PPF",
          ["Front-facing panels filmed", "Anti-scratch protection", "Easier to clean", "10-year warranty"]),
      PKG("Most popular", "Full Stainless", "Full-body clear PPF",
          ["Every panel filmed", "Keeps stainless pristine", "Resists smudges &amp; marks", "Self-healing film"], featured=True),
      PKG("Color", "Colored Cybertruck", "Full-body colored PPF",
          ["Gloss, satin or stealth color", "Full impact protection", "Reversible", "Genuine XPEL"]),
    ],
    "specs": [("Body type", "Bare stainless steel, not painted"),
              ("Keep it pristine", "Full-body clear PPF over stainless"),
              ("Change the color", "Full-body colored PPF, reversible"),
              ("Heat &amp; glare", "Ceramic window tint"),
              ("Film", "Genuine XPEL, warranty to VIN"),
              ("Location", "Doral, FL, serving all of Miami-Dade")],
    "faqs": [("Does a Cybertruck need PPF if it has no paint?",
              "The stainless does not chip like paint, but it scratches and shows fingerprints and marks. Clear PPF keeps it pristine and much easier to clean."),
             ("Can you change the color of a Cybertruck?",
              "Yes. Colored PPF wraps the stainless in gloss, satin or stealth color while protecting it underneath, and it is fully reversible."),
             ("Do you film the whole Cybertruck?",
              "We can do full-front or full-body coverage. The large flat panels actually pattern well with genuine XPEL film.")],
  },
}

# ---------------------------------------------------------------- SERVICES data
SERVICES = {
  "paint-protection-film": {
    "name": "Paint Protection Film", "img": "tesla-model-3-ppf-doral",
    "h1": 'Tesla <span class="highlight">Paint Protection Film</span>',
    "lead": "Invisible, self-healing XPEL film that takes the rock chips and scratches so your Tesla's paint does not. The single best thing you can do to keep a Tesla looking new in Miami.",
    "sections": [
      ("What is paint protection film?",
       ["Paint protection film (PPF, or a clear bra) is a transparent, flexible urethane film bonded directly to your Tesla's painted surfaces. It absorbs impacts: gravel, sand, bug acid and minor abrasions hit the film instead of the paint. XPEL's self-healing top coat goes further, so fine swirl marks vanish with the warmth of the Miami sun.",
        "Unlike a coating, PPF has real physical thickness, so it is the only option that genuinely stops chips. On a Tesla, whose factory clear coat is famously soft, that difference is the whole point."]),
      ("Why Tesla owners choose PPF",
       ["<ul><li><strong>Stops rock chips</strong> on the hood, bumper and fenders.</li>"
        "<li><strong>Self-healing finish</strong> erases light swirls.</li>"
        "<li><strong>Preserves resale value</strong> by protecting factory paint.</li>"
        "<li><strong>Invisible</strong>, gloss film disappears.</li>"
        "<li><strong>Stain &amp; chemical resistant</strong> against bugs and water spots.</li></ul>"]),
      ("The technology and XPEL products we use",
       ["We install genuine <strong>XPEL Ultimate Plus</strong>, the reference self-healing PPF, and <strong>XPEL Stealth</strong> for a satin finish. Patterns are pre-cut for each Tesla model, then refined by hand so edges wrap cleanly. Every install is registered to your VIN for the full 10-year XPEL warranty."]),
    ],
    "options": ("Coverage options", "How much to protect?", [
      PKG("Entry", "Partial Front", "Highest-impact zones", ["Partial hood &amp; fenders", "Mirrors", "Front bumper"]),
      PKG("Most popular", "Full Front", "Stops ~90% of road impacts", ["Full hood &amp; fenders", "Full bumper &amp; mirrors", "Headlights"], featured=True),
      PKG("Maximum", "Full Body", "Every painted panel", ["Complete coverage", "Gloss or Stealth finish", "Best resale protection"]),
    ]),
    "faqs": [("What is paint protection film (PPF)?",
              "A clear, durable urethane film applied over your Tesla's paint. It absorbs rock chips and scratches, and XPEL's self-healing top coat makes light swirls disappear with heat."),
             ("Is PPF worth it on a Tesla?",
              "Yes. Tesla factory paint is relatively soft and chips easily on Miami highways. PPF preserves the finish and resale value, and is far cheaper than repainting panels."),
             ("How long does XPEL PPF last?",
              "Genuine XPEL Ultimate Plus carries a 10-year manufacturer warranty against yellowing, cracking and peeling when professionally installed."),
             ("Full-front or full-body PPF?",
              "Full-front covers the areas that take about 90% of road impacts and is most popular. Full-body films every painted panel for maximum protection.")],
  },
  "colored-ppf": {
    "name": "Colored PPF", "img": "tesla-cybertruck-red-and-black",
    "h1": 'Tesla <span class="highlight">Colored PPF</span>',
    "lead": "Change your Tesla's color and protect it at the same time. Colored PPF gives you gloss, satin or stealth finishes with full impact protection, and it is fully reversible.",
    "sections": [
      ("Color change that also protects",
       ["Colored PPF is paint protection film with pigment. You get a real color change in gloss, satin or matte stealth, plus the same self-healing chip protection as clear PPF. Because it is film, your factory paint stays untouched underneath, which protects resale value and lets you return the car to original whenever you want.",
        "It is the smart alternative to a respray or a cheap vinyl wrap: tougher than vinyl, reversible unlike paint, and protective rather than just cosmetic."]),
      ("Finishes and the XPEL products we use",
       ["We install genuine XPEL colored and stealth films in a range of factory-style and custom shades. On the Cybertruck especially, colored PPF is the cleanest way to add color to bare stainless while protecting it."]),
    ],
    "options": ("Popular finishes", "Choose your look", [
      PKG("Gloss", "Gloss Color", "Deep, wet-look color", ["Vivid color change", "Self-healing film", "Reversible"]),
      PKG("Most popular", "Satin / Stealth", "Matte factory-look finish", ["Satin or matte stealth", "Hides fine marks", "Full protection"], featured=True),
      PKG("Accents", "Color Accents", "Roof, mirrors, trim", ["Two-tone looks", "Blackout accents", "Precise patterns"]),
    ]),
    "faqs": [("Is colored PPF better than vinyl wrap?",
              "For most owners, yes. Colored PPF is thicker and self-healing, protects against chips rather than just covering paint, and tends to last longer than vinyl."),
             ("Will colored PPF damage my Tesla's paint?",
              "No. It protects the factory paint underneath and is designed to be removed cleanly, so you can return the car to original color."),
             ("Can you change a Cybertruck's color?",
              "Yes. Colored PPF is the ideal way to add gloss, satin or stealth color to the Cybertruck's bare stainless while protecting it.")],
  },
  "ceramic-coating": {
    "name": "Ceramic Coating", "img": "tesla-model-s-ceramic-coating",
    "h1": 'Tesla <span class="highlight">Ceramic Coating</span>',
    "lead": "A hydrophobic XPEL Fusion Plus ceramic layer that deepens gloss, repels water and dirt, and makes your Tesla dramatically easier to keep clean.",
    "sections": [
      ("What ceramic coating does",
       ["A ceramic coating is a liquid polymer that bonds to your Tesla's surface and cures into a hard, slick, hydrophobic layer. Water beads and sheets off, dirt and bugs struggle to stick, and the paint gains a deep, glassy gloss. It is not a chip barrier like PPF, it is a gloss-and-easy-clean upgrade, and the two work beautifully together.",
        "Ceramic also adds UV and chemical resistance, which matters under the Miami sun."]),
      ("XPEL Fusion Plus and how we apply it",
       ["We apply genuine <strong>XPEL Fusion Plus</strong> after a proper decontamination and, where needed, paint correction, so the coating locks in a flawless finish rather than sealing in swirls. It can be applied over bare paint and over PPF for a uniform look."]),
    ],
    "options": None,
    "faqs": [("Does ceramic coating replace PPF?",
              "No. Ceramic adds gloss and easy cleaning but does not stop rock chips. For impact protection you need PPF. Many owners do PPF on the front and ceramic everywhere."),
             ("How long does ceramic coating last?",
              "A professionally applied XPEL Fusion Plus coating lasts for years with proper maintenance, far longer than a wax or sealant."),
             ("Should I correct the paint first?",
              "Usually yes. Ceramic locks in whatever is underneath, so removing swirls with paint correction first gives the best, deepest result.")],
  },
  "window-tint": {
    "name": "Window Tint", "img": "tesla-model-y-window-tinting",
    "h1": 'Tesla <span class="highlight">Window Tint</span>',
    "lead": "XPEL Prime XR Plus ceramic tint rejects up to 98% of infrared heat and blocks UV, keeping your Tesla's cabin cool and comfortable in the Miami sun, without changing the look.",
    "sections": [
      ("Why ceramic tint, not cheap film",
       ["Cheap dyed tint fades to purple and blocks signals. <strong>XPEL Prime XR Plus</strong> is a ceramic film that rejects up to 98% of infrared heat and 99% of UV while staying signal-friendly and color-stable. In Miami, the difference in cabin comfort is dramatic, and it protects your interior from fading.",
        "On Teslas with a panoramic glass roof, adding ceramic film to the roof is one of the biggest comfort upgrades you can make."]),
      ("Coverage and the XPEL products we use",
       ["We tint side and rear glass, panoramic roofs and, where legal, the windshield, all with genuine XPEL ceramic film and a lifetime warranty against fading and bubbling."]),
    ],
    "options": None,
    "faqs": [("How much heat does ceramic tint block?",
              "XPEL Prime XR Plus rejects up to 98% of infrared heat, the part of sunlight you feel as warmth, which makes a real difference in the Miami sun."),
             ("Can you tint the Tesla glass roof?",
              "Yes. Adding ceramic film to a panoramic glass roof is one of the most effective comfort upgrades, cutting heat without changing the look."),
             ("Will tint affect my Tesla's signals or cameras?",
              "No. Ceramic film is non-metallic, so it does not interfere with GPS, cellular or Tesla's cameras and sensors.")],
  },
  "windshield-protection": {
    "name": "Windshield Protection", "img": "model-s",
    "h1": 'Tesla <span class="highlight">Windshield Protection</span>',
    "lead": "An optically clear protective film that helps shield your Tesla's expensive windshield from rock strikes, cracks and pitting, a smart, low-cost insurance policy.",
    "sections": [
      ("Why protect the windshield",
       ["Tesla windshields are large, raked and costly to replace, and on some models the replacement also involves recalibrating cameras. A windshield protection film is an optically clear layer that absorbs the impact of small rocks and debris, helping prevent the chips and cracks that send you to a glass shop.",
        "It is one of the most cost-effective protections you can add, especially for highway commuters."]),
      ("How it works",
       ["We apply a clear, durable film engineered for glass that maintains optical clarity and works with your wipers and sensors. It is replaceable, so a film that takes a hit can be swapped far more cheaply than the windshield itself."]),
    ],
    "options": None,
    "faqs": [("Does windshield film affect visibility?",
              "No. It is optically clear and designed to maintain full visibility and work normally with wipers, rain sensors and cameras."),
             ("Is it worth it on a Tesla?",
              "If you drive highways often, yes. Replacing a Tesla windshield is expensive and can require camera recalibration, so a replaceable protective film is smart insurance."),
             ("Can the film be replaced if it gets damaged?",
              "Yes, that is the point. A damaged film is swapped far more cheaply than replacing the windshield glass.")],
  },
  "paint-correction": {
    "name": "Paint Correction", "img": "tesla-model-s-ceramic-coating",
    "h1": 'Tesla <span class="highlight">Paint Correction</span>',
    "lead": "Multi-stage machine polishing that removes swirls, scratches and haze to restore a flawless, mirror-like finish, the right first step before any coating or film.",
    "sections": [
      ("What paint correction does",
       ["Paint correction is the careful, multi-stage polishing of your Tesla's clear coat to remove swirl marks, light scratches, water spots and oxidation. The result is a deep, glassy, defect-free finish that reflects cleanly instead of scattering light.",
        "It is also the essential first step before ceramic coating or PPF, because those lock in whatever is underneath. Correct first, then protect."]),
      ("Our process",
       ["We assess the paint, then use a measured, multi-stage polishing process to level defects without removing more clear coat than necessary. Done right, it transforms how a Tesla looks, especially darker colors."]),
    ],
    "options": None,
    "faqs": [("Do I need paint correction before ceramic or PPF?",
              "Usually yes. Coatings and film lock in the current condition, so correcting swirls first gives a far better, deeper final result."),
             ("Will correction thin my clear coat?",
              "Done professionally, we remove only what is needed to level defects, preserving as much clear coat as possible."),
             ("My new Tesla already has swirls, is that normal?",
              "Unfortunately yes, transport and dealer washing often introduce swirls. A single-stage correction usually brings a new Tesla to a true flawless finish.")],
  },
}

import json

# ---------------------------------------------------------------- page builders
def build_model(slug, d):
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                        ("Tesla Models", prefix + "index.html#models"), (d["name"], "")])
    ctas = (f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">Get a {d["name"]} quote</a>'
            f'<a href="#packages" class="btn btn-outline btn-lg">See packages</a></div>')
    hero = page_hero(prefix, d["img"], f'Tesla <span class="highlight">{d["name"]}</span> protection in Miami', d["lead"], ctas, crumbs)
    intro = "".join(f"<p>{p}</p>" for p in d["intro"])
    intro_sec = (f'<section class="section"><div class="container"><div class="prose">'
                 f'<h2>Protecting the {d["name"]} in South Florida</h2>{intro}</div></div></section>')
    svc = service_cards_block(f"Recommended for the {d['name']}", "Services we suggest", prefix, d["services"])
    pk = packages_block(f"{d['name']} packages", f"Popular ways to protect a {d['name']}",
                        "Starting points most owners choose. Every build is tailored, final pricing is confirmed on a quick call or visit.", d["packages"])
    sp = spec_block(f"{d['name']} protection at a glance", d["specs"])
    fq = faq_block(d["faqs"])
    chips = []
    if d.get("combo"):
        chips.append(chip(d["combo"][0], d["combo"][1]))
    chips += [chip(prefix + "services/window-tint.html", "Tesla window tint"),
              chip(prefix + "services/ceramic-coating.html", "Tesla ceramic coating"),
              chip(prefix + "projects/index.html", f"See {d['name']} projects")]
    rel = related_block("Related", chips)
    cta = cta_block(f"Protect your {d['name']}", f"Tell us your color and how you drive, and we will recommend the right PPF, tint and ceramic combination for your {d['name']}.")
    body = hero + intro_sec + svc + pk + sp + fq + rel + cta
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Tesla Models", DOMAIN + "/#models"),
                                 (d["name"], f"{DOMAIN}/models/{slug}.html")]),
          faq_ld(d["faqs"])]
    title = f'Tesla {d["name"]} PPF, Ceramic Coating &amp; Window Tint in Miami | Tesla Boutique Miami'
    desc = f'Protect your Tesla {d["name"]} in Miami and Doral: XPEL paint protection film, ceramic coating and ceramic window tint. Packages, projects and FAQs. Call (786) 505-6162.'
    return doc(f"models/{slug}.html", title, desc, body, active="models", preload=d["img"], extra_ld=ld)

def build_service(slug, d):
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                        ("Services", prefix + "index.html#services"), (d["name"], "")])
    ctas = (f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">Get a quote</a>'
            f'<a href="#packages" class="btn btn-outline btn-lg">Learn more</a></div>') if d.get("options") else \
           (f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">Get a quote</a></div>')
    hero = page_hero(prefix, d["img"], d["h1"], d["lead"], ctas, crumbs)
    secs = ""
    for h2, paras in d["sections"]:
        body_inner = "".join(p if p.lstrip().startswith("<ul") else f"<p>{p}</p>" for p in paras)
        secs += f'<section class="section"><div class="container"><div class="prose"><h2>{h2}</h2>{body_inner}</div></div></section>'
    opts = ""
    if d.get("options"):
        tag, title, cards = d["options"]
        opts = packages_block(tag, title, "Every build is tailored, final pricing is confirmed on a quick call or visit.", cards)
    bymodel = ('<section class="section section-alt"><div class="container">'
               '<div class="section-header left"><span class="section-tag">By Tesla model</span>'
               '<h2 class="section-title">Pick your Tesla</h2></div><div class="link-cloud">'
               + "".join(chip(prefix + f"models/{s}.html", f"{l} {d['name'].split()[0] if False else ''}".strip() or l) for s, l in MODELS_NAV)
               + "</div></div></section>")
    fq = faq_block(d["faqs"])
    cta = cta_block(f"Ready for {d['name']}?", "Tell us your Tesla and what you are after, and we will give you a clear quote and timeline.")
    body = hero + secs + opts + bymodel + fq + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service",
        "name": f"Tesla {d['name']}", "serviceType": d["name"], "brand": {"@type": "Brand", "name": "XPEL"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162",
                     "url": DOMAIN + "/", "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave",
                     "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"}},
        "areaServed": [{"@type": "City", "name": "Miami"}, {"@type": "City", "name": "Doral"}],
        "description": d["lead"]}, ensure_ascii=False)
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Services", DOMAIN + "/#services"),
                                 (d["name"], f"{DOMAIN}/services/{slug}.html")]), service_ld, faq_ld(d["faqs"])]
    title = f'Tesla {d["name"]} in Miami &amp; Doral | XPEL | Tesla Boutique Miami'
    desc = d["lead"]
    return doc(f"services/{slug}.html", title, desc, body, active="services", preload=d["img"], extra_ld=ld)

def build_combo():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                        ("Model Y", prefix + "models/model-y.html"), ("Model Y PPF in Miami", "")])
    ctas = f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">Get a Model Y PPF quote</a></div>'
    hero = page_hero(prefix, "tesla-model-y-window-tinting", 'Tesla Model Y <span class="highlight">PPF</span> in Miami',
        "Genuine XPEL paint protection film for the Model Y, installed in our Doral shop and serving all of Miami-Dade. Full-front to full-body coverage, self-healing, with a 10-year warranty.", ctas, crumbs)
    prose = ('<section class="section"><div class="container"><div class="prose">'
             '<h2>The right PPF for a Model Y in Miami</h2>'
             '<p>Miami highways are tough on a Model Y. Between construction sand on the Palmetto and gravel on I-95, the hood and front bumper take constant fire, and Tesla\'s soft factory paint chips fast. Paint protection film is the fix: a clear, self-healing XPEL layer that takes the hits so your paint stays flawless.</p>'
             '<p>For the Model Y specifically, we cut patterns to the exact panels: full hood, fenders, mirror caps and the deep front bumper that catches the most debris. Owners keeping the car long term often extend coverage to the full body.</p>'
             '<h3>Most-requested Model Y PPF in Miami</h3><ul>'
             '<li><strong>Full-front:</strong> hood, fenders, mirrors, bumper, headlights.</li>'
             '<li><strong>Track package:</strong> full-front plus rockers and rear-arch impact zones.</li>'
             '<li><strong>Full-body:</strong> every painted panel, optionally in XPEL Stealth satin.</li></ul>'
             '<p>Want the broader picture? See the full <a href="model-y.html">Tesla Model Y protection guide</a> or the <a href="../services/paint-protection-film.html">PPF service overview</a>.</p>'
             '</div></div></section>')
    rel = related_block("Nearby &amp; related", [chip("model-y.html", "Model Y window tint Miami"),
        chip("model-3.html", "Model 3 PPF Miami"), chip("../projects/index.html", "Model Y PPF projects"),
        chip("../services/paint-protection-film.html", "About XPEL PPF")])
    cta = cta_block("Get your Model Y filmed", "Quick quote for full-front or full-body PPF on your Model Y.")
    body = hero + prose + rel + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service",
        "name": "Tesla Model Y Paint Protection Film (PPF) in Miami", "serviceType": "Paint Protection Film installation",
        "brand": {"@type": "Brand", "name": "XPEL"}, "audience": {"@type": "Audience", "name": "Tesla Model Y owners"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162", "url": DOMAIN + "/"},
        "areaServed": {"@type": "City", "name": "Miami"},
        "description": "XPEL self-healing paint protection film installed on the Tesla Model Y in Miami and Doral, FL."}, ensure_ascii=False)
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Model Y", DOMAIN + "/models/model-y.html"),
                                 ("Model Y PPF in Miami", DOMAIN + "/models/tesla-model-y-ppf-miami.html")]), service_ld]
    title = "Tesla Model Y PPF in Miami | Full-Front &amp; Full-Body XPEL | Tesla Boutique Miami"
    desc = "Paint protection film (PPF) for the Tesla Model Y in Miami and Doral. XPEL self-healing film, full-front and full-body, 10-year warranty. Call (786) 505-6162."
    return doc("models/tesla-model-y-ppf-miami.html", title, desc, body, active="models", preload="tesla-model-y-window-tinting", extra_ld=ld)

def build_projects_index():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Projects", "")])
    hero = page_hero(prefix, "tesla-cybertruck-ppf-miami", 'Real Tesla <span class="highlight">projects</span>',
        "Every Tesla that comes through our Doral shop will be documented here: the work, the products, the result. This is the part no competitor can copy, because it is our actual cars.", "", crumbs)
    tiles = [
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-model-y-window-tinting", ["Model Y", "Full-Front PPF"],
         "Model Y, Full-Front PPF + Tint", "Sample project showing how each real install will be documented, with photos, services and products."),
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-model-3-ppf-doral", ["Model 3", "Full-Body PPF"],
         "Model 3, Full-Body PPF", "Coming soon. Real Model 3 projects will appear here as they are completed."),
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-cybertruck-red-and-black", ["Cybertruck", "Colored PPF"],
         "Cybertruck, Colored PPF", "Coming soon. Real Cybertruck projects will appear here as they are completed."),
    ]
    cards = ""
    for href, img, pills, h3, p in tiles:
        pillhtml = "".join(f'<span class="pill">{x}</span>' for x in pills)
        cards += (f'<a class="project-tile reveal" href="{href}">{pic(prefix, img, h3 + " Tesla project in Miami", 700, 438)}'
                  f'<div class="project-tile-body"><div class="tag-row">{pillhtml}</div>'
                  f'<h3>{h3}</h3><p>{p}</p><span class="card-link">View project &rarr;</span></div></a>')
    grid = (f'<section class="section"><div class="container">'
            f'<div class="section-header"><span class="section-tag">Our work</span><h2 class="section-title">Latest installs</h2></div>'
            f'<div class="project-list-grid">{cards}</div>'
            f'<p style="text-align:center;color:var(--gray);margin-top:40px;font-size:0.95rem">'
            f'New projects are added every week. This is a starter set, the archive grows with each Tesla we protect.</p>'
            f'</div></section>')
    cta = cta_block("Your Tesla could be next", "Book your install and we will document your project too.")
    body = hero + grid + cta
    ld = [json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Tesla Protection Projects", "url": DOMAIN + "/projects/index.html",
        "description": "Real Tesla PPF, ceramic coating and window tint projects by Tesla Boutique Miami in Doral, FL."}, ensure_ascii=False)]
    return doc("projects/index.html", "Tesla Projects, Real PPF, Ceramic &amp; Tint Installs in Miami | Tesla Boutique Miami",
               "Browse real Tesla protection projects from our Doral shop: PPF, ceramic coating and window tint on Model 3, Y, S, X and Cybertruck.",
               body, active="projects", preload="tesla-cybertruck-ppf-miami", extra_ld=ld)

def build_project_sample():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                        ("Projects", prefix + "projects/index.html"), ("Sample, Model Y Full-Front PPF", "")])
    hero = page_hero(prefix, "tesla-model-y-window-tinting",
        'Tesla Model Y<br><span class="highlight">Full-Front PPF + Ceramic Tint</span>',
        "Sample project. This is an illustrative example of how every real Tesla we protect will be documented, with original photos, services, products and install time. Real client projects replace these as work comes in.", "", crumbs)
    meta = ('<dl class="project-meta">'
            '<div><dt>Vehicle</dt><dd>Tesla Model Y</dd></div>'
            '<div><dt>Services</dt><dd>Full-Front PPF, Ceramic Tint</dd></div>'
            '<div><dt>Products</dt><dd>XPEL Ultimate Plus, Prime XR Plus</dd></div>'
            '<div><dt>Install time</dt><dd>2 days</dd></div>'
            '<div><dt>Location</dt><dd>Doral, FL</dd></div></dl>')
    gallery = (f'<div class="project-gallery">'
               f'{pic(prefix, "tesla-model-y-window-tinting", "Sample Tesla Model Y after full-front PPF and ceramic tint", 1200, 675).replace("<img ", "<img ").replace("><img", "><img")}'
               f'{pic(prefix, "model-s", "Sample Tesla Model Y PPF hood edge detail", 700, 525)}'
               f'{pic(prefix, "tesla-cybertruck-ppf-miami", "Sample Tesla in the Doral install booth", 700, 525)}'
               f'</div>')
    prose = (f'<section class="section"><div class="container"><div class="prose wide">{meta}'
             '<p style="background:rgba(43,57,144,0.12);border:1px solid rgba(43,57,144,0.4);padding:14px 18px;border-radius:8px;color:var(--gray-light)"><strong>Note:</strong> This is a sample layout, not a real client job. It exists so you can see exactly how documented projects will look once we start publishing real installs.</p>'
             '<h2>The project</h2>'
             '<p>A new Model Y comes in straight from the Tesla Doral dealer for protection before its first highway drive. Protecting a Tesla before it accumulates road miles means the paint underneath the film stays factory-perfect.</p>'
             '<p>We install XPEL Ultimate Plus full-front coverage: hood, both front fenders, the front bumper, mirror caps and headlights, with wrapped edges and no visible seams. Then XPEL Prime XR Plus ceramic tint on the side and rear glass plus the panoramic roof to cut the Miami heat.</p>'
             '<h2>Photos</h2>' + gallery +
             '<h2>Services performed</h2><ul>'
             '<li><a href="../services/paint-protection-film.html">Full-front paint protection film</a></li>'
             '<li><a href="../services/window-tint.html">Ceramic window tint</a>, side, rear and roof glass</li></ul>'
             '<h2>Products used</h2><ul>'
             '<li><strong>XPEL Ultimate Plus</strong>, self-healing clear PPF, 10-year warranty</li>'
             '<li><strong>XPEL Prime XR Plus</strong>, ceramic IR-rejecting window film</li></ul>'
             '<p style="margin-top:32px"><a href="../models/model-y.html" class="btn btn-outline">More on Model Y protection</a></p>'
             '</div></div></section>')
    cta = cta_block("Protect your Model Y like this", "New Tesla? Bring it in before the first road trip and keep the paint perfect.")
    body = hero + prose + cta
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Projects", DOMAIN + "/projects/index.html"),
            ("Sample Model Y Full-Front PPF", DOMAIN + "/projects/sample-tesla-model-y-full-front-ppf.html")]),
          json.dumps({"@context": "https://schema.org", "@type": "CreativeWork",
            "name": "Sample, Tesla Model Y Full-Front PPF + Ceramic Tint", "about": "Tesla Model Y paint protection film and window tint",
            "creator": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "url": DOMAIN + "/", "telephone": "+1-786-505-6162"},
            "locationCreated": {"@type": "Place", "name": "Doral, FL"},
            "description": "Illustrative sample of a documented Tesla Model Y full-front PPF and ceramic tint project."}, ensure_ascii=False)]
    return doc("projects/sample-tesla-model-y-full-front-ppf.html",
               "Sample Project, Tesla Model Y Full-Front PPF + Ceramic Tint | Tesla Boutique Miami",
               "Sample project layout showing how Tesla Boutique Miami documents each real install: photos, services, products and install time.",
               body, active="projects", preload="tesla-model-y-window-tinting", extra_ld=ld)

def build_news():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Updates", "")])
    hero = page_hero(prefix, "tesla-model-s-ceramic-coating", 'Tesla Boutique <span class="highlight">Updates</span>',
        "News and resources from Tesla Boutique Miami: fresh projects, XPEL product updates, and practical tips on caring for your Tesla's film, coating and tint. Updated regularly.", "", crumbs)
    posts = [
        ("Tesla", "How soon after buying a Tesla should you get PPF?", "The short answer: before the first long drive. Here is why protecting factory-fresh paint matters most."),
        ("Maintenance", "Caring for your PPF and ceramic coating in Miami", "Simple wash habits that keep XPEL film and Fusion Plus coating performing for years in the Florida heat."),
        ("XPEL", "Ultimate Plus vs Stealth: which PPF finish is right for you?", "Gloss or satin? A quick guide to choosing the XPEL film finish that suits your Tesla."),
        ("Maintenance", "Removing water spots from glass and paint", "What causes hard-water spotting in South Florida and how to remove it safely without damaging your finish."),
    ]
    cards = ""
    for i, (pill, h3, p) in enumerate(posts):
        if i == 0:
            meta = '<span class="post-date">Published &middot; May 2026</span>'
            link = '<a class="card-link" href="#">Read article &rarr;</a>'
        else:
            meta = ''
            link = '<span class="card-link">Coming soon</span>'
        cards += (f'<div class="project-tile reveal"><div class="project-tile-body">'
                  f'<div class="tag-row"><span class="pill">{pill}</span></div>{meta}'
                  f'<h3>{h3}</h3><p>{p}</p>{link}</div></div>')
    grid = (f'<section class="section"><div class="container">'
            f'<div class="section-header"><span class="section-tag">Tesla Boutique News</span>'
            f'<h2 class="section-title">Latest updates</h2>'
            f'<p class="section-desc">A preview of the topics we will cover. New posts are published as projects and products roll in.</p></div>'
            f'<div class="project-list-grid">{cards}</div></div></section>')
    cta = cta_block("Have a question about your Tesla?", "We are happy to help, whether you are a customer or just researching.")
    body = hero + grid + cta
    ld = [json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Tesla Boutique Updates", "url": DOMAIN + "/news/index.html",
        "description": "News, updates and Tesla care resources from Tesla Boutique Miami."}, ensure_ascii=False)]
    return doc("news/index.html", "Tesla Boutique Updates, News &amp; Tesla Care Tips | Tesla Boutique Miami",
               "Updates from Tesla Boutique Miami: new projects, XPEL product news and practical tips for caring for your Tesla's PPF, ceramic coating and tint.",
               body, active="news", preload="tesla-model-s-ceramic-coating", extra_ld=ld)

def build_home():
    prefix = ""
    hero = (f'<section class="hero"><div class="hero-bg"><div class="hero-bg-image" style="{bg_style(prefix, "model-s")}"></div></div>'
            f'<div class="container"><div class="hero-content">'
            f'<h1 class="hero-title"><span class="tesla">Tesla</span> Protection<br>Experts in <span class="highlight">Miami</span></h1>'
            f'<p class="hero-subtitle">Premium paint protection film, window tint and ceramic coating built exclusively for Tesla. Master XPEL installers with 15+ years protecting Model 3, Y, S, X and Cybertruck across Doral and Miami-Dade.</p>'
            f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{svg(IC["phone"], w=20, h=20)} Call Now</a>'
            f'<a href="#models" class="btn btn-outline btn-lg">Find My Tesla</a></div>'
            f'<div class="hero-stats">'
            f'<div class="hero-stat"><span class="hero-stat-value">15+</span><span class="hero-stat-label">Years Experience</span></div>'
            f'<div class="hero-stat"><span class="hero-stat-value">Tesla</span><span class="hero-stat-label">Only Specialists</span></div>'
            f'<div class="hero-stat"><span class="hero-stat-value">XPEL</span><span class="hero-stat-label">Exclusive Dealer</span></div>'
            f'</div></div></div></section>')
    banner = ('<section class="xpel-banner"><div class="container"><div class="xpel-banner-content">'
              '<div class="xpel-badge"><span class="xpel-banner-logo" role="img" aria-label="XPEL">XPEL</span>'
              '<span class="xpel-text"><strong>Exclusive Dealer</strong>, genuine XPEL products only</span></div>'
              '<div class="xpel-badge"><span class="xpel-text">10-Year Warranty on all PPF installations</span></div>'
              '</div></div></section>')
    # models grid
    mcards = ""
    for s, l in MODELS_NAV:
        d = MODELS[s]
        mcards += (f'<a class="model-card reveal" href="models/{s}.html">{pic(prefix, d["img"], f"Tesla {l} protection in Miami", 700, 525)}'
                   f'<div class="model-card-overlay"><h3>{l}</h3><span>PPF &middot; Tint &middot; Ceramic</span></div></a>')
    models_sec = (f'<section class="section" id="models"><div class="container">'
                  f'<div class="section-header"><span class="section-tag">Start with your Tesla</span>'
                  f'<h2 class="section-title">Pick your model</h2>'
                  f'<p class="section-desc">You do not think "I need PPF", you think "I have a Model Y". So every Tesla gets its own page, with the right packages, real projects and pricing guidance for that exact model.</p></div>'
                  f'<div class="models-grid">{mcards}</div></div></section>')
    # services grid (6)
    scards = ""
    for s, l in SERVICES_NAV:
        sc = SERVICE_CARDS[s]
        scards += (f'<div class="service-card reveal"><div class="service-icon">{svg(sc["icon"])}</div>'
                   f'<h3>{sc["title"]}</h3><p>{sc["blurb"]}</p>'
                   f'<a class="card-link" href="services/{s}.html">{sc["cta"]} &rarr;</a></div>')
    services_sec = (f'<section class="section section-alt" id="services"><div class="container">'
                    f'<div class="section-header"><span class="section-tag">What we do</span>'
                    f'<h2 class="section-title">Protection &amp; detailing for Tesla</h2>'
                    f'<p class="section-desc">Six specialized services, each with its own page explaining the technology, the XPEL products we use and exactly what you get.</p></div>'
                    f'<div class="services-grid">{scards}</div></div></section>')
    why = ('<section class="section section-grad"><div class="container">'
           '<div class="section-header"><span class="section-tag">Why Tesla Boutique Miami</span>'
           '<h2 class="section-title">Tesla only, XPEL certified</h2></div><div class="why-grid">'
           '<div class="why-item reveal"><span class="why-number">01</span><h3>XPEL Exclusive Dealer</h3><p>Authorized XPEL exclusive dealer with 15+ years installing PPF, ceramic and films on Tesla, exotic and luxury vehicles.</p></div>'
           '<div class="why-item reveal"><span class="why-number">02</span><h3>Tesla Specialists</h3><p>We know every panel, sensor and camera placement on Model 3, Y, S, X and Cybertruck. Patterns made for Tesla, not adapted.</p></div>'
           '<div class="why-item reveal"><span class="why-number">03</span><h3>Genuine XPEL Products</h3><p>Only authentic XPEL film and coatings, with full manufacturer warranty registered to your vehicle.</p></div>'
           '<div class="why-item reveal"><span class="why-number">04</span><h3>Real Project Documentation</h3><p>Every car we protect is photographed and documented, so you can see exactly the work that comes out of our shop.</p></div>'
           '</div></div></section>')
    gimgs = ["tesla-model-y-window-tinting", "tesla-model-3-ppf-doral",
             "tesla-model-x-full-body-ppf", "tesla-cybertruck-ppf-miami"]
    galleries = ""
    for i, g in enumerate(gimgs):
        inner = pic(prefix, g, "Recent Tesla project in Miami and Doral", 700, 525)
        if i == 0:
            galleries += f'<a class="gallery-item reveal" href="projects/sample-tesla-model-y-full-front-ppf.html">{inner}</a>'
        else:
            galleries += f'<div class="gallery-item reveal">{inner}</div>'
    work = (f'<section class="section section-alt"><div class="container">'
            f'<div class="section-header"><span class="section-tag">Our work</span>'
            f'<h2 class="section-title">Recent Tesla projects</h2>'
            f'<p class="section-desc">Real Teslas, real installs in our Doral shop. See the full archive in <a href="projects/index.html" style="color:var(--accent-text)">Projects</a>.</p></div>'
            f'<div class="gallery-grid">{galleries}</div></div></section>')
    areas = ('<section class="section"><div class="container">'
             '<div class="section-header"><span class="section-tag">Service areas</span>'
             '<h2 class="section-title">Serving Tesla owners across Miami-Dade</h2>'
             '<p class="section-desc">Based in Doral, protecting Teslas throughout South Florida.</p></div><div class="areas-grid">'
             '<div class="area-item reveal"><h3>Doral, FL</h3><p>Our home base and installation shop.</p></div>'
             '<div class="area-item reveal"><h3>Miami, FL</h3><p>Downtown, Brickell and Wynwood.</p></div>'
             '<div class="area-item reveal"><h3>Miami Beach</h3><p>South Beach, Mid-Beach and North Beach.</p></div>'
             '<div class="area-item reveal"><h3>Coral Gables</h3><p>Ceramic coating and PPF for the Gables.</p></div>'
             '<div class="area-item reveal"><h3>Aventura</h3><p>Aventura and Sunny Isles.</p></div>'
             '<div class="area-item reveal"><h3>Kendall</h3><p>Tesla PPF for the Kendall community.</p></div>'
             '</div></div></section>')
    pin_svg = svg('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>')
    clock_svg = svg('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>')
    phone_svg = svg(IC["phone"], w=20, h=20)
    contact = (f'<section class="cta-section" id="contact"><div class="container"><div class="cta-content">'
               f'<h2 class="cta-title">Ready to protect your Tesla?</h2>'
               f'<p class="cta-desc">Tell us your model and what you are after, and we will guide you to the right PPF, tint or ceramic package. Booking is currently handled through our parent shop, Unlimited Wraps.</p>'
               f'<div class="cta-buttons"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{phone_svg} {PHONE_DISP}</a>'
               f'<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Book via Unlimited Wraps</a></div>'
               f'<div class="cta-contact-info">'
               f'<div class="cta-contact-item">{pin_svg}<span>1835 NW 79th Ave, Doral, FL 33126</span></div>'
               f'<div class="cta-contact-item">{clock_svg}<span>Mon to Fri: 9AM to 5:30PM</span></div>'
               f'</div></div></div></section>')
    body = hero + banner + models_sec + services_sec + why + work + areas + contact
    local_ld = json.dumps({"@context": "https://schema.org", "@type": "AutoBodyShop",
        "@id": DOMAIN + "/#business", "name": "Tesla Boutique Miami",
        "alternateName": ["Tesla Boutique Miami (Unlimited Wraps)", "XPEL Tesla Doral"],
        "description": "Tesla only paint protection film, ceramic coating and window tint in Doral and Miami, FL. XPEL exclusive dealer powered by Unlimited Wraps, with 15+ years protecting Tesla, exotic and luxury vehicles.",
        "url": DOMAIN + "/", "telephone": "+1-786-505-6162", "image": DOMAIN + "/assets/img/model-s.webp",
        "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave", "addressLocality": "Doral",
                    "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 25.791474, "longitude": -80.323911},
        "areaServed": [{"@type": "City", "name": n} for n in ["Doral", "Miami", "Miami Beach", "Coral Gables", "Aventura", "Brickell", "Hialeah", "Kendall"]],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30"}],
        "priceRange": "$$$", "currenciesAccepted": "USD", "paymentAccepted": ["Cash", "Credit Card", "Debit Card"],
        "sameAs": ["https://www.unlimitedwraps.com", "https://www.instagram.com/unlimitedwraps",
                   "https://www.facebook.com/UnlimitedWraps", "https://www.youtube.com/user/UnlimitedWraps",
                   "https://www.tiktok.com/@unlimitedwraps"],
        "parentOrganization": {"@type": "Organization", "name": "Unlimited Wraps, Inc.", "url": "https://www.unlimitedwraps.com"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tesla " + l}} for _, l in SERVICES_NAV]},
        ensure_ascii=False)
    website_ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "@id": DOMAIN + "/#website",
        "url": DOMAIN + "/", "name": "Tesla Boutique Miami", "inLanguage": ["en", "es"],
        "publisher": {"@id": DOMAIN + "/#business"}}, ensure_ascii=False)
    title = "Tesla PPF, Ceramic Coating &amp; Window Tint in Miami &amp; Doral | Tesla Boutique Miami, XPEL"
    desc = "Tesla only paint protection film (PPF), ceramic coating and window tint in Doral and Miami, FL. XPEL exclusive dealer, 15+ years on Tesla. Model 3, Y, S, X and Cybertruck. Call (786) 505-6162."
    return doc("index.html", title, desc, body, active="", preload="model-s", extra_ld=[local_ld, website_ld])

def main():
    pages = {}
    pages["index.html"] = build_home()
    for slug, d in MODELS.items():
        pages[f"models/{slug}.html"] = build_model(slug, d)
    pages["models/tesla-model-y-ppf-miami.html"] = build_combo()
    for slug, d in SERVICES.items():
        pages[f"services/{slug}.html"] = build_service(slug, d)
    pages["projects/index.html"] = build_projects_index()
    pages["projects/sample-tesla-model-y-full-front-ppf.html"] = build_project_sample()
    pages["news/index.html"] = build_news()
    for path, html in pages.items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)
    print("\n%d pages generated." % len(pages))

if __name__ == "__main__":
    main()
