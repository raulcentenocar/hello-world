#!/usr/bin/env python3
"""
F4 - Dibujo DXF de la variante V1 "Calle de casas" (reglas fijas, sin IA).
Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Canada).

Genera en planos/:
  V1_implantacion.dxf       implantacion en UTM ETRS89 30N (EPSG:25830), con capa CONFLICTOS_F3
  V1_casa_tipo.dxf          casa U-V1 de 6,50 x 12,00 m: planta baja y planta primera (esquematicas)
  V1_bloque_planta_tipo.dxf bloque M-V1: planta tipo (P1 y P2) y planta baja esquematica

Toda la geometria sale de fases/ (se cita la fuente en cada dato). Lo que no tiene cota
en los entregables va en la capa POSICION_APROXIMADA. Los conflictos de F3 NO se resuelven:
se dibuja lo ultimo aprobado (F2/F3) y se marcan en la capa CONFLICTOS_F3.

Uso (desde la raiz del repositorio):
    python3 scripts/dibujo_v1.py
Dependencias: ezdxf >= 1.1, shapely >= 2.0 (scripts/requirements.txt)
"""
import os

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, box

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANOS = os.path.join(RAIZ, "planos")
FECHA = "2026-11-16"
AVISO = "PENDIENTE DE VALIDAR POR EL ARQUITECTO"

# =============================================================== DATOS (de fases/)
# 01_urbanismo 1.4: vertices UTM; 02_diseno 1.3: origen local en el vertice 3, x este, y norte
ORIGEN_UTM = (414896.93, 4478781.24)
VERTICES_LOCAL = [  # 02_diseno 1.3 (V1..V6)
    (91.85, 73.52), (91.85, 0.76), (0.0, 0.0), (-31.45, 96.66), (-2.47, 93.07), (71.90, 77.05)]
LINDEROS = [  # 01_urbanismo 1.5 (lado i: vertice i+1 -> i+2)
    "UA-03-02 (lindero este) · recta · 71,30 m en cédula (cuerda 72,76 m)",
    "AVDA. DE LA DEHESA (fachada) · curva R 433 · 92,02 m · se dibuja la CUERDA",
    "CALLE FLORISTAS (fachada, accesos) · recta · 101,65 m",
    "ZV-02 tramo 1 · curva R 100 · 29,30 m · se dibuja la CUERDA",
    "ZV-02 tramo 2 · curva R 669,75 · 76,12 m · se dibuja la CUERDA",
    "ZV-02 tramo 3 · curva R 500 · 20,26 m · se dibuja la CUERDA",
]
RETRANQUEOS = [3.0, 5.0]  # 01_urbanismo 2.2: unifamiliar 3 m / multifamiliar 5 m en todos los lados

# Casas U-V1 (02_diseno 2.1 y 2.2): 6,50 x 12,00 m. Numeracion de esquema_V1.svg (oeste -> este)
ANCHO_CASA, FONDO_CASA = 6.50, 12.00
HILERAS = [  # (nombre, x0, n casas, y_sur, banda, 1er numero)
    ("A-oeste (Ag-1)", 2.0, 8, 9.0, "A", 1),
    ("A-este (Ag-3)", 60.0, 4, 9.0, "A", 9),
    ("B-oeste (Ag-2)", -2.5, 4, 37.0, "B", 13),
    ("B-centro (Ag-2)", 29.5, 4, 37.0, "B", 17),
    ("B-este (Ag-3)", 61.5, 4, 37.0, "B", 21),
]
E_MURO = 0.24            # 03_estructura 1.1: medianera / testero de 24 cm
JUNTA_X = 28.0           # 03_estructura 1.3: junta entre viviendas 4 y 5, doble muro 2 x 0,24 + 0,03
# Viario y aparcamiento (02_diseno 2.1, 2.5; poligonos hasta la cuerda de Floristas, esquema_V1.svg)
CALLE_CASAS = [(-8.46, 26), (88, 26), (88, 32), (-10.41, 32)]
CALLE_BOLSA = [(-20.17, 62), (13.5, 62), (13.5, 68), (-22.12, 68)]
PLAZA = (2.50, 5.00)     # H-APA-1
# Bloque M-V1 (02_diseno 2.1; 03_estructura 2.2 reticula ajustada)
BLOQUE = (19.5, 61.0, 57.0, 73.0)
EJES_X = [19.75 + i * 37.0 / 6 for i in range(7)]          # 1..7
EJES_Y = {"A": 61.25, "B": 67.00, "C": 72.75}
# Nucleos y patinillos: POSICION APROXIMADA (esquema_V1.svg; F2 solo dice "entre ejes 2-3 y 5-6")
NUCLEOS = [(EJES_X[1], 64.75, EJES_X[2], 69.25), (EJES_X[4], 64.75, EJES_X[5], 69.25)]
PATINILLOS_BLOQUE = [("PB-1", EJES_X[1]), ("PB-2", EJES_X[2]), ("PB-3", EJES_X[4]), ("PB-4", EJES_X[5])]


def to_utm(p):
    return (ORIGEN_UTM[0] + p[0], ORIGEN_UTM[1] + p[1])


def y_sur(x):
    """Cuerda de la Avda. de la Dehesa (02_diseno 1.3): y = 0,0083 x (V3 -> V2)."""
    return 0.76 / 91.85 * x


def casas():
    """Lista de casas: dict con numero, hilera, banda, x0, y0 (esquina SO)."""
    res = []
    for nombre, x0, n, ys, banda, n0 in HILERAS:
        for i in range(n):
            res.append(dict(num=n0 + i, hilera=nombre, banda=banda, x0=x0 + i * ANCHO_CASA, y0=ys))
    return res


