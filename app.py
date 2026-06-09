#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streamlit preview & batch UI for the WC26 Banner Engine."""
import os, json, tempfile, io, zipfile
# Render with Chromium so @font-face fonts match local/dev output exactly
# (librsvg ignores embedded @font-face). Must be set before importing the engine.
os.environ.setdefault("WC26_RENDERER", "playwright")
import streamlit as st
from wc26_template import render, render_portrait

st.set_page_config(page_title="WC26 Banner Engine", layout="wide")

FIXTURES_PATH  = "fixtures.json"
FONT_CFG_PATH  = "font_config.json"
FONT_DEFAULTS  = {"ls_dt": 80, "ls_nm": 163, "pt_dt": 65, "pt_nm": 163}

def _load_font_cfg():
    if os.path.exists(FONT_CFG_PATH):
        try:
            with open(FONT_CFG_PATH) as f:
                return {**FONT_DEFAULTS, **json.load(f)}
        except Exception:
            pass
    return dict(FONT_DEFAULTS)

def _save_font_cfg(cfg):
    with open(FONT_CFG_PATH, "w") as f:
        json.dump(cfg, f)

# initialise session_state from persisted file once per session
if "font_cfg" not in st.session_state:
    st.session_state.font_cfg = _load_font_cfg()

# Stadium info keyed by match index (1-based) — sourced from official schedule
VENUE_INFO = {
    1:  {"stadium": "Estadio Azteca",            "city": "Mexico City",      "country": "Mexico"},
    2:  {"stadium": "Estadio Akron",             "city": "Guadalajara",      "country": "Mexico"},
    3:  {"stadium": "Estadio BBVA",              "city": "Monterrey",        "country": "Mexico"},
    4:  {"stadium": "Estadio Azteca",            "city": "Mexico City",      "country": "Mexico"},
    5:  {"stadium": "Estadio Akron",             "city": "Guadalajara",      "country": "Mexico"},
    6:  {"stadium": "Estadio BBVA",              "city": "Monterrey",        "country": "Mexico"},
    7:  {"stadium": "BMO Field",                 "city": "Toronto",          "country": "Canada"},
    8:  {"stadium": "BC Place",                  "city": "Vancouver",        "country": "Canada"},
    9:  {"stadium": "BC Place",                  "city": "Vancouver",        "country": "Canada"},
    10: {"stadium": "BMO Field",                 "city": "Toronto",          "country": "Canada"},
    11: {"stadium": "BC Place",                  "city": "Vancouver",        "country": "Canada"},
    12: {"stadium": "BMO Field",                 "city": "Toronto",          "country": "Canada"},
    13: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    14: {"stadium": "Gillette Stadium",          "city": "Foxborough",       "country": "USA"},
    15: {"stadium": "Gillette Stadium",          "city": "Foxborough",       "country": "USA"},
    16: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    17: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    18: {"stadium": "Gillette Stadium",          "city": "Foxborough",       "country": "USA"},
    19: {"stadium": "SoFi Stadium",              "city": "Inglewood",        "country": "USA"},
    20: {"stadium": "SoFi Stadium",              "city": "Inglewood",        "country": "USA"},
    21: {"stadium": "SoFi Stadium",              "city": "Inglewood",        "country": "USA"},
    22: {"stadium": "Rose Bowl Stadium",         "city": "Pasadena",         "country": "USA"},
    23: {"stadium": "Rose Bowl Stadium",         "city": "Pasadena",         "country": "USA"},
    24: {"stadium": "SoFi Stadium",              "city": "Inglewood",        "country": "USA"},
    25: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    26: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    27: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    28: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    29: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    30: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    31: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    32: {"stadium": "Arrowhead Stadium",         "city": "Kansas City",      "country": "USA"},
    33: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    34: {"stadium": "Arrowhead Stadium",         "city": "Kansas City",      "country": "USA"},
    35: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    36: {"stadium": "Arrowhead Stadium",         "city": "Kansas City",      "country": "USA"},
    37: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    38: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    39: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    40: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    41: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    42: {"stadium": "Lumen Field",               "city": "Seattle",          "country": "USA"},
    43: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    44: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    45: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    46: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    47: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    48: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    49: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    50: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    51: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    52: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    53: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    54: {"stadium": "MetLife Stadium",           "city": "East Rutherford",  "country": "USA"},
    55: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    56: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
    57: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    58: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
    59: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
    60: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    61: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    62: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    63: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    64: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    65: {"stadium": "Mercedes-Benz Stadium",     "city": "Atlanta",          "country": "USA"},
    66: {"stadium": "Lincoln Financial Field",   "city": "Philadelphia",     "country": "USA"},
    67: {"stadium": "AT&T Stadium",              "city": "Arlington",        "country": "USA"},
    68: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
    69: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
    70: {"stadium": "BMO Field",                 "city": "Toronto",          "country": "Canada"},
    71: {"stadium": "BMO Field",                 "city": "Toronto",          "country": "Canada"},
    72: {"stadium": "NRG Stadium",               "city": "Houston",          "country": "USA"},
}

