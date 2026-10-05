#!/usr/bin/env python3
"""Assembles the Fox Transportation static pages (shared nav, footer, SVG art)."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fox-transportation")

PHONE = "630-261-0800"
PHONE_TEL = "+16302610800"
PHONE_FBT = "630-932-9040"
PHONE_FBT_TEL = "+16309329040"
EMAIL = "dispatch@foxtrans.net"
ADDR1 = "10 E Progress Road"
ADDR2 = "Lombard, IL 60148"

ARROW = '<svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 10h13M11 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'
ICO_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
ICO_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="m3 7 9 6 9-6" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
ICO_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.5" fill="currentColor"/></svg>'

LOGO = '<img class="brand__logo" src="assets/img/fox-logo.webp" alt="Fox Transportation Services Inc, home" width="280" height="293">'

CUR = ' aria-current="page"'
CDN = "https://d2ol7oe51mr4n9.cloudfront.net/user_3InJjoRwe0fRAqbB5OrU49Jvmiy/"
IMG_FLEET = "https://fox-transportation.floot.app/_cdn/static/eaaa88b3-57d3-4c0c-8811-96cab24a5355-fox-brothers-fleet.jpg"  # Fox Brothers fleet photo from foxtrans.net
TEAM = [
    ("Thomas W. Fox", "Transportation management", CDN + "3b7be492-89e2-4a21-8581-4a2c9b8ad8d8.png",
     "Thomas has worked in transportation management since he was about 19, and he learned it from the ground up: driving tractor-trailers, working the docks, hand-loading trailers and putting in more overtime than anyone could count. He still loses sleep over freight, which is exactly the kind of person you want watching yours."),
    ("Ramon G. Fox", "Fleet and drivers", CDN + "91c44d27-a000-4b6e-a9d5-c44dd5dee256.png",
     "Ramon has spent his whole life in trucking. He can back a tractor-trailer faster and straighter than most drivers can pull one forward, and when freight has to move overnight, he is the one up moving it. He runs the Fox tractor-trailer drivers with a firm, fair hand."),
    ("Richard Nisivaco", "Sales and customer accounts · Owner", CDN + "38575cec-166b-48d7-9989-4bf7171ab499.png",
     "Rich brings thirty years of sales experience and works side by side with operations to shape service around what each customer actually needs. He stays on the account after the sale to make sure the standard holds, and as an owner he can make the call on the spot. If Rich promised it, Fox delivers it, even when a single move costs the company money."),
]
HERO = {"video": "", "poster": "", "ending": "", "bytes": 0}
try:
    import json as _json
    HERO.update(_json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero.json"))))
except Exception:
    pass
NAV = [("index.html", "Home"), ("services.html", "Services"), ("equipment.html", "Equipment"),
       ("about.html", "About"), ("carriers.html", "Carriers"), ("contact.html", "Contact")]


# ---------------------------------------------------------------- map
def shield(x, y, n):
    w = 20 if len(n) <= 2 else 26
    return (f'<g class="shield" transform="translate({x} {y})"><rect x="{-w/2}" y="-7" width="{w}" height="14" rx="3"/>'
            f'<text y="3.5">{n}</text></g>')


def chicago_map(uid, hero=False):
    """Schematic Chicagoland: Loop at (442,250), 4px per mile, 45-mile ring."""
    roads = {
        "I-290": "M442 250 L374 252 L366 244 L350 222 L338 210 L306 196",
        "I-88": "M374 252 L366 258 L350 264 L326 276 L286 282 L214 292",
        "I-355": "M350 222 L348 250 L344 298 L376 352",
        "I-294": "M396 176 L384 200 L376 222 L380 254 L392 290 L430 318 L470 328",
        "I-90": "M442 250 L410 232 L374 222 L338 206 L300 198 L230 176",
        "I-94": "M430 236 L412 200 L396 176 L380 130 L372 50",
        "I-90/94": "M442 250 L444 300 L462 324 L500 334",
        "I-55": "M440 256 L406 280 L344 300 L300 340 L262 400",
        "I-57": "M444 300 L432 380 L420 470",
        "I-80": "M200 352 L338 350 L376 352 L460 346 L500 334 L600 318",
    }
    paths = "\n".join(f'<path class="road" pathLength="1" d="{d}"/>' for d in roads.values())
    cities = [
        (442, 250, "CHICAGO", True, 10, -12), (374, 222, "O'Hare", False, 8, -6),
        (406, 274, "Midway", False, 8, 12), (338, 350, "Joliet", False, -38, 16),
        (286, 282, "Aurora", False, -30, 16), (298, 206, "Elgin", False, -12, -10),
        (394, 118, "Waukegan", False, -66, 4), (486, 326, "Gary", False, 8, 16),
        (326, 276, "Naperville", False, -34, -8),
    ]
    city_svg = ""
    for x, y, name, big, dx, dy in cities:
        cls = "city city--big" if big else "city"
        r = 5 if big else 3
        city_svg += f'<circle class="dot" cx="{x}" cy="{y}" r="{r}"/><text class="{cls}" x="{x+dx}" y="{y+dy}">{name}</text>'
    shields = shield(322, 320, "55") + shield(250, 287, "88") + shield(346, 280, "355") + shield(381, 134, "94") + shield(250, 351, "80") + shield(378, 238, "294") + shield(262, 186, "90")
    outs = [
        ("M286 282 L214 292 L172 296", 172, 296, "", 0, 0),
        ("M380 130 L372 50 L370 20", 370, 20, "", 0, 0),
        ("M500 334 L600 318 L660 306", 660, 306, "", 0, 0),
        ("M300 340 L262 400 L232 452", 232, 452, "", 0, 0),
    ]
    out_svg = ""
    mask_svg = ""
    for i, (d, ex, ey, label, lx, ly) in enumerate(outs):
        out_svg += f'<path class="out" d="{d}" mask="url(#{uid}-m{i})"/>'
        mask_svg += (f'<mask id="{uid}-m{i}" maskUnits="userSpaceOnUse" x="100" y="0" width="640" height="520">'
                     f'<path class="out-draw" pathLength="1" d="{d}" fill="none" stroke="#fff" stroke-width="12"/></mask>')
        out_svg += f'<circle class="out-head" data-end cx="{ex}" cy="{ey}" r="5"/>'
        if label:
            out_svg += f'<text class="out-label" x="{lx}" y="{ly}">{label}</text>'
    rail = "M406 280 L380 300 L330 330 L284 372 L236 430 L214 470"
    out_svg += f'<path class="rail" d="{rail}" mask="url(#{uid}-mr)"/>'
    mask_svg += (f'<mask id="{uid}-mr" maskUnits="userSpaceOnUse" x="100" y="0" width="640" height="520">'
                 f'<path class="out-draw" pathLength="1" d="{rail}" fill="none" stroke="#fff" stroke-width="14"/></mask>')
    out_svg += '<text class="out-label" x="226" y="416" transform="rotate(-52 226 416)">Rail · major metros</text><text class="out-label" x="176" y="314">Truckload</text><text class="out-label" x="176" y="327">single or team</text>'

    grid = "".join(f'<line class="grid-line" x1="{x}" y1="0" x2="{x}" y2="520"/>' for x in range(180, 660, 40))
    grid += "".join(f'<line class="grid-line" x1="140" y1="{y}" x2="680" y2="{y}"/>' for y in range(40, 500, 40))

    lake = "M402 0 L401 82 L399 118 L412 160 L430 202 L448 250 L462 292 L486 322 L540 318 L600 300 L700 290 L700 0 Z"
    title = "Map of the Chicago area showing the Fox terminal in Lombard and the 45-mile local service ring around Chicago"
    return f'''<div class="map" data-map{' data-hero-map' if hero else ''}>
<svg viewBox="170 30 470 450" role="img" aria-labelledby="{uid}-t">
<title id="{uid}-t">{title}</title>
<defs>{mask_svg}<clipPath id="{uid}-clip"><rect x="140" y="0" width="560" height="520"/></clipPath></defs>
<g aria-hidden="true">
{grid}
<path class="lake" d="{lake}"/><path class="lake-edge" d="{lake}"/>
<text class="city" x="560" y="200" style="fill:#6d8599;letter-spacing:.3em;font-size:10px">LAKE MICHIGAN</text>
<g class="ring-g" data-ring><circle class="ring" cx="442" cy="250" r="180"/>
<text class="ring-label"><textPath href="#{uid}-arc" startOffset="22%">45-mile local service radius</textPath></text></g>
<path id="{uid}-arc" d="M309 353 A168 168 0 0 0 575 353" fill="none"/>
<path class="road road--minor" pathLength="1" d="M250 242 L440 238"/>
{paths}
{shields}
{city_svg}
<g data-outs>{out_svg}</g>
<g class="pin" data-pin transform="translate(348 242)">
<circle class="pin-pulse" r="9"/>
<path class="pin-head" d="M0 0 C-10 -12 -10 -26 0 -26 C10 -26 10 -12 0 0Z"/><circle r="3.6" cy="-17" fill="#fff"/>
<line class="pin-lead" x1="-40" y1="-66" x2="-6" y2="-24"/><g class="pin-label" transform="translate(-160 -104)"><rect width="128" height="38" rx="3"/>
<text x="10" y="16">FOX TERMINAL</text><text class="sub" x="10" y="29">I-355 &amp; NORTH AVE</text></g>
</g>
</g>
</svg>
</div>'''


# ---------------------------------------------------------------- trucks
def cab(x0=0):
    return f'''<g transform="translate({x0} 0)">
<path class="body" d="M24 204 L24 150 Q26 134 42 132 L96 128 L102 74 Q104 60 118 60 L168 60 Q178 60 178 70 L178 204 Z"/>
<path class="glass" d="M108 76 L146 74 L146 108 L104 112 Z"/>
<path class="detail" d="M150 70 L150 196 M24 170 L96 168"/>
<rect class="body" x="16" y="186" width="14" height="18" rx="2"/>
</g>'''


def tire(cx, cy=202, r=20):
    return f'<circle class="tire" cx="{cx}" cy="{cy}" r="{r}"/><circle class="hub" cx="{cx}" cy="{cy}" r="{r*0.35:.1f}"/>'


def truck_svg(uid, length=53, unit="tractor", configurable=False, label=None):
    L = length * 10
    delta = (53 - length) * -10  # offset of rear group relative to the 53 ft drawing
    tt_vis = "" if unit == "tractor" else ' style="opacity:0"'
    st_vis = "" if unit == "straight" else ' style="opacity:0"'
    ribs = f'''<pattern id="{uid}-ribs" x="180" y="0" width="40" height="10" patternUnits="userSpaceOnUse"><line x1="20" y1="0" x2="20" y2="10" class="rib"/></pattern>'''
    lbl = label or f"{length} ft trailer"
    tractor = f'''<g class="fade" data-unit="tractor"{tt_vis}>
<rect class="body" x="24" y="196" width="270" height="10"/>
{cab()}
<rect class="box" data-box x="180" y="46" height="132" style="width:{L}px"/>
<rect data-box x="184" y="50" height="124" fill="url(#{uid}-ribs)" style="width:{L-8}px" class="box-ribs"/>
<rect class="accent-stripe" data-box x="180" y="150" height="6" style="width:{L}px"/>
<path class="detail" d="M300 178 L300 212 M292 212 L308 212"/>
{tire(70)}{tire(214)}{tire(258)}
<g class="move" data-move style="transform:translateX({delta}px)">
<rect class="body" x="596" y="178" width="120" height="10"/>
{tire(626)}{tire(668)}
<path class="detail" d="M708 46 L708 178 M700 206 L716 206 M708 188 L708 206"/>
</g>
<g class="dim-g">
<line class="dim" x1="180" y1="18" x2="180" y2="34"/>
<rect class="dim-line" data-box x="180" y="25.4" height="1.2" style="width:{L}px" fill="currentColor"/>
<line class="dim move" data-move style="transform:translateX({delta}px)" x1="710" y1="18" x2="710" y2="34"/>
<g class="move" data-half style="transform:translateX({delta/2}px)"><rect x="385" y="12" width="120" height="28" fill="#121a21"/>
<text class="dim-label" x="445" y="31" text-anchor="middle" data-len>{lbl}</text></g>
</g>
</g>'''
    straight = f'''<g class="fade" data-unit="straight"{st_vis}>
<rect class="body" x="24" y="196" width="440" height="10"/>
{cab()}
<rect class="box" x="184" y="62" width="280" height="122"/>
<rect x="188" y="66" width="272" height="114" fill="url(#{uid}-ribs)"/>
<rect class="accent-stripe" x="184" y="156" width="280" height="6"/>
<rect class="liftgate" x="464" y="170" width="8" height="40" rx="1"/>
<path class="detail" d="M472 176 L490 176 M472 204 L490 204"/>
{tire(70)}{tire(392)}
<line class="dim" x1="184" y1="30" x2="184" y2="46"/><line class="dim" x1="464" y1="30" x2="464" y2="46"/>
<line class="dim" x1="184" y1="38" x2="464" y2="38"/>
<rect x="244" y="24" width="160" height="28" fill="#121a21"/>
<text class="dim-label" x="324" y="43" text-anchor="middle">Straight truck</text>
<text class="dim-label" x="500" y="196" style="font-size:12px;fill:#f07a3e">LIFT GATE</text>
</g>'''
    if not configurable:
        tractor = tractor if unit == "tractor" else ""
        straight = straight if unit == "straight" else ""
    return f'''<svg class="truck rig__side" viewBox="0 0 780 240" aria-hidden="true" data-truck>
<defs>{ribs}</defs>
<line class="ground" x1="0" y1="224" x2="780" y2="224"/>
{tractor}{straight}
</svg>'''


def rear_svg(door="swing", configurable=False):
    swing = '''<g class="layer" data-door="swing">
<line class="door-line" x1="60" y1="10" x2="60" y2="128"/>
<line class="rod" x1="24" y1="14" x2="24" y2="124"/><line class="rod" x1="44" y1="14" x2="44" y2="124"/>
<line class="rod" x1="76" y1="14" x2="76" y2="124"/><line class="rod" x1="96" y1="14" x2="96" y2="124"/>
<rect class="handle" x="40" y="80" width="10" height="4"/><rect class="handle" x="72" y="80" width="10" height="4"/>
<path class="door-line" d="M8 24h6M8 64h6M8 104h6M106 24h6M106 64h6M106 104h6"/>
</g>'''
    slats = "".join(f'<line class="slat" x1="12" y1="{y}" x2="108" y2="{y}"/>' for y in range(18, 126, 9))
    roll = f'''<g class="layer" data-door="roll">{slats}<rect class="handle" x="50" y="118" width="20" height="5" rx="1"/></g>'''
    lift = '''<g class="layer" data-door="lift">
<line class="slat" x1="12" y1="30" x2="108" y2="30"/><line class="slat" x1="12" y1="60" x2="108" y2="60"/><line class="slat" x1="12" y1="90" x2="108" y2="90"/>
<rect class="handle" x="4" y="132" width="112" height="10" rx="1"/>
</g>'''
    def vis(n):
        return "" if n == door else ' style="opacity:0"'
    if configurable:
        layers = swing.replace('data-door="swing"', f'data-door="swing"{vis("swing")}') + roll.replace('data-door="roll"', f'data-door="roll"{vis("roll")}') + lift.replace('data-door="lift"', f'data-door="lift"{vis("lift")}')
    else:
        layers = {"swing": swing, "roll": roll, "lift": lift}[door]
    return f'''<svg class="rear rig__rear" viewBox="0 0 120 170" aria-hidden="true">
<rect class="frame" x="4" y="4" width="112" height="128" rx="2"/>
{layers}
<rect x="8" y="136" width="104" height="6" fill="#56646f"/>
<circle class="tire" cx="26" cy="154" r="12"/><circle class="tire" cx="94" cy="154" r="12"/>
</svg>'''


def photo(src, alt, caption, fallback, pos="50% 50%"):
    return f'''<figure class="photo" data-photo="{src}" data-alt="{alt}" style="--pos:{pos}">
<div class="photo__fallback" aria-hidden="true">{fallback}</div>
{f'<figcaption>{caption}</figcaption>' + chr(10) if caption else ''}</figure>'''


# ---------------------------------------------------------------- shell
def head(title, desc, page):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#e9ece9">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/fox-icon-32.png">
<link rel="apple-touch-icon" href="assets/img/fox-icon-180.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<!-- DEPLOY STEP: add og:url and og:image with absolute URLs once the live domain is set -->
<link rel="preload" href="assets/fonts/overpass-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/overpass-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Fox Transportation Services, Inc.","url":"https://www.foxtrans.net/","telephone":"+1-{PHONE}","email":"{EMAIL}","address":{{"@type":"PostalAddress","streetAddress":"10 East Progress Road","addressLocality":"Lombard","addressRegion":"IL","postalCode":"60148","addressCountry":"US"}}}}</script>
</head>
<body data-page="{page}">
<div class="env" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
{nav(page)}
<main id="main" tabindex="-1">
'''


def nav(page):
    links = "".join(
        f'<li><a href="{h}"{CUR if h == page else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="nav" data-nav>
<div class="wrap nav__in">
<a class="brand" href="index.html">{LOGO}</a>
<button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-panel" data-nav-toggle><span></span><span></span><span></span><b class="sr-only">Menu</b></button>
<div class="nav__panel" id="nav-panel" data-nav-panel>
<nav aria-label="Main"><ul class="nav__links">{links}</ul></nav>
<a class="nav__phone" href="tel:{PHONE_TEL}">{PHONE}</a>
<a class="btn btn--fox nav__cta" href="quote.html">Request a quote</a>
</div>
</div>
</header>'''


def foot():
    return f'''</main>
<footer class="foot on-dark">
<div class="wrap">
<div class="foot__grid">
<div>
<a class="brand" href="index.html">{LOGO}</a>
<p style="margin-top:20px;max-width:34ch">Local truckload and LTL across Chicagoland. Truckload and rail beyond it. Out of Lombard since 1991.</p>
</div>
<div><h2>Company</h2><ul>
<li><a href="services.html">Services</a></li><li><a href="equipment.html">Equipment</a></li>
<li><a href="about.html">About</a></li><li><a href="carriers.html">Haul for Fox</a></li></ul></div>
<div><h2>Ship with us</h2><ul>
<li><a href="quote.html">Request a quote</a></li><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
<div><h2>Terminal</h2><address>{ADDR1}<br>{ADDR2}<br>Near I-355 &amp; North Avenue</address></div>
</div>
<div class="foot__legal">
<span>© <span data-year>2026</span> Fox Transportation Services, Inc. &amp; Fox Brothers Transfer, Inc.</span>
<span>Fox Transportation Services: USDOT 2238384 · MC 592002</span>
</div>
</div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''


def page_head(crumb, kicker, title_lines, lede):
    lines = "".join(f'<span class="split-line"><span style="--d:{i*0.08:.2f}s">{l}</span></span>' for i, l in enumerate(title_lines))
    return f'''<section class="page-head">
<div class="wrap">
<p class="crumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></p>
<div class="page-head__grid">
<div><p class="kicker" data-reveal>{kicker}</p><h1 class="h-xl" data-reveal-lines>{lines}</h1></div>
<p class="lede" data-reveal style="--d:.3s">{lede}</p>
</div>
<div class="page-head__rule" data-reveal-rule></div>
</div>
</section>'''


def cta_block():
    return f'''<section class="cta on-dark" aria-labelledby="cta-h">
<div class="cta__road" aria-hidden="true"></div>
<div class="wrap cta__grid">
<div>
<p class="kicker" data-reveal>Request a quote</p>
<h2 id="cta-h" data-reveal-lines><span class="split-line"><span>Tell us the pickup,</span></span><span class="split-line"><span style="--d:.08s">the drop and the date.</span></span></h2>
<p class="lede" data-reveal style="--d:.2s;margin-top:1.4rem">Dispatch sorts out the rest: our own trucks inside the 45-mile ring, a vetted carrier or rail beyond it.</p>
</div>
<div class="cta__card" data-reveal="scale" style="--d:.15s">
<a class="btn btn--fox" href="quote.html">Start a quote {ARROW}</a>
<a class="cta__phone" href="tel:{PHONE_TEL}"><small>Call dispatch</small><b>{PHONE}</b></a>
<a class="cta__phone" href="mailto:{EMAIL}"><small>Email</small><b style="font-size:1.2rem">{EMAIL}</b></a>
</div>
</div>
</section>'''


def rig_section(heading_tag="h2", title="Pick the unit. See what shows up at your dock.", kicker="Equipment", sid="rig-h"):
    return f'''<section class="rig on-dark" aria-labelledby="{sid}">
<div class="wrap">
<div class="rig__head">
<div><p class="kicker" data-reveal>{kicker}</p><{heading_tag} id="{sid}" class="h-lg" data-reveal>{title}</{heading_tag}></div>
<p class="lede" data-reveal style="--d:.15s">Fox Brothers Transfer runs 48' and 53' trailers with swing or roll doors, and straight trucks with lift gates for stops without a dock.</p>
</div>
<form class="rig__controls" data-rig aria-label="Equipment options" onsubmit="return false">
<fieldset class="seg"><legend>Unit</legend><div class="seg__opts">
<input type="radio" name="unit" id="{sid}-u1" value="tractor" checked><label for="{sid}-u1">Tractor-trailer</label>
<input type="radio" name="unit" id="{sid}-u2" value="straight"><label for="{sid}-u2">Straight truck</label></div></fieldset>
<fieldset class="seg" data-for="tractor"><legend>Trailer length</legend><div class="seg__opts">
<input type="radio" name="len" id="{sid}-l1" value="53" checked><label for="{sid}-l1">53 ft</label>
<input type="radio" name="len" id="{sid}-l2" value="48"><label for="{sid}-l2">48 ft</label></div></fieldset>
<fieldset class="seg" data-for="tractor"><legend>Rear doors</legend><div class="seg__opts">
<input type="radio" name="door" id="{sid}-d1" value="swing" checked><label for="{sid}-d1">Swing</label>
<input type="radio" name="door" id="{sid}-d2" value="roll"><label for="{sid}-d2">Roll</label></div></fieldset>
</form>
<div class="rig__stage" data-reveal>
<div>{truck_svg(sid + "-t", 53, "tractor", configurable=True)}</div>
<figure class="rig__rear-wrap" style="margin:0">{rear_svg("swing", configurable=True)}<figcaption data-rear-cap>Rear view · swing doors</figcaption></figure>
</div>
<dl class="rig__readout" aria-live="polite" data-readout>
<div><dt>Unit</dt><dd data-r-unit>53 ft trailer</dd></div>
<div><dt>Rear</dt><dd data-r-rear>Swing doors, full-width opening</dd></div>
<div><dt>Best for</dt><dd data-r-use>Full truckloads to a dock</dd></div>
</dl>
</div>
</section>'''


def team_section(heading="Management team", kicker="Who runs Fox", sid="team-h"):
    cards = ""
    for i, (name, role, img, bio) in enumerate(TEAM):
        cards += f'''<article class="person" data-reveal style="--d:{i*0.1:.1f}s">
<div class="person__photo"><img src="{img}" alt="Portrait of {name}" width="150" height="130" loading="lazy" decoding="async"></div>
<div class="person__body"><h3>{name}</h3><span class="person__role">{role}</span><p>{bio}</p></div>
</article>'''
    return f'''<section class="team" aria-labelledby="{sid}">
<div class="wrap">
<div class="team__head"><div><p class="kicker" data-reveal>{kicker}</p><h2 id="{sid}" class="h-lg" data-reveal>{heading}</h2></div>
<p class="lede" data-reveal style="--d:.15s">Decades of Chicagoland freight between them, from the cab, the dock and the sales desk.</p></div>
<div class="team__grid">{cards}</div>
</div>
</section>'''


def write(name, html):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)


# ================================================================ HOME
home = head("Fox Transportation | Chicagoland trucking and truckload freight, Lombard IL",
            "Local truckload and limited LTL within 45 miles of Chicago on Fox Brothers Transfer trucks, plus truckload and rail beyond through Fox Transportation Services. Lombard, IL since 1991.",
            "index.html")
home += f'''
<section class="scrub" data-scrub aria-labelledby="hero-h" data-video="{HERO['video']}" data-poster="{HERO['poster']}" data-ending="{HERO['ending']}" data-bytes="{HERO['bytes']}">
<div class="scrub__stage">
<div class="scrub__media" aria-hidden="true">
<div class="scrub__still" data-still></div>
<video data-video muted playsinline preload="none" tabindex="-1" aria-hidden="true" disablepictureinpicture></video>
<div class="scrub__scrim"></div>
</div>
<svg class="ring" viewBox="0 0 48 48" aria-hidden="true" data-ring-load><circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-opacity=".25" stroke-width="3"/><circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="126" style="stroke-dashoffset:var(--ld,126)" transform="rotate(-90 24 24)"/></svg>
<div class="wrap scrub__bands">
<div class="band band--1" data-band data-a="0" data-b="0.3">
<p class="kicker">Lombard, Illinois · Since 1991</p>
<h1 id="hero-h" class="band__title" data-split>Our trucks in Chicagoland. <span class="fox">The right carrier beyond it.</span></h1>
<p class="band__lede band__late">Truckload and limited LTL on Fox trucks inside 45 miles of Chicago. Single or team drivers, more than 5,000 contracted carriers and rail for everything farther.</p>
<div class="band__actions band__later">
<a class="btn btn--fox" href="quote.html">Request a quote {ARROW}</a>
<a class="btn btn--glass" href="tel:{PHONE_TEL}">Call {PHONE}</a>
</div>
</div>
<div class="band band--2" data-band data-a="0.34" data-b="0.64" data-ramp="0.05">
<p class="band__tag">Dispatch</p>
<h2 class="band__title" data-split>Someone picks up by the second ring.</h2>
<p class="band__lede band__late">Every shipment is tracked and traced, and you hear how it is going the way you prefer: phone, text or email.</p>
</div>
<div class="band band--3" data-band data-a="0.68" data-b="1">
<p class="band__tag">Quotes</p>
<h2 class="band__title" data-split>Send the lane. Hear back within the hour.</h2>
<p class="band__lede band__late">Email a quote request and dispatch replies within the hour. Or call {PHONE}.</p>
<div class="band__actions band__later"><a class="btn btn--fox" href="quote.html">Request a quote {ARROW}</a></div>
</div>
</div>
<div class="scroll-cue" aria-hidden="true" data-cue><i></i>Scroll</div>
</div>
</section>

<section class="markers" aria-label="Fox at a glance">
<div class="wrap markers__grid">
<div class="marker" data-reveal><div class="marker__plate"><small>Since</small><span class="marker__num" data-count="1991" data-plain>1991</span></div>
<p><b>Trucking from Lombard</b>Fox Brothers Transfer, at the same terminal near I-355 and North Avenue.</p></div>
<div class="marker" data-reveal style="--d:.08s"><div class="marker__plate"><small>Local radius</small><span class="marker__num"><span data-count="45">45</span> mi</span></div>
<p><b>Around Chicago</b>Truckload and limited LTL on Fox trucks inside that ring.</p></div>
<div class="marker" data-reveal style="--d:.16s"><div class="marker__plate"><small>Carriers</small><span class="marker__num"><span data-count="5000">5,000</span>+</span></div>
<p><b>Under contract</b>Each with its own authority, a steady service record and sound finances.</p></div>
<div class="marker" data-reveal style="--d:.24s"><div class="marker__plate"><small>Dispatch</small><span class="marker__num"><span data-count="2">2</span> rings</span></div>
<p><b>Or fewer</b>Call Fox Brothers and someone answers within two rings.</p></div>
</div>
</section>

<section class="split" aria-labelledby="split-h">
<div class="wrap">
<div class="split__head">
<div><p class="kicker" data-reveal>Two ways we move freight</p><h2 id="split-h" class="h-lg" data-reveal-lines><span class="split-line"><span>Close to home,</span></span><span class="split-line"><span style="--d:.08s">and past the ring.</span></span></h2></div>
<p class="lede" data-reveal style="--d:.15s">Fox is two companies under one roof in Lombard. One runs trucks around Chicago. The other finds capacity for everything that has to travel farther.</p>
</div>
<div class="split__cols">
<article class="lane lane--local on-dark" data-reveal="left">
<svg class="lane__art" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="6 5"/><circle cx="50" cy="50" r="6" fill="#fff"/></svg>
<span class="lane__idx">01 · Inside 45 miles</span>
<h3>Local truckload &amp; LTL</h3>
<span class="lane__co">Fox Brothers Transfer, Inc.</span>
<p>Our own trucks and our own drivers on Chicagoland pickups and deliveries: full truckloads, plus limited LTL.</p>
<ul><li>48' and 53' trailers</li><li>Swing or roll rear doors</li><li>Straight trucks with lift gates</li><li>Hazmat-certified drivers</li></ul>
</article>
<article class="lane lane--wide" data-reveal style="--d:.12s">
<svg class="lane__art" viewBox="0 0 100 100" aria-hidden="true"><path d="M10 50h70M62 32l18 18-18 18" fill="none" stroke="#111820" stroke-width="6"/></svg>
<span class="lane__idx">02 · Beyond the ring</span>
<h3>Truckload &amp; rail</h3>
<span class="lane__co">Fox Transportation Services, Inc.</span>
<p>Freight headed out of the area moves with a carrier we have vetted, or by rail when the lane calls for it.</p>
<ul><li>Single or team drivers</li><li>More than 5,000 carriers under contract</li><li>Rail service to major metro areas</li><li>Every carrier checked for authority and insurance</li></ul>
</article>
</div>
</div>
</section>

<section class="ringmap" aria-labelledby="ring-h">
<div class="wrap ringmap__grid">
<div data-reveal="scale">{chicago_map("rm")}</div>
<div>
<p class="kicker" data-reveal>The 45-mile ring</p>
<h2 id="ring-h" class="h-lg" data-reveal>Inside it, our trucks. Past it, our network.</h2>
<p class="lede" data-reveal style="--d:.15s;margin-top:1.2rem">The Lombard terminal sits near I-355 and North Avenue. Everything within 45 miles of Chicago runs on Fox Brothers equipment. Freight headed farther rides with a contracted carrier, single or team, or goes by rail.</p>
<ul class="legend" data-reveal style="--d:.25s">
<li><i class="legend__ring"></i>Fox Brothers local truckload and LTL</li>
<li><i class="legend__route"></i>Contracted truckload, single or team</li>
<li><i class="legend__rail"></i>Rail to major metro areas</li>
</ul>
</div>
</div>
</section>


<section class="terminal" aria-labelledby="term-h">
<div class="wrap terminal__grid">
<div data-reveal="scale">{photo(IMG_FLEET, "Fox Brothers Transfer tractors lined up at the Lombard terminal", "", truck_svg("ph1", 53, "tractor").replace('rig__side', ''), "58% 45%")}</div>
<div>
<p class="kicker" data-reveal>Home base</p>
<h2 id="term-h" class="h-lg" data-reveal-lines><span class="split-line"><span>Off I-355,</span></span><span class="split-line"><span style="--d:.08s">in Lombard.</span></span></h2>
<p class="lede" data-reveal style="--d:.15s;margin-top:1.2rem">The terminal sits near I-355 and North Avenue in Lombard, with I-88, I-290 and I-294 all a short run away. That puts O'Hare, the western suburbs and the city within easy reach of a local run.</p>
<div class="terminal__addr" data-reveal style="--d:.25s"><b>{ADDR1}</b><span>{ADDR2}</span></div>
</div>
</div>
</section>

<section class="reasons" aria-labelledby="why-h">
<div class="wrap reasons__grid">
<div class="reasons__sticky">
<p class="kicker" data-reveal>Why shippers call Fox</p>
<h2 id="why-h" class="h-lg" data-reveal-lines><span class="split-line"><span>Freight people</span></span><span class="split-line"><span style="--d:.08s">who know the</span></span><span class="split-line"><span style="--d:.16s">Chicago map.</span></span></h2>
</div>
<ol>
<li class="reason" data-reveal><div><h3>Drivers cleared for hazmat</h3><p>Every Fox Brothers driver holds hazardous materials certification, so a regulated load does not mean hunting for a qualified driver.</p></div></li>
<li class="reason" data-reveal><div><h3>A person on the line</h3><p>Someone answers your call within two rings, every shipment is tracked and traced, and updates come the way you want them: phone, text or email.</p></div></li>
<li class="reason" data-reveal><div><h3>Covered on every Fox truck</h3><p>Fox Brothers carries high value insurance, so your freight is covered while it rides with us.</p></div></li>
<li class="reason" data-reveal><div><h3>Carriers we are willing to sign for</h3><p>Every carrier under contract has its own operating authority, a record of consistent service and sound finances, plus $1,000,000 liability and $100,000 cargo coverage.</p></div></li>
<li class="reason" data-reveal><div><h3>Chicagoland since 1991</h3><p>More than three decades working out of the same Lombard terminal: the docks, the expressways and the timing of a Chicago day are familiar ground.</p></div></li>
</ol>
</div>
</section>

{team_section()}

<section class="haul" aria-labelledby="haul-h">
<div class="wrap haul__in">
<div><h2 id="haul-h">Own your authority? Haul for Fox.</h2><p>Carriers get paid the same day the shipment delivers, with no quick pay deductions. Guaranteed.</p></div>
<a class="btn" href="carriers.html">Carrier requirements {ARROW}</a>
</div>
</section>

{cta_block()}
'''
home += foot()
write("index.html", home)

# ================================================================ SERVICES
svc = head("Services | Fox Transportation", "Local truckload and limited LTL within 45 miles of Chicago, truckload with single or team drivers, rail to major metro areas and hazmat-certified drivers.", "services.html")
svc += page_head("Services", "What we haul, and how", ["Four ways to", "move it."],
                 "Local work runs on Fox Brothers Transfer trucks. Anything headed farther goes through Fox Transportation Services, on a contracted carrier or by rail.")
blocks = [
    ("01", "Local truckload &amp; limited LTL", "Fox Brothers Transfer, Inc.",
     ["Pickups and deliveries anywhere within a forty-five mile radius of Chicago, on Fox trucks with Fox drivers.",
      "Full truckloads are the core of the work, with limited LTL alongside. Fox Brothers carries high value insurance, and when you call, someone answers within two rings."],
     [("Area", "Within 45 miles of Chicago"), ("Service", "Truckload · limited LTL"), ("Trailers", "48' and 53', swing or roll doors"), ("Also", "Straight trucks with lift gates"), ("Insurance", "High value coverage")], False),
    ("02", "Truckload beyond Chicagoland", "Fox Transportation Services, Inc.",
     ["When freight leaves the local ring, dispatch researches the lane and presents the best carrier at a fair and reasonable price, drawn from more than 5,000 truckload and LTL carriers under contract.",
      "Loads that need to keep rolling can run with team drivers. Every shipment is tracked and traced, and you hear about it by phone, text or email, whichever you prefer."],
     [("Drivers", "Single or team"), ("Network", "5,000+ truckload and LTL carriers"), ("Tracking", "Every shipment, traced"), ("Standard", "Own authority, consistent service, sound finances"), ("Coverage", "$1M liability · $100K cargo")], True),
    ("03", "Rail", "Fox Transportation Services, Inc.",
     ["Rail service to major metro areas, for freight that suits a rail move better than a long highway run."],
     [("Coverage", "Major metro areas"), ("Booked by", "Fox Transportation Services"), ("Start with", "Origin, destination and ready date")], False),
    ("04", "Hazardous materials", "Fox Brothers Transfer, Inc.",
     ["Every Fox Brothers driver is hazardous materials certified and brings years of experience. Tell dispatch what the load is when you ask for a quote, and it goes to the right truck."],
     [("Drivers", "All hazmat certified"), ("Area", "Within 45 miles of Chicago"), ("Tell us", "Commodity, class and quantity")], False),
]
for num, title, by, paras, specs, dark in blocks:
    ps = "".join(f"<p>{p}</p>" for p in paras)
    sp = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in specs)
    svc += f'''<section class="svc{' svc--dark on-dark' if dark else ''}" aria-labelledby="svc-{num}">
<div class="wrap svc__grid">
<div class="svc__num" data-reveal aria-hidden="true">{num}</div>
<div class="svc__body" data-reveal style="--d:.08s"><h2 id="svc-{num}">{title}</h2><span class="svc__by">{by}</span>{ps}</div>
<dl class="specs" data-reveal style="--d:.16s">{sp}</dl>
</div>
</section>'''
svc += f'''<section class="steps" aria-labelledby="steps-h">
<div class="wrap">
<p class="kicker" data-reveal>How a load gets moving</p>
<h2 id="steps-h" class="h-lg" data-reveal>Three steps, one call.</h2>
<div class="steps__row">
<div class="step" data-reveal>{ICO_PIN}<h3>Send the lane</h3><p>Pickup, delivery, ready date and what is on the pallets. Emailed quote requests get an answer within the hour.</p></div>
<div class="step" data-reveal style="--d:.1s"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="3 3"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/></svg><h3>We pick the mode</h3><p>Inside the 45-mile ring it goes on a Fox truck. Beyond it, a vetted carrier or rail.</p></div>
<div class="step" data-reveal style="--d:.2s">{ICO_PHONE}<h3>Dispatch confirms</h3><p>Fox dispatch follows up with the plan and the price.</p></div>
</div>
</div>
</section>'''
svc += cta_block() + foot()
write("services.html", svc)

# ================================================================ EQUIPMENT
eq = head("Equipment | Fox Transportation", "48' and 53' trailers with swing or roll doors and straight trucks with lift gates, run by hazmat-certified drivers from Lombard, IL.", "equipment.html")
eq += page_head("Equipment", "The fleet, drawn to scale", ["Built for", "Chicago docks."],
                "Every unit below runs out of the Lombard terminal on local truckload and LTL work. Drawings are to scale, so a 48 against a 53 reads the way it looks at the dock.")
eq += rig_section("h2", "Try the combinations.", "Configure", "rig2")
units = [
    ("53ft", "53 ft trailer", "53' van trailers",
     "The standard full-size trailer for truckload freight, with room for a full floor of pallets.", truck_svg("u53", 53, "tractor"), "assets/photos/trailer-53.jpg"),
    ("48ft", "48 ft trailer", "48' van trailers",
     "Five feet shorter, for docks, yards and city streets where a 53 is a tight fit.", truck_svg("u48", 48, "tractor"), "assets/photos/trailer-48.jpg"),
    ("doors", "Rear doors", "Swing doors or roll doors",
     "Swing doors open the full width of the trailer. A roll door lifts straight up, which helps at crowded docks where there is no room to swing.",
     f'<div style="display:flex;gap:10%;justify-content:center;width:100%">{rear_svg("swing")}{rear_svg("roll")}</div>', ""),
    ("straight", "Straight truck", "Straight trucks with lift gates",
     "A single-chassis truck with a hydraulic lift gate, for deliveries to a curb, a storefront or anywhere without a loading dock.", truck_svg("ust", 53, "straight"), "assets/photos/straight-truck.jpg"),
]
eq += '<section class="units" aria-label="Units"><div class="wrap">'
for key, tag, title, text, art, ph in units:
    inner = art
    if ph:
        inner = f'{art}<figure class="photo" data-photo="{ph}" data-alt="{title} at the Fox terminal" style="background:transparent"><div class="photo__fallback" aria-hidden="true"></div></figure>'
    eq += f'''<article class="unit">
<div class="unit__art" data-reveal="scale">{inner}</div>
<div data-reveal style="--d:.1s"><span class="unit__tag">{tag}</span><h2>{title}</h2><p>{text}</p></div>
</article>'''
eq += '''<article class="unit">
<div class="unit__art" data-reveal="scale" style="aspect-ratio:auto;padding:0;background:transparent"><dl class="specs" style="width:100%">
<div><dt>Certification</dt><dd>Hazardous materials, every driver</dd></div>
<div><dt>Experience</dt><dd>Years in the industry, each driver</dd></div>
<div><dt>Base</dt><dd>10 E Progress Road, Lombard</dd></div></dl></div>
<div data-reveal style="--d:.1s"><span class="unit__tag">Drivers</span><h2>The people in the cab</h2><p>Equipment only matters if the driver knows the job. Fox Brothers drivers are all hazmat certified and experienced in Chicagoland freight.</p></div>
</article>'''
eq += '</div></section>' + cta_block() + foot()
write("equipment.html", eq)

# ================================================================ ABOUT
ab = head("About | Fox Transportation", "Fox Brothers Transfer has trucked out of Lombard, IL since 1991. Fox Transportation Services added truckload brokerage and rail in 2006.", "about.html")
ab += page_head("About", "The company", ["One terminal.", "Two companies."],
                "Fox Brothers Transfer runs the trucks. Fox Transportation Services books the capacity beyond them. Both work from 10 E Progress Road in Lombard.")
ab += f'''<section class="companies" aria-label="Fox companies">
<div class="wrap companies__grid">
<article class="co" data-reveal>
<span class="co__year">1991</span>
<span class="co__role">Motor carrier</span>
<h2>Fox Brothers Transfer, Inc.</h2>
<p>Truckload and limited LTL within a forty-five mile radius of Chicago, from the terminal near I-355 and North Avenue. 48' and 53' trailers, straight trucks with lift gates, hazmat-certified drivers.</p>
<dl class="specs"><div><dt>USDOT</dt><dd><a href="https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&amp;query_type=queryCarrierSnapshot&amp;query_param=USDOT&amp;query_string=515265" rel="noopener">515265</a></dd></div>
<div><dt>Phone</dt><dd><a href="tel:{PHONE_FBT_TEL}">{PHONE_FBT}</a></dd></div></dl>
</article>
<article class="co" data-reveal style="--d:.1s">
<span class="co__year">2006</span>
<span class="co__role">Freight broker</span>
<h2>Fox Transportation Services, Inc.</h2>
<p>Truckload with single or team drivers and rail to major metro areas, through more than 5,000 contracted carriers. Every one has proper authority, a consistent service record and sound finances.</p>
<dl class="specs"><div><dt>USDOT</dt><dd><a href="https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&amp;query_type=queryCarrierSnapshot&amp;query_param=USDOT&amp;query_string=2238384" rel="noopener">2238384</a></dd></div>
<div><dt>MC</dt><dd>592002</dd></div>
<div><dt>Phone</dt><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd></div></dl>
</article>
</div>
</section>
{team_section("Management team", "Who runs Fox", "about-team-h")}
<section class="timeline on-dark" aria-labelledby="tl-h">
<div class="wrap">
<p class="kicker" data-reveal>Timeline</p>
<h2 id="tl-h" class="h-lg" data-reveal>Same address, more reach.</h2>
<div class="timeline__track" data-timeline>
<div class="timeline__fill" aria-hidden="true"></div>
<div class="tl" data-reveal><b>1991</b><p>Fox Brothers Transfer starts trucking from a terminal near I-355 and North Avenue in Lombard.</p></div>
<div class="tl" data-reveal style="--d:.12s"><b>2006</b><p>Fox Transportation Services forms late in the year to take on truckload and rail beyond the local ring.</p></div>
<div class="tl" data-reveal style="--d:.24s"><b>Today</b><p>Local trucks, 5,000+ contracted carriers and rail, all run from 10 E Progress Road.</p></div>
</div>
</div>
</section>
<section class="terminal" aria-labelledby="yard-h">
<div class="wrap terminal__grid">
<div data-reveal="scale">{photo(HERO['ending'] or "assets/photos/yard.jpg", "A Fox tractor on a winter lot, seen low from the front", "Fox Brothers Transfer · Lombard, IL", truck_svg("ph2", 48, "tractor").replace('rig__side', ''), "70% 50%")}</div>
<div>
<p class="kicker" data-reveal>Where we work</p>
<h2 id="yard-h" class="h-lg" data-reveal>Chicago is the job.</h2>
<p class="lede" data-reveal style="--d:.15s;margin-top:1.2rem">Staying local means the expressways, the dock schedules and the suburban truck routes are everyday work, not guesswork. Fox Brothers has run Chicagoland freight from Lombard since 1991.</p>
<a class="btn btn--ghost" href="services.html" data-reveal style="--d:.25s;margin-top:1rem">See services {ARROW}</a>
</div>
</div>
</section>'''
ab += cta_block() + foot()
write("about.html", ab)

# ================================================================ CARRIERS
ca = head("Carriers | Haul for Fox Transportation", "Carrier requirements for Fox Transportation Services: your own MC authority, $100,000 cargo insurance, $1,000,000 liability insurance and a completed W-9.", "carriers.html")
ca += page_head("Carriers", "Haul for Fox", ["Bring your authority.", "We bring the freight."],
                "Fox Transportation Services contracts with carriers that run under their own authority and carry the coverage shippers expect.")
ico_doc = '<svg viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6z M14 3v4h4" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
ico_shield = '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
ico_box = '<svg viewBox="0 0 24 24"><path d="M3 7l9-4 9 4v10l-9 4-9-4z M3 7l9 4 9-4 M12 11v10" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
ico_id = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M7 10h6M7 14h10" stroke="currentColor" stroke-width="2"/></svg>'
ca += f'''<section class="checklist" aria-labelledby="req-h">
<div class="wrap checklist__grid">
<div>
<h2 id="req-h" class="h-md" data-reveal style="margin-bottom:24px">What you need to get set up</h2>
<ul class="req">
<li data-reveal><span class="req__ico" aria-hidden="true">{ico_id}</span><div><b>MC number</b><span>Your own operating authority.</span></div></li>
<li data-reveal style="--d:.08s"><span class="req__ico" aria-hidden="true">{ico_box}</span><div><b>$100,000 cargo insurance</b><span>Certificate naming your company.</span></div></li>
<li data-reveal style="--d:.16s"><span class="req__ico" aria-hidden="true">{ico_shield}</span><div><b>$1,000,000 liability insurance</b><span>Auto liability at or above this limit.</span></div></li>
<li data-reveal style="--d:.24s"><span class="req__ico" aria-hidden="true">{ico_doc}</span><div><b>Completed W-9</b><span>For carrier payment setup.</span></div></li>
</ul>
<h2 class="h-md" data-reveal style="margin:48px 0 16px">Equipment we want to hear about</h2>
<p data-reveal style="color:var(--ink-2);max-width:56ch">Fox Transportation Services coordinates hundreds of shipments each week. Professionalism, dependability and clear communication go a long way here.</p>
<ul class="tags" data-reveal>
<li>Dry vans</li><li>Reefers</li><li>Flatbeds</li><li>Team drivers</li><li>Drop trailers</li><li>Hazmat</li><li>High value insurance</li><li>Produce and perishables</li>
</ul>
</div>
<aside class="note on-dark" data-reveal="scale" style="--d:.1s">
<h2>Paid the day it delivers.</h2>
<p>Fox pays every carrier invoice on receipt of the invoice and POD: the same day the shipment delivers, with no quick pay deductions. Guaranteed. Fox has been on the carrier side too, and knows what waiting to get paid is like.</p>
<p>Email your authority, insurance certificates and W-9 to dispatch, or call to talk through lanes and equipment.</p>
<p style="margin-top:20px"><a class="btn btn--fox" href="mailto:{EMAIL}?subject=Carrier%20setup">Email dispatch {ARROW}</a></p>
<p style="margin:16px 0 0"><a href="tel:{PHONE_TEL}" style="font:800 1.4rem var(--f-display);text-decoration:none">{PHONE}</a></p>
</aside>
</div>
</section>'''
ca += foot()
write("carriers.html", ca)

# ================================================================ QUOTE
qt = head("Request a Quote | Fox Transportation", "Request a freight quote from Fox Transportation: local truckload and LTL around Chicago, truckload with single or team drivers, or rail.", "quote.html")
qt += page_head("Request a quote", "Get a price", ["Where is it", "going?"],
                "Send the lane and dispatch will come back with the plan and a price. Local, truckload or rail, it starts here.")
def chip_group(name, opts, req=False):
    return "".join(f'<input type="radio" name="{name}" id="{name}-{i}" value="{o}"{" required" if req and i == 0 else ""}><label for="{name}-{i}">{o}</label>' for i, o in enumerate(opts))
qt += f'''<section class="quote" aria-label="Quote request">
<div class="wrap quote__grid">
<form class="form" data-quote novalidate aria-describedby="form-note">
<div class="form__body">
<fieldset><legend><span>01</span>The freight</legend>
<div class="fields">
<div class="field field--full"><span class="label" id="svc-l">Service</span><div class="chips" role="radiogroup" aria-labelledby="svc-l">{chip_group("service", ["Local truckload (within 45 mi)", "Local LTL", "Truckload, single driver", "Truckload, team drivers", "Rail", "Not sure"])}</div></div>
<div class="field field--full"><span class="label" id="eq-l">Equipment <span class="opt">optional</span></span><div class="chips" role="radiogroup" aria-labelledby="eq-l">{chip_group("equipment", ["53 ft trailer", "48 ft trailer", "Straight truck with lift gate", "Not sure"])}</div></div>
<div class="field"><label for="q-weight">Weight or pallet count <span class="opt">optional</span></label><input id="q-weight" name="weight" autocomplete="off"></div>
<div class="field"><label for="q-haz">Hazardous materials?</label><select id="q-haz" name="hazmat"><option>No</option><option>Yes</option><option>Not sure</option></select></div>
</div></fieldset>
<fieldset><legend><span>02</span>The lane</legend>
<div class="fields">
<div class="field"><label for="q-from">Pickup city or ZIP</label><input id="q-from" name="pickup" required aria-describedby="q-from-e"><span class="field__err" id="q-from-e"></span></div>
<div class="field"><label for="q-to">Delivery city or ZIP</label><input id="q-to" name="delivery" required aria-describedby="q-to-e"><span class="field__err" id="q-to-e"></span></div>
<div class="field"><label for="q-date">Ready date</label><input id="q-date" name="date" type="date"></div>
<div class="field"><label for="q-freq">How often <span class="opt">optional</span></label><select id="q-freq" name="frequency"><option>One time</option><option>Weekly</option><option>Several times a week</option><option>Daily</option></select></div>
</div></fieldset>
<fieldset><legend><span>03</span>You</legend>
<div class="fields">
<div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required aria-describedby="q-name-e"><span class="field__err" id="q-name-e"></span></div>
<div class="field"><label for="q-co">Company <span class="opt">optional</span></label><input id="q-co" name="company" autocomplete="organization"></div>
<div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" aria-describedby="q-phone-e"><span class="field__err" id="q-phone-e"></span></div>
<div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" aria-describedby="q-email-e"><span class="field__err" id="q-email-e"></span></div>
<div class="field field--full"><label for="q-notes">Anything else <span class="opt">optional</span></label><textarea id="q-notes" name="notes" placeholder="Dock hours, appointment times, commodity, special handling"></textarea></div>
</div></fieldset>
<div class="form__foot">
<p id="form-note">Sending opens your email app with this request addressed to {EMAIL}. Prefer the phone? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<button class="btn btn--fox" type="submit">Send request {ARROW}</button>
</div>
</div>
<div class="form__done" role="status" tabindex="-1" data-done>
<h2>Your request is ready to send.</h2>
<p>Your email app should have opened with the request addressed to <a href="mailto:{EMAIL}">{EMAIL}</a>. Press send there and dispatch will pick it up.</p>
<p>Nothing opened? Call <a href="tel:{PHONE_TEL}">{PHONE}</a> or <a href="#" data-copy>copy the request</a> and email it yourself.</p>
</div>
</form>
<aside class="aside">
<div class="aside__card on-dark"><h2>Faster by phone</h2><a class="big" href="tel:{PHONE_TEL}">{PHONE}</a><p>Fox Transportation Services dispatch</p></div>
<div class="aside__card on-dark"><h2>Local cartage</h2><a class="big" href="tel:{PHONE_FBT_TEL}">{PHONE_FBT}</a><p>Fox Brothers Transfer</p></div>
<div class="aside__list"><h2>Helps us price it</h2><ul><li>Exact pickup and delivery addresses</li><li>Dock or lift gate at each end</li><li>Pallet count, weight and dimensions</li><li>Hazmat class, if any</li></ul></div>
</aside>
</div>
</section>'''
qt += foot()
write("quote.html", qt)

# ================================================================ CONTACT
ct = head("Contact | Fox Transportation", "Fox Transportation, 10 E Progress Road, Lombard, IL 60148. Dispatch 630-261-0800, dispatch@foxtrans.net.", "contact.html")
ct += page_head("Contact", "Reach dispatch", ["Call, email", "or stop by."],
                "One terminal in Lombard, near I-355 and North Avenue. For a price, the quote form is the quickest route.")
ct += f'''<section class="contact" aria-label="Contact details">
<div class="wrap contact__grid">
<div class="lines">
<a class="line" href="tel:{PHONE_TEL}" data-reveal><div><small>Fox Transportation Services</small><b>{PHONE}</b><span>Truckload, team and rail</span></div>{ICO_PHONE}</a>
<a class="line" href="tel:{PHONE_FBT_TEL}" data-reveal style="--d:.06s"><div><small>Fox Brothers Transfer</small><b>{PHONE_FBT}</b><span>Local truckload and LTL</span></div>{ICO_PHONE}</a>
<a class="line" href="mailto:{EMAIL}" data-reveal style="--d:.12s"><div><small>Email</small><b>{EMAIL}</b></div>{ICO_MAIL}</a>
<a class="line" href="https://www.google.com/maps/search/?api=1&amp;query=10+E+Progress+Rd+Lombard+IL+60148" rel="noopener" data-reveal style="--d:.18s"><div><small>Terminal</small><b>{ADDR1}</b><span>{ADDR2}</span></div>{ICO_PIN}</a>
<a class="btn btn--fox" href="quote.html" data-reveal style="--d:.24s;margin-top:8px">Request a quote {ARROW}</a>
</div>
<div data-reveal="scale">{chicago_map("cm")}</div>
</div>
</section>'''
ct += foot()
write("contact.html", ct)
print("ok")
