#!/usr/bin/env python3
"""
Fernando Alvarez - Cover Letter Template
Same design as CV: Montserrat fonts, same header, same visual language.

Usage:
    python3 cover_letter_template.py --version es --company N26 --role "Senior PM" --output output/cl.pdf
    python3 cover_letter_template.py --version ar --company Ripio --role "Product Manager"

When adapting per JD: modify the paragraphs/highlights sections below.
NEVER modify fonts, colors, layout, or header structure.
"""
import os
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS_DIR = '/Users/fernando/career-ops/CV-Reframe-Skill/fonts'
OUTPUT_DIR = '/Users/fernando/career-ops/output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

pdfmetrics.registerFont(TTFont('Montserrat-Bold',        os.path.join(FONTS_DIR, 'Montserrat-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Regular',     os.path.join(FONTS_DIR, 'Montserrat-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Light',       os.path.join(FONTS_DIR, 'Montserrat-Light.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Italic',      os.path.join(FONTS_DIR, 'Montserrat-Italic.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-LightItalic', os.path.join(FONTS_DIR, 'Montserrat-LightItalic.ttf')))

WIDTH         = 595.5
HEIGHT        = 842.25
MARGIN        = 20.5
RIGHT_MARGIN  = WIDTH - MARGIN
CONTENT_WIDTH = RIGHT_MARGIN - MARGIN
DARK          = black
LINE_COLOR    = HexColor("#333333")


def draw_paragraph(c, x, y, text, font, size, max_width, leading=None, alignment=TA_JUSTIFY):
    if leading is None:
        leading = size * 1.5
    style = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading,
                           textColor=DARK, alignment=alignment)
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, 700)
    p.drawOn(c, x, y - h)
    return y - h


def create_cover_letter(version='es', company='Company', role_subtitle='Senior Product Manager',
                        addressee='Hiring Team', paragraphs=None, highlights=None,
                        closing=None, output_path=None):
    """
    version:       'ar' or 'es'
    company:       company name for filename
    role_subtitle: shown in header subtitle (same position as CV subtitle)
    addressee:     first line of letter body (bold)
    paragraphs:    list of body paragraph strings (HTML tags supported: <b>, <i>)
    highlights:    list of bulleted highlight strings (bold lead-in supported via <b>)
    closing:       closing paragraph string
    output_path:   full output path (auto-generated if None)
    """
    if version == 'es':
        contact_line = 'Barcelona, España  |  fernando.alvarez@gmail.com  |  linkedin.com/in/falvarez/'
        version_label = 'ESP'
    else:
        contact_line = 'Buenos Aires, Argentina  |  fernando.alvarez@gmail.com  |  linkedin.com/in/falvarez/'
        version_label = 'ARG'

    if output_path is None:
        safe = company.replace(' ', '_').replace('/', '-')[:30]
        output_path = os.path.join(OUTPUT_DIR, f'FernandoAlvarez_CoverLetter_{safe}_{version_label}.pdf')

    c = canvas.Canvas(output_path, pagesize=(WIDTH, HEIGHT))
    y = HEIGHT - 30

    # NAME
    c.setFont('Montserrat-Bold', 28)
    c.setFillColor(DARK)
    name = 'Fernando Alvarez'
    tw = c.stringWidth(name, 'Montserrat-Bold', 28)
    c.drawString((WIDTH - tw) / 2, y, name)
    y -= 22

    # Contact
    c.setFont('Montserrat-Regular', 10)
    tw = c.stringWidth(contact_line, 'Montserrat-Regular', 10)
    c.drawString((WIDTH - tw) / 2, y, contact_line)
    y -= 22

    # Subtitle
    c.setFont('Montserrat-Bold', 15)
    tw = c.stringWidth(role_subtitle, 'Montserrat-Bold', 15)
    c.drawString((WIDTH - tw) / 2, y, role_subtitle)
    y -= 18

    # Divider
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 22

    # Addressee
    y = draw_paragraph(c, MARGIN, y, addressee, 'Montserrat-Bold', 11,
                       CONTENT_WIDTH, alignment=TA_LEFT)
    y -= 18

    # Body paragraphs
    if paragraphs:
        for para in paragraphs:
            y = draw_paragraph(c, MARGIN, y, para, 'Montserrat-Regular', 10.5, CONTENT_WIDTH)
            y -= 12

    # Highlights (bulleted)
    if highlights:
        y -= 4
        for h in highlights:
            c.setFont('Montserrat-Regular', 10.5)
            c.setFillColor(DARK)
            c.drawString(MARGIN, y, '\u2022')
            y = draw_paragraph(c, MARGIN + 12, y + 1, h, 'Montserrat-Regular', 10.5,
                               CONTENT_WIDTH - 12)
            y -= 10
        y -= 4

    # Closing
    if closing:
        y = draw_paragraph(c, MARGIN, y, closing, 'Montserrat-Regular', 10.5, CONTENT_WIDTH)
        y -= 22

    # Signature
    c.setFont('Montserrat-Bold', 11)
    c.setFillColor(DARK)
    c.drawString(MARGIN, y, 'Fernando Alvarez')
    y -= 14
    c.setFont('Montserrat-Light', 10)
    c.drawString(MARGIN, y, 'fernando.alvarez@gmail.com  |  linkedin.com/in/falvarez/')

    c.save()
    return output_path


# ── DEFAULT CONTENT (N26 — adapt per JD when copying to /tmp) ──────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',  choices=['ar', 'es'], default='es')
    parser.add_argument('--company',  default='N26')
    parser.add_argument('--role',     default='Senior Product Manager | Payments Platform, Fintech & Backend Products')
    parser.add_argument('--output',   default=None)
    args = parser.parse_args()

    # ── ADAPT THESE SECTIONS PER JD ──
    addressee = f'Hiring Team, {args.company} — {args.role}'

    paragraphs = [
        (
            "Payment infrastructure is where I've spent the last three years. At Ripio, one of Latin "
            "America's leading crypto-fintech platforms, I owned the full product lifecycle for payment "
            "integrations — fiat on/off-ramp flows, local stablecoins, cross-border settlement, and "
            "third-party payment providers across multiple markets. The result: <b>42% operated volume "
            "growth in H2, versus a 25% target.</b>"
        ),
        (
            "The specifics matter here. I didn't manage payment products at arm's length. I worked directly "
            "with Compliance, Treasury, and Operations to define integration requirements, drafted the technical "
            "specs for each payment rail, and coordinated engineering delivery end-to-end. When Ripio needed "
            "to add a new fiat provider, I owned the process from provider selection through regulatory review "
            "through launch — the same ownership model N26 describes for SEPA, SWIFT, and APM expansion."
        ),
        (
            "The gap worth addressing directly: my payment scheme experience is in crypto rails, not "
            "traditional EU schemes. What transfers is the complexity — multiple regulators, varying "
            "settlement windows, edge cases in reconciliation, and the constant tension between speed "
            "and compliance. I've navigated all of that. SEPA and SWIFT are new names for a familiar "
            "problem structure."
        ),
    ]

    highlights = [
        (
            "<b>Regulated environment ownership.</b> At Ripio I shipped Proof of Reserves — a product "
            "requiring alignment across Legal, Treasury, external auditors, and Engineering. We were the "
            "first exchange in LATAM to publish it. That's the cross-functional ownership your Compliance "
            "and Finance stakeholders need from a PM."
        ),
        (
            "<b>Data-driven prioritization.</b> I took DeFi product adoption from 30% to 95% — above a "
            "70% target — by rebuilding the roadmap based on funnel data. I use Amplitude and Metabase as "
            "primary decision tools, not reporting tools."
        ),
        (
            "<b>Delivery under ambiguity.</b> I built Ripio's crypto product roadmap from scratch with no "
            "prior structure, a volatile market, and multiple competing priorities. In 18 months: volume "
            "+42%, churn -9%, AUM +100%, NPS consistently above 60."
        ),
    ]

    closing = (
        "I'm based in Barcelona, available immediately, and have Spanish work authorization. "
        "I'd welcome a conversation about the payment rails N26 is prioritizing and where I "
        "can accelerate that roadmap."
    )

    path = create_cover_letter(
        version=args.version,
        company=args.company,
        role_subtitle=args.role,
        addressee=addressee,
        paragraphs=paragraphs,
        highlights=highlights,
        closing=closing,
        output_path=args.output,
    )
    print(f'✅ Cover letter generated: {path}')
