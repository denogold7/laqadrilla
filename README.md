# 🪖 LaQAdrilla

**Agentes de QA para Claude Code y OpenCode** que aceleran las tareas del día a día del testing manual: analizar historias, escribir casos de prueba (manuales, BDD y de API), generar datos de prueba, redactar reportes de bug, ejecutar pruebas end-to-end en el navegador y armar reportes de resultados en HTML — todo en español.

> Pensado para QAs manuales. No hace falta saber programar: se trabaja conversando con tu agente de IA (Claude Code u OpenCode) desde la terminal o VS Code.

🌐 Web: coming soon

---

## ¿Qué es esto?

Imagina un equipo de QA que nunca se cansa y que puedes convocar cuando lo necesites. Eso es LaQAdrilla: una **cuadrilla de agentes especializados**, cada uno experto en una tarea concreta del ciclo de pruebas.

El trato es simple. Tú dejas un insumo en `input/` —una historia de usuario, la observación de un bug, el contrato de una API— y le pides en palabras normales lo que necesitas. El agente indicado se encarga y te deja el resultado listo en `output/`, siguiendo siempre el mismo formato para que todo se vea parejo entre entregas.

Los **casos de prueba** salen como planilla **Excel** (`.xlsx`) junto a un **informe de cobertura** en Markdown que señala ambigüedades y preguntas para el PO. El formato del **reporte de bug** lo controlas tú desde su plantilla. Y cuando quieras dejar de solo diseñar y empezar a **probar de verdad**, los mismos casos se **ejecutan en un navegador real** (con Playwright MCP) o contra una **API** (con Newman), y obtienes un **reporte de resultados en HTML**.

```
input/ → [ agente de QA ] → output/
                ↑
        plantillas/ + scripts/   (formato)
```

Una regla que respetan todos: **no inventan**. Si les falta un dato, un paso o una regla de negocio, lo marcan y lo preguntan en vez de rellenar con suposiciones. Prefieren un artefacto con huecos señalados a uno completo pero falso.

### La cuadrilla

| Agente | Qué hace |
|--------|----------|
| 🔍 **Analista de historias** | Analiza historias y criterios de aceptación; detecta ambigüedades y arma preguntas de refinamiento |
| 🗺️ **Estratega de pruebas** | Arma el plan/estrategia (alcance, riesgos, tipos de prueba, criterios) como dashboard HTML en modo oscuro |
| 📝 **Casos manuales** | Genera los casos en Excel (.xlsx) y Markdown (.md), + un informe de cobertura (.md) con ambigüedades y preguntas para el PO |
| 🥒 **Casos BDD** | Genera escenarios en Gherkin (keywords en inglés, contenido en español) + un informe de cobertura por criterio (.md) |
| 🐞 **Reportes de bug** | Convierte notas sueltas en reportes profesionales, siguiendo tu plantilla |
| 🎲 **Datos de prueba** | Genera datos realistas (Markdown o CSV) |
| 🔌 **Casos de API** | Genera casos de prueba de API a partir de un contrato |
| ▶️ **Ejecutor E2E** | Ejecuta los casos/escenarios pedidos en un navegador real con Playwright MCP (headed o headless) y genera el reporte de la corrida con evidencia |
| 🧪 **Ejecutor de API** | Ejecuta una colección de Postman con Newman contra la API y genera el reporte de la corrida |
| 📊 **Reporte HTML** | Arma el reporte HTML (dashboard en modo oscuro) de una ejecución a partir de sus resultados |
| 🏁 **Informe de cierre** | Resume toda la ronda (resultados, bugs, recomendación go/no-go) en un dashboard HTML en modo oscuro |

---

## Requisitos

- **Un agente de IA de terminal**, a elección:
  - **Claude Code**, o
  - **OpenCode** (los mismos agentes viven también en `.opencode/`).
- Acceso al modelo que use tu agente:
  - Con **Claude Code**: una cuenta de Claude (plan **Pro**, **Max**, **Team** o **Enterprise**) o acceso por **API** de Anthropic. El plan gratuito no incluye Claude Code.
  - Con **OpenCode**: la clave o cuenta del proveedor que elijas (por ejemplo Anthropic, u otro que soporte OpenCode).
