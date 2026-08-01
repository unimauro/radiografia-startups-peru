# -*- coding: utf-8 -*-
"""Descarga y parsea las publicaciones de resultados de StartUp Perú (ProInnóvate),
extrae postulante/estado/sector y detecta solicitantes repetidos entre generaciones.

Requiere: pdftotext (poppler) en el PATH. Sin dependencias Python externas.
Salida en ../data/: proinnovate_postulaciones.(csv|json), proinnovate_repetidos.json,
proinnovate_resumen.json
"""
import os, re, json, subprocess, urllib.request, ssl, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
TMP  = os.path.join(HERE, "_pdf")
os.makedirs(TMP, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

# Fuentes: (generación, concurso, año-ciclo, URL). Ampliable.
# (generación, concurso, año, URL, orden de columnas: "ti"=título antes de solicitante / "sol"=al revés)
FUENTES = [
  ("9G",  "EIN", 2022, "https://startup.proinnovate.gob.pe/wp-content/uploads/2023/03/Resultados-Preliminares-Startup-Peru-9G-Emprendimientos-Innovadores-24.03.23.pdf", "ti"),
  ("10G", "EIN", 2023, "https://startup.proinnovate.gob.pe/wp-content/uploads/2023/12/Resultados-Preliminares-Emprendimientos-Innovadores-StartUp-Peru-10G.pdf", "ti"),
  ("11G", "EIN", 2024, "https://startup.proinnovate.gob.pe/wp-content/uploads/2025/05/Resultados-Finales-EI-11G-.pdf", "ti"),
  ("12G", "EIN", 2025, "https://startup.proinnovate.gob.pe/wp-content/uploads/2025/06/Resultados-Preliminares-Emprendimientos-Innovadores-12G.pdf", "ti"),
  ("13G", "EIN", 2025, "https://startup.proinnovate.gob.pe/wp-content/uploads/2026/02/Publicaciones-de-Resultados-EIN-13g.pdf", "ti"),
  # Emprendimientos Dinámicos (EDI)
  ("11G", "EDI", 2024, "https://startup.proinnovate.gob.pe/wp-content/uploads/2025/05/Resultados-Finales-EDI-11G.pdf", "ti"),
  ("13G", "EDI", 2025, "https://startup.proinnovate.gob.pe/wp-content/uploads/2026/02/RESULTADOS_-PRELIMINARES_EMPRENDIMIENTOS_DINAMICOS_13G.pdf", "ti"),
  # PENDIENTE: EDI 7G (2019) usa formato antiguo incompatible (sin columna solicitante, estado
  # "ADMITIDO/Ingresa al comité"): requiere un parser aparte. No se incluye para no meter datos mal parseados.
  # https://www.proinnovate.gob.pe/fincyt/doc/emprendimiento-dinamico/7G/resultados/StartUp_Peru_7G_Resultados_EDI.pdf
  # PLUG — Atracción de Emprendedores del Exterior (programa distinto; columnas invertidas)
  ("PLUG-4G",  "AEE", 2023, "https://startup.proinnovate.gob.pe/wp-content/uploads/2023/10/Resultados-Finales-Atraccion-de-Emprendedores-StartUpPeruPLUG4G.pdf", "sol"),
  ("PLUG-AEE", "AEE", 2024, "https://startup.proinnovate.gob.pe/wp-content/uploads/2024/12/Resultados-Finales-Startup-Peru-PLUG-Atraccion-de-Emprendedores.pdf", "sol"),
]

CODE_RE = re.compile(r'\b([A-Z]{2,4}-\d+-P-\d+-\d+)\b')
ESTADOS = ["Aprobado*", "Aprobado", "Desaprobado", "No admitido", "No Admitido",
           "En Proceso", "Inadmisible", "Desestimado"]

# Clasificador simple por palabras clave del título.
SECTORES = {
  "Fintech": ["fintech","pago","pagos","crédito","credito","finan","billetera","cobr","préstamo","prestamo","seguro","insurtech"],
  "Salud/Healthtech": ["salud","health","médic","medic","clínic","clinic","hospital","paciente","terap","farmac","odontol","psicolog"],
  "Educación/Edtech": ["educ","edtech","aprend","escuela","colegio","curso","enseñ","estudiant","académ","academ"],
  "Agritech/Agro": ["agro","agri","cultivo","cosecha","riego","ganad","pecuar","siembr","fertiliz","café","cafe","cacao"],
  "E-commerce/Retail": ["e-commerce","ecommerce","marketplace","tienda","retail","venta","comercializ","delivery","logíst","logist"],
  "Software/IA": ["software","plataforma digital","app ","aplicaci","inteligencia artificial","ia ","data","dato","saas","automatiz","digital"],
  "Foodtech/Alimentos": ["aliment","food","bebida","gastron","nutri","snack","restauran"],
  "Turismo": ["turismo","turíst","turist","viaj","hotel"],
  "Energía/Ambiental": ["energ","solar","recicl","ambient","sosten","residuo","agua","biomater","eco"],
  "Manufactura/Otros": [],
}
def clasificar(titulo):
    t = titulo.lower()
    for sec, kws in SECTORES.items():
        if any(k in t for k in kws):
            return sec
    return "Manufactura/Otros"

def descargar(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000: return
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=45) as r, open(dest,"wb") as f:
        f.write(r.read())

def pdf_text(path):
    return subprocess.run(["pdftotext","-layout",path,"-"],capture_output=True,text=True).stdout

def parse_pdf(text, gen, concurso, anio, orden="ti"):
    filas = []
    for line in text.splitlines():
        m = CODE_RE.search(line)
        if not m: continue
        codigo = m.group(1)
        cols = [c.strip() for c in re.split(r'\s{2,}', line.strip()) if c.strip()]
        # localizar el código dentro de las columnas
        try: ci = next(i for i,c in enumerate(cols) if CODE_RE.fullmatch(c) or codigo in c)
        except StopIteration: continue
        resto = cols[ci+1:]
        if not resto: continue
        # estado = primera columna que sea un estado conocido
        estado = ""; est_idx = None
        for i,c in enumerate(resto):
            if c in ESTADOS: estado=c; est_idx=i; break
        # dos columnas de texto: la primera tras el código, y la anterior al estado
        col_a = resto[0] if resto else ""
        if est_idx is not None:
            col_b = resto[est_idx-1] if est_idx-1 >= 1 else ""
        else:
            col_b = resto[1] if len(resto) > 1 else ""
        # orden "ti": [título, solicitante]; orden "sol": [solicitante, título]
        titulo, solicitante = (col_a, col_b) if orden == "ti" else (col_b, col_a)
        if solicitante in ESTADOS: solicitante = ""
        if titulo in ESTADOS: titulo = ""
        anio_codigo = "20"+codigo.split("-")[-1] if codigo.split("-")[-1].isdigit() else str(anio)
        filas.append({
            "generacion": gen, "concurso": concurso, "anio": int(anio_codigo),
            "codigo": codigo, "titulo": titulo, "solicitante": solicitante,
            "estado": estado, "aprobado": estado.startswith("Aprobado"),
            "sector": clasificar(titulo),
            "tipo_solicitante": "empresa" if re.search(r'S\.?A\.?C|E\.?I\.?R\.?L|S\.?R\.?L|S\.?A\.?A|\bBIC\b|SOCIEDAD|EMPRESA', solicitante, re.I) else "persona natural",
        })
    return filas

def norm(s): return re.sub(r'\s+',' ',s or '').strip().upper()

def main():
    todo = []
    for gen, concurso, anio, url, orden in FUENTES:
        dest = os.path.join(TMP, f"{gen}_{concurso}.pdf")
        try: descargar(url, dest)
        except Exception as e: print("skip",url,e); continue
        filas = parse_pdf(pdf_text(dest), gen, concurso, anio, orden)
        print(f"{gen} {concurso}: {len(filas)} filas")
        todo += filas

    # guardar postulaciones
    with open(os.path.join(DATA,"proinnovate_postulaciones.json"),"w",encoding="utf-8") as f:
        json.dump({"fuente":"ProInnóvate — publicaciones de resultados","total":len(todo),"filas":todo},
                  f, ensure_ascii=False, indent=1)
    def escribir_csv(path, filas):
        if not filas: return
        cols = list(filas[0].keys())
        with open(path,"w",encoding="utf-8") as f:
            f.write(",".join(cols)+"\n")
            for r in filas:
                f.write(",".join('"'+str(r[c]).replace('"',"'")+'"' for c in cols)+"\n")
    escribir_csv(os.path.join(DATA,"proinnovate_postulaciones.csv"), todo)
    # archivo separado de GANADORES (aprobados en evaluación)
    ganadores = [r for r in todo if r["aprobado"]]
    escribir_csv(os.path.join(DATA,"proinnovate_ganadores.csv"), ganadores)
    with open(os.path.join(DATA,"proinnovate_ganadores.json"),"w",encoding="utf-8") as f:
        json.dump({"nota":"Ganadores = aprobados en evaluación externa (etapa preliminar/final según generación).",
                   "total":len(ganadores),"filas":ganadores}, f, ensure_ascii=False, indent=1)

    # repetidos: mismo solicitante en >1 postulación (y marcar si en >1 generación)
    by = collections.defaultdict(list)
    for r in todo:
        if r["solicitante"]: by[norm(r["solicitante"])].append(r)
    repetidos = []
    for nombre, rs in by.items():
        if len(rs) > 1:
            gens = sorted(set(r["generacion"] for r in rs))
            repetidos.append({
                "solicitante": rs[0]["solicitante"], "postulaciones": len(rs),
                "generaciones": gens, "en_varias_generaciones": len(gens)>1,
                "aprobado_alguna_vez": any(r["aprobado"] for r in rs),
                "veces_aprobado": sum(1 for r in rs if r["aprobado"]),
                "proyectos": [{"gen":r["generacion"],"titulo":r["titulo"],"estado":r["estado"],"anio":r["anio"]} for r in rs],
            })
    repetidos.sort(key=lambda x:(-x["postulaciones"], not x["en_varias_generaciones"]))
    with open(os.path.join(DATA,"proinnovate_repetidos.json"),"w",encoding="utf-8") as f:
        json.dump({"total_solicitantes_repetidos":len(repetidos),
                   "repetidos_en_varias_generaciones":sum(1 for r in repetidos if r["en_varias_generaciones"]),
                   "lista":repetidos}, f, ensure_ascii=False, indent=1)

    # resumen para el dashboard
    def cuenta(key, filtro=lambda r:True):
        c=collections.Counter(r[key] for r in todo if filtro(r)); return dict(c.most_common())
    ganadores_por_gen = collections.Counter(r["generacion"] for r in todo if r["aprobado"])
    resumen = {
        "total_postulaciones": len(todo),
        "total_aprobados": sum(1 for r in todo if r["aprobado"]),
        "generaciones_incluidas": sorted(set(r["generacion"] for r in todo)),
        "por_generacion": cuenta("generacion"),
        "ganadores_por_generacion": dict(ganadores_por_gen),
        "aprobados_por_sector": cuenta("sector", lambda r:r["aprobado"]),
        "por_tipo_solicitante": cuenta("tipo_solicitante"),
        "solicitantes_repetidos": len(repetidos),
        "repetidos_multi_generacion": sum(1 for r in repetidos if r["en_varias_generaciones"]),
    }
    with open(os.path.join(DATA,"proinnovate_resumen.json"),"w",encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