# ---------------------------------------------------------------------------
# Load fixtures
# ---------------------------------------------------------------------------
@st.cache_data
def load_fixtures(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

st.title("FIFA World Cup 2026 — Banner Engine")

if not os.path.exists(FIXTURES_PATH):
    st.error(f"`{FIXTURES_PATH}` not found. Run from the project root.")
    st.stop()

fixtures = load_fixtures(FIXTURES_PATH)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader("⚽ Match Selector")

    options = [
        f"Match {i} — {m['a_code']} vs {m['b_code']}  |  {m.get('stage','')}"
        for i, m in enumerate(fixtures, 1)
    ]
    selected_idx = st.selectbox("Choose a match", range(len(options)), format_func=lambda i: options[i])
    match = fixtures[selected_idx]
    match_no = selected_idx + 1

    # ---- Match Info (accordion) ----
    venue = VENUE_INFO.get(match_no, {})
    with st.expander("📋 Match Info", expanded=True):
        st.markdown(f"""
| | |
|---|---|
| **Group** | {match.get('stage', '—')} |
| **Date** | {match.get('line1', '—')} |
| **Time (BST)** | {match.get('line2', '—')} |
| **Stadium** | {venue.get('stadium', '—')} |
| **City** | {venue.get('city', '—')}, {venue.get('country', '')} |
""")

    # ---- Font Sizes (collapsed) ----
    with st.expander("⚙ Font Sizes", expanded=False):
        fc = st.session_state.font_cfg
        st.caption("16:9 Landscape")
        ls_dt_fs   = st.slider("Date/Time",    40, 140, fc["ls_dt"], 2, key="sl_ls_dt")
        ls_name_fs = st.slider("Country Name", 60, 260, fc["ls_nm"], 2, key="sl_ls_nm")
        st.caption("2:3 Portrait")
        pt_dt_fs   = st.slider("Date/Time",    40, 120, fc["pt_dt"], 2, key="sl_pt_dt")
        pt_name_fs = st.slider("Country Name", 60, 260, fc["pt_nm"], 2, key="sl_pt_nm")
        new_cfg = {"ls_dt": ls_dt_fs, "ls_nm": ls_name_fs, "pt_dt": pt_dt_fs, "pt_nm": pt_name_fs}
        if new_cfg != fc:
            st.session_state.font_cfg = new_cfg
            _save_font_cfg(new_cfg)
    fc = st.session_state.font_cfg
    ls_dt_fs, ls_name_fs = fc["ls_dt"], fc["ls_nm"]
    pt_dt_fs, pt_name_fs = fc["pt_dt"], fc["pt_nm"]

    # ---- Custom Background (collapsed) ----
    with st.expander("🖼 Custom Background", expanded=False):
        bg_file = st.file_uploader("Upload PNG/JPG (overrides default)", type=["png","jpg","jpeg"])

    # ---- Preview button — at the end of all sidebar sections ----
    st.divider()
    preview_btn = st.button("▶  Preview", use_container_width=True, type="primary")

# ---------------------------------------------------------------------------
# PREVIEW
# ---------------------------------------------------------------------------
if preview_btn:
    m = dict(match)

    with st.spinner("Rendering…"):
        with tempfile.TemporaryDirectory() as tmp:
            if bg_file:
                bg_path = os.path.join(tmp, "bg.png")
                with open(bg_path, "wb") as f:
                    f.write(bg_file.read())
                m["bg"] = bg_path

            h = dict(m); h["mode"] = "highlights"; h.setdefault("tag", "ম্যাচ হাইলাইটস")

            paths = {
                "ls":    os.path.join(tmp, "ls.png"),
                "ls_hl": os.path.join(tmp, "ls_hl.png"),
                "pt":    os.path.join(tmp, "pt.png"),
                "pt_hl": os.path.join(tmp, "pt_hl.png"),
            }
            ls_cfg = {"datetime_fs": ls_dt_fs, "name_base": ls_name_fs}
            pt_cfg = {"datetime_fs": pt_dt_fs, "name_base": pt_name_fs}
            render(m,          paths["ls"],    font_cfg=ls_cfg)
            render(h,          paths["ls_hl"], font_cfg=ls_cfg)
            render_portrait(m, paths["pt"],    font_cfg=pt_cfg)
            render_portrait(h, paths["pt_hl"], font_cfg=pt_cfg)

            # read bytes into memory before tempdir is deleted, so the preview
            # (and its download button) survive Streamlit reruns
            base = f"match_{match_no:03d}_{m['a_code']}_{m['b_code']}"
            files = {
                f"{base}.png":      (paths["ls"],    "Fixture — Landscape 16:9"),
                f"{base}_HL.png":   (paths["ls_hl"], "Highlights — Landscape 16:9"),
                f"{base}_P.png":    (paths["pt"],    "Fixture — Portrait 2:3"),
                f"{base}_HL_P.png": (paths["pt_hl"], "Highlights — Portrait 2:3"),
            }
            imgs = {}
            for fname, (p, cap) in files.items():
                with open(p, "rb") as f:
                    imgs[fname] = (f.read(), cap)

    st.session_state.preview = {
        "no": match_no, "base": base,
        "title": f"Match {match_no}: {m['a_name']} vs {m['b_name']}",
        "imgs": imgs,
    }

pv = st.session_state.get("preview")
if pv:
    imgs = pv["imgs"]

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname, (data, _cap) in imgs.items():
            zf.writestr(fname, data)

    head_l, head_r = st.columns([3, 1])
    with head_l:
        st.subheader(pv["title"])
    with head_r:
        st.download_button(
            "⬇  Download All (ZIP)",
            data=zip_buf.getvalue(),
            file_name=f"{pv['base']}.zip",
            mime="application/zip",
            use_container_width=True,
        )

    col1, col2, col3 = st.columns([9, 9, 4])
    names = list(imgs.keys())
    with col1:
        for n in names[:2]:
            data, cap = imgs[n]
            st.image(data, caption=cap, use_container_width=True)
    with col2:
        pass  # spacer keeps portrait from stretching
    with col3:
        for n in names[2:]:
            data, cap = imgs[n]
            st.image(data, caption=cap, use_container_width=True)

# ---------------------------------------------------------------------------
# TOURNAMENT OVERVIEW  (replaces the old batch generator)
# ---------------------------------------------------------------------------
st.divider()
st.header("📊 Tournament at a Glance")

_stadiums = {v["stadium"] for v in VENUE_INFO.values()}
_cities   = {v["city"]    for v in VENUE_INFO.values()}
_teams    = {c for m in fixtures for c in (m.get("a_code"), m.get("b_code")) if c}

c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches",   len(fixtures))
c2.metric("Teams",     len(_teams))
c3.metric("Stadiums",  len(_stadiums))
c4.metric("Host Cities", len(_cities))

st.markdown("""
### 🟢 How to use
1. **Pick a match** in the left sidebar.
2. *(Optional)* open **Custom Background** to upload your own photo, or **Font Sizes** to fine-tune.
3. Hit **▶ Preview** — fixture + highlights banners render in both landscape and portrait.
4. Click **⬇ Download All (ZIP)** above the preview to save all four PNGs.

### 💡 Tips
- Country names auto-shrink **together**, so any name length fills the same slot cleanly.
- Need every match at once? Run the batch locally: `python3 batch.py` → images land in `out/`.
""")

st.divider()
gh = "https://github.com/haradhansarker-commits/wc26-banner-engine"
lc1, lc2 = st.columns(2)
lc1.link_button("📖  README & Guide", f"{gh}#readme", use_container_width=True)
lc2.link_button("⭐  Source on GitHub", gh, use_container_width=True)
st.caption("FIFA World Cup 2026 · Bengali team-vs-team banners · 16:9 + 2:3")
