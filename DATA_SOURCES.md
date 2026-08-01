# Fuentes de datos — Radiografía Startups Perú

URLs marcadas con ✅ verificadas (HTTP 200) al 31/07/2026. Las marcadas ⚠️ existen pero
bloquean datacenters o cambian de ruta (revisar manualmente). Sin URL = por confirmar dominio.

## 1. Estado / programas públicos
- ✅ **ProInnóvate — StartUp Perú** · https://startup.proinnovate.gob.pe/
  - Concursos con ganadores públicos: *Emprendimientos Innovadores (EIN)*, *Emprendimientos
    Dinámicos*, *Escalamiento*, y generaciones (8G+, 13G, etc.). Grants S/ 50k–150k, no
    reembolsables, sin equity. → lista de ganadores por generación, sector y región.
  - Otros estímulos de ProInnóvate (además de StartUp Perú): misiones tecnológicas, desarrollo
    empresarial, capital para innovación. Todo bajo el paraguas ProInnóvate/PRODUCE.
- ⚠️ **Datos Abiertos del Estado** · https://www.datosabiertos.gob.pe/ (bloquea bots; abrir manual)
- **INEI** — ENAHO (encuesta de hogares) para cruzar estrato socioeconómico y precariedad laboral.

## 2. Inversión / venture capital
- ✅ **PECAP** (Asociación Peruana de Capital Semilla y Emprendedor) · https://pecap.pe/
  - Reporte anual de VC: montos, número de operaciones, etapa, sector, origen del capital.
  - Dato 2024: US$ 47M en 33 operaciones · 97% capital extranjero · fintech ~85%.
- **LAVCA** — datos regionales de VC en LatAm (agregador, parte de pago).
- **Crunchbase / Dealroom / PitchBook** — agregadores globales (mayormente de pago; útiles para exits).

## 3. Aceleradoras / inversionistas (portafolios públicos)
- ✅ **Wayra** (Telefónica) · https://www.wayra.com/ — portafolio de startups invertidas.
- ✅ **UTEC Ventures** · https://www.utecventures.com/ — aceleradora, cohortes públicas.
- ✅ **Angel Ventures Perú** · https://angelventures.vc/
- ✅ **Salkantay Ventures** · https://salkantay.vc/
- **Endeavor Perú** — scale-ups de alto impacto (confirmar dominio).
- **StartUPC** (UPC), **Emprende UP** (U. del Pacífico), **1551 / PUCP**, **Bit Fund**,
  **Kickstart**, **Winnipeg** — incubadoras/aceleradoras con cohortes públicas (confirmar dominios).

## 4. Perfil del emprendedor / academia
- **GEM Perú** (Global Entrepreneurship Monitor, operado por **ESAN**) — reportes bianuales con
  perfil demográfico y socioeconómico del emprendedor. Dato: edad ~37, ~70% hombres, 56% pregrado,
  67% Lima. **Los microdatos GEM** permiten cortar por estrato/educación/motivación.
- Repositorios académicos (UPC, ESAN, PUCP) — tesis con perfiles de fundadores.

## 5. Trackers del ecosistema
- ⚠️ **StartupBlink** · https://www.startupblink.com/startup-ecosystem/peru (bloquea bots; Perú #67, ~229 startups).
- **ecosistemastartup.com** — notas y cifras del ecosistema peruano.

## Notas de recolección
- Preferir descarga/scraping respetuoso y **guardar los datasets crudos en `data/`** (CSV + JSON).
- Muchas cifras viven en **PDFs** (PECAP, GEM) → extraer con parser y versionar el resultado.
- La **capa social** (estrato, respaldo familiar, precariedad) NO está en estas bases → requiere
  microdatos GEM/ENAHO o **encuesta propia** a fundadores.

## 6. Microdatos parseados (nuevo)
- `scripts/parse_proinnovate.py` — descarga y parsea las publicaciones de resultados de StartUp Perú
  (requiere `pdftotext`/poppler). Genera en `data/`:
  - `proinnovate_postulaciones.(csv|json)` — 1,480 postulaciones (9G 2023 + 13G 2026): código, título,
    solicitante, estado, sector aproximado, tipo de solicitante.
  - `proinnovate_repetidos.json` — solicitantes que postularon/ganaron en más de una generación.
  - `proinnovate_resumen.json` — agregados para el dashboard.
- Ampliable: agregar URLs de 8G, 10G, 11G, 12G en `FUENTES` del script.
- Directorio de incubadoras/aceleradoras de la Red ProInnóvate (38 entidades): PDF en el sitio de ProInnóvate.
