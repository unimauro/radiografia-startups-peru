# -*- coding: utf-8 -*-
"""Genera la imagen Open Graph (1200x630) para compartir en redes."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "og-image.png")
W, H = 1200, 630
AZUL2 = (31, 78, 121); NARANJA = (224, 138, 74); BLANCO = (255, 255, 255)
CLARO = (215, 228, 242); ACENTO = (224, 185, 138)

img = Image.new("RGB", (W, H), AZUL2)
d = ImageDraw.Draw(img)

# franja superior naranja + círculo tenue (cancha/dato)
d.rectangle([0, 0, W, 12], fill=NARANJA)
d.ellipse([W-360, H-360, W+120, H+120], outline=(46, 110, 90), width=3)

def F(sz, bold=True):
    base = "/System/Library/Fonts/Supplemental/"
    p = base + ("Arial Bold.ttf" if bold else "Arial.ttf")
    try: return ImageFont.truetype(p, sz)
    except Exception: return ImageFont.load_default()

d.text((70, 78),  "OBSERVATORIO ABIERTO · DATOS PÚBLICOS", font=F(26, False), fill=ACENTO)
d.text((70, 138), "Radiografía de las", font=F(78), fill=BLANCO)
d.text((70, 224), "Startups en Perú", font=F(78), fill=BLANCO)
d.text((70, 348), "Inversión, concursos del Estado y perfil del fundador —", font=F(30, False), fill=CLARO)
d.text((70, 388), "la pregunta que casi nadie cruza con datos.", font=F(30, False), fill=CLARO)

# línea de hallazgos destacados
d.rectangle([70, 470, 76, 560], fill=NARANJA)
d.text((96, 470), "97% del capital invertido es extranjero", font=F(30), fill=BLANCO)
d.text((96, 512), "82 recibieron más de un fondo del Estado", font=F(30), fill=BLANCO)

d.text((70, 588), "unimauro.github.io/radiografia-startups-peru", font=F(24, False), fill=(160, 190, 220))

img.save(OUT)
print("Guardado:", OUT, img.size)
