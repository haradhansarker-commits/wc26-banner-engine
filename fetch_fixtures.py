#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch all 104 FIFA World Cup 2026 fixtures from ESPN API and write fixtures.json.
Run: python3 fetch_fixtures.py
"""
import json, urllib.request, sys
from datetime import datetime, timedelta, timezone

# ── Bengali helpers ────────────────────────────────────────────────────────────
_NUM = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
def bn(n): return str(n).translate(_NUM)

MONTHS = ["","জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন",
          "জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"]

def bst(utc_str):
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return dt + timedelta(hours=6)   # Bangladesh Standard Time

def fmt_date(dt):
    return f"{bn(dt.day)} {MONTHS[dt.month]} {bn(dt.year)}"

def fmt_time(dt):
    h = dt.hour; m = dt.minute
    h12 = h % 12 or 12
    if   h == 0:        pfx = "রাত"
    elif h < 4:         pfx = "রাত"
    elif h < 6:         pfx = "ভোর"
    elif h < 12:        pfx = "সকাল"
    elif h == 12:       pfx = "দুপুর"
    elif h < 15:        pfx = "দুপুর"
    elif h < 18:        pfx = "বিকাল"
    elif h < 20:        pfx = "সন্ধ্যা"
    else:               pfx = "রাত"
    mm = f"{bn(m):0>2}" if m else "০০"
    return f"{pfx} {bn(h12)}ঃ{mm}"

# ── Team code → Bengali name ───────────────────────────────────────────────────
TEAM_BN = {
    "MEX": "মেক্সিকো",      "RSA": "দক্ষিণ আফ্রিকা", "ARG": "আর্জেন্টিনা",
    "BRA": "ব্রাজিল",       "ENG": "ইংল্যান্ড",       "FRA": "ফ্রান্স",
    "ESP": "স্পেন",          "GER": "জার্মানি",         "POR": "পর্তুগাল",
    "USA": "যুক্তরাষ্ট্র",  "MAR": "মরক্কো",
    "KOR": "দক্ষিণ কোরিয়া","CZE": "চেক রিপাবলিক",
    "CAN": "কানাডা",         "BIH": "বসনিয়া ও হার্জেগোভিনা",
    "QAT": "কাতার",          "SUI": "সুইজারল্যান্ড",
    "HAI": "হাইতি",          "SCO": "স্কটল্যান্ড",
    "PAR": "প্যারাগুয়ে",    "AUS": "অস্ট্রেলিয়া",   "TUR": "তুরস্ক",
    "CUW": "কুরাসাও",        "CIV": "আইভোরি কোস্ট",   "ECU": "ইকুয়েডর",
    "NED": "নেদারল্যান্ডস", "JPN": "জাপান",           "SWE": "সুইডেন",
    "TUN": "তিউনিসিয়া",    "BEL": "বেলজিয়াম",       "EGY": "মিশর",
    "IRN": "ইরান",           "NZL": "নিউজিল্যান্ড",   "CPV": "কাবো ভার্দে",
    "KSA": "সৌদি আরব",      "URU": "উরুগুয়ে",
    "SEN": "সেনেগাল",        "IRQ": "ইরাক",            "NOR": "নরওয়ে",
    "ALG": "আলজেরিয়া",     "AUT": "অস্ট্রিয়া",      "JOR": "জর্ডান",
    "COD": "কঙ্গো ডিআর",    "UZB": "উজবেকিস্তান",   "COL": "কলম্বিয়া",
    "CRO": "ক্রোয়েশিয়া",  "GHA": "ঘানা",            "PAN": "পানামা",
}

# ── Official group assignments from ESPN standings ────────────────────────────
TEAM_GROUP = {
    "CZE":"A","KOR":"A","MEX":"A","RSA":"A",
    "BIH":"B","CAN":"B","QAT":"B","SUI":"B",
    "BRA":"C","HAI":"C","MAR":"C","SCO":"C",
    "AUS":"D","PAR":"D","TUR":"D","USA":"D",
    "CIV":"E","CUW":"E","ECU":"E","GER":"E",
    "JPN":"F","NED":"F","SWE":"F","TUN":"F",
    "BEL":"G","EGY":"G","IRN":"G","NZL":"G",
    "CPV":"H","ESP":"H","KSA":"H","URU":"H",
    "FRA":"I","IRQ":"I","NOR":"I","SEN":"I",
    "ALG":"J","ARG":"J","AUT":"J","JOR":"J",
    "COD":"K","COL":"K","POR":"K","UZB":"K",
    "CRO":"L","ENG":"L","GHA":"L","PAN":"L",
}

# ── Group winner/runner-up placeholder names ───────────────────────────────────
GRP_LETTER = {
    "A":"এ","B":"বি","C":"সি","D":"ডি","E":"ই","F":"এফ",
    "G":"জি","H":"এইচ","I":"আই","J":"জে","K":"কে","L":"এল",
}

def placeholder_name(code, display):
    """Return Bengali name for TBD placeholder codes."""
    # Winner codes: "1A".."1L"
    if len(code) == 2 and code[0] == "1" and code[1] in GRP_LETTER:
        return f"গ্রুপ {GRP_LETTER[code[1]]} বিজয়ী"
    # Runner-up codes: "2A".."2L"
    if len(code) == 2 and code[0] == "2" and code[1] in GRP_LETTER:
        return f"গ্রুপ {GRP_LETTER[code[1]]} রানার্সআপ"
    # Third-place group combos
    if code.startswith("3"):
        return f"সেরা তৃতীয় দল"
    # Round of 32 winner e.g. "RD32"
    if "RD32" in code:
        return "রাউন্ড অব ৩২ বিজয়ী"
    # Round of 16 winners e.g. "RD16 W1"
    if "RD16" in code:
        n = code.split()[-1].replace("W","")
        return f"আর-১৬ ম্যাচ {bn(n)} বিজয়ী"
    # Quarterfinal winners "QFW1".."QFW4" / "QW4"
    if code.startswith("QF") or code.startswith("QW"):
        n = code[-1]
        return f"কোয়ার্টার ফাইনাল {bn(n)} বিজয়ী"
    # Semifinal winner/loser "SFW1","SFW2","SF L1","SF L2"
    if code.startswith("SF"):
        n = code[-1]
        if "L" in code:
            return f"সেমি ফাইনাল {bn(n)} পরাজিত"
        return f"সেমি ফাইনাল {bn(n)} বিজয়ী"
    # fallback: use ESPN display name transliterated
    return display

def team_bn(code, display):
    return TEAM_BN.get(code, placeholder_name(code, display))

# ── Stage name in Bengali ──────────────────────────────────────────────────────
STAGE_BN = {
    "group-stage":      "গ্রুপ পর্ব",
    "round-of-32":      "রাউন্ড অব ৩২",
    "round-of-16":      "রাউন্ড অব ১৬",
    "quarterfinals":    "কোয়ার্টার ফাইনাল",
    "semifinals":       "সেমি ফাইনাল",
    "3rd-place-match":  "তৃতীয় স্থান নির্ধারণী",
    "final":            "ফাইনাল",
}

# ── Fetch from ESPN ────────────────────────────────────────────────────────────
ESPN_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world"
    "/scoreboard?dates=20260611-20260720&limit=200"
)

def fetch_events():
    req = urllib.request.Request(ESPN_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)["events"]

def parse_event(ev, _=None):
    comp   = ev["competitions"][0]
    slug   = ev["season"]["slug"]
    dt_utc = ev["date"]
    dt     = bst(dt_utc)

    competitors = comp["competitors"]
    # home = index 0 is away, index 1 is home in ESPN — use order as-is (a=away, b=home)
    away = competitors[0]; home = competitors[1]
    a_code = away["team"]["abbreviation"]
    b_code = home["team"]["abbreviation"]
    a_disp = away["team"]["displayName"]
    b_disp = home["team"]["displayName"]

    # Stage label
    if slug == "group-stage":
        grp = TEAM_GROUP.get(a_code) or TEAM_GROUP.get(b_code) or "?"
        stage = f"গ্রুপ {GRP_LETTER.get(grp, grp)}"
    else:
        stage = STAGE_BN.get(slug, slug)

    # Determine team code to use (map ESPN code → our FLAGS code)
    # ESPN codes match our codes for real teams; placeholder codes stay as-is
    fixture = {
        "a_code": a_code if a_code in TEAM_BN else "TBD",
        "a_name": team_bn(a_code, a_disp),
        "b_code": b_code if b_code in TEAM_BN else "TBD",
        "b_name": team_bn(b_code, b_disp),
        "mode":   "fixture",
        "stage":  stage,
        "line1":  fmt_date(dt),
        "line2":  fmt_time(dt),
    }
    return fixture

def main():
    print("Fetching WC2026 fixtures from ESPN…", flush=True)
    try:
        events = fetch_events()
    except Exception as ex:
        print(f"ERROR: {ex}"); sys.exit(1)

    print(f"  {len(events)} events received")

    fixtures = []
    for ev in events:
        try:
            fixtures.append(parse_event(ev, {}))
        except Exception as ex:
            print(f"  skip {ev.get('name','?')}: {ex}")

    out = "fixtures.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)

    print(f"  Written {len(fixtures)} fixtures → {out}")

    from collections import Counter
    for stage, n in Counter(fx["stage"] for fx in fixtures).most_common():
        print(f"    {stage}: {n}")

if __name__ == "__main__":
    main()
