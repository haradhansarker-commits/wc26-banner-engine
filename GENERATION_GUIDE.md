# FIFA WC26 Banner Generator — Full Guide

How to generate the actual images, add real **venue background photos**, and what the
`.py` file is for.

---

## TL;DR — what's in this folder

| File | What it is | Do you run it? |
|---|---|---|
| **`wc26_template.py`** | The generator. Contains the design, the flag library, and the `render()` function. | **This is the engine.** You don't normally *edit* it — you *import* it from a small driver script (see §4), or run it directly to make the examples. |
| `make_stadium_bg.py` | One-off script that draws the fallback `stadium_bg.png`. | Run once if you ever delete the fallback image. |
| `stadium_bg.png` | Default backdrop used when a match has no real venue photo. | No — it's data. |
| `banner_opening.png` etc. | The three example outputs. | No — samples. |

**So: what do I do with the `.py`?**
Keep `wc26_template.py` as your reusable library and call its `render(match, output_path)`
function once per match from a tiny loop. Section 4 has a copy-paste driver. Running
`python3 wc26_template.py` by itself just regenerates the three demo images.

---

## 0. The things you asked about

- **Date/time legibility (small screens):** fixed. Date and time are now a single bold
  line ("১১ জুন ২০২৬ · রাত ১২ঃ৩০") at 50px, alone in the bottom bar. Verified readable
  down to a 300px-wide thumbnail.
