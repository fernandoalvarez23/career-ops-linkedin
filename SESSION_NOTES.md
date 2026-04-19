# Session Notes — Setup Completo (Apr 2026)

Este archivo documenta todo lo que se configuró en la sesión inicial de setup para que una nueva instancia de Claude pueda retomar el trabajo sin perder contexto.

---

## Estado del sistema

Sistema completamente funcional. Se procesaron 7 ofertas de trabajo:

| # | Empresa | Rol | Score | Mercado |
|---|---------|-----|-------|---------|
| 001 | UST | Project Manager / PO / BA (Banking) | 3.5/5 | ES (remoto) |
| 002 | N26 | Senior PM - Payments Platform | 4.3/5 | ES (BCN) |
| 003 | Santander Digital | PM Prevención del Fraude | 3.4/5 | ES (Madrid hybrid) |
| 004 | Apex Group | Product Lead - Tokenised Funds | 3.0/5 | ES (BCN) |
| 005 | DEPT® | Senior Technical PM | 3.2/5 | AR |
| 006 | AlixPartners | Senior PM | 3.5/5 | AR |
| 007 | Personal Pay | PO Pago de Servicios | 4.0/5 | AR |

**Próximas acciones recomendadas:** Aplicar a N26 (4.3/5) y Personal Pay (4.0/5).

---

## Archivos creados en esta sesión

### CVs (fuente de verdad para adaptaciones)
- `cv-ar.md` — CV completo, datos de contacto Argentina (Buenos Aires, +54 9 11 2387-5178)
- `cv-es.md` — CV completo, datos de contacto España (Barcelona, +34 664 26 02 53)
- `cv.md` — alias de cv-ar.md (default)

### Pipeline de generación de PDFs (Python + reportlab)
- `CV-Reframe-Skill/cv_template.py` — script principal, adaptado para macOS
  - Fuentes: `CV-Reframe-Skill/fonts/` (Montserrat TTF)
  - Output: `output/FernandoAlvarez_CV_{role}_{ARG|ESP}.pdf`
  - Uso: `/opt/homebrew/bin/python3.11 cv_template.py --version es --role "Rol Exacto"`
- `CV-Reframe-Skill/experience.md` — fuente de verdad de toda la experiencia de Fernando
- `CV-Reframe-Skill/SKILL.md` — instrucciones de la skill
- `.claude/skills/cv-adaptation/SKILL.md` — skill registrada en el sistema

### Scanner JobSpy (LinkedIn + Indeed)
- `scan-jobspy.mjs` — llama a Python 3.11 con JobSpy
  - Uso: `node scan-jobspy.mjs --market both` (ar / es / both)
  - Requiere: `pip3.11 install python-jobspy`
  - Python path: `/opt/homebrew/bin/python3.11`

### Dashboard TUI (Go + Bubble Tea)
- `career-dashboard` — binario compilado (no versionado — recompilar con `cd dashboard && go build -o ../career-dashboard .`)
- Go ya instalado en `/opt/homebrew/bin/go`

### Modes actualizados
- `modes/pdf.md` — reescrito para usar pipeline Python/reportlab (no HTML/Playwright)
- `modes/oferta.md` — agrega Paso 0 con detección de mercado AR vs ES

---

## Archivos gitignoreados por diseño (NO están en el repo)

Estos archivos son esenciales pero se excluyen por contener datos personales o configuración de usuario. Si clonás el repo en una nueva máquina, necesitás recrearlos.

### `config/profile.yml`
Perfil completo de Fernando. Copiar desde `config/profile.example.yml` y completar:
- name, email, linkedin
- contact_ar (Buenos Aires, +54 9 11 2387-5178)
- contact_es (Barcelona, +34 664 26 02 53)
- roles: Senior PM, Senior Project Manager, Technical PM, Fintech PM
- compensation_ar: USD 4000-6000/mes
- compensation_es: EUR 55000-80000/año
- work_permit_spain: true

### `modes/_profile.md`
Perfil de arquetipos y narrativa. Copiar desde `modes/_profile.template.md` — pero en este repo está bien configurado con los 6 arquetipos de Fernando (Senior PM, Senior Project Manager, Technical PM, Fintech PM, Digital Transformation PM, Growth PM). Si se pierde, la sesión original documentó todo el contenido en el commit de `modes/_profile.md`.

