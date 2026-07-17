# -*- coding: utf-8 -*-
"""Compare les questions du schema FAQPage avec les <summary> visibles de la page."""
import json
import pathlib
import re
import html

ROOT = pathlib.Path(__file__).resolve().parent.parent
JSONLD_RE = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.DOTALL)
SUMMARY_RE = re.compile(r'<summary>(.*?)</summary>', re.DOTALL)

FILES = [
    "disque-roue-grossesse-calcul-terme.html",
    "journal-grossesse-a-imprimer-gratuit.html",
    "prise-de-sang-grossesse-taux-beta-hcg.html",
]


def clean(s):
    s = html.unescape(s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.replace('\u00a0', ' ')
    return s


for name in FILES:
    text = (ROOT / name).read_text(encoding="utf-8")
    faq_questions = []
    for block in JSONLD_RE.findall(text):
        data = json.loads(block)
        if data.get("@type") == "FAQPage":
            faq_questions = [clean(q["name"]) for q in data["mainEntity"]]
    visible = [clean(s) for s in SUMMARY_RE.findall(text)]
    print(f"\n=== {name} ===")
    print(f"FAQPage: {len(faq_questions)} questions | Visible: {len(visible)} <summary>")
    missing_in_visible = [q for q in faq_questions if q not in visible]
    missing_in_schema = [q for q in visible if q not in faq_questions]
    if not missing_in_visible and not missing_in_schema and len(faq_questions) == len(visible):
        print("OK : correspondance exacte")
    else:
        if missing_in_visible:
            print("Dans le schema mais absent du visible:")
            for q in missing_in_visible:
                print(f"  - {q}")
        if missing_in_schema:
            print("Visible mais absent du schema:")
            for q in missing_in_schema:
                print(f"  - {q}")
