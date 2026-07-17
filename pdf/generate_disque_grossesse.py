# -*- coding: utf-8 -*-
"""
Génère le PDF "Disque de grossesse à imprimer" (Health Corner).

Page 1 : deux disques concentriques à découper
  - Disque calendrier (fixe, plus grand) : jours de l'année (365 j), 12 mois.
  - Disque des semaines (mobile, plus petit) : SA 0 à 42, avec repères
    (déclaration 14 SA, écho T1 11-13SA+6j, écho T2 22 SA, écho T3 32 SA,
    terme 41 SA, terme dépassé 42 SA).
  Les deux disques utilisent la même échelle (360° / 365 jours) : une fois
  assemblés avec une attache parisienne au centre et la flèche "SA 0"
  alignée sur la date des dernières règles, chaque repère du disque des
  semaines indique, sur le disque calendrier situé dessous, la date
  calendaire correspondante.

Page 2 : notice d'utilisation, règle de Naegele, tableau SA/SG,
  disclaimer médical.

Usage : python generate_disque_grossesse.py
Sortie : disque-grossesse-a-imprimer.pdf (dans le même dossier)
"""
import math
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

# ---- Palette Health Corner ----
CREAM = HexColor('#fdfaf6')
SAND = HexColor('#f5ede4')
GOLD = HexColor('#b8860b')
ROSE = HexColor('#c4868c')
INK = HexColor('#2c2420')
BODY = HexColor('#5c524a')
MUTED = HexColor('#9c8e82')
SAGE = HexColor('#6b8f71')
MIST = HexColor('#8fa3b0')
BORDER = HexColor('#e8dfd4')
ALERT = HexColor('#b3413a')

PAGE_W, PAGE_H = A4
OUT_PATH = os.path.join(os.path.dirname(__file__), 'disque-grossesse-a-imprimer.pdf')

