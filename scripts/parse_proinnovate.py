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
FUENTES = [
  ("9G",  "EIN", 2023, "https://startup.proinnovate.gob.pe/wp-content/uploads/2023/03/Resultados-Preliminares-Startup-Peru-9G-Emprendimientos-Innovadores-24.03.23.pdf"),
  ("13G", "EIN", 2026, "https://startup.proinnovate.gob.pe/wp-content/uploads/2026/02/Publicaciones-de-Resultados-EIN-13g.pdf"),
  ("13G", "EDI", 2026, "https://startup.proinnovate.gob.pe/wp-content/uploads/2026/02/Publicaciones-de-Resultados-EDI-13g.pdf"),
]

CODE_RE = re.compile(r'\b(E[ID][IN]-\d+-P-\d+-\d+)\b')
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

def parse_pdf(text, gen, concurso, anio):
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
        titulo = resto[0] if len(resto)>0 else ""
        # solicitante = la columna inmediatamente anterior al estado.
        # Si el estado va pegado al título (est_idx<=1) no hay solicitante identificable.
        if est_idx is not None:
            solicitante = resto[est_idx-1] if est_idx-1 >= 1 else ""
        else:
            solicitante = resto[1] if len(resto) > 1 else ""
        if solicitante in ESTADOS:  # nunca confundir estado con solicitante
            solicitante = ""
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
    for gen, concurso, anio, url in FUENTES:
        dest = os.path.join(TMP, f"{gen}_{concurso}.pdf")
        try: descargar(url, dest)
        except Exception as e: print("skip",url,e); continue
        filas = parse_pdf(pdf_text(dest), gen, concurso, anio)
        print(f"{gen} {concurso}: {len(filas)} filas")
        todo += filas

    # guardar postulaciones
    with open(os.path.join(DATA,"proinnovate_postulaciones.json"),"w",encoding="utf-8") as f:
        json.dump({"fuente":"ProInnóvate — publicaciones de resultados","total":len(todo),"filas":todo},
                  f, ensure_ascii=False, indent=1)
    if todo:
        cols = list(todo[0].keys())
        with open(os.path.join(DATA,"proinnovate_postulaciones.csv"),"w",encoding="utf-8") as f:
            f.write(",".join(cols)+"\n")
            for r in todo:
                f.write(",".join('"'+str(r[c]).replace('"',"'")+'"' for c in cols)+"\n")

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
    resumen = {
        "total_postulaciones": len(todo),
        "total_aprobados": sum(1 for r in todo if r["aprobado"]),
        "por_generacion": cuenta("generacion"),
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
