#!/usr/bin/env python3
"""
Fernando Alvarez - CV adapted for a specific role.
EXACT replica of original design (Montserrat fonts, same layout).
Only content changed to match JD.

Usage:
    python3 cv_template.py --version ar --role "Senior Product Manager" --output output/cv.pdf
    python3 cv_template.py --version es --role "Project Manager" --output output/cv.pdf
"""

import sys
import os
import argparse

# Resolve font directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, 'fonts')
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Montserrat fonts (local fonts/ directory)
pdfmetrics.registerFont(TTFont('Montserrat-Bold', os.path.join(FONTS_DIR, 'Montserrat-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Regular', os.path.join(FONTS_DIR, 'Montserrat-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Light', os.path.join(FONTS_DIR, 'Montserrat-Light.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Italic', os.path.join(FONTS_DIR, 'Montserrat-Italic.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-LightItalic', os.path.join(FONTS_DIR, 'Montserrat-LightItalic.ttf')))

# Page dimensions (from original: 595.5 x 842.25)
WIDTH = 595.5
HEIGHT = 842.25
MARGIN = 20.5  # from original char positions
RIGHT_MARGIN = WIDTH - 20.5
CONTENT_WIDTH = RIGHT_MARGIN - MARGIN

# Colors
DARK = black
GRAY_BG = HexColor("#F0F0F0")  # Light gray background for summary box
LINE_COLOR = HexColor("#333333")


def draw_centered_text(c, y, text, font, size):
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    c.drawString((WIDTH - tw) / 2, y, text)


def draw_paragraph(c, x, y, text, font, size, max_width, leading=None, alignment=TA_JUSTIFY):
    if leading is None:
        leading = size * 1.4
    style = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading,
                           textColor=DARK, alignment=alignment)
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, 500)
    p.drawOn(c, x, y - h)
    return y - h


def draw_bullet_item(c, x, y, text, font='Montserrat-Regular', size=10.5, max_width=None):
    if max_width is None:
        max_width = CONTENT_WIDTH - 15
    # Draw bullet
    c.setFont(font, size)
    c.setFillColor(DARK)
    c.drawString(x, y, "\u2022")
    # Draw text
    style = ParagraphStyle('bullet', fontName=font, fontSize=size,
                           leading=size * 1.45, textColor=DARK, alignment=TA_JUSTIFY)
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, 500)
    p.drawOn(c, x + 12, y - h + size)
    return y - h - 2


def create_cv(version='ar', role_subtitle=None, output_path=None):
    """
    version: 'ar' (Argentina) or 'es' (Spain/Barcelona)
    role_subtitle: full subtitle string, e.g. "Senior Product Manager | Fintech & AI-Driven Products"
    output_path: full path for output PDF (defaults to output/ in project root)
    """
    # Contact info by version
    if version == 'es':
        contact = "Barcelona, España | +34 664 26 02 53 | fernando.alvarez@gmail.com | linkedin.com/in/falvarez/"
        version_label = "ESP"
    else:
        contact = "Buenos Aires, Argentina | +54 9 11 2387-5178 | fernando.alvarez@gmail.com | linkedin.com/in/falvarez/"
        version_label = "ARG"

    # Default subtitle if none provided
    if role_subtitle is None:
        role_subtitle = "Senior Product Manager | Fintech, Crypto & AI-Driven Products"

    # Default output path
    if output_path is None:
        safe_role = role_subtitle.split('|')[0].strip().replace(' ', '_').replace('/', '-')[:40]
        output_path = os.path.join(OUTPUT_DIR, f"FernandoAlvarez_CV_{safe_role}_{version_label}.pdf")

    c = canvas.Canvas(output_path, pagesize=(WIDTH, HEIGHT))

    y = HEIGHT - 30

    # === NAME (centered, Montserrat-Bold, 28pt) ===
    c.setFillColor(DARK)
    draw_centered_text(c, y, "Fernando Alvarez", "Montserrat-Bold", 28)
    y -= 22

    # === Contact info (centered, Montserrat-Regular, 10pt) ===
    c.setFont("Montserrat-Regular", 10)
    tw = c.stringWidth(contact, "Montserrat-Regular", 10)
    c.drawString((WIDTH - tw) / 2, y, contact)
    y -= 25

    # === SUBTITLE (centered, Montserrat-Bold, 18pt) — set from JD ===
    # If subtitle is long, split at '|' boundary that exceeds width
    max_w = CONTENT_WIDTH
    c.setFont("Montserrat-Bold", 18)
    if c.stringWidth(role_subtitle, "Montserrat-Bold", 18) <= max_w:
        draw_centered_text(c, y, role_subtitle, "Montserrat-Bold", 18)
        y -= 18
    else:
        # Split at last '|' that fits
        parts = role_subtitle.split('|')
        line1 = parts[0].strip()
        line2 = ' | '.join(p.strip() for p in parts[1:])
        draw_centered_text(c, y, line1, "Montserrat-Bold", 18)
        y -= 20
        draw_centered_text(c, y, line2, "Montserrat-Bold", 18)
        y -= 18

    # === GRAY SUMMARY BOX (Montserrat-Light italic, ~11.5pt, justified) ===
    box_padding = 12
    # DEFAULT summary — adapt per JD
    summary_text = (
        "Senior Technology Professional with 20+ years of experience leading globally distributed, "
        "cross-functional teams and delivering complex technology initiatives end to end. I combine "
        "a strong IT foundation with applied AI to automate workflows, uncover insights from product "
        "and business data, speed up decision-making, and rapidly prototype solutions using design "
        "systems and AI-assisted development. I bridge business and technology effectively, helping "
        "teams move faster, improve execution, and deliver meaningful customer impact."
    )
    style = ParagraphStyle('summary', fontName='Montserrat-LightItalic', fontSize=11.5,
                           leading=16, textColor=DARK, alignment=TA_JUSTIFY)
    p = Paragraph(summary_text, style)
    w, h = p.wrap(CONTENT_WIDTH - box_padding * 2, 300)
    
    # Draw gray background
    c.setFillColor(GRAY_BG)
    c.rect(MARGIN, y - h - box_padding * 2, CONTENT_WIDTH, h + box_padding * 2, fill=1, stroke=0)
    c.setFillColor(DARK)
    p.drawOn(c, MARGIN + box_padding, y - h - box_padding)
    y -= h + box_padding * 2 + 15

    # === EXPERIENCE (Montserrat-Bold, 18pt) ===
    y -= 10  # extra spacing before section title
    c.setFont("Montserrat-Bold", 18)
    c.drawString(MARGIN, y, "EXPERIENCE")
    y -= 8
    # Thin line under
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 18

    # --- Ripio ---
    c.setFont("Montserrat-Bold", 14)
    c.drawString(MARGIN, y, "Ripio ")
    rw = c.stringWidth("Ripio ", "Montserrat-Bold", 14)
    c.setFont("Montserrat-Regular", 14)
    c.drawString(MARGIN + rw, y, "(Fintech Industry)")
    y -= 16
    c.setFont("Montserrat-Bold", 11)
    c.drawString(MARGIN, y, "Senior Product Manager")
    bw = c.stringWidth("Senior Product Manager", "Montserrat-Bold", 11)
    c.setFont("Montserrat-Regular", 11)
    c.drawString(MARGIN + bw, y, " | LATAM | Jun 2022 - Present")
    y -= 14

    # DEFAULT Ripio bullets — results first, then descriptive. Adapt per JD.
    ripio_bullets = [
        "Achieved 42% operated volume growth in the second half of the year, versus a 25% target.",
        "Drove adoption of the company's DeFi product to over 95%, versus a 70% target, contributing to an estimated USD 3M in annual revenue.",
        "Helped drive B2C revenue to 1.5x target while maintaining NPS above 60.",
        "Improved growth sustainability by increasing retention above target and reducing churn by nearly 9% compared with the first half of the year.",
        "Helped drive over 100% AUM growth across key crypto assets, including BTC, ETH, and stablecoins, compared with the first half of the year.",
        "Led the evolution of Ripio's wallet and crypto product ecosystem across trading, DeFi, lending, blockchain integrations, local stablecoins and fiat on/off-ramp capabilities.",
        "Owned the delivery of strategic initiatives including Proof of Reserves (PoR), crypto yield functionality, BTC-collateralized loans, and Solana DEX integration.",
        "Directed globally distributed, cross-functional teams across Product, UX, Engineering, and QA, aligning business priorities with technical execution in a fast-paced crypto environment.",
        "Leveraged AI to analyze product and business data, support decision-making, and create rapid product proposals and prototypes using the company's design system, accelerating solution design and delivery readiness.",
    ]
    for bullet in ripio_bullets:
        y = draw_bullet_item(c, MARGIN, y, bullet, size=10.5)
    
    y -= 8

    # --- América Móvil / Global Hitss ---
    c.setFont("Montserrat-Bold", 14)
    c.drawString(MARGIN, y, "América Móvil / Global Hitss ")
    rw = c.stringWidth("América Móvil / Global Hitss ", "Montserrat-Bold", 14)
    c.setFont("Montserrat-Regular", 14)
    c.drawString(MARGIN + rw, y, "(Streaming Media Industry)")
    y -= 16
    c.setFont("Montserrat-Bold", 11)
    c.drawString(MARGIN, y, "Senior Delivery & Product Manager")
    bw = c.stringWidth("Senior Delivery & Product Manager", "Montserrat-Bold", 11)
    c.setFont("Montserrat-Regular", 11)
    c.drawString(MARGIN + bw, y, " | LATAM & México | Jan 2019 - Jun 2022")
    y -= 14

    # CHANGED bullets for PM focus
    am_bullets = [
        "Led and coordinated multiple concurrent projects across a regional streaming platform (Claro Video, Claro TV, Claro Música) operating in 16 LATAM markets.",
        "Managed vendor relationships and acted as the main point of contact between internal teams and external technology partners.",
        "Tracked progress, timelines, risks, and dependencies across system implementations, migrations, and process improvement initiatives.",
        "Directed a 200+ person organization embedding Agile delivery practices (SAFe, Scrum, Kanban, Lean) to improve coordination and delivery.",
        "Owned multi-million-dollar CAPEX/OPEX budgets, including procurement, vendor management, and strategic partnerships.",
        "Documented and improved operational processes, workflows, and system knowledge across the technology organization.",
    ]
    for bullet in am_bullets:
        y = draw_bullet_item(c, MARGIN, y, bullet, size=10.5)

    # ===================== PAGE 2 =====================
    c.showPage()
    y = HEIGHT - 30

    # --- América Móvil / AMCO ---
    c.setFillColor(DARK)
    c.setFont("Montserrat-Bold", 14)
    c.drawString(MARGIN, y, "América Móvil / AMCO ")
    rw = c.stringWidth("América Móvil / AMCO ", "Montserrat-Bold", 14)
    c.setFont("Montserrat-Regular", 14)
    c.drawString(MARGIN + rw, y, "(Streaming Media Industry)")
    y -= 16
    c.setFont("Montserrat-Bold", 11)
    c.drawString(MARGIN, y, "Senior IT Project Manager")
    bw = c.stringWidth("Senior IT Project Manager", "Montserrat-Bold", 11)
    c.setFont("Montserrat-Regular", 11)
    c.drawString(MARGIN + bw, y, " | Argentina & México | Feb 2016 - Dec 2018")
    y -= 14

    # CHANGED bullets for PM focus
    amco_bullets = [
        "Led system implementation and migration projects, including data migration from on-premises to AWS cloud environments.",
        "Built and coordinated the DevOps & IT Infrastructure teams (40+ professionals), managing issue routing, prioritization, and resolution under ITIL best practices.",
        "Configured and maintained CDN (Akamai) and platform infrastructure, supporting day-to-day operational continuity.",
        "Defined and documented technology processes, support policies, and operational procedures for the infrastructure team.",
        "Led, coached, and developed team member skills in technology and support.",
    ]
    for bullet in amco_bullets:
        y = draw_bullet_item(c, MARGIN, y, bullet, size=10.5)

    y -= 18  # extra spacing before section

    # --- Previous Experience ---
    c.setFont("Montserrat-Bold", 13)
    c.drawString(MARGIN, y, "Previous Experience")
    y -= 14
    c.setFont("Montserrat-Regular", 11)
    c.drawString(MARGIN + 3, y, "2000 - 2016")
    y -= 16

    # CHANGED to emphasize CRM, help desk, system admin (nice to haves from JD)
    prev_text = (
        "IT Infrastructure, Operations, and Project Management across consulting, streaming media, "
        "and internet services environments (2000–2016), including roles at DLA, Claxson, Datco, and "
        "Via Net Works. Hands-on experience with CRM platforms, help desk operations, system "
        "administration, and cross-team coordination."
    )
    style = ParagraphStyle('prev', fontName='Montserrat-Regular', fontSize=10.5,
                           leading=15, textColor=DARK, alignment=TA_JUSTIFY)
    p = Paragraph(prev_text, style)
    w, h = p.wrap(CONTENT_WIDTH, 200)
    p.drawOn(c, MARGIN, y - h)
    y -= h + 20

    # === EDUCATION ===
    y -= 18  # extra spacing before section title
    c.setFont("Montserrat-Bold", 18)
    c.drawString(MARGIN, y, "EDUCATION")
    y -= 8
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 18
    c.setFont("Montserrat-Bold", 13)
    c.drawString(MARGIN, y, "Bachelor Degree in Computer Engineering")
    y -= 15
    c.setFont("Montserrat-Regular", 11)
    c.drawString(MARGIN, y, "National Technological University (UTN) | Argentina | Mar 2000 - Mar 2008")
    y -= 25

    # === CERTIFICATIONS ===
    y -= 18  # extra spacing before section title
    c.setFont("Montserrat-Bold", 18)
    c.drawString(MARGIN, y, "CERTIFICATIONS")
    y -= 8
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 18

    # PMP first (more relevant for PM role)
    certs = [
        ("PMP® CERTIFIED PROJECT MANAGEMENT", " | Project Management Institute | Nov 2013"),
        ("CERTIFIED SCRUM MASTER", " | Scrum Alliance | Nov 2018"),
        ("CERTIFIED SAFe 4 AGILIST", " | Scaled Agile, Inc. | Nov 2019"),
        ("CERTIFIED PRODUCT OWNER", " | Scrum, Inc. | Aug 2022"),
    ]
    for bold_part, regular_part in certs:
        c.setFont("Montserrat-Bold", 11)
        c.drawString(MARGIN, y, bold_part)
        bw = c.stringWidth(bold_part, "Montserrat-Bold", 11)
        c.setFont("Montserrat-Regular", 11)
        c.drawString(MARGIN + bw, y, regular_part)
        y -= 15
    
    y -= 12

    # === LANGUAGES ===
    y -= 18  # extra spacing before section title
    c.setFont("Montserrat-Bold", 18)
    c.drawString(MARGIN, y, "LANGUAGES")
    y -= 8
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 18

    langs = [
        ("Spanish:", " Native"),
        ("English:", " Professional working proficiency (B2)"),
        ("Italian:", " Basic (A2 level)"),
        ("Japanese:", " Basic (A1 level)"),
    ]
    for bold_part, regular_part in langs:
        c.setFont("Montserrat-Bold", 10.5)
        c.drawString(MARGIN + 12, y, bold_part)
        bw = c.stringWidth(bold_part, "Montserrat-Bold", 10.5)
        c.setFont("Montserrat-Regular", 10.5)
        c.drawString(MARGIN + 12 + bw, y, regular_part)
        y -= 14
    # Add bullet points
    for i, lang in enumerate(langs):
        lang_y = y + 14 * (len(langs) - i) 
    
    y -= 12

    # === TOP SKILLS & TOOLS & DOMAINS (two columns) ===
    y -= 18  # extra spacing before section title
    c.setFont("Montserrat-Bold", 18)
    c.drawString(MARGIN, y, "TOP SKILLS")
    col2_x = WIDTH / 2 + 10
    c.drawString(col2_x, y, "TOOLS & DOMAINS")
    y -= 8
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, RIGHT_MARGIN, y)
    y -= 16

    # CHANGED skills to match PM JD
    left_skills = [
        "Project Management & Coordination",
        "System Implementations & Migrations",
        "Process Documentation & Workflows",
        "Vendor & Stakeholder Management",
        "Risk & Dependency Tracking",
        "Cross-functional Team Leadership",
        "Agile Product Management",
        "Technical Product Execution",
        "Go-to-Market Strategy Development",
    ]
    right_skills = [
        "JIRA / Confluence / Notion",
        "Figma",
        "Amplitude",
        "Metabase",
        "CRM & Operational Platforms",
        "System Integrations (APIs, SDKs)",
        "Cloud Infrastructure (AWS, Azure)",
        "Platform Migrations & Transitions",
        "AI-Driven Productivity",
    ]

    skill_y = y
    c.setFont("Montserrat-Regular", 10.5)
    for skill in left_skills:
        c.drawString(MARGIN + 12, skill_y, "\u2022  " + skill)
        skill_y -= 14
    
    skill_y = y
    for skill in right_skills:
        c.drawString(col2_x + 12, skill_y, "\u2022  " + skill)
        skill_y -= 14

    c.save()
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Fernando Alvarez CV PDF')
    parser.add_argument('--version', choices=['ar', 'es'], default='ar',
                        help='CV version: ar (Argentina) or es (Spain)')
    parser.add_argument('--role', type=str, default=None,
                        help='Role subtitle, e.g. "Senior Product Manager | Fintech & AI"')
    parser.add_argument('--output', type=str, default=None,
                        help='Output PDF path (optional)')
    args = parser.parse_args()

    path = create_cv(version=args.version, role_subtitle=args.role, output_path=args.output)
    print(f"✅ CV generated: {path}")
