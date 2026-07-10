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
CSS_VER = "20260709c"  # bump on every style.css change to bust browser cache

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

def img_alt(name, lang="en"):
    """Unique, SEO-friendly alt text derived from a car-photo basename (EN/ES)."""
    b = name.split("/")[-1]
    if "cybertruck" in b: model = "Cybertruck"
    elif "model-3" in b: model = "Model 3"
    elif "model-s" in b: model = "Model S"
    elif "model-x" in b: model = "Model X"
    elif "model-y" in b: model = "Model Y"
    else: model = "Tesla"
    detail = ("detalle" in b) or ("detail" in b)
    colEn = colEs = None
    for t, en, es in [("red","red","rojo"),("white","white","blanco"),("black","black","negro"),
                      ("metallic","metallic gray","gris metálico"),("grey","gray","gris"),("gray","gray","gris"),("blue","blue","azul")]:
        if t in b:
            colEn, colEs = en, es; break
    svcEn = svcEs = None
    if "window-tint" in b: svcEn, svcEs = "XPEL ceramic window tint", "polarizado cerámico XPEL"
    elif "ceramic" in b: svcEn, svcEs = "XPEL ceramic coating", "recubrimiento cerámico XPEL"
    elif "ppf" in b: svcEn, svcEs = "XPEL paint protection film (PPF)", "film de protección de pintura XPEL (PPF)"
    runs = []; cur = ""
    for ch in b:
        if ch.isdigit(): cur += ch
        elif cur: runs.append(cur); cur = ""
    if cur: runs.append(cur)
    idx = int(runs[-1]) if runs else len(b)
    techEn = ["XPEL paint protection film (PPF)", "self-healing XPEL PPF", "XPEL clear bra film", "genuine XPEL paint protection"]
    techEs = ["film de protección de pintura XPEL (PPF)", "PPF XPEL autorreparable", "film clear bra XPEL", "protección de pintura XPEL original"]
    loc = ["Doral, Miami", "Miami-Dade, FL", "Miami, FL"]
    tEn = svcEn or techEn[idx % len(techEn)]
    tEs = svcEs or techEs[idx % len(techEs)]
    L = loc[idx % len(loc)]
    if lang == "es":
        if detail: return f"Primer plano del {tEs} en un Tesla {model} en {L}"
        if colEs: return f"Tesla {model} en {colEs} con {tEs} en {L}"
        return f"Tesla {model} con {tEs} en {L}"
    if detail: return f"Close-up of {tEn} on a Tesla {model} in {L}"
    if colEn: return f"Tesla {model} in {colEn} with {tEn} in {L}"
    return f"Tesla {model} with {tEn} in {L}"

def product_badge(prefix, b):
    return (f'<div class="product-badge"><span class="product-badge-label">Genuine XPEL product</span>'
            f'<img class="product-badge-logo" src="{prefix}assets/img/{b["img"]}" alt="{b["alt"]}"></div>')

def model_gallery(prefix, name, names):
    items = "".join(
        f'<div class="gallery-item reveal"><picture>'
        f'<source srcset="{prefix}assets/img/{n}.avif" type="image/avif">'
        f'<source srcset="{prefix}assets/img/{n}.webp" type="image/webp">'
        f'<img src="{prefix}assets/img/{n}.webp" alt="{img_alt(n, "en")}" width="700" height="525" decoding="async" loading="lazy">'
        f'</picture></div>' for n in names)
    return (f'<section class="section"><div class="container">'
            f'<div class="section-header"><span class="section-tag">{name} gallery</span>'
            f'<h2 class="section-title">Real Tesla {name} work</h2></div>'
            f'<div class="gallery-grid">{items}</div></div></section>')

def media_showcase(prefix, s):
    cap = f'<figcaption>{s["caption"]}</figcaption>' if s.get("caption") else ""
    return (f'<section class="section"><div class="container"><figure class="media-showcase">'
            f'<img src="{prefix}assets/img/{s["img"]}" alt="{s["alt"]}" width="{s["w"]}" height="{s["h"]}" loading="lazy" decoding="async">'
            f'{cap}</figure></div></section>')

def process_block(prefix, tag, title, items):
    figs = ""
    for it in items:
        cap = f'<figcaption>{it["caption"]}</figcaption>' if it.get("caption") else ""
        figs += f'<figure class="{it["cls"]}">{pic(prefix, it["img"], it["alt"], it["w"], it["h"])}{cap}</figure>'
    return (f'<section class="section"><div class="container">'
            f'<div class="section-header"><span class="section-tag">{tag}</span>'
            f'<h2 class="section-title">{title}</h2></div>'
            f'<div class="process-row">{figs}</div></div></section>')

def page_hero(prefix, img, title_html, lead, ctas_html, crumbs_html=""):
    return (f'<section class="page-hero"><div class="page-hero-bg" style="{bg_style(prefix, img)}"></div>'
            f'<div class="container">{crumbs_html}<div class="page-hero-content">'
            f'<h1 class="page-title">{title_html}</h1><p class="page-lead">{lead}</p>'
            f'{ctas_html}</div></div></section>')

# ---------------------------------------------------------------- chrome
LOGO = ('<span class="logo-main"><span class="logo-tesla">Tesla</span> '
        '<span class="logo-boutique">Boutique</span> <span class="logo-miami">Miami</span></span>'
        '<span class="logo-sub">Powered by <a href="https://unlimitedwraps.com" class="logo-uw" target="_blank" rel="noopener"><strong>UnlimitedWraps</strong></a></span>'
        '<span class="logo-sub logo-xpel">XPEL Exclusive Dealer</span>')