- **VS Code** (recomendado, aunque ambos agentes corren en cualquier terminal).
- Para instalar por npm: **Node.js 18 o superior**.
- **Python 3** — lo usan los scripts que dan formato a las salidas: `scripts/generar_casos.py` (planilla `.xlsx` y `.md` de casos) y `scripts/formatear_tablas.py` (alinea las tablas de los `.md`). Instalan `openpyxl`/`tabulate` solo si faltan, o las instalas tú con `pip install -r requirements.txt`.
- **Para ejecutar pruebas E2E** (opcional): los navegadores de Playwright, que se instalan una sola vez con `npx playwright install` (en Linux, además `npx playwright install-deps`). Requiere Node.js.
- **Para ejecutar pruebas de API** (opcional): **Newman**, la CLI de Postman: `npm install -g newman` (requiere Node.js).

---

## Instalación

### 1. Instala tu agente de IA

Elige **uno** de los dos. Los agentes de este repo funcionan en ambos.

**Opción A — Claude Code:**

- Windows (PowerShell): sigue la guía oficial en https://docs.claude.com/en/docs/claude-code/overview
- Con npm (requiere Node.js 18+):
  ```bash
  npm install -g @anthropic-ai/claude-code
  ```
  > No uses `sudo`. Si te da un error de permisos, configura un directorio global propio de npm (`~/.npm-global`).

Verifica la instalación:
```bash
claude --version
```

**Opción B — OpenCode:**

- Instalador (macOS / Linux):
  ```bash
  curl -fsSL https://opencode.ai/install | bash
  ```
- Con npm (requiere Node.js 18+):
  ```bash
  npm install -g opencode-ai
  ```

Verifica la instalación:
```bash
opencode --version
```

### 2. Clonar este repositorio

```bash
git clone https://github.com/denogold7/laqadrilla.git
cd laqadrilla
```

> Si hiciste un fork, reemplaza la URL por la de tu repositorio.

(Opcional) instala las dependencias de los scripts de una:
```bash
pip install -r requirements.txt
```

### 3. Abrir en VS Code y lanzar el agente

```bash
code .
```
Abre la terminal integrada de VS Code (no hace falta una extensión aparte) y ejecuta el que instalaste:
```bash
claude      # si usas Claude Code
# o
opencode    # si usas OpenCode
```
La primera vez te pedirá autenticarte (en el navegador o con la clave de tu proveedor). Listo: tu agente reconoce la cuadrilla de QA —Claude Code lee `.claude/agents/`; OpenCode lee `.opencode/`.

### 4. (Opcional) Preparar la ejecución (E2E y API)

Solo si vas a **ejecutar** pruebas (no únicamente generarlas).

Para **E2E en el navegador**, instala los navegadores de Playwright una vez:
```bash
npx playwright install
```
> En Linux puede pedirte además `npx playwright install-deps`.

Para **pruebas de API**, instala Newman (la CLI de Postman):
```bash
npm install -g newman
```

Si la app/API que vas a probar pide **login o token**, copia la plantilla de variables y completa tus datos (el `.env` no se sube al repo):
```bash
cp .env.example .env
```
Edita `.env` con la URL y las credenciales (`APP_URL`, `APP_USER`, `APP_PASSWORD`, `API_TOKEN`). Los agentes las leen de ahí; nunca las commitean.

---

## Cómo se usa

1. Pon tu insumo en la carpeta de `input/` que corresponda (hay un ejemplo en cada una para arrancar).
2. Pídele a tu agente lo que necesites, en lenguaje natural. Él elige el especialista adecuado.
3. Revisa el resultado en `output/`.

**Ejemplos de lo que puedes pedir:**

