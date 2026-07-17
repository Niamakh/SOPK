# -*- coding: utf-8 -*-
"""
Génère la fiche PDF "Comprendre mon taux de bêta-hCG" (Health Corner) — 2 pages.

Usage : python generate_fiche_hcg.py
Sortie : fiche-taux-hcg-grossesse.pdf (dans le même dossier)
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

CREAM = HexColor('#fdfaf6')
SAND = HexColor('#f5ede4')
SAND2 = HexColor('#f8f4ee')
GOLD = HexColor('#b8860b')
ROSE = HexColor('#c4868c')
INK = HexColor('#2c2420')
BODY = HexColor('#5c524a')
MUTED = HexColor('#9c8e82')
BORDER = HexColor('#e8dfd4')
ALERT = HexColor('#b3413a')
ALERT_BG = HexColor('#fbeceb')
WHITE = HexColor('#ffffff')

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
OUT_PATH = os.path.join(os.path.dirname(__file__), 'fiche-taux-hcg-grossesse.pdf')

# Tableau 2 — Guide des analyses spécialisées Cerba (valeurs en UI/l, semaines d'aménorrhée)
CERBA_TABLE = [
    ('4–5', '200 à 8 000'), ('5–6', '4 000 à 90 000'), ('6–7', '8 000 à 170 000'),
    ('7–8', '12 000 à 230 000'), ('8–9', '16 000 à 256 000'), ('9–10', '44 000 à 260 000'),
    ('10–11', '34 000 à 240 000'), ('11–12', '30 000 à 220 000'), ('12–13', '24 000 à 168 000'),
    ('13–15', '16 000 à 144 000'), ('15–17', '8 000 à 120 000'), ('17–19', '8 000 à 70 000'),
    ('19–21', '8 000 à 44 000'), ('21–23', '8 000 à 36 000'), ('23–25', '8 000 à 34 000'),
    ('25–27', '6 000 à 38 000'), ('27–29', '10 000 à 46 000'), ('29–31', '16 000 à 48 000'),
    ('31–33', '22 000 à 44 000'), ('33–35', '18 000 à 42 000'), ('35–40', '12 000 à 34 000'),
]


def wrap_text(text, font, size, max_width):
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(c, x, y, text, font='Helvetica', size=8.8, color=BODY, max_width=None, leading=4.4):
    if max_width is None:
        max_width = CONTENT_W
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading * mm
    return y


def frame(c, kicker, title, page_num, total=2, accent=GOLD):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.6)
    c.rect(9 * mm, 9 * mm, PAGE_W - 18 * mm, PAGE_H - 18 * mm, stroke=1, fill=0)
    c.setStrokeColor(accent)
    c.setLineWidth(0.4)
    c.rect(11.5 * mm, 11.5 * mm, PAGE_W - 23 * mm, PAGE_H - 23 * mm, stroke=1, fill=0)

    y = PAGE_H - 23 * mm
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(accent)
    c.drawString(MARGIN, y, kicker.upper())
    y -= 7 * mm
    c.setFont('Helvetica-Bold', 17)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, title)
    y -= 2 * mm
    c.setStrokeColor(accent)
    c.setLineWidth(1)
    c.line(MARGIN, y, MARGIN + 32 * mm, y)

    c.setFont('Helvetica', 7)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 13 * mm, 'Comprendre mon taux de b\u00eata-hCG \u00b7 healthcorner.fr')
    c.drawRightString(PAGE_W - MARGIN, 13 * mm, f'{page_num} / {total}')
    return y - 11 * mm


def box(c, x, y, width, height, fill=SAND, stroke=BORDER, radius=3 * mm):
    c.setFillColor(fill)
    c.roundRect(x, y - height, width, height, radius, stroke=0, fill=1)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.5)
        c.roundRect(x, y - height, width, height, radius, stroke=1, fill=0)


def page_1(c):
    y = frame(c, 'Fiche pratique', 'Comprendre mon taux de b\u00eata-hCG', 1)

    y = draw_text_block(c, MARGIN, y,
        "Cette fiche vous aide à comprendre les grandes lignes d'un dosage de bêta-hCG. Elle ne "
        "remplace jamais l'interprétation de votre médecin ou de votre sage-femme, seuls compétents "
        "pour analyser votre résultat dans votre contexte clinique.",
        size=8.6, leading=4.3)
    y -= 5 * mm

    # Encadré seuils
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'LES SEUILS DE R\u00c9F\u00c9RENCE')
    y -= 8 * mm
    seuils_h = 24 * mm
    box(c, MARGIN, y, CONTENT_W, seuils_h, fill=SAND)
    col_w = CONTENT_W / 3
    labels = [
        ('< 5 UI/l', 'N\u00e9gatif', BODY),
        ('> 5 UI/l', 'Positif', GOLD),
        ('5 \u00e0 25 UI/l', 'Zone grise \u2014 recontr\u00f4le \u00e0 48 h', ALERT),
    ]
    for i, (val, lab, color) in enumerate(labels):
        cx = MARGIN + col_w * i + col_w / 2
        c.setFont('Helvetica-Bold', 13)
        c.setFillColor(color)
        c.drawCentredString(cx, y - 10 * mm, val)
        c.setFont('Helvetica', 7.6)
        c.setFillColor(BODY)
        for j, line in enumerate(wrap_text(lab, 'Helvetica', 7.6, col_w - 6 * mm)):
            c.drawCentredString(cx, y - 16 * mm - j * 3.4 * mm, line)
        if i > 0:
            c.setStrokeColor(BORDER)
            c.setLineWidth(0.4)
            c.line(MARGIN + col_w * i, y - seuils_h + 3 * mm, MARGIN + col_w * i, y - 3 * mm)
    y -= seuils_h + 8 * mm

    c.setFont('Helvetica-Oblique', 7.6)
    c.setFillColor(MUTED)
    y = draw_text_block(c, MARGIN, y,
        "Le taux de bêta-hCG double généralement toutes les 48 à 72 heures en tout début de "
        "grossesse et atteint un pic entre 8 et 11 SA avant de redescendre en plateau.",
        font='Helvetica-Oblique', size=7.8, leading=3.8)
    y -= 6 * mm

    # Tableau indicatif
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'TABLEAU INDICATIF DU TAUX D\u2019hCG PAR SA')
    y -= 5 * mm
    c.setFont('Helvetica', 7)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, y, '(Guide des analyses sp\u00e9cialis\u00e9es Cerba \u2014 tableau 2, valeurs en UI/l)')
    y -= 7 * mm

    # bandeau rouge d'avertissement
    warn_text = ("VALEURS INDICATIVES \u2014 elles varient fortement selon les laboratoires et les femmes "
                 "\u2014 ne remplacent pas l'avis m\u00e9dical.")
    warn_lines = wrap_text(warn_text, 'Helvetica-Bold', 8, CONTENT_W - 8 * mm)
    warn_h = len(warn_lines) * 3.8 * mm + 4 * mm
    box(c, MARGIN, y, CONTENT_W, warn_h, fill=ALERT_BG, stroke=ALERT)
    yy = y - 4 * mm
    for line in warn_lines:
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(ALERT)
        c.drawCentredString(PAGE_W / 2, yy, line)
        yy -= 3.8 * mm
    y -= warn_h + 6 * mm

    # Table à deux colonnes (comme le tableau Cerba original)
    half = (len(CERBA_TABLE) + 1) // 2
    left_rows = CERBA_TABLE[:half]
    right_rows = CERBA_TABLE[half:]
    row_h = 5.6 * mm
    table_h = max(len(left_rows), len(right_rows)) * row_h + row_h
    col_gap = 6 * mm
    tcol_w = (CONTENT_W - col_gap) / 2

    def draw_mini_table(x, rows, top_y):
        c.setFillColor(SAND)
        c.rect(x, top_y - row_h, tcol_w, row_h, stroke=0, fill=1)
        c.setFont('Helvetica-Bold', 7.4)
        c.setFillColor(INK)
        c.drawString(x + 2.5 * mm, top_y - row_h + 1.6 * mm, 'SA')
        c.drawString(x + tcol_w * 0.32, top_y - row_h + 1.6 * mm, 'Taux (UI/l)')
        yy = top_y - row_h
        for i, (sa, val) in enumerate(rows):
            yy -= row_h
            if i % 2 == 0:
                c.setFillColor(SAND2)
                c.rect(x, yy, tcol_w, row_h, stroke=0, fill=1)
            c.setFont('Helvetica', 7.4)
            c.setFillColor(BODY)
            c.drawString(x + 2.5 * mm, yy + 1.6 * mm, sa + ' SA')
            c.drawString(x + tcol_w * 0.32, yy + 1.6 * mm, val)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        c.rect(x, yy, tcol_w, top_y - yy, stroke=1, fill=0)

    draw_mini_table(MARGIN, left_rows, y)
    draw_mini_table(MARGIN + tcol_w + col_gap, right_rows, y)
    y -= table_h + 8 * mm

    c.setFont('Helvetica', 7.4)
    c.setFillColor(MUTED)
    y = draw_text_block(c, MARGIN, y,
        "SA = semaines d'aménorrhée, comptées depuis le premier jour des dernières règles.",
        font='Helvetica-Oblique', size=7.4, leading=3.6)

    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PAGE_W / 2, 15 * mm, 'healthcorner.fr')
    c.showPage()


def page_2(c):
    y = frame(c, 'Ce qu\u2019il faut savoir', 'Ce que le taux ne dit PAS', 2, accent=ROSE)

    items = [
        ('Il ne date pas précisément la grossesse', 'La fourchette de valeurs possibles pour une même semaine est immense (parfois de 1 à 10). Seule l\u2019échographie de datation (11 à 13 SA + 6 j) permet de dater précisément une grossesse.'),
        ('Il n\u2019indique pas, à lui seul, une grossesse gémellaire', 'Un taux élevé peut l\u2019évoquer, mais seule l\u2019échographie confirme le nombre d\u2019embryons.'),
        ('Il ne prédit pas, à lui seul, une fausse couche', 'C\u2019est l\u2019évolution du taux sur plusieurs dosages — et non une valeur isolée — qui oriente le diagnostic, en complément de l\u2019échographie.'),
        ('Un taux isolé n\u2019a pas de sens sans comparaison', 'C\u2019est la progression entre deux prélèvements, en général espacés de 48 heures, qui est cliniquement informative.'),
    ]
    for title, body in items:
        c.setFont('Helvetica-Bold', 9.3)
        c.setFillColor(INK)
        for j, line in enumerate(wrap_text('\u2717 ' + title, 'Helvetica-Bold', 9.3, CONTENT_W)):
            c.drawString(MARGIN, y - j * 4.2 * mm, line)
        y -= 4.2 * mm * len(wrap_text('\u2717 ' + title, 'Helvetica-Bold', 9.3, CONTENT_W)) + 1.5 * mm
        y = draw_text_block(c, MARGIN + 4 * mm, y, body, size=8.3, leading=4, max_width=CONTENT_W - 4 * mm)
        y -= 5 * mm

    y -= 2 * mm
    # Encadré urgence
    urgence_text = ("CONSULTER EN URGENCE si vous ressentez des douleurs pelviennes (surtout "
                     "unilatérales) associées à un saignement, avec ou sans malaise ou fièvre : ces "
                     "signes peuvent évoquer une grossesse extra-utérine ou une fausse couche.")
    lines = wrap_text(urgence_text, 'Helvetica-Bold', 8.6, CONTENT_W - 10 * mm)
    h = len(lines) * 4 * mm + 8 * mm
    box(c, MARGIN, y, CONTENT_W, h, fill=ALERT_BG, stroke=ALERT)
    yy = y - 6 * mm
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(ALERT)
    c.drawString(MARGIN + 5 * mm, yy, '\u26a0 SIGNAUX D\u2019ALERTE')
    yy -= 5.5 * mm
    for line in lines:
        c.setFont('Helvetica-Bold', 8.6)
        c.setFillColor(ALERT)
        c.drawString(MARGIN + 5 * mm, yy, line)
        yy -= 4 * mm
    y -= h + 8 * mm

    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'AVERTISSEMENT M\u00c9DICAL')
    y -= 6 * mm
    disclaimer = (
        "Cette fiche est un outil d'information générale, publié par la rédaction de Health Corner "
        "à partir de sources médicales de référence (Cerba, Ameli). Elle ne fournit aucune "
        "interprétation individualisée de votre résultat et ne remplace jamais l'avis de votre "
        "médecin ou de votre sage-femme, seuls compétents pour analyser un dosage dans son "
        "contexte clinique. En cas de doute sur votre grossesse, consultez un professionnel de santé."
    )
    c.setFont('Helvetica', 8.4)
    c.setFillColor(BODY)
    for line in wrap_text(disclaimer, 'Helvetica', 8.4, CONTENT_W):
        c.drawString(MARGIN, y, line)
        y -= 4.4 * mm

    y -= 8 * mm
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, y, 'SOURCES')
    y -= 5 * mm
    c.setFont('Helvetica', 7.6)
    c.setFillColor(MUTED)
    for line in [
        "Laboratoire Cerba \u2014 Guide des analyses spécialisées, fiche hCG (documents.lab-cerba.com/files/FR/0268F.pdf)",
        "Ameli \u2014 Suivi de la grossesse (ameli.fr)",
        "Ameli \u2014 Grossesse extra-utérine, Fausse couche (ameli.fr)",
    ]:
        c.drawString(MARGIN, y, line)
        y -= 4 * mm

    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PAGE_W / 2, 15 * mm, 'healthcorner.fr')
    c.showPage()


def main():
    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    c.setTitle('Comprendre mon taux de b\u00eata-hCG \u2014 Health Corner')
    c.setAuthor('Health Corner')
    page_1(c)
    page_2(c)
    c.save()
    print('PDF généré :', OUT_PATH)


if __name__ == '__main__':
    main()
