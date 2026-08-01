# -*- coding: utf-8 -*-
"""Genera la imagen Open Graph (1200x630): tono sarcástico y peruano —
fundador jalándose los pelos, un cohete con los colores del Perú que no despega,
y una gráfica que cae. Solo requiere Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "og-image.png")
W, H = 1200, 630

BLUE_T=(16,44,72); BLUE_B=(31,78,121)
WHITE=(255,255,255); CREAM=(200,220,240)
ORANGE=(233,150,80); GOLD=(224,185,138)
RED=(206,42,54)                      # rojo bandera Perú
SKIN=(244,208,175); SKIN_D=(206,168,135)
PANEL=(244,248,252); PANEL_LINE=(206,220,234); MUTED=(120,136,158); DARK=(28,42,60)
SWEAT=(90,180,235)

img=Image.new("RGB",(W,H),BLUE_T); d=ImageDraw.Draw(img)
for y in range(H):                                   # degradado vertical
    t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(BLUE_T[i]+(BLUE_B[i]-BLUE_T[i])*t) for i in range(3)))
d.rectangle([0,0,W,9],fill=RED); d.rectangle([0,H-9,W,H],fill=RED)   # franjas Perú

def F(sz,bold=True):
    base="/System/Library/Fonts/Supplemental/"
    try: return ImageFont.truetype(base+("Arial Bold.ttf" if bold else "Arial.ttf"),sz)
    except Exception: return ImageFont.load_default()

def rrect(box,r,fill):
    x0,y0,x1,y1=box
    d.rectangle([x0+r,y0,x1-r,y1],fill=fill); d.rectangle([x0,y0+r,x1,y1-r],fill=fill)
    for cx,cy in [(x0+r,y0+r),(x1-r,y0+r),(x0+r,y1-r),(x1-r,y1-r)]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=fill)

# ---------------- TEXTO (izquierda) ----------------
d.text((70,64),"OBSERVATORIO ABIERTO · DATOS PÚBLICOS",font=F(23),fill=GOLD)
d.text((66,112),"Radiografía de las",font=F(70),fill=WHITE)
d.text((66,186),"Startups en Perú",font=F(70),fill=WHITE)
d.text((70,296),"Premiada. Subsidiada.",font=F(33),fill=ORANGE)
d.text((70,336),"Y todavía sin despegar.",font=F(33),fill=ORANGE)
d.rectangle([70,404,75,492],fill=ORANGE)
d.text((92,400),"97% del capital invertido es extranjero",font=F(26),fill=WHITE)
d.text((92,438),"S/ 268M en fondos… y 82 cobraron más de 1 vez",font=F(26),fill=WHITE)
d.text((70,566),"unimauro.github.io/radiografia-startups-peru",font=F(21,False),fill=(155,188,220))

# ---------------- ESCENA CÓMIC (derecha) ----------------
# --- gráfica que cae ---
cx0,cy0,cx1,cy1=772,110,1150,336
rrect([cx0,cy0,cx1,cy1],18,PANEL)
d.text((cx0+26,cy0+16),"tracción",font=F(19),fill=MUTED)
for gy in range(cy0+66,cy1-16,44): d.line([(cx0+30,gy),(cx1-22,gy)],fill=PANEL_LINE,width=2)
d.line([(cx0+30,cy0+40),(cx0+30,cy1-26)],fill=MUTED,width=3)
d.line([(cx0+30,cy1-26),(cx1-22,cy1-26)],fill=MUTED,width=3)
pts=[(cx0+42,cy0+66),(cx0+120,cy0+120),(cx0+200,cy0+96),(cx0+300,cy1-40)]  # sube y se desploma
d.line(pts,fill=RED,width=7,joint="curve")
ex,ey=pts[-1]                                            # punta de flecha hacia abajo
d.polygon([(ex-14,ey-16),(ex+14,ey-16),(ex,ey+8)],fill=RED)

# --- cohete peruano que NO despega (tumbado, chisporroteando) ---
rx,ry=880,506
d.line([(rx-70,ry+34),(rx+95,ry+34)],fill=(60,86,120),width=4)   # suelo/thud
for sx in (rx-40,rx-8,rx+30):                                     # rayitas de golpe
    d.line([(sx,ry+42),(sx+14,ry+52)],fill=(80,110,150),width=3)
d.polygon([(rx-46,ry-24),(rx-46,ry+24),(rx-88,ry)],fill=RED)      # cono (izq)
rrect([rx-46,ry-24,rx+52,ry+24],20,WHITE)                         # cuerpo
d.rectangle([rx-46,ry-24,rx-22,ry+24],fill=RED)                   # banda roja
d.rectangle([rx+30,ry-24,rx+52,ry+24],fill=RED)                   # banda roja (bandera r-b-r)
d.polygon([(rx+50,ry-24),(rx+74,ry-38),(rx+52,ry-6)],fill=(120,120,140))  # aletas
d.polygon([(rx+50,ry+24),(rx+74,ry+38),(rx+52,ry+6)],fill=(120,120,140))
d.ellipse([rx-8,ry-13,rx+18,ry+13],fill=(150,205,238))           # ventana
d.ellipse([rx-2,ry-5,rx+3,ry],fill=DARK); d.ellipse([rx+8,ry-5,rx+13,ry],fill=DARK)  # ojos :(
d.arc([rx-1,ry+2,rx+13,ry+12],200,340,fill=DARK,width=2)         # boca triste
for i,(px,py,pr) in enumerate([(rx+86,ry,11),(rx+104,ry-9,7),(rx+104,ry+11,6)]):     # humito (no fuego)
    d.ellipse([px-pr,py-pr,px+pr,py+pr],fill=(205,210,220))

# --- fundador jalándose los pelos ---
hx,hy=1010,432; r=54
d.polygon([(hx-62,548),(hx+62,548),(hx+42,496),(hx-42,496)],fill=(64,116,168))  # camiseta
d.rectangle([hx-13,472,hx+13,500],fill=SKIN_D)                                  # cuello
d.ellipse([hx-r,hy-r,hx+r,hy+r],fill=SKIN)                                      # cabeza
for a in (-34,-20,-6,8,22):                                                     # pelos parados
    d.line([(hx+a,hy-r+6),(hx+a-4,hy-r-24)],fill=DARK,width=4)
for fx,fy in [(hx-70,hy-70),(hx+72,hy-64)]:                                     # pelos volando
    d.line([(fx,fy),(fx+16,fy-10)],fill=DARK,width=3)
    d.line([(fx+4,fy+8),(fx+20,fy+2)],fill=DARK,width=3)
d.ellipse([hx-30,hy-6,hx-14,hy+8],fill=WHITE); d.ellipse([hx+14,hy-6,hx+30,hy+8],fill=WHITE)  # ojos
d.ellipse([hx-25,hy-3,hx-18,hy+5],fill=DARK); d.ellipse([hx+19,hy-3,hx+26,hy+5],fill=DARK)
d.line([(hx-32,hy-14),(hx-14,hy-8)],fill=DARK,width=3); d.line([(hx+32,hy-14),(hx+14,hy-8)],fill=DARK,width=3)  # cejas
d.ellipse([hx-9,hy+18,hx+9,hy+34],fill=(150,60,60))            # boca gritando
for (sx,sy) in [(hx-r-6,hy-8),(hx+r+2,hy-2)]:                  # gotas de sudor
    d.polygon([(sx,sy-12),(sx-7,sy+4),(sx+7,sy+4)],fill=SWEAT); d.ellipse([sx-7,sy-2,sx+7,sy+12],fill=SWEAT)
d.ellipse([hx-r-4,hy-r-4,hx+r+4,hy+r+4],outline=None)
# manos agarrando la cabeza
for mx,my in [(hx-r+6,hy-r+18),(hx+r-6,hy-r+18)]:
    d.ellipse([mx-17,my-17,mx+17,my+17],fill=SKIN)
    for k in range(4): d.line([(mx-12+k*8,my-14),(mx-12+k*8,my-24)],fill=SKIN_D,width=4)
# marcas de estrés (rojas)
for (ex2,ey2) in [(hx-r-22,hy-r+6),(hx+r+16,hy-r+2)]:
    d.line([(ex2,ey2),(ex2-12,ey2-10)],fill=RED,width=3); d.line([(ex2+6,ey2+6),(ex2-6,ey2+16)],fill=RED,width=3)

img.save(OUT); print("Guardado:",OUT,img.size)