def pilares():
    """03_estructura 4.2: esquina 30x30, fachada larga 30x40 (40 perpendicular a fachada),
    testero B1/B7 30x40 (40 perpendicular al testero), interior 40x40. Centrados en los ejes."""
    res = []
    for i, x in enumerate(EJES_X):
        for ej, y in EJES_Y.items():
            ext_x = i in (0, 6)
            if ej in ("A", "C") and ext_x:
                dx, dy, tipo = 0.30, 0.30, "esquina 30x30"
            elif ej in ("A", "C"):
                dx, dy, tipo = 0.30, 0.40, "fachada 30x40"
            elif ext_x:
                dx, dy, tipo = 0.40, 0.30, "testero 30x40"
            else:
                dx, dy, tipo = 0.40, 0.40, "interior 40x40"
            res.append(dict(nombre=f"{ej}{i + 1}", x=x, y=y, dx=dx, dy=dy, tipo=tipo))
    return res


# =============================================================== utilidades DXF
CAPAS = {  # nombre: (color ACI, tipo de linea)
    "U-PARCELA": (7, "Continuous"), "U-RETRANQUEO": (8, "DASHED"), "U-VIARIO": (9, "Continuous"),
    "U-PLAZA": (8, "Continuous"), "U-PLAZA-ACCESIBLE": (5, "Continuous"), "U-JARDIN": (3, "Continuous"),
    "U-PEATONAL": (40, "Continuous"), "A-CASA": (30, "Continuous"), "A-CASA-NUM": (7, "Continuous"),
    "A-MURO": (7, "Continuous"), "A-TABIQUE": (8, "Continuous"), "A-CARPINTERIA": (4, "Continuous"),
    "A-BLOQUE": (7, "Continuous"), "S-EJE": (5, "CENTER"), "S-PILAR": (1, "Continuous"),
    "S-VIGA": (1, "DASHED"), "I-PATINILLO": (6, "Continuous"), "A-COTA": (2, "Continuous"),
    "A-TEXTO": (7, "Continuous"), "A-CAJETIN": (7, "Continuous"),
    "POSICION_APROXIMADA": (200, "DASHED"), "CONFLICTOS_F3": (1, "Continuous"),
}


def nuevo_doc(capas):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.M
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LTSCALE"] = 0.05
    for c in capas:
        color, lt = CAPAS[c]
        doc.layers.add(c, color=color, linetype=lt)
    return doc


class Dib:
    def __init__(self, doc, tf=lambda p: p):
        self.doc, self.msp, self.tf = doc, doc.modelspace(), tf

    def pl(self, pts, capa, cerrada=True):
        return self.msp.add_lwpolyline([self.tf(p) for p in pts], close=cerrada, dxfattribs={"layer": capa})

    def rect(self, x0, y0, x1, y1, capa):
        return self.pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], capa)

    def linea(self, a, b, capa):
        return self.msp.add_line(self.tf(a), self.tf(b), dxfattribs={"layer": capa})

    def circulo(self, c, r, capa):
        return self.msp.add_circle(self.tf(c), r, dxfattribs={"layer": capa})

    def texto(self, s, p, h, capa, rot=0.0, al=TextEntityAlignment.MIDDLE_CENTER):
        t = self.msp.add_text(s, height=h, rotation=rot, dxfattribs={"layer": capa})
        t.set_placement(self.tf(p), align=al)
        return t

    def izq(self, s, p, h, capa):
        return self.texto(s, p, h, capa, al=TextEntityAlignment.LEFT)

    def cota(self, p1, p2, base, vertical=False, txt=0.6):
        medida = abs(p2[1] - p1[1]) if vertical else abs(p2[0] - p1[0])
        d = self.msp.add_linear_dim(
            base=self.tf(base), p1=self.tf(p1), p2=self.tf(p2), angle=90 if vertical else 0,
            text=cota_txt(medida),
            dxfattribs={"layer": "A-COTA"},
            override={"dimlfac": 1.0, "dimtxt": txt, "dimasz": txt * 0.6, "dimexo": 0.2, "dimexe": 0.3, "dimdec": 2,
                      "dimdsep": 44, "dimgap": 0.1, "dimclrd": 2, "dimclre": 2, "dimtad": 1})
        d.render()

    def conflicto(self, cod, c, r=1.6, h=0.9):
        self.circulo(c, r, "CONFLICTOS_F3")
        self.texto(cod, c, h, "CONFLICTOS_F3")

    def cajetin(self, x0, y0, titulo, lineas, escala, w=80.0):
        k = w / 80.0  # los textos escalan con el ancho del cajetin
        h_l = 1.6 * k
        alto = (12 + 1.6 * len(lineas)) * k
        self.rect(x0, y0, x0 + w, y0 + alto, "A-CAJETIN")
        self.linea((x0, y0 + 5 * k), (x0 + w, y0 + 5 * k), "A-CAJETIN")
        self.texto(AVISO, (x0 + w / 2, y0 + 2.5 * k), 1.6 * k, "A-CAJETIN")
        y = y0 + alto - 2.2 * k
        self.izq(titulo, (x0 + k, y), 1.4 * k, "A-CAJETIN")
        y -= 2.4 * k
        for ln in [f"Escala {escala} · unidades del dibujo: metros · F4 dibujo · {FECHA}"] + lineas:
            self.izq(ln, (x0 + k, y), 0.8 * k, "A-CAJETIN")
            y -= h_l


