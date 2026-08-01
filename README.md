# Radiografía de las Startups en Perú 🇵🇪

Observatorio de datos sobre el ecosistema de **startups de tecnología en Perú**: no solo
"cuánto se invirtió", sino las preguntas incómodas que casi nadie cruza con datos —
**quién logra emprender, de qué estrato viene, cuánto pesa el respaldo familiar y la
precariedad laboral, y si las startups viven de crear valor o de ganar concursos.**

> Estado: **en construcción** (scaffolding + fuentes mapeadas). Repo privado por ahora.

## Las preguntas que queremos responder

**Capa dura (hay datos):**
- ¿Cuánto se invierte al año y en qué sectores? ¿Cuánto es capital **peruano vs extranjero**?
- ¿Quiénes ganan los concursos del Estado (StartUp Perú) y cuánto reciben?
- ¿Cuánto tiempo viven las startups? ¿Cuántas sobreviven al grant?
- ¿Qué tan concentrado está todo en Lima y en fintech?

**Capa social (la tesis fuerte — requiere datos primarios):**
- ¿De qué **estrato social** vienen los fundadores que sí logran salir adelante?
- ¿Es lo mismo emprender **con una familia que te respalda** (sin gastos corrientes que cubrir)
  que sin ella? ¿La precariedad laboral hace más difícil emprender?
- ¿Las startups peruanas **viven de ganar concursos** o de mercado/inversión real?
- ¿Tienen que **emigrar** para conseguir capital y velocidad de crecimiento?

## Qué SÍ se puede responder con datos existentes, y qué NO

| Pregunta | ¿Hay dato? | Fuente |
|---|---|---|
| Inversión anual, sectores, etapa | ✅ Sí | PECAP (reportes VC) |
| % capital extranjero vs nacional | ✅ Sí (97% extranjero en 2024) | PECAP |
| Ganadores y montos de grants del Estado | ✅ Sí | ProInnóvate / StartUp Perú |
| Perfil del fundador (edad, género, educación, geografía) | ⚠️ Parcial | GEM Perú (ESAN) |
| Supervivencia / tiempo de vida | ⚠️ Débil (hay que construirlo) | Cruce SUNAT/registros + StartUp Perú |
| Retornos / exits reales | ⚠️ Escaso | Prensa + PECAP |
| **Estrato social, respaldo familiar, precariedad** | ❌ **No en bases de startups** | Encuesta propia / microdatos GEM / ENAHO (INEI) |

La capa social —lo más original del proyecto— **no está en ninguna base de startups**.
Se construye con: (a) microdatos del GEM Perú, (b) cruce con la ENAHO del INEI, o (c) una
**encuesta propia a fundadores**. Ver `docs/plan-dashboard.md`.

## Datos duros ya encontrados (2024)
- Inversión VC: **US$ 47M en 33 operaciones**; **97% capital extranjero**; **fintech ~85%** del monto (PECAP).
- ~US$ 300M de VC en Perú en los últimos 4 años.
- StartUp Perú (microdatos 9G–13G, 2022–2026): **2,820 postulaciones**, **1,347 ganadores posibles**; **81 aprobados 2+ veces** (uno en 4 generaciones seguidas). Grants S/ 50k–150k, sin equity.
- Perfil (GEM): edad promedio **37**, **~70% hombres**, **56% con pregrado**, **67% de Lima**.
- Fracaso tech global: ~**63% en 5 años**; LatAm capta solo **1–2%** del VC mundial.

## Estructura del repo
- `data/` — datasets crudos y procesados (CSV/JSON), publicados junto al dashboard.
- `scripts/` — scrapers y pipeline de datos (Python, venv).
- `docs/` — plan del dashboard, fuentes y metodología.
- Ver **`DATA_SOURCES.md`** para el detalle de fuentes y URLs verificadas.

## Enfoque técnico (propuesto)
Pipeline autónomo cron → JSON estático en el repo; dashboard como sitio estático
(Next.js o similar), responsive. Datos versionados en el repo (CSV + JSON).
