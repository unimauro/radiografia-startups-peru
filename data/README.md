# Datasets — Radiografía Startups Perú

Cifras recopiladas de fuentes públicas (agosto 2026). Cada archivo incluye la fuente.
Las cifras de inversión varían según la fuente y la metodología (año calendario vs. fecha
de reporte, rondas incluidas); se documenta la fuente en cada caso.

## Archivos
- `vc_inversion_anual.csv` / `.json` — Inversión de venture capital por año (US$ millones). Fuente: PECAP (vía Gestión / Bloomberg Línea).
- `capital_origen_sector.json` — Origen del capital (extranjero vs nacional) y concentración por sector, 2024. Fuente: PECAP.
- `startup_peru.json` — Programa StartUp Perú / ProInnóvate: generaciones, ganadores e inversión histórica. Fuente: ProInnóvate / gob.pe.
- `perfil_fundador_gem.json` — Perfil del fundador. Fuente: GEM Perú (ESAN) / Gestión.
- `ecosistema.json` — Indicadores del ecosistema. Fuentes: StartupBlink, PECAP, prensa.

## Nota sobre la "capa social"
El estrato social de origen, el respaldo familiar y la precariedad laboral de los fundadores
NO están en estas fuentes. Requieren microdatos GEM/ENAHO o una encuesta propia (ver
`../docs/plan-dashboard.md`).
