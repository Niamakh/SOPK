# -*- coding: utf-8 -*-
"""Valide que tous les blocs <script type="application/ld+json"> de chaque page HTML sont du JSON valide."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.DOTALL
)


def main():
    total_ok = 0
    total_err = 0
    for f in sorted(ROOT.glob("*.html")):
        text = f.read_text(encoding="utf-8")
        blocks = PATTERN.findall(text)
        for i, block in enumerate(blocks):
            try:
                json.loads(block)
                total_ok += 1
            except json.JSONDecodeError as e:
                total_err += 1
                print(f"ERREUR JSON dans {f.name} (bloc {i + 1}): {e}")
    print(f"\n{total_ok} blocs JSON-LD valides, {total_err} erreurs.")


if __name__ == "__main__":
    main()