def header(prefix, active=""):
    models_dd = "".join(
        f'<li><a href="{prefix}models/{s}.html">{l}</a></li>' for s, l in MODELS_NAV)
    services_dd = "".join(
        f'<li><a href="{prefix}services/{s}.html">{l}</a></li>' for s, l in SERVICES_NAV)
    area_cols = ""
    for c in COUNTIES:
        if not c["cities"]:
            continue
        city_lis = "".join(
            f'<li><a href="{prefix}service-area/{c["slug"]}/{cs}.html">{CITIES[cs]["name"]}</a></li>'
            for cs in c["cities"])
        area_cols += (f'<li class="mega-col"><a class="mega-head" href="{prefix}service-area/{c["slug"]}/index.html">{c["short"]}</a>'
                      f'<ul>{city_lis}</ul></li>')
    def cur(key):
        return ' aria-current="page"' if active == key else ""
    return f'''<header class="header" id="header">
  <div class="container"><div class="header-inner">
    <div class="logo"><a href="{prefix}index.html" class="logo-home-link" aria-label="Tesla Boutique Miami home"></a>{LOGO}</div>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      {svg('<path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>')}
    </button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary">
      <ul class="main-nav-links">
        <li class="has-dropdown"><a href="{prefix}index.html#models"{cur('models')}>Tesla Models</a>
          <ul class="dropdown">{models_dd}</ul></li>
        <li class="has-dropdown"><a href="{prefix}index.html#services"{cur('services')}>Services</a>
          <ul class="dropdown">{services_dd}</ul></li>
        <li class="has-dropdown"><a href="{prefix}service-area/index.html"{cur('area')}>Service Area</a>
          <ul class="dropdown dropdown-mega">{area_cols}</ul></li>
        <li><a href="{prefix}guides/index.html"{cur('guides')}>Guides</a></li>
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
    '<a href="https://www.instagram.com/teslaboutiquemiami" target="_blank" rel="noopener" class="footer-social" aria-label="Instagram"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>'
    '<a href="https://www.facebook.com/UnlimitedWraps" target="_blank" rel="noopener" class="footer-social" aria-label="Facebook"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/></svg></a>'
    '<a href="https://www.youtube.com/user/UnlimitedWraps" target="_blank" rel="noopener" class="footer-social" aria-label="YouTube"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg></a>'
    '<a href="https://www.tiktok.com/@unlimitedwraps" target="_blank" rel="noopener" class="footer-social" aria-label="TikTok"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a>'
    '<a href="https://www.threads.net/@unlimitedwraps" target="_blank" rel="noopener" class="footer-social" aria-label="Threads"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.785-1.548 7.158-1.85 1.812-4.094 2.628-7.277 2.65zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"/></svg></a>'
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
        preload_tag = (f'<link rel="preload" as="image" type="image/avif" href="{prefix}assets/img/{preload}.avif" fetchpriority="high">')
    ld = ""
    for block in (extra_ld or []):
        ld += f'<script type="application/ld+json">{block}</script>\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap"></noscript>
{preload_tag}
<link rel="stylesheet" href="{prefix}assets/css/style.css?v={CSS_VER}">
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
    "name": "Model 3", "img": "cars/model-3/model-3-blue-performance", "card": "tesla-model-3-ppf-doral",
    "gallery": ["cars/model-3/model-3-grey-2", "cars/model-3/model-3-detalle", "cars/model-3/model-3-grey", "cars/model-3/model-3-grey-3", "cars/model-3/model-3-grey-5", "cars/model-3/model-3-grey-6"],
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
    "name": "Model Y", "img": "cars/model-y/model-y-blue-studio", "card": "tesla-model-y-window-tinting",
    "gallery": ["cars/model-y/model-y-grey-2", "cars/model-y/model-y-grey-3", "cars/model-y/model-y-grey-1", "cars/model-y/model-y-3", "cars/model-y/model-y-1", "cars/model-y/model-y-2", "cars/model-y/model-y-detail-1", "cars/model-y/model-y-white-1", "cars/model-y/model-y-white-2", "cars/model-y/model-y-white-3"],
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
    "name": "Model S", "img": "cars/model-s/model-s-blue-studio", "card": "tesla-model-s-ceramic-coating",
    "gallery": ["cars/model-s/model-s-black-1", "cars/model-s/model-s-red-2", "cars/model-s/model-s-detalle", "cars/model-s/model-s-detalle-2", "cars/model-s/model-s-red", "cars/model-s/model-s-blue-1", "cars/model-s/model-s-blue-2", "cars/model-s/model-s-blue-3", "cars/model-s/model-s-blue-4"],
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
    "name": "Model X", "img": "cars/model-x/model-x-red-studio", "card": "cars/model-x/model-x-red-6",
    "gallery": ["cars/model-x/model-x-red-1", "cars/model-x/model-x-red-2", "cars/model-x/model-x-red-3", "cars/model-x/model-x-red-4", "cars/model-x/model-x-red-5", "cars/model-x/model-x-red-6"],
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
    "name": "Cybertruck", "img": "cars/cybertruck/cybertruck-1-black", "card": "tesla-cybertruck-ppf-miami",
    "gallery": ["cars/cybertruck/cybertruck-2-black", "cars/cybertruck/cybertruck-3-white", "cars/cybertruck/cybertruck-4-white", "cars/cybertruck/cybertruck-5-white", "cars/cybertruck/cybertruck-6-white", "cars/cybertruck/cybertruck-7-metallic", "cars/cybertruck/cybertruck-8-metallic", "cars/cybertruck/cybertruck-9-metallic", "cars/cybertruck/cybertruck-10-red", "cars/cybertruck/cybertruck-11-red", "cars/cybertruck/cybertruck-12-red"],
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
    "badge": {"img": "xpel-ultimate-plus.png", "alt": "XPEL Ultimate Plus paint protection film"},
    "process": ("Real PPF work in our Doral shop", "Paint protection film, applied by hand", [
      {"img": "tesla-model-y-ppf-hood", "w": 1600, "h": 901, "cls": "pr-wide",
       "alt": "Installer squeegeeing XPEL paint protection film across a Tesla Model Y hood in Doral",
       "caption": "Laying the film across the hood"},
      {"img": "tesla-model-y-ppf-edge", "w": 1600, "h": 766, "cls": "pr-wide",
       "alt": "Close-up of XPEL paint protection film being tucked into a Tesla Model Y panel edge",
       "caption": "Wrapping the film into the panel edges"},
    ]),
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
    "badge": {"img": "xpel-logo-solid.png", "alt": "Genuine XPEL film"},
    "showcase": {"img": "colored-ppf-samples.jpg", "w": 1600, "h": 1067,
                 "alt": "XPEL colored PPF color and finish samples", "caption": "Real XPEL color &amp; finish samples"},
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
    "badge": {"img": "xpel-fusion-plus.png", "alt": "XPEL Fusion Plus ceramic coating"},
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
    "badge": {"img": "xpel-prime-xr-plus.png", "alt": "XPEL Prime XR Plus window film"},
    "process": ("In our Doral shop", "How a Tesla tint install looks", [
      {"img": "tesla-window-tint-squeegee", "w": 940, "h": 1278, "cls": "pr-tall",
       "alt": "Installer squeegeeing XPEL ceramic window tint onto a Tesla side window in Doral",
       "caption": "Squeegeeing the ceramic film for a bubble-free finish"},
      {"img": "tesla-window-tint-result", "w": 1080, "h": 1575, "cls": "pr-tall",
       "alt": "Tesla side window with freshly installed XPEL ceramic window tint in Doral",
       "caption": "The finished tint, crisp and even"},
    ]),
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
    "name": "Windshield Protection", "img": "tesla-windshield-protection-install",
    "badge": {"img": "xpel-windshield-film.png", "alt": "XPEL windshield protection film"},
    "process": ("In our Doral shop", "How a Tesla windshield install looks", [
      {"img": "tesla-windshield-film-application", "w": 1080, "h": 706, "cls": "pr-wide",
       "alt": "Two installers positioning XPEL windshield protection film over a Tesla windshield in Doral",
       "caption": "Positioning the film before squeegeeing"},
      {"img": "tesla-windshield-film-detail", "w": 1080, "h": 1920, "cls": "pr-tall",
       "alt": "Close-up of XPEL windshield protection film being squeegeed onto a Tesla windshield",
       "caption": "Working out the slip solution for an optically clear finish"},
    ]),
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
              chip(prefix + "services/ceramic-coating.html", "Tesla ceramic coating")]
    rel = related_block("Related", chips)
    cta = cta_block(f"Protect your {d['name']}", f"Tell us your color and how you drive, and we will recommend the right PPF, tint and ceramic combination for your {d['name']}.")
    gallery = model_gallery(prefix, d["name"], d["gallery"]) if d.get("gallery") else ""
    body = hero + intro_sec + gallery + svc + pk + sp + fq + rel + cta
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
    nsec = len(d["sections"])
    for i, (h2, paras) in enumerate(d["sections"]):
        body_inner = "".join(p if p.lstrip().startswith("<ul") else f"<p>{p}</p>" for p in paras)
        badge = product_badge(prefix, d["badge"]) if (d.get("badge") and i == nsec - 1) else ""
        secs += f'<section class="section"><div class="container"><div class="prose"><h2>{h2}</h2>{badge}{body_inner}</div></div></section>'
    opts = ""
    if d.get("options"):
        tag, title, cards = d["options"]
        opts = packages_block(tag, title, "Every build is tailored, final pricing is confirmed on a quick call or visit.", cards)
    showcase = media_showcase(prefix, d["showcase"]) if d.get("showcase") else ""
    proc = process_block(prefix, *d["process"]) if d.get("process") else ""
    bymodel = ('<section class="section section-alt"><div class="container">'
               '<div class="section-header left"><span class="section-tag">By Tesla model</span>'
               '<h2 class="section-title">Pick your Tesla</h2></div><div class="link-cloud">'
               + "".join(chip(prefix + f"models/{s}.html", f"{l} {d['name'].split()[0] if False else ''}".strip() or l) for s, l in MODELS_NAV)
               + "</div></div></section>")
    fq = faq_block(d["faqs"])
    cta = cta_block(f"Ready for {d['name']}?", "Tell us your Tesla and what you are after, and we will give you a clear quote and timeline.")
    body = hero + secs + showcase + proc + opts + bymodel + fq + cta
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
        chip("model-3.html", "Model 3 PPF Miami"),
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

POSTS = {
  "xpel-care-products": {
    "pill": "XPEL", "date": "June 2026", "crumb": "XPEL care products", "img": "tesla-model-s-ceramic-coating",
    "title": "Beyond PPF: XPEL Tesla Care Products We Use | Tesla Boutique Miami",
    "desc": "The XPEL care products we use and sell, from Detail Spray and Ceramic Boost to PPF Cleaner and Iron Remover, to keep your Tesla protected between shop visits.",
    "h1": 'Beyond <span class="highlight">PPF</span>: the XPEL care products we use, and that you can use too',
    "card_title": "Beyond PPF: the XPEL care products we use, and that you can use too",
    "blurb": "The XPEL care products we use, sell and recommend, from Detail Spray and Ceramic Boost to PPF Cleaner and Iron Remover, to keep your Tesla looking new between visits.",
    "lead": "At Tesla Boutique we talk a lot about PPF, ceramic coating and windshield protection, because they are the foundation of protecting a Tesla. But protection does not end the day your car leaves the shop. XPEL also makes a line of care products we use every day in the shop, and that you can use at home to keep your Tesla looking like new. Here is what they are and what each one does.",
    "cta_title": "Not sure which product fits your Tesla?",
    "cta_desc": "Tell us what is installed on your car and we will point you to the right XPEL care products.",
    "sections": [
      ("Everyday care", [
        "<strong>XPEL Detail Spray.</strong> Our go-to for the final touch. It removes light dust, fingerprints and smudges without washing the whole car, leaving a streak-free finish. It is formulated to be safe on both paint and PPF, so the protected areas are covered too. It also works as a clay lubricant during decontamination. Shop tip: in direct sunlight, mist it onto the microfiber towel, not directly on the surface.",
        "<strong>XPEL Ceramic Boost.</strong> A silicon dioxide (SiO2) spray that repels water, dust and lint and restores gloss after every wash. It maintains an installed FUSION PLUS <a href=\"../services/ceramic-coating.html\">ceramic coating</a>, and also works on its own as a layer of protection and shine. It is the easy way to top up the hydrophobic effect between detailing sessions.",
        "<strong>XPEL Wash Solution.</strong> A pH-balanced shampoo for hand washing, safe for both PPF and ceramic coatings. Made so routine washing does not attack your protection layers."]),
      ("Deep cleaning and spots", [
        "<strong>XPEL PPF Cleaner.</strong> A cleaner made specifically for <a href=\"../services/paint-protection-film.html\">PPF</a>. It removes environmental deposits like tar, oil, hard water stains and bug acids, and restores the film's clear, freshly installed look. Keeping PPF clean is what preserves its protection and clarity over time.",
        "<strong>XPEL Water Spot Remover.</strong> Dissolves hard water spots (the kind left by sprinklers and tap water) in seconds. It is formulated to be safe on paint, XPEL films and FUSION PLUS coating, targeting mineral deposits without harming the surfaces. How to use: shake, spray, let it sit 30 to 45 seconds, then wipe with microfiber. Do not use in direct sunlight. For the full method on glass and paint, see our guide to <a href=\"removing-water-spots.html\">removing water spots</a>.",
        "<strong>XPEL Iron Remover.</strong> A specialized formula that helps lift iron oxide particles embedded in the paint and the PPF (they come from brake dust and the environment). Note: it has a strong scent, so use it in a well ventilated area or outdoors."]),
      ("Interior and glass", [
        "<strong>XPEL Interior Cleaner.</strong> Removes dirt and stains from various interior surfaces. Not for fabrics, and best tested on a hidden area first. Apply to the microfiber, clean, and wipe off the excess.",
        "<strong>XPEL Anti-Static Window Tint Cleaner.</strong> A cleaner for glass and <a href=\"../services/window-tint.html\">window film</a>, formulated so it will not damage the tint."]),
      ("Which one do you need?", [
        'We keep all of these in the shop, we use them on every Tesla that comes through our hands, and we sell them to anyone who wants to maintain their car at home. If you are not sure which one you need, ask us: we will tell you exactly what to use based on what is installed on your Tesla. For official spec sheets, the source is <a href="https://www.xpel.com" target="_blank" rel="noopener">xpel.com</a>.']),
    ],
  },
  "when-to-get-ppf-new-tesla": {
    "pill": "Tesla", "date": "June 2026", "crumb": "When to get PPF", "img": "tesla-model-3-ppf-doral",
    "title": "How Soon Should You Get PPF on a New Tesla? | Tesla Boutique",
    "desc": "The short answer: before the first long drive. Why factory-fresh paint is the best canvas for PPF, and why waiting costs more in Miami.",
    "h1": 'How soon after buying a Tesla should you get <span class="highlight">PPF</span>?',
    "card_title": "How soon after buying a Tesla should you get PPF?",
    "blurb": "The short answer: before the first long drive. Here is why protecting factory-fresh paint matters most.",
    "lead": "The short answer: before the first long drive. Here is why protecting factory-fresh paint matters most.",
    "cta_title": "Getting a new Tesla?",
    "cta_desc": "Tell us your delivery date and we will have genuine XPEL PPF ready the day it arrives."},
  "ultimate-plus-vs-stealth": {
    "pill": "XPEL", "date": "June 2026", "crumb": "Ultimate Plus vs Stealth", "img": "tesla-cybertruck-ppf-miami",
    "title": "Ultimate Plus vs Stealth: Which PPF Finish for Your Tesla?",
    "desc": "Gloss or satin? Same XPEL protection, two very different looks. A quick guide to choosing between Ultimate Plus and Stealth for your Tesla.",
    "h1": 'Ultimate Plus vs Stealth: which <span class="highlight">PPF</span> finish is right for you?',
    "card_title": "Ultimate Plus vs Stealth: which PPF finish is right for you?",
    "blurb": "Gloss or satin? A quick guide to choosing the XPEL film finish that suits your Tesla.",
    "lead": "Gloss or satin? A quick guide to choosing the XPEL film finish that suits your Tesla.",
    "cta_title": "Want to see satin next to gloss?",
    "cta_desc": "We keep both finishes on hand at the Doral shop. Come compare them in person."},
  "ppf-ceramic-care-miami": {
    "pill": "Maintenance", "date": "June 2026", "crumb": "Caring for PPF and ceramic", "img": "tesla-model-s-ceramic-coating",
    "title": "Caring for PPF &amp; Ceramic Coating in Miami | Tesla Boutique",
    "desc": "Simple wash habits that keep XPEL film and Fusion Plus ceramic performing for years in the Florida heat, from a Tesla-only shop in Doral.",
    "h1": 'Caring for your <span class="highlight">PPF</span> and ceramic coating in Miami',
    "card_title": "Caring for your PPF and ceramic coating in Miami",
    "blurb": "Simple wash habits that keep XPEL film and Fusion Plus coating performing for years in the Florida heat.",
    "lead": "Simple wash habits that keep XPEL film and Fusion Plus coating performing for years in the Florida heat.",
    "cta_title": "Not sure how to care for your setup?",
    "cta_desc": "Call us and tell us what your Tesla is wearing. We will tell you exactly how to care for it."},
  "removing-water-spots": {
    "pill": "Maintenance", "date": "June 2026", "crumb": "Removing water spots", "img": "tesla-model-y-window-tinting",
    "title": "How to Remove Water Spots from a Tesla, Glass &amp; Paint | Tesla Boutique Miami",
    "desc": "What causes hard-water spots on a Tesla in South Florida, how to remove them safely from glass and paint, and how to stop them coming back. From a Tesla-only shop in Doral.",
    "h1": 'Removing <span class="highlight">water spots</span> from your Tesla, glass and paint',
    "card_title": "Removing water spots from your Tesla's glass and paint",
    "blurb": "What causes hard-water spotting in South Florida and how to remove it safely from glass and paint without damaging your finish.",
    "lead": "What causes hard-water spotting in South Florida and how to remove it safely from glass and paint without damaging your finish.",
    "cta_title": "Stubborn water spots on your Tesla?",
    "cta_desc": "Bring it to our Doral shop and we will safely remove the spots and help keep them from coming back."},
}

GUIDES = {
  "does-a-leased-tesla-need-ppf": {
    "pill": "Leasing", "crumb": "Leased Tesla and PPF", "img": "tesla-model-3-ppf-doral", "reviewed": "July 2026",
    "title": "Does a Leased Tesla Need PPF? | Tesla Boutique Miami",
    "desc": "Straight answer for South Florida: yes, and on a lease PPF often pays for itself, because Tesla bills lease-return chips and scratches that Miami highways cause.",
    "h1": 'Does a leased Tesla need <span class="highlight">PPF</span>?',
    "card_title": "Does a leased Tesla need PPF?",
    "blurb": "Short answer: on a lease it can pay for itself at return. Here is the South Florida math.",
    "lead": "Short answer: yes, and on a lease it often pays for itself. Tesla bills lease-end damage like rock chips, scratches and curb rash, and South Florida highways cause exactly that. Front PPF keeps the paint factory-perfect so you hand the car back with no chip charges, and genuine XPEL film removes cleanly so you take none of the value with you.",
    "cta_title": "Leasing a Tesla in South Florida?",
    "cta_desc": "Tell us your delivery or pickup date and we will have genuine XPEL PPF ready so it returns spotless.",
    "sections": [
      ("What Tesla charges for at lease return", [
        "A Tesla lease return is inspected for excess wear, and chipped paint, scratches, curb-rashed panels and stone-pitting on the hood and bumper are the classic line items. In a market like Miami, where I-95, the Palmetto and the Dolphin Expressway throw gravel and construction debris every day, a bare front end picks those up fast. Paying at return for damage you could have prevented is the worst-value way to spend that money.",
        "Paint protection film is the direct fix: a clear, self-healing XPEL layer over the panels that take the hits, so the paint underneath stays exactly as delivered."]),
      ("Why leasing is arguably the strongest case for PPF", [
        "When you own a car, PPF protects resale. When you lease, it protects you from a bill you did not budget for, and that bill can rival the cost of the film itself. Full-front coverage on the hood, fenders, mirrors and front bumper is usually the sweet spot for a lease: it guards the panels most likely to be flagged, without the cost of full-body.",
        "And because you keep the car for a set term, the film does not even need to last a decade. It just has to keep the paint clean through the lease, which quality PPF does easily."]),
      ("Does the film come off cleanly at the end?", [
        "Yes. Genuine <a href=\"../services/paint-protection-film.html\">XPEL film</a> is made to be removed without lifting factory paint or clear coat, so at lease return the panels are revealed in the same condition they were installed. You get the protection during the lease and leave nothing behind. And if you decide to buy the car out at the end, even better: the film is already there protecting your now-owned Tesla."]),
      ("Get it before the first long drive", [
        "The ideal moment is right after delivery, before the paint sees highway miles. Many of our clients pick up a new lease at the Doral Tesla center and bring it straight to us so the film goes on factory-fresh paint. If your Tesla already has a few thousand miles, we correct the paint first, then film it."]),
    ],
    "faqs": [
      ("Is PPF worth it on a 2 or 3 year Tesla lease?", "In South Florida, usually yes. A single lease-return chip or scratch charge can approach the cost of front PPF, and highway debris here makes that damage almost inevitable on a bare front end. The film prevents it and removes cleanly at return."),
      ("Will PPF damage the paint when it is removed at lease end?", "No. Genuine XPEL film is designed to peel off without lifting factory paint or clear coat, leaving the panels as they were when installed. That is exactly why it works so well for leases."),
      ("How much of the car should I film on a lease?", "Full-front (hood, fenders, mirrors and front bumper) is the usual lease choice: it covers the panels Tesla is most likely to flag for chips, without the cost of full-body coverage."),
    ],
  },
  "florida-window-tint-laws-tesla": {
    "pill": "Legal and tint", "crumb": "Florida tint laws", "img": "tesla-model-y-window-tinting", "reviewed": "July 2026",
    "title": "Window Tint Laws in Florida for Tesla Owners | Tesla Boutique Miami",
    "desc": "The legal tint limits in Florida for a Tesla: front sides 28% VLT, rears 15%, windshield and reflectivity rules, and how to get maximum heat rejection while staying legal.",
    "h1": 'Window tint laws in Florida for <span class="highlight">Tesla</span> owners',
    "card_title": "Window tint laws in Florida for Tesla owners",
    "blurb": "The legal limits, plainly: front sides 28% VLT, rears 15%, plus windshield and reflectivity rules.",
    "lead": "In Florida, a Tesla's front side windows must let in at least 28% of light (28% VLT), and the rear side and back windows at least 15%. The windshield can only take non-reflective tint along the top strip. Here is what that means for your Model 3, Y, S, X or Cybertruck, and how to get the most heat rejection while staying legal.",
    "cta_title": "Want legal tint that actually beats the Miami heat?",
    "cta_desc": "We install XPEL ceramic tint to Florida-legal limits: maximum heat rejection, no ticket. Call us.",
    "sections": [
      ("The legal limits for a passenger vehicle in Florida", [
        "For a private passenger car in Florida, the tint darkness (VLT, the percentage of visible light the glass lets through) has to meet these minimums: <strong>front side windows, 28% VLT or more</strong>; <strong>rear side windows, 15% VLT or more</strong>; <strong>rear window, 15% VLT or more</strong>. Lower VLT means darker, so 28% is the darkest legal shade for the fronts and 15% for the rears.",
        "There are also reflectivity limits, tint cannot be too mirror-like: front side windows no more than 25% reflective, rear side windows no more than 35% reflective. On the windshield, only a non-reflective strip along the top (above the manufacturer's AS-1 line) is allowed."]),
      ("What that means for each Tesla", [
        "The percentages apply to the side and rear glass, so they are the same across the Model 3, Model Y, Model S, Model X and Cybertruck. What differs is the glass area: the Model 3 and Model Y have a large fixed glass roof, and the Model S and Model X have panoramic glass, all of which lets in a lot of heat under the Florida sun. That glass roof is not a side window under the darkness rule, so it can take a heat-rejecting film to cut the greenhouse effect.",
        "Tesla's factory glass already blocks some UV and infrared, but on its own it is not enough for a car that bakes in Miami. A quality ceramic tint adds serious heat rejection on top."]),
      ("How to get maximum heat rejection while staying legal", [
        "Darkness and heat rejection are not the same thing. A cheap dark dye film can be very dark and still let heat through, while a <a href=\"../services/window-tint.html\">ceramic film</a> like XPEL Prime XR Plus rejects up to 98% of infrared heat even at a legal, lighter shade. In other words, you do not need to break the 28% front rule to keep a Tesla cool, you need the right film. We install to the legal VLT and let the ceramic technology do the heat work.",
        "That is the combination we recommend for South Florida: a legal shade that keeps the car comfortable, protects the interior from UV fading, and will not get you a ticket."]),
      ("Medical exemption, and a word of caution", [
        "Florida allows a medical exemption for drivers with certain light-sensitivity conditions, which permits darker tint with the proper documentation. If that applies to you, keep the paperwork in the car.",
        "One caution: tint law is set by the state and can change, and this guide is general information, not legal advice. We install to the current Florida limits and can walk you through the exact VLT options for your Tesla. When in doubt, verify the current statute or ask us."]),
    ],
    "faqs": [
      ("What is the darkest legal tint on a Tesla in Florida?", "For a passenger vehicle, the front side windows must be 28% VLT or lighter (that is the darkest legal front shade), and the rear side and back windows 15% VLT or lighter. The windshield only allows a non-reflective strip along the top."),
      ("Can I tint the glass roof on my Model 3 or Model Y?", "Yes. The fixed glass roof is not covered by the side-window darkness limits, so it can take a heat-rejecting film to cut the sun load. It is one of the highest-impact comfort upgrades in the Florida heat."),
      ("Does a legal tint still block the Miami heat?", "Yes, if it is a ceramic film. Heat rejection comes from the film technology, not just how dark it is. XPEL Prime XR Plus rejects up to 98% of infrared heat at a legal shade, so you stay cool and legal."),
      ("Is this legal advice?", "No. This is general information based on Florida's tint rules; laws can change and enforcement varies. We install to the current legal limits; for anything official, verify the current statute."),
    ],
  },
  "best-protection-model-y-south-florida": {
    "pill": "Model Y", "crumb": "Best package for a Model Y", "img": "cars/model-y/model-y-blue-studio", "reviewed": "July 2026",
    "title": "Best Protection Package for a Model Y in South Florida | Tesla Boutique Miami",
    "desc": "What actually protects a Model Y in Miami's sun, salt and highway debris: our recommended full-front PPF, ceramic coating and ceramic tint combination for a daily-driven Model Y.",
    "h1": 'The best protection package for a <span class="highlight">Model Y</span> in South Florida',
    "card_title": "Best protection package for a Model Y in South Florida",
    "blurb": "For a daily-driven Model Y here: full-front PPF, a ceramic coating and ceramic tint. Here is why.",
    "lead": "For a Model Y that lives in South Florida, the package that makes sense is full-front PPF, a Fusion Plus ceramic coating and ceramic window tint. It covers the three things that actually age a Model Y here: highway rock chips, sun and heat, and the salt-and-grime that dulls the paint. Here is how we would spec it, and where to start if you do a bit at a time.",
    "cta_title": "Protecting a Model Y in South Florida?",
    "cta_desc": "Tell us how you drive it and we will spec the exact PPF, ceramic and tint package for your Model Y.",
    "sections": [
      ("Why the Model Y is a specific case", [
        "The Model Y is the family-and-commuter Tesla, which in South Florida means real daily miles on I-95, the Turnpike and I-75, plus long hours parked in the sun. That combination, highway debris up front and relentless UV and heat, is exactly what wears a Model Y: chips on the hood and bumper, a hot cabin, and paint that loses its depth. The soft factory clear coat does not help. So the right package is not about buying everything, it is about matching protection to those three threats."]),
      ("1) Full-front PPF, for the highway", [
        "The single most valuable piece on a commuter Model Y is <a href=\"../services/paint-protection-film.html\">full-front paint protection film</a>: hood, fenders, mirrors and front bumper. That is where the Turnpike and I-95 do their damage, and self-healing XPEL film takes the chips instead of the paint. If the budget stretches, adding the rocker panels and rear-arch high-wear areas is the next step; full-body is for owners who want the whole car untouched."]),
      ("2) Ceramic coating, for the sun and the wash cycle", [
        "Over the paint (and over the PPF), a <a href=\"../services/ceramic-coating.html\">Fusion Plus ceramic coating</a> does two jobs in Florida: it adds UV and chemical resistance so the finish holds its gloss under the sun, and it makes the car far easier to keep clean, water, salt residue and love-bug season rinse off instead of bonding. On a family car that gets washed a lot, that is a real time-saver."]),
      ("3) Ceramic tint, for the cabin and the kids", [
        "A Model Y's big glass roof turns the cabin into a greenhouse fast. <a href=\"../services/window-tint.html\">XPEL Prime XR Plus ceramic tint</a>, installed to Florida-legal limits, rejects up to 98% of the infrared heat and 99% of UV, so the interior stays cooler and does not fade. For a family Model Y, it is one of the most-felt upgrades on the daily drive."]),
      ("Where to start if you do it in stages", [
        "If you are not doing it all at once, we usually sequence it: front PPF first (it protects paint you can never get back), then ceramic tint (immediate comfort), then the ceramic coating. New Model Y? The best time is right after delivery, before the first long drive, so the film goes on factory-fresh paint. We will spec the exact package for your Model Y and how you actually drive it."]),
    ],
    "faqs": [
      ("What is the minimum I should do to protect a Model Y here?", "If you only do one thing, do full-front PPF, the hood, fenders, mirrors and bumper that take South Florida's highway rock chips. It protects paint you cannot restore later. Ceramic tint is the next most-felt upgrade for the heat."),
      ("Do I need full-body PPF on a Model Y?", "Usually not. Full-front handles the panels that actually get hit on the Turnpike and I-95. Full-body is for owners who want every panel untouched or plan to keep the car long-term. We will tell you honestly what your driving calls for."),
      ("Can I get PPF, ceramic and tint done together?", "Yes, and it is the most efficient way: one visit, correct sequence, with film and coating layered properly and tint done alongside. Tell us your Model Y and we will quote the combined package."),
    ],
  },
}

def build_guide(slug, d):
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Guides", prefix + "guides/index.html"), (d["crumb"], "")])
    hero = page_hero(prefix, d["img"], d["h1"], d["lead"], "", crumbs)
    inner = f'<span class="post-date">Last reviewed &middot; {d["reviewed"]}</span>'
    for h2, paras in d["sections"]:
        bi = "".join(p if p.lstrip().startswith("<ul") else f"<p>{p}</p>" for p in paras)
        inner += f'<h2>{h2}</h2>{bi}'
    faqs = d.get("faqs") or []
    if faqs:
        inner += '<h2>Frequently asked questions</h2>'
        for q, a in faqs:
            inner += f'<h3>{q}</h3><p>{a}</p>'
    prose = f'<section class="section"><div class="container"><div class="prose">{inner}</div></div></section>'
    cta = cta_block(d["cta_title"], d["cta_desc"])
    body = hero + prose + cta
    art_ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": d["card_title"],
        "description": d["desc"], "inLanguage": "en",
        "author": {"@type": "Organization", "name": "Tesla Boutique Miami"},
        "publisher": {"@type": "Organization", "name": "Tesla Boutique Miami", "url": DOMAIN + "/"},
        "image": f"{DOMAIN}/assets/img/{d['img']}.webp",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}/guides/{slug}.html"}}, ensure_ascii=False)
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Guides", DOMAIN + "/guides/index.html"), (d["crumb"], f"{DOMAIN}/guides/{slug}.html")]), art_ld]
    if faqs:
        ld.append(json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False))
    return doc(f"guides/{slug}.html", d["title"], d["desc"], body, active="guides", preload=d["img"], extra_ld=ld)

def build_guides():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Guides", "")])
    hero = page_hero(prefix, "cars/model-s/model-s-blue-1", 'Tesla Care <span class="highlight">Guides</span>',
        "Straight, no-fluff answers to the questions Tesla owners in South Florida actually ask, from a Tesla-only XPEL shop in Doral. Evergreen reference, not news.", "", crumbs)
    cards = ""
    for slug, d in GUIDES.items():
        cards += (f'<div class="project-tile reveal"><div class="project-tile-body">'
                  f'<div class="tag-row"><span class="pill">{d["pill"]}</span></div>'
                  f'<h3>{d["card_title"]}</h3><p>{d["blurb"]}</p>'
                  f'<a class="card-link" href="{slug}.html">Read guide &rarr;</a></div></div>')
    grid = (f'<section class="section"><div class="container">'
            f'<div class="section-header"><span class="section-tag">Tesla Knowledge</span>'
            f'<h2 class="section-title">Guides for Tesla owners in South Florida</h2>'
            f'<p class="section-desc">The questions Tesla owners ask before they protect a car, answered by a shop that only works on Teslas.</p></div>'
            f'<div class="project-list-grid">{cards}</div></div></section>')
    cta = cta_block("A question we have not covered yet?", "Ask us directly. We would rather answer it than have you guess.")
    body = hero + grid + cta
    ld = [json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tesla Care Guides",
        "url": DOMAIN + "/guides/index.html",
        "description": "Evergreen guides on protecting and caring for a Tesla in Miami and South Florida."}, ensure_ascii=False)]
    return doc("guides/index.html", "Tesla Care Guides for South Florida Owners | Tesla Boutique Miami",
               "Evergreen guides for Tesla owners in Miami and South Florida: PPF, ceramic coating, window tint laws, model-specific care and more, from a Tesla-only XPEL shop in Doral.",
               body, active="guides", preload="cars/model-s/model-s-blue-1", extra_ld=ld)

def build_post(slug, d):
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Updates", prefix + "news/index.html"), (d["crumb"], "")])
    hero = page_hero(prefix, d["img"], d["h1"], d["lead"], "", crumbs)
    inner = f'<span class="post-date">Published &middot; {d["date"]}</span>'
    if d.get("sections"):
        for h2, paras in d["sections"]:
            bi = "".join(p if p.lstrip().startswith("<ul") else f"<p>{p}</p>" for p in paras)
            inner += f'<h2>{h2}</h2>{bi}'
    else:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts", f"{slug}.en.html"), encoding="utf-8") as _f:
            inner += _f.read()
    prose = f'<section class="section"><div class="container"><div class="prose">{inner}</div></div></section>'
    cta = cta_block(d["cta_title"], d["cta_desc"])
    body = hero + prose + cta
    post_ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": d["card_title"],
        "description": d["desc"], "datePublished": "2026-06-03", "dateModified": "2026-06-03", "inLanguage": "en",
        "author": {"@type": "Organization", "name": "Tesla Boutique Miami"},
        "publisher": {"@type": "Organization", "name": "Tesla Boutique Miami", "url": DOMAIN + "/"},
        "image": f"{DOMAIN}/assets/img/{d['img']}.webp",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}/news/{slug}.html"}}, ensure_ascii=False)
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Updates", DOMAIN + "/news/index.html"), (d["crumb"], f"{DOMAIN}/news/{slug}.html")]), post_ld]
    return doc(f"news/{slug}.html", d["title"], d["desc"], body, active="news", preload=d["img"], extra_ld=ld)

def build_news():
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Updates", "")])
    hero = page_hero(prefix, "tesla-model-s-ceramic-coating", 'Tesla Boutique <span class="highlight">Updates</span>',
        "News and resources from Tesla Boutique Miami: fresh projects, XPEL product updates, and practical tips on caring for your Tesla's film, coating and tint. Updated regularly.", "", crumbs)
    posts = []
    cards = ""
    for slug, d in POSTS.items():
        cards += (f'<div class="project-tile reveal"><div class="project-tile-body">'
                  f'<div class="tag-row"><span class="pill">{d["pill"]}</span></div>'
                  f'<span class="post-date">Published &middot; {d["date"]}</span>'
                  f'<h3>{d["card_title"]}</h3><p>{d["blurb"]}</p>'
                  f'<a class="card-link" href="{slug}.html">Read article &rarr;</a></div></div>')
    for pill, h3, p in posts:
        cards += (f'<div class="project-tile reveal"><div class="project-tile-body">'
                  f'<div class="tag-row"><span class="pill">{pill}</span></div>'
                  f'<h3>{h3}</h3><p>{p}</p><span class="card-link">Coming soon</span></div></div>')
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

HERO_SLIDES = [
    "cars/model-s/model-s-blue-1",
    "cars/model-y/model-y-1",
    "cars/model-x/model-x-red-6",
    "cars/cybertruck/cybertruck-3-white",
]

def hero_slides(prefix):
    # Only the first slide gets its background eagerly (it is the LCP and is
    # preloaded). The rest carry the style in data-bg and are hydrated by JS
    # after load, so they do not compete with the LCP image for bandwidth.
    out = []
    for i, n in enumerate(HERO_SLIDES):
        if i == 0:
            out.append(f'<div class="hero-bg-image is-active" style="{bg_style(prefix, n)}"></div>')
        else:
            out.append(f'<div class="hero-bg-image" data-bg="{bg_style(prefix, n)}"></div>')
    return "".join(out)

CONTACT_FORM_EN = '''<div class="cform-wrap">
  <h3 class="cform-title">Or send us the details</h3>
  <p class="cform-sub">Tell us about your Tesla and we will get back to you.</p>
  <form class="cform" action="https://script.google.com/macros/s/AKfycbwxH5z4fadzu_YAI_FFUNs7oHej3mgeVG67v6A2-Ds1ZjqhBY8AN0qxv4hvWs9GRWXV/exec" method="POST" novalidate>
    <input type="hidden" name="lang" value="en">
    <input type="hidden" name="page" value="home-en">
    <input type="hidden" name="ts" value="">
    <div class="cform-hp" aria-hidden="true">
      <label>Company<input type="text" name="company" tabindex="-1" autocomplete="off"></label>
    </div>
    <div class="cform-grid">
      <label class="cform-field"><span>Name *</span><input type="text" name="name" required autocomplete="name"></label>
      <label class="cform-field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel" inputmode="tel"></label>
      <label class="cform-field"><span>Email</span><input type="email" name="email" autocomplete="email" inputmode="email"></label>
      <label class="cform-field"><span>Tesla model</span><select name="model"><option value="">Select your model</option><option>Model 3</option><option>Model Y</option><option>Model S</option><option>Model X</option><option>Cybertruck</option><option>Other</option></select></label>
      <label class="cform-field cform-full"><span>Service you are interested in</span><select name="service"><option value="">Select a service</option><option>Paint Protection Film (PPF)</option><option>Colored PPF</option><option>Ceramic Coating</option><option>Window Tint</option><option>Windshield Protection</option><option>Paint Correction</option><option>Not sure yet</option></select></label>
      <label class="cform-field cform-full"><span>Message</span><textarea name="message" rows="4" placeholder="Color, year, what you have in mind..."></textarea></label>
    </div>
    <p class="cform-note">Provide at least a phone number or an email so we can reach you.</p>
    <button type="submit" class="btn btn-primary btn-lg cform-btn">Send inquiry</button>
    <p class="cform-msg cform-ok" hidden>Thank you! We received your inquiry and will contact you shortly.</p>
    <p class="cform-msg cform-err" hidden>Something went wrong. Please call us at (786) 505-6162 and we will take care of you.</p>
  </form>
