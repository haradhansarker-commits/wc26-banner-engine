#!/usr/bin/env bash
# One-shot setup for the WC26 banner engine.
# Run from the project root:  bash setup.sh
set -e

echo "==> 1/4  System rasterizer (librsvg)"
if ! command -v rsvg-convert >/dev/null 2>&1; then
  if   command -v apt-get >/dev/null 2>&1; then sudo apt-get update && sudo apt-get install -y librsvg2-bin
  elif command -v brew    >/dev/null 2>&1; then brew install librsvg
  elif command -v dnf     >/dev/null 2>&1; then sudo dnf install -y librsvg2-tools
  elif command -v choco   >/dev/null 2>&1; then choco install -y rsvg-convert
  else echo "!! Install librsvg manually (need the 'rsvg-convert' command)."; fi
else
  echo "    rsvg-convert already present."
fi

echo "==> 2/4  Python deps"
pip install -r requirements.txt

echo "==> 3/4  Fonts"
mkdir -p fonts
dl () { [ -f "fonts/$2" ] || curl -fsSL "$1" -o "fonts/$2"; }
dl "https://github.com/google/fonts/raw/main/ofl/anekbangla/AnekBangla%5Bwdth%2Cwght%5D.ttf" "AnekBangla.ttf"
dl "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"          "HindSiliguri-Bold.ttf"
dl "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-SemiBold.ttf"      "HindSiliguri-SemiBold.ttf"
dl "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Regular.ttf"       "HindSiliguri-Regular.ttf"
dl "https://github.com/google/fonts/raw/main/ofl/bigshouldersdisplay/BigShouldersDisplay%5Bwght%5D.ttf" "BigShoulders-Bold.ttf"
echo "    fonts ready:"; ls fonts/

echo "==> 4/4  Fallback stadium background"
[ -f stadium_bg.png ] || python3 make_stadium_bg.py

echo ""
echo "Setup complete. Try:  python3 wc26_template.py    (renders the 3 examples)"
echo "Then batch:           python3 batch.py             (reads fixtures.json -> out/)"