def cota_txt(v):
    return f"{v:.2f}".replace(".", ",")


# =============================================================== 1. IMPLANTACION (UTM)
CONFLICTOS_IMPL = [  # codigo, posicion local (como esquema_V1.svg), resumen (conflictos.md)
    ("N-1", (85.0, 29.0), "Fondo de saco ≈ 98 m sin espacio de maniobra de bomberos (SI 5-1.2.4)"),
    ("N-2", (14.0, 29.0), "Calle de casas sin acera: itinerario accesible por la calzada (SUA 9)"),
    ("E1", (28.0, 15.0), "Junta de dilatación x = 28,0: doble muro 0,51 m resta ≈ 0,27 m a viviendas 4 y 5"),
    ("E3", (59.5, 67.0), "Cota PB +0,30 / forjado sanitario / cornisa bloque ≈ 9,7-10,25 m frente a 10 m"),
    ("E4/I-3/N-4", (EJES_X[1] + 3.08, 71.3), "Patinillos PB-1/PB-2 en zona 6d de punzonamiento y junto a meseta"),
    ("E4/I-3/N-4", (EJES_X[4] + 3.08, 71.3), "Patinillos PB-3/PB-4 en zona 6d de punzonamiento y junto a meseta"),
    ("E6", (44.0, 23.5), "Plazas en batería contra fachadas y medianeras: impacto 50 kN / topes"),
    ("I-8", (89.5, 10.5), "≈ 243 kW > 100 kW: posible CT sin reserva; elemento SE sin identificar"),
    ("I-9", (32.5, 58.6), "Armario de contadores en el portal 1 (recorrido de evacuación)"),
    ("I-9", (51.0, 58.6), "Armario de contadores en el portal 2 (recorrido de evacuación)"),
    ("NC-1", (25.5, 58.6), "Entrada accesible del bloque sin resolver (PB +0,30, sin rampa) - portal 1"),
    ("NC-1", (44.0, 58.6), "Entrada accesible del bloque sin resolver (PB +0,30, sin rampa) - portal 2"),
    ("NC-5", (16.3, 57.0), "Trazado F2 con 1 plaza accesible frente a las 2 aprobadas"),
]


