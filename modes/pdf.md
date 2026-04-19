# Modo: pdf — Generación de CV/PDF Adaptado al JD

**Este modo usa el pipeline Python + reportlab** que preserva el diseño original exacto de Fernando (fuentes Montserrat, layout, colores). NO usa el HTML template. Delega en la skill `cv-adaptation`.

## Pipeline completo

### Paso 1 — Obtener el JD
Si el JD no está en contexto, pedirlo al usuario: texto o URL.

### Paso 2 — Detectar versión AR vs ES
- Mención de Spain, España, Madrid, Barcelona, empresa española, "contrato indefinido" → `es`
- Argentina, LATAM, empresa global sin señales de España → `ar`
- Si ambigüedad → preguntar al usuario

### Paso 3 — Leer fuente de verdad
Leer `CV-Reframe-Skill/experience.md` **completo** antes de generar cualquier contenido.
Esta es la fuente de verdad para TODA la experiencia de Fernando — más detallada que cv.md.
NUNCA inventar experiencia. Solo reformular lo que ya está en ese archivo.

### Paso 4 — Analizar el JD
Extraer:
- **Título exacto del rol** → será el nuevo subtitle del CV
- **Responsabilidades clave** → reformular bullets con estos verbos
- **Skills requeridas** → asegurar que aparezcan en summary + columna de skills
- **Herramientas mencionadas** → agregar a TOOLS & DOMAINS
- **Nice-to-haves** → destacar en Previous Experience si Fernando los tiene

### Paso 5 — Adaptar contenido

**Subtitle:** Usar el título exacto del JD. Ejemplos:
- "Project Manager | Systems, Operations & Product Workflows"
- "Technical Product Manager | Integrations, Middleware & AI-Driven Products"
- "Senior Product Manager | Fintech, Payments & Growth"

**Summary box:** Reescribir usando keywords, verbos y lenguaje del JD. Mantener tono professional, ~4-5 líneas.

**Ripio bullets** (regla inamovible: resultados primero):
- Los 5 bullets de resultados (42% growth, DeFi 95%, etc.) siempre van primero
- Los 4 bullets descriptivos pueden reordenarse y reenmarcarse con terminología del JD

**América Móvil / Global Hitss bullets:** Reformular con foco en lo que el JD valora (entrega, coordinación, escala, procesos, etc.)

**AMCO bullets:** Ídem, adaptando el foco técnico/delivery según el JD.

**Previous Experience text:** Si el JD menciona nice-to-haves que Fernando tiene (CRM, help desk, migraciones, networking), añadirlos explícitamente.

**TOP SKILLS (izquierda):** Reordenar y reemplazar skills para que las más relevantes para el JD vayan primero.

**TOOLS & DOMAINS (derecha):** Agregar herramientas que menciona el JD y que Fernando usa. No inventar.

**Orden de certificaciones:** La cert más relevante para el rol va primera:
- Roles PM producto → CSPO primero
- Roles PM proyecto → PMP primero
- Roles técnicos / ágiles → CSM o SAFe primero

### Paso 6 — Generar el script adaptado
Copiar `CV-Reframe-Skill/cv_template.py` a `/tmp/cv_adapted_{timestamp}.py`.
Modificar SOLO los bloques de contenido (summary_text, bullets, skills, certs, prev_text).
NO modificar nada de la lógica de renderizado, fuentes, colores, layout o posicionamiento.

### Paso 7 — Ejecutar y generar PDF
```bash
/opt/homebrew/bin/python3.11 /tmp/cv_adapted_{timestamp}.py --version {ar|es} --role "{TITULO EXACTO DEL JD}"
```
El PDF queda en `output/FernandoAlvarez_CV_{role}_{ARG|ESP}.pdf`.

### Paso 8 — Reportar al usuario
Informar:
- Ruta del PDF generado
- Qué cambió: subtitle, 3 cambios clave en skills, cuál cert fue primera y por qué
- Si se usó versión AR o ES y por qué

### Paso 9 — Actualizar tracker
Si la oferta ya está registrada en `data/applications.md`, cambiar PDF de ❌ a ✅.

---

## Reglas absolutas

- **NUNCA modificar diseño**: fuentes, colores, layout, tamaños, márgenes son intocables
- **NUNCA inventar experiencia**: solo reformular lo que está en `CV-Reframe-Skill/experience.md`
- **SIEMPRE resultados de Ripio primero**: los 5 bullets de métricas no se mueven de su posición
- **NUNCA cambiar títulos reales de posiciones** (Senior Product Manager, Senior Delivery & Product Manager, etc.)
- **NUNCA cambiar nombres de empresas ni fechas**

---

## Post-generación

Actualizar tracker si la oferta ya está registrada: cambiar PDF de ❌ a ✅.
