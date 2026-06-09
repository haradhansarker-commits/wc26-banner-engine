#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIFA World Cup 2026 — Bengali "Team vs Team" banner/thumbnail template.
Stadium Lithograph aesthetic. 16:9, batch-ready, procedural flags (no external images).
"""
import base64, os, subprocess, math

W,  H  = 1920, 1080   # landscape 16:9
WP, HP = 1080, 1620   # portrait  2:3

# All paths are relative to this script's folder, so the engine works wherever it lives.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("WC26_FONT_DIR", os.path.join(BASE_DIR, "fonts"))

def b64font(p):
    with open(os.path.join(FONT_DIR, p), "rb") as f:
        return base64.b64encode(f.read()).decode()

FONTS = {
    "anek": b64font("AnekBangla.ttf"),         # display Bengali
    "hind_b": b64font("HindSiliguri-Bold.ttf"),
    "hind_sb": b64font("HindSiliguri-SemiBold.ttf"),
    "hind_r": b64font("HindSiliguri-Regular.ttf"),
    "latin": b64font("BigShoulders-Bold.ttf"), # latin accents / VS
    "mono": None,
}

def _register_fonts_with_fontconfig():
    """Make the bundled TTFs visible to fontconfig so librsvg/rsvg-convert can
    shape Bengali. librsvg ignores @font-face data-URLs (unlike the Playwright
    fallback), so on hosts using rsvg-convert it relies on system fonts via
    fontconfig. Copies fonts/ into the user font dir and refreshes the cache.
    Best-effort and idempotent — safe to call on every import."""
    import shutil, glob
    dest = os.path.expanduser("~/.fonts")
    try:
        os.makedirs(dest, exist_ok=True)
        changed = False
        for f in glob.glob(os.path.join(FONT_DIR, "*.ttf")):
            target = os.path.join(dest, os.path.basename(f))
            if not os.path.exists(target):
                shutil.copy2(f, target); changed = True
        if changed and shutil.which("fc-cache"):
            subprocess.run(["fc-cache", "-f", dest], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

_register_fonts_with_fontconfig()

# ----------------------------------------------------------------------------
# FLAG LIBRARY — each returns SVG drawn inside a 0..100 x 0..66.67 (3:2) box,
# placed via a <g transform>. Kept simple/iconic so they read at thumbnail size.
# ----------------------------------------------------------------------------
def _stripes_h(colors):
    n=len(colors); h=66.667/n; out=""
    for i,c in enumerate(colors):
        out+=f'<rect x="0" y="{i*h:.3f}" width="100" height="{h:.3f}" fill="{c}"/>'
    return out
def _stripes_v(colors):
    n=len(colors); w=100/n; out=""
    for i,c in enumerate(colors):
        out+=f'<rect x="{i*w:.3f}" y="0" width="{w:.3f}" height="66.667" fill="{c}"/>'
    return out

def flag_mexico():
    return (_stripes_v(["#006847","#FFFFFF","#CE1126"]) +
            '<circle cx="50" cy="33.3" r="9" fill="#5d4225" opacity="0.85"/>'
            '<circle cx="50" cy="33.3" r="9" fill="none" stroke="#4a3315" stroke-width="0.8"/>')
def flag_south_africa():
    return (
        '<rect width="100" height="66.667" fill="#FFFFFF"/>'
        '<rect x="0" y="0" width="100" height="20" fill="#D80027"/>'
        '<rect x="0" y="22" width="100" height="22.7" fill="#007A4D"/>'
        '<rect x="0" y="46.7" width="100" height="20" fill="#003DA5"/>'
        '<path d="M0,0 L42,33.3 L0,66.667 Z" fill="#000000"/>'
        '<path d="M0,5.5 L37,33.3 L0,61.1 Z" fill="#FFB612"/>'
        '<path d="M0,11.5 L30,33.3 L0,55.1 Z" fill="#007A4D"/>'
    )
def flag_argentina():
    return (_stripes_h(["#74ACDF","#FFFFFF","#74ACDF"]) +
            '<circle cx="50" cy="33.3" r="6" fill="#F6B40E"/>'
            '<circle cx="50" cy="33.3" r="6" fill="none" stroke="#85340A" stroke-width="0.5"/>')
def flag_brazil():
    return ('<rect width="100" height="66.667" fill="#009C3B"/>'
            '<path d="M50,5 L92,33.3 L50,61.6 L8,33.3 Z" fill="#FFDF00"/>'
            '<circle cx="50" cy="33.3" r="13" fill="#002776"/>'
            '<path d="M37,30 Q50,26 63,32" stroke="#fff" stroke-width="2.4" fill="none"/>')
def flag_england():
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            '<rect x="42" y="0" width="16" height="66.667" fill="#CE1124"/>'
            '<rect x="0" y="25.3" width="100" height="16" fill="#CE1124"/>')
def flag_france():
    return _stripes_v(["#0055A4","#FFFFFF","#EF4135"])
def flag_spain():
    return ('<rect width="100" height="66.667" fill="#AA151B"/>'
            '<rect x="0" y="16.67" width="100" height="33.3" fill="#F1BF00"/>')
def flag_germany():
    return _stripes_h(["#000000","#DD0000","#FFCE00"])
def flag_portugal():
    return ('<rect width="100" height="66.667" fill="#FF0000"/>'
            '<rect x="0" y="0" width="40" height="66.667" fill="#006600"/>'
            '<circle cx="40" cy="33.3" r="9" fill="#FFD700"/>'
            '<circle cx="40" cy="33.3" r="9" fill="none" stroke="#fff" stroke-width="0.6"/>')
def flag_usa():
    out='<rect width="100" height="66.667" fill="#fff"/>'
    sh=66.667/13
    for i in range(13):
        if i%2==0: out+=f'<rect x="0" y="{i*sh:.2f}" width="100" height="{sh:.2f}" fill="#B22234"/>'
    out+='<rect x="0" y="0" width="40" height="35.9" fill="#3C3B6E"/>'
    return out
def flag_morocco():
    return ('<rect width="100" height="66.667" fill="#C1272D"/>'
            '<path d="M50,21 L53.4,31.5 L64.5,31.5 L55.5,38 L58.9,48.5 L50,42 L41.1,48.5 '
            'L44.5,38 L35.5,31.5 L46.6,31.5 Z" fill="none" stroke="#006233" stroke-width="2"/>')
def flag_generic(c1="#1a3a6b", c2="#c9a23a"):
    # fallback for TBD / playoff slots
    return (f'<rect width="100" height="66.667" fill="{c1}"/>'
            f'<path d="M0,66.667 L100,0 V66.667 Z" fill="{c2}" opacity="0.5"/>'
            '<circle cx="50" cy="33.3" r="8" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.7"/>')

def flag_south_korea():
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            '<circle cx="50" cy="33.3" r="13" fill="#CD2E3A"/>'
            '<path d="M37,33.3 A13,13 0 0,0 63,33.3 Z" fill="#003478"/>'
            '<rect x="16" y="13" width="14" height="2.5" fill="#000"/>'
            '<rect x="16" y="17.5" width="6" height="2.5" fill="#000"/>'
            '<rect x="24" y="17.5" width="6" height="2.5" fill="#000"/>'
            '<rect x="16" y="22" width="14" height="2.5" fill="#000"/>'
            '<rect x="70" y="42" width="14" height="2.5" fill="#000"/>'
            '<rect x="70" y="46.5" width="6" height="2.5" fill="#000"/>'
            '<rect x="78" y="46.5" width="6" height="2.5" fill="#000"/>'
            '<rect x="70" y="51" width="14" height="2.5" fill="#000"/>')

def flag_czechia():
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            '<rect x="0" y="33.3" width="100" height="33.3" fill="#D7141A"/>'
            '<path d="M0,0 L45,33.3 L0,66.667 Z" fill="#11457E"/>')

def flag_canada():
    return ('<rect width="100" height="66.667" fill="#FF0000"/>'
            '<rect x="25" y="0" width="50" height="66.667" fill="#FFFFFF"/>'
            '<path d="M50,14 L53,26 L65,26 L55,34 L59,46 L50,38 L41,46 L45,34 L35,26 L47,26 Z" fill="#FF0000"/>')

def flag_bosnia():
    return ('<rect width="100" height="66.667" fill="#003DA5"/>'
            '<path d="M25,0 L100,66.667 H100 V0 Z" fill="#FFCE00"/>'
            '<circle cx="16" cy="4" r="3" fill="#FFFFFF"/>'
            '<circle cx="23" cy="13" r="3" fill="#FFFFFF"/>'
            '<circle cx="30" cy="22" r="3" fill="#FFFFFF"/>'
            '<circle cx="37" cy="31" r="3" fill="#FFFFFF"/>'
            '<circle cx="44" cy="40" r="3" fill="#FFFFFF"/>'
            '<circle cx="51" cy="49" r="3" fill="#FFFFFF"/>'
            '<circle cx="58" cy="58" r="3" fill="#FFFFFF"/>')

def flag_qatar():
    return ('<rect width="100" height="66.667" fill="#8D1B3D"/>'
            '<path d="M0,0 H20 L32,6.7 L20,13.3 L32,20 L20,26.7 L32,33.3 L20,40 L32,46.7 L20,53.3 L32,60 L20,66.667 H0 Z" fill="#FFFFFF"/>')

def flag_switzerland():
    return ('<rect width="100" height="66.667" fill="#FF0000"/>'
            '<rect x="43" y="14" width="14" height="38.667" fill="#FFFFFF"/>'
            '<rect x="31" y="26" width="38" height="14" fill="#FFFFFF"/>')

def flag_haiti():
    return ('<rect width="100" height="33.3" fill="#003DA5"/>'
            '<rect y="33.3" width="100" height="33.3" fill="#D21034"/>'
            '<rect x="34" y="24" width="32" height="18.667" fill="#FFFFFF" opacity="0.9"/>')

def flag_scotland():
    return ('<rect width="100" height="66.667" fill="#003DA5"/>'
            '<line x1="0" y1="0" x2="100" y2="66.667" stroke="#FFFFFF" stroke-width="10"/>'
            '<line x1="100" y1="0" x2="0" y2="66.667" stroke="#FFFFFF" stroke-width="10"/>')

def flag_paraguay():
    return (_stripes_h(["#D52B1E","#FFFFFF","#009B3A"]) +
            '<circle cx="50" cy="33.3" r="7" fill="#FFDA00" opacity="0.9"/>')

def flag_australia():
    return ('<rect width="100" height="66.667" fill="#003DA5"/>'
            '<rect x="12" y="0" width="6" height="33.3" fill="#FFFFFF"/>'
            '<rect x="0" y="13.7" width="40" height="6" fill="#FFFFFF"/>'
            '<rect x="13" y="0" width="4" height="33.3" fill="#CC142B"/>'
            '<rect x="0" y="14.7" width="40" height="4" fill="#CC142B"/>'
            '<line x1="0" y1="0" x2="40" y2="33.3" stroke="#FFFFFF" stroke-width="5"/>'
            '<line x1="40" y1="0" x2="0" y2="33.3" stroke="#FFFFFF" stroke-width="5"/>'
            '<line x1="0" y1="0" x2="40" y2="33.3" stroke="#CC142B" stroke-width="3"/>'
            '<line x1="40" y1="0" x2="0" y2="33.3" stroke="#CC142B" stroke-width="3"/>'
            '<circle cx="68" cy="52" r="5" fill="#FFFFFF"/>'
            '<circle cx="80" cy="40" r="3.5" fill="#FFFFFF"/>'
            '<circle cx="78" cy="55" r="3" fill="#FFFFFF"/>'
            '<circle cx="62" cy="40" r="3" fill="#FFFFFF"/>')

def flag_turkey():
    return ('<rect width="100" height="66.667" fill="#E30A17"/>'
            '<circle cx="44" cy="33.3" r="13" fill="#FFFFFF"/>'
            '<circle cx="49" cy="33.3" r="10" fill="#E30A17"/>'
            '<path d="M58,27 L61.5,33.3 L58,39.6 L63,33.3 Z" fill="#FFFFFF"/>'
            '<path d="M57,29 L65,33.3 L57,37.6 Z" fill="#FFFFFF"/>')

def flag_curacao():
    return ('<rect width="100" height="66.667" fill="#002395"/>'
            '<rect x="0" y="40" width="100" height="9" fill="#F9E814"/>'
            '<circle cx="30" cy="22" r="4.5" fill="#FFFFFF"/>'
            '<circle cx="44" cy="16" r="4.5" fill="#FFFFFF"/>')

def flag_ivory_coast():
    return _stripes_v(["#F77F00","#FFFFFF","#009A44"])

def flag_ecuador():
    return ('<rect width="100" height="66.667" fill="#FFD100"/>'
            '<rect y="26.667" width="100" height="20" fill="#003DA5"/>'
            '<rect y="46.667" width="100" height="20" fill="#CC0001"/>'
            '<circle cx="50" cy="30" r="7" fill="#FFD100" stroke="#003DA5" stroke-width="1"/>')

def flag_netherlands():
    return _stripes_h(["#AE1C28","#FFFFFF","#21468B"])

def flag_japan():
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            '<circle cx="50" cy="33.3" r="15" fill="#BC002D"/>')

def flag_sweden():
    return ('<rect width="100" height="66.667" fill="#006AA7"/>'
            '<rect x="31" y="0" width="11" height="66.667" fill="#FECC02"/>'
            '<rect x="0" y="27.8" width="100" height="11" fill="#FECC02"/>')

def flag_tunisia():
    return ('<rect width="100" height="66.667" fill="#E70013"/>'
            '<circle cx="50" cy="33.3" r="16" fill="#FFFFFF"/>'
            '<circle cx="50" cy="33.3" r="13" fill="#E70013"/>'
            '<circle cx="46" cy="29" r="9" fill="#FFFFFF"/>'
            '<circle cx="51" cy="29" r="9" fill="#E70013"/>'
            '<path d="M55,26 L59,33.3 L55,40.6 L58.5,33.3 Z" fill="#FFFFFF"/>')

def flag_belgium():
    return _stripes_v(["#000000","#FAE042","#EF3340"])

def flag_egypt():
    return (_stripes_h(["#CE1126","#FFFFFF","#000000"]) +
            '<circle cx="50" cy="33.3" r="7" fill="#C09300" opacity="0.8"/>')

def flag_iran():
    return (_stripes_h(["#239F40","#FFFFFF","#DA0000"]) +
            '<rect x="43" y="30.3" width="14" height="6" fill="#DA0000" opacity="0.4"/>')

def flag_new_zealand():
    return ('<rect width="100" height="66.667" fill="#00247D"/>'
            '<rect x="12" y="0" width="6" height="33.3" fill="#FFFFFF"/>'
            '<rect x="0" y="13.7" width="40" height="6" fill="#FFFFFF"/>'
            '<rect x="13" y="0" width="4" height="33.3" fill="#CC142B"/>'
            '<rect x="0" y="14.7" width="40" height="4" fill="#CC142B"/>'
            '<line x1="0" y1="0" x2="40" y2="33.3" stroke="#FFFFFF" stroke-width="5"/>'
            '<line x1="40" y1="0" x2="0" y2="33.3" stroke="#FFFFFF" stroke-width="5"/>'
            '<line x1="0" y1="0" x2="40" y2="33.3" stroke="#CC142B" stroke-width="3"/>'
            '<line x1="40" y1="0" x2="0" y2="33.3" stroke="#CC142B" stroke-width="3"/>'
            '<circle cx="72" cy="14" r="4" fill="#CC142B" stroke="#FFFFFF" stroke-width="1.2"/>'
            '<circle cx="84" cy="28" r="4" fill="#CC142B" stroke="#FFFFFF" stroke-width="1.2"/>'
            '<circle cx="78" cy="44" r="3.5" fill="#CC142B" stroke="#FFFFFF" stroke-width="1.2"/>'
            '<circle cx="63" cy="38" r="3.5" fill="#CC142B" stroke="#FFFFFF" stroke-width="1.2"/>')

def flag_cabo_verde():
    stars = ''.join(f'<circle cx="{38+7*i}" cy="45" r="2.5" fill="#F7D116"/>' for i in range(10))
    return ('<rect width="100" height="66.667" fill="#003893"/>'
            '<rect y="40" width="100" height="7" fill="#FFFFFF"/>'
            '<rect y="47" width="100" height="5" fill="#CF111A"/>'
            '<rect y="52" width="100" height="7" fill="#FFFFFF"/>'
            + stars)

def flag_saudi_arabia():
    return ('<rect width="100" height="66.667" fill="#006C35"/>'
            '<rect x="14" y="26" width="72" height="3" fill="#FFFFFF"/>'
            '<rect x="14" y="31" width="72" height="3" fill="#FFFFFF"/>'
            '<rect x="14" y="36" width="72" height="3" fill="#FFFFFF"/>'
            '<path d="M35,39 L50,50 L65,39" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>'
            '<line x1="50" y1="50" x2="50" y2="56" stroke="#FFFFFF" stroke-width="2.5"/>')

def flag_uruguay():
    stripes = ''.join(f'<rect y="{7.4+i*14.8:.1f}" width="70" height="7.4" fill="#75AADB"/>' for i in range(4))
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            + stripes +
            '<circle cx="20" cy="33.3" r="10" fill="#FCD116"/>')

def flag_senegal():
    return (_stripes_v(["#00A859","#FCD116","#E31B23"]) +
            '<polygon points="50,24 51.8,29.5 57.6,29.5 52.9,32.8 54.7,38.3 50,35 45.3,38.3 47.1,32.8 42.4,29.5 48.2,29.5" fill="#00A859"/>')

def flag_iraq():
    return (_stripes_h(["#CE1126","#FFFFFF","#000000"]) +
            '<rect x="40" y="29.3" width="20" height="8" fill="#007A3D"/>')

def flag_norway():
    return ('<rect width="100" height="66.667" fill="#EF2B2D"/>'
            '<rect x="27" y="0" width="14" height="66.667" fill="#FFFFFF"/>'
            '<rect x="0" y="26.3" width="100" height="14" fill="#FFFFFF"/>'
            '<rect x="30" y="0" width="8" height="66.667" fill="#002868"/>'
            '<rect x="0" y="29.3" width="100" height="8" fill="#002868"/>')

def flag_algeria():
    return ('<rect width="100" height="66.667" fill="#FFFFFF"/>'
            '<rect x="50" y="0" width="50" height="66.667" fill="#006233"/>'
            '<circle cx="52" cy="29" r="11" fill="#FFFFFF"/>'
            '<circle cx="57" cy="29" r="11" fill="#006233"/>'
            '<path d="M54,19 L57,29 L54,39 L57.5,29 Z" fill="#D21034"/>'
            '<path d="M50,24 L63,29 L50,34 Z" fill="#D21034"/>')

def flag_austria():
    return _stripes_h(["#ED2939","#FFFFFF","#ED2939"])

def flag_jordan():
    return (_stripes_h(["#007A3D","#FFFFFF","#000000"]) +
            '<path d="M0,0 L40,33.3 L0,66.667 Z" fill="#CE1126"/>'
            '<circle cx="16" cy="33.3" r="4" fill="#FFFFFF"/>')

def flag_dr_congo():
    return ('<rect width="100" height="66.667" fill="#007FFF"/>'
            '<path d="M0,66.667 L100,0" stroke="#F7D116" stroke-width="9"/>'
            '<rect width="100" height="14" fill="#CE1126"/>'
            '<circle cx="15" cy="7" r="5.5" fill="#F7D116"/>')

def flag_uzbekistan():
    return ('<rect y="0" width="100" height="22.2" fill="#1EB53A"/>'
            '<rect y="22.2" width="100" height="4" fill="#FFFFFF"/>'
            '<rect y="26.2" width="100" height="22.2" fill="#FFFFFF"/>'
            '<rect y="48.4" width="100" height="4" fill="#FFFFFF"/>'
            '<rect y="52.4" width="100" height="14.3" fill="#CE1126"/>'
            '<circle cx="13" cy="11" r="7" fill="#FFFFFF"/>'
            '<circle cx="17.5" cy="11" r="7" fill="#1EB53A"/>')

def flag_colombia():
    return ('<rect width="100" height="33.3" fill="#FCD116"/>'
            '<rect y="33.3" width="100" height="16.7" fill="#003087"/>'
            '<rect y="50" width="100" height="16.7" fill="#CE1126"/>')

def flag_croatia():
    checks = ''.join(
        f'<rect x="{36+7*j}" y="{21+6*i}" width="7" height="6" fill="{"#FF0000" if (i+j)%2==0 else "#FFFFFF"}"/>'
        for i in range(4) for j in range(4))
    return (_stripes_h(["#FF0000","#FFFFFF","#171796"]) +
            '<rect x="36" y="21" width="28" height="24" fill="#FFFFFF"/>'
            + checks)

def flag_ghana():
    return (_stripes_h(["#EF3340","#FCD116","#006B3F"]) +
            '<polygon points="50,27 51.7,32 57,32 52.8,35 54.5,40 50,37 45.5,40 47.2,35 43,32 48.3,32" fill="#000000"/>')

def flag_panama():
    return ('<rect width="50" height="33.3" fill="#FFFFFF"/>'
            '<rect x="50" y="0" width="50" height="33.3" fill="#D21034"/>'
            '<rect y="33.3" width="50" height="33.3" fill="#005DAA"/>'
            '<rect x="50" y="33.3" width="50" height="33.3" fill="#FFFFFF"/>'
            '<polygon points="25,14 26.7,19.5 32.5,19.5 27.8,22.7 29.5,28.2 25,25 20.5,28.2 22.2,22.7 17.5,19.5 23.3,19.5" fill="#005DAA"/>'
            '<polygon points="75,38 76.7,43.5 82.5,43.5 77.8,46.7 79.5,52.2 75,49 70.5,52.2 72.2,46.7 67.5,43.5 73.3,43.5" fill="#D21034"/>')

FLAGS = {
    "MEX": flag_mexico,      "RSA": flag_south_africa, "ARG": flag_argentina,
    "BRA": flag_brazil,      "ENG": flag_england,       "FRA": flag_france,
    "ESP": flag_spain,       "GER": flag_germany,       "POR": flag_portugal,
    "USA": flag_usa,         "MAR": flag_morocco,
    "KOR": flag_south_korea, "CZE": flag_czechia,
    "CAN": flag_canada,      "BIH": flag_bosnia,        "QAT": flag_qatar,   "SUI": flag_switzerland,
    "HAI": flag_haiti,       "SCO": flag_scotland,
    "PAR": flag_paraguay,    "AUS": flag_australia,     "TUR": flag_turkey,
    "CUW": flag_curacao,     "CIV": flag_ivory_coast,   "ECU": flag_ecuador,
    "NED": flag_netherlands, "JPN": flag_japan,         "SWE": flag_sweden,  "TUN": flag_tunisia,
    "BEL": flag_belgium,     "EGY": flag_egypt,         "IRN": flag_iran,    "NZL": flag_new_zealand,
    "CPV": flag_cabo_verde,  "KSA": flag_saudi_arabia,  "URU": flag_uruguay,
    "SEN": flag_senegal,     "IRQ": flag_iraq,           "NOR": flag_norway,
    "ALG": flag_algeria,     "AUT": flag_austria,        "JOR": flag_jordan,
    "COD": flag_dr_congo,    "UZB": flag_uzbekistan,    "COL": flag_colombia,
    "CRO": flag_croatia,     "GHA": flag_ghana,          "PAN": flag_panama,
    "TBD": flag_generic,
}
# team accent colors (used for the side glow)
ACCENT = {
    "MEX":"#0a7d4a","RSA":"#ffb81c","ARG":"#74acdf","BRA":"#ffdf00","ENG":"#ce1124",
    "FRA":"#3b6fb6","ESP":"#f1bf00","GER":"#dd0000","POR":"#1f8a3b","USA":"#3c5fa8",
    "MAR":"#c1272d",
    "KOR":"#cd2e3a","CZE":"#d7141a","CAN":"#ff0000","BIH":"#ffce00","QAT":"#8d1b3d",
    "SUI":"#ff0000","HAI":"#003da5","SCO":"#003da5","PAR":"#d52b1e","AUS":"#003da5",
    "TUR":"#e30a17","CUW":"#002395","CIV":"#f77f00","ECU":"#ffd100","NED":"#ae1c28",
    "JPN":"#bc002d","SWE":"#006aa7","TUN":"#e70013","BEL":"#ef3340","EGY":"#ce1126",
    "IRN":"#239f40","NZL":"#00247d","CPV":"#003893","KSA":"#006c35","URU":"#75aadb",
    "SEN":"#00a859","IRQ":"#ce1126","NOR":"#ef2b2d","ALG":"#006233","AUT":"#ed2939",
    "JOR":"#007a3d","COD":"#007fff","UZB":"#1eb53a","COL":"#fcd116","CRO":"#ff0000",
    "GHA":"#006b3f","PAN":"#d21034","TBD":"#5b6b86",
}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

from PIL import ImageFont
_FIT_CACHE = {}
def _name_font(px):
    px = int(px)
    if px not in _FIT_CACHE:
        _FIT_CACHE[px] = ImageFont.truetype(os.path.join(FONT_DIR, "AnekBangla.ttf"), px)
    return _FIT_CACHE[px]

def fit_size(text, base, max_w):
    """Width-aware shrink so long Bengali names stay inside their slot.
    Measures the real advance width with the actual display font instead of
    guessing from character count (Bengali conjuncts/matras make len() overcount).
    Width scales ~linearly with px, so a single measurement gives an accurate fit."""
    w = _name_font(base).getlength(text)
    if w <= max_w:
        return base
    # Absolute legibility floor (px) rather than a ratio of base: a 0.45*base
    # floor still overflowed long real names like "বসনিয়া ও হার্জেগোভিনা".
    return max(base * max_w / w, 44)

def build_svg(m, bg_b64=None, font_cfg=None):
    fc = font_cfg or {}
    a_code, b_code = m["a_code"], m["b_code"]
    a_name, b_name = m["a_name"], m["b_name"]
    a_acc = ACCENT.get(a_code,"#888"); b_acc = ACCENT.get(b_code,"#888")
    mode = m.get("mode","fixture")  # 'fixture' or 'highlights'
    line1 = m.get("line1","")       # date  (fixture) or empty
    line2 = m.get("line2","")       # time
    venue = m.get("venue","")       # NOT drawn on image (kept for metadata only)
    stage = m.get("stage","")
    tag   = m.get("tag", "হাইলাইটস" if mode=="highlights" else "")

    slot_w = 658; base = fc.get("name_base", 163)
    name_sz = min(fit_size(a_name, base, slot_w), fit_size(b_name, base, slot_w))

    flag_a = FLAGS.get(a_code, flag_generic)()
    flag_b = FLAGS.get(b_code, flag_generic)()

    cx = W/2
    flag_w = 658; flag_h = 438
    ax = 155; bx = 1107
    flag_y = 343
    sclf = flag_w/100.0
    name_ax = ax + flag_w/2
    name_bx = bx + flag_w/2

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
<style>
@font-face{{font-family:'Anek';src:url(data:font/ttf;base64,{FONTS["anek"]}) format('truetype');}}
@font-face{{font-family:'HindB';src:url(data:font/ttf;base64,{FONTS["hind_b"]}) format('truetype');}}
@font-face{{font-family:'HindSB';src:url(data:font/ttf;base64,{FONTS["hind_sb"]}) format('truetype');}}
@font-face{{font-family:'HindR';src:url(data:font/ttf;base64,{FONTS["hind_r"]}) format('truetype');}}
@font-face{{font-family:'Latin';src:url(data:font/ttf;base64,{FONTS["latin"]}) format('truetype');}}
text{{-webkit-font-smoothing:antialiased;}}
</style>

<linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#10141c"/>
  <stop offset="55%" stop-color="#0a0d13"/>
  <stop offset="100%" stop-color="#05070b"/>
</linearGradient>
<radialGradient id="glowA" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{a_acc}" stop-opacity="0.35"/>
  <stop offset="100%" stop-color="{a_acc}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowB" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{b_acc}" stop-opacity="0.35"/>
  <stop offset="100%" stop-color="{b_acc}" stop-opacity="0"/>
</radialGradient>
<clipPath id="flagClipA"><rect x="{ax}" y="{flag_y}" width="{flag_w}" height="{flag_h}" rx="13"/></clipPath>
<clipPath id="flagClipB"><rect x="{bx}" y="{flag_y}" width="{flag_w}" height="{flag_h}" rx="13"/></clipPath>
<filter id="soft"><feGaussianBlur stdDeviation="1.1"/></filter>
<linearGradient id="scrimTop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#05070b" stop-opacity="0.92"/>
  <stop offset="100%" stop-color="#05070b" stop-opacity="0"/>
</linearGradient>
<linearGradient id="scrimBot" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0%" stop-color="#05070b" stop-opacity="0.95"/>
  <stop offset="100%" stop-color="#05070b" stop-opacity="0"/>
</linearGradient>
<radialGradient id="vign" cx="50%" cy="46%" r="75%">
  <stop offset="55%" stop-color="#05070b" stop-opacity="0"/>
  <stop offset="100%" stop-color="#05070b" stop-opacity="0.7"/>
</radialGradient>
</defs>

<!-- BASE -->
<rect width="{W}" height="{H}" fill="url(#base)"/>
'''
    if bg_b64:
        # Real venue photo (or procedural stadium) fills the frame, slightly darkened.
        svg += f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" '
        svg += f'href="data:image/png;base64,{bg_b64}" opacity="1.0"/>'
        svg += f'<rect width="{W}" height="{H}" fill="#05070b" opacity="0.25"/>'
        svg += f'<rect x="0" y="0" width="{W}" height="240" fill="url(#scrimTop)"/>'
        svg += f'<rect x="0" y="{H-260}" width="{W}" height="260" fill="url(#scrimBot)"/>'
        svg += f'<rect width="{W}" height="{H}" fill="url(#vign)"/>'
    else:
        # ---- procedural fallback stadium (vector arcs) ----
        svg += '<g opacity="0.5" stroke-linecap="round" fill="none">'
        for i in range(11):
            rx = 560 + i*120; ry = 150 + i*44
            op = 0.16 - i*0.011
            svg += f'<ellipse cx="{cx}" cy="-40" rx="{rx}" ry="{ry}" stroke="#3a4a66" stroke-width="2" opacity="{max(op,0.02):.3f}"/>'
        svg += '</g>'
        for px,py in [(150,70),(1770,70),(480,40),(1440,40)]:
            svg += f'<g opacity="0.6">'
            for dx in (-14,0,14):
                for dy in (-8,6):
                    svg += f'<circle cx="{px+dx}" cy="{py+dy}" r="2.4" fill="#cfe0ff" opacity="0.7"/>'
            svg += '</g>'

    svg += f'''
'''

    # --- DATE/TIME PILL ---
    pill_w = 1068; pill_h = 153; pill_rx = 58
    pill_x = cx - pill_w/2; pill_y_top = 0
    line1_disp = line1.replace(" ২০২৬", "").replace("২০২৬ ", "").replace("২০২৬", "")
    if mode == "highlights":
        pill_text = esc(tag) if tag else "হাইলাইটস"
    else:
        pill_text = esc(f"{line1_disp}, {line2}") if (line1_disp and line2) else esc(line1_disp or line2 or tag)
    px = int(pill_x)
    pill_path = f"M{px},0 H{px+pill_w} V{pill_h-pill_rx} Q{px+pill_w},{pill_h} {px+pill_w-pill_rx},{pill_h} H{px+pill_rx} Q{px},{pill_h} {px},{pill_h-pill_rx} Z"
    dt_fs = fc.get("datetime_fs", 80)
    svg += f'<path d="{pill_path}" fill="#672BE6"/>'
    svg += f'<text x="{cx:.0f}" y="{pill_y_top + int(dt_fs*1.2)}" text-anchor="middle" font-family="HindB, Hind Siliguri, Noto Sans Bengali, sans-serif" font-size="{dt_fs}" fill="#ffffff">{pill_text}</text>'

    # --- FLAGS ---
    for fx, flag, clip_id, glow_id in [
        (ax, flag_a, "flagClipA", "glowA"),
        (bx, flag_b, "flagClipB", "glowB"),
    ]:
        glow_pad = 80
        svg += f'<ellipse cx="{fx+flag_w/2:.0f}" cy="{flag_y+flag_h/2:.0f}" rx="{flag_w/2+glow_pad}" ry="{flag_h/2+glow_pad}" fill="url(#{glow_id})"/>'
        svg += f'<rect x="{fx-8:.0f}" y="{flag_y-8}" width="{flag_w+16}" height="{flag_h+16}" rx="18" fill="#0b0e14" stroke="#1e2a38" stroke-width="2"/>'
        svg += f'<g clip-path="url(#{clip_id})"><g transform="translate({fx:.0f},{flag_y}) scale({sclf})">{flag}</g></g>'
        svg += f'<rect x="{fx:.0f}" y="{flag_y}" width="{flag_w}" height="{flag_h}" rx="13" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.25"/>'
        svg += f'<rect x="{fx:.0f}" y="{flag_y}" width="{flag_w}" height="{flag_h*0.35:.0f}" rx="13" fill="#ffffff" opacity="0.06"/>'

    # --- VS ---
    vy = flag_y + flag_h/2
    svg += f'<circle cx="{cx:.0f}" cy="{vy:.0f}" r="54" fill="#111827" stroke="#ffffff" stroke-width="1.5" opacity="1"/>'
    svg += f'<text x="{cx:.0f}" y="{vy+19:.0f}" text-anchor="middle" font-family="Latin, Big Shoulders Display, sans-serif" font-size="52" fill="#ffffff" letter-spacing="1">VS</text>'

    # --- TEAM NAMES ---
    name_y = flag_y + flag_h + 50 + int(name_sz * 0.80)
    svg += f'<text x="{name_ax:.0f}" y="{name_y}" text-anchor="middle" font-family="Anek, Anek Bangla, Noto Sans Bengali, sans-serif" font-weight="800" font-size="{name_sz:.0f}" fill="#ffffff">{esc(a_name)}</text>'
    svg += f'<text x="{name_bx:.0f}" y="{name_y}" text-anchor="middle" font-family="Anek, Anek Bangla, Noto Sans Bengali, sans-serif" font-weight="800" font-size="{name_sz:.0f}" fill="#ffffff">{esc(b_name)}</text>'

    svg += '</svg>'
    return svg

VENUE_DIR = os.environ.get("WC26_VENUE_DIR", os.path.join(BASE_DIR, "venues"))   # real stadium photos
FALLBACK_BG = os.path.join(BASE_DIR, "stadium_bg.png")                            # procedural backdrop

def _load_bg_b64(m):
    """Return base64 PNG for the background.
    Priority: m['bg'] explicit path  ->  venues/<venue_img>.png  ->  procedural fallback."""
    candidates = []
    if m.get("bg"):
        candidates.append(m["bg"])
    if m.get("venue_img"):
        candidates.append(os.path.join(VENUE_DIR, m["venue_img"]))
    candidates.append(FALLBACK_BG)
    for p in candidates:
        if p and os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def _chromium_path():
    """System Chromium binary if installed (Streamlit Cloud installs it via the
    `chromium` apt package). Returns None locally, where Playwright's own bundled
    browser is used instead."""
    for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"):
        if os.path.exists(p):
            return p
    return None

def _render_with_playwright(svg_path, out_png, w=W, h=H):
    from playwright.sync_api import sync_playwright
    svg_abs = os.path.abspath(svg_path)
    html = f'<!doctype html><html><body style="margin:0;padding:0;background:#000"><img src="file://{svg_abs}" width="{w}" height="{h}" style="display:block"/></body></html>'
    html_path = svg_path.replace(".svg", "_pw.html")
    with open(html_path, "w", encoding="utf-8") as f: f.write(html)
    exe = _chromium_path()
    launch_kw = {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
    if exe:
        launch_kw["executable_path"] = exe
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**launch_kw)
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(f"file://{os.path.abspath(html_path)}")
            page.wait_for_timeout(200)
            page.screenshot(path=out_png, full_page=False)
            browser.close()
    finally:
        if os.path.exists(html_path): os.remove(html_path)

def render(m, out_png, font_cfg=None):
    bg_b64 = _load_bg_b64(m)
    svg = build_svg(m, bg_b64=bg_b64, font_cfg=font_cfg)
    svg_path = out_png.replace(".png",".svg")
    with open(svg_path,"w", encoding="utf-8") as f: f.write(svg)
    # WC26_RENDERER=playwright forces Chromium (honors @font-face → exact fonts).
    # Otherwise try rsvg-convert first, fall back to Playwright/Chromium.
    if os.environ.get("WC26_RENDERER") == "playwright":
        try:
            _render_with_playwright(svg_path, out_png)
        except Exception:
            subprocess.run(["rsvg-convert","-w",str(W),"-h",str(H),svg_path,"-o",out_png], check=False)
    else:
        try:
            subprocess.run(["rsvg-convert","-w",str(W),"-h",str(H),svg_path,"-o",out_png], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            _render_with_playwright(svg_path, out_png)
    if os.path.exists(svg_path):
        os.remove(svg_path)
    return out_png

# ---------------------------------------------------------------------------
# PORTRAIT (2:3 — 1080×1620) — same aesthetic, teams stacked vertically
# ---------------------------------------------------------------------------
def build_svg_portrait(m, bg_b64=None, font_cfg=None):
    fc = font_cfg or {}
    a_code, b_code = m["a_code"], m["b_code"]
    a_name, b_name = m["a_name"], m["b_name"]
    a_acc = ACCENT.get(a_code, "#888"); b_acc = ACCENT.get(b_code, "#888")
    mode  = m.get("mode", "fixture")
    line1 = m.get("line1", ""); line2 = m.get("line2", "")
    stage = m.get("stage", "")
    tag   = m.get("tag", "হাইলাইটস" if mode == "highlights" else "")

    slot_w = 500; base = fc.get("name_base", 163)
    name_sz = min(fit_size(a_name, base, slot_w), fit_size(b_name, base, slot_w))

    flag_a = FLAGS.get(a_code, flag_generic)()
    flag_b = FLAGS.get(b_code, flag_generic)()

    cx = WP / 2                        # 540
    flag_w = 540; flag_h = int(flag_w * 2 / 3)  # 540×360
    sclf   = flag_w / 100.0
    flag_x = int(cx - flag_w / 2)     # 270

    cy_vs    = HP / 2                  # 810
    flag_y_a = 195
    name_y_a = 685
    rule_y_a  = 731
    name_y_b  = 1002
    rule_y_b  = 1048
    flag_y_b  = 1098

    svg = f'''<svg width="{WP}" height="{HP}" viewBox="0 0 {WP} {HP}" xmlns="http://www.w3.org/2000/svg">
<defs>
<style>
@font-face{{font-family:'Anek';src:url(data:font/ttf;base64,{FONTS["anek"]}) format('truetype');}}
@font-face{{font-family:'HindB';src:url(data:font/ttf;base64,{FONTS["hind_b"]}) format('truetype');}}
@font-face{{font-family:'HindSB';src:url(data:font/ttf;base64,{FONTS["hind_sb"]}) format('truetype');}}
@font-face{{font-family:'HindR';src:url(data:font/ttf;base64,{FONTS["hind_r"]}) format('truetype');}}
@font-face{{font-family:'Latin';src:url(data:font/ttf;base64,{FONTS["latin"]}) format('truetype');}}
text{{-webkit-font-smoothing:antialiased;}}
</style>
<linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#10141c"/>
  <stop offset="55%" stop-color="#0a0d13"/>
  <stop offset="100%" stop-color="#05070b"/>
</linearGradient>
<clipPath id="flagClipA"><rect x="{flag_x}" y="{flag_y_a}" width="{flag_w}" height="{flag_h}" rx="13"/></clipPath>
<clipPath id="flagClipB"><rect x="{flag_x}" y="{flag_y_b}" width="{flag_w}" height="{flag_h}" rx="13"/></clipPath>
<filter id="soft"><feGaussianBlur stdDeviation="1.1"/></filter>
<linearGradient id="scrimTop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#05070b" stop-opacity="0.92"/>
  <stop offset="100%" stop-color="#05070b" stop-opacity="0"/>
</linearGradient>
<linearGradient id="scrimBot" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0%" stop-color="#05070b" stop-opacity="0.95"/>
  <stop offset="100%" stop-color="#05070b" stop-opacity="0"/>
</linearGradient>
</defs>

<rect width="{WP}" height="{HP}" fill="url(#base)"/>
'''
    if bg_b64:
        svg += f'<image x="0" y="0" width="{WP}" height="{HP}" preserveAspectRatio="xMidYMid slice" href="data:image/png;base64,{bg_b64}" opacity="0.9"/>'
        svg += f'<rect width="{WP}" height="{HP}" fill="#05070b" opacity="0.25"/>'
        svg += f'<rect x="0" y="0" width="{WP}" height="300" fill="url(#scrimTop)"/>'
        svg += f'<rect x="0" y="{HP-300}" width="{WP}" height="300" fill="url(#scrimBot)"/>'
    else:
        svg += '<g opacity="0.45" stroke-linecap="round" fill="none">'
        for i in range(11):
            rx = 340 + i*70; ry = 90 + i*25
            op = 0.16 - i*0.011
            svg += f'<ellipse cx="{cx}" cy="-40" rx="{rx}" ry="{ry}" stroke="#3a4a66" stroke-width="2" opacity="{max(op,0.02):.3f}"/>'
        svg += '</g>'

    svg += f'''
'''

    # --- DATE/TIME PILL ---
    dt_fs_val = fc.get("datetime_fs", 65)
    pill_w = 900; pill_h = int(dt_fs_val * 1.75); pill_rx = int(pill_h * 0.38)
    pill_x = cx - pill_w/2; pill_y_top = 0
    line1_disp = line1.replace(" ২০২৬", "").replace("২০২৬ ", "").replace("২০২৬", "")
    if mode == "highlights":
        pill_text = esc(tag) if tag else "হাইলাইটস"
    else:
        pill_text = esc(f"{line1_disp}, {line2}") if (line1_disp and line2) else esc(line1_disp or line2 or tag)
    ppx = int(pill_x)
    pill_path = f"M{ppx},0 H{ppx+pill_w} V{pill_h-pill_rx} Q{ppx+pill_w},{pill_h} {ppx+pill_w-pill_rx},{pill_h} H{ppx+pill_rx} Q{ppx},{pill_h} {ppx},{pill_h-pill_rx} Z"
    svg += f'<path d="{pill_path}" fill="#672BE6"/>'
    svg += f'<text x="{cx:.0f}" y="{pill_y_top + int(dt_fs_val*1.2)}" text-anchor="middle" font-family="HindB, Hind Siliguri, Noto Sans Bengali, sans-serif" font-size="{dt_fs_val}" fill="#ffffff">{pill_text}</text>'

    # --- FLAG A (top) ---
    svg += f'<rect x="{flag_x-8}" y="{flag_y_a-8}" width="{flag_w+16}" height="{flag_h+16}" rx="18" fill="#0b0e14" stroke="#1e2a38" stroke-width="2"/>'
    svg += f'<g clip-path="url(#flagClipA)"><g transform="translate({flag_x},{flag_y_a}) scale({sclf})">{flag_a}</g></g>'
    svg += f'<rect x="{flag_x}" y="{flag_y_a}" width="{flag_w}" height="{flag_h}" rx="13" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.25"/>'
    svg += f'<rect x="{flag_x}" y="{flag_y_a}" width="{flag_w}" height="{flag_h*0.35:.0f}" rx="13" fill="#ffffff" opacity="0.06"/>'
    svg += f'<text x="{cx:.0f}" y="{flag_y_a + flag_h + 50 + int(name_sz * 0.80)}" text-anchor="middle" font-family="Anek, Anek Bangla, Noto Sans Bengali, sans-serif" font-weight="800" font-size="{name_sz:.0f}" fill="#ffffff">{esc(a_name)}</text>'
    svg += f'<line x1="{cx-120}" y1="{rule_y_a}" x2="{cx+120}" y2="{rule_y_a}" stroke="#ffffff" stroke-width="1" opacity="0.2"/>'

    # --- VS ---
    svg += f'<circle cx="{cx:.0f}" cy="{cy_vs:.0f}" r="58" fill="#111827" stroke="#ffffff" stroke-width="1.5" opacity="1"/>'
    svg += f'<text x="{cx:.0f}" y="{cy_vs+21:.0f}" text-anchor="middle" font-family="Latin, Big Shoulders Display, sans-serif" font-size="58" fill="#ffffff" letter-spacing="1">VS</text>'

    # --- FLAG B (bottom) ---
    svg += f'<rect x="{flag_x-8}" y="{flag_y_b-8}" width="{flag_w+16}" height="{flag_h+16}" rx="18" fill="#0b0e14" stroke="#1e2a38" stroke-width="2"/>'
    svg += f'<g clip-path="url(#flagClipB)"><g transform="translate({flag_x},{flag_y_b}) scale({sclf})">{flag_b}</g></g>'
    svg += f'<rect x="{flag_x}" y="{flag_y_b}" width="{flag_w}" height="{flag_h}" rx="13" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.25"/>'
    svg += f'<rect x="{flag_x}" y="{flag_y_b}" width="{flag_w}" height="{flag_h*0.35:.0f}" rx="13" fill="#ffffff" opacity="0.06"/>'
    svg += f'<text x="{cx:.0f}" y="{name_y_b}" text-anchor="middle" font-family="Anek, Anek Bangla, Noto Sans Bengali, sans-serif" font-weight="800" font-size="{name_sz:.0f}" fill="#ffffff">{esc(b_name)}</text>'
    svg += f'<line x1="{cx-120}" y1="{rule_y_b}" x2="{cx+120}" y2="{rule_y_b}" stroke="#ffffff" stroke-width="1" opacity="0.2"/>'

    svg += '</svg>'
    return svg

def render_portrait(m, out_png, font_cfg=None):
    bg_b64  = _load_bg_b64(m)
    svg     = build_svg_portrait(m, bg_b64=bg_b64, font_cfg=font_cfg)
    svg_path = out_png.replace(".png", ".svg")
    with open(svg_path, "w", encoding="utf-8") as f: f.write(svg)
    if os.environ.get("WC26_RENDERER") == "playwright":
        try:
            _render_with_playwright(svg_path, out_png, w=WP, h=HP)
        except Exception:
            subprocess.run(["rsvg-convert", "-w", str(WP), "-h", str(HP), svg_path, "-o", out_png], check=False)
    else:
        try:
            subprocess.run(["rsvg-convert", "-w", str(WP), "-h", str(HP), svg_path, "-o", out_png], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            _render_with_playwright(svg_path, out_png, w=WP, h=HP)
    if os.path.exists(svg_path):
        os.remove(svg_path)
    return out_png

# ---------------------------------------------------------------------------
# EXAMPLE: opening match (also a 2nd demo with a very long name to prove template)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    opening = {
        "a_code":"MEX","a_name":"মেক্সিকো",
        "b_code":"RSA","b_name":"দক্ষিণ আফ্রিকা",
        "mode":"fixture",
        "stage":"গ্রুপ এ — উদ্বোধনী ম্যাচ",
        "line1":"১১ জুন ২০২৬",
        "line2":"রাত ১২ঃ৩০",
        "venue":"আজতেকা স্টেডিয়াম",
    }
    render(opening, os.path.join(BASE_DIR,"banner_opening.png"))
    print("opening done")

    # Highlights variant of the same match (same template)
    hl = dict(opening); hl["mode"]="highlights"; hl["stage"]="গ্রুপ এ"; hl["tag"]="ম্যাচ হাইলাইটস"
    render(hl, os.path.join(BASE_DIR,"banner_highlights.png"))
    print("highlights done")

    # Long-name stress test (proves the shared slot holds)
    longname = {
        "a_code":"USA","a_name":"যুক্তরাষ্ট্র",
        "b_code":"TBD","b_name":"বসনিয়া ও হার্জেগোভিনা",
        "mode":"fixture","stage":"গ্রুপ ডি",
        "line1":"১৮ জুন ২০২৬","line2":"ভোর ৫ঃ০০","venue":"সোফাই স্টেডিয়াম",
    }
    render(longname, os.path.join(BASE_DIR,"banner_longname.png"))
    print("longname done")