- *"Analiza la historia HU-001 y dime qué ambigüedades tiene."*
- *"Arma el plan de pruebas de HU-001."* → genera el plan en HTML (modo oscuro) en `output/planes-de-prueba/`
- *"Genera los casos de prueba de HU-001."* → arma `casos-HU-001.xlsx`, `casos-HU-001.md` y `casos-HU-001-cobertura.md`
- *"Pasa la historia HU-001 a escenarios BDD."* → arma `HU-001-registro.feature` + `HU-001-cobertura.md`
- *"Toma la observación de `input/bugs/` y arma el reporte de bug."*
- *"Genera datos de prueba para el formulario de registro."*
- *"Genera los casos de prueba de la API de autenticación."*
- *"Ejecuta SOLO el escenario de registro válido de HU-001 contra https://tu-app.com."* → corre la prueba en el navegador y genera el reporte HTML de esa corrida en `output/ejecuciones/`
- *"Ejecuta la colección de API de `input/api/` contra https://tu-api.com."* → corre la colección con Newman y genera el reporte HTML en `output/ejecuciones/`
- *"Arma el informe de cierre de las pruebas de HU-001."* → resume la ronda en un informe HTML (modo oscuro) en `output/informes-cierre/`

> 💡 El formato del **reporte de bug** lo defines en `plantillas/plantilla-reporte-bug.md`. Los **casos de prueba** salen como planilla Excel (referencia `plantillas/plantilla-casos-prueba.xlsx`, la arma `scripts/generar_casos.py`) más un informe de cobertura (referencia `plantillas/plantilla-cobertura.md`).

---

## Estructura del repositorio

```
laqadrilla/
├── CLAUDE.md              # Contexto y estándares del proyecto (Claude Code lo lee siempre)
├── README.md
├── ARQUITECTURA.md        # Cómo está pensado el repo para crecer (agentes/skills/MCP/herramientas/scripts)
├── requirements.txt       # Dependencias de Python (openpyxl, tabulate)
├── .mcp.json              # Conexiones MCP activas (Playwright headed + headless)
├── .mcp.json.example      # Plantilla para más conexiones (Jira, Xray, etc.)
├── .env.example           # Plantilla de variables/credenciales (copiar a .env, que no se versiona)
├── .claude/
│   ├── agents/            # Los agentes de QA para Claude Code (el "quién")
│   └── skills/            # Skills (el "cómo"): técnicas de diseño + ejecución E2E y de API
├── .opencode/             # Los mismos agentes, para OpenCode
├── herramientas/          # Herramientas externas de testing (Newman para API; JMeter/k6 a futuro)
├── plantillas/            # Referencias de formato (bug + casos .xlsx + cobertura .md)
├── scripts/               # Utilidades internas en Python (casos, reporte HTML, conversor Newman, plan e informe de cierre)
├── input/                 # Tus insumos (con un ejemplo en cada carpeta; incluye una colección de API en input/api/)
└── output/                # Lo que generan los agentes (ejecuciones, planes-de-prueba, informes-cierre…)
```

> 🧱 ¿Quieres entender cómo está armado el repo o sumarle un skill / un server MCP a futuro? Mira [`ARQUITECTURA.md`](ARQUITECTURA.md).

---

## Cómo agregar un agente nuevo

El proyecto está pensado para crecer. Para sumar un agente:

1. Crea un archivo en `.claude/agents/` (ej.: `mi-agente.md`).
2. Agrégale el frontmatter con `name`, `description` y `tools`. La `description` es clave: es lo que usa el agente para saber cuándo invocarlo.
3. Escribe el cuerpo (rol, entradas, proceso, salida y reglas), en español.
4. Si genera un artefacto con formato propio, suma su plantilla en `plantillas/` (o su script en `scripts/`) y su carpeta en `output/`.
5. Si genera tablas en un `.md`, hazlas pasar por `scripts/formatear_tablas.py` para que queden alineadas (es el estándar del repo).

> Para usarlo también en OpenCode, corre `scripts/convertir_agentes_opencode.py` y vuelca la versión equivalente en `.opencode/`.

Toma los agentes existentes como referencia de estilo.

## Licencia

Licencia **MIT** — © 2026 **JirenDen**. Puedes usarlo, modificarlo y compartirlo libremente; se entrega sin garantías.
