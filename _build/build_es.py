#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spanish (ES) page generator for Tesla Boutique Miami.
Reuses data + neutral helpers from site.py, adds Spanish chrome, UI and content.
Run from the repo: python3 _build/build_es.py
Writes pages into es/models, es/services, es/projects, es/news.
"""
import os, json, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("ensite", os.path.join(ROOT, "_build", "site.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

DOMAIN, PHONE_TEL, PHONE_DISP = S.DOMAIN, S.PHONE_TEL, S.PHONE_DISP
svg, IC, MODELS_NAV = S.svg, S.IC, S.MODELS_NAV
SERVICE_CARDS = S.SERVICE_CARDS

SERVICES_NAV_ES = [
    ("paint-protection-film", "Protección de Pintura (PPF)"),
    ("colored-ppf", "PPF de Color"),
    ("ceramic-coating", "Recubrimiento Cerámico"),
    ("window-tint", "Polarizado"),
    ("windshield-protection", "Protección de Parabrisas"),
    ("paint-correction", "Corrección de Pintura"),
]
SERVICE_CARDS_ES = {
    "paint-protection-film": dict(icon=IC["ppf"], title="Protección de Pintura",
        blurb="Film XPEL autorreparable e invisible contra piedras, rayones y escombros. Cobertura frontal, track y cuerpo completo.", cta="Ver PPF"),
    "colored-ppf": dict(icon=IC["color"], title="PPF de Color",
        blurb="Cambia el color de tu Tesla y protege la pintura debajo, en acabados brillante, satinado y stealth. Totalmente reversible.", cta="Ver PPF de Color"),
    "ceramic-coating": dict(icon=IC["ceramic"], title="Recubrimiento Cerámico",
        blurb="Cerámico hidrofóbico XPEL Fusion Plus que profundiza el brillo y hace tu Tesla mucho más fácil de mantener limpio.", cta="Ver Cerámico"),
    "window-tint": dict(icon=IC["tint"], title="Polarizado",
        blurb="Polarizado cerámico XPEL Prime XR Plus, hasta 98% de rechazo de calor infrarrojo sin cambiar el aspecto de tu Tesla.", cta="Ver Polarizado"),
    "windshield-protection": dict(icon=IC["windshield"], title="Protección de Parabrisas",
        blurb="Un film ópticamente claro que ayuda a proteger el costoso parabrisas del Tesla de grietas y picaduras.", cta="Ver Parabrisas"),
    "paint-correction": dict(icon=IC["correction"], title="Corrección de Pintura",
        blurb="Pulido multietapa que elimina remolinos y restaura un acabado impecable antes del cerámico o el film.", cta="Ver Corrección"),
}

def esp_root(path):
    depth = path.count("/")
    esp = "../" * depth            # within /es to es-root
    rootp = "../" * (depth + 1)    # to site root (assets, EN pages)
    return esp, rootp

LOGO_ES = ('<span class="logo-main"><span class="logo-tesla">Tesla</span> '
           '<span class="logo-boutique">Boutique</span> <span class="logo-miami">Miami</span></span>'
           '<span class="logo-sub">Impulsado por <a href="https://unlimitedwraps.com" class="logo-uw" target="_blank" rel="noopener"><strong>UnlimitedWraps</strong></a></span>'
           '<span class="logo-sub logo-xpel">Distribuidor Exclusivo XPEL</span>')

def header_es(esp, rootp, en_path, active=""):
    md = "".join('<li><a href="%smodels/%s.html">%s</a></li>' % (esp, s, l) for s, l in MODELS_NAV)
    sd = "".join('<li><a href="%sservices/%s.html">%s</a></li>' % (esp, s, l) for s, l in SERVICES_NAV_ES)
    ac = ""
    for c in COUNTIES_ES:
        if not c["cities"]:
            continue
        cl = "".join('<li><a href="%sservice-area/%s/%s.html">%s</a></li>' % (esp, c["slug"], cs, CITIES_ES[cs]["name"]) for cs in c["cities"])
        ac += ('<li class="mega-col"><a class="mega-head" href="%sservice-area/%s/index.html">%s</a><ul>%s</ul></li>'
               % (esp, c["slug"], c["short"], cl))
    cur = lambda k: ' aria-current="page"' if active == k else ""
    return ('<header class="header" id="header"><div class="container"><div class="header-inner">'
        '<div class="logo"><a href="%sindex.html" class="logo-home-link" aria-label="Tesla Boutique Miami inicio"></a>%s</div>'
        '<button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="primary-nav">%s</button>'
        '<nav class="main-nav" id="primary-nav" aria-label="Principal"><ul class="main-nav-links">'
        '<li class="has-dropdown"><a href="%sindex.html#models"%s>Modelos Tesla</a><ul class="dropdown">%s</ul></li>'
        '<li class="has-dropdown"><a href="%sindex.html#services"%s>Servicios</a><ul class="dropdown">%s</ul></li>'
        '<li class="has-dropdown"><a href="%sservice-area/index.html"%s>Zona de Servicio</a><ul class="dropdown dropdown-mega">%s</ul></li>'
        '<li><a href="%snews/index.html"%s>Updates</a></li>'
        '<li><a href="%sindex.html#contact">Contacto</a></li></ul>'
        '<div class="lang-switch" aria-label="Idioma"><a href="%s%s">EN</a><a href="#" aria-current="true">ES</a></div></nav>'
        '<div class="header-cta"><a href="tel:%s" class="header-phone">%s<span>%s</span></a>'
        '<a href="%sindex.html#contact" class="btn btn-primary">Reservar</a></div>'
        '</div></div></header>') % (
        esp, LOGO_ES, svg('<path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>'),
        esp, cur("models"), md, esp, cur("services"), sd,
        esp, cur("area"), ac, esp, cur("news"), esp,
        rootp, en_path, PHONE_TEL, svg(IC["phone"]), PHONE_DISP, esp)

def footer_es(esp, rootp):
    md = "".join('<li><a href="%smodels/%s.html">%s</a></li>' % (esp, s, l) for s, l in MODELS_NAV)
    sd = "".join('<li><a href="%sservices/%s.html">%s</a></li>' % (esp, s, l) for s, l in SERVICES_NAV_ES[:5])
    return ('<footer class="footer"><div class="container"><div class="footer-main">'
        '<div class="footer-brand"><div class="footer-logo"><span class="logo-tesla">Tesla</span> '
        '<span class="logo-boutique">Boutique</span> <span class="logo-miami">Miami</span></div>'
        '<p>Protección de pintura, cerámico y polarizado solo para Tesla en Doral y Miami. Distribuidor exclusivo XPEL.</p>'
        '<div class="footer-powered"><span>Un servicio impulsado por </span><a href="https://www.unlimitedwraps.com" target="_blank" rel="noopener">Unlimited Wraps</a></div></div>'
        '<div class="footer-links"><h3>Modelos Tesla</h3><ul>%s</ul></div>'
        '<div class="footer-links"><h3>Servicios</h3><ul>%s</ul></div>'
        '<div class="footer-links"><h3>Horario</h3><div class="footer-hours">'
        '<div class="footer-hours-row"><span class="footer-hours-day">Lun a Vie</span><span class="footer-hours-time">9:00 a 5:30</span></div>'
        '<div class="footer-hours-row"><span class="footer-hours-day">Sábado</span><span class="footer-hours-time">Cerrado</span></div>'
        '<div class="footer-hours-row"><span class="footer-hours-day">Domingo</span><span class="footer-hours-time">Cerrado</span></div>'
        '</div></div></div>'
        '<div class="footer-bottom"><p class="footer-copyright">&copy; 2026 Tesla Boutique Miami, un servicio de Unlimited Wraps, Inc. &middot; '
        '<a href="%slegal.html" class="footer-legal-link">Aviso Legal y de Marcas</a></p>'
        '<div class="footer-socials">%s</div></div></div></footer>') % (md, sd, rootp, S.SOCIALS)

def doc_es(path, title, desc, body, active="", preload=None, extra_ld=None):
    esp, rootp = esp_root(path)
    canonical = DOMAIN + "/es/" + path
    en_url = DOMAIN + "/" + path
    preload_tag = ('<link rel="preload" as="image" type="image/avif" href="%sassets/img/%s.avif" fetchpriority="high">' % (rootp, preload)) if preload else ""
    ld = "".join('<script type="application/ld+json">%s</script>\n' % b for b in (extra_ld or []))
    fav = ('<link rel="icon" href="%sfavicon.ico" sizes="any">\n'
           '<link rel="icon" type="image/svg+xml" href="%sfavicon.svg">\n'
           '<link rel="icon" type="image/png" sizes="32x32" href="%sfavicon-32.png">\n'
           '<link rel="icon" type="image/png" sizes="16x16" href="%sfavicon-16.png">\n'
           '<link rel="apple-touch-icon" sizes="180x180" href="%sapple-touch-icon.png">\n') % (rootp, rootp, rootp, rootp, rootp)
    return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n'
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n%s'
        '<title>%s</title>\n<meta name="description" content="%s">\n'
        '<meta name="robots" content="index, follow, max-image-preview:large">\n'
        '<link rel="canonical" href="%s">\n'
        '<link rel="alternate" hreflang="en" href="%s">\n'
        '<link rel="alternate" hreflang="es" href="%s">\n'
        '<link rel="alternate" hreflang="x-default" href="%s">\n'
        '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
        '<meta property="og:type" content="website">\n<meta property="og:url" content="%s">\n'
        '<meta property="og:image" content="%s/assets/img/%s.webp">\n<meta property="og:locale" content="es_US">\n'
        '<meta property="og:site_name" content="Tesla Boutique Miami">\n<meta name="twitter:card" content="summary_large_image">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" media="print" onload="this.media=\'all\'">\n'
        '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap"></noscript>\n'
        '%s\n<link rel="stylesheet" href="%sassets/css/style.css?v=%s">\n%s</head>\n<body>\n%s\n<main>\n%s\n</main>\n%s\n'
        '<script src="%sassets/js/main.js" defer></script>\n</body>\n</html>\n') % (
        fav, title, desc, canonical, en_url, canonical, en_url, title, desc, canonical,
        DOMAIN, (preload or "model-s"), preload_tag, rootp, S.CSS_VER, ld,
        header_es(esp, rootp, path, active), body, footer_es(esp, rootp), rootp)

# ---------- ES section helpers ----------
def faq_es(items):
    rows = "".join('<div class="faq-item"><button class="faq-q">%s</button>'
                   '<div class="faq-a"><div class="faq-a-inner">%s</div></div></div>' % (q, a) for q, a in items)
    return ('<section class="section section-alt"><div class="container">'
            '<div class="section-header"><span class="section-tag">Preguntas</span>'
            '<h2 class="section-title">Preguntas frecuentes</h2></div>'
            '<div class="faq-list">%s</div></div></section>' % rows)

def packages_es(tag, title, desc, cards):
    out = []
    for c in cards:
        feats = "".join('<li>%s %s</li>' % (svg(IC["check"]), f) for f in c["items"])
        fc = " featured" if c.get("featured") else ""
        btn = "btn-primary" if c.get("featured") else "btn-outline"
        out.append('<div class="package-card%s reveal"><span class="package-badge">%s</span>'
                   '<h3>%s</h3><p class="package-price"><strong>%s</strong></p><ul>%s</ul>'
                   '<a href="tel:%s" class="btn %s">Cotizar</a></div>' % (fc, c["badge"], c["name"], c["price"], feats, PHONE_TEL, btn))
    return ('<section class="section" id="packages"><div class="container">'
            '<div class="section-header"><span class="section-tag">%s</span>'
            '<h2 class="section-title">%s</h2><p class="section-desc">%s</p></div>'
            '<div class="packages-grid">%s</div></div></section>' % (tag, title, desc, "".join(out)))

def service_cards_es(tag, title, esp, keys):
    cards = ""
    for k in keys:
        sc = SERVICE_CARDS_ES[k]
        cards += ('<div class="service-card reveal"><div class="service-icon">%s</div>'
                  '<h3>%s</h3><p>%s</p><a class="card-link" href="%sservices/%s.html">%s &rarr;</a></div>' % (
                  svg(sc["icon"]), sc["title"], sc["blurb"], esp, k, sc["cta"]))
    return ('<section class="section section-alt"><div class="container">'
            '<div class="section-header"><span class="section-tag">%s</span>'
            '<h2 class="section-title">%s</h2></div><div class="services-grid">%s</div></div></section>' % (tag, title, cards))

def spec_es(title, rows):
    trs = "".join('<tr><th>%s</th><td>%s</td></tr>' % (k, v) for k, v in rows)
    return ('<section class="section section-alt"><div class="container"><div class="prose">'
            '<h2>%s</h2><table class="spec-table">%s</table></div></div></section>' % (title, trs))

def cta_es(title, desc):
    return ('<section class="cta-section"><div class="container"><div class="cta-content">'
            '<h2 class="cta-title">%s</h2><p class="cta-desc">%s</p><div class="cta-buttons">'
            '<a href="tel:%s" class="btn btn-primary btn-lg">%s</a>'
            '<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Reservar vía Unlimited Wraps</a>'
            '</div></div></div></section>' % (title, desc, PHONE_TEL, PHONE_DISP))

def related_es(chips):
    return ('<section class="section"><div class="container">'
            '<div class="section-header left"><span class="section-tag">Relacionado</span>'
            '<h2 class="section-title">Sigue explorando</h2></div>'
            '<div class="link-cloud">%s</div></div></section>' % "".join(chips))

def crumbs_es(esp, items):
    lis = ""
    for label, href in items:
        lis += ('<li><a href="%s">%s</a></li>' % (href, label)) if href else ('<li aria-current="page">%s</li>' % label)
    return '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % lis

def chip(href, label):
    return '<a class="link-chip" href="%s">%s</a>' % (href, label)

PK = S.PKG

# ---------- ES models content ----------
MODELS_ES = {
  "model-3": dict(name="Model 3", img="cars/model-3/model-3-blue-performance", gallery=["cars/model-3/model-3-grey-2","cars/model-3/model-3-detalle","cars/model-3/model-3-grey","cars/model-3/model-3-grey-3","cars/model-3/model-3-grey-5","cars/model-3/model-3-grey-6"],
    lead="El Model 3 es el Tesla que vive en la autopista, y por eso su frente recibe el mayor castigo. Así mantenemos un Model 3 de uso diario como nuevo en Miami.",
    intro=["Como el Tesla más manejado en el sur de Florida, el Model 3 acumula kilómetros de autopista rápido, y con ellos llegan las picaduras en el capó y el parachoques, más una cabina caliente bajo el sol de Miami. La solución es puntual: protección de pintura donde ocurren los impactos, polarizado cerámico para el calor, y un recubrimiento cerámico opcional para brillo y lavado fácil.",
           "Usamos patrones XPEL cortados para el Model 3, así la cobertura es precisa, sin bordes levantados, y cada instalación queda registrada a tu VIN."],
    services=["paint-protection-film", "window-tint", "ceramic-coating"],
    packages=[
      PK("Esencial", "Protección Frontal", "PPF frontal completo",
         ["Capó y guardabarros completos", "Parachoques y espejos", "Film XPEL autorreparable", "Garantía de 10 años"]),
      PK("Más popular", "Uso Diario", "PPF frontal + polarizado cerámico",
         ["Todo lo de Protección Frontal", "Polarizado cerámico en todo el vidrio", "Cabina más fresca", "Look más limpio"], featured=True),
      PK("Máximo", "Blindaje Total", "PPF de cuerpo completo + polarizado + cerámico",
         ["Todos los paneles pintados con film", "Polarizado cerámico", "Recubrimiento Fusion Plus", "Mejor protección de reventa"]),
    ],
    specs=[("Mejor servicio de entrada", "PPF frontal completo (capó, guardabarros, espejos, parachoques)"),
           ("Calor y deslumbre", "Polarizado cerámico en todo el vidrio"),
           ("Brillo y lavado fácil", "Recubrimiento cerámico XPEL Fusion Plus"),
           ("Film", "XPEL original, patrones por modelo, garantía al VIN"),
           ("Ubicación", "Doral, FL, para todo Miami-Dade")],
    faqs=[("¿Cuánto cuesta proteger un Tesla Model 3 en Miami?",
           "Depende de la cobertura. El PPF frontal, el polarizado cerámico y el recubrimiento cerámico son servicios separados que puedes combinar. Llama al (786) 505-6162 para una cotización del Model 3."),
          ("¿Vale la pena el PPF en un Model 3?",
           "Sí. El Model 3 pasa casi toda su vida en la autopista, donde ocurren las picaduras, y su pintura de fábrica es delgada. El PPF frontal protege las zonas que reciben más impactos."),
          ("¿Pueden polarizar un Model 3 en Miami?",
           "Sí, con film cerámico XPEL Prime XR Plus que rechaza hasta el 98% del calor infrarrojo, una gran mejora de confort bajo el sol de Miami.")]),
  "model-y": dict(name="Model Y", img="cars/model-y/model-y-blue-studio", gallery=["cars/model-y/model-y-grey-2","cars/model-y/model-y-grey-3","cars/model-y/model-y-grey-1","cars/model-y/model-y-3","cars/model-y/model-y-1","cars/model-y/model-y-2","cars/model-y/model-y-detail-1","cars/model-y/model-y-white-1","cars/model-y/model-y-white-2","cars/model-y/model-y-white-3"],
    lead="El Model Y es el Tesla que más protegemos. Así blindamos su pintura, su techo de cristal y su acabado contra las calles, el sol y el desgaste de reventa de Miami.",
    intro=["El Tesla Model Y vive en la I-95, el Palmetto y el Turnpike, justo donde la arena y la grava pican una capa transparente de fábrica blanda. Suma el UV implacable y el calor de la tarde, y un Model Y sin protección empieza a mostrar picaduras en el capó, remolinos en la pintura y una cabina caliente bajo el techo panorámico de cristal.",
           "Nuestro enfoque: protección de pintura donde ocurren los impactos, recubrimiento cerámico para brillo y lavado fácil, y polarizado cerámico para mantener el calor afuera. Cada servicio usa patrones XPEL cortados para el Model Y."],
    services=["paint-protection-film", "window-tint", "ceramic-coating"],
    packages=[
      PK("Esencial", "Protección Frontal", "PPF frontal completo",
         ["Capó y guardabarros completos", "Parachoques y espejos", "Film XPEL autorreparable", "Garantía de 10 años"]),
      PK("Más popular", "Confort Completo", "PPF frontal + polarizado + cerámico",
         ["Todo lo de Protección Frontal", "Polarizado cerámico incl. techo de cristal", "Recubrimiento cerámico Fusion Plus", "Cabina fresca, mantenimiento fácil"], featured=True),
      PK("Máximo", "Blindaje Total", "PPF de cuerpo completo + polarizado + cerámico",
         ["Todos los paneles pintados con film", "Acabado brillante o stealth", "Polarizado + cerámico", "Mejor protección de reventa"]),
    ],
    specs=[("Mejor servicio de entrada", "PPF frontal completo (capó, guardabarros, espejos, parachoques)"),
           ("Calor y deslumbre", "Polarizado cerámico, incluido el techo panorámico de cristal"),
           ("Brillo y lavado fácil", "Recubrimiento cerámico XPEL Fusion Plus"),
           ("Cambio de color", "PPF de color en brillante, satinado o stealth"),
           ("Film", "XPEL original, patrones por modelo, garantía al VIN"),
           ("Ubicación", "Doral, FL, para todo Miami-Dade")],
    faqs=[("¿Cuánto cuesta proteger un Tesla Model Y en Miami?",
           "El precio depende de la cobertura. El PPF frontal, el polarizado cerámico y el recubrimiento cerámico son servicios separados que puedes combinar. Llama al (786) 505-6162 para una cotización del Model Y."),
          ("¿Qué cobertura de PPF es mejor para un Model Y?",
           "Para la mayoría recomendamos al menos un paquete frontal completo (capó, guardabarros, espejos y parachoques). Para máxima protección de reventa, el PPF de cuerpo completo cubre cada panel pintado."),
          ("¿Pueden polarizar el techo de cristal del Model Y?",
           "Sí. El techo panorámico de cristal puede recibir film cerámico XPEL para cortar el calor infrarrojo y el UV sin cambiar su aspecto."),
          ("¿Usan film XPEL original en el Model Y?",
           "Siempre. Como distribuidor exclusivo XPEL instalamos solo film y recubrimientos XPEL originales, registrados al VIN de tu Model Y.")],
    combo=("tesla-model-y-ppf-miami.html", "Model Y PPF en Miami")),
  "model-s": dict(name="Model S", img="cars/model-s/model-s-blue-studio", gallery=["cars/model-s/model-s-black-1","cars/model-s/model-s-red-2","cars/model-s/model-s-detalle","cars/model-s/model-s-detalle-2","cars/model-s/model-s-red","cars/model-s/model-s-blue-1","cars/model-s/model-s-blue-2","cars/model-s/model-s-blue-3","cars/model-s/model-s-blue-4"],
    lead="El Model S es el buque insignia de Tesla, y merece protección de buque insignia. Film de cuerpo completo, cerámico y polarizado que mantienen impecable un sedán premium.",
    intro=["Quien tiene un Model S protege una inversión importante, así que la cobertura suele ir más a fondo: protección de pintura de cuerpo completo para mantener cada panel impecable, un recubrimiento cerámico Fusion Plus para un brillo líquido, y polarizado cerámico para confort y protección UV.",
           "Tratamos el Model S como el buque insignia que es, con bordes envueltos meticulosamente y materiales XPEL originales registrados a tu VIN."],
    services=["paint-protection-film", "ceramic-coating", "window-tint"],
    packages=[
      PK("Esencial", "Protección Frontal", "PPF frontal completo",
         ["Capó y guardabarros completos", "Parachoques y espejos", "Film XPEL autorreparable", "Garantía de 10 años"]),
      PK("Más popular", "Buque Insignia", "PPF frontal + cerámico + polarizado",
         ["Film XPEL frontal completo", "Recubrimiento cerámico Fusion Plus", "Polarizado cerámico, todo el vidrio", "Acabado de brillo líquido"], featured=True),
      PK("Máximo", "Blindaje Total", "PPF de cuerpo completo + cerámico + polarizado",
         ["Todos los paneles pintados con film", "Cerámico sobre el film", "Polarizado cerámico", "Mejor protección de reventa"]),
    ],
    specs=[("Mejor para buque insignia", "PPF de cuerpo completo + cerámico"),
           ("Brillo", "XPEL Fusion Plus sobre pintura y film"),
           ("Calor y deslumbre", "Polarizado cerámico, todo el vidrio"),
           ("Film", "XPEL original, garantía al VIN"),
           ("Ubicación", "Doral, FL, para todo Miami-Dade")],
    faqs=[("¿Debería poner PPF de cuerpo completo en un Model S?",
           "Para un buque insignia que piensas conservar, sí. El film de cuerpo completo mantiene cada panel sin picaduras y protege la reventa muy por encima del costo de repintar."),
          ("¿Pueden poner cerámico sobre el PPF en un Model S?",
           "Sí. Un recubrimiento cerámico Fusion Plus va sobre pintura y film para un acabado uniforme, fácil de limpiar y de alto brillo."),
          ("¿Cuánto cuesta proteger un Model S en Miami?",
           "Depende de la cobertura. Llama al (786) 505-6162 y armamos un paquete según cómo usas el auto.")]),
  "model-x": dict(name="Model X", img="cars/model-x/model-x-red-studio", gallery=["cars/model-x/model-x-red-1","cars/model-x/model-x-red-2","cars/model-x/model-x-red-3","cars/model-x/model-x-red-4","cars/model-x/model-x-red-5","cars/model-x/model-x-red-6"],
    lead="Superficies grandes, puertas tipo halcón y un parabrisas panorámico. El Model X tiene más que proteger, y lo cubrimos todo con XPEL original.",
    intro=["El Model X tiene paneles grandes y puertas falcon-wing únicas, lo que significa más superficie pintada expuesta a picaduras y más bordes que envolver correctamente. Aquí es popular el PPF de cuerpo completo o frontal extendido, junto con polarizado cerámico para la gran área de vidrio y un recubrimiento cerámico para el brillo.",
           "Patrónamos el Model X con precisión, incluidos los bordes de las puertas que muchos instaladores apuran, y registramos cada instalación a tu VIN."],
    services=["paint-protection-film", "ceramic-coating", "window-tint"],
    packages=[
      PK("Esencial", "Protección Frontal", "PPF frontal completo",
         ["Capó y guardabarros completos", "Parachoques y espejos", "Film XPEL autorreparable", "Garantía de 10 años"]),
      PK("Más popular", "SUV Familiar", "PPF frontal extendido + polarizado + cerámico",
         ["Frontal completo más estribos", "Polarizado cerámico, vidrio grande", "Recubrimiento Fusion Plus", "Cabina más fresca"], featured=True),
      PK("Máximo", "Blindaje Total", "PPF de cuerpo completo + polarizado + cerámico",
         ["Todos los paneles pintados con film", "Bordes de puertas falcon-wing", "Polarizado + cerámico", "Mejor protección de reventa"]),
    ],
    specs=[("Mejor para superficies grandes", "PPF frontal extendido o de cuerpo completo"),
           ("Calor y deslumbre", "Polarizado cerámico, gran área de vidrio"),
           ("Brillo y lavado fácil", "Recubrimiento cerámico XPEL Fusion Plus"),
           ("Film", "XPEL original, garantía al VIN"),
           ("Ubicación", "Doral, FL, para todo Miami-Dade")],
    faqs=[("¿Las puertas falcon-wing necesitan un PPF especial?",
           "Sí, los bordes y juntas de las puertas requieren un patrón cuidadoso para que el film envuelva limpio y no interfiera con el mecanismo. Lo patrónamos con precisión."),
          ("¿Vale la pena el PPF de cuerpo completo en un Model X?",
           "En un SUV grande y premium que conserva valor, el film de cuerpo completo es una opción popular. Mantiene cada panel sin picaduras y protege la reventa."),
          ("¿Pueden polarizar el gran vidrio del Model X?",
           "Sí, con film cerámico XPEL Prime XR Plus para cortar el calor y el UV en toda la gran área de vidrio.")]),
  "cybertruck": dict(name="Cybertruck", img="cars/cybertruck/cybertruck-1-black", gallery=["cars/cybertruck/cybertruck-2-black","cars/cybertruck/cybertruck-3-white","cars/cybertruck/cybertruck-4-white","cars/cybertruck/cybertruck-5-white","cars/cybertruck/cybertruck-6-white","cars/cybertruck/cybertruck-7-metallic","cars/cybertruck/cybertruck-8-metallic","cars/cybertruck/cybertruck-9-metallic","cars/cybertruck/cybertruck-10-red","cars/cybertruck/cybertruck-11-red","cars/cybertruck/cybertruck-12-red"],
    lead="Acero inoxidable, no pintura. El Cybertruck necesita otro manual, y lo tenemos: PPF para proteger el acabado y PPF de color para de verdad cambiarlo.",
    intro=["El Cybertruck es distinto a cualquier otro Tesla porque su carrocería es acero inoxidable puro, no pintada. Eso lo cambia todo: no hay capa transparente que se pique, pero el inoxidable se raya, se mancha y muestra marcas finas. La protección de pintura sobre el inoxidable lo mantiene impecable y mucho más fácil de limpiar, mientras que el PPF de color es la forma de darle al Cybertruck color real con protección debajo.",
           "Cubrimos con film los grandes paneles planos del Cybertruck con XPEL original, incluidas opciones satinadas y stealth que combinan con su diseño angular."],
    services=["paint-protection-film", "colored-ppf", "window-tint"],
    packages=[
      PK("Esencial", "Guardia de Inoxidable", "PPF frontal completo",
         ["Paneles frontales con film", "Protección antirrayas", "Más fácil de limpiar", "Garantía de 10 años"]),
      PK("Más popular", "Inoxidable Total", "PPF transparente de cuerpo completo",
         ["Todos los paneles con film", "Mantiene el inoxidable impecable", "Resiste manchas y marcas", "Film autorreparable"], featured=True),
      PK("Color", "Cybertruck de Color", "PPF de color de cuerpo completo",
         ["Color brillante, satinado o stealth", "Protección total contra impactos", "Reversible", "XPEL original"]),
    ],
    specs=[("Tipo de carrocería", "Acero inoxidable puro, no pintado"),
           ("Mantenerlo impecable", "PPF transparente de cuerpo completo sobre el inoxidable"),
           ("Cambiar el color", "PPF de color de cuerpo completo, reversible"),
           ("Calor y deslumbre", "Polarizado cerámico"),
           ("Film", "XPEL original, garantía al VIN"),
           ("Ubicación", "Doral, FL, para todo Miami-Dade")],
    faqs=[("¿Un Cybertruck necesita PPF si no tiene pintura?",
           "El inoxidable no se pica como la pintura, pero se raya y muestra huellas y marcas. El PPF transparente lo mantiene impecable y mucho más fácil de limpiar."),
          ("¿Pueden cambiar el color de un Cybertruck?",
           "Sí. El PPF de color envuelve el inoxidable en color brillante, satinado o stealth mientras lo protege debajo, y es totalmente reversible."),
          ("¿Cubren todo el Cybertruck con film?",
           "Podemos hacer cobertura frontal completa o de cuerpo completo. Los grandes paneles planos en realidad se patrónan muy bien con film XPEL original.")]),
}

# ---------- ES services content ----------
SERVICES_ES = {
  "paint-protection-film": dict(name="Protección de Pintura", img="tesla-model-3-ppf-doral",
    badge=dict(img="xpel-ultimate-plus.png", alt="Film de protección XPEL Ultimate Plus"),
    process=("Trabajo real de PPF en nuestro taller de Doral", "Protección de pintura, aplicada a mano", [
      dict(img="tesla-model-y-ppf-hood", w=1600, h=901, cls="pr-wide",
           alt="Instalador pasando el squeegee con film de protección de pintura XPEL sobre el capó de un Tesla Model Y en Doral",
           caption="Aplicando el film sobre el capó"),
      dict(img="tesla-model-y-ppf-edge", w=1600, h=766, cls="pr-wide",
           alt="Primer plano del film de protección de pintura XPEL metiéndose en el borde de un panel de un Tesla Model Y",
           caption="Metiendo el film en los bordes del panel"),
    ]),
    h1='Tesla <span class="highlight">Protección de Pintura</span>',
    lead="Film XPEL invisible y autorreparable que recibe las picaduras y rayones para que la pintura de tu Tesla no lo haga. Lo mejor que puedes hacer para mantener un Tesla como nuevo en Miami.",
    sections=[
      ("¿Qué es la protección de pintura?",
       ["La protección de pintura (PPF, o clear bra) es un film de uretano transparente y flexible adherido a las superficies pintadas de tu Tesla. Absorbe los impactos: grava, arena, ácido de insectos y abrasiones menores golpean el film en vez de la pintura. La capa superior autorreparable de XPEL va más allá, así los remolinos finos desaparecen con el calor del sol de Miami.",
        "A diferencia de un recubrimiento, el PPF tiene grosor físico real, así que es la única opción que de verdad detiene las picaduras. En un Tesla, cuya capa transparente de fábrica es famosamente blanda, esa diferencia es justo el punto."]),
      ("Por qué los dueños de Tesla eligen el PPF",
       ["<ul><li><strong>Detiene picaduras</strong> en el capó, parachoques y guardabarros.</li>"
        "<li><strong>Acabado autorreparable</strong> que borra remolinos ligeros.</li>"
        "<li><strong>Preserva el valor de reventa</strong> al proteger la pintura de fábrica.</li>"
        "<li><strong>Invisible</strong>, el film brillante desaparece.</li>"
        "<li><strong>Resistente a manchas</strong> de insectos y agua.</li></ul>"]),
      ("La tecnología y los productos XPEL que usamos",
       ["Instalamos <strong>XPEL Ultimate Plus</strong> original, el PPF autorreparable de referencia, y <strong>XPEL Stealth</strong> para un acabado satinado. Los patrones se precortan para cada modelo Tesla y luego se afinan a mano para que los bordes envuelvan limpio. Cada instalación queda registrada a tu VIN con la garantía XPEL de 10 años."]),
    ],
    options=("Opciones de cobertura", "¿Cuánto proteger?", [
      PK("Entrada", "Frontal Parcial", "Zonas de mayor impacto", ["Capó y guardabarros parciales", "Espejos", "Parachoques delantero"]),
      PK("Más popular", "Frontal Completo", "Detiene ~90% de los impactos", ["Capó y guardabarros completos", "Parachoques y espejos completos", "Faros"], featured=True),
      PK("Máximo", "Cuerpo Completo", "Cada panel pintado", ["Cobertura total", "Acabado brillante o Stealth", "Mejor protección de reventa"]),
    ]),
    faqs=[("¿Qué es la protección de pintura (PPF)?",
           "Un film de uretano transparente y duradero aplicado sobre la pintura de tu Tesla. Absorbe picaduras y rayones, y la capa autorreparable de XPEL hace que los remolinos ligeros desaparezcan con el calor."),
          ("¿Vale la pena el PPF en un Tesla?",
           "Sí. La pintura de fábrica de Tesla es relativamente blanda y se pica fácil en las autopistas de Miami. El PPF preserva el acabado y la reventa, y es mucho más barato que repintar paneles."),
          ("¿Cuánto dura el PPF de XPEL?",
           "El XPEL Ultimate Plus original tiene una garantía de fabricante de 10 años contra amarilleo, agrietamiento y desprendimiento cuando se instala profesionalmente."),
          ("¿Frontal completo o cuerpo completo?",
           "El frontal completo cubre las zonas que reciben cerca del 90% de los impactos y es lo más popular. El de cuerpo completo cubre cada panel pintado para máxima protección.")]),
  "colored-ppf": dict(name="PPF de Color", img="tesla-cybertruck-red-and-black",
    badge=dict(img="xpel-logo-solid.png", alt="Film XPEL original"),
    showcase=dict(img="colored-ppf-samples.jpg", w=1600, h=1067,
                  alt="Muestras de color y acabado de PPF XPEL", caption="Muestras reales de color y acabado XPEL"),
    h1='Tesla <span class="highlight">PPF de Color</span>',
    lead="Cambia el color de tu Tesla y protégelo a la vez. El PPF de color te da acabados brillante, satinado o stealth con protección total contra impactos, y es totalmente reversible.",
    sections=[
      ("Cambio de color que además protege",
       ["El PPF de color es protección de pintura con pigmento. Obtienes un cambio de color real en brillante, satinado o stealth mate, más la misma protección autorreparable contra picaduras del PPF transparente. Como es film, tu pintura de fábrica queda intacta debajo, lo que protege la reventa y te deja volver al original cuando quieras.",
        "Es la alternativa inteligente a un repintado o a un vinilo barato: más resistente que el vinilo, reversible a diferencia de la pintura, y protector en lugar de solo cosmético."]),
      ("Acabados y los productos XPEL que usamos",
       ["Instalamos films XPEL de color y stealth originales en una gama de tonos tipo fábrica y personalizados. En el Cybertruck en especial, el PPF de color es la forma más limpia de añadir color al inoxidable mientras lo protege."]),
    ],
    options=("Acabados populares", "Elige tu look", [
      PK("Brillante", "Color Brillante", "Color profundo tipo mojado", ["Cambio de color vívido", "Film autorreparable", "Reversible"]),
      PK("Más popular", "Satinado / Stealth", "Acabado mate tipo fábrica", ["Satinado o stealth mate", "Disimula marcas finas", "Protección total"], featured=True),
      PK("Detalles", "Acentos de Color", "Techo, espejos, molduras", ["Looks bicolor", "Acentos en negro", "Patrones precisos"]),
    ]),
    faqs=[("¿El PPF de color es mejor que el vinilo?",
           "Para la mayoría, sí. El PPF de color es más grueso y autorreparable, protege contra picaduras en vez de solo cubrir la pintura, y tiende a durar más que el vinilo."),
          ("¿El PPF de color daña la pintura de mi Tesla?",
           "No. Protege la pintura de fábrica debajo y está diseñado para retirarse limpiamente, así que puedes volver al color original."),
          ("¿Pueden cambiar el color de un Cybertruck?",
           "Sí. El PPF de color es la forma ideal de añadir color brillante, satinado o stealth al inoxidable del Cybertruck mientras lo protege.")]),
  "ceramic-coating": dict(name="Recubrimiento Cerámico", img="tesla-model-s-ceramic-coating",
    badge=dict(img="xpel-fusion-plus.png", alt="Recubrimiento cerámico XPEL Fusion Plus"),
    h1='Tesla <span class="highlight">Recubrimiento Cerámico</span>',
    lead="Una capa cerámica hidrofóbica XPEL Fusion Plus que profundiza el brillo, repele agua y suciedad, y hace tu Tesla mucho más fácil de mantener limpio.",
    sections=[
      ("Qué hace el recubrimiento cerámico",
       ["Un recubrimiento cerámico es un polímero líquido que se adhiere a la superficie de tu Tesla y cura en una capa dura, resbalosa e hidrofóbica. El agua resbala, la suciedad y los insectos cuesta que se peguen, y la pintura gana un brillo profundo y vidrioso. No es una barrera contra picaduras como el PPF, es una mejora de brillo y limpieza fácil, y los dos trabajan muy bien juntos.",
        "El cerámico también añade resistencia a UV y químicos, algo que importa bajo el sol de Miami."]),
      ("XPEL Fusion Plus y cómo lo aplicamos",
       ["Aplicamos <strong>XPEL Fusion Plus</strong> original tras una descontaminación adecuada y, donde haga falta, corrección de pintura, para que el recubrimiento fije un acabado impecable en vez de sellar remolinos. Puede aplicarse sobre pintura y sobre PPF para un look uniforme."]),
    ],
    options=None,
    faqs=[("¿El cerámico reemplaza al PPF?",
           "No. El cerámico añade brillo y limpieza fácil, pero no detiene las picaduras. Para protección contra impactos necesitas PPF. Muchos hacen PPF al frente y cerámico en todo lo demás."),
          ("¿Cuánto dura el recubrimiento cerámico?",
           "Un XPEL Fusion Plus aplicado profesionalmente dura años con el mantenimiento adecuado, mucho más que una cera o sellador."),
          ("¿Debo corregir la pintura primero?",
           "Normalmente sí. El cerámico fija lo que haya debajo, así que quitar los remolinos con corrección de pintura primero da el mejor y más profundo resultado.")]),
  "window-tint": dict(name="Polarizado", img="tesla-model-y-window-tinting",
    badge=dict(img="xpel-prime-xr-plus.png", alt="Polarizado cerámico XPEL Prime XR Plus"),
    process=("En nuestro taller de Doral", "Cómo es una instalación de polarizado Tesla", [
      dict(img="tesla-window-tint-squeegee", w=940, h=1278, cls="pr-tall",
           alt="Instalador pasando el squeegee sobre el polarizado cerámico XPEL en la ventana de un Tesla en Doral",
           caption="Pasando el squeegee para un acabado sin burbujas"),
      dict(img="tesla-window-tint-result", w=1080, h=1575, cls="pr-tall",
           alt="Ventana lateral de un Tesla con polarizado cerámico XPEL recién instalado en Doral",
           caption="El polarizado terminado, limpio y parejo"),
    ]),
    h1='Tesla <span class="highlight">Polarizado</span>',
    lead="El polarizado cerámico XPEL Prime XR Plus rechaza hasta el 98% del calor infrarrojo y bloquea el UV, manteniendo la cabina de tu Tesla fresca y cómoda bajo el sol de Miami, sin cambiar su aspecto.",
    sections=[
      ("Por qué cerámico y no film barato",
       ["El polarizado teñido barato se decolora a morado y bloquea señales. El <strong>XPEL Prime XR Plus</strong> es un film cerámico que rechaza hasta el 98% del calor infrarrojo y el 99% del UV, sin interferir señales y con color estable. En Miami, la diferencia en confort de cabina es enorme, y protege tu interior del decoloramiento.",
        "En los Tesla con techo panorámico de cristal, añadir film cerámico al techo es una de las mayores mejoras de confort posibles."]),
      ("Cobertura y los productos XPEL que usamos",
       ["Polarizamos vidrios laterales y trasero, techos panorámicos y, donde sea legal, el parabrisas, todo con film cerámico XPEL original y garantía de por vida contra decoloramiento y burbujas."]),
    ],
    options=None,
    faqs=[("¿Cuánto calor bloquea el polarizado cerámico?",
           "El XPEL Prime XR Plus rechaza hasta el 98% del calor infrarrojo, la parte de la luz solar que sientes como calor, lo que marca una diferencia real bajo el sol de Miami."),
          ("¿Pueden polarizar el techo de cristal del Tesla?",
           "Sí. Añadir film cerámico a un techo panorámico de cristal es una de las mejoras de confort más efectivas, cortando el calor sin cambiar el look."),
          ("¿El polarizado afecta las señales o cámaras de mi Tesla?",
           "No. El film cerámico no es metálico, así que no interfiere con GPS, celular ni las cámaras y sensores de Tesla.")]),
  "windshield-protection": dict(name="Protección de Parabrisas", img="tesla-windshield-protection-install",
    badge=dict(img="xpel-windshield-film.png", alt="Film de protección de parabrisas XPEL"),
    process=("En nuestro taller de Doral", "Cómo es una instalación de parabrisas Tesla", [
      dict(img="tesla-windshield-film-application", w=1080, h=706, cls="pr-wide",
           alt="Dos instaladores colocando film de protección de parabrisas XPEL sobre un Tesla en Doral",
           caption="Posicionando el film antes de pasar el squeegee"),
      dict(img="tesla-windshield-film-detail", w=1080, h=1920, cls="pr-tall",
           alt="Primer plano del film de protección de parabrisas XPEL trabajado con squeegee en un Tesla",
           caption="Eliminando la solución para un acabado ópticamente claro"),
    ]),
    h1='Tesla <span class="highlight">Protección de Parabrisas</span>',
    lead="Un film protector ópticamente claro que ayuda a proteger el costoso parabrisas de tu Tesla de impactos de piedra, grietas y picaduras, un seguro inteligente y de bajo costo.",
    sections=[
      ("Por qué proteger el parabrisas",
       ["Los parabrisas de Tesla son grandes, inclinados y costosos de reemplazar, y en algunos modelos el reemplazo también implica recalibrar cámaras. Un film de protección de parabrisas es una capa ópticamente clara que absorbe el impacto de piedras pequeñas y escombros, ayudando a evitar las picaduras y grietas que te llevan al taller de vidrios.",
        "Es una de las protecciones más costo-efectivas que puedes añadir, sobre todo para quienes manejan mucho en autopista."]),
      ("Cómo funciona",
       ["Aplicamos un film claro y duradero diseñado para vidrio que mantiene la claridad óptica y funciona con tus limpiaparabrisas y sensores. Es reemplazable, así que un film que recibe un golpe se cambia mucho más barato que el parabrisas mismo."]),
    ],
    options=None,
    faqs=[("¿El film de parabrisas afecta la visibilidad?",
           "No. Es ópticamente claro y está diseñado para mantener la visibilidad completa y funcionar normal con limpiaparabrisas, sensores de lluvia y cámaras."),
          ("¿Vale la pena en un Tesla?",
           "Si manejas autopista a menudo, sí. Reemplazar un parabrisas de Tesla es caro y puede requerir recalibrar cámaras, así que un film protector reemplazable es un seguro inteligente."),
          ("¿El film se puede reemplazar si se daña?",
           "Sí, ese es el punto. Un film dañado se cambia mucho más barato que reemplazar el vidrio del parabrisas.")]),
  "paint-correction": dict(name="Corrección de Pintura", img="tesla-model-s-ceramic-coating",
    h1='Tesla <span class="highlight">Corrección de Pintura</span>',
    lead="Pulido mecánico multietapa que elimina remolinos, rayones y opacidad para restaurar un acabado impecable tipo espejo, el primer paso correcto antes de cualquier recubrimiento o film.",
    sections=[
      ("Qué hace la corrección de pintura",
       ["La corrección de pintura es el pulido cuidadoso y multietapa de la capa transparente de tu Tesla para eliminar remolinos, rayones ligeros, manchas de agua y oxidación. El resultado es un acabado profundo, vidrioso y sin defectos que refleja limpio en vez de dispersar la luz.",
        "También es el primer paso esencial antes del cerámico o el PPF, porque esos fijan lo que haya debajo. Corrige primero, luego protege."]),
      ("Nuestro proceso",
       ["Evaluamos la pintura y usamos un proceso de pulido multietapa medido para nivelar defectos sin remover más capa transparente de la necesaria. Bien hecho, transforma cómo se ve un Tesla, sobre todo en colores oscuros."]),
    ],
    options=None,
    faqs=[("¿Necesito corrección de pintura antes del cerámico o el PPF?",
           "Normalmente sí. Los recubrimientos y el film fijan la condición actual, así que corregir los remolinos primero da un resultado final mucho mejor y más profundo."),
          ("¿La corrección adelgaza mi capa transparente?",
           "Hecho profesionalmente, removemos solo lo necesario para nivelar defectos, preservando la mayor cantidad posible de capa transparente."),
          ("¿Mi Tesla nuevo ya tiene remolinos, es normal?",
           "Lamentablemente sí, el transporte y el lavado del dealer suelen introducir remolinos. Una corrección de una etapa normalmente lleva un Tesla nuevo a un acabado realmente impecable.")]),
}

# ---------- ES builders ----------
def build_model_es(slug, d):
    path = "models/%s.html" % slug
    esp, rootp = esp_root(path); name = d["name"]
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Modelos Tesla", esp+"index.html#models"), (name, "")])
    ctas = ('<div class="hero-ctas"><a href="tel:%s" class="btn btn-primary btn-lg">Cotiza tu %s</a>'
            '<a href="#packages" class="btn btn-outline btn-lg">Ver paquetes</a></div>') % (PHONE_TEL, name)
    hero = S.page_hero(rootp, d["img"], 'Tesla <span class="highlight">%s</span> protección en Miami' % name, d["lead"], ctas, crumbs)
    intro = "".join("<p>%s</p>" % p for p in d["intro"])
    intro_sec = '<section class="section"><div class="container"><div class="prose"><h2>Protegiendo el %s en el sur de Florida</h2>%s</div></div></section>' % (name, intro)
    svc = service_cards_es("Recomendado para el %s" % name, "Servicios que sugerimos", esp, d["services"])
    pk = packages_es("Paquetes %s" % name, "Formas populares de proteger un %s" % name,
                     "Puntos de partida que la mayoría elige. Cada proyecto es a medida, el precio final se confirma con una llamada o visita.", d["packages"])
    sp = spec_es("El %s de un vistazo" % name, d["specs"])
    fq = faq_es(d["faqs"])
    chips = []
    if d.get("combo"): chips.append(chip(d["combo"][0], d["combo"][1]))
    chips += [chip(esp+"services/window-tint.html", "Polarizado Tesla"),
              chip(esp+"services/ceramic-coating.html", "Cerámico Tesla")]
    rel = related_es(chips)
    cta = cta_es("Protege tu %s" % name, "Dinos tu color y cómo manejas, y te recomendamos la combinación correcta de PPF, polarizado y cerámico para tu %s." % name)
    gallery = model_gallery_es(rootp, name, d["gallery"]) if d.get("gallery") else ""
    body = hero + intro_sec + gallery + svc + pk + sp + fq + rel + cta
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Modelos Tesla", DOMAIN+"/es/#models"), (name, "%s/es/models/%s.html" % (DOMAIN, slug))]), S.faq_ld(d["faqs"])]
    title = "Tesla %s: PPF, Cerámico y Polarizado en Miami | Tesla Boutique Miami" % name
    desc = "Protege tu Tesla %s en Miami y Doral: protección de pintura XPEL, recubrimiento cerámico y polarizado cerámico. Paquetes, proyectos y preguntas frecuentes. Llama al (786) 505-6162." % name
    return doc_es(path, title, desc, body, active="models", preload=d["img"], extra_ld=ld)

def product_badge_es(rootp, b):
    return ('<div class="product-badge"><span class="product-badge-label">Producto XPEL original</span>'
            '<img class="product-badge-logo" src="%sassets/img/%s" alt="%s"></div>' % (rootp, b["img"], b["alt"]))

def model_gallery_es(rootp, name, names):
    items = "".join(
        ('<div class="gallery-item reveal"><picture>'
         '<source srcset="%sassets/img/%s.avif" type="image/avif">'
         '<source srcset="%sassets/img/%s.webp" type="image/webp">'
         '<img src="%sassets/img/%s.webp" alt="%s" width="700" height="525" decoding="async" loading="lazy">'
         '</picture></div>') % (rootp, n, rootp, n, rootp, n, S.img_alt(n, "es")) for n in names)
    return ('<section class="section"><div class="container">'
            '<div class="section-header"><span class="section-tag">Galería %s</span>'
            '<h2 class="section-title">Trabajos reales en %s</h2></div>'
            '<div class="gallery-grid">%s</div></div></section>') % (name, name, items)

def media_showcase_es(rootp, s):
    cap = '<figcaption>%s</figcaption>' % s["caption"] if s.get("caption") else ""
    return ('<section class="section"><div class="container"><figure class="media-showcase">'
            '<img src="%sassets/img/%s" alt="%s" width="%s" height="%s" loading="lazy" decoding="async">%s</figure></div></section>' % (
            rootp, s["img"], s["alt"], s["w"], s["h"], cap))

def process_es(rootp, tag, title, items):
    figs = ""
    for it in items:
        cap = '<figcaption>%s</figcaption>' % it["caption"] if it.get("caption") else ""
        figs += '<figure class="%s">%s%s</figure>' % (it["cls"], S.pic(rootp, it["img"], it["alt"], it["w"], it["h"]), cap)
    return ('<section class="section"><div class="container">'
            '<div class="section-header"><span class="section-tag">%s</span>'
            '<h2 class="section-title">%s</h2></div>'
            '<div class="process-row">%s</div></div></section>') % (tag, title, figs)

def build_service_es(slug, d):
    path = "services/%s.html" % slug
    esp, rootp = esp_root(path); name = d["name"]
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Servicios", esp+"index.html#services"), (name, "")])
    extra = '<a href="#packages" class="btn btn-outline btn-lg">Ver más</a>' if d.get("options") else ""
    ctas = '<div class="hero-ctas"><a href="tel:%s" class="btn btn-primary btn-lg">Pedir cotización</a>%s</div>' % (PHONE_TEL, extra)
    hero = S.page_hero(rootp, d["img"], d["h1"], d["lead"], ctas, crumbs)
    secs = ""
    nsec = len(d["sections"])
    for i, (h2, paras) in enumerate(d["sections"]):
        inner = "".join(p if p.lstrip().startswith("<ul") else "<p>%s</p>" % p for p in paras)
        badge = product_badge_es(rootp, d["badge"]) if (d.get("badge") and i == nsec - 1) else ""
        secs += '<section class="section"><div class="container"><div class="prose"><h2>%s</h2>%s%s</div></div></section>' % (h2, badge, inner)
    opts = ""
    if d.get("options"):
        tag, title, cards = d["options"]
        opts = packages_es(tag, title, "Cada proyecto es a medida, el precio final se confirma con una llamada o visita.", cards)
    bymodel = ('<section class="section section-alt"><div class="container">'
               '<div class="section-header left"><span class="section-tag">Por modelo Tesla</span>'
               '<h2 class="section-title">Elige tu Tesla</h2></div><div class="link-cloud">%s</div></div></section>') % (
               "".join(chip(esp+"models/%s.html" % s, l) for s, l in MODELS_NAV))
    fq = faq_es(d["faqs"])
    cta = cta_es("¿Listo para %s?" % name, "Dinos tu Tesla y qué buscas, y te damos una cotización y tiempos claros.")
    showcase = media_showcase_es(rootp, d["showcase"]) if d.get("showcase") else ""
    proc = process_es(rootp, *d["process"]) if d.get("process") else ""
    body = hero + secs + showcase + proc + opts + bymodel + fq + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service", "name": "Tesla %s" % name,
        "serviceType": name, "brand": {"@type": "Brand", "name": "XPEL"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162", "url": DOMAIN+"/es/",
                     "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave", "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"}},
        "areaServed": [{"@type": "City", "name": "Miami"}, {"@type": "City", "name": "Doral"}],
        "description": d["lead"]}, ensure_ascii=False)
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Servicios", DOMAIN+"/es/#services"), (name, "%s/es/services/%s.html" % (DOMAIN, slug))]), service_ld, S.faq_ld(d["faqs"])]
    title = "Tesla %s en Miami y Doral | XPEL | Tesla Boutique Miami" % name
    return doc_es(path, title, d["lead"], body, active="services", preload=d["img"], extra_ld=ld)

def build_combo_es():
    path = "models/tesla-model-y-ppf-miami.html"
    esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Model Y", esp+"models/model-y.html"), ("Model Y PPF en Miami", "")])
    ctas = '<div class="hero-ctas"><a href="tel:%s" class="btn btn-primary btn-lg">Cotiza el PPF de tu Model Y</a></div>' % PHONE_TEL
    hero = S.page_hero(rootp, "tesla-model-y-window-tinting", 'Tesla Model Y <span class="highlight">PPF</span> en Miami',
        "Protección de pintura XPEL original para el Model Y, instalada en nuestro taller de Doral y para todo Miami-Dade. Cobertura de frontal a cuerpo completo, autorreparable, con garantía de 10 años.", ctas, crumbs)
    prose = ('<section class="section"><div class="container"><div class="prose">'
             '<h2>El PPF correcto para un Model Y en Miami</h2>'
             '<p>Las autopistas de Miami son duras con un Model Y. Entre la arena de construcción del Palmetto y la grava de la I-95, el capó y el parachoques delantero reciben fuego constante, y la pintura blanda de fábrica de Tesla se pica rápido. La protección de pintura es la solución: una capa XPEL transparente y autorreparable que recibe los golpes para que tu pintura quede impecable.</p>'
             '<p>Para el Model Y en específico, cortamos patrones a los paneles exactos: capó completo, guardabarros, espejos y el profundo parachoques delantero que atrapa más escombros. Quien conserva el auto a largo plazo suele extender la cobertura al cuerpo completo.</p>'
             '<h3>Lo más pedido en PPF de Model Y en Miami</h3><ul>'
             '<li><strong>Frontal completo:</strong> capó, guardabarros, espejos, parachoques, faros.</li>'
             '<li><strong>Paquete track:</strong> frontal completo más estribos y zonas de impacto traseras.</li>'
             '<li><strong>Cuerpo completo:</strong> cada panel pintado, opcionalmente en XPEL Stealth satinado.</li></ul>'
             '<p>¿Quieres el panorama completo? Ve la <a href="model-y.html">guía de protección del Tesla Model Y</a> o el <a href="../services/paint-protection-film.html">resumen del servicio de PPF</a>.</p>'
             '</div></div></section>')
    rel = related_es([chip("model-y.html", "Polarizado de Model Y en Miami"), chip("model-3.html", "PPF de Model 3 en Miami"),
                      chip("../services/paint-protection-film.html", "Sobre el PPF de XPEL")])
    cta = cta_es("Pon film a tu Model Y", "Cotización rápida para PPF frontal o de cuerpo completo en tu Model Y.")
    body = hero + prose + rel + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service",
        "name": "Protección de Pintura (PPF) para Tesla Model Y en Miami", "serviceType": "Instalación de protección de pintura",
        "brand": {"@type": "Brand", "name": "XPEL"}, "audience": {"@type": "Audience", "name": "Dueños de Tesla Model Y"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162", "url": DOMAIN+"/es/"},
        "areaServed": {"@type": "City", "name": "Miami"},
        "description": "Film de protección de pintura XPEL autorreparable instalado en el Tesla Model Y en Miami y Doral, FL."}, ensure_ascii=False)
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Model Y", DOMAIN+"/es/models/model-y.html"), ("Model Y PPF en Miami", DOMAIN+"/es/models/tesla-model-y-ppf-miami.html")]), service_ld]
    title = "Tesla Model Y PPF en Miami | Frontal y Cuerpo Completo XPEL | Tesla Boutique Miami"
    desc = "Protección de pintura (PPF) para el Tesla Model Y en Miami y Doral. Film XPEL autorreparable, frontal y cuerpo completo, garantía de 10 años. Llama al (786) 505-6162."
    return doc_es(path, title, desc, body, active="models", preload="tesla-model-y-window-tinting", extra_ld=ld)

def build_projects_index_es():
    path = "projects/index.html"; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Proyectos", "")])
    hero = S.page_hero(rootp, "tesla-cybertruck-ppf-miami", 'Proyectos <span class="highlight">Tesla</span> reales',
        "Cada Tesla que pasa por nuestro taller de Doral quedará documentado aquí: el trabajo, los productos, el resultado. Esta es la parte que ningún competidor puede copiar, porque son nuestros autos reales.", "", crumbs)
    tiles = [
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-model-y-window-tinting", ["Model Y", "PPF Frontal"],
         "Model Y, PPF Frontal + Polarizado", "Proyecto de muestra que enseña cómo se documentará cada instalación real, con fotos, servicios y productos."),
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-model-3-ppf-doral", ["Model 3", "PPF Cuerpo Completo"],
         "Model 3, PPF de Cuerpo Completo", "Próximamente. Los proyectos reales de Model 3 aparecerán aquí a medida que se completen."),
        ("sample-tesla-model-y-full-front-ppf.html", "tesla-cybertruck-red-and-black", ["Cybertruck", "PPF de Color"],
         "Cybertruck, PPF de Color", "Próximamente. Los proyectos reales de Cybertruck aparecerán aquí a medida que se completen."),
    ]
    cards = ""
    for href, img, pills, h3, p in tiles:
        ph = "".join('<span class="pill">%s</span>' % x for x in pills)
        cards += ('<a class="project-tile reveal" href="%s">%s<div class="project-tile-body"><div class="tag-row">%s</div>'
                  '<h3>%s</h3><p>%s</p><span class="card-link">Ver proyecto &rarr;</span></div></a>') % (
                  href, S.pic(rootp, img, h3+" proyecto Tesla en Miami", 700, 438), ph, h3, p)
    grid = ('<section class="section"><div class="container">'
            '<div class="section-header"><span class="section-tag">Nuestro trabajo</span><h2 class="section-title">Últimas instalaciones</h2></div>'
            '<div class="project-list-grid">%s</div>'
            '<p style="text-align:center;color:var(--gray);margin-top:40px;font-size:0.95rem">'
            'Se añaden proyectos nuevos cada semana. Este es un conjunto inicial, el archivo crece con cada Tesla que protegemos.</p></div></section>') % cards
    cta = cta_es("Tu Tesla podría ser el próximo", "Reserva tu instalación y también documentamos tu proyecto.")
    body = hero + grid + cta
    ld = [json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Proyectos de Protección Tesla",
        "url": DOMAIN+"/es/projects/index.html", "description": "Proyectos reales de PPF, cerámico y polarizado Tesla por Tesla Boutique Miami en Doral, FL."}, ensure_ascii=False)]
    return doc_es(path, "Proyectos Tesla, instalaciones reales de PPF, Cerámico y Polarizado en Miami | Tesla Boutique Miami",
                  "Explora proyectos reales de protección Tesla de nuestro taller de Doral: PPF, recubrimiento cerámico y polarizado en Model 3, Y, S, X y Cybertruck.",
                  body, active="projects", preload="tesla-cybertruck-ppf-miami", extra_ld=ld)

def build_project_sample_es():
    path = "projects/sample-tesla-model-y-full-front-ppf.html"; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Proyectos", esp+"projects/index.html"), ("Muestra, Model Y PPF Frontal", "")])
    hero = S.page_hero(rootp, "tesla-model-y-window-tinting", 'Tesla Model Y<br><span class="highlight">PPF Frontal + Polarizado Cerámico</span>',
        "Proyecto de muestra. Este es un ejemplo ilustrativo de cómo documentaremos cada Tesla real que protejamos, con fotos originales, servicios, productos y tiempo de instalación. Los proyectos reales de clientes reemplazan estos a medida que llega el trabajo.", "", crumbs)
    meta = ('<dl class="project-meta">'
            '<div><dt>Vehículo</dt><dd>Tesla Model Y</dd></div>'
            '<div><dt>Servicios</dt><dd>PPF Frontal, Polarizado Cerámico</dd></div>'
            '<div><dt>Productos</dt><dd>XPEL Ultimate Plus, Prime XR Plus</dd></div>'
            '<div><dt>Tiempo de instalación</dt><dd>2 días</dd></div>'
            '<div><dt>Ubicación</dt><dd>Doral, FL</dd></div></dl>')
    gallery = ('<div class="project-gallery">%s%s%s</div>') % (
        S.pic(rootp, "tesla-model-y-window-tinting", "Muestra de Tesla Model Y tras PPF frontal y polarizado cerámico", 1200, 675),
        S.pic(rootp, "model-s", "Detalle del borde del capó con PPF en Model Y", 700, 525),
        S.pic(rootp, "tesla-cybertruck-ppf-miami", "Tesla de muestra en la cabina de instalación de Doral", 700, 525))
    prose = ('<section class="section"><div class="container"><div class="prose wide">%s'
             '<p style="background:rgba(43,57,144,0.12);border:1px solid rgba(43,57,144,0.4);padding:14px 18px;border-radius:8px;color:var(--gray-light)"><strong>Nota:</strong> Este es un diseño de muestra, no un trabajo real de cliente. Existe para que veas exactamente cómo se verán los proyectos documentados cuando empecemos a publicar instalaciones reales.</p>'
             '<h2>El proyecto</h2>'
             '<p>Un Model Y nuevo llega directo del dealer Tesla de Doral para protección antes de su primer viaje por autopista. Proteger un Tesla antes de acumular kilómetros significa que la pintura debajo del film queda perfecta de fábrica.</p>'
             '<p>Instalamos XPEL Ultimate Plus en cobertura frontal completa: capó, ambos guardabarros, el parachoques delantero, espejos y faros, con bordes envueltos y sin costuras visibles. Luego polarizado cerámico XPEL Prime XR Plus en vidrios laterales y trasero más el techo panorámico para cortar el calor de Miami.</p>'
             '<h2>Fotos</h2>%s'
             '<h2>Servicios realizados</h2><ul>'
             '<li><a href="../services/paint-protection-film.html">Protección de pintura frontal completa</a></li>'
             '<li><a href="../services/window-tint.html">Polarizado cerámico</a>, vidrios laterales, trasero y techo</li></ul>'
             '<h2>Productos usados</h2><ul>'
             '<li><strong>XPEL Ultimate Plus</strong>, PPF transparente autorreparable, garantía de 10 años</li>'
             '<li><strong>XPEL Prime XR Plus</strong>, film cerámico para ventanas que rechaza infrarrojos</li></ul>'
             '<p style="margin-top:32px"><a href="../models/model-y.html" class="btn btn-outline">Más sobre la protección del Model Y</a></p>'
             '</div></div></section>') % (meta, gallery)
    cta = cta_es("Protege tu Model Y como este", "¿Tesla nuevo? Tráelo antes del primer viaje y mantén la pintura perfecta.")
    body = hero + prose + cta
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Proyectos", DOMAIN+"/es/projects/index.html"), ("Muestra Model Y PPF Frontal", DOMAIN+"/es/projects/sample-tesla-model-y-full-front-ppf.html")]),
          json.dumps({"@context": "https://schema.org", "@type": "CreativeWork", "name": "Muestra, Tesla Model Y PPF Frontal + Polarizado Cerámico",
            "about": "Protección de pintura y polarizado para Tesla Model Y", "creator": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "url": DOMAIN+"/es/", "telephone": "+1-786-505-6162"},
            "locationCreated": {"@type": "Place", "name": "Doral, FL"},
            "description": "Muestra ilustrativa de un proyecto documentado de PPF frontal y polarizado cerámico en un Tesla Model Y."}, ensure_ascii=False)]
    return doc_es(path, "Proyecto de muestra, Tesla Model Y PPF Frontal + Polarizado | Tesla Boutique Miami",
                  "Diseño de proyecto de muestra que enseña cómo Tesla Boutique Miami documenta cada instalación real: fotos, servicios, productos y tiempo de instalación.",
                  body, active="projects", preload="tesla-model-y-window-tinting", extra_ld=ld)

POSTS_ES = {
  "xpel-care-products": dict(
    pill="XPEL", date="Junio 2026", crumb="Productos de cuidado XPEL", img="tesla-model-s-ceramic-coating",
    title="Más allá del PPF: productos de cuidado XPEL | Tesla Boutique Miami",
    desc="Los productos de cuidado XPEL que usamos y vendemos, de Detail Spray y Ceramic Boost a PPF Cleaner e Iron Remover, para mantener tu Tesla protegido entre visitas.",
    h1='Más allá del <span class="highlight">PPF</span>: los productos XPEL que usamos y que tú también puedes usar',
    card_title="Más allá del PPF: los productos XPEL que usamos y que tú también puedes usar",
    blurb="Los productos de cuidado XPEL que usamos, vendemos y recomendamos, de Detail Spray y Ceramic Boost a PPF Cleaner e Iron Remover, para mantener tu Tesla como nuevo entre visitas.",
    lead="En Tesla Boutique hablamos mucho de PPF, recubrimiento cerámico y protección de parabrisas, porque son la base de proteger un Tesla. Pero la protección no termina el día que sale del taller. XPEL fabrica una línea de productos de cuidado que usamos a diario en el shop y que tú puedes usar en casa para que tu Tesla se mantenga como el primer día. Aquí te contamos cuáles son y para qué sirve cada uno.",
    cta_title="¿No sabes qué producto le va a tu Tesla?",
    cta_desc="Dinos qué tienes instalado y te indicamos los productos de cuidado XPEL correctos.",
    sections=[
      ("Cuidado del día a día", [
        "<strong>XPEL Detail Spray.</strong> Es nuestro producto de cabecera para el toque final. Limpia polvo ligero, huellas y manchas sin necesidad de lavar el carro completo, y deja un acabado sin marcas. Está formulado para ser seguro tanto sobre la pintura como sobre el PPF, así que no tienes que preocuparte por la zona protegida. También funciona como lubricante de arcilla durante la descontaminación. Un consejo de taller: bajo sol directo, rocía el producto sobre el paño de microfibra, no directamente sobre la superficie.",
        "<strong>XPEL Ceramic Boost.</strong> Un spray con dióxido de silicio (SiO2) que repele agua, polvo y pelusa, y devuelve brillo después de cada lavado. Sirve para mantener un <a href=\"../services/ceramic-coating.html\">recubrimiento cerámico</a> FUSION PLUS ya instalado, y también funciona por sí solo como capa de protección y brillo. Es la forma fácil de recargar el efecto hidrofóbico entre mantenimientos.",
        "<strong>XPEL Wash Solution.</strong> Champú con pH balanceado para lavado a mano, seguro tanto para PPF como para recubrimientos cerámicos. Pensado para que el lavado de rutina no agreda las capas de protección."]),
      ("Limpieza profunda y manchas", [
        "<strong>XPEL PPF Cleaner.</strong> Limpiador específico para <a href=\"../services/paint-protection-film.html\">PPF</a>. Elimina depósitos del ambiente como alquitrán, aceite, manchas de agua dura y ácidos de insectos, y devuelve al film su aspecto claro y recién instalado. Mantener limpio el PPF es lo que conserva su protección y su transparencia con el tiempo.",
        "<strong>XPEL Water Spot Remover.</strong> Disuelve manchas de agua dura (las que dejan los aspersores y el agua de grifo) en segundos. Está formulado para usarse con seguridad sobre pintura, films XPEL y recubrimiento FUSION PLUS, atacando los depósitos minerales sin dañar las superficies. Modo de uso: agitar, rociar, dejar actuar 30 a 45 segundos y retirar con microfibra. No usar bajo sol directo. Para el método completo en vidrio y pintura, mira nuestra guía para <a href=\"removing-water-spots.html\">quitar manchas de agua</a>.",
        "<strong>XPEL Iron Remover (removedor de óxido de hierro).</strong> Fórmula especializada que ayuda a retirar las partículas de óxido de hierro que se incrustan en la pintura y en el PPF (vienen del polvo de frenos y del ambiente). Importante: tiene un olor fuerte, así que se usa en zona ventilada o al aire libre."]),
      ("Interior y cristales", [
        "<strong>XPEL Interior Cleaner.</strong> Limpia suciedad y manchas en distintas superficies interiores. No es para textiles, y conviene probar primero en una zona oculta. Se aplica a la microfibra, se limpia y se retira el exceso.",
        "<strong>XPEL Anti-Static Window Tint Cleaner.</strong> Limpiador para cristales y <a href=\"../services/window-tint.html\">laminado de control solar</a>, formulado para no dañar el tinte."]),
      ("¿Cuál necesitas?", [
        'Todos estos productos los tenemos en el shop, los usamos en cada Tesla que pasa por nuestras manos y los vendemos a quien quiera mantener su carro en casa. Si no sabes cuál necesitas para tu caso, pregúntanos: te decimos exactamente qué usar según lo que tengas instalado en tu Tesla. Para fichas técnicas oficiales, la fuente es <a href="https://www.xpel.com" target="_blank" rel="noopener">xpel.com</a>.']),
    ],
  ),
  "when-to-get-ppf-new-tesla": dict(
    pill="Tesla", date="Junio 2026", crumb="Cuándo poner PPF", img="tesla-model-3-ppf-doral",
    title="Cuándo ponerle PPF a un Tesla nuevo | Tesla Boutique Miami",
    desc="La respuesta corta: antes del primer viaje largo. Por qué la pintura recién salida de fábrica es el mejor momento para proteger tu Tesla.",
    h1='Acabas de comprar un Tesla: ¿cuándo ponerle el <span class="highlight">PPF</span>?',
    card_title="Acabas de comprar un Tesla: ¿cuándo ponerle el PPF?",
    blurb="La respuesta corta: antes del primer viaje largo. Aquí te explicamos por qué proteger la pintura recién salida de fábrica es lo que más importa.",
    lead="La respuesta corta: antes del primer viaje largo. Aquí te explicamos por qué proteger la pintura recién salida de fábrica es lo que más importa.",
    cta_title="¿Vas a estrenar un Tesla?",
    cta_desc="Dinos tu fecha de entrega y tendremos el PPF XPEL genuino listo el día que llegue."),
  "ultimate-plus-vs-stealth": dict(
    pill="XPEL", date="Junio 2026", crumb="Ultimate Plus vs Stealth", img="tesla-cybertruck-ppf-miami",
    title="Ultimate Plus vs Stealth: qué acabado PPF para tu Tesla",
    desc="¿Brillo o satinado? La misma protección XPEL con dos looks muy distintos. Guía rápida para elegir entre Ultimate Plus y Stealth para tu Tesla.",
    h1='Ultimate Plus vs Stealth: ¿cuál acabado de <span class="highlight">PPF</span> es para ti?',
    card_title="Ultimate Plus vs Stealth: ¿cuál acabado de PPF es para ti?",
    blurb="¿Brillo o satinado? Una guía rápida para elegir el acabado de film XPEL que le va a tu Tesla.",
    lead="¿Brillo o satinado? Una guía rápida para elegir el acabado de film XPEL que le va a tu Tesla.",
    cta_title="¿Quieres ver el satinado junto al brillo?",
    cta_desc="Tenemos ambos acabados a mano en el taller de Doral. Ven a compararlos en persona."),
  "ppf-ceramic-care-miami": dict(
    pill="Mantenimiento", date="Junio 2026", crumb="Cuidar PPF y cerámico", img="tesla-model-s-ceramic-coating",
    title="Cómo cuidar tu PPF y cerámico en Miami | Tesla Boutique",
    desc="Hábitos simples de lavado para que tu film XPEL y tu cerámico Fusion Plus rindan por años bajo el calor de la Florida, desde Doral.",
    h1='Cómo cuidar tu <span class="highlight">PPF</span> y tu recubrimiento cerámico en Miami',
    card_title="Cómo cuidar tu PPF y tu recubrimiento cerámico en Miami",
    blurb="Hábitos simples de lavado para que tu film XPEL y tu cerámico Fusion Plus rindan por años bajo el calor de la Florida.",
    lead="Hábitos simples de lavado para que tu film XPEL y tu cerámico Fusion Plus rindan por años bajo el calor de la Florida.",
    cta_title="¿No sabes cómo cuidar tu Tesla?",
    cta_desc="Llámanos y dinos qué lleva puesto. Te decimos exactamente cómo cuidarlo."),
  "removing-water-spots": dict(
    pill="Mantenimiento", date="Junio 2026", crumb="Quitar manchas de agua", img="tesla-model-y-window-tinting",
    title="Cómo quitar manchas de agua de un Tesla (vidrio y pintura) | Tesla Boutique Miami",
    desc="Qué causa las manchas de agua dura en un Tesla en el sur de Florida, cómo quitarlas con seguridad del vidrio y la pintura, y cómo evitar que vuelvan. Desde un taller solo Tesla en Doral.",
    h1='Quitar <span class="highlight">manchas de agua</span> de tu Tesla, vidrio y pintura',
    card_title="Quitar manchas de agua del vidrio y la pintura de tu Tesla",
    blurb="Qué causa las manchas de agua dura en el sur de Florida y cómo quitarlas con seguridad del vidrio y la pintura sin dañar tu acabado.",
    lead="Qué causa las manchas de agua dura en el sur de Florida y cómo quitarlas con seguridad del vidrio y la pintura sin dañar tu acabado.",
    cta_title="¿Manchas de agua rebeldes en tu Tesla?",
    cta_desc="Tráelo a nuestro taller de Doral y las quitamos con seguridad, y te ayudamos a que no vuelvan."),
}

def build_post_es(slug, d):
    path = "news/%s.html" % slug; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Updates", esp+"news/index.html"), (d["crumb"], "")])
    hero = S.page_hero(rootp, d["img"], d["h1"], d["lead"], "", crumbs)
    inner = '<span class="post-date">Publicado &middot; %s</span>' % d["date"]
    if d.get("sections"):
        for h2, paras in d["sections"]:
            bi = "".join(p if p.lstrip().startswith("<ul") else "<p>%s</p>" % p for p in paras)
            inner += "<h2>%s</h2>%s" % (h2, bi)
    else:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts", "%s.es.html" % slug), encoding="utf-8") as _f:
            inner += _f.read()
    prose = '<section class="section"><div class="container"><div class="prose">%s</div></div></section>' % inner
    cta = cta_es(d["cta_title"], d["cta_desc"])
    body = hero + prose + cta
    post_ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": d["card_title"],
        "description": d["desc"], "datePublished": "2026-06-03", "dateModified": "2026-06-03", "inLanguage": "es",
        "author": {"@type": "Organization", "name": "Tesla Boutique Miami"},
        "publisher": {"@type": "Organization", "name": "Tesla Boutique Miami", "url": DOMAIN+"/"},
        "image": "%s/assets/img/%s.webp" % (DOMAIN, d["img"]),
        "mainEntityOfPage": {"@type": "WebPage", "@id": "%s/es/news/%s.html" % (DOMAIN, slug)}}, ensure_ascii=False)
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Updates", DOMAIN+"/es/news/index.html"), (d["crumb"], "%s/es/news/%s.html" % (DOMAIN, slug))]), post_ld]
    return doc_es(path, d["title"], d["desc"], body, active="news", preload=d["img"], extra_ld=ld)

def build_news_es():
    path = "news/index.html"; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Updates", "")])
    hero = S.page_hero(rootp, "tesla-model-s-ceramic-coating", 'Tesla Boutique <span class="highlight">Updates</span>',
        "Noticias y recursos de Tesla Boutique Miami: proyectos nuevos, novedades de productos XPEL y consejos prácticos para cuidar el film, el recubrimiento y el polarizado de tu Tesla. Actualizado seguido.", "", crumbs)
    posts = []
    cards = ""
    for slug, d in POSTS_ES.items():
        cards += ('<div class="project-tile reveal"><div class="project-tile-body"><div class="tag-row"><span class="pill">%s</span></div>'
                  '<span class="post-date">Publicado &middot; %s</span><h3>%s</h3><p>%s</p>'
                  '<a class="card-link" href="%s.html">Leer artículo &rarr;</a></div></div>') % (d["pill"], d["date"], d["card_title"], d["blurb"], slug)
    for pill, h3, p in posts:
        cards += ('<div class="project-tile reveal"><div class="project-tile-body"><div class="tag-row"><span class="pill">%s</span></div>'
                  '<h3>%s</h3><p>%s</p><span class="card-link">Próximamente</span></div></div>') % (pill, h3, p)
    grid = ('<section class="section"><div class="container"><div class="section-header">'
            '<span class="section-tag">Tesla Boutique News</span><h2 class="section-title">Últimas novedades</h2>'
            '<p class="section-desc">Un adelanto de los temas que cubriremos. Publicamos entradas nuevas a medida que llegan proyectos y productos.</p></div>'
            '<div class="project-list-grid">%s</div></div></section>') % cards
    cta = cta_es("¿Tienes una pregunta sobre tu Tesla?", "Con gusto ayudamos, seas cliente o estés investigando.")
    body = hero + grid + cta
    ld = [json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tesla Boutique Updates",
        "url": DOMAIN+"/es/news/index.html", "description": "Noticias, novedades y recursos de cuidado Tesla de Tesla Boutique Miami."}, ensure_ascii=False)]
    return doc_es(path, "Tesla Boutique Updates, novedades y consejos de cuidado Tesla | Tesla Boutique Miami",
                  "Novedades de Tesla Boutique Miami: proyectos nuevos, noticias de productos XPEL y consejos para cuidar el PPF, el cerámico y el polarizado de tu Tesla.",
                  body, active="news", preload="tesla-model-s-ceramic-coating", extra_ld=ld)

# ---------- ES SERVICE AREA ----------
COUNTIES_ES = [
  {"slug": "miami-dade", "name": "Condado de Miami-Dade", "short": "Miami-Dade",
   "img": "cars/model-y/model-y-1", "tag": "Nuestro condado",
   "lead": "De Doral a las playas, Miami-Dade es donde Tesla Boutique Miami vive y trabaja. Es nuestro condado, y el que mejor conocemos.",
   "intro": [
     "Miami-Dade es el condado más poblado de Florida y uno de los mercados Tesla más densos del país. También es nuestra casa: nuestro taller está en Doral, en el corazón del condado, lo que significa que los propietarios de Tesla en Miami-Dade reciben el servicio más rápido y conveniente que ofrecemos. De las torres financieras de Brickell a la arena de Miami Beach y las calles arboladas de Coral Gables, el condado concentra una enorme variedad de condiciones de manejo en poco espacio.",
     "Lo que todo Tesla de Miami-Dade comparte es la exposición: la I-95, el Palmetto y el Dolphin Expressway lanzan grava y escombros de construcción sin parar, el sol es implacable todo el año, y el estacionamiento denso de valet y garajes significa golpes de puerta y espacios apretados. Ese es exactamente el entorno para el que se crearon la protección de pintura, el recubrimiento cerámico y el polarizado cerámico XPEL. Elige tu ciudad abajo para ver cómo protegemos Teslas en tu parte de Miami-Dade."],
   "cities": ["miami", "miami-beach", "doral", "coral-gables", "aventura"]},
  {"slug": "broward", "name": "Condado de Broward", "short": "Broward",
   "img": "cars/model-3/model-3-grey", "tag": "Fort Lauderdale y norte",
   "lead": "Fort Lauderdale, Hollywood y las ciudades justo al norte. Los propietarios de Tesla en Broward están a un corto trayecto por la I-95 o el Turnpike desde nuestro taller en Doral.",
   "intro": [
     "El condado de Broward se extiende de las playas del Atlántico hacia el interior hasta el borde de los Everglades, y es uno de los mercados Tesla de más rápido crecimiento del sur de Florida. Para los propietarios en Fort Lauderdale, Hollywood y los suburbios del oeste, estamos a un trayecto directo por la I-95 o el Turnpike desde nuestro taller en Doral. Broward combina la vida de playa con suburbios extensos, así que un Tesla aquí enfrenta aire salino cerca de la costa y largos kilómetros de autopista llenos de grava tierra adentro.",
     "Ya sea que cruces la 595, estaciones cerca de Las Olas o viajes desde Weston, las amenazas son las mismas: picaduras, sol implacable y sal costera. La protección de pintura, el recubrimiento cerámico y el polarizado cerámico XPEL están hechos justo para esto. Elige tu ciudad de Broward abajo para ver cómo protegemos Teslas en tu zona."],
   "cities": ["fort-lauderdale", "hollywood", "pembroke-pines", "weston", "miramar"]},
  {"slug": "palm-beach", "name": "Condado de Palm Beach", "short": "Palm Beach",
   "img": "cars/model-x/model-x-red-1", "tag": "Boca Raton y la costa",
   "lead": "Boca Raton, West Palm Beach y las comunidades acomodadas del condado de Palm Beach, donde los Teslas están por todas partes y un acabado impecable es el estándar.",
   "intro": [
     "El condado de Palm Beach es donde el sur de Florida se vuelve acomodado y tranquilo, y los Teslas están por todas partes, de las comunidades cerradas de Boca Raton a las mansiones frente al agua de la propia Palm Beach. Es el extremo norte de nuestra zona de servicio, a un trayecto fácil por la I-95 o el Turnpike desde Doral. El condado combina una vida costera impecable con largos recorridos suburbanos, así que los Teslas aquí ven tanto aire salino como kilómetros serios de autopista.",
     "Para los propietarios que esperan que su auto luzca perfecto de sala de exhibición todo el año, la protección de pintura, el recubrimiento cerámico y el polarizado cerámico XPEL son el estándar. Elige tu ciudad de Palm Beach abajo para ver cómo protegemos Teslas ahí."],
   "cities": ["boca-raton", "west-palm-beach", "delray-beach", "wellington", "jupiter"]},
  {"slug": "monroe", "name": "Condado de Monroe", "short": "Monroe (Los Cayos)",
   "img": "cars/cybertruck/cybertruck-3-white", "tag": "Los Cayos de Florida",
   "lead": "Key West, Key Largo y la cadena de islas. El aire salino y el sol hacen de los Cayos uno de los lugares más duros de Florida para la pintura y el vidrio de un Tesla.",
   "intro": [
     "El condado de Monroe son los Cayos de Florida, una cadena de islas de 160 km donde la Overseas Highway es la única vía de entrada y salida. Es el entorno más exigente de nuestra zona de servicio para un vehículo: aire salino constante, sol cegador y una sola autopista larga que concentra cada kilómetro de manejo. Un Tesla en los Cayos es precioso y está muy expuesto.",
     "Ahí es exactamente donde la protección XPEL rinde: film contra el sol implacable y los escombros de la US-1, recubrimiento cerámico que hace que la sal se enjuague, y polarizado cerámico para cortar el calor del cielo abierto. Atendemos a propietarios de Tesla en los Cayos con cita, así que contáctanos y coordinamos los tiempos para el viaje hasta Doral. Elige tu comunidad isleña abajo."],
   "cities": ["key-west", "key-largo", "islamorada", "marathon", "tavernier"]},
]
COUNTY_BY_SLUG_ES = {c["slug"]: c for c in COUNTIES_ES}

CITIES_ES = {
  "miami": {"name": "Miami", "county": "miami-dade", "img": "cars/model-3/model-3-grey-2",
    "lead": "De los rascacielos de Brickell a Wynwood y Coconut Grove, Miami es dura con un Tesla: garajes de valet apretados, picaduras de la I-95 y sol implacable. Así protegemos los Teslas de los propietarios de Miami.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium creados exclusivamente para propietarios de Tesla en Miami, FL. Ya sea que estaciones en una torre de Brickell, manejes al centro o pases el fin de semana en Coconut Grove, tu Model 3, Y, S, X o Cybertruck enfrenta las mismas amenazas diarias: grava y escombros de construcción en la I-95 y el Dolphin Expressway, golpes de puerta en garajes de valet llenos, y el tipo de sol y calor que decolora interiores y castiga la blanda pintura Tesla.",
      "Nuestra respuesta es específica para Tesla. Instalamos protección de pintura XPEL original en los paneles que reciben más impactos, polarizado cerámico XPEL Prime XR Plus para cortar el calor que se acumula bajo el sol de Miami, y recubrimiento cerámico XPEL Fusion Plus para brillo y lavado fácil. Cada instalación usa patrones cortados para tu Tesla exacto y queda registrada a tu VIN. Nuestro taller está cerca, en Doral, atendiendo a propietarios de Miami con cita."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Ofrecen PPF y polarizado para Tesla en Miami?",
       "Sí. Protegemos Teslas de propietarios en todo Miami, de Brickell y el centro a Wynwood y Coconut Grove. Nuestro taller está en la cercana Doral, a un trayecto fácil desde cualquier punto de la ciudad. Llama al (786) 505-6162 para reservar."),
      ("¿Qué tan lejos está su taller de Brickell o el centro de Miami?",
       "Nuestro taller en Doral, en 1835 NW 79th Ave, está a unos 15 a 20 minutos de Brickell y el centro por el Dolphin Expressway o la NW 12th Street. La mayoría deja el auto y coordinamos los tiempos según su día."),
      ("¿Por qué mi Tesla necesita PPF en Miami?",
       "Autopistas como la I-95 y el Palmetto lanzan grava y escombros de construcción sin parar, y la capa transparente de fábrica del Tesla es blanda y se pica fácil. El PPF frontal protege capó, guardabarros, espejos y parachoques, que reciben más impactos.")]},
  "miami-beach": {"name": "Miami Beach", "county": "miami-dade", "img": "cars/model-y/model-y-white-3",
    "lead": "Aire salino, arena de playa y sol todo el día. Miami Beach es uno de los entornos más duros de Florida para la pintura y el vidrio de un Tesla, y justo donde la protección rinde.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo Miami Beach, de South Beach a Mid-Beach y North Beach. La vida en la isla es bella y brutal con un auto: el aire cargado de sal del océano, la arena que vuela, el UV intenso y el estacionamiento en la calle dejan tu Model 3, Y, S, X o Cybertruck constantemente expuesto.",
      "Protegemos los Teslas de Miami Beach con film XPEL original que recibe la arena y la grava en lugar de tu pintura, recubrimiento cerámico que bloquea la sal y hace fácil enjuagar los residuos de playa, y polarizado cerámico XPEL que bloquea el calor y el UV que entran por el vidrio. Los patrones se cortan específicamente para tu Tesla y se registran a tu VIN. Tenemos base en Doral, a un trayecto directo por las causeways, y atendemos a propietarios de Miami Beach con cita."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Vale la pena el recubrimiento cerámico para un Tesla en Miami Beach?",
       "Muchísimo. El aire salino y los residuos de playa son implacables en la isla. Un recubrimiento cerámico Fusion Plus hace que la sal y la arena se enjuaguen mucho más fácil y añade resistencia a UV y químicos, protegiendo tu Tesla entre lavados."),
      ("¿Van a Miami Beach o llevo el auto a ustedes?",
       "Las instalaciones se hacen en nuestro taller controlado de Doral para un resultado impecable y sin polvo. Miami Beach está a un trayecto corto por la MacArthur o la Julia Tuttle Causeway. Llama al (786) 505-6162 y coordinamos los tiempos."),
      ("¿El polarizado ayuda con el sol y el calor de Miami Beach?",
       "Sí. El polarizado cerámico XPEL Prime XR Plus rechaza hasta el 98% del calor infrarrojo y el 99% del UV, una gran mejora de confort para un Tesla estacionado bajo el sol de la isla, y protege el interior de la decoloración.")]},
  "doral": {"name": "Doral", "county": "miami-dade", "img": "cars/model-s/model-s-blue-1",
    "lead": "Doral es casa. Nuestro taller está aquí, a minutos de CityPlace y del concesionario Tesla, lo que lo hace el lugar más fácil del sur de Florida para proteger tu Tesla.",
    "intro": [
      "Tesla Boutique Miami tiene su base aquí mismo en Doral, FL, y los propietarios de Tesla en Doral son nuestros vecinos. Desde nuestro taller en 1835 NW 79th Ave ofrecemos protección de pintura, recubrimiento cerámico, polarizado y servicios de wrap personalizado para cada Tesla, a minutos de CityPlace Doral, Downtown Doral y el concesionario Tesla en la NW 12th Street.",
      "Como somos locales, proteger un Tesla de Doral es facilísimo: deja el auto antes del trabajo y recógelo listo. Instalamos PPF XPEL original donde la grava del Palmetto Expressway hace daño, polarizado cerámico XPEL Prime XR Plus para el calor de Doral, y recubrimiento XPEL Fusion Plus para un brillo profundo y fácil de lavar. Muchos de nuestros clientes compran nuevo en la tienda Tesla de Doral y traen el auto directo a nosotros para que la pintura quede protegida antes de su primer kilómetro de autopista. Cada instalación usa patrones por modelo y queda registrada a tu VIN."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Dónde está su taller Tesla en Doral?",
       "Estamos en 1835 NW 79th Ave, Doral, FL 33126, cerca del Palmetto Expressway y a minutos de CityPlace Doral y el concesionario Tesla. Llama al (786) 505-6162 para reservar tu instalación."),
      ("Acabo de comprar un Tesla en el concesionario de Doral. ¿Pueden protegerlo antes de manejarlo?",
       "Por supuesto, y es el momento ideal. Tráelo directo del concesionario e instalamos PPF y polarizado antes de que la pintura vea kilómetros de autopista, para que el acabado debajo quede perfecto de fábrica."),
      ("¿Ofrecen conveniencia local para los residentes de Doral?",
       "Sí. Ser locales significa entrega y recogida fáciles, cotizaciones rápidas en persona y sin trayectos largos. Doral es nuestra base y la zona que atendemos más rápido.")]},
  "coral-gables": {"name": "Coral Gables", "county": "miami-dade", "img": "cars/model-s/model-s-red",
    "lead": "Arbolada, exclusiva y obsesionada con el detalle. Los propietarios de Tesla en Coral Gables esperan un acabado impecable, y eso es exactamente lo que entregamos.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios exigentes en todo Coral Gables, FL. The Gables es conocida por su belleza, sus calles bordeadas de banianos y sus estándares, y la misma fronda que hace hermosas la Miracle Mile y Old Cutler Road también deja savia, polen y escombros sobre tu Model 3, Y, S, X o Cybertruck.",
      "Protegemos los Teslas de Coral Gables con protección de pintura XPEL original contra picaduras y escombros de árboles, recubrimiento cerámico Fusion Plus para que la savia y el polen se enjuaguen en lugar de grabar la pintura, y polarizado cerámico XPEL para confort y protección UV sin alterar el aspecto elegante del auto. Cada instalación es meticulosa, con bordes envueltos y registrada a tu VIN, el nivel de acabado que los propietarios de the Gables esperan. Nuestro taller está a un corto trayecto en Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿La savia y el polen realmente dañan la pintura Tesla en Coral Gables?",
       "Con el tiempo, sí. La savia y el polen pueden grabar una capa transparente blanda, sobre todo con el calor. Un recubrimiento cerámico los hace mucho más fáciles de quitar y añade una barrera protectora, mientras el PPF protege contra escombros que caen y picaduras."),
      ("¿Se puede polarizar sin cambiar el aspecto de mi Tesla en the Gables?",
       "Sí. El polarizado cerámico XPEL viene en tonos que mantienen una apariencia limpia y de fábrica mientras cortan el calor y el UV, así tu Tesla se ve refinado y permanece cómodo."),
      ("¿Atienden Coral Gables?",
       "Sí, protegemos Teslas en todo Coral Gables, de Miracle Mile a Cocoplum y Gables Estates. Nuestro taller en Doral está a un corto trayecto. Llama al (786) 505-6162 para agendar.")]},
  "aventura": {"name": "Aventura", "county": "miami-dade", "img": "cars/model-x/model-x-red-3",
    "lead": "Entre el océano, los rascacielos y el tráfico del Aventura Mall, un Tesla de Aventura se gana su protección. Así lo mantenemos impecable.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium creados exclusivamente para propietarios de Tesla en Aventura, FL y la zona cercana de Sunny Isles. Vivir cerca del agua significa aire salino y sol intenso, mientras que la realidad diaria de los garajes del Aventura Mall, Biscayne Boulevard y el valet de los rascacielos significa golpes de puerta, estacionamiento apretado y exposición constante para tu Model 3, Y, S, X o Cybertruck.",
      "Protegemos los Teslas de Aventura con protección de pintura XPEL original en los paneles de alto impacto, recubrimiento cerámico XPEL Fusion Plus que aguanta el aire salino y facilita el lavado, y polarizado cerámico XPEL Prime XR Plus que rechaza el calor y el UV que vienen del agua y el cielo abierto. Los patrones son por modelo y cada instalación queda registrada a tu VIN. Nuestro taller está en Doral, a un trayecto fácil por la US-1 o el Turnpike."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Protegen Teslas en Aventura y Sunny Isles?",
       "Sí. Atendemos a propietarios de Tesla en Aventura, Sunny Isles Beach y Williams Island. Las instalaciones se hacen en nuestro taller de Doral, a un trayecto fácil por la US-1 o el Turnpike. Llama al (786) 505-6162."),
      ("¿El aire salino del océano es malo para mi Tesla cerca de Aventura?",
       "El aire salino acelera la corrosión y deja residuos que se adhieren a pintura y vidrio. Un recubrimiento cerámico más PPF da una barrera protectora y fácil de limpiar que resiste el entorno costero mucho mejor que la pintura desnuda."),
      ("¿Cuánto cuesta proteger un Tesla en Aventura?",
       "Depende de la cobertura; el PPF frontal o de cuerpo completo, el polarizado y el cerámico son servicios separados que puedes combinar. Llama al (786) 505-6162 para una cotización a la medida de tu Tesla y de cómo manejas.")]},
  # ----- Broward -----
  "fort-lauderdale": {"name": "Fort Lauderdale", "county": "broward", "img": "cars/model-s/model-s-blue-2",
    "lead": "Yates, Las Olas y la playa. Los Teslas de Fort Lauderdale viven entre el aire salino y el tráfico de ciudad, y eso es justo para lo que se creó la protección XPEL.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo Fort Lauderdale, FL. De Las Olas Boulevard a la playa y los rascacielos del centro, un Tesla de Fort Lauderdale enfrenta aire salino costero, sol intenso y el pare y siga de una ciudad ajetreada, todo lo cual desgasta la pintura de fábrica y calienta la cabina.",
      "Protegemos los Teslas de Fort Lauderdale con film XPEL original en los paneles de alto impacto, recubrimiento cerámico Fusion Plus que hace fácil enjuagar la sal y la mugre, y polarizado cerámico XPEL Prime XR Plus para cortar el calor cerca del agua. Los patrones son por modelo y quedan registrados a tu VIN. Nuestro taller está a un trayecto rápido al sur por la I-95 desde Fort Lauderdale."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Fort Lauderdale?",
       "Sí. Protegemos Teslas en todo Fort Lauderdale, de Las Olas y Victoria Park a la playa. Las instalaciones se hacen en nuestro taller de Doral, a un trayecto rápido al sur por la I-95. Llama al (786) 505-6162 para reservar."),
      ("¿El aire salino cerca de la playa es malo para mi Tesla?",
       "Sí. El aire salino costero deja residuos que se adhieren a pintura y vidrio. Un recubrimiento cerámico más PPF hace mucho más fácil enjuagarlos y protege el acabado de los efectos corrosivos de vivir cerca del agua."),
      ("¿Dónde instalan y qué tan lejos está de Fort Lauderdale?",
       "Todo el trabajo se hace en nuestro taller controlado de Doral para un resultado impecable. Está a unos 30 a 40 minutos al sur por la I-95 o el Turnpike. La mayoría deja el auto y coordinamos según su agenda.")]},
  "hollywood": {"name": "Hollywood", "county": "broward", "img": "cars/model-y/model-y-2",
    "lead": "Entre el Broadwalk y el Turnpike, un Tesla de Hollywood ve sal de playa y grava de autopista el mismo día. Así lo mantenemos impecable.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium creados exclusivamente para propietarios de Tesla en Hollywood, FL. Del Hollywood Beach Broadwalk a Young Circle y los barrios a lo largo del Turnpike, un Tesla de Hollywood vive entre el aire salino del Atlántico y autopistas de viaje al trabajo llenas de grava, con el sol pegando todo el año.",
      "Protegemos los Teslas de Hollywood con film de protección de pintura XPEL original donde ocurren las picaduras, recubrimiento cerámico Fusion Plus para quitarse de encima los residuos de playa y facilitar el lavado, y polarizado cerámico XPEL Prime XR Plus para mantener la cabina fresca. Cada instalación usa patrones por modelo registrados a tu VIN. Nuestro taller de Doral está a un corto trayecto al sur."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Protegen Teslas en Hollywood, FL?",
       "Sí, atendemos a propietarios de Tesla en todo Hollywood, de la playa y el Broadwalk a Young Circle y West Hollywood. Las instalaciones se hacen en nuestro cercano taller de Doral. Llama al (786) 505-6162."),
      ("Mi Tesla se estaciona cerca de Hollywood Beach. ¿Qué recomiendan?",
       "Cerca de la playa, el aire salino es el principal enemigo. Recomendamos un recubrimiento cerámico para que la sal se enjuague fácil, más PPF en el frente para detener picaduras. El polarizado cerámico mantiene la cabina fresca."),
      ("¿Cuánto cuesta el PPF Tesla para un propietario de Hollywood?",
       "Depende de la cobertura; el PPF frontal o de cuerpo completo, el polarizado y el cerámico son servicios separados que puedes combinar. Llama al (786) 505-6162 para una cotización a la medida de tu Tesla.")]},
  "pembroke-pines": {"name": "Pembroke Pines", "county": "broward", "img": "cars/model-3/model-3-grey-3",
    "lead": "El Tesla de quien viaja al trabajo en Pembroke Pines acumula kilómetros de autopista en la I-75 y Pines Boulevard. Ahí es justo donde la protección de pintura rinde.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo Pembroke Pines, FL. Como uno de los mayores suburbios familiares de Broward, Pembroke Pines significa kilometraje diario real, en la I-75, Pines Boulevard y el Turnpike, donde la grava y los escombros de construcción pican una capa transparente de fábrica blanda, además de largas horas estacionado bajo el sol de Florida.",
      "Protegemos los Teslas de Pembroke Pines con film XPEL original en el capó, los guardabarros y el parachoques que reciben más impactos, polarizado cerámico XPEL Prime XR Plus para combatir el calor en entradas y estacionamientos, y recubrimiento cerámico Fusion Plus para brillo y lavado fácil. Patrones por modelo, registrados a tu VIN. Nuestro taller de Doral está a un salto corto por la I-75 o el Turnpike."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Atienden Pembroke Pines?",
       "Sí, protegemos Teslas en todo Pembroke Pines. Las instalaciones se hacen en nuestro taller de Doral, a un trayecto fácil por la I-75 o el Turnpike. Llama al (786) 505-6162 para agendar."),
      ("Viajo mucho por la I-75. ¿Vale la pena el PPF?",
       "Sin duda. El alto kilometraje de autopista es justo cuando se acumulan las picaduras. El PPF frontal protege los paneles que reciben más impactos y conserva la pintura de tu Tesla, y su valor de reventa."),
      ("¿El polarizado cerámico ayuda en una entrada calurosa de Pembroke Pines?",
       "Sí. El XPEL Prime XR Plus rechaza hasta el 98% del calor infrarrojo, así que un Tesla estacionado en una entrada o lote abierto se mantiene mucho más fresco y el interior queda protegido de la decoloración por UV.")]},
  "weston": {"name": "Weston", "county": "broward", "img": "cars/model-x/model-x-red-2",
    "lead": "Cuidada, cerrada y con ojo para el detalle. Los propietarios de Tesla en Weston quieren sus autos tan impecables como sus vecindarios, y eso entregamos.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado, exclusivamente para Tesla, a propietarios en todo Weston, FL. Conocida por sus comunidades planificadas y cuidadas en el borde oeste de Broward, cerca de la I-75 y los Everglades, Weston es hogar de propietarios exigentes que esperan un acabado impecable, y de largos viajes al trabajo que exponen un Tesla a escombros de autopista y sol intenso.",
      "Protegemos los Teslas de Weston con film XPEL meticuloso y con bordes envueltos, recubrimiento cerámico Fusion Plus para un brillo profundo y fácil de lavar, y polarizado cerámico XPEL Prime XR Plus para confort y protección UV. Cada instalación usa patrones por modelo y queda registrada a tu VIN. Nuestro taller de Doral está a un trayecto directo al sur por la I-75."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Weston?",
       "Sí, protegemos Teslas en todo Weston. Las instalaciones se hacen en nuestro taller de Doral, a un trayecto directo al sur por la I-75. Llama al (786) 505-6162 para reservar."),
      ("Quiero un acabado de sala de exhibición. ¿Qué da el mejor brillo?",
       "La corrección de pintura seguida de un recubrimiento cerámico Fusion Plus entrega el acabado más profundo y cristalino, y el recubrimiento hace el auto mucho más fácil de mantener limpio. Suma PPF al frente para detener picaduras."),
      ("¿Es popular el PPF de cuerpo completo en Weston?",
       "Sí. Para quienes mantienen su Tesla impecable y protegen la reventa, el film de cuerpo completo cubre cada panel pintado. Lo cortamos con precisión y bordes envueltos.")]},
  "miramar": {"name": "Miramar", "county": "broward", "img": "cars/model-y/model-y-white-1",
    "lead": "Un Tesla en crecimiento de Miramar pasa su vida en el Turnpike y la I-75. Protege la pintura antes de que los kilómetros de autopista se acumulen.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo Miramar, FL. Como uno de los suburbios de más rápido crecimiento del sur de Florida, Miramar significa viajar al trabajo, en el Turnpike, la I-75 y Miramar Parkway, donde la grava y los escombros pican la pintura de fábrica, además del sol todo el año sobre autos estacionados al aire libre.",
      "Protegemos los Teslas de Miramar con film XPEL original en el frente de alto impacto, polarizado cerámico XPEL Prime XR Plus para cortar el calor y el UV, y recubrimiento cerámico Fusion Plus para brillo y limpieza fácil. Los patrones son por modelo y quedan registrados a tu VIN. Nuestro taller de Doral está a solo minutos al sur."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Atienden Miramar?",
       "Sí, protegemos Teslas en todo Miramar, y nuestro taller de Doral está a solo minutos al sur. Llama al (786) 505-6162 para agendar tu instalación."),
      ("Acabo de comprar un Tesla nuevo en Miramar. ¿Cuándo debo poner PPF?",
       "Antes del primer viaje largo por autopista. Proteger la pintura recién salida de fábrica significa que el acabado bajo el film queda perfecto. Tráelo temprano y tendremos XPEL original listo."),
      ("¿Cuál es el taller de protección Tesla más cercano a Miramar?",
       "Nuestro taller de Doral es uno de los estudios de protección Tesla dedicados más cercanos, a un corto trayecto al sur. Somos solo Tesla y distribuidor exclusivo XPEL.")]},
  # ----- Palm Beach -----
  "boca-raton": {"name": "Boca Raton", "county": "palm-beach", "img": "cars/model-s/model-s-blue-3",
    "lead": "Golf, comunidades cerradas y ojo para el detalle. Los propietarios de Tesla en Boca Raton esperan perfección, y la protección XPEL la entrega.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado, creados exclusivamente para Tesla, a propietarios en todo Boca Raton, FL. De Mizner Park a las comunidades de golf cerradas y la costa de la A1A, Boca es sinónimo de altos estándares, y su mezcla de aire salino costero y estacionamiento bajo el sol es dura con un Tesla sin protección.",
      "Protegemos los Teslas de Boca Raton con film de protección de pintura XPEL meticuloso, recubrimiento cerámico Fusion Plus que evita que la sal y la mugre se adhieran, y polarizado cerámico XPEL Prime XR Plus para confort y defensa contra UV. Cada instalación usa patrones por modelo y queda registrada a tu VIN. Estamos a un trayecto fácil bajando por la I-95 desde Boca."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Boca Raton?",
       "Sí. Protegemos Teslas en todo Boca Raton, de Mizner Park a las comunidades costeras. Las instalaciones se hacen en nuestro taller de Doral, a un trayecto directo al sur por la I-95. Llama al (786) 505-6162."),
      ("¿Qué protección mantiene un Tesla perfecto de sala de exhibición en Boca?",
       "Una combinación: PPF para detener picaduras, un recubrimiento cerámico Fusion Plus para brillo profundo y limpieza fácil, y polarizado cerámico para el sol. Juntos mantienen el auto impecable todo el año."),
      ("¿Vale la pena el trayecto de Boca a su taller?",
       "Nuestros clientes creen que sí. Somos solo Tesla, distribuidor exclusivo XPEL, y documentamos cada instalación. La mayoría deja el auto y coordinamos los tiempos para el viaje.")]},
  "west-palm-beach": {"name": "West Palm Beach", "county": "palm-beach", "img": "cars/model-3/model-3-grey-4",
    "lead": "Energía del centro y vistas al agua. Un Tesla de West Palm Beach enfrenta kilómetros de ciudad y sol costero por igual.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo West Palm Beach, FL. De Clematis Street y el centro al frente de agua del Intracoastal, un Tesla de West Palm ve manejo de ciudad ajetreado, aire salino costero y sol fuerte todo el año, una combinación que pica la pintura y calienta las cabinas.",
      "Protegemos los Teslas de West Palm Beach con film XPEL original en las zonas de impacto del frente, recubrimiento cerámico Fusion Plus para limpieza fácil y brillo, y polarizado cerámico XPEL Prime XR Plus para cortar el calor. Patrones por modelo, registrados a tu VIN. Nuestro taller de Doral está a un trayecto claro al sur por la I-95 o el Turnpike."],
    "services": ["paint-protection-film", "window-tint", "ceramic-coating"],
    "faqs": [
      ("¿Protegen Teslas en West Palm Beach?",
       "Sí, atendemos a propietarios de Tesla en todo West Palm Beach. Las instalaciones se hacen en nuestro taller de Doral por la I-95 o el Turnpike. Llama al (786) 505-6162 para reservar."),
      ("¿El aire salino del frente de agua afecta mi Tesla?",
       "Sí. El residuo de sal del Intracoastal y el océano se adhiere a pintura y vidrio. Un recubrimiento cerámico hace mucho más fácil enjuagarlo y protege el acabado; el PPF protege contra picaduras."),
      ("¿Cuánto cuesta proteger un Tesla desde West Palm Beach?",
       "El precio depende de la cobertura que elijas. Llama al (786) 505-6162 y armamos un paquete de PPF, polarizado y cerámico según cómo usas el auto.")]},
  "delray-beach": {"name": "Delray Beach", "county": "palm-beach", "img": "cars/model-y/model-y-3",
    "lead": "Atlantic Avenue, la playa y el sol. Un Tesla de Delray Beach es un auto de pueblo de playa, y esos autos necesitan protección real.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado, exclusivamente para Tesla, a propietarios en todo Delray Beach, FL. Entre Atlantic Avenue, la playa y los barrios costeros, un Tesla de Delray vive en aire salino y sol, las dos cosas más duras para la pintura y los interiores de un auto.",
      "Protegemos los Teslas de Delray Beach con film XPEL original contra picaduras, recubrimiento cerámico Fusion Plus para que la sal y la arena se enjuaguen en lugar de grabar el acabado, y polarizado cerámico XPEL Prime XR Plus para bloquear el calor y el UV. Los patrones son por modelo y quedan registrados a tu VIN. Nuestro taller está a un trayecto directo al sur en Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden Delray Beach?",
       "Sí, protegemos Teslas en todo Delray Beach, de Atlantic Avenue a los barrios costeros. Las instalaciones se hacen en nuestro taller de Doral. Llama al (786) 505-6162."),
      ("¿Es buena idea el recubrimiento cerámico para un Tesla de pueblo de playa?",
       "Por supuesto. En un entorno de sal y arena como Delray, un recubrimiento cerámico hace que el residuo se enjuague fácil, añade resistencia UV y mantiene el brillo fresco entre lavados."),
      ("¿Usan XPEL original en los Teslas de Delray?",
       "Siempre. Como distribuidor exclusivo XPEL instalamos solo film y recubrimientos XPEL originales, registrados al VIN de tu Tesla con la garantía de fábrica completa.")]},
  "wellington": {"name": "Wellington", "county": "palm-beach", "img": "cars/model-x/model-x-red-4",
    "lead": "Tierra ecuestre, cuidada y refinada. Los propietarios de Tesla en Wellington exigen mucho de sus autos, y nosotros también.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en todo Wellington, FL. Conocida por sus fincas ecuestres y comunidades cuidadas, Wellington combina gustos refinados con manejo real, caminos largos, sol abierto y el polvo y los escombros de un entorno semirrural en el borde del condado de Palm Beach.",
      "Protegemos los Teslas de Wellington con film de protección de pintura XPEL meticuloso, recubrimiento cerámico Fusion Plus para un acabado de alto brillo y fácil de limpiar, y polarizado cerámico XPEL Prime XR Plus para confort bajo el cielo abierto. Cada instalación usa patrones por modelo y queda registrada a tu VIN. Estamos a un trayecto claro al sur desde Wellington."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Wellington?",
       "Sí, protegemos Teslas en todo Wellington. Las instalaciones se hacen en nuestro taller de Doral. Llama al (786) 505-6162 y coordinamos los tiempos para el viaje."),
      ("¿Importan el polvo y los escombros de camino abierto para mi Tesla?",
       "Sí. Los caminos abiertos y un entorno semirrural significan más grava en el aire y picaduras. El PPF protege las zonas de impacto del frente y un recubrimiento cerámico evita que el polvo se adhiera a la pintura."),
      ("¿Cuál es la mejor protección para un acabado brillante y de bajo mantenimiento?",
       "Un recubrimiento cerámico sobre pintura corregida da el brillo más profundo y el mantenimiento más fácil. Suma PPF al frente para detener picaduras y tu Tesla se mantiene fresco de sala de exhibición con mínimo esfuerzo.")]},
  "jupiter": {"name": "Jupiter", "county": "palm-beach", "img": "cars/cybertruck/cybertruck-4-white",
    "lead": "Faro, playas y náutica. En el extremo norte de nuestra zona de servicio, un Tesla de Jupiter vive en aire salino y sol.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado, creados exclusivamente para Tesla, a propietarios en Jupiter, FL. Del faro de Jupiter Inlet a las playas y las comunidades náuticas a lo largo del Loxahatchee, un Tesla de Jupiter está constantemente expuesto al aire salino costero y al sol fuerte en el extremo norte del condado de Palm Beach.",
      "Protegemos los Teslas de Jupiter con film XPEL original contra picaduras y escombros, recubrimiento cerámico Fusion Plus que hace fácil enjuagar el residuo de sal, y polarizado cerámico XPEL Prime XR Plus para cortar el calor y el UV. Los patrones son por modelo y quedan registrados a tu VIN. Atendemos a propietarios de Jupiter con cita en nuestro taller de Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Jupiter, FL?",
       "Sí. Jupiter está en el extremo norte de nuestra zona de servicio; protegemos Teslas ahí con cita en nuestro taller de Doral. Llama al (786) 505-6162 y coordinamos los tiempos."),
      ("¿El aire salino del inlet y el océano es duro con un Tesla?",
       "Sí. La sal costera se adhiere a pintura y vidrio y acelera el desgaste. Un recubrimiento cerámico más PPF da una barrera protectora y fácil de limpiar que maneja el entorno costero mucho mejor que la pintura desnuda."),
      ("¿Vale la pena el trayecto desde Jupiter?",
       "Para quienes quieren un especialista solo Tesla y distribuidor exclusivo XPEL, sí. La mayoría deja el auto y coordinamos la visita. Documentamos cada instalación para que veas exactamente el acabado.")]},
  # ----- Monroe (Los Cayos) -----
  "key-west": {"name": "Key West", "county": "monroe", "img": "cars/cybertruck/cybertruck-5-white",
    "lead": "La ciudad más al sur de EE. UU., pura sal y sol. Un Tesla de Key West es precioso y está muy expuesto.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en Key West, FL. Al final mismo de la Overseas Highway, Key West está rodeada de océano por todos lados, lo que significa aire salino implacable, sol cegador y humedad, casi el entorno más duro en el que puede vivir un vehículo.",
      "Protegemos los Teslas de Key West con film XPEL original contra el sol y los escombros del camino, recubrimiento cerámico Fusion Plus que hace que el residuo de sal se enjuague y añade resistencia a UV y químicos, y polarizado cerámico XPEL Prime XR Plus para cortar el calor del cielo abierto. Los patrones son por modelo y quedan registrados a tu VIN. Atendemos a propietarios de los Cayos con cita; contáctanos y coordinamos el viaje hasta Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Key West?",
       "Sí, protegemos Teslas de propietarios de Key West con cita. Como las instalaciones se hacen en nuestro taller de Doral, coordinamos los tiempos para el viaje por la US-1. Llama al (786) 505-6162."),
      ("¿El entorno de Key West es realmente tan duro con un Tesla?",
       "Sí. Rodeada de océano, Key West somete a un auto a aire salino constante, UV intenso y humedad. El recubrimiento cerámico más PPF es la defensa más eficaz, y el polarizado cerámico protege el interior."),
      ("¿Cómo funciona el servicio si estoy en los Cayos?",
       "Coordinamos una ventana de entrega conveniente en nuestro taller de Doral y planificamos el trabajo en torno a tu viaje por la Overseas Highway, así el trayecto se hace una vez y tu Tesla vuelve totalmente protegido.")]},
  "key-largo": {"name": "Key Largo", "county": "monroe", "img": "cars/model-y/model-y-white-2",
    "lead": "La capital del buceo y la puerta de entrada a los Cayos. Un Tesla de Key Largo empieza cada viaje en la US-1, a pleno sol y aire salino.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado, exclusivamente para Tesla, a propietarios en Key Largo, FL. Como la primera isla de la cadena y la puerta de entrada a los Cayos, Key Largo significa vida en la US-1, rodeada de agua, sol y sal que trabajan sin descanso sobre la pintura, el vidrio y los interiores de un auto.",
      "Protegemos los Teslas de Key Largo con film XPEL original contra el sol y los escombros de la Overseas Highway, recubrimiento cerámico Fusion Plus para que la sal se enjuague fácil, y polarizado cerámico XPEL Prime XR Plus para bloquear el calor y el UV. Los patrones son por modelo y quedan registrados a tu VIN. Somos la comunidad de los Cayos más cercana a nuestro taller de Doral; contáctanos para coordinar."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden Key Largo?",
       "Sí. Key Largo es la comunidad de los Cayos más cercana a nuestro taller de Doral. Protegemos Teslas ahí con cita y coordinamos los tiempos para el viaje por la US-1. Llama al (786) 505-6162."),
      ("¿Cuál es la mejor protección para un Tesla en los Cayos?",
       "Recubrimiento cerámico más PPF. El recubrimiento combate la sal y el UV y mantiene el auto fácil de enjuagar; el PPF detiene picaduras en los largos kilómetros de la US-1. El polarizado cerámico mantiene la cabina fresca."),
      ("¿Pueden proteger mi Tesla nuevo antes de llevarlo a los Cayos?",
       "Idealmente sí. Proteger la pintura recién salida de fábrica antes de la sal y el sol de la vida isleña mantiene el acabado debajo perfecto. Tráelo temprano y tendremos XPEL original listo.")]},
  "islamorada": {"name": "Islamorada", "county": "monroe", "img": "cars/model-s/model-s-blue-4",
    "lead": "El pueblo de pesca deportiva de las islas. Un Tesla de Islamorada es un auto costero de pies a cabeza, y necesita protección a la altura.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en Islamorada, FL. Repartida en varias islas de los Cayos Altos, Islamorada es todo frente de agua, lo que significa aire salino constante, sol fuerte y la exposición abierta de la vida a lo largo de la Overseas Highway.",
      "Protegemos los Teslas de Islamorada con film XPEL original contra escombros y UV, recubrimiento cerámico Fusion Plus que evita que la sal se adhiera al acabado, y polarizado cerámico XPEL Prime XR Plus para cortar el calor. Los patrones son por modelo y quedan registrados a tu VIN. Atendemos a propietarios de Islamorada con cita en nuestro taller de Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Islamorada?",
       "Sí, con cita. Las instalaciones se hacen en nuestro taller de Doral, así que coordinamos los tiempos para el viaje por la US-1 desde los Cayos Altos. Llama al (786) 505-6162."),
      ("¿Por qué un Tesla costero necesita recubrimiento cerámico?",
       "El aire salino y el sol son implacables en Islamorada. Un recubrimiento cerámico hace que el residuo de sal se enjuague fácil, añade resistencia a UV y químicos, y mantiene el brillo fresco mucho más que una cera."),
      ("¿Solo trabajan en Teslas?",
       "Sí. Somos un estudio solo Tesla y distribuidor exclusivo XPEL, así que cada patrón, producto y proceso está afinado específicamente para Tesla, incluido el tuyo en los Cayos.")]},
  "marathon": {"name": "Marathon", "county": "monroe", "img": "cars/model-x/model-x-red-5",
    "lead": "Cayos Medios, el Seven Mile Bridge y agua abierta a ambos lados. Un Tesla de Marathon vive en aire salino y sol.",
    "intro": [
      "Tesla Boutique Miami lleva protección de pintura, recubrimiento cerámico y polarizado, creados exclusivamente para Tesla, a propietarios en Marathon, FL. En el corazón de los Cayos Medios, cerca del Seven Mile Bridge, Marathon está rodeada de agua abierta, lo que significa que un Tesla aquí enfrenta aire salino constante, sol intenso y los largos kilómetros de autopista de la vida isleña.",
      "Protegemos los Teslas de Marathon con film XPEL original contra escombros del camino y UV, recubrimiento cerámico Fusion Plus para que la sal se enjuague fácil, y polarizado cerámico XPEL Prime XR Plus para bloquear el calor del cielo abierto. Los patrones son por modelo y quedan registrados a tu VIN. Atendemos a propietarios de Marathon con cita en nuestro taller de Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden Marathon en los Cayos?",
       "Sí, con cita. Como las instalaciones son en nuestro taller de Doral, coordinamos los tiempos para el viaje por la Overseas Highway. Llama al (786) 505-6162 para planificarlo."),
      ("¿El aire salino cruzando el Seven Mile Bridge es malo para mi Tesla?",
       "Agua abierta a ambos lados significa exposición fuerte a la sal. Un recubrimiento cerámico más PPF da la mejor protección: enjuague fácil de la sal, resistencia UV y defensa contra picaduras en los largos kilómetros de autopista."),
      ("¿Cuánto tarda la protección si subo manejando desde Marathon?",
       "Planificamos el trabajo en torno a un solo viaje: deja el auto en nuestro taller de Doral y completamos el PPF, el polarizado o el cerámico para que vuelva totalmente protegido. Los tiempos dependen de la cobertura; los confirmamos por adelantado.")]},
  "tavernier": {"name": "Tavernier", "county": "monroe", "img": "cars/model-3/model-3-grey-5",
    "lead": "Una comunidad tranquila de los Cayos Altos en la US-1. Un Tesla de Tavernier igual enfrenta el aire salino y el sol de la vida isleña cada día.",
    "intro": [
      "Tesla Boutique Miami ofrece protección de pintura, recubrimiento cerámico y polarizado premium solo para Tesla a propietarios en Tavernier, FL. Una comunidad residencial de los Cayos Altos justo al sur de Key Largo, Tavernier significa vida diaria en la US-1, rodeada de agua y sol, con el aire salino trabajando constantemente sobre la pintura, el vidrio y los interiores.",
      "Protegemos los Teslas de Tavernier con film XPEL original contra picaduras y UV, recubrimiento cerámico Fusion Plus que hace fácil enjuagar la sal, y polarizado cerámico XPEL Prime XR Plus para cortar el calor y proteger el interior. Los patrones son por modelo y quedan registrados a tu VIN. Atendemos a propietarios de Tavernier con cita en nuestro taller de Doral."],
    "services": ["paint-protection-film", "ceramic-coating", "window-tint"],
    "faqs": [
      ("¿Atienden a propietarios de Tesla en Tavernier?",
       "Sí, con cita. Tavernier está en los Cayos Altos, un viaje manejable por la US-1 hasta nuestro taller de Doral. Llama al (786) 505-6162 y coordinamos los tiempos."),
      ("¿Cuál es la protección más importante para un Tesla de los Cayos?",
       "Un recubrimiento cerámico para manejar la sal y el UV, junto con PPF al frente para detener picaduras en los largos kilómetros de la US-1. El polarizado cerámico mantiene la cabina fresca bajo el sol isleño."),
      ("¿Instalan productos XPEL originales?",
       "Siempre. Como distribuidor exclusivo XPEL usamos solo film y recubrimientos XPEL originales, registrados al VIN de tu Tesla con la garantía de fábrica completa.")]},
}

def sa_postcard_es(rootp, href, img, pills, title, text, cta="Explorar"):
    pill_html = "".join('<span class="pill">%s</span>' % p for p in pills)
    img_html = S.pic(rootp, img, "%s - protección Tesla por Tesla Boutique Miami" % title, 700, 438)
    if href:
        return ('<a class="project-tile reveal" href="%s">%s<div class="project-tile-body">'
                '<div class="tag-row">%s</div><h3>%s</h3><p>%s</p>'
                '<span class="card-link">%s &rarr;</span></div></a>' % (href, img_html, pill_html, title, text, cta))
    return ('<div class="project-tile reveal">%s<div class="project-tile-body">'
            '<div class="tag-row">%s</div><h3>%s</h3><p>%s</p>'
            '<span class="card-link" style="opacity:.55">Próximamente</span></div></div>' % (img_html, pill_html, title, text))

def sa_why_es(place):
    return ('<section class="section section-grad"><div class="container">'
            '<div class="section-header"><span class="section-tag">Por qué Tesla Boutique Miami</span>'
            '<h2 class="section-title">¿Por qué elegir Tesla Boutique Miami?</h2></div><div class="why-grid">'
            '<div class="why-item reveal"><span class="why-number">01</span><h3>Solo especialistas Tesla</h3>'
            '<p>Trabajamos exclusivamente en Tesla. Conocemos cada panel, sensor y cámara del Model 3, Y, S, X y Cybertruck, así que los propietarios de %s reciben patrones hechos para Tesla, no adaptados.</p></div>'
            '<div class="why-item reveal"><span class="why-number">02</span><h3>Distribuidor exclusivo XPEL</h3>'
            '<p>Distribuidor exclusivo XPEL autorizado con más de 15 años instalando PPF, cerámico y films. Solo productos XPEL originales, con garantía de fábrica registrada a tu VIN.</p></div>'
            '<div class="why-item reveal"><span class="why-number">03</span><h3>Hecho para el sur de Florida</h3>'
            '<p>El aire salino, el sol intenso y los caminos con escombros son justo lo que protegemos a diario. Nuestras recomendaciones se ajustan a cómo se manejan los Teslas en %s.</p></div>'
            '<div class="why-item reveal"><span class="why-number">04</span><h3>Trabajo impecable y documentado</h3>'
            '<p>Bordes envueltos con precisión, una bahía de instalación controlada en Doral, y cada proyecto fotografiado, para que veas exactamente el acabado que sale de nuestro taller.</p></div>'
            '</div></div></section>') % (place, place)

def sa_cta_es(esp, title, desc):
    return ('<section class="cta-section"><div class="container"><div class="cta-content">'
            '<h2 class="cta-title">%s</h2><p class="cta-desc">%s</p><div class="cta-buttons">'
            '<a href="tel:%s" class="btn btn-primary btn-lg">%s</a>'
            '<a href="%sindex.html#contact" class="btn btn-outline btn-lg">Enviar consulta</a>'
            '<a href="https://www.unlimitedwraps.com/contact-us" target="_blank" rel="noopener" class="btn btn-outline btn-lg">Reservar vía Unlimited Wraps</a>'
            '</div></div></div></section>' % (title, desc, PHONE_TEL, PHONE_DISP, esp))

def build_service_area_hub_es():
    path = "service-area/index.html"; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Zona de Servicio", "")])
    hero = S.page_hero(rootp, "cars/model-s/model-s-blue-1", 'Zona de <span class="highlight">Servicio</span> Tesla en el Sur de Florida',
        "Tesla Boutique Miami protege Teslas en todo el sur de Florida. Encuentra tu condado y ciudad para ver cómo mantenemos tu Tesla impecable en tu zona.", "", crumbs)
    intro = ('<section class="section"><div class="container"><div class="prose">'
             '<h2>Dónde protegemos Teslas</h2>'
             '<p>Con base en Doral, Tesla Boutique Miami atiende a propietarios de Tesla en todo el sur de Florida con protección de pintura XPEL original, recubrimiento cerámico, polarizado y wraps personalizados. Hemos organizado nuestra zona de servicio por condado y ciudad para que veas exactamente cómo protegemos Teslas donde vives y manejas: las carreteras locales, el clima y los riesgos cotidianos que enfrenta tu Model 3, Y, S, X o Cybertruck.</p>'
             '<p>Elige tu condado abajo para empezar. Cada zona enlaza a las ciudades que atendemos, con detalle local y los servicios que más recomendamos.</p>'
             '</div></div></section>')
    cards = ""
    for c in COUNTIES_ES:
        live = bool(c["cities"])
        href = esp + "service-area/%s/index.html" % c["slug"] if live else ""
        text = c["lead"] if live else c["lead"] + " Proximamente."
        cards += sa_postcard_es(rootp, href, c["img"], [c["tag"]], c["name"], text, cta="Explorar %s" % c["short"])
    grid = ('<section class="section section-alt"><div class="container">'
            '<div class="section-header"><span class="section-tag">Por condado</span>'
            '<h2 class="section-title">Elige tu condado</h2></div>'
            '<div class="project-list-grid">%s</div></div></section>' % cards)
    cta = sa_cta_es(esp, "Protege tu Tesla, estés donde estés en el sur de Florida",
                    "Dinos tu Tesla y tu ciudad, y te recomendamos el paquete correcto de PPF, polarizado y cerámico y una hora conveniente en nuestro taller de Doral.")
    body = hero + intro + grid + cta
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Zona de Servicio", DOMAIN+"/es/service-area/index.html")]),
          json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
            "name": "Zona de Servicio de Tesla Boutique Miami", "url": DOMAIN+"/es/service-area/index.html",
            "description": "Condados y ciudades que atiende Tesla Boutique Miami para PPF, recubrimiento cerámico y polarizado Tesla en el sur de Florida."}, ensure_ascii=False)]
    title = "Zona de Servicio Tesla en Miami y el Sur de Florida | Tesla Boutique Miami"
    desc = "Tesla Boutique Miami atiende a propietarios de Tesla en todo el sur de Florida con PPF, recubrimiento cerámico y polarizado XPEL. Encuentra tu condado y ciudad, de Miami-Dade a los Cayos. Llama al (786) 505-6162."
    return doc_es(path, title, desc, body, active="area", preload="cars/model-s/model-s-blue-1", extra_ld=ld)

def build_county_es(c):
    slug = c["slug"]; path = "service-area/%s/index.html" % slug; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Zona de Servicio", esp+"service-area/index.html"), (c["name"], "")])
    hero = S.page_hero(rootp, c["img"], 'Protección Tesla en <span class="highlight">%s</span>' % c["name"], c["lead"], "", crumbs)
    intro = "".join("<p>%s</p>" % p for p in c["intro"])
    intro_sec = ('<section class="section"><div class="container"><div class="prose">'
                 '<h2>Protegiendo Teslas en %s</h2>%s</div></div></section>' % (c["short"], intro))
    cards = ""
    for cs in c["cities"]:
        ci = CITIES_ES[cs]
        cards += sa_postcard_es(rootp, esp+"service-area/%s/%s.html" % (slug, cs), ci["img"],
                                [ci["name"]], ci["name"] + ", FL", ci["lead"], cta="Proteccion Tesla en %s" % ci["name"])
    grid = ('<section class="section section-alt"><div class="container">'
            '<div class="section-header"><span class="section-tag">Ciudades que atendemos</span>'
            '<h2 class="section-title">Encuentra tu ciudad en %s</h2></div>'
            '<div class="project-list-grid">%s</div></div></section>' % (c["short"], cards))
    svc = service_cards_es("Lo que hacemos", "Servicios Tesla que recomendamos", esp,
                           ["paint-protection-film", "window-tint", "ceramic-coating"])
    cta = sa_cta_es(esp, "Protege tu Tesla en %s" % c["short"],
                    "Elige tu ciudad arriba para el detalle local, o dinos tu Tesla y te recomendamos la protección correcta y una hora en nuestro taller de Doral.")
    body = hero + intro_sec + grid + svc + cta
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Zona de Servicio", DOMAIN+"/es/service-area/index.html"),
                               (c["name"], "%s/es/service-area/%s/index.html" % (DOMAIN, slug))])]
    title = "Tesla PPF, Cerámico y Polarizado en %s | Tesla Boutique Miami" % c["name"]
    desc = (c["lead"][:150]).rsplit(" ", 1)[0] + " PPF, cerámico y polarizado XPEL. Llama al (786) 505-6162."
    return doc_es(path, title, desc, body, active="area", preload=c["img"], extra_ld=ld)

def build_city_es(slug, d):
    county = COUNTY_BY_SLUG_ES[d["county"]]; cslug = county["slug"]
    path = "service-area/%s/%s.html" % (cslug, slug); esp, rootp = esp_root(path); city = d["name"]
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Zona de Servicio", esp+"service-area/index.html"),
                             (county["name"], esp+"service-area/%s/index.html" % cslug), (city, "")])
    ctas = ('<div class="hero-ctas"><a href="tel:%s" class="btn btn-primary btn-lg">Pedir cotización</a>'
            '<a href="%sindex.html#contact" class="btn btn-outline btn-lg">Enviar consulta</a></div>' % (PHONE_TEL, esp))
    hero = S.page_hero(rootp, d["img"], 'Protección Tesla en <span class="highlight">%s, FL</span>' % city, d["lead"], ctas, crumbs)
    intro = "".join("<p>%s</p>" % p for p in d["intro"])
    intro_sec = ('<section class="section"><div class="container"><div class="prose">'
                 '<h2>PPF, cerámico y polarizado premium para Tesla en %s, FL</h2>%s</div></div></section>' % (city, intro))
    svc = service_cards_es("Para propietarios de Tesla en %s" % city, "Nuestros servicios", esp, d["services"])
    why = sa_why_es(city)
    fq = faq_es(d["faqs"])
    rel_chips = [chip(esp+"service-area/%s/index.html" % cslug, "Todo %s" % county["short"])]
    for cs in county["cities"]:
        if cs != slug:
            rel_chips.append(chip(esp+"service-area/%s/%s.html" % (cslug, cs), CITIES_ES[cs]["name"]))
    rel = related_es(rel_chips)
    cta = sa_cta_es(esp, "Listo para proteger tu Tesla en %s" % city,
                    "Dinos tu modelo y que buscas. Te recomendamos el PPF, polarizado o ceramico correcto para manejar en %s y agendamos una hora en nuestro taller de Doral." % city)
    body = hero + intro_sec + svc + why + fq + rel + cta
    service_ld = json.dumps({"@context": "https://schema.org", "@type": "Service",
        "name": "Protección de pintura, recubrimiento cerámico y polarizado Tesla en %s" % city,
        "serviceType": "Protección de pintura, recubrimiento cerámico y polarizado de autos",
        "brand": {"@type": "Brand", "name": "XPEL"},
        "provider": {"@type": "AutoBodyShop", "name": "Tesla Boutique Miami", "telephone": "+1-786-505-6162", "url": DOMAIN+"/es/",
                     "address": {"@type": "PostalAddress", "streetAddress": "1835 NW 79th Ave", "addressLocality": "Doral", "addressRegion": "FL", "postalCode": "33126", "addressCountry": "US"}},
        "areaServed": {"@type": "City", "name": city + ", FL"}, "description": d["lead"]}, ensure_ascii=False)
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Zona de Servicio", DOMAIN+"/es/service-area/index.html"),
                               (county["name"], "%s/es/service-area/%s/index.html" % (DOMAIN, cslug)),
                               (city, "%s/es/%s" % (DOMAIN, path))]), service_ld, S.faq_ld(d["faqs"])]
    title = "Tesla PPF, Cerámico y Polarizado en %s, FL | Tesla Boutique Miami" % city
    desc = "Protección de pintura, recubrimiento cerámico y polarizado premium para Tesla en %s, FL. XPEL original, especialistas solo en Tesla en la cercana Doral. Llama al (786) 505-6162." % city
    return doc_es(path, title, desc, body, active="area", preload=d["img"], extra_ld=ld)

def main():
    pages = {}
    for slug, d in MODELS_ES.items():
        pages["models/%s.html" % slug] = build_model_es(slug, d)
    pages["models/tesla-model-y-ppf-miami.html"] = build_combo_es()
    for slug, d in SERVICES_ES.items():
        pages["services/%s.html" % slug] = build_service_es(slug, d)
    pages["news/index.html"] = build_news_es()
    for slug, d in POSTS_ES.items():
        pages["news/%s.html" % slug] = build_post_es(slug, d)
    pages["service-area/index.html"] = build_service_area_hub_es()
    for c in COUNTIES_ES:
        if c["cities"]:
            pages["service-area/%s/index.html" % c["slug"]] = build_county_es(c)
    for slug, d in CITIES_ES.items():
        county = COUNTY_BY_SLUG_ES[d["county"]]
        pages["service-area/%s/%s.html" % (county["slug"], slug)] = build_city_es(slug, d)
    for path, html in pages.items():
        full = os.path.join(ROOT, "es", path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote es/%s" % path)
    print("\n%d ES pages generated." % len(pages))

if __name__ == "__main__":
    main()