MONTHS = ['JANV', 'FÉVR', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUIL', 'AOÛT', 'SEPT', 'OCT', 'NOV', 'DÉC']
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DEG_PER_DAY = 360.0 / 365.0

MILESTONES = [
    (98, '14 SA', 'Déclaration', GOLD),
    (77, '11 SA', None, ROSE),
    (97, '13 SA+6', 'Écho T1', ROSE),
    (154, '22 SA', 'Écho T2', SAGE),
    (224, '32 SA', 'Écho T3', MIST),
    (287, '41 SA', 'Terme', ALERT),
    (294, '42 SA', 'Terme dépassé', INK),
]


def polar(cx, cy, r, clock_deg):
    """Point sur un cercle. clock_deg=0 -> 12h (haut), sens horaire."""
    a = math.radians(90 - clock_deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def draw_dashed_circle(c, cx, cy, r, color, dash_len=3, gap_len=2.2, width=0.7):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    circumference = 2 * math.pi * r
    n_dashes = max(int(circumference / (dash_len + gap_len)), 8)
    step = 360.0 / n_dashes
    dash_deg = step * (dash_len / (dash_len + gap_len))
    a = 0.0
    while a < 360.0:
        p1 = polar(cx, cy, r, a)
        p2 = polar(cx, cy, r, a + dash_deg)
        # petite ligne droite (arc approximé par corde, dashes fins donc négligeable)
        c.line(p1[0], p1[1], p2[0], p2[1])
        a += step
    c.restoreState()


def draw_radial_text(c, cx, cy, r, clock_deg, text, font='Helvetica', size=5.5, color=INK, bold=False):
    if bold:
        font = 'Helvetica-Bold'
    c.saveState()
    c.translate(cx, cy)
    c.rotate(-clock_deg)
    c.setFillColor(color)
    c.setFont(font, size)
    w = stringWidth(text, font, size)
    c.drawString(-w / 2.0, r, text)
    c.restoreState()


def draw_radial_tick(c, cx, cy, r_in, r_out, clock_deg, color, width=0.5):
    p1 = polar(cx, cy, r_in, clock_deg)
    p2 = polar(cx, cy, r_out, clock_deg)
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(p1[0], p1[1], p2[0], p2[1])
    c.restoreState()


def draw_calendar_disc(c, cx, cy, r):
    """Disque calendrier fixe : 365 jours, 12 mois."""
    c.setFillColor(CREAM)
    c.setStrokeColor(BORDER)
    c.circle(cx, cy, r, stroke=1, fill=1)

    day = 0
    for m_idx, ndays in enumerate(MONTH_DAYS):
        start_deg = day * DEG_PER_DAY
        end_deg = (day + ndays) * DEG_PER_DAY
        mid_deg = (start_deg + end_deg) / 2.0

        # alternance de fond très légère entre mois
        if m_idx % 2 == 0:
            p = c.beginPath()
            p.moveTo(cx, cy)
            steps = 12
            for i in range(steps + 1):
                dd = start_deg + (end_deg - start_deg) * i / steps
                x, y = polar(cx, cy, r, dd)
                p.lineTo(x, y)
            p.close()
            c.setFillColor(HexColor('#f6efe6'))
            c.drawPath(p, fill=1, stroke=0)

        # ticks tous les jours (fins), tous les 5 jours (moyens)
        for d in range(ndays):
            deg = (day + d) * DEG_PER_DAY
            if d % 5 == 0:
                draw_radial_tick(c, cx, cy, r - 3.2 * mm, r, deg, MUTED, width=0.6)
                if d % 10 == 0 and d != 0:
                    draw_radial_text(c, cx, cy, r - 5.6 * mm, deg, str(d), size=4.3, color=MUTED)
            else:
                draw_radial_tick(c, cx, cy, r - 1.6 * mm, r, deg, HexColor('#d8cdbf'), width=0.3)

        # séparateur de mois (trait plus marqué)
        draw_radial_tick(c, cx, cy, r - 6 * mm, r, start_deg, GOLD, width=0.9)
        # nom du mois
        draw_radial_text(c, cx, cy, r - 10.5 * mm, mid_deg, MONTHS[m_idx], size=6.4, color=INK, bold=True)

        day += ndays

    draw_dashed_circle(c, cx, cy, r + 2.2 * mm, ROSE)


def draw_week_disc(c, cx, cy, r):
    """Disque des semaines (mobile) : SA 0 à 42 + repères clés."""
    c.setFillColor(HexColor('#ffffff'))
    c.setStrokeColor(BORDER)
    c.circle(cx, cy, r, stroke=1, fill=1)

    # ticks de semaine (0 à 42), tous les 2 SA
    for w in range(0, 43, 2):
        deg = w * 7 * DEG_PER_DAY
        draw_radial_tick(c, cx, cy, r - 3 * mm, r, deg, MUTED, width=0.5)
        draw_radial_text(c, cx, cy, r - 6.2 * mm, deg, str(w), size=4.6, color=BODY)

    # arc écho T1 (11 -> 13SA+6j)
    a1 = 77 * DEG_PER_DAY
    a2 = 97 * DEG_PER_DAY
    c.saveState()
    c.setStrokeColor(ROSE)
    c.setLineWidth(3.2)
    p = c.beginPath()
    steps = 20
    for i in range(steps + 1):
        dd = a1 + (a2 - a1) * i / steps
        x, y = polar(cx, cy, r - 1.2 * mm, dd)
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

    # repères clés
    for day_offset, sa_label, milestone_label, color in MILESTONES:
        deg = day_offset * DEG_PER_DAY
        draw_radial_tick(c, cx, cy, r - 4.4 * mm, r + 1.5 * mm, deg, color, width=1.3)
        c.saveState()
        c.translate(cx, cy)
        c.rotate(-deg)
        c.setFillColor(color)
        c.circle(0, r + 3 * mm, 1.1 * mm, stroke=0, fill=1)
        c.restoreState()
        label = milestone_label if milestone_label else sa_label
        draw_radial_text(c, cx, cy, r + 5.5 * mm, deg, sa_label, size=4.6, color=color, bold=True)
        if milestone_label:
            draw_radial_text(c, cx, cy, r + 9.2 * mm, deg, milestone_label, size=4.0, color=color)

    # flèche pointeur "SA 0 / DDR" à l'angle 0 (référence d'alignement)
    tip = polar(cx, cy, r + 9 * mm, 0)
    base_l = polar(cx, cy, r - 2 * mm, -3)
    base_r = polar(cx, cy, r - 2 * mm, 3)
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(*tip)
    p.lineTo(*base_l)
    p.lineTo(*base_r)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    draw_radial_text(c, cx, cy, r + 12.5 * mm, 0, 'SA 0 \u2014 DDR', size=5.2, color=INK, bold=True)
    _ = None  # (repère de fin du disque des semaines)

    draw_dashed_circle(c, cx, cy, r + 2.2 * mm, GOLD)


def draw_center_mark(c, cx, cy):
    c.setFillColor(INK)
    c.circle(cx, cy, 1.1 * mm, stroke=0, fill=1)
    c.setStrokeColor(INK)
    c.setLineWidth(0.4)
    c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
    c.line(cx, cy - 3 * mm, cx, cy + 3 * mm)


def page_1(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # En-tête
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 14 * mm, 'DISQUE DE GROSSESSE À IMPRIMER')
    c.setFont('Helvetica', 8)
    c.setFillColor(BODY)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 19 * mm, 'Découpez les deux disques, percez le centre, assemblez-les avec une attache parisienne.')

    # Disque calendrier (grand, fixe)
    cx1, cy1 = PAGE_W / 2, PAGE_H - 95 * mm
    r1 = 64 * mm
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(cx1, cy1 + r1 + 6 * mm, '① DISQUE CALENDRIER — fixe, en dessous')
    draw_calendar_disc(c, cx1, cy1, r1)
    draw_center_mark(c, cx1, cy1)

    # Disque des semaines (petit, mobile)
    cx2, cy2 = PAGE_W / 2, PAGE_H - 226 * mm
    r2 = 40 * mm
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(cx2, cy2 + r2 + 19 * mm, '② DISQUE DES SEMAINES — mobile, au-dessus')
    draw_week_disc(c, cx2, cy2, r2)
    draw_center_mark(c, cx2, cy2)

    # Pied de page
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(PAGE_W / 2, 10 * mm, 'healthcorner.fr · Outil indicatif — ne remplace pas l\u2019échographie de datation')
    c.drawRightString(PAGE_W - 12 * mm, 10 * mm, 'Page 1 / 2')
    c.showPage()


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


def page_2(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    margin = 20 * mm
    y = PAGE_H - 22 * mm
    max_w = PAGE_W - 2 * margin

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(margin, y, 'Notice d\u2019utilisation')
    y -= 10 * mm

    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(GOLD)
    c.drawString(margin, y, 'ASSEMBLAGE')
    y -= 6 * mm
    steps = [
        '1. Découpez les deux disques en suivant les traits pointillés (rose pour le disque calendrier, or pour le disque des semaines).',
        '2. Percez avec précaution le point central de chaque disque (marque en croix).',
        '3. Superposez le disque des semaines (petit) sur le disque calendrier (grand), centres alignés.',
        '4. Insérez une attache parisienne au centre pour permettre la rotation.',
        '5. Faites tourner le disque des semaines jusqu\u2019à ce que la flèche « SA 0 — DDR » pointe sur la date de vos dernières règles, sur le disque calendrier.',
        '6. Lisez directement, sur le disque calendrier, les dates correspondant aux repères imprimés sur le disque des semaines (déclaration, échographies, terme).',
    ]
    c.setFont('Helvetica', 9.3)
    c.setFillColor(BODY)
    for step in steps:
        for line in wrap_text(step, 'Helvetica', 9.3, max_w):
            c.drawString(margin, y, line)
            y -= 4.6 * mm
        y -= 1.6 * mm

    y -= 4 * mm
    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(GOLD)
    c.drawString(margin, y, 'LA RÈGLE DE NAEGELE')
    y -= 6 * mm
    c.setFillColor(SAND)
    box_h = 20 * mm
    c.roundRect(margin, y - box_h + 4 * mm, max_w, box_h, 3 * mm, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margin + 5 * mm, y - 4 * mm, 'DPA = DDR + 280 jours (40 SA)')
    c.setFont('Helvetica', 8.8)
    c.setFillColor(BODY)
    for line in wrap_text('Ajustement si votre cycle diffère de 28 jours : DPA = DDR + 280 j ± (durée du cycle − 28) j.', 'Helvetica', 8.8, max_w - 10 * mm):
        y -= 5 * mm
        c.drawString(margin + 5 * mm, y - 4 * mm, line)
    y -= box_h - 5 * mm

    y -= 8 * mm
    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(GOLD)
    c.drawString(margin, y, 'SA (SEMAINES D\u2019AMÉNORRHÉE) vs SG (SEMAINES DE GROSSESSE)')
    y -= 7 * mm

    # petit tableau
    col_w = [max_w * 0.3, max_w * 0.3, max_w * 0.4]
    headers = ['SA', 'SG', 'Repère']
    rows = [
        ['14 SA', '12 SG', 'Date limite de déclaration'],
        ['22 SA', '20 SG', 'Échographie du 2e trimestre'],
        ['32 SA', '30 SG', 'Échographie du 3e trimestre'],
        ['41 SA', '39 SG', 'Terme officiel France'],
    ]
    row_h = 7 * mm
    table_top = y
    c.setFillColor(SAND)
    c.rect(margin, table_top - row_h, max_w, row_h, stroke=0, fill=1)
    x = margin
    c.setFont('Helvetica-Bold', 8.6)
    c.setFillColor(INK)
    for i, h in enumerate(headers):
        c.drawString(x + 3 * mm, table_top - row_h + 2.3 * mm, h)
        x += col_w[i]
    yy = table_top - row_h
    c.setFont('Helvetica', 8.6)
    c.setFillColor(BODY)
    for r_idx, row in enumerate(rows):
        yy -= row_h
        if r_idx % 2 == 0:
            c.setFillColor(HexColor('#f8f4ee'))
            c.rect(margin, yy, max_w, row_h, stroke=0, fill=1)
        c.setFillColor(BODY)
        x = margin
        for i, val in enumerate(row):
            c.drawString(x + 3 * mm, yy + 2.3 * mm, val)
            x += col_w[i]
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.rect(margin, yy, max_w, table_top - yy, stroke=1, fill=0)
    y = yy - 10 * mm

    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(ALERT)
    c.drawString(margin, y, '⚠ AVERTISSEMENT MÉDICAL')
    y -= 6 * mm
    disclaimer = (
        'Ce disque fournit une estimation indicative basée sur une formule statistique (règle de Naegele) '
        'et les seuils officiels français (HAS, CNGOF). Il ne constitue pas un avis médical individualisé et ne '
        'remplace jamais l\u2019échographie de datation réalisée par un professionnel de santé, seule à confirmer '
        'le terme réel de la grossesse. En cas de doute, consultez votre médecin ou votre sage-femme.'
    )
    c.setFont('Helvetica', 8.8)
    c.setFillColor(BODY)
    for line in wrap_text(disclaimer, 'Helvetica', 8.8, max_w):
        c.drawString(margin, y, line)
        y -= 4.6 * mm

    y -= 8 * mm
    c.setFont('Helvetica-Bold', 8.6)
    c.setFillColor(MUTED)
    c.drawString(margin, y, 'Sources : Ameli.fr · HAS/CNGOF (RPC « Grossesse prolongée et terme dépassé », 2011) · service-public.gouv.fr')

    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(PAGE_W / 2, 14 * mm, 'healthcorner.fr')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.5)
    c.drawRightString(PAGE_W - 12 * mm, 10 * mm, 'Page 2 / 2')
    c.showPage()


def main():
    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    c.setTitle('Disque de grossesse — Health Corner')
    c.setAuthor('Health Corner')
    page_1(c)
    page_2(c)
    c.save()
    print('PDF généré :', OUT_PATH)


if __name__ == '__main__':
    main()
