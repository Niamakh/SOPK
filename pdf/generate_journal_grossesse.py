# -*- coding: utf-8 -*-
"""
Génère le carnet PDF "Mon journal de grossesse" (Health Corner) — 22 pages,
gratuit, à remplir à la main. Complément souvenir, ne remplace jamais le
carnet de maternité officiel ni le suivi médical.

Usage : python generate_journal_grossesse.py
Sortie : journal-grossesse-a-remplir.pdf (dans le même dossier)
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
SAGE = HexColor('#6b8f71')
MIST = HexColor('#8fa3b0')
BORDER = HexColor('#e8dfd4')
ALERT = HexColor('#b3413a')
WHITE = HexColor('#ffffff')

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
OUT_PATH = os.path.join(os.path.dirname(__file__), 'journal-grossesse-a-remplir.pdf')

MONTHS_INFO = [
    (1, 'De 4 à 8 SA environ'),
    (2, 'De 8 à 13 SA environ'),
    (3, 'De 13 à 17 SA environ'),
    (4, 'De 17 à 22 SA environ'),
    (5, 'De 22 à 26 SA environ'),
    (6, 'De 26 à 30 SA environ'),
    (7, 'De 30 à 35 SA environ'),
    (8, 'De 35 à 39 SA environ'),
    (9, "Jusqu'à la naissance"),
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


def draw_text_block(c, x, y, text, font='Helvetica', size=8.6, color=BODY, max_width=None, leading=4.4):
    if max_width is None:
        max_width = CONTENT_W
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading * mm
    return y


def frame(c, kicker, title, page_num, total=22, accent=GOLD):
    """Fond + cadre décoratif + bandeau titre, commun à toutes les pages."""
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # cadre décoratif fin
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.6)
    c.rect(9 * mm, 9 * mm, PAGE_W - 18 * mm, PAGE_H - 18 * mm, stroke=1, fill=0)
    c.setStrokeColor(accent)
    c.setLineWidth(0.4)
    c.rect(11.5 * mm, 11.5 * mm, PAGE_W - 23 * mm, PAGE_H - 23 * mm, stroke=1, fill=0)

    y = PAGE_H - 24 * mm
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(accent)
    c.drawString(MARGIN, y, kicker.upper())
    y -= 7.5 * mm
    c.setFont('Helvetica-Bold', 19)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, title)
    y -= 2 * mm
    c.setStrokeColor(accent)
    c.setLineWidth(1)
    c.line(MARGIN, y, MARGIN + 32 * mm, y)

    # pied de page
    c.setFont('Helvetica', 7)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 13 * mm, 'Mon journal de grossesse · healthcorner.fr')
    c.drawRightString(PAGE_W - MARGIN, 13 * mm, f'{page_num} / {total}')

    return y - 12 * mm  # y de départ pour le contenu


def ruled_lines(c, x, y, width, n, gap=8.5 * mm, color=BORDER):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    for i in range(n):
        yy = y - i * gap
        c.line(x, yy, x + width, yy)
    return y - (n - 1) * gap


def checkbox(c, x, y, size=4 * mm, color=GOLD):
    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    c.rect(x, y, size, size, stroke=1, fill=0)


def checklist_row(c, x, y, label, note=None, color=GOLD):
    checkbox(c, x, y - 3 * mm, color=color)
    c.setFont('Helvetica', 9)
    c.setFillColor(BODY)
    c.drawString(x + 7 * mm, y - 2.7 * mm, label)
    if note:
        c.setFont('Helvetica', 7.3)
        c.setFillColor(MUTED)
        c.drawRightString(x + CONTENT_W - 24 * mm, y - 2.5 * mm, note)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    c.line(x + CONTENT_W - 20 * mm, y - 3 * mm, x + CONTENT_W, y - 3 * mm)
    c.setFont('Helvetica', 6.4)
    c.setFillColor(MUTED)
    c.drawString(x + CONTENT_W - 20 * mm, y - 2.6 * mm, 'Date :')


def field(c, x, y, label, width):
    c.setFont('Helvetica', 6.8)
    c.setFillColor(MUTED)
    c.drawString(x, y, label.upper())
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(x, y - 5 * mm, x + width, y - 5 * mm)


def disclaimer_box(c, x, y, width, text, small=False):
    lines = wrap_text(text, 'Helvetica', 7.6 if not small else 7, width - 8 * mm)
    h = len(lines) * 3.9 * mm + 6 * mm
    c.setFillColor(SAND)
    c.roundRect(x, y - h, width, h, 2.5 * mm, stroke=0, fill=1)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    c.roundRect(x, y - h, width, h, 2.5 * mm, stroke=1, fill=0)
    yy = y - 4.5 * mm
    c.setFont('Helvetica-Oblique', 7.6 if not small else 7)
    c.setFillColor(BODY)
    for line in lines:
        c.drawString(x + 4 * mm, yy, line)
        yy -= 3.9 * mm
    return y - h


# ---------------------------------------------------------------- PAGES ----

def page_cover(c):
    c.setFillColor(HexColor('#211c19'))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.rect(12 * mm, 12 * mm, PAGE_W - 24 * mm, PAGE_H - 24 * mm, stroke=1, fill=0)
    c.setStrokeColor(ROSE)
    c.setLineWidth(0.5)
    c.rect(16 * mm, 16 * mm, PAGE_W - 32 * mm, PAGE_H - 32 * mm, stroke=1, fill=0)

    cx = PAGE_W / 2
    c.setFillColor(GOLD)
    c.setFont('Helvetica', 9)
    c.drawCentredString(cx, PAGE_H - 70 * mm, 'H E A L T H   C O R N E R')

    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 30)
    c.drawCentredString(cx, PAGE_H - 105 * mm, 'Mon journal')
    c.setFont('Helvetica-Bold', 30)
    c.drawCentredString(cx, PAGE_H - 118 * mm, 'de grossesse')

    c.setStrokeColor(ROSE)
    c.setLineWidth(1)
    c.line(cx - 24 * mm, PAGE_H - 128 * mm, cx + 24 * mm, PAGE_H - 128 * mm)

    c.setFillColor(HexColor('#cbb89a'))
    c.setFont('Helvetica-Oblique', 10.5)
    c.drawCentredString(cx, PAGE_H - 140 * mm, 'Un carnet souvenir à remplir, mois après mois')

    c.setFont('Helvetica', 9)
    c.setFillColor(HexColor('#a89684'))
    y = PAGE_H - 220 * mm
    for line in wrap_text(
        "Ce carnet est un complément personnel et souvenir. Il ne remplace ni le carnet de "
        "maternité officiel, ni le suivi médical de votre grossesse.",
        'Helvetica', 9, PAGE_W - 60 * mm
    ):
        c.drawCentredString(cx, y, line)
        y -= 4.6 * mm

    c.setFillColor(HexColor('#7d6f61'))
    c.setFont('Helvetica', 8)
    c.drawCentredString(cx, 20 * mm, 'healthcorner.fr')
    c.showPage()


def page_intro(c):
    y = frame(c, 'Bienvenue', 'Comment utiliser ce journal', 2)
    y = draw_text_block(c, MARGIN, y,
        "Ce carnet vous accompagne, mois après mois, pour garder une trace personnelle de votre "
        "grossesse : ressentis, symptômes, rendez-vous, prénoms envisagés... Remplissez-le à votre "
        "rythme, à la main, sans pression : il n'y a pas de bonne façon de le tenir.",
        size=9.4, leading=5.2)
    y -= 6 * mm

    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'CE QU\u2019IL CONTIENT')
    y -= 7 * mm
    items = [
        'Le test positif — votre annonce',
        'Le suivi médical officiel — une checklist des rendez-vous prévus par la loi',
        'Mes rendez-vous — un tableau à remplir au fil du suivi',
        '9 pages « un mois, une page » — humeur, poids, symptômes, photo, mot au bébé',
        '3 pages échographies — pour coller vos photos et noter vos souvenirs',
        'La valise de maternité, le projet de naissance, les prénoms envisagés',
        'Mon corps qui change — une page de suivi des sensations',
        'Une dernière page souvenir',
    ]
    for item in items:
        checkbox(c, MARGIN, y - 3 * mm, size=2.6 * mm, color=ROSE)
        c.setFont('Helvetica', 8.8)
        c.setFillColor(BODY)
        c.drawString(MARGIN + 6 * mm, y - 2.6 * mm, item)
        y -= 6.2 * mm

    y -= 8 * mm
    disclaimer_box(c, MARGIN, y, CONTENT_W,
        "AVERTISSEMENT — Ce journal est un complément personnel et souvenir, pensé par la rédaction "
        "de Health Corner. Il n'est pas rédigé ni validé par des professionnels de santé et ne "
        "remplace en aucun cas le carnet de maternité officiel (CERFA 17595*01) ni le suivi médical "
        "réalisé par votre sage-femme ou votre médecin. En cas de doute sur votre grossesse, "
        "consultez toujours un professionnel de santé.")
    c.showPage()


def page_test_positif(c):
    y = frame(c, 'Le début de l\u2019histoire', 'Le test positif', 3)
    y = draw_text_block(c, MARGIN, y,
        "Le moment où vous avez découvert que vous étiez enceinte. Un instant souvent unique, "
        "à garder en mémoire.", size=9, leading=5)
    y -= 8 * mm

    field(c, MARGIN, y, 'Date du test', 60 * mm)
    field(c, MARGIN + 70 * mm, y, 'Type de test (urinaire / sanguin)', CONTENT_W - 70 * mm)
    y -= 16 * mm

    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'MON RESSENTI À CE MOMENT-LÀ')
    y -= 8 * mm
    y = ruled_lines(c, MARGIN, y, CONTENT_W, 6)
    y -= 14 * mm

    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, '\u00c0 QUI L\u2019AI-JE ANNONC\u00c9 EN PREMIER ? COMMENT ?')
    y -= 8 * mm
    y = ruled_lines(c, MARGIN, y, CONTENT_W, 6)
    y -= 14 * mm

    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'CE QUE J\u2019AI RESSENTI PHYSIQUEMENT CETTE SEMAINE-L\u00c0')
    y -= 8 * mm
    ruled_lines(c, MARGIN, y, CONTENT_W, 4)
    c.showPage()


def page_suivi_medical(c):
    y = frame(c, 'Rep\u00e8res officiels', 'Suivi m\u00e9dical officiel', 4)
    y = draw_text_block(c, MARGIN, y,
        "La checklist des rendez-vous et examens prévus par la réglementation française (Ameli, "
        "service-public.gouv.fr). Cochez au fur et à mesure — cette page ne remplace pas votre carnet "
        "de maternité officiel, qui reste la référence.", size=8.8, leading=4.8)
    y -= 10 * mm

    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'LES 7 EXAMENS PR\u00c9NATAUX OBLIGATOIRES')
    y -= 9 * mm
    exams = [
        '1er examen prénatal (avant 14 SA)',
        '2e examen (vers 4 mois)',
        '3e examen (vers 5 mois)',
        '4e examen (vers 6 mois)',
        '5e examen (vers 7 mois)',
        '6e examen (vers 8 mois)',
        '7e examen (vers 9 mois)',
    ]
    for exam in exams:
        checklist_row(c, MARGIN, y, exam)
        y -= 8.4 * mm

    y -= 6 * mm
    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'LES 3 \u00c9CHOGRAPHIES + AUTRES REP\u00c8RES')
    y -= 9 * mm
    others = [
        'Déclaration de grossesse (avant la fin de la 14e semaine)',
        'Échographie du 1er trimestre (11 SA à 13 SA + 6 j)',
        'Échographie du 2e trimestre (vers 22 SA)',
        'Échographie du 3e trimestre (vers 32 SA)',
        'HGPO — dépistage diabète gestationnel (24-28 SA)',
        'Consultation anesthésiste (vers le 8e mois)',
        'Entretien prénatal précoce (facultatif, recommandé)',
    ]
    for item in others:
        checklist_row(c, MARGIN, y, item)
        y -= 8.4 * mm

    y -= 6 * mm
    disclaimer_box(c, MARGIN, y, CONTENT_W,
        "Ces repères sont donnés à titre indicatif et sourcés auprès d'Ameli et service-public.gouv.fr. "
        "Seul votre professionnel de santé référent adapte ce calendrier à votre situation.")
    c.showPage()


def page_rendez_vous(c):
    y = frame(c, 'Suivi personnel', 'Mes rendez-vous', 5)
    y = draw_text_block(c, MARGIN, y,
        "Un tableau libre pour noter vos rendez-vous au fil de la grossesse : sage-femme, "
        "gynécologue, échographiste, sophrologue...", size=8.8, leading=4.8)
    y -= 10 * mm

    col1, col2, col3 = 28 * mm, 45 * mm, CONTENT_W - 28 * mm - 45 * mm
    headers = ['Date', 'Professionnel / motif', 'Notes']
    c.setFillColor(SAND)
    c.rect(MARGIN, y - 7 * mm, CONTENT_W, 7 * mm, stroke=0, fill=1)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(INK)
    x = MARGIN
    for i, h in enumerate(headers):
        c.drawString(x + 2.5 * mm, y - 5 * mm, h)
        x += [col1, col2, col3][i]
    y -= 7 * mm
    row_h = 12 * mm
    for i in range(15):
        if i % 2 == 0:
            c.setFillColor(SAND2)
            c.rect(MARGIN, y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
        y -= row_h
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    total_h = 15 * row_h
    top = y + total_h
    for i in range(16):
        yy = top - i * row_h
        c.line(MARGIN, yy, MARGIN + CONTENT_W, yy)
    x = MARGIN
    for w in [col1, col2]:
        x += w
        c.line(x, top, x, top - total_h)
    c.rect(MARGIN, top - total_h, CONTENT_W, total_h, stroke=1, fill=0)
    c.showPage()


def page_month(c, num, info, page_num):
    y = frame(c, f'Mois {num}', f'Mois {num} de grossesse', page_num, accent=ROSE)
    c.setFont('Helvetica-Oblique', 8.6)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, y + 4 * mm, info)

    col_w = CONTENT_W / 2 - 4 * mm
    left_x = MARGIN
    right_x = MARGIN + CONTENT_W / 2 + 4 * mm

    ly = y - 6 * mm
    field(c, left_x, ly, 'Date de ce mois', col_w * 0.48)
    field(c, left_x + col_w * 0.55, ly, 'Poids', col_w * 0.45)
    ly -= 12 * mm
    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(left_x, ly, 'MON HUMEUR CE MOIS-CI (entourez)')
    ly -= 8 * mm
    moods = ['Joyeuse', 'Calme', 'Fatiguée', 'Stressée', 'Émue', 'Anxieuse']
    mx = left_x
    c.setFont('Helvetica', 7.6)
    for m in moods:
        w = stringWidth(m, 'Helvetica', 7.6)
        c.setStrokeColor(ROSE)
        c.setLineWidth(0.6)
        c.roundRect(mx - 1.5 * mm, ly - 2.6 * mm, w + 3 * mm, 5.4 * mm, 2.6 * mm, stroke=1, fill=0)
        c.setFillColor(BODY)
        c.drawString(mx, ly - 1 * mm, m)
        mx += w + 7 * mm
    ly -= 11 * mm

    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(left_x, ly, 'MES SYMPT\u00d4MES / SENSATIONS')
    ly -= 7 * mm
    ly = ruled_lines(c, left_x, ly, col_w, 5, gap=7.5 * mm)
    ly -= 12 * mm

    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(left_x, ly, 'UN PETIT MOT AU B\u00c9B\u00c9')
    ly -= 7 * mm
    ruled_lines(c, left_x, ly, col_w, 5, gap=7.5 * mm)

    # colonne droite : cadre photo + envies
    ry = y - 6 * mm
    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(right_x, ry, 'PHOTO DE MON VENTRE')
    ry -= 6 * mm
    photo_h = 62 * mm
    c.setStrokeColor(BORDER)
    c.setDash(2, 2)
    c.setLineWidth(0.7)
    c.rect(right_x, ry - photo_h, col_w, photo_h, stroke=1, fill=0)
    c.setDash()
    c.setFont('Helvetica', 7.5)
    c.setFillColor(MUTED)
    c.drawCentredString(right_x + col_w / 2, ry - photo_h / 2, '(collez votre photo ici)')
    ry -= photo_h + 10 * mm

    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(right_x, ry, 'MES PETITES ENVIES / AVERSIONS')
    ry -= 7 * mm
    ruled_lines(c, right_x, ry, col_w, 5, gap=7.5 * mm)

    # bandeau plein-largeur en bas de page
    bottom_y = 46 * mm
    c.setFont('Helvetica-Bold', 8.4)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, bottom_y, 'CE QUE JE VEUX RETENIR DE CE MOIS')
    bottom_y -= 7 * mm
    ruled_lines(c, MARGIN, bottom_y, CONTENT_W, 3, gap=7.5 * mm)

    c.showPage()


def page_echo(c, title, kicker, page_num):
    y = frame(c, kicker, title, page_num, accent=MIST)
    photo_w, photo_h = CONTENT_W, 95 * mm
    c.setStrokeColor(BORDER)
    c.setDash(2, 2)
    c.setLineWidth(0.8)
    c.rect(MARGIN, y - photo_h, photo_w, photo_h, stroke=1, fill=0)
    c.setDash()
    c.setFont('Helvetica', 8)
    c.setFillColor(MUTED)
    c.drawCentredString(MARGIN + photo_w / 2, y - photo_h / 2, '(collez votre photo d\u2019échographie ici)')
    y -= photo_h + 10 * mm

    col_w = CONTENT_W / 2 - 4 * mm
    field(c, MARGIN, y, 'Date de l\u2019échographie', col_w)
    field(c, MARGIN + CONTENT_W / 2 + 4 * mm, y, 'Terme (SA)', col_w)
    y -= 14 * mm

    c.setFont('Helvetica-Bold', 8.6)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'CE QUE NOUS A DIT LE PROFESSIONNEL')
    y -= 7.5 * mm
    y = ruled_lines(c, MARGIN, y, CONTENT_W, 6)
    y -= 14 * mm
    c.setFont('Helvetica-Bold', 8.6)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'MES \u00c9MOTIONS DEVANT L\u2019\u00c9CRAN')
    y -= 7.5 * mm
    ruled_lines(c, MARGIN, y, CONTENT_W, 4)
    c.showPage()


def page_valise(c):
    y = frame(c, 'Pr\u00e9paration', 'La valise de maternit\u00e9', 18, accent=SAGE)
    y = draw_text_block(c, MARGIN, y,
        "Une checklist indicative à adapter selon les conseils de votre maternité — chaque "
        "établissement peut avoir sa propre liste.", size=8.8, leading=4.8)
    y -= 8 * mm

    cols = [
        ('Pour moi', ['Chemises de nuit / pyjamas ouverts', 'Soutiens-gorge d\u2019allaitement', 'Serviettes de maternité', 'Nécessaire de toilette', 'Sous-vêtements jetables', 'Tenue de sortie', 'Chaussons / claquettes', 'Chargeur de téléphone']),
        ('Pour le bébé', ['Bodys et pyjamas (plusieurs tailles)', 'Turbulette / couverture', 'Bonnet et chaussons', 'Couches nouveau-né', 'Coton et liniment', 'Tenue de sortie de maternité', 'Siège auto (déjà installé)']),
        ('Papiers & administratif', ['Carnet de maternité', 'Carte Vitale + mutuelle', 'Pièce d\u2019identité', 'Dossier médical / résultats d\u2019examens', 'Projet de naissance (si rédigé)', 'Attestation de choix du prénom (si prévue)']),
    ]
    col_w = CONTENT_W / 3 - 4 * mm
    x = MARGIN
    for title, items in cols:
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(GOLD)
        c.drawString(x, y, title.upper())
        yy = y - 8 * mm
        for item in items:
            checkbox(c, x, yy - 2.6 * mm, size=3 * mm, color=SAGE)
            c.setFont('Helvetica', 7.6)
            c.setFillColor(BODY)
            for j, line in enumerate(wrap_text(item, 'Helvetica', 7.6, col_w - 6 * mm)):
                c.drawString(x + 5.5 * mm, yy - 2.2 * mm - j * 3.6 * mm, line)
            yy -= 6 * mm + (len(wrap_text(item, 'Helvetica', 7.6, col_w - 6 * mm)) - 1) * 3.6 * mm
        x += col_w + 6 * mm
    c.showPage()


def page_projet_naissance(c):
    y = frame(c, 'Mes souhaits', 'Mon projet de naissance', 19, accent=ROSE)
    y = draw_text_block(c, MARGIN, y,
        "Un espace pour noter vos souhaits pour le jour J — à partager avec l\u2019équipe qui vous "
        "accompagnera. Ces souhaits restent indicatifs et peuvent être adaptés en fonction de la "
        "situation médicale du moment.", size=8.8, leading=4.8)
    y -= 8 * mm

    sections = [
        'Qui je souhaite avoir à mes côtés',
        'Ma position souhaitée pour l\u2019accouchement',
        'Gestion de la douleur (péridurale, méthodes alternatives...)',
        'Souhaits concernant le peau à peau et le premier allaitement',
        'Souhaits particuliers (musique, lumière, ambiance...)',
    ]
    for s in sections:
        c.setFont('Helvetica-Bold', 8.6)
        c.setFillColor(GOLD)
        c.drawString(MARGIN, y, s.upper())
        y -= 7 * mm
        y = ruled_lines(c, MARGIN, y, CONTENT_W, 3, gap=7.2 * mm)
        y -= 9 * mm
    c.showPage()


def page_prenoms(c):
    y = frame(c, 'Le choix du pr\u00e9nom', 'Pr\u00e9noms envisag\u00e9s', 20, accent=MIST)
    col_w = CONTENT_W / 2 - 5 * mm
    for label, x in [('Prénoms féminins', MARGIN), ('Prénoms masculins', MARGIN + CONTENT_W / 2 + 5 * mm)]:
        c.setFont('Helvetica-Bold', 9.5)
        c.setFillColor(GOLD)
        c.drawString(x, y, label.upper())
        yy = y - 9 * mm
        for i in range(10):
            c.setStrokeColor(BORDER)
            c.setLineWidth(0.4)
            c.line(x, yy, x + col_w, yy)
            yy -= 9 * mm
    y -= 100 * mm
    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'NOTRE CHOIX FINAL')
    y -= 10 * mm
    field(c, MARGIN, y, 'Prénom(s)', col_w)
    field(c, MARGIN + CONTENT_W / 2 + 5 * mm, y, 'Signification / pourquoi ce choix', col_w)
    c.showPage()


def page_corps(c):
    y = frame(c, 'Suivi personnel', 'Mon corps qui change', 21, accent=SAGE)
    y = draw_text_block(c, MARGIN, y,
        "Une page libre pour noter les sensations physiques qui vous marquent, sans obligation "
        "ni comparaison — chaque grossesse est différente.", size=8.8, leading=4.8)
    y -= 8 * mm
    prompts = [
        'Ce qui a changé dans mon corps que je n\u2019attendais pas',
        'Comment j\u2019ai vécu les nausées / la fatigue / les mouvements du bébé',
        'Ce qui m\u2019a fait du bien (sommeil, alimentation, mouvement, repos...)',
        'Ce que j\u2019aimerais me rappeler de cette période',
    ]
    for p in prompts:
        c.setFont('Helvetica-Bold', 8.6)
        c.setFillColor(GOLD)
        for j, line in enumerate(wrap_text(p.upper(), 'Helvetica-Bold', 8.6, CONTENT_W)):
            c.drawString(MARGIN, y - j * 4 * mm, line)
        y -= 4 * mm * len(wrap_text(p.upper(), 'Helvetica-Bold', 8.6, CONTENT_W)) + 4 * mm
        y = ruled_lines(c, MARGIN, y, CONTENT_W, 3, gap=7.2 * mm)
        y -= 9 * mm
    c.showPage()


def page_souvenir(c):
    y = frame(c, 'Pour finir', 'Page souvenir', 22, accent=GOLD)
    y = draw_text_block(c, MARGIN, y,
        "Le dernier mot de ce carnet, à écrire quand vous le souhaitez : avant, pendant ou après "
        "la naissance.", size=9, leading=5)
    y -= 8 * mm
    field(c, MARGIN, y, 'Date de naissance', 60 * mm)
    field(c, MARGIN + 70 * mm, y, 'Prénom', 50 * mm)
    field(c, MARGIN + 130 * mm, y, 'Poids / Taille', CONTENT_W - 130 * mm)
    y -= 16 * mm

    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, y, 'CE QUE J\u2019AI ENVIE DE ME RAPPELER DE CETTE GROSSESSE')
    y -= 8 * mm
    y = ruled_lines(c, MARGIN, y, CONTENT_W, 8)
    y -= 18 * mm

    disclaimer_box(c, MARGIN, y, CONTENT_W,
        "RAPPEL — Ce journal est un complément personnel et souvenir. Il ne remplace ni le carnet "
        "de maternité officiel, ni le suivi médical par un professionnel de santé. Merci de l\u2019avoir "
        "rempli avec Health Corner.")
    c.showPage()


def main():
    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    c.setTitle('Mon journal de grossesse — Health Corner')
    c.setAuthor('Health Corner')

    page_cover(c)                 # 1
    page_intro(c)                 # 2
    page_test_positif(c)          # 3
    page_suivi_medical(c)         # 4
    page_rendez_vous(c)           # 5
    for i, (num, info) in enumerate(MONTHS_INFO):  # 6-14
        page_month(c, num, info, 6 + i)
    page_echo(c, "Échographie du 1er trimestre", "11 à 13 SA + 6 j", 15)   # 15
    page_echo(c, "Échographie du 2e trimestre", "vers 22 SA", 16)          # 16
    page_echo(c, "Échographie du 3e trimestre", "vers 32 SA", 17)          # 17
    page_valise(c)                 # 18
    page_projet_naissance(c)       # 19
    page_prenoms(c)                # 20
    page_corps(c)                  # 21
    page_souvenir(c)               # 22

    c.save()
    print('PDF généré :', OUT_PATH, '—', 'pages: 22')


if __name__ == '__main__':
    main()