def dibujar_implantacion():
    doc = nuevo_doc([c for c in CAPAS if c not in ("A-TABIQUE", "A-CARPINTERIA", "S-VIGA", "I-PATINILLO")])
    d = Dib(doc, to_utm)
    # Parcela y vertices
    d.pl(VERTICES_LOCAL, "U-PARCELA")
    for i, v in enumerate(VERTICES_LOCAL):
        d.circulo(v, 0.4, "U-PARCELA")
        u = to_utm(v)
        d.izq(f"V{i + 1}  X {u[0]:.2f}  Y {u[1]:.2f}".replace(".", ","), (v[0] + 0.8, v[1] + 0.8), 0.7, "U-PARCELA")
    n = len(VERTICES_LOCAL)
    import math
    for i in range(n):
        a, b = VERTICES_LOCAL[i], VERTICES_LOCAL[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        if ang > 90 or ang < -90:
            ang += 180
        # desplazar el rotulo hacia fuera de la parcela
        nx, ny = (b[1] - a[1]), -(b[0] - a[0])
        L = math.hypot(nx, ny)
        d.texto(f"Lado {i}: {LINDEROS[i]}", (mx - 2.5 * nx / L, my - 2.5 * ny / L), 0.9, "U-PARCELA", rot=ang)
    # Retranqueos (offset interior de las cuerdas con shapely, juntas en inglete)
    parcela = Polygon(VERTICES_LOCAL)
    for r in RETRANQUEOS:
        off = parcela.buffer(-r, join_style="mitre")
        d.pl(list(off.exterior.coords)[:-1], "U-RETRANQUEO")
    d.texto("retranqueo 3 m (unifamiliar)", (45, 3.6 + 0.9), 0.7, "U-RETRANQUEO")
    d.texto("retranqueo 5 m (multifamiliar)", (45, 5.6 + 0.9), 0.7, "U-RETRANQUEO")
    # Viario
    d.pl(CALLE_CASAS, "U-VIARIO")
    d.pl(CALLE_BOLSA, "U-VIARIO")
    d.texto("CALLE DE CASAS · calzada 6,00 m · fondo de saco ≈ 98 m · sin acera (F2 2.1)", (40, 29), 0.9, "A-TEXTO")
    d.texto("BOLSA DEL BLOQUE · maniobra 6,00 m", (-3.5, 65), 0.8, "A-TEXTO")
    d.texto("acceso rodado 1", (-27, 65), 0.8, "A-TEXTO")
    d.texto("acceso rodado 2", (-15, 29), 0.8, "A-TEXTO")
    # Pasos peatonales (6 m entre hileras)
    d.pl([(54, y_sur(54)), (60, y_sur(60)), (60, 21), (54, 21)], "U-PEATONAL")
    d.rect(23.5, 32, 29.5, 55, "U-PEATONAL")
    d.rect(55.5, 32, 61.5, 55, "U-PEATONAL")
    # Casas, jardines privados, plazas a la puerta
    lista = casas()
    for c in lista:
        x0, y0 = c["x0"], c["y0"]
        d.rect(x0, y0, x0 + ANCHO_CASA, y0 + FONDO_CASA, "A-CASA")
        d.texto(str(c["num"]), (x0 + 3.25, y0 + 6), 2.0, "A-CASA-NUM")
        if c["banda"] == "A":
            d.pl([(x0, y_sur(x0)), (x0 + 6.5, y_sur(x0 + 6.5)), (x0 + 6.5, 9), (x0, 9)], "U-JARDIN")
            yp = 21.0
        else:
            d.rect(x0, 49, x0 + 6.5, 55, "U-JARDIN")
            yp = 32.0
        # 2 plazas de 2,50 x 5,00 + paso de 1,50 m (F2 2.5); orden dentro del frente: aproximado
        d.rect(x0, yp, x0 + 2.5, yp + 5, "U-PLAZA")
        d.rect(x0 + 2.5, yp, x0 + 5.0, yp + 5, "U-PLAZA")
        d.rect(x0 + 5.0, yp, x0 + 6.5, yp + 5, "U-PEATONAL")
    d.texto("jardines privados (F2 2.1)", (20, 5.6), 0.6, "A-TEXTO")
    d.texto("orden plazas / paso de 1,50 m dentro de cada frente: aproximado", (40, 20.3), 0.6, "POSICION_APROXIMADA")
    # Medianeras, testeros y junta
    for nombre, x0, nn, ys, banda, n0 in HILERAS:
        x1 = x0 + nn * ANCHO_CASA
        d.rect(x0, ys, x0 + E_MURO, ys + FONDO_CASA, "A-MURO")       # testero oeste (cara ext. = envolvente)
        d.rect(x1 - E_MURO, ys, x1, ys + FONDO_CASA, "A-MURO")       # testero este
        for k in range(1, nn):
            xm = x0 + k * ANCHO_CASA
            if abs(xm - JUNTA_X) < 1e-6 and ys == 9.0:
                d.rect(xm - 0.255, ys, xm - 0.015, ys + FONDO_CASA, "A-MURO")
                d.rect(xm + 0.015, ys, xm + 0.255, ys + FONDO_CASA, "A-MURO")
            else:
                d.rect(xm - E_MURO / 2, ys, xm + E_MURO / 2, ys + FONDO_CASA, "A-MURO")
        d.texto(f"Hilera {nombre} · {nn} casas · {cota_txt(nn * ANCHO_CASA)} m",
                (x0 + nn * 3.25, 1.6 + y_sur(x0) if banda == "A" else ys + FONDO_CASA + 1.0 + 6), 0.8, "A-TEXTO")
    d.texto("JD x = 28,0 (doble muro 2 × 0,24 + 0,03)", (28, 22.6 - 1.6), 0.6, "A-TEXTO")
    # Bolsa del bloque: fila sur 9 plazas + 1 accesible (3,70 m), fila norte 12 plazas (F2 2.5)
    for i in range(9):
        d.rect(-13.3 + 2.5 * i, 57, -10.8 + 2.5 * i, 62, "U-PLAZA")
    d.rect(9.8, 57, 11.0, 62, "U-PLAZA-ACCESIBLE")   # transferencia 1,20
    d.rect(11.0, 57, 13.5, 62, "U-PLAZA-ACCESIBLE")  # plaza 2,50 x 5,00
    d.texto("PMR", (12.25, 59.5), 0.8, "U-PLAZA-ACCESIBLE")
    d.texto("posición de la plaza accesible en la fila: aproximada (extremo este, 03_normativa)", (0, 55.8), 0.55,
            "POSICION_APROXIMADA")
    for i in range(12):
        d.rect(-16.9 + 2.5 * i, 68, -14.4 + 2.5 * i, 73, "U-PLAZA")
    # Bloque
    bx0, by0, bx1, by1 = BLOQUE
    d.rect(bx0, by0, bx1, by1, "A-BLOQUE")
    d.texto("BLOQUE M-V1 · 12,00 × 37,50 m · PB + 2 · 10 viviendas · 2 portales", (38.25, 75.2), 0.9, "A-TEXTO")
    for i, x in enumerate(EJES_X):
        d.linea((x, 59.6), (x, 74.4), "S-EJE")
        d.circulo((x, 58.9), 0.6, "S-EJE")
        d.texto(str(i + 1), (x, 58.9), 0.6, "S-EJE")
    for ej, y in EJES_Y.items():
        d.linea((18.4, y), (58.4, y), "S-EJE")
        d.circulo((17.7, y), 0.6, "S-EJE")
        d.texto(ej, (17.7, y), 0.6, "S-EJE")
    for p in pilares():
        d.rect(p["x"] - p["dx"] / 2, p["y"] - p["dy"] / 2, p["x"] + p["dx"] / 2, p["y"] + p["dy"] / 2, "S-PILAR")
    for k, (x0, y0, x1, y1) in enumerate(NUCLEOS):
        d.rect(x0, y0, x1, y1, "POSICION_APROXIMADA")
        d.texto(f"núcleo {k + 1} (aprox.)", ((x0 + x1) / 2, (y0 + y1) / 2), 0.6, "POSICION_APROXIMADA")
    for nom, x in PATINILLOS_BLOQUE:
        d.rect(x - 0.5, 68.1, x + 0.5, 68.7, "POSICION_APROXIMADA")
    for k, x in enumerate([29.0, 47.5]):  # portales: F2 "uno en cada mitad"; fachada sur aproximada
        d.linea((x, 57.4), (x, 61.0), "POSICION_APROXIMADA")
        d.pl([(x - 0.4, 60.2), (x + 0.4, 60.2), (x, 61.0)], "POSICION_APROXIMADA")
        d.texto(f"portal {k + 1} (aprox.)", (x, 56.8), 0.55, "POSICION_APROXIMADA")
    # Otros elementos aproximados
    d.rect(-6.5, 22.5, -3.5, 24.0, "POSICION_APROXIMADA")
    d.rect(-15.5, 74.0, -12.5, 75.5, "POSICION_APROXIMADA")
    d.texto("R (residuos, H-APA-4, aprox.)", (-5, 21.8), 0.5, "POSICION_APROXIMADA")
    d.texto("R (residuos, aprox.)", (-14, 76.2), 0.5, "POSICION_APROXIMADA")
    d.rect(89.3, 1.0, 91.3, 3.0, "POSICION_APROXIMADA")
    d.texto("elemento SE sin identificar (FALTA DATO)", (84, 2.0), 0.55, "POSICION_APROXIMADA")
    d.texto("jardín común (sin trazado en F2)", (75, 64), 0.8, "POSICION_APROXIMADA")
    d.texto("espacio libre común (sin trazado en F2)", (-8, 46), 0.8, "POSICION_APROXIMADA")
    # Cotas principales (F2 2.1 / 2.4)
    d.cota((2, 9), (54, 9), (0, 7.9))
    d.cota((54, 9), (60, 9), (0, 7.9))
    d.cota((60, 9), (86, 9), (0, 7.9))
    for a, b in [(-2.5, 23.5), (23.5, 29.5), (29.5, 55.5), (55.5, 61.5), (61.5, 87.5)]:
        d.cota((a, 49), (b, 49), (0, 51.3))
    d.cota((2, 21), (8.5, 21), (0, 20.6), txt=0.45)
    for a, b in [(9, 21), (21, 26), (26, 32), (32, 37), (37, 49), (49, 61), (61, 73)]:
        d.cota((57, a), (57, b), (58.3, 0), vertical=True)
    d.cota((88, 21), (88, 37), (90.0, 0), vertical=True)
    d.texto("A–B 16,00", (90.8, 29), 0.6, "A-COTA", rot=90)
    d.cota((bx0, by1), (bx1, by1), (0, 76.6))
    # Conflictos
    for cod, pos, _ in CONFLICTOS_IMPL:
        d.conflicto(cod, pos, r=1.6 if len(cod) < 5 else 2.2, h=0.8 if len(cod) < 5 else 0.55)
    # Leyenda de conflictos (fuera de parcela, al este)
    xl, yl = 96.0, 96.0
    d.izq("CONFLICTOS F3 ABIERTOS (fases/conflictos.md) · ninguno resuelto en F4", (xl, yl), 1.0, "CONFLICTOS_F3")
    vistos = []
    for cod, _, txt in CONFLICTOS_IMPL:
        if (cod, txt[:20]) in vistos:
            continue
        vistos.append((cod, txt[:20]))
        yl -= 1.5
        d.izq(f"{cod}: {txt} · pendiente de decisión", (xl, yl), 0.7, "CONFLICTOS_F3")
    # Norte y notas
    d.pl([(-40, 70), (-38.5, 78), (-40, 76.5), (-41.5, 78)], "A-TEXTO")
    d.texto("N", (-40, 79.5), 1.5, "A-TEXTO")
    d.cajetin(96.0, 30.0, "UA-03-01 · V1 «Calle de casas» · PLANO DE IMPLANTACIÓN", [
        "Coordenadas: ETRS89 / UTM huso 30N (EPSG:25830). Vértices: cédula (01_urbanismo 1.4).",
        "Local F2 = UTM − (414.896,93 ; 4.478.781,24); origen en el vértice 3.",
        "Linderos curvos (R 433, 100, 669,75, 500): se dibujan las cuerdas; geometría exacta FALTA DATO.",
        "Superficie oficial 8.839 m² (polígono de cuerdas 9.022,15 m²).",
        "Retranqueos: offset interior de las cuerdas, 3 m (unifamiliar) y 5 m (multifamiliar).",
        "Topografía y cotas de rasante: FALTA DATO (dibujo solo en planta).",
        "Fuentes: 01_urbanismo, 02_diseno (V1), 03_estructura, 03_instalaciones, 03_normativa, conflictos.md.",
        "Capa POSICION_APROXIMADA: elementos sin cota en los entregables.",
        "Capa CONFLICTOS_F3: conflictos abiertos; se dibuja la solución de F2/F3 sin resolverlos.",
    ], "1:500")
    ruta = os.path.join(PLANOS, "V1_implantacion.dxf")
    doc.saveas(ruta)
    return ruta


# =============================================================== 2. CASA TIPO
# Estancias de F2 2.2 (superficie util). Geometria: POSICION APROXIMADA (F2 no da cotas interiores).
# Coordenadas de la casa: x 0..6,50 entre ejes de medianera; y = 0 fachada del jardin, y = 12 fachada de calle.
ESTANCIAS_PB = [
    ("Salón-comedor", 28.0, (0.12, 0.24, 6.38, 4.71)),
    ("Escalera", 5.5, (0.12, 5.00, 1.22, 10.00)),
    ("Distribuidor", 3.0, (1.22, 5.00, 2.42, 7.50)),
    ("Vestíbulo", 5.0, (1.22, 7.50, 2.42, 11.76)),
    ("Cocina", 12.0, (2.42, 6.88, 4.88, 11.76)),
    ("Lavadero-despensa", 4.0, (4.88, 6.69, 6.38, 9.36)),
    ("Aseo", 3.0, (4.88, 9.76, 6.38, 11.76)),
]
ESTANCIAS_P1 = [
    ("Dormitorio 2", 11.0, (0.12, 0.24, 2.58, 4.71)),
    ("Dormitorio principal", 15.0, (3.02, 0.24, 6.38, 4.71)),
    ("Vestidor", 3.0, (4.38, 4.71, 6.38, 6.21)),
    ("Escalera (hueco)", 5.5, (0.12, 5.00, 1.22, 10.00)),
    ("Distribuidor", 6.0, (1.22, 4.71, 4.38, 6.61)),
    ("Baño principal", 5.0, (4.38, 6.86, 6.38, 9.36)),
    ("Dormitorio 3", 10.0, (1.22, 8.32, 4.13, 11.76)),
    ("Baño 2", 4.5, (4.13, 9.76, 6.38, 11.76)),
]
# Patinillo PU (I-1 / E5): 0,80 m en E-O x 0,40 m en N-S, a 0,10 m de la cara de la medianera opuesta
# a la escalera. Cota E-O fijada por E5; posicion N-S aproximada (crujia de calle, junto a zona humeda).
PU = (6.38 - 0.10 - 0.80, 9.36, 6.38 - 0.10, 9.76)


def dibujar_casa_tipo():
    doc = nuevo_doc(["A-MURO", "A-TABIQUE", "A-CARPINTERIA", "S-EJE", "I-PATINILLO", "A-COTA", "A-TEXTO",
                     "A-CAJETIN", "POSICION_APROXIMADA", "CONFLICTOS_F3"])
    for k, (planta, estancias, util) in enumerate([("PLANTA BAJA", ESTANCIAS_PB, 60.5),
                                                   ("PLANTA PRIMERA", ESTANCIAS_P1, 60.0)]):
        dx = k * 14.0
        d = Dib(doc, lambda p, dx=dx: (p[0] + dx, p[1]))
        d.texto(f"CASA U-V1 · {planta}", (3.25, 15.6), 0.4, "A-TEXTO")
        d.texto(f"78,00 m² construidos · útil F2 ≈ {cota_txt(util)} m²", (3.25, 14.9), 0.3, "A-TEXTO")
        d.rect(0, 0, 6.5, 12, "A-MURO")  # envolvente 6,50 x 12,00 (caras exteriores / ejes de medianera)
        d.rect(-0.12, 0, 0.12, 12, "A-MURO")      # medianera 24 cm centrada en el eje
        d.rect(6.38, 0, 6.62, 12, "A-MURO")
        d.rect(0.12, 0, 6.38, 0.24, "A-MURO")     # fachadas: espesor FALTA DATO (0,24 de representacion)
        d.rect(0.12, 11.76, 6.38, 12, "A-MURO")
        for nombre, sup, (x0, y0, x1, y1) in estancias:
            d.rect(x0, y0, x1, y1, "POSICION_APROXIMADA")
            d.texto(nombre, ((x0 + x1) / 2, (y0 + y1) / 2 + 0.2), 0.22, "A-TEXTO")
            d.texto(f"{cota_txt(sup)} m² (F2)", ((x0 + x1) / 2, (y0 + y1) / 2 - 0.2), 0.2, "A-TEXTO")
        d.rect(*PU, "I-PATINILLO")
        d.linea(PU[:2], PU[2:], "I-PATINILLO")
        d.linea((PU[0], PU[3]), (PU[2], PU[1]), "I-PATINILLO")
        d.texto("PU 0,80 × 0,40", ((PU[0] + PU[2]) / 2, PU[3] + 0.25), 0.18, "I-PATINILLO")
        d.texto("posición N-S aprox.", ((PU[0] + PU[2]) / 2, PU[1] - 0.2), 0.15, "POSICION_APROXIMADA")
        # Ejes
        for x, n in [(0, "1"), (6.5, "2")]:
            d.linea((x, -1.2), (x, 13.2), "S-EJE")
            d.circulo((x, -1.7), 0.4, "S-EJE")
            d.texto(n, (x, -1.7), 0.35, "S-EJE")
        for y, n in [(0, "A"), (12, "C")]:
            d.linea((-1.2, y), (7.7, y), "S-EJE")
            d.circulo((-1.7, y), 0.4, "S-EJE")
            d.texto(n, (-1.7, y), 0.35, "S-EJE")
        d.linea((-1.2, 6.0), (7.7, 6.0), "POSICION_APROXIMADA")
        d.texto("B ≈ (zuncho escalera / muro E2)", (3.25, 6.0 + 0.0), 0.15, "POSICION_APROXIMADA",
                al=TextEntityAlignment.LEFT)
        d.texto("JARDÍN (sur en banda A / norte en banda B)", (3.25, -0.6), 0.25, "A-TEXTO")
        d.texto("CALLE: entrada y 2 plazas", (3.25, 12.6), 0.25, "A-TEXTO")
        d.texto("entrada (aprox.)", (1.82, 12.25), 0.15, "POSICION_APROXIMADA") if k == 0 else None
        # Cotas
        d.cota((0, 0), (6.5, 0), (0, -2.6), txt=0.35)
        d.cota((6.5, 0), (6.5, 12), (8.4, 0), vertical=True, txt=0.35)
        d.cota((PU[0], PU[1]), (PU[2], PU[1]), (0, PU[1] - 0.7), txt=0.15)
        d.cota((PU[2], PU[1]), (PU[2], PU[3]), (PU[2] + 0.7, 0), vertical=True, txt=0.15)
        d.cota((PU[2], PU[3]), (6.38, PU[3]), (0, PU[3] + 0.9), txt=0.15)
        # Conflictos
        d.conflicto("E5/I-1/I-2", (5.0, 8.4), r=0.85, h=0.17)
        d.conflicto("N-3", (6.5, 2.5), r=0.5, h=0.2)
        d.conflicto("E2", (3.25, 7.9 if k == 0 else 7.6), r=0.45, h=0.2)
        d.conflicto("I-5", (1.6, 2.5), r=0.45, h=0.2)
    d = Dib(doc)
    notas = [
        "Estancias y superficies útiles: 02_diseno 2.2. Rectángulos de estancias: POSICION_APROXIMADA (F2 sin cotas",
        "  interiores); las superficies rotuladas son las de F2, no las del rectángulo dibujado.",
        "Zonas en blanco: circulación, tabiquería y holgura no asignadas en F2.",
        "Medianeras 24 cm centradas en ejes cada 6,50 m (03_estructura 1.1, 2.1); fachadas: espesor FALTA DATO.",
        "Patinillo PU 0,80 (E-O) × 0,40 (N-S) a 0,10 m de la medianera opuesta a la escalera (I-1, E5).",
        "Lado de la escalera (oeste/este) y simetría por hilera: FALTA DATO (se dibuja escalera al oeste).",
        "Casas 4 y 5: ≈ 0,14 m más estrechas si se adopta E1 (a); no se dibuja (E1 abierto).",
        "Carpinterías: sin definir en F2 (capa A-CARPINTERIA vacía). Altura de planta 3,00 m (H-ALT).",
        "Conflictos: E5/I-1/I-2 patinillo · E2 arriostramiento E-O · N-3 medianera HR/SI · I-5 alturas libres.",
    ]
    d.cajetin(-2.5, -15.0, "UA-03-01 · V1 · CASA TIPO U-V1 (6,50 × 12,00 m) · PB y P1", notas, "1:50", w=28.0)
    ruta = os.path.join(PLANOS, "V1_casa_tipo.dxf")
    doc.saveas(ruta)
    return ruta


# =============================================================== 3. BLOQUE
VIV_TIPO = ("M-V1-a", 98.5, 80.5)    # 02_diseno 2.2
VIV_PB = ("M-V1-b", 156.0, 121.5)


def dibujar_bloque():
    doc = nuevo_doc(["A-MURO", "A-TABIQUE", "A-CARPINTERIA", "S-EJE", "S-PILAR", "S-VIGA", "I-PATINILLO",
                     "A-COTA", "A-TEXTO", "A-CAJETIN", "POSICION_APROXIMADA", "CONFLICTOS_F3"])
    bx0, by0, bx1, by1 = BLOQUE
    mitades = [(bx0, (bx0 + bx1) / 2), ((bx0 + bx1) / 2, bx1)]
    for k, planta in enumerate(["PLANTA TIPO (P1 y P2)", "PLANTA BAJA (esquemática)"]):
        dy = -25.0 * k
        d = Dib(doc, lambda p, dy=dy: (p[0], p[1] + dy))
        d.texto(f"BLOQUE M-V1 · {planta} · 12,00 × 37,50 m = 450 m² por planta", (38.25, 78.0), 0.7, "A-TEXTO")
        d.rect(bx0, by0, bx1, by1, "A-MURO")
        for i, x in enumerate(EJES_X):
            d.linea((x, 59.3), (x, 74.7), "S-EJE")
            d.circulo((x, 58.6), 0.55, "S-EJE")
            d.texto(str(i + 1), (x, 58.6), 0.5, "S-EJE")
        for ej, y in EJES_Y.items():
            d.linea((18.2, y), (58.3, y), "S-EJE")
            d.circulo((17.5, y), 0.55, "S-EJE")
            d.texto(ej, (17.5, y), 0.5, "S-EJE")
        for p in pilares():
            d.rect(p["x"] - p["dx"] / 2, p["y"] - p["dy"] / 2, p["x"] + p["dx"] / 2, p["y"] + p["dy"] / 2, "S-PILAR")
            if p["nombre"] in ("B2", "B3", "B5", "B6"):
                d.rect(p["x"] - 1.7, p["y"] - 1.7, p["x"] + 1.7, p["y"] + 1.7, "CONFLICTOS_F3")
        d.texto("S-VIGA: sin vigas de cuelgue; losa maciza 30 cm con zunchos de borde 30×30 y brochales embebidos "
                "(03_estructura 1.2, 4.2)", (38.25, 59.8 - 2.6), 0.4, "S-VIGA")
        for n, (x0, y0, x1, y1) in enumerate(NUCLEOS):
            d.rect(x0, y0, x1, y1, "POSICION_APROXIMADA")
            d.texto(f"núcleo {n + 1}: escalera + ascensor ≈ 28 m² (aprox.)", ((x0 + x1) / 2, (y0 + y1) / 2), 0.3,
                    "POSICION_APROXIMADA")
        for nom, x in PATINILLOS_BLOQUE:
            d.rect(x - 0.5, 68.1, x + 0.5, 68.7, "I-PATINILLO")
            d.linea((x - 0.5, 68.1), (x + 0.5, 68.7), "I-PATINILLO")
            d.texto(f"{nom} 1,00×0,60", (x, 69.0), 0.22, "I-PATINILLO")
        d.texto("patinillos PB-1..PB-4: posición aproximada (sobre ejes 2, 3, 5 y 6 según E4)", (38.25, 74.0), 0.3,
                "POSICION_APROXIMADA")
        for n, (xa, xb) in enumerate(mitades):
            xc = (NUCLEOS[n][0] + NUCLEOS[n][2]) / 2
            nx0, ny0, nx1, ny1 = NUCLEOS[n]
            mitad = box(xa, by0, xb, by1)
            if k == 0:
                partes = [mitad.intersection(box(xa, by0, xc, by1)).difference(box(*NUCLEOS[n])),
                          mitad.intersection(box(xc, by0, xb, by1)).difference(box(*NUCLEOS[n]))]
                for j, g in enumerate(partes):
                    d.pl(list(g.exterior.coords)[:-1], "POSICION_APROXIMADA")
                    cx = (g.bounds[0] + g.bounds[2]) / 2
                    d.texto(f"VIVIENDA {VIV_TIPO[0]} (P1 y P2) · portal {n + 1}-{j + 1}", (cx, 63.2), 0.32, "A-TEXTO")
                    d.texto(f"{cota_txt(VIV_TIPO[1])} m² constr. / {cota_txt(VIV_TIPO[2])} m² útil (F2)",
                            (cx, 62.5), 0.28, "A-TEXTO")
                    d.texto("límite aproximado", (cx, 71.5), 0.25, "POSICION_APROXIMADA")
            else:
                comun = box(nx0, by0, nx1, ny1)
                viv = mitad.difference(comun)
                d.pl(list(viv.exterior.coords)[:-1], "POSICION_APROXIMADA")
                d.rect(nx0, by0, nx1, ny1, "POSICION_APROXIMADA")
                cx = (xa + nx0) / 2
                d.texto(f"VIVIENDA {VIV_PB[0]} (PB) · portal {n + 1}", (cx, 63.2), 0.32, "A-TEXTO")
                d.texto(f"{cota_txt(VIV_PB[1])} m² constr. / {cota_txt(VIV_PB[2])} m² útil (F2)", (cx, 62.5), 0.28,
                        "A-TEXTO")
                d.texto("jardín privativo al sur (F2)", (cx, 61.8), 0.25, "A-TEXTO")
                d.texto("comunes PB (F2): portal 18 + contadores CI 8 + bicis/basuras 15 m²", ((nx0 + nx1) / 2, 62.0),
                        0.18, "A-TEXTO")
                d.texto("distribución de PB sin definir en F2", (xb - 4.5, 71.8), 0.25, "POSICION_APROXIMADA")
                d.linea((xc, 57.4), (xc, by0), "POSICION_APROXIMADA")
                d.texto(f"portal {n + 1} (aprox.)", (xc, 57.0), 0.3, "POSICION_APROXIMADA")
                d.conflicto("NC-1", (xc - 3.0, 57.6), r=0.8, h=0.35)
                d.conflicto("I-9", (xc + 2.6, 57.6), r=0.8, h=0.35)
            d.conflicto("E4/I-3/N-4", (xc, 70.8), r=1.1, h=0.25)
        if k == 0:
            d.conflicto("I-7", (23.0, 70.5), r=0.7, h=0.3)
            d.conflicto("E3", (55.0, 75.5), r=0.7, h=0.3)
            d.conflicto("I-5", (63.5, 67.0), r=0.7, h=0.3)
        # Cotas
        d.cota((bx0, by0), (bx1, by0), (0, 55.9))
        prev = EJES_X[0]
        for x in EJES_X[1:]:
            d.cota((prev, by1), (x, by1), (0, 76.0), txt=0.35)
            prev = x
        d.cota((bx0, by1), (EJES_X[0], by1), (0, 76.0), txt=0.2)
        d.cota((bx1, by0), (bx1, by1), (61.0, 0), vertical=True)
        d.cota((bx1, EJES_Y["A"]), (bx1, EJES_Y["B"]), (59.4, 0), vertical=True, txt=0.35)
        d.cota((bx1, EJES_Y["B"]), (bx1, EJES_Y["C"]), (59.4, 0), vertical=True, txt=0.35)
    d = Dib(doc)
    d.cajetin(64.0, 38.0, "UA-03-01 · V1 · BLOQUE M-V1 · PLANTA TIPO Y PB", [
        "Coordenadas locales de F2 (origen vértice 3). Envolvente 12,00 × 37,50 m a cara exterior (02_diseno 2.1).",
        "Retícula ajustada 2 × 5,75 × 6 × 6,17 m, ejes a 0,25 m de las caras (03_estructura 2.2).",
        "Pilares: esquina 30×30, fachada 30×40, testero 30×40, interior 40×40 (03_estructura 4.2).",
        "Recuadros rojos en B2, B3, B5, B6: zona 6d ≈ 1,50 m desde la cara del pilar (E4).",
        "Núcleos, patinillos, portales y límites de viviendas: posición aproximada (sin cotas en F2/F3).",
        "Viviendas: P1 y P2 = 2 × 4 M-V1-a; PB = 2 M-V1-b. Total 10 (02_diseno 2.2).",
        "Superficies rotuladas: las de F2; los recintos dibujados no las reproducen (distribución FALTA DATO).",
        "Canaladuras PE/PT, armarios AC y CI de instalaciones: sin posición en F3 (no se dibujan).",
        "Conflictos: E4/I-3/N-4, I-9, NC-1, I-7, E3, I-5 (abiertos, ver fases/conflictos.md).",
    ], "1:100", w=46.0)
    ruta = os.path.join(PLANOS, "V1_bloque_planta_tipo.dxf")
    doc.saveas(ruta)
    return ruta


if __name__ == "__main__":
    os.makedirs(PLANOS, exist_ok=True)
    for f in (dibujar_implantacion, dibujar_casa_tipo, dibujar_bloque):
        print("generado:", os.path.relpath(f(), RAIZ))
