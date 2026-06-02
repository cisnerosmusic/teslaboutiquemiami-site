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
           '<span class="logo-sub">Impulsado por <strong>UnlimitedWraps</strong></span>'
           '<span class="logo-sub logo-xpel">Distribuidor Exclusivo XPEL</span>')

def header_es(esp, rootp, en_path, active=""):
    md = "".join('<li><a href="%smodels/%s.html">%s</a></li>' % (esp, s, l) for s, l in MODELS_NAV)
    sd = "".join('<li><a href="%sservices/%s.html">%s</a></li>' % (esp, s, l) for s, l in SERVICES_NAV_ES)
    cur = lambda k: ' aria-current="page"' if active == k else ""
    return ('<header class="header" id="header"><div class="container"><div class="header-inner">'
        '<a href="%sindex.html" class="logo" aria-label="Tesla Boutique Miami inicio">%s</a>'
        '<button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="primary-nav">%s</button>'
        '<nav class="main-nav" id="primary-nav" aria-label="Principal"><ul class="main-nav-links">'
        '<li class="has-dropdown"><a href="%sindex.html#models"%s>Modelos Tesla</a><ul class="dropdown">%s</ul></li>'
        '<li class="has-dropdown"><a href="%sindex.html#services"%s>Servicios</a><ul class="dropdown">%s</ul></li>'
        '<li><a href="%sprojects/index.html"%s>Proyectos</a></li>'
        '<li><a href="%snews/index.html"%s>Updates</a></li>'
        '<li><a href="%sindex.html#contact">Contacto</a></li></ul>'
        '<div class="lang-switch" aria-label="Idioma"><a href="%s%s">EN</a><a href="#" aria-current="true">ES</a></div></nav>'
        '<div class="header-cta"><a href="tel:%s" class="header-phone">%s<span>%s</span></a>'
        '<a href="%sindex.html#contact" class="btn btn-primary">Reservar</a></div>'
        '</div></div></header>') % (
        esp, LOGO_ES, svg('<path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>'),
        esp, cur("models"), md, esp, cur("services"), sd,
        esp, cur("projects"), esp, cur("news"), esp,
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
    preload_tag = ('<link rel="preload" as="image" href="%sassets/img/%s.webp" fetchpriority="high">' % (rootp, preload)) if preload else ""
    ld = "".join('<script type="application/ld+json">%s</script>\n' % b for b in (extra_ld or []))
    return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n'
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
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
        '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">\n'
        '%s\n<link rel="stylesheet" href="%sassets/css/style.css">\n%s</head>\n<body>\n%s\n<main>\n%s\n</main>\n%s\n'
        '<script src="%sassets/js/main.js" defer></script>\n</body>\n</html>\n') % (
        title, desc, canonical, en_url, canonical, en_url, title, desc, canonical,
        DOMAIN, (preload or "model-s"), preload_tag, rootp, ld,
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
  "model-3": dict(name="Model 3", img="tesla-model-3-ppf-doral",
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
  "model-y": dict(name="Model Y", img="tesla-model-y-window-tinting",
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
  "model-s": dict(name="Model S", img="tesla-model-s-ceramic-coating",
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
  "model-x": dict(name="Model X", img="tesla-model-x-full-body-ppf",
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
  "cybertruck": dict(name="Cybertruck", img="tesla-cybertruck-ppf-miami",
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
  "windshield-protection": dict(name="Protección de Parabrisas", img="model-s",
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
              chip(esp+"services/ceramic-coating.html", "Cerámico Tesla"),
              chip(esp+"projects/index.html", "Ver proyectos %s" % name)]
    rel = related_es(chips)
    cta = cta_es("Protege tu %s" % name, "Dinos tu color y cómo manejas, y te recomendamos la combinación correcta de PPF, polarizado y cerámico para tu %s." % name)
    body = hero + intro_sec + svc + pk + sp + fq + rel + cta
    ld = [S.breadcrumb_ld("", [("Inicio", DOMAIN+"/es/"), ("Modelos Tesla", DOMAIN+"/es/#models"), (name, "%s/es/models/%s.html" % (DOMAIN, slug))]), S.faq_ld(d["faqs"])]
    title = "Tesla %s: PPF, Cerámico y Polarizado en Miami | Tesla Boutique Miami" % name
    desc = "Protege tu Tesla %s en Miami y Doral: protección de pintura XPEL, recubrimiento cerámico y polarizado cerámico. Paquetes, proyectos y preguntas frecuentes. Llama al (786) 505-6162." % name
    return doc_es(path, title, desc, body, active="models", preload=d["img"], extra_ld=ld)

def build_service_es(slug, d):
    path = "services/%s.html" % slug
    esp, rootp = esp_root(path); name = d["name"]
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Servicios", esp+"index.html#services"), (name, "")])
    extra = '<a href="#packages" class="btn btn-outline btn-lg">Ver más</a>' if d.get("options") else ""
    ctas = '<div class="hero-ctas"><a href="tel:%s" class="btn btn-primary btn-lg">Pedir cotización</a>%s</div>' % (PHONE_TEL, extra)
    hero = S.page_hero(rootp, d["img"], d["h1"], d["lead"], ctas, crumbs)
    secs = ""
    for h2, paras in d["sections"]:
        inner = "".join(p if p.lstrip().startswith("<ul") else "<p>%s</p>" % p for p in paras)
        secs += '<section class="section"><div class="container"><div class="prose"><h2>%s</h2>%s</div></div></section>' % (h2, inner)
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
    body = hero + secs + opts + bymodel + fq + cta
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
                      chip("../projects/index.html", "Proyectos de PPF Model Y"), chip("../services/paint-protection-film.html", "Sobre el PPF de XPEL")])
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

def build_news_es():
    path = "news/index.html"; esp, rootp = esp_root(path)
    crumbs = crumbs_es(esp, [("Inicio", esp+"index.html"), ("Updates", "")])
    hero = S.page_hero(rootp, "tesla-model-s-ceramic-coating", 'Tesla Boutique <span class="highlight">Updates</span>',
        "Noticias y recursos de Tesla Boutique Miami: proyectos nuevos, novedades de productos XPEL y consejos prácticos para cuidar el film, el recubrimiento y el polarizado de tu Tesla. Actualizado seguido.", "", crumbs)
    posts = [
        ("Tesla", "¿Cuándo poner PPF tras comprar un Tesla?", "La respuesta corta: antes del primer viaje largo. Aquí explicamos por qué proteger la pintura de fábrica importa más."),
        ("Mantenimiento", "Cuidar tu PPF y cerámico en Miami", "Hábitos simples de lavado que mantienen el film XPEL y el cerámico Fusion Plus rindiendo por años bajo el calor de Florida."),
        ("XPEL", "Ultimate Plus vs Stealth: ¿qué acabado de PPF es para ti?", "¿Brillante o satinado? Una guía rápida para elegir el acabado de film XPEL que le va a tu Tesla."),
        ("Mantenimiento", "Quitar manchas de agua del vidrio y la pintura", "Qué causa las manchas de agua dura en el sur de Florida y cómo quitarlas con seguridad sin dañar tu acabado."),
    ]
    cards = ""
    for i, (pill, h3, p) in enumerate(posts):
        if i == 0:
            meta = '<span class="post-date">Publicado &middot; Mayo 2026</span>'
            link = '<a class="card-link" href="#">Leer artículo &rarr;</a>'
        else:
            meta = ''
            link = '<span class="card-link">Próximamente</span>'
        cards += ('<div class="project-tile reveal"><div class="project-tile-body"><div class="tag-row"><span class="pill">%s</span></div>%s'
                  '<h3>%s</h3><p>%s</p>%s</div></div>') % (pill, meta, h3, p, link)
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

def main():
    pages = {}
    for slug, d in MODELS_ES.items():
        pages["models/%s.html" % slug] = build_model_es(slug, d)
    pages["models/tesla-model-y-ppf-miami.html"] = build_combo_es()
    for slug, d in SERVICES_ES.items():
        pages["services/%s.html" % slug] = build_service_es(slug, d)
    pages["projects/index.html"] = build_projects_index_es()
    pages["projects/sample-tesla-model-y-full-front-ppf.html"] = build_project_sample_es()
    pages["news/index.html"] = build_news_es()
    for path, html in pages.items():
        full = os.path.join(ROOT, "es", path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote es/%s" % path)
    print("\n%d ES pages generated." % len(pages))

if __name__ == "__main__":
    main()
