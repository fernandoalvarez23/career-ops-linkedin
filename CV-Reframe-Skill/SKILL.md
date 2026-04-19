---
name: cv-adaptation
description: Adapt Fernando Alvarez's CV to match specific job proposals. Use this skill whenever the user shares a job description, job posting, or hiring proposal and wants a tailored CV generated. Also trigger when the user says "adapt my CV", "tailor my resume", "apply to this", "new proposal", or shares a JD and asks for help applying. This skill preserves the exact original CV design (Montserrat fonts, layout, colors, spacing) and only modifies content to match the target role. Always use this skill — never generate a CV from scratch or invent a new design.
---

# CV Adaptation Skill

## Overview
This skill adapts Fernando Alvarez's CV to match specific job proposals. It changes ONLY the content (subtitle, summary, bullets, skills, cert order) while preserving the EXACT original design pixel for pixel.

## Quick Start

1. Read the job proposal
2. Ask: ARG or ESP version?
3. Run `apt-get install -y fonts-montserrat -q` (required for fonts)
4. Copy the template script from `scripts/cv_template.py`
5. Modify ONLY the content sections (see "What Changes" below)
6. Generate PDF, rasterize with `pdftoppm`, visually verify, deliver

## What ALWAYS Changes Per Job Proposal

1. **Subtitle** → Match the exact job title from the JD (e.g., "Technical Product Manager | Integrations, Middleware & AI-Driven Products")
2. **Summary box** → Rewrite to mirror JD keywords, focus areas, and language
3. **Bullet points** → Reframe Fernando's real experience using JD verbs and keywords
4. **TOP SKILLS column** → Reorder/replace to match JD priorities
5. **TOOLS & DOMAINS column** → Add/swap tools mentioned in JD
6. **Certification order** → Most relevant cert first
7. **Previous Experience text** → Emphasize JD "nice to have" items Fernando actually has

## IMPORTANT: Ripio Bullet Order Rule
In Fernando's current base CV, Ripio bullets follow a **results-first** structure:
- First 5 bullets = quantified results (42% growth, DeFi 95%, B2C 1.5x, churn -9%, AUM 100%+)
- Next 4 bullets = descriptive (ecosystem, strategic initiatives, teams, AI)

When adapting for a JD, you may reframe and reorder these bullets, but **always keep quantified results prominent** unless the JD explicitly calls for a non-results-oriented profile.

## What NEVER Changes

- Design, fonts, colors, spacing, layout
- Company names and date ranges
- Role titles within each company (real titles)
- Education details
- Language levels
- Contact info (only switches between ARG/ESP)

## Adaptation Process

### Step 1: Analyze the JD
Extract from the job posting:
- **Job title** (exact wording) → becomes the subtitle
- **Key responsibilities** → reframe bullets to mirror these
- **Required skills** → ensure they appear in summary, bullets, or skills columns
- **Nice-to-haves** → mention in Previous Experience or skills if Fernando has them
- **Tools mentioned** → add to TOOLS & DOMAINS column
- **Industry/domain keywords** → weave into summary and bullets

### Step 2: Determine Version
- **ARG**: Buenos Aires, Argentina | +54 9 11 2387-5178
- **ESP**: Barcelona, España | +34 664 26 02 53
- Email and LinkedIn are the same for both

### Step 3: Adapt Content
Read `references/experience.md` for Fernando's full real experience — this is the source of truth. Never invent experience. Only reframe what's real using the JD's language.

**Reframing rules:**
- Use the JD's exact verbs and phrases when describing Fernando's work
- If the JD says "gather requirements from clients" and Fernando did that, use those exact words
- If the JD says "middleware" and Fernando worked with integration layers, call them middleware
- If the JD mentions something Fernando hasn't done, DON'T add it — skip it silently

### Step 4: Generate PDF
```bash
apt-get install -y fonts-montserrat -q
cp scripts/cv_template.py /home/claude/cv_adapted.py
# Edit the content sections in cv_adapted.py
python3 /home/claude/cv_adapted.py
```

### Step 5: Verify
```bash
pdftoppm -jpeg -r 200 /home/claude/output.pdf /home/claude/verify_page
# Then view the images to check layout
```

### Step 6: Deliver
```bash
cp /home/claude/output.pdf /mnt/user-data/outputs/FernandoAlvarez_CV_[RoleName]_[ARG|ESP].pdf
```

## Design Specifications

Read `references/design_specs.md` for the complete design specification including fonts, sizes, colors, spacing values, and layout structure. These are extracted from the original PDF and must not be modified.

## Examples of Successful Adaptations

### Project Manager role (Systems & Operations)
- Subtitle: "Project Manager | Systems, Operations & Product Workflows"
- Summary emphasized: system implementations, vendor coordination, operational continuity, transition to product
- Bullets reframed around: coordinating delivery, tracking timelines/risks/dependencies, documenting processes
- Skills led with: Project Management & Coordination, System Implementations & Migrations
- Certs: PMP first

### Technical Product Manager role (Integrations & AI)
- Subtitle: "Technical Product Manager | Integrations, Middleware & AI-Driven Products"
- Summary emphasized: system integrations (APIs, middleware, data mapping), hybrid BA + Product, LLMs/agentic workflows
- Bullets reframed around: integration solutions, specification packages (BRDs, FRDs), architecture-level decisions, data transformation flows
- Skills led with: Technical Product Management, System Integrations (APIs, Middleware), AI/LLM
- Certs: Product Owner first