</div>'''

def build_home():
    prefix = ""
    hero = (f'<section class="hero"><div class="hero-bg">{hero_slides(prefix)}</div>'
            f'<div class="container"><div class="hero-content">'
            f'<h1 class="hero-title"><span class="tesla">Tesla</span> Protection<br>Experts in <span class="highlight">Miami</span></h1>'
            f'<p class="hero-subtitle">Premium paint protection film, window tint and ceramic coating, especially recommended for Tesla. Expert XPEL installers with 15+ years of experience across Florida.</p>'
            f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{svg(IC["phone"], w=20, h=20)} Call Now</a>'
            f'<a href="#models" class="btn btn-outline btn-lg">Find My Tesla</a></div>'
            f'<div class="hero-stats">'
            f'<div class="hero-stat"><span class="hero-stat-value">15+</span><span class="hero-stat-label">Years Experience</span></div>'
            f'<div class="hero-stat"><span class="hero-stat-value">Tesla</span><span class="hero-stat-label">Only Specialists</span></div>'
            f'<div class="hero-stat"><span class="hero-stat-value"><img class="hero-stat-logo" src="{prefix}assets/img/xpel-logo.png" alt="XPEL" width="600" height="183"></span><span class="hero-stat-label">Exclusive Dealer</span></div>'
            f'</div></div></div></section>')
    banner = ('<section class="xpel-banner"><div class="container"><div class="xpel-banner-content">'
              '<div class="xpel-badge"><span class="xpel-banner-logo"><img src="assets/img/xpel-logo-solid.png" alt="XPEL" width="700" height="190"></span>'
              '<span class="xpel-text"><strong>Exclusive Dealer</strong>, genuine XPEL products only</span></div>'
              '<div class="xpel-badge"><span class="xpel-text">10-Year Warranty on all PPF installations</span></div>'
              '</div></div></section>')
    # models grid
    mcards = ""
    for s, l in MODELS_NAV:
        d = MODELS[s]
        mcards += (f'<a class="model-card reveal" href="models/{s}.html">{pic(prefix, d.get("card", d["img"]), img_alt(d.get("card", d["img"]), "en"), 700, 525)}'
                   f'<div class="model-card-overlay"><h3>{l}</h3></div></a>')
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
           '<div class="why-item reveal"><span class="why-number">01</span><h3>XPEL Exclusive Dealer</h3><p>Authorized XPEL exclusive dealer. 15+ years installing PPF, ceramic and film on exotic and luxury vehicles, now 100% focused on Tesla.</p></div>'
           '<div class="why-item reveal"><span class="why-number">02</span><h3>Tesla Specialists</h3><p>We know every panel, sensor and camera placement on Model 3, Y, S, X and Cybertruck. Patterns made for Tesla, not adapted.</p></div>'
           '<div class="why-item reveal"><span class="why-number">03</span><h3>Genuine XPEL Products</h3><p>Only authentic XPEL film and coatings, with full manufacturer warranty registered to your vehicle.</p></div>'
           '<div class="why-item reveal"><span class="why-number">04</span><h3>Real Project Documentation</h3><p>Every car we protect is photographed and documented, so you can see exactly the work that comes out of our shop.</p></div>'
           '</div></div></section>')
    areas = ('<section class="section"><div class="container">'
             '<div class="section-header"><span class="section-tag">Service areas</span>'
             '<h2 class="section-title">Serving Tesla owners across South Florida</h2>'
             '<p class="section-desc">Based in Doral, protecting Teslas across Miami-Dade, Broward, Palm Beach and the Florida Keys.</p></div><div class="areas-grid">'
             '<a class="area-item reveal" href="service-area/miami-dade/doral.html"><h3>Doral, FL</h3><p>Our home base and installation shop.</p></a>'
             '<a class="area-item reveal" href="service-area/miami-dade/miami.html"><h3>Miami, FL</h3><p>Downtown, Brickell and Wynwood.</p></a>'
             '<a class="area-item reveal" href="service-area/miami-dade/miami-beach.html"><h3>Miami Beach</h3><p>South Beach, Mid-Beach and North Beach.</p></a>'
             '<a class="area-item reveal" href="service-area/miami-dade/coral-gables.html"><h3>Coral Gables</h3><p>Ceramic coating and PPF for the Gables.</p></a>'
             '<a class="area-item reveal" href="service-area/miami-dade/aventura.html"><h3>Aventura</h3><p>Aventura and Sunny Isles.</p></a>'
             '<a class="area-item reveal" href="service-area/index.html"><h3>Broward, Palm Beach &amp; the Keys</h3><p>Fort Lauderdale, Boca Raton, Key West and more.</p></a>'
             '</div>'
             '<div class="areas-cta"><a href="service-area/index.html" class="btn btn-outline btn-lg">Explore our full service area &rarr;</a></div>'
             '</div></section>')
    pin_svg = svg('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>')
    clock_svg = svg('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>')
    phone_svg = svg(IC["phone"], w=20, h=20)
    contact = (f'<section class="cta-section" id="contact"><div class="container"><div class="cta-content">'
               f'<h2 class="cta-title">Ready to protect your Tesla?</h2>'
               f'<p class="cta-desc">Tell us your model and what you are after, and we will guide you to the right PPF, tint or ceramic package. Booking is currently handled through our parent shop, Unlimited Wraps.</p>'
               f'<div class="cta-buttons"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{phone_svg} {PHONE_DISP}</a>'
               f'<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Book via Unlimited Wraps</a></div>'
               f'{CONTACT_FORM_EN}'
               f'<div class="cta-contact-info">'
               f'<div class="cta-contact-item">{pin_svg}<span>1835 NW 79th Ave, Doral, FL 33126</span></div>'
               f'<div class="cta-contact-item">{clock_svg}<span>Mon to Fri: 9AM to 5:30PM</span></div>'
               f'</div></div></div></section>')
    body = hero + banner + models_sec + services_sec + why + areas + contact
    local_ld = json.dumps({"@context": "https://schema.org", "@type": "AutoBodyShop",
        "@id": DOMAIN + "/#business", "name": "Tesla Boutique Miami",
        "alternateName": ["Tesla Boutique Miami (Unlimited Wraps)", "XPEL Tesla Doral"],
        "description": "Tesla only paint protection film, ceramic coating and window tint in Doral and Miami, FL. XPEL exclusive dealer powered by Unlimited Wraps, with 15+ years protecting exotic and luxury vehicles and now focused exclusively on Tesla.",
        "url": DOMAIN + "/", "telephone": "+1-786-505-6162", "image": DOMAIN + "/assets/img/cars/model-s/model-s-blue-1.webp",
        "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave", "addressLocality": "Doral",
                    "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 25.791474, "longitude": -80.323911},
        "areaServed": [{"@type": "City", "name": n} for n in ["Doral", "Miami", "Miami Beach", "Coral Gables", "Aventura", "Brickell", "Hialeah", "Kendall"]],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30"}],
        "priceRange": "$$$", "currenciesAccepted": "USD", "paymentAccepted": ["Cash", "Credit Card", "Debit Card"],
        "sameAs": ["https://www.unlimitedwraps.com", "https://www.instagram.com/teslaboutiquemiami",
                   "https://www.facebook.com/UnlimitedWraps", "https://www.youtube.com/user/UnlimitedWraps",
                   "https://www.tiktok.com/@unlimitedwraps"],
        "parentOrganization": {"@type": "Organization", "name": "Unlimited Wraps, Inc.", "url": "https://www.unlimitedwraps.com"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tesla " + l}} for _, l in SERVICES_NAV]},
        ensure_ascii=False)
    website_ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "@id": DOMAIN + "/#website",
        "url": DOMAIN + "/", "name": "Tesla Boutique Miami", "inLanguage": ["en", "es"],
        "publisher": {"@id": DOMAIN + "/#business"}}, ensure_ascii=False)
    title = "Tesla PPF, Ceramic Coating &amp; Window Tint in Miami &amp; Doral | Tesla Boutique Miami, XPEL"
    desc = "Tesla only paint protection film (PPF), ceramic coating and window tint in Doral and Miami, FL. XPEL exclusive dealer, 15+ years in paint protection, now Tesla-only. Model 3, Y, S, X and Cybertruck. Call (786) 505-6162."
    return doc("index.html", title, desc, body, active="", preload="cars/model-s/model-s-blue-1", extra_ld=[local_ld, website_ld])

# ---------------------------------------------------------------- SERVICE AREA data
COUNTIES = [
  {"slug": "miami-dade", "name": "Miami-Dade County", "short": "Miami-Dade",
   "img": "cars/model-y/model-y-1", "tag": "Our home county",
   "lead": "From Doral to the beaches, Miami-Dade is where Tesla Boutique Miami lives and works. This is our home county, and the one we know best.",
   "intro": [
     "Miami-Dade is the most populous county in Florida and one of the densest Tesla markets in the country. It is also our home: our shop sits in Doral, in the heart of the county, which means Miami-Dade Tesla owners get the fastest, most convenient service we offer. From the financial towers of Brickell to the sand of Miami Beach and the canopy streets of Coral Gables, the county packs an enormous range of driving conditions into a small area.",
     "What every Miami-Dade Tesla shares is exposure: I-95, the Palmetto and the Dolphin Expressway throw constant gravel and construction debris, the sun is relentless year-round, and dense valet and garage parking means door dings and tight squeezes. That is exactly the environment XPEL paint protection film, ceramic coating and ceramic window tint were built for. Choose your city below to see how we protect Teslas in your part of Miami-Dade."],
   "cities": ["miami", "miami-beach", "doral", "coral-gables", "aventura"]},
  {"slug": "broward", "name": "Broward County", "short": "Broward",
   "img": "cars/model-3/model-3-grey", "tag": "Fort Lauderdale & north",
   "lead": "Fort Lauderdale, Hollywood and the cities just north of us. Broward Tesla owners are a short drive up I-95 or the Turnpike from our Doral shop.",
   "intro": [
     "Broward County stretches from the Atlantic beaches inland to the edge of the Everglades, and it is one of the fastest-growing Tesla markets in South Florida. For owners in Fort Lauderdale, Hollywood and the western suburbs, we are a straight shot down I-95 or the Turnpike from our Doral shop. Broward blends beach living with sprawling commuter suburbs, so a Tesla here faces salt air near the coast and long, gravel-strewn highway miles inland.",
     "Whether you are crossing the 595, parking near Las Olas or commuting from Weston, the threats are the same: rock chips, relentless sun and coastal salt. XPEL paint protection film, ceramic coating and ceramic window tint are built for exactly this. Choose your Broward city below to see how we protect Teslas in your area."],
   "cities": ["fort-lauderdale", "hollywood", "pembroke-pines", "weston", "miramar"]},
  {"slug": "palm-beach", "name": "Palm Beach County", "short": "Palm Beach",
   "img": "cars/model-x/model-x-red-1", "tag": "Boca Raton & the coast",
   "lead": "Boca Raton, West Palm Beach and the affluent communities of Palm Beach County, where Teslas are everywhere and a flawless finish is the standard.",
   "intro": [
     "Palm Beach County is where South Florida turns affluent and unhurried, and Teslas are everywhere, from Boca Raton's gated communities to the waterfront estates of Palm Beach itself. It is the northern edge of our service area, an easy run up I-95 or the Turnpike from Doral. The county pairs pristine coastal living with long suburban drives, so Teslas here see both salt air and serious highway mileage.",
     "For owners who expect their car to look showroom-perfect year-round, XPEL paint protection film, ceramic coating and ceramic tint are the standard. Pick your Palm Beach city below to see how we protect Teslas there."],
   "cities": ["boca-raton", "west-palm-beach", "delray-beach", "wellington", "jupiter"]},
  {"slug": "monroe", "name": "Monroe County", "short": "Monroe (The Keys)",
   "img": "cars/cybertruck/cybertruck-3-white", "tag": "The Florida Keys",
   "lead": "Key West, Key Largo and the island chain. Salt air and sun make the Keys one of the harshest places in Florida for a Tesla's paint and glass.",
   "intro": [
     "Monroe County is the Florida Keys, a 100-mile island chain where the Overseas Highway is the only road in or out. It is the most demanding environment in our service area for a vehicle: constant salt air, blinding sun and a single long highway that funnels every mile of driving. A Tesla in the Keys is gorgeous and seriously exposed.",
     "That is exactly where XPEL protection earns its keep: film against the relentless sun and road debris of US-1, ceramic coating that makes salt residue rinse off, and ceramic tint to cut the open-sky heat. We serve Keys Tesla owners by appointment, so reach out and we will coordinate timing for the drive up to Doral. Choose your island community below."],
   "cities": ["key-west", "key-largo", "islamorada", "marathon", "tavernier"]},
]
COUNTY_BY_SLUG = {c["slug"]: c for c in COUNTIES}

CITIES = {
  "miami": {"name": "Miami", "county": "miami-dade", "img": "cars/model-3/model-3-grey-2",
    "lead": "From Brickell high-rises to Wynwood and Coconut Grove, Miami is hard on a Tesla: tight valet garages, I-95 rock chips and relentless sun. Here is how we protect Teslas for Miami owners.",
    "intro": [
      "Tesla Boutique Miami provides premium paint protection film, ceramic coating and window tint built exclusively for Tesla owners across Miami, FL. Whether you park in a Brickell tower, commute downtown or weekend in Coconut Grove, your Model 3, Y, S, X or Cybertruck faces the same daily threats: gravel and construction debris on I-95 and the Dolphin Expressway, door dings in packed valet garages, and the kind of sun and heat that fades interiors and bakes soft Tesla paint.",
      "Our answer is Tesla-specific. We install genuine XPEL paint protection film on the panels that take the most impact, XPEL Prime XR Plus ceramic tint to cut the heat that builds under the Miami sun, and XPEL Fusion Plus ceramic coating for gloss and easy washing. Every install uses model-specific patterns cut for your exact Tesla and is registered to your VIN. Our shop is a short drive away in Doral, serving Miami owners by appointment."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Do you provide Tesla PPF and tint in Miami?",
       "Yes. We protect Teslas for owners across Miami, from Brickell and Downtown to Wynwood and Coconut Grove. Our installation shop is in nearby Doral, an easy drive from anywhere in the city. Call (786) 505-6162 to book."),
      ("How far is your shop from Brickell or Downtown Miami?",
       "Our Doral shop at 1835 NW 79th Ave is roughly 15 to 20 minutes from Brickell and Downtown via the Dolphin Expressway or NW 12th Street. Most clients drop the car off and we coordinate timing around their day."),
      ("Why does my Tesla need PPF in Miami?",
       "Miami highways like I-95 and the Palmetto throw constant gravel and construction debris, and Tesla's factory clear coat is soft and chips easily. Full-front PPF shields the hood, fenders, mirrors and bumper that take the most hits."),
      ("I keep my Model S or Model X in a Brickell tower with valet and tight garage ramps. What protects against scrapes?",
       "Brickell's narrow garage ramps and valet parking are where Teslas pick up rocker-panel and lower-bumper scrapes and door-edge dings, and Model S and Model X are especially common here. Paint protection film on the rockers, lower bumper and door edges takes those hits, and because XPEL film is self-healing, light valet swirl marks disappear with heat.")]},
  "miami-beach": {"name": "Miami Beach", "county": "miami-dade", "img": "cars/model-y/model-y-white-3",
    "lead": "Salt air, beach sand and sun all day. Miami Beach is one of the toughest environments in Florida for a Tesla's paint and glass, and exactly where protection pays off.",
    "intro": [
      "Tesla Boutique Miami brings premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across Miami Beach, from South Beach to Mid-Beach and North Beach. Life on the island is beautiful and brutal on a car: salt-laden ocean air, blowing sand, intense UV and street parking mean your Model 3, Y, S, X or Cybertruck is constantly exposed.",
      "We protect Miami Beach Teslas with genuine XPEL film that takes the sand and grit instead of your paint, ceramic coating that locks out salt and makes rinsing off beach residue effortless, and XPEL ceramic tint that blocks the heat and UV pouring through the glass. Patterns are cut specifically for your Tesla and registered to your VIN. We are based in Doral, a straight shot over the causeways, and serve Miami Beach owners by appointment."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Is ceramic coating worth it for a Tesla in Miami Beach?",
       "Very much. Salt air and beach residue are relentless on the island. A Fusion Plus ceramic coating makes salt and sand far easier to rinse off and adds UV and chemical resistance, protecting your Tesla between washes."),
      ("Do you come to Miami Beach or do I drive to you?",
       "Installs are done in our controlled Doral shop for a flawless, dust-free result. Miami Beach is a quick drive over the MacArthur or Julia Tuttle Causeway. Call (786) 505-6162 and we will coordinate timing."),
      ("Will tint help with the Miami Beach sun and heat?",
       "Yes. XPEL Prime XR Plus ceramic tint rejects up to 98% of infrared heat and 99% of UV, a major comfort upgrade for a Tesla parked in island sun, and it protects the interior from fading."),
      ("Bird droppings keep etching my Tesla near the beach. Can protection help?",
       "On the island the gulls and harbor birds are relentless, and in the Miami Beach heat their droppings are acidic enough to etch a clear coat within hours. A ceramic coating makes them bead up and rinse off instead of bonding, and PPF adds a sacrificial barrier. Between the birds, blowing sand and tourist-season street parking, coated and filmed is how a Beach Tesla stays clean.")]},
  "doral": {"name": "Doral", "county": "miami-dade", "img": "cars/model-s/model-s-blue-1",
    "lead": "Doral is home. Our shop is here, minutes from CityPlace and the Tesla dealership, which makes it the easiest place in South Florida to protect your Tesla.",
    "intro": [
      "Tesla Boutique Miami is based right here in Doral, FL, and Doral Tesla owners are our neighbors. From our shop at 1835 NW 79th Ave we provide premium paint protection film, ceramic coating, window tint and custom vehicle wrap services for every Tesla, just minutes from CityPlace Doral, Downtown Doral and the Tesla dealership on NW 12th Street.",
      "Because we are local, protecting a Doral Tesla is effortless: drop the car off before work and pick it up ready. We install genuine XPEL PPF where Palmetto Expressway gravel does its damage, XPEL Prime XR Plus ceramic tint for the Doral heat, and XPEL Fusion Plus coating for a deep, easy-clean gloss. Many of our clients buy new at the Doral Tesla store and bring the car straight to us so the paint is protected before its first highway mile. Every install uses model-specific patterns and is registered to your VIN.",
      "Doral also has one of the densest Tesla populations in South Florida, and its commercial corridors, plus constant truck and construction traffic on the Palmetto (SR-826) and NW 12th Street, throw a lot of debris. That is why so much of our Doral work is front-end PPF, including for the corporate fleets and executives who buy new at the Tesla center nearby and want the paint protected from day one."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Where is your Tesla shop in Doral?",
       "We are at 1835 NW 79th Ave, Doral, FL 33126, near the Palmetto Expressway and minutes from CityPlace Doral and the Tesla dealership. Call (786) 505-6162 to book your install."),
      ("I just bought a Tesla at the Doral dealership. Can you protect it before I drive it?",
       "Absolutely, and it is the ideal time. Bring it straight from the dealership and we will install PPF and tint before the paint sees highway miles, so the finish underneath stays factory-perfect."),
      ("Do you offer same-area convenience for Doral residents?",
       "Yes. Being local means easy drop-off and pickup, quick in-person quotes, and no long drive. Doral is our home base and our fastest-served area."),
      ("My Tesla drives Doral's commercial corridors and the Palmetto every day. Is that hard on the paint?",
       "Yes. Doral runs on truck and commercial traffic, and the Palmetto (SR-826) and NW 12th Street constantly throw gravel and construction debris that chip a Tesla's soft factory clear coat. Full-front or track PPF on the hood, fenders, mirrors and bumper is the fix, and because we are minutes from the Tesla center, many owners bring a new car straight over before the first highway mile.")]},
  "coral-gables": {"name": "Coral Gables", "county": "miami-dade", "img": "cars/model-s/model-s-red",
    "lead": "Tree-lined, upscale and detail-obsessed. Coral Gables Tesla owners expect a flawless finish, and that is exactly what we deliver.",
    "intro": [
      "Tesla Boutique Miami offers premium, Tesla-only paint protection film, ceramic coating and window tint to discerning Tesla owners throughout Coral Gables, FL. The Gables is known for its beauty, its banyan-lined streets and its standards, and the same canopy that makes Miracle Mile and Old Cutler Road gorgeous also drops sap, pollen and debris onto your Model 3, Y, S, X or Cybertruck.",
      "We protect Coral Gables Teslas with genuine XPEL paint protection film against chips and tree debris, Fusion Plus ceramic coating so sap and pollen rinse away instead of etching the paint, and XPEL ceramic tint for comfort and UV protection without altering the car's elegant look. Every install is meticulous, edge-wrapped and registered to your VIN, the level of finish Gables owners expect. Our shop is a short drive away in Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Does tree sap and pollen really damage Tesla paint in Coral Gables?",
       "Over time, yes. Sap and pollen can etch a soft clear coat, especially in the heat. A ceramic coating makes them far easier to remove and adds a protective barrier, while PPF guards against falling debris and chips."),
      ("Can window tint be done without changing my Tesla's look in the Gables?",
       "Yes. XPEL ceramic tint comes in shades that keep a clean, factory-correct appearance while cutting heat and UV, so your Tesla looks refined and stays comfortable."),
      ("Do you serve Coral Gables?",
       "Yes, we protect Teslas throughout Coral Gables, from Miracle Mile to Cocoplum and Gables Estates. Our Doral shop is a short drive away. Call (786) 505-6162 to schedule."),
      ("My Gables home has no garage and the car sits under the trees. What do you recommend?",
       "That is the toughest case in the Gables: a Tesla parked outdoors under the banyan and oak canopy takes sap, pollen, blossoms and bird droppings around the clock, plus full sun. A ceramic coating so all of that rinses off instead of etching, PPF for the falling debris and chips, and ceramic tint for the heat is the combination that keeps an always-outdoor Gables Tesla flawless.")]},
  "aventura": {"name": "Aventura", "county": "miami-dade", "img": "cars/model-x/model-x-red-3",
    "lead": "Between the ocean, the high-rises and the Aventura Mall traffic, an Aventura Tesla earns its protection. Here is how we keep it pristine.",
    "intro": [
      "Tesla Boutique Miami provides premium paint protection film, ceramic coating and window tint built exclusively for Tesla owners in Aventura, FL and the surrounding Sunny Isles area. Life near the water means salt air and intense sun, while the daily reality of Aventura Mall garages, Biscayne Boulevard and high-rise valet means door dings, tight parking and constant exposure for your Model 3, Y, S, X or Cybertruck.",
      "We protect Aventura Teslas with genuine XPEL paint protection film on high-impact panels, XPEL Fusion Plus ceramic coating that shrugs off salt air and makes washing easy, and XPEL Prime XR Plus ceramic tint that rejects the heat and UV coming off the water and the open sky. Patterns are model-specific and every install is registered to your VIN. Our installation shop is in Doral, an easy drive down US-1 or the Turnpike."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you protect Teslas in Aventura and Sunny Isles?",
       "Yes. We serve Tesla owners across Aventura, Sunny Isles Beach and Williams Island. Installs are done at our Doral shop, an easy drive via US-1 or the Turnpike. Call (786) 505-6162."),
      ("Is salt air from the ocean bad for my Tesla near Aventura?",
       "Salt air accelerates corrosion and leaves residue that bonds to paint and glass. A ceramic coating plus PPF gives a protective, easy-clean barrier that stands up to the coastal environment far better than bare paint."),
      ("How much does it cost to protect a Tesla in Aventura?",
       "It depends on coverage; full-front vs full-body PPF, tint and ceramic are separate services you can combine. Call (786) 505-6162 for a quote tailored to your Tesla and how you drive.")]},
  # ----- Broward -----
  "fort-lauderdale": {"name": "Fort Lauderdale", "county": "broward", "img": "cars/model-s/model-s-blue-2",
    "lead": "Yachts, Las Olas and the beach. Fort Lauderdale Teslas live between salt air and city traffic, and that is exactly what XPEL protection is built for.",
    "intro": [
      "Tesla Boutique Miami brings premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across Fort Lauderdale, FL. From Las Olas Boulevard to the beach and the downtown high-rises, a Fort Lauderdale Tesla deals with coastal salt air, intense sun and the stop-and-go of a busy city, all of which wear on factory paint and heat up the cabin.",
      "We protect Fort Lauderdale Teslas with genuine XPEL film on the high-impact panels, Fusion Plus ceramic coating that makes salt and grime easy to rinse off, and XPEL Prime XR Plus ceramic tint to cut the heat near the water. Patterns are model-specific and registered to your VIN. Our shop is a quick run south on I-95 from Fort Lauderdale."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Fort Lauderdale Tesla owners?",
       "Yes. We protect Teslas across Fort Lauderdale, from Las Olas and Victoria Park to the beach. Installs are done at our Doral shop, a quick drive south on I-95. Call (786) 505-6162 to book."),
      ("Is salt air near the beach bad for my Tesla?",
       "Yes. Coastal salt air leaves residue that bonds to paint and glass. A ceramic coating plus PPF makes it far easier to rinse off and protects the finish from the corrosive effects of living near the water."),
      ("Where do you install, and how far is it from Fort Lauderdale?",
       "All work is done in our controlled Doral shop for a flawless result. It is roughly 30 to 40 minutes south on I-95 or the Turnpike. Most clients drop off and we coordinate around their schedule.")]},
  "hollywood": {"name": "Hollywood", "county": "broward", "img": "cars/model-y/model-y-2",
    "lead": "Between the Broadwalk and the Turnpike, a Hollywood Tesla sees beach salt and highway grit in the same day. Here is how we keep it flawless.",
    "intro": [
      "Tesla Boutique Miami provides premium paint protection film, ceramic coating and window tint built exclusively for Tesla owners in Hollywood, FL. From the Hollywood Beach Broadwalk to Young Circle and the neighborhoods along the Turnpike, a Hollywood Tesla lives between salt air off the Atlantic and gravel-strewn commuter highways, with sun beating down year-round.",
      "We protect Hollywood Teslas with genuine XPEL paint protection film where chips happen, Fusion Plus ceramic coating to shrug off beach residue and make washing easy, and XPEL Prime XR Plus ceramic tint to keep the cabin cool. Every install uses model-specific patterns registered to your VIN. Our Doral shop is a short drive south."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Do you protect Teslas in Hollywood, FL?",
       "Yes, we serve Tesla owners throughout Hollywood, from the beach and Broadwalk to Young Circle and West Hollywood. Installs are at our nearby Doral shop. Call (786) 505-6162."),
      ("My Tesla is parked near Hollywood Beach. What do you recommend?",
       "Near the beach, the salt air is the main enemy. We recommend a ceramic coating to make salt residue easy to rinse, plus PPF on the front to stop chips. Ceramic tint keeps the cabin cool."),
      ("How much does Tesla PPF cost for a Hollywood owner?",
       "It depends on coverage; full-front vs full-body PPF, tint and ceramic are separate services you can combine. Call (786) 505-6162 for a quote tailored to your Tesla.")]},
  "pembroke-pines": {"name": "Pembroke Pines", "county": "broward", "img": "cars/model-3/model-3-grey-3",
    "lead": "A commuter's Tesla in Pembroke Pines racks up highway miles on I-75 and Pines Boulevard. That is exactly where paint protection pays off.",
    "intro": [
      "Tesla Boutique Miami offers premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across Pembroke Pines, FL. As one of Broward's largest family suburbs, Pembroke Pines means real daily mileage, on I-75, Pines Boulevard and the Turnpike, where gravel and construction debris chip a soft factory clear coat, plus long hours parked under the Florida sun.",
      "We protect Pembroke Pines Teslas with genuine XPEL film on the hood, fenders and bumper that take the most impacts, XPEL Prime XR Plus ceramic tint to fight the heat in driveways and lots, and Fusion Plus ceramic coating for gloss and easy washing. Model-specific patterns, registered to your VIN. Our Doral shop is a short hop down I-75 or the Turnpike."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Do you serve Pembroke Pines?",
       "Yes, we protect Teslas throughout Pembroke Pines. Installs are done at our Doral shop, an easy drive via I-75 or the Turnpike. Call (786) 505-6162 to schedule."),
      ("I commute a lot on I-75. Is PPF worth it?",
       "Definitely. High highway mileage is exactly when rock chips accumulate. Full-front PPF shields the panels that take the most fire and keeps your Tesla's paint, and resale value, intact."),
      ("Does ceramic tint help in a hot Pembroke Pines driveway?",
       "Yes. XPEL Prime XR Plus rejects up to 98% of infrared heat, so a Tesla parked in an open driveway or lot stays far cooler and the interior is protected from UV fading.")]},
  "weston": {"name": "Weston", "county": "broward", "img": "cars/model-x/model-x-red-2",
    "lead": "Manicured, gated and detail-conscious. Weston Tesla owners want their cars as immaculate as their neighborhoods, and we deliver exactly that.",
    "intro": [
      "Tesla Boutique Miami brings premium paint protection film, ceramic coating and window tint, exclusively for Tesla, to owners throughout Weston, FL. Known for its planned, manicured communities at the western edge of Broward near I-75 and the Everglades, Weston is home to discerning owners who expect a flawless finish, and to long commutes that expose a Tesla to highway debris and intense sun.",
      "We protect Weston Teslas with meticulous, edge-wrapped XPEL film, Fusion Plus ceramic coating for a deep, easy-clean gloss, and XPEL Prime XR Plus ceramic tint for comfort and UV protection. Every install uses model-specific patterns and is registered to your VIN. Our Doral shop is a straight run south on I-75."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Weston Tesla owners?",
       "Yes, we protect Teslas throughout Weston. Installs are done at our Doral shop, a straight drive south on I-75. Call (786) 505-6162 to book."),
      ("I want a showroom finish. What gives the best gloss?",
       "Paint correction followed by a Fusion Plus ceramic coating delivers the deepest, glassiest finish, and the coating makes the car far easier to keep clean. Add PPF up front to stop chips."),
      ("Is full-body PPF popular in Weston?",
       "Yes. For owners who keep their Tesla pristine and protect resale, full-body film covers every painted panel. We pattern it precisely with wrapped edges."),
      ("We commute from Weston on the Turnpike and I-75 in our Model Y. What is the smart protection?",
       "That is the classic Weston setup: a family Model Y logging real daily miles at the west edge of Broward on the Florida Turnpike and I-75, where highway gravel and debris chip the front end. Full-front or track PPF on the hood, fenders, mirrors and bumper is the smart buy, and ceramic tint keeps the cabin cool for the kids on the drive home.")]},
  "miramar": {"name": "Miramar", "county": "broward", "img": "cars/model-y/model-y-white-1",
    "lead": "A growing Miramar Tesla spends its life on the Turnpike and I-75. Protect the paint before the highway miles add up.",
    "intro": [
      "Tesla Boutique Miami provides premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across Miramar, FL. As one of South Florida's fastest-growing suburbs, Miramar means commuting, on the Turnpike, I-75 and Miramar Parkway, where gravel and debris chip factory paint, plus year-round sun on cars parked in the open.",
      "We protect Miramar Teslas with genuine XPEL film on the high-impact front end, XPEL Prime XR Plus ceramic tint to cut heat and UV, and Fusion Plus ceramic coating for gloss and easy cleaning. Patterns are model-specific and registered to your VIN. Our Doral shop is just minutes away to the south."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Do you serve Miramar?",
       "Yes, we protect Teslas throughout Miramar, and our Doral shop is only minutes south. Call (786) 505-6162 to schedule your install."),
      ("I just got a new Tesla in Miramar. When should I get PPF?",
       "Before the first long highway drive. Protecting factory-fresh paint means the finish under the film stays perfect. Bring it in early and we will have genuine XPEL ready."),
      ("What is the closest Tesla protection shop to Miramar?",
       "Our Doral shop is one of the closest dedicated Tesla protection studios, just a short drive south. We are Tesla-only and an XPEL exclusive dealer.")]},
  # ----- Palm Beach -----
  "boca-raton": {"name": "Boca Raton", "county": "palm-beach", "img": "cars/model-s/model-s-blue-3",
    "lead": "Golf, gated communities and an eye for detail. Boca Raton Tesla owners expect perfection, and XPEL protection delivers it.",
    "intro": [
      "Tesla Boutique Miami offers premium paint protection film, ceramic coating and window tint, built exclusively for Tesla, to owners throughout Boca Raton, FL. From Mizner Park to the gated golf communities and the A1A coastline, Boca is synonymous with high standards, and its mix of coastal salt air and sun-drenched parking is hard on an unprotected Tesla.",
      "We protect Boca Raton Teslas with meticulous XPEL paint protection film, Fusion Plus ceramic coating that keeps salt and grime from bonding, and XPEL Prime XR Plus ceramic tint for comfort and UV defense. Every install uses model-specific patterns and is registered to your VIN. We are an easy run down I-95 from Boca."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Boca Raton Tesla owners?",
       "Yes. We protect Teslas across Boca Raton, from Mizner Park to the coastal communities. Installs are at our Doral shop, a straightforward drive south on I-95. Call (786) 505-6162."),
      ("What protection keeps a Tesla looking showroom-perfect in Boca?",
       "A combination: PPF to stop chips, a Fusion Plus ceramic coating for deep gloss and easy cleaning, and ceramic tint for the sun. Together they keep the car immaculate year-round."),
      ("Is the drive from Boca to your shop worth it?",
       "Our clients think so. We are Tesla-only, an XPEL exclusive dealer, and we document every install. Most drop the car and we coordinate timing for the drive down.")]},
  "west-palm-beach": {"name": "West Palm Beach", "county": "palm-beach", "img": "cars/model-3/model-3-grey-4",
    "lead": "Downtown energy and waterfront views. A West Palm Beach Tesla deals with city miles and coastal sun in equal measure.",
    "intro": [
      "Tesla Boutique Miami provides premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across West Palm Beach, FL. From Clematis Street and downtown to the Intracoastal waterfront, a West Palm Tesla sees busy city driving, coastal salt air and strong year-round sun, a combination that chips paint and bakes cabins.",
      "We protect West Palm Beach Teslas with genuine XPEL film on the front-end impact zones, Fusion Plus ceramic coating for easy cleaning and gloss, and XPEL Prime XR Plus ceramic tint to cut the heat. Model-specific patterns, registered to your VIN. Our Doral shop is a clear run south on I-95 or the Turnpike."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("Do you protect Teslas in West Palm Beach?",
       "Yes, we serve Tesla owners throughout West Palm Beach. Installs are at our Doral shop via I-95 or the Turnpike. Call (786) 505-6162 to book."),
      ("Does the waterfront salt air affect my Tesla?",
       "Yes. Salt residue from the Intracoastal and ocean bonds to paint and glass. A ceramic coating makes it far easier to rinse off and protects the finish; PPF guards against chips."),
      ("How much to protect a Tesla from West Palm Beach?",
       "Pricing depends on the coverage you choose. Call (786) 505-6162 and we will build a PPF, tint and ceramic package around how you use the car.")]},
  "delray-beach": {"name": "Delray Beach", "county": "palm-beach", "img": "cars/model-y/model-y-3",
    "lead": "Atlantic Avenue, the beach and the sun. A Delray Beach Tesla is a beach-town car, and beach-town cars need real protection.",
    "intro": [
      "Tesla Boutique Miami brings premium paint protection film, ceramic coating and window tint, exclusively for Tesla, to owners throughout Delray Beach, FL. Between Atlantic Avenue, the beach and the coastal neighborhoods, a Delray Tesla lives in salt air and sun, the two things hardest on automotive paint and interiors.",
      "We protect Delray Beach Teslas with genuine XPEL film against chips, Fusion Plus ceramic coating so salt and sand rinse away instead of etching the finish, and XPEL Prime XR Plus ceramic tint to block heat and UV. Patterns are model-specific and registered to your VIN. Our shop is a straightforward drive south in Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Delray Beach?",
       "Yes, we protect Teslas throughout Delray Beach, from Atlantic Avenue to the coastal neighborhoods. Installs are at our Doral shop. Call (786) 505-6162."),
      ("Is ceramic coating a good idea for a beach-town Tesla?",
       "Absolutely. In a salt-and-sand environment like Delray, a ceramic coating makes residue easy to rinse, adds UV resistance and keeps the gloss looking fresh between washes."),
      ("Do you use genuine XPEL on Delray Teslas?",
       "Always. As an XPEL exclusive dealer we install only genuine XPEL film and coatings, registered to your Tesla's VIN with the full manufacturer warranty.")]},
  "wellington": {"name": "Wellington", "county": "palm-beach", "img": "cars/model-x/model-x-red-4",
    "lead": "Equestrian country, manicured and refined. Wellington Tesla owners hold their cars to a high standard, and so do we.",
    "intro": [
      "Tesla Boutique Miami offers premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners across Wellington, FL. Known for its equestrian estates and manicured communities, Wellington pairs refined tastes with real driving, long roads, open sun and the dust and debris of a semi-rural setting at the edge of Palm Beach County.",
      "We protect Wellington Teslas with meticulous XPEL paint protection film, Fusion Plus ceramic coating for an easy-clean, high-gloss finish, and XPEL Prime XR Plus ceramic tint for comfort under the open sky. Every install uses model-specific patterns and is registered to your VIN. We are a clear run south from Wellington."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Wellington Tesla owners?",
       "Yes, we protect Teslas throughout Wellington. Installs are done at our Doral shop. Call (786) 505-6162 and we will coordinate timing for the drive."),
      ("Does dust and open-road debris matter for my Tesla?",
       "It does. Open roads and a semi-rural setting mean more airborne grit and chips. PPF protects the front-end impact zones and a ceramic coating keeps dust from bonding to the paint."),
      ("What is the best protection for a low-maintenance, glossy finish?",
       "A ceramic coating over corrected paint gives the deepest gloss and the easiest upkeep. Add front PPF to stop chips and your Tesla stays showroom-fresh with minimal effort.")]},
  "jupiter": {"name": "Jupiter", "county": "palm-beach", "img": "cars/cybertruck/cybertruck-4-white",
    "lead": "Lighthouse, beaches and boating. At the northern tip of our service area, a Jupiter Tesla lives in salt air and sun.",
    "intro": [
      "Tesla Boutique Miami provides premium paint protection film, ceramic coating and window tint, built exclusively for Tesla, to owners in Jupiter, FL. From the Jupiter Inlet Lighthouse to the beaches and the boating communities along the Loxahatchee, a Jupiter Tesla is constantly exposed to coastal salt air and strong sun at the northern edge of Palm Beach County.",
      "We protect Jupiter Teslas with genuine XPEL film against chips and debris, Fusion Plus ceramic coating that makes salt residue easy to rinse, and XPEL Prime XR Plus ceramic tint to cut heat and UV. Patterns are model-specific and registered to your VIN. We serve Jupiter owners by appointment at our Doral shop."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Jupiter, FL Tesla owners?",
       "Yes. Jupiter is at the northern edge of our service area; we protect Teslas there by appointment at our Doral shop. Call (786) 505-6162 and we will coordinate timing."),
      ("Is salt air from the inlet and ocean hard on a Tesla?",
       "Yes. Coastal salt bonds to paint and glass and accelerates wear. A ceramic coating plus PPF gives a protective, easy-clean barrier that handles the coastal environment far better than bare paint."),
      ("Is the drive from Jupiter worth it?",
       "For owners who want a Tesla-only, XPEL exclusive specialist, yes. Most drop the car and we coordinate the visit. We document every install so you see exactly the finish.")]},
  # ----- Monroe (The Keys) -----
  "key-west": {"name": "Key West", "county": "monroe", "img": "cars/cybertruck/cybertruck-5-white",
    "lead": "The southernmost city in the US, all salt air and sun. A Key West Tesla is gorgeous and seriously exposed.",
    "intro": [
      "Tesla Boutique Miami brings premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners in Key West, FL. At the very end of the Overseas Highway, Key West is surrounded by ocean on all sides, which means relentless salt air, blinding sun and humidity, about the harshest environment a vehicle can live in.",
      "We protect Key West Teslas with genuine XPEL film against sun and road debris, Fusion Plus ceramic coating that makes salt residue rinse off and adds UV and chemical resistance, and XPEL Prime XR Plus ceramic tint to cut the open-sky heat. Patterns are model-specific and registered to your VIN. We serve Keys owners by appointment; reach out and we will coordinate the drive up to Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Key West Tesla owners?",
       "Yes, we protect Teslas for Key West owners by appointment. Because installs are done at our Doral shop, we coordinate timing for the drive up US-1. Call (786) 505-6162."),
      ("Is the Key West environment really that hard on a Tesla?",
       "Yes. Surrounded by ocean, Key West subjects a car to constant salt air, intense UV and humidity. Ceramic coating plus PPF is the most effective defense, and ceramic tint protects the interior."),
      ("How does service work if I am in the Keys?",
       "We arrange a convenient drop-off window at our Doral shop and plan the work around your trip up the Overseas Highway, so the drive happens once and your Tesla comes back fully protected.")]},
  "key-largo": {"name": "Key Largo", "county": "monroe", "img": "cars/model-y/model-y-white-2",
    "lead": "The diving capital and gateway to the Keys. A Key Largo Tesla starts every trip on US-1, in full sun and salt air.",
    "intro": [
      "Tesla Boutique Miami offers premium paint protection film, ceramic coating and window tint, exclusively for Tesla, to owners in Key Largo, FL. As the first island in the chain and the gateway to the Keys, Key Largo means life on US-1, surrounded by water, sun and salt that work relentlessly on automotive paint, glass and interiors.",
      "We protect Key Largo Teslas with genuine XPEL film against the sun and road debris of the Overseas Highway, Fusion Plus ceramic coating so salt rinses off easily, and XPEL Prime XR Plus ceramic tint to block heat and UV. Patterns are model-specific and registered to your VIN. We are the closest Keys community to our Doral shop; reach out to coordinate."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Key Largo?",
       "Yes. Key Largo is the closest Keys community to our Doral shop. We protect Teslas there by appointment and coordinate timing for the drive up US-1. Call (786) 505-6162."),
      ("What protection is best for a Tesla in the Keys?",
       "Ceramic coating plus PPF. The coating fights salt and UV and keeps the car easy to rinse; PPF stops chips on the long US-1 miles. Ceramic tint keeps the cabin cool."),
      ("Can you protect my new Tesla before I take it to the Keys?",
       "Ideally yes. Protecting factory-fresh paint before the salt and sun of island life keeps the finish underneath perfect. Bring it in early and we will have genuine XPEL ready.")]},
  "islamorada": {"name": "Islamorada", "county": "monroe", "img": "cars/model-s/model-s-blue-4",
    "lead": "The sport-fishing village of islands. An Islamorada Tesla is a coastal car through and through, and needs protection to match.",
    "intro": [
      "Tesla Boutique Miami provides premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners in Islamorada, FL. Strung across several islands in the Upper Keys, Islamorada is all waterfront, which means constant salt air, strong sun and the open exposure of life along the Overseas Highway.",
      "We protect Islamorada Teslas with genuine XPEL film against debris and UV, Fusion Plus ceramic coating that keeps salt from bonding to the finish, and XPEL Prime XR Plus ceramic tint to cut the heat. Patterns are model-specific and registered to your VIN. We serve Islamorada owners by appointment at our Doral shop."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Islamorada Tesla owners?",
       "Yes, by appointment. Installs are done at our Doral shop, so we coordinate timing for the drive up US-1 from the Upper Keys. Call (786) 505-6162."),
      ("Why does a coastal Tesla need ceramic coating?",
       "Salt air and sun are relentless in Islamorada. A ceramic coating makes salt residue easy to rinse, adds UV and chemical resistance, and keeps the gloss looking fresh far longer than wax."),
      ("Do you only work on Teslas?",
       "Yes. We are a Tesla-only studio and an XPEL exclusive dealer, so every pattern, product and process is tuned specifically for Tesla, including yours in the Keys.")]},
  "marathon": {"name": "Marathon", "county": "monroe", "img": "cars/model-x/model-x-red-5",
    "lead": "Middle Keys, the Seven Mile Bridge and open water on both sides. A Marathon Tesla lives in salt air and sun.",
    "intro": [
      "Tesla Boutique Miami brings premium paint protection film, ceramic coating and window tint, built exclusively for Tesla, to owners in Marathon, FL. In the heart of the Middle Keys near the Seven Mile Bridge, Marathon is surrounded by open water, which means a Tesla here faces constant salt air, intense sun and the long highway miles of island living.",
      "We protect Marathon Teslas with genuine XPEL film against road debris and UV, Fusion Plus ceramic coating so salt rinses away easily, and XPEL Prime XR Plus ceramic tint to block the open-sky heat. Patterns are model-specific and registered to your VIN. We serve Marathon owners by appointment at our Doral shop."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Marathon in the Keys?",
       "Yes, by appointment. Because installs are at our Doral shop, we coordinate timing for the drive up the Overseas Highway. Call (786) 505-6162 to plan it."),
      ("Is salt air across the Seven Mile Bridge bad for my Tesla?",
       "Open water on both sides means heavy salt exposure. A ceramic coating plus PPF gives the best protection: easy salt rinse-off, UV resistance and chip defense for the long highway miles."),
      ("How long does protection take if I drive up from Marathon?",
       "We plan the work around a single trip: drop the car at our Doral shop, and we complete the PPF, tint or ceramic so it comes back fully protected. Timelines depend on coverage; we confirm up front.")]},
  "tavernier": {"name": "Tavernier", "county": "monroe", "img": "cars/model-3/model-3-grey-5",
    "lead": "A quiet Upper Keys community on US-1. A Tavernier Tesla still faces the salt air and sun of island life every day.",
    "intro": [
      "Tesla Boutique Miami offers premium, Tesla-only paint protection film, ceramic coating and window tint to Tesla owners in Tavernier, FL. A residential community in the Upper Keys just south of Key Largo, Tavernier means everyday life on US-1, surrounded by water and sun, with salt air working constantly on paint, glass and interiors.",
      "We protect Tavernier Teslas with genuine XPEL film against chips and UV, Fusion Plus ceramic coating that makes salt easy to rinse off, and XPEL Prime XR Plus ceramic tint to cut heat and protect the interior. Patterns are model-specific and registered to your VIN. We serve Tavernier owners by appointment at our Doral shop."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("Do you serve Tavernier Tesla owners?",
       "Yes, by appointment. Tavernier is in the Upper Keys, a manageable drive up US-1 to our Doral shop. Call (786) 505-6162 and we will coordinate timing."),
      ("What is the most important protection for a Keys Tesla?",
       "A ceramic coating to handle salt and UV, paired with PPF on the front to stop chips on the long US-1 miles. Ceramic tint keeps the cabin cool under the island sun."),
      ("Do you install genuine XPEL products?",
       "Always. As an XPEL exclusive dealer we use only genuine XPEL film and coatings, registered to your Tesla's VIN with the full manufacturer warranty.")]},
}

def sa_postcard(prefix, href, img, pills, title, text, cta="Explore"):
    pill_html = "".join(f'<span class="pill">{p}</span>' for p in pills)
    img_html = pic(prefix, img, f"{title} - Tesla protection by Tesla Boutique Miami", 700, 438)
    if href:
        return (f'<a class="project-tile reveal" href="{href}">{img_html}'
                f'<div class="project-tile-body"><div class="tag-row">{pill_html}</div>'
                f'<h3>{title}</h3><p>{text}</p><span class="card-link">{cta} &rarr;</span></div></a>')
    return (f'<div class="project-tile reveal">{img_html}'
            f'<div class="project-tile-body"><div class="tag-row">{pill_html}</div>'
            f'<h3>{title}</h3><p>{text}</p>'
            f'<span class="card-link" style="opacity:.55">Coming soon</span></div></div>')

def sa_why_block(place):
    return ('<section class="section section-grad"><div class="container">'
            '<div class="section-header"><span class="section-tag">Why Tesla Boutique Miami</span>'
            '<h2 class="section-title">Why choose Tesla Boutique Miami?</h2></div><div class="why-grid">'
            '<div class="why-item reveal"><span class="why-number">01</span><h3>Tesla Specialists Only</h3>'
            f'<p>We work exclusively on Tesla. We know every panel, sensor and camera placement on Model 3, Y, S, X and Cybertruck, so {place} owners get patterns made for Tesla, not adapted.</p></div>'
            '<div class="why-item reveal"><span class="why-number">02</span><h3>XPEL Exclusive Dealer</h3>'
            '<p>Authorized XPEL exclusive dealer with 15+ years installing PPF, ceramic and films. Only genuine XPEL products, with full manufacturer warranty registered to your VIN.</p></div>'
            '<div class="why-item reveal"><span class="why-number">03</span><h3>Built for South Florida</h3>'
            f'<p>Salt air, intense sun and debris-strewn roads are exactly what we protect against every day. Our recommendations are tuned to how Teslas actually get driven in {place}.</p></div>'
            '<div class="why-item reveal"><span class="why-number">04</span><h3>Flawless, Documented Work</h3>'
            '<p>Meticulous edge wraps, a controlled install bay in Doral, and every project photographed, so you see exactly the finish that comes out of our shop.</p></div>'
            '</div></div></section>')

def sa_cta(prefix, title, desc):
    return (f'<section class="cta-section"><div class="container"><div class="cta-content">'
            f'<h2 class="cta-title">{title}</h2><p class="cta-desc">{desc}</p>'
            f'<div class="cta-buttons">'
            f'<a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">{PHONE_DISP}</a>'
            f'<a href="{prefix}index.html#contact" class="btn btn-outline btn-lg">Send an inquiry</a>'
            f'<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Book via Unlimited Wraps</a>'
            f'</div></div></div></section>')

def build_service_area_hub():
    path = "service-area/index.html"
    prefix = "../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"), ("Service Area", "")])
    hero = page_hero(prefix, "cars/model-s/model-s-blue-1", 'Tesla <span class="highlight">Service Area</span> in South Florida',
        "Tesla Boutique Miami protects Teslas across South Florida. Find your county and city to see how we keep your Tesla flawless in your area.", "", crumbs)
    intro = ('<section class="section"><div class="container"><div class="prose">'
             '<h2>Where we protect Teslas</h2>'
             '<p>Based in Doral, Tesla Boutique Miami serves Tesla owners throughout South Florida with genuine XPEL paint protection film, ceramic coating, window tint and custom wraps. We have organized our service area by county and city so you can see exactly how we protect Teslas where you live and drive: the local roads, the climate and the everyday hazards your Model 3, Y, S, X or Cybertruck faces.</p>'
             '<p>Choose your county below to get started. Each area links to the cities we serve, with local detail and the services we recommend most.</p>'
             '</div></div></section>')
    cards = ""
    for c in COUNTIES:
        live = bool(c["cities"])
        href = f"{prefix}service-area/{c['slug']}/index.html" if live else ""
        n = len(c["cities"])
        text = c["lead"] if live else c["lead"] + " Coming soon."
        cards += sa_postcard(prefix, href, c["img"], [c["tag"]], c["name"], text,
                             cta=f"Explore {c['short']}")
    grid = (f'<section class="section section-alt"><div class="container">'
            f'<div class="section-header"><span class="section-tag">By county</span>'
            f'<h2 class="section-title">Choose your county</h2></div>'
            f'<div class="project-list-grid">{cards}</div></div></section>')
    cta = sa_cta(prefix, "Protect your Tesla, wherever you are in South Florida",
                 "Tell us your Tesla and your city, and we will recommend the right PPF, tint and ceramic package and a convenient time at our Doral shop.")
    body = hero + intro + grid + cta
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Service Area", f"{DOMAIN}/service-area/index.html")]),
          json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
            "name": "Tesla Boutique Miami Service Area", "url": f"{DOMAIN}/service-area/index.html",
            "description": "Counties and cities served by Tesla Boutique Miami for Tesla PPF, ceramic coating and window tint across South Florida."}, ensure_ascii=False)]
    title = "Tesla Service Area in Miami &amp; South Florida | Tesla Boutique Miami"
    desc = "Tesla Boutique Miami serves Tesla owners across South Florida with XPEL PPF, ceramic coating and window tint. Find your county and city, from Miami-Dade to the Keys. Call (786) 505-6162."
    return doc(path, title, desc, body, active="area", preload="cars/model-s/model-s-blue-1", extra_ld=ld)

def build_county(c):
    slug = c["slug"]
    path = f"service-area/{slug}/index.html"
    prefix = "../../"
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                       ("Service Area", prefix + "service-area/index.html"), (c["name"], "")])
    hero = page_hero(prefix, c["img"], f'Tesla protection in <span class="highlight">{c["name"]}</span>',
                     c["lead"], "", crumbs)
    intro = "".join(f"<p>{p}</p>" for p in c["intro"])
    intro_sec = (f'<section class="section"><div class="container"><div class="prose">'
                 f'<h2>Protecting Teslas across {c["short"]}</h2>{intro}</div></div></section>')
    cards = ""
    for cs in c["cities"]:
        ci = CITIES[cs]
        cards += sa_postcard(prefix, f"{prefix}service-area/{slug}/{cs}.html", ci["img"],
                             [ci["name"]], ci["name"] + ", FL",
                             ci["lead"], cta=f"Tesla protection in {ci['name']}")
    grid = (f'<section class="section section-alt"><div class="container">'
            f'<div class="section-header"><span class="section-tag">Cities we serve</span>'
            f'<h2 class="section-title">Find your city in {c["short"]}</h2></div>'
            f'<div class="project-list-grid">{cards}</div></div></section>')
    svc = service_cards_block("What we do", "Tesla services we recommend", prefix,
                              ["paint-protection-film", "window-tint", "ceramic-coating"])
    cta = sa_cta(prefix, f"Protect your Tesla in {c['short']}",
                 "Pick your city above for local detail, or tell us your Tesla and we will recommend the right protection and a time at our Doral shop.")
    body = hero + intro_sec + grid + svc + cta
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Service Area", f"{DOMAIN}/service-area/index.html"),
                                 (c["name"], f"{DOMAIN}/service-area/{slug}/index.html")])]
    title = f'Tesla PPF, Ceramic &amp; Window Tint in {c["name"]} | Tesla Boutique Miami'
    desc = (c["lead"][:150]).rsplit(" ", 1)[0] + " XPEL PPF, ceramic and tint. Call (786) 505-6162."
    return doc(path, title, desc, body, active="area", preload=c["img"], extra_ld=ld)

def build_city(slug, d):
    county = COUNTY_BY_SLUG[d["county"]]
    path = f"service-area/{county['slug']}/{slug}.html"
    prefix = "../../"
    city = d["name"]
    crumbs = breadcrumbs_html(prefix, [("Home", prefix + "index.html"),
                                       ("Service Area", prefix + "service-area/index.html"),
                                       (county["name"], prefix + f"service-area/{county['slug']}/index.html"),
                                       (city, "")])
    ctas = (f'<div class="hero-ctas"><a href="tel:{PHONE_TEL}" class="btn btn-primary btn-lg">Get a quote</a>'
            f'<a href="{prefix}index.html#contact" class="btn btn-outline btn-lg">Send an inquiry</a></div>')
    hero = page_hero(prefix, d["img"], f'Tesla protection in <span class="highlight">{city}, FL</span>',
                     d["lead"], ctas, crumbs)
    intro = "".join(f"<p>{p}</p>" for p in d["intro"])
    intro_sec = (f'<section class="section"><div class="container"><div class="prose">'
                 f'<h2>Premium Tesla PPF, ceramic &amp; tint in {city}, FL</h2>{intro}</div></div></section>')
    svc = service_cards_block(f"For {city} Tesla owners", "Our services", prefix, d["services"])
    why = sa_why_block(city)
    fq = faq_block(d["faqs"])
    rel_chips = [chip(prefix + f"service-area/{county['slug']}/index.html", f"All of {county['short']}")]
    for cs in county["cities"]:
        if cs != slug:
            rel_chips.append(chip(prefix + f"service-area/{county['slug']}/{cs}.html", CITIES[cs]["name"]))
    rel = related_block("Nearby cities", rel_chips)
    cta = sa_cta(prefix, f"Ready to protect your Tesla in {city}?",
                 f"Tell us your model and what you are after. We will recommend the right PPF, tint or ceramic for {city} driving and set a time at our Doral shop.")
    body = hero + intro_sec + svc + why + fq + rel + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service",
        "name": f"Tesla Paint Protection, Ceramic Coating &amp; Window Tint in {city}",
        "serviceType": "Automotive paint protection film, ceramic coating and window tint",
        "brand": {"@type": "Brand", "name": "XPEL"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162",
                     "url": DOMAIN + "/", "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave",
                     "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"}},
        "areaServed": {"@type": "City", "name": city + ", FL"},
        "description": d["lead"]}, ensure_ascii=False)
    ld = [breadcrumb_ld(prefix, [("Home", DOMAIN + "/"), ("Service Area", f"{DOMAIN}/service-area/index.html"),
                                 (county["name"], f"{DOMAIN}/service-area/{county['slug']}/index.html"),
                                 (city, f"{DOMAIN}/{path}")]), service_ld, faq_ld(d["faqs"])]
    title = f'Tesla PPF, Ceramic Coating &amp; Window Tint in {city}, FL | Tesla Boutique Miami'
    desc = f'Premium Tesla paint protection film, ceramic coating and window tint for {city}, FL. Genuine XPEL, Tesla-only specialists in nearby Doral. Call (786) 505-6162.'
    return doc(path, title, desc, body, active="area", preload=d["img"], extra_ld=ld)

def main():
    pages = {}
    pages["index.html"] = build_home()
    for slug, d in MODELS.items():
        pages[f"models/{slug}.html"] = build_model(slug, d)
    pages["models/tesla-model-y-ppf-miami.html"] = build_combo()
    for slug, d in SERVICES.items():
        pages[f"services/{slug}.html"] = build_service(slug, d)
    pages["news/index.html"] = build_news()
    for slug, d in POSTS.items():
        pages[f"news/{slug}.html"] = build_post(slug, d)
    pages["guides/index.html"] = build_guides()
    for slug, d in GUIDES.items():
        pages[f"guides/{slug}.html"] = build_guide(slug, d)
    pages["service-area/index.html"] = build_service_area_hub()
    for c in COUNTIES:
        if c["cities"]:
            pages[f"service-area/{c['slug']}/index.html"] = build_county(c)
    for slug, d in CITIES.items():
        county = COUNTY_BY_SLUG[d["county"]]
        pages[f"service-area/{county['slug']}/{slug}.html"] = build_city(slug, d)
    for path, html in pages.items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)
    print("\n%d pages generated." % len(pages))

if __name__ == "__main__":
    main()
