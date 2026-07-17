# -*- coding: utf-8 -*-
"""
Ajoute les 3 nouvelles pages "outils PDF grossesse"
(disque-roue-grossesse-calcul-terme.html, journal-grossesse-a-imprimer-gratuit.html,
prise-de-sang-grossesse-taux-beta-hcg.html) dans :
  1. le mega-menu desktop "Rubriques"
  2. le menu mobile "Rubriques"
  3. le footer "Rubriques" (uniquement sur les pages où c'est pertinent)
sur toutes les pages existantes du site qui ne les ont pas encore.
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_FILES = {
    "disque-roue-grossesse-calcul-terme.html",
    "journal-grossesse-a-imprimer-gratuit.html",
    "prise-de-sang-grossesse-taux-beta-hcg.html",
}

DESKTOP_ANCHOR = (
    '<a href="saignement-nidation-couleur-duree.html" class="flex items-center gap-3 '
    'rounded-xl p-3 transition hover:bg-sand"><span class="text-xl leading-none">🩸</span>'
    '<div><p class="font-semibold text-ink text-sm leading-tight">Saignement de nidation</p>'
    '<p class="text-xs text-muted mt-0.5">Couleur, durée, différences</p></div></a>'
)

DESKTOP_INSERT = (
    '\n                  <a href="disque-roue-grossesse-calcul-terme.html" class="flex items-center gap-3 rounded-xl p-3 transition hover:bg-sand"><span class="text-xl leading-none">🧮</span><div><p class="font-semibold text-ink text-sm leading-tight">Disque de grossesse</p><p class="text-xs text-muted mt-0.5">Calcul DPA &amp; SA en ligne</p></div></a>'
    '\n                  <a href="journal-grossesse-a-imprimer-gratuit.html" class="flex items-center gap-3 rounded-xl p-3 transition hover:bg-sand"><span class="text-xl leading-none">📔</span><div><p class="font-semibold text-ink text-sm leading-tight">Journal de grossesse</p><p class="text-xs text-muted mt-0.5">Carnet à imprimer gratuit</p></div></a>'
    '\n                  <a href="prise-de-sang-grossesse-taux-beta-hcg.html" class="flex items-center gap-3 rounded-xl p-3 transition hover:bg-sand"><span class="text-xl leading-none">🧪</span><div><p class="font-semibold text-ink text-sm leading-tight">Taux bêta-hCG</p><p class="text-xs text-muted mt-0.5">Comprendre sa prise de sang</p></div></a>'
)

MOBILE_ANCHOR = (
    '<a href="saignement-nidation-couleur-duree.html" class="flex items-center gap-3 '
    'font-serif text-2xl leading-none" data-mobile-link><span>🩸</span> Saignement de nidation</a>'
)

MOBILE_INSERT = (
    '\n            <a href="disque-roue-grossesse-calcul-terme.html" class="flex items-center gap-3 font-serif text-2xl leading-none" data-mobile-link><span>🧮</span> Disque de grossesse</a>'
    '\n            <a href="journal-grossesse-a-imprimer-gratuit.html" class="flex items-center gap-3 font-serif text-2xl leading-none" data-mobile-link><span>📔</span> Journal de grossesse</a>'
    '\n            <a href="prise-de-sang-grossesse-taux-beta-hcg.html" class="flex items-center gap-3 font-serif text-2xl leading-none" data-mobile-link><span>🧪</span> Taux bêta-hCG</a>'
)

# Pages où le footer "Rubriques" doit aussi recevoir les 3 nouveaux liens
# (pages thématiquement liées à la grossesse / nidation).
FOOTER_TARGET_FILES = {
    "index.html",
    "blog.html",
    "a-propos.html",
    "article-sopk-grossesse.html",
    "nidation-combien-de-temps-apres-rapport.html",
    "saignement-nidation-couleur-duree.html",
}

FOOTER_ITEM_RE = re.compile(
    r'<li><a class="([^"]+)" href="(saignement-nidation-couleur-duree\.html|'
    r'nidation-combien-de-temps-apres-rapport\.html|article-sopk-grossesse\.html)">'
    r'[^<]*</a></li>'
)


def build_footer_insert(cls, existing_hrefs):
    items = []
    if "disque-roue-grossesse-calcul-terme.html" not in existing_hrefs:
        items.append(f'<li><a class="{cls}" href="disque-roue-grossesse-calcul-terme.html">Disque de grossesse</a></li>')
    if "journal-grossesse-a-imprimer-gratuit.html" not in existing_hrefs:
        items.append(f'<li><a class="{cls}" href="journal-grossesse-a-imprimer-gratuit.html">Journal de grossesse</a></li>')
    if "prise-de-sang-grossesse-taux-beta-hcg.html" not in existing_hrefs:
        items.append(f'<li><a class="{cls}" href="prise-de-sang-grossesse-taux-beta-hcg.html">Taux bêta-hCG</a></li>')
    if not items:
        return ""
    return "\n                " + "\n                ".join(items)


def process(path: pathlib.Path):
    name = path.name
    if name in SKIP_FILES:
        return "skip (nouvelle page)"

    text = path.read_text(encoding="utf-8")
    original = text
    changes = []

    if DESKTOP_ANCHOR in text and "disque-roue-grossesse-calcul-terme.html" not in text:
        text = text.replace(DESKTOP_ANCHOR, DESKTOP_ANCHOR + DESKTOP_INSERT, 1)
        changes.append("desktop")

    if MOBILE_ANCHOR in text and "font-serif text-2xl leading-none\" data-mobile-link><span>🧮</span>" not in text:
        text = text.replace(MOBILE_ANCHOR, MOBILE_ANCHOR + MOBILE_INSERT, 1)
        changes.append("mobile")

    if name in FOOTER_TARGET_FILES:
        matches = list(FOOTER_ITEM_RE.finditer(text))
        if matches:
            last = matches[-1]
            cls = last.group(1)
            # Ne regarder que le <ul> englobant ce lien pour déterminer les hrefs déjà présents
            ul_start = text.rfind("<ul", 0, last.start())
            ul_end = text.find("</ul>", last.end())
            ul_block = text[ul_start:ul_end] if ul_start != -1 and ul_end != -1 else text
            existing_hrefs = set(re.findall(r'href="([^"]+\.html)"', ul_block))
            insert = build_footer_insert(cls, existing_hrefs)
            if insert:
                text = text[: last.end()] + insert + text[last.end():]
                changes.append("footer")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return ", ".join(changes)
    return "aucun changement (motif non trouvé ou déjà présent)"


def main():
    html_files = sorted(ROOT.glob("*.html"))
    for f in html_files:
        result = process(f)
        print(f"{f.name}: {result}")


if __name__ == "__main__":
    main()