- **Venue as background, no venue name printed:** done. The stadium photo fills the whole
  frame behind a darkening scrim; the venue *text* was removed from the image. (You can
  still pass `venue` in the data for filenames/notes — it just isn't drawn.)

---

## 1. One-time setup

**Rasterizer (turns the SVG into a PNG):**
```bash
sudo apt-get install -y librsvg2-bin     # Ubuntu/Debian -> gives `rsvg-convert`
brew install librsvg                      # macOS
# Windows: WSL + the apt line, or `choco install rsvg-convert`
```

**Python libs:**
```bash
pip install pillow        # for the fallback-bg script + thumbnail resizing
```

**Fonts** — keep these five in a `fonts/` folder next to `wc26_template.py`
(they get embedded into each image, so viewers don't need them installed):
```
fonts/AnekBangla.ttf  HindSiliguri-Bold.ttf  HindSiliguri-SemiBold.ttf
fonts/HindSiliguri-Regular.ttf  BigShoulders-Bold.ttf
```
Download commands are in §8. Adjust `FONT_DIR` at the top of the script if needed.

---

## 2. Add your venue background photos  ← the new part

Create a `venues/` folder next to the script and drop in one image per stadium:
```
venues/
  azteca.png
  metlife.png
  sofi.png
  ...
```

**Photo tips**
- Landscape, ideally ≥ 1920×1080. The script crops-to-fill (`xMidYMid slice`); larger is
  fine, very tall/narrow images get center-cropped.
- Interior night/floodlit shots (pitch + stands) look best; the scrim darkens them so the
  flags and text stay readable.
- PNG or JPG both work (for JPG, change `image/png` → `image/jpeg` in `build_svg`, or just
  convert once with Pillow).
- **Licensing:** use photos you have rights to (official media kits, licensed stock, CC
  with attribution, or your own). The generator ships none.

**How the script picks the background (priority order):**
1. `m["bg"]` — explicit full path in the match dict, if present.
2. `venues/<m["venue_img"]>` — a filename in the match dict.
3. `stadium_bg.png` — procedural fallback, so matches with no photo still render.

---

## 3. Generate the examples (sanity check)

```bash
python3 wc26_template.py
```
Produces `banner_opening.png`, `banner_highlights.png`, `banner_longname.png`
(1920×1080, 16:9). Each also writes a sibling `.svg` you can delete.

---

## 4. The match dictionary + batch driver

One dict per banner:
```python
match = {
    "a_code": "MEX", "a_name": "মেক্সিকো",        # left team: code drives flag+color, name is the big text
    "b_code": "RSA", "b_name": "দক্ষিণ আফ্রিকা",   # right team

    "mode":  "fixture",                           # "fixture" = date/time bar | "highlights" = badge
    "stage": "গ্রুপ এ — উদ্বোধনী ম্যাচ",            # small line under the title (optional)

    "line1": "১১ জুন ২০২৬",                        # date (fixture mode)
    "line2": "রাত ১২ঃ৩০",                          # time (fixture mode)

    "venue_img": "azteca.png",                    # ← background photo in venues/  (optional)
    # "bg": "/full/path/to/some.png",             # ← or an explicit path (optional)
    # "venue": "...",                             # optional, NOT drawn — for your own filenames/notes
    # "tag": "ম্যাচ হাইলাইটস",                     # highlights-mode badge text (default provided)
}
```

`batch.py` — put next to `wc26_template.py`, fill `fixtures.json`, run:
```python
import json, os
from wc26_template import render

os.makedirs("out", exist_ok=True)
for i, m in enumerate(json.load(open("fixtures.json", encoding="utf-8")), 1):
    base = f"out/match_{i:03d}_{m['a_code']}_{m['b_code']}"
    render(m, base + ".png")                                    # fixture banner
    h = dict(m); h["mode"] = "highlights"; h["tag"] = "ম্যাচ হাইলাইটস"
    render(h, base + "_HL.png")                                 # highlights banner
    print("done", base)
```
```bash
python3 batch.py
```

`fixtures.json` example:
```json
[
  {"a_code":"MEX","a_name":"মেক্সিকো","b_code":"RSA","b_name":"দক্ষিণ আফ্রিকা",
   "mode":"fixture","stage":"গ্রুপ এ — উদ্বোধনী ম্যাচ",
   "line1":"১১ জুন ২০২৬","line2":"রাত ১২ঃ৩০","venue_img":"azteca.png"},

  {"a_code":"ARG","a_name":"আর্জেন্টিনা","b_code":"BRA","b_name":"ব্রাজিল",
   "mode":"fixture","stage":"গ্রুপ সি",
   "line1":"১৩ জুন ২০২৬","line2":"রাত ৯ঃ০০","venue_img":"metlife.png"}
]
```

---

## 5. Thumbnails for app lists

```bash
rsvg-convert -w 384 -h 216 out/match_001_MEX_RSA.svg -o out/thumb_001.png
# or downscale the PNG:
python3 - <<'PY'
from PIL import Image
Image.open("out/match_001_MEX_RSA.png").resize((384,216), Image.LANCZOS).save("out/thumb_001.png")
PY
```
Layout was tuned so names, flags, VS, and the date/time line stay legible to ~300px wide.

---

## 6. Adding a team (flag + accent color)

In `wc26_template.py`:
```python
ACCENT["NED"] = "#f36c21"                       # side-glow color
def flag_netherlands(): return _stripes_h(["#AE1C28","#FFFFFF","#21468B"])
FLAGS["NED"] = flag_netherlands
```
Unknown codes fall back to a neutral gold/blue "TBD" crest (good for undecided slots).

Bengali numerals helper:
```python
def bn(s): return s.translate(str.maketrans("0123456789","০১২৩৪৫৬৭৮৯"))
```

---

## 7. Quick tweaks

| Want | Change |
|---|---|
| Different size (e.g. 1280×720) | `W, H` at top (keep 16:9) |
| Lighter/darker photo | the `#05070b opacity="0.45"` scrim rect, and `scrimTop/scrimBot/vign` stops in `<defs>` |
| Less color tint over photo | the two `floodL/floodR` wash `opacity="0.7"` values |
| Bigger date/time | `font-size="50"` on the `dt` line |
| JPG venue photos | change `image/png` → `image/jpeg` in `build_svg` |

---

## 8. Font downloads (run once)

```bash
mkdir -p fonts && cd fonts
curl -sL "https://github.com/google/fonts/raw/main/ofl/anekbangla/AnekBangla%5Bwdth%2Cwght%5D.ttf" -o AnekBangla.ttf
curl -sL "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf" -o HindSiliguri-Bold.ttf
curl -sL "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-SemiBold.ttf" -o HindSiliguri-SemiBold.ttf
curl -sL "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Regular.ttf" -o HindSiliguri-Regular.ttf
# BigShoulders-Bold.ttf: Google Fonts "Big Shoulders Display" Bold (or any bold Latin font)
```

---

## 9. Troubleshooting

- `rsvg-convert: command not found` → install librsvg (§1).
- Bengali shows as boxes, or conjuncts (ক্ষ, র্জে) look broken → wrong/missing Bengali
  font; confirm `fonts/` + `FONT_DIR`. Generic system fonts often lack Bengali shaping.
- Always seeing the generic stadium → your `venue_img`/`bg` path is wrong; the script
  silently falls back to `stadium_bg.png`.
- Text hard to read over a bright photo → raise the scrim opacity (§7).

---

### Recap of your three questions
1. **Date/time legible on small screens?** Yes — re-verified at 300px; one big bold line.
2. **Venue image as background, name not printed?** Done — photo fills the frame, name removed.
3. **What to do with the `.py`?** Keep `wc26_template.py` as your library; drive it from
   `batch.py` (one `render()` call per match). Running it directly just rebuilds the demos.