### `portals.yml`
50+ empresas configuradas. Copiar desde `templates/portals.example.yml`. En esta sesión se configuraron:
- LATAM: MercadoLibre, Ualá, Naranja X, Pomelo, dLocal, Bitso, VTEX, Despegar, Kueski, etc.
- España: BBVA, Santander, Cabify, Glovo, Factorial, Typeform, Flywire, TravelPerk, etc.
- Global Fintech: Stripe, Adyen, Klarna, Revolut, N26, Wise, GoCardless, Nubank, etc.

### `data/applications.md`
Tracker de postulaciones. Se genera automáticamente con `node merge-tracker.mjs`. Actualmente tiene 7 entradas (ver tabla arriba).

---

## Setup desde cero (nuevo clon)

```bash
# 1. Clonar y dependencias
git clone https://github.com/fernandoalvarez23/career-ops-linkedin.git career-ops
cd career-ops
npm install

# 2. Python para PDFs
/opt/homebrew/bin/python3.11 -m pip install reportlab python-jobspy

# 3. Recrear archivos gitignoreados
cp config/profile.example.yml config/profile.yml
# → Editar con datos de Fernando (ver sección arriba)
cp modes/_profile.template.md modes/_profile.md
# → El archivo ya tiene el contenido correcto si viene del repo

# 4. Compilar dashboard
cd dashboard && /opt/homebrew/bin/go build -o ../career-dashboard . && cd ..

# 5. Verificar setup
node doctor.mjs
```

---

## Cómo funciona el circuito completo

```
Terminal normal (sin tokens):
  node scan-jobspy.mjs --market both   → busca en LinkedIn/Indeed → data/pipeline.md
  node scan.mjs                        → busca en portales directos → data/pipeline.md
  ./career-dashboard                   → ver tracker visual

Claude Code (con tokens):
  /career-ops {URL}                    → auto-pipeline: eval + PDF + tracker
  /career-ops pipeline                 → procesa todas las URLs de data/pipeline.md
  /career-ops pdf                      → solo generar PDF adaptado
  /career-ops tracker                  → ver estado de postulaciones
```

## Pipeline de generación de PDFs (detalle técnico)

El modo `/career-ops pdf` NO usa HTML/Playwright. Usa Python + reportlab:

1. Leer JD → extraer keywords y título exacto
2. Detectar mercado → AR (`cv-ar.md`) o ES (`cv-es.md`)
3. Leer `CV-Reframe-Skill/experience.md` como fuente de verdad
4. Copiar `CV-Reframe-Skill/cv_template.py` a `/tmp/cv_adapted_{timestamp}.py`
5. Modificar SOLO el contenido (subtitle, summary, bullets, skills, certs)
6. Fix de paths en el script copiado:
   ```python
   FONTS_DIR = '/Users/fernando/career-ops/CV-Reframe-Skill/fonts'
   PROJECT_ROOT = '/Users/fernando/career-ops'
   OUTPUT_DIR = '/Users/fernando/career-ops/output'
   ```
7. Ejecutar: `/opt/homebrew/bin/python3.11 /tmp/cv_adapted_X.py --version es --role "Titulo Exacto" --output output/FernandoAlvarez_CV_Rol_ESP.pdf`

**Reglas absolutas del CV:**
- Los 5 bullets de resultados de Ripio SIEMPRE van primero (nunca moverlos)
- NUNCA inventar experiencia — solo reframear lo que está en experience.md
- NUNCA modificar diseño (Montserrat, layout, colores)
- NUNCA cambiar títulos reales de posiciones ni nombres de empresas

---

## Superpoderes de Fernando (para evaluaciones y cover letters)

1. PM técnico que habla el idioma de engineering — specs precisas, cero fricción con devs
2. Track record en Fintech real: +42% volumen, USD 3M revenue DeFi, -9% churn, AUM +100%
3. Ejecuta con AI: ya lo usa en el workflow diario, no es aspiracional
4. Liderazgo a escala: 200+ personas, 16 mercados en América Móvil
5. Doble mercado: permiso de trabajo España vigente + experiencia LATAM

**Proof points exactos (siempre citar con métricas):**
- Ripio DeFi: 95% adoption (vs 70% target) → ~USD 3M revenue anual
- Ripio Volume: +42% operated volume H2 (vs 25% target)
- Ripio Retention: -9% churn vs H1, NPS >60, revenue 1.5x target
- Ripio AUM: +100% en BTC/ETH/stablecoins H2 vs H1
- América Móvil: 98%→99.95% availability, 16 mercados, millones de usuarios
- América Móvil: 200+ profesionales liderados (Dev, DevOps, PMO, QA)
