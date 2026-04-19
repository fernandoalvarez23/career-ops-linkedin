---
name: cv-adaptation
description: Adapt Fernando Alvarez's CV to match a specific job posting. Use whenever the user shares a JD and wants a tailored PDF. Preserves EXACT original design (Montserrat fonts, layout, colors). Only modifies content. Also trigger when user says "adaptá mi CV", "generá el CV para esta oferta", "apply to this", or shares a JD.
---

# CV Adaptation Skill

## Overview
Adapts Fernando's CV to a specific JD. Changes ONLY content — never design.

## What ALWAYS Changes

1. **Subtitle** → exact job title from JD (e.g. "Technical Product Manager | Integrations & AI")
2. **Summary box** → rewritten to mirror JD keywords, focus areas, language
3. **Ripio bullets** → reframed with JD verbs/keywords (results always stay first)
4. **América Móvil bullets** → reframed to match JD responsibilities
5. **TOP SKILLS** → reordered/replaced to match JD priorities
6. **TOOLS & DOMAINS** → add tools mentioned in JD
7. **Cert order** → most relevant cert goes first
8. **Previous Experience text** → highlight JD "nice to haves" Fernando actually has

## What NEVER Changes
- Fonts (Montserrat), colors, layout, spacing
- Company names, date ranges, real role titles
- Education, language levels
- Contact info (only AR ↔ ES switch)

## Source of Truth
Read `CV-Reframe-Skill/experience.md` for ALL of Fernando's real experience.
NEVER invent experience. Only reframe what's real using JD language.

## Ripio Bullet Rule
Results bullets ALWAYS go first (42% growth, DeFi 95%, etc.).
Only reorder descriptive bullets (ecosystem, initiatives, teams, AI) to match JD.

## Reframing Rules
- Use the JD's exact verbs and phrases
- If JD says "middleware" and Fernando worked with integration layers → call them middleware
- If JD says "gather requirements" and Fernando did that → use those exact words
- If JD mentions something Fernando hasn't done → skip silently, never invent

## Process

### Step 1: Analyze JD
Extract:
- Exact job title → subtitle
- Key responsibilities → reframe bullets
- Required skills → appears in summary + skills columns
- Tools mentioned → TOOLS & DOMAINS column
- Nice-to-haves → Previous Experience text

### Step 2: Detect Version
- Offer from Spain / España / Madrid / Barcelona → `--version es`
- Otherwise → `--version ar`

### Step 3: Generate adapted Python script
Copy `CV-Reframe-Skill/cv_template.py` to a temp file `/tmp/cv_adapted.py`.
Modify ONLY these sections in the copy:
- `role_subtitle` default value → JD title
- `summary_text` → rewritten for JD
- `ripio_bullets` list → reframed for JD
- `am_bullets` list → reframed for JD
- `amco_bullets` list → reframed for JD
- `prev_text` → highlight JD nice-to-haves
- `left_skills` → TOP SKILLS reordered for JD
- `right_skills` → TOOLS & DOMAINS updated for JD
- `certs` order → most relevant first

### Step 4: Execute
```bash
/opt/homebrew/bin/python3.11 /tmp/cv_adapted.py --version ar --role "EXACT JD TITLE"
```
Output goes to `output/FernandoAlvarez_CV_{role}_{ARG|ESP}.pdf`

### Step 5: Confirm
Tell the user:
- PDF path
- What changed (subtitle, summary, key skill swaps)
- Which cert was put first and why

## Examples

### Project Manager role
- Subtitle: "Project Manager | Systems, Operations & Product Workflows"
- Summary: emphasize delivery, vendor coordination, operational continuity
- Bullets: tracking timelines/risks/dependencies, coordinating delivery, ITIL, migrations
- Skills lead: Project Management, System Implementations, Process Documentation
- Certs: PMP first

### Technical Product Manager role (Integrations & AI)
- Subtitle: "Technical Product Manager | Integrations, Middleware & AI-Driven Products"
- Summary: system integrations, APIs, middleware, LLMs, rapid prototyping
- Bullets: integration solutions, BRDs/FRDs, architecture decisions, data flows
- Skills lead: Technical Product Management, System Integrations, AI/LLM
- Certs: Product Owner first

### Senior PM (Fintech / Payments)
- Subtitle: "Senior Product Manager | Fintech, Payments & Growth"
- Summary: payments, DeFi, fiat on/off-ramp, growth metrics, cross-functional leadership
- Bullets: results bullets first unchanged, descriptive reframed for payments/fintech
- Skills lead: Product Performance Analytics, Fintech & Payments Products, Growth Metrics
- Certs: Product Owner first
