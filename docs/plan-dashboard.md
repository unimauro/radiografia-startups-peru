# Plan del dashboard — Radiografía Startups Perú

Dashboard en secciones. Cada una indica de dónde sale el dato y qué tan sólido es.

## Sección 1 — El dinero (capa dura) ✅
- Inversión VC por año (línea de tiempo). *Fuente: PECAP.*
- **Capital peruano vs extranjero** (el hallazgo fuerte: 97% extranjero en 2024).
- Inversión por sector (fintech domina) y por etapa (semilla vs crecimiento).
- Comparativo Perú vs LatAm (Perú capta poco del VC regional).

## Sección 2 — Los ganadores del Estado (capa dura) ✅
- Ganadores de StartUp Perú por generación, sector y región. *Fuente: ProInnóvate.*
- Monto de grants entregados y evolución en el tiempo.
- Concentración: ¿cuánto se va a Lima vs regiones?
- **¿Viven de concursos?** Cruce: startups que solo aparecen como ganadoras de grants vs las que
  además levantaron inversión privada (PECAP/aceleradoras).

## Sección 3 — Aceleradoras e inversionistas ✅/⚠️
- Portafolios de Wayra, UTEC Ventures, Angel Ventures, Salkantay, Endeavor, etc.
- ¿Cuántas startups pasan por aceleradora antes de levantar capital? ¿Cuáles emigraron
  (se domiciliaron en Delaware/Chile/México) para levantar más?

## Sección 4 — ¿Quién emprende? (radiografía del fundador) ⚠️
- Edad, género, educación, carrera, geografía. *Fuente: GEM Perú.*
- Universidades de origen de los fundadores exitosos.

## Sección 5 — Supervivencia y retorno (capa débil, hay que construir) ⚠️
- Tiempo de vida de las startups (cruce registros + año de fundación).
- Exits/retornos conocidos (prensa + PECAP). Ser honestos: el dato es escaso.

## Sección 6 — La capa social (LA TESIS FUERTE — requiere datos primarios) ❌→🔬
Lo más original y lo que nadie cruza con datos:
- **Estrato social de origen** de los fundadores que lograron salir adelante.
- **Respaldo familiar vs precariedad**: ¿es lo mismo emprender teniendo la vida cubierta
  (familia que apoya, sin gastos corrientes urgentes) que sin ese colchón?
- Hipótesis a testear: *el "éxito" startup está sesgado hacia quienes pudieron permitirse el
  riesgo* (colchón familiar, educación privada, Lima), más que hacia el mérito puro.

**Cómo obtener el dato (no está en bases de startups):**
1. **Microdatos GEM Perú** (cortar por nivel socioeconómico, educación, motivación de necesidad vs oportunidad).
2. **Cruce con ENAHO (INEI)** para contextualizar estrato/precariedad laboral.
3. **Encuesta propia** a fundadores (la vía más directa para la tesis): estrato de origen,
   si tenían empleo/ingreso paralelo, respaldo familiar, gastos que cubrir al emprender.

## Roadmap sugerido
1. **Fase A — Datos duros (rápido):** scrapear ganadores ProInnóvate + parsear reportes PECAP →
   secciones 1, 2, 3. Es lo que se puede publicar primero y ya cuenta una historia.
2. **Fase B — Radiografía:** integrar GEM (sección 4) y construir supervivencia (sección 5).
3. **Fase C — Capa social:** diseñar y correr la encuesta a fundadores (sección 6) + cruce ENAHO.

## Técnico
- Pipeline en `scripts/` (Python + venv): scrapers → CSV/JSON crudos en `data/`.
- Dashboard estático (Next.js o Astro), responsive, consumiendo JSON del repo.
- Todo versionado: dataset crudo + procesado publicados junto al dashboard.
