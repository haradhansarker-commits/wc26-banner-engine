# CLAUDE.md — WC26 Banner Engine

This project generates **FIFA World Cup 2026 "team vs team" banners/thumbnails** in
**Bengali**, 16:9 (1920×1080). It is a small, self-contained Python engine.

## What each file is
- `wc26_template.py` — the engine. Exposes `render(match_dict, output_path)`. Holds the
  design, the procedural flag library (`FLAGS`), and team accent colors (`ACCENT`).
  Running it directly renders 3 example images. **Edit it only to add teams or tweak style.**
- `batch.py` — driver. Reads `fixtures.json`, calls `render()` once per match, and also
  emits a `_HL` highlights version of each. Run: `python3 batch.py [fixtures.json] [out_dir]`.
- `fixtures.json` — the input data (list of match dicts).
- `make_stadium_bg.py` — regenerates the procedural fallback `stadium_bg.png`.
- `fonts/` — embedded Bengali + Latin fonts (required).
- `venues/` — optional real stadium photos used as backgrounds.
- `setup.sh` — installs everything (librsvg, Pillow, fonts, fallback bg).

## Hard dependency
`rsvg-convert` (from **librsvg**) must be on PATH — it converts the SVG to PNG. `pip`
cannot provide it; install via the OS package manager (see `setup.sh`).

## Match dict schema
```jsonc
{
  "a_code": "MEX", "a_name": "মেক্সিকো",      // left team (code -> flag + glow color)
  "b_code": "RSA", "b_name": "দক্ষিণ আফ্রিকা", // right team
  "mode": "fixture",                          // "fixture" (date/time bar) | "highlights" (badge)
  "stage": "গ্রুপ এ — উদ্বোধনী ম্যাচ",          // optional small line under the title
  "line1": "১১ জুন ২০২৬",                      // date  (fixture mode; Bengali numerals)
  "line2": "রাত ১২ঃ৩০",                        // time  (fixture mode)
  "venue_img": "azteca.png",                  // optional bg photo in venues/
  "bg": "/abs/path.png",                      // optional explicit bg path (overrides venue_img)
  "tag": "ম্যাচ হাইলাইটস"                      // highlights-mode badge text (has a default)
}
```
Notes: country names auto-shrink **together** so any length fills the same slot.
The venue NAME is never drawn on the image (the photo is the venue cue).
Background priority: `bg` -> `venues/<venue_img>` -> `stadium_bg.png` fallback.

## Common tasks (how to help the user)
- **"Generate banners for these fixtures"** → write/append to `fixtures.json`, then run
  `python3 batch.py`. Output PNGs land in `out/`.
- **"Add a team"** → in `wc26_template.py`: add `ACCENT["XXX"] = "#color"` and a
  `flag_xxx()` function, then `FLAGS["XXX"] = flag_xxx`. Flags draw inside a 0..100 × 0..66.667 box.
- **"Use a real stadium photo"** → drop a landscape image into `venues/` and set
  `"venue_img": "<file>"` on the match. Larger than 1920×1080 is fine (crop-to-fill).
- **"Make thumbnails"** → `rsvg-convert -w 384 -h 216 out/<file>.svg -o thumb.png`,
  or downscale the PNG with Pillow.
- **English digits → Bengali**: `str.maketrans("0123456789","০১২৩৪৫৬৭৮৯")`.

## Conventions
- Keep output 16:9. To change size, edit `W, H` (top of `wc26_template.py`).
- Don't commit `venues/*` photos unless you own the rights.
- Generated `.svg` siblings next to each PNG can be deleted; they're intermediate.
