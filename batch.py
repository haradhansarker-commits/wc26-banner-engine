#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-generate WC26 banners from fixtures.json.

Usage:
    python3 batch.py                 # reads fixtures.json, writes to ./out
    python3 batch.py myfixtures.json out_folder
"""
import json, os, sys
from wc26_template import render, render_portrait

def main():
    fixtures_path = sys.argv[1] if len(sys.argv) > 1 else "fixtures.json"
    out_dir       = sys.argv[2] if len(sys.argv) > 2 else "out"
    os.makedirs(out_dir, exist_ok=True)

    with open(fixtures_path, encoding="utf-8") as f:
        fixtures = json.load(f)

    for i, m in enumerate(fixtures, 1):
        base = os.path.join(out_dir, f"match_{i:03d}_{m['a_code']}_{m['b_code']}")
        h = dict(m); h["mode"] = "highlights"; h.setdefault("tag", "ম্যাচ হাইলাইটস")
        # landscape (16:9)
        render(m, base + ".png")
        render(h, base + "_HL.png")
        # portrait (2:3)
        render_portrait(m, base + "_P.png")
        render_portrait(h, base + "_HL_P.png")
        print(f"[{i}/{len(fixtures)}] {m['a_code']} vs {m['b_code']}  ->  {base}.png + _HL + _P + _HL_P")

    print(f"\nDone. {len(fixtures)} matches -> {len(fixtures)*4} images in '{out_dir}/'.")

if __name__ == "__main__":
    main()
