#!/usr/bin/env python3
"""
Predimensionado estructural orientativo (reglas fijas, sin IA) - F3 estructura.
Parcela UA-03-01, variante V1 "Calle de casas" (24 adosadas + bloque de 10 pisos).

NO SUSTITUYE AL CALCULO. Todas las constantes son HIPOTESIS declaradas en
fases/03_estructura.md (cargas segun CTE DB SE-AE, reglas del Codigo Estructural
y DB SE-F). La tension admisible del terreno es FALTA DATO: se dan escenarios.

Uso (desde la raiz del repositorio):
    python3 scripts/estructura_predim.py
"""
import math

# ---------------------------------------------------------------- utilidades
def ceil05(x):
    """Redondea por exceso a multiplos de 0,05 m."""
    return math.ceil(round(x / 0.05, 6)) * 0.05


def canto_rigido(B, c, minimo=0.40):
    """Canto de zapata rigida: vuelo v = (B - c)/2 <= 2h  ->  h >= v/2 (con minimo constructivo)."""
    return max(minimo, ceil05((B - c) / 4.0))


SIGMAS_KPA = [100.0, 200.0, 300.0]   # escenarios 0,10 / 0,20 / 0,30 MPa (HIPOTESIS)
K_ZAP = 1.10                          # +10 % peso propio de zapata y tierras

# ---------------------------------------------------------------- cargas (kN/m2)
# Casas (forjado unidireccional 25+5, viguetas pretensadas)
G_FORJ_U = 3.5
PAV = 1.5          # pavimento + recrecido / suelo radiante
TAB = 1.0          # tabiqueria (DB SE-AE 2.1)
FT = 0.2           # falso techo + instalaciones colgadas
G_CUB = 2.5        # cubierta plana invertida con grava (DB SE-AE tabla C.5)
Q_VIV = 2.0        # A1 (DB SE-AE tabla 3.1)
Q_CUB = max(1.0, 0.6)   # G1 = 1,0 (no concomitante) frente a nieve 0,6 (hipotesis)

q_p1_u = G_FORJ_U + PAV + TAB + FT + Q_VIV
q_cub_u = G_FORJ_U + G_CUB + FT + Q_CUB
q_san = G_FORJ_U + PAV + TAB + Q_VIV
g_p1_u = G_FORJ_U + PAV + TAB + FT
g_cub_u = G_FORJ_U + G_CUB + FT

# Bloque (losa maciza de 0,30 m)
H_LOSA = 0.30
G_LOSA = 25.0 * H_LOSA
g_tipo_m = G_LOSA + PAV + TAB + FT
g_cub_m = G_LOSA + G_CUB + FT
q_tipo_m = g_tipo_m + Q_VIV
q_cub_m = g_cub_m + Q_CUB
FACH = 8.0         # kN/m por planta de cerramiento (hipotesis)
PETO = 3.0         # kN/m (hipotesis)

print("PREDIMENSIONADO ESTRUCTURAL ORIENTATIVO (reglas fijas, sin IA) - NO SUSTITUYE AL CALCULO")
print("=" * 88)
print("Cargas caracteristicas totales (kN/m2):")
print(f"  Casas  P1 {q_p1_u:.1f} | cubierta {q_cub_u:.1f} | forjado sanitario {q_san:.1f}")
print(f"  Bloque planta tipo {q_tipo_m:.1f} | cubierta {q_cub_m:.1f} | forjado sanitario {q_san:.1f}")

# ---------------------------------------------------------------- canto forjado casas
L_U = 6.50
d1 = math.sqrt(q_p1_u / 7.0)
d2 = (L_U / 6.0) ** 0.25
print("\nCanto minimo forjado unidireccional casas (Codigo Estructural 50.2.2.1, h = d1*d2*L/C):")
print(f"  L = {L_U:.2f} m, q = {q_p1_u:.1f} kN/m2, d1 = {d1:.3f}, d2 = {d2:.3f}")
for nombre, C in [("tramo aislado (C=19)", 19), ("tramo extremo (C=23)", 23), ("tramo interior (C=26)", 26)]:
    print(f"  {nombre:24s} h_min = {d1 * d2 * L_U / C:.3f} m")

# ---------------------------------------------------------------- canto losa bloque
L_M = 6.25
d_req = L_M / 24.0
print("\nCanto losa maciza bloque (tabla 50.2.2.1.a, placa sin vigas K=1,2, L/d=24 con rho=0,5 %):")
print(f"  L = {L_M:.2f} m -> d >= {d_req:.3f} m -> h ~ {d_req + 0.04:.2f} m")

# ---------------------------------------------------------------- muro de carga casas
PESO_FAB = 15.0 * 0.24          # kN/m2 de muro de 24 cm
TRAS = 0.3                      # kN/m2 por trasdosado
muro_total = PESO_FAB * 6.0 + 2 * TRAS * 5.4
Nd_muro = (6.5 * (1.35 * g_cub_u + 1.5 * Q_CUB)
           + 6.5 * (1.35 * g_p1_u + 1.5 * Q_VIV)
           + 1.35 * 5.4 * (PESO_FAB + 2 * TRAS))
print("\nMuro de medianera de fabrica 24 cm (base de PB):")
print(f"  N_d = {Nd_muro:.1f} kN/m -> sigma_d = {Nd_muro / 240.0:.3f} N/mm2")

# ---------------------------------------------------------------- zapatas corridas casas
lineas = {
    "Medianera interior (trib. 6,50)": (6.5 * (q_cub_u + q_p1_u + q_san) + muro_total, 0.24, 0.60),
    "Testero / extremo (trib. 3,25)": (3.25 * (q_cub_u + q_p1_u + q_san) + muro_total, 0.24, 0.60),
    "Junta (doble muro, zapata comun)": (2 * (3.25 * (q_cub_u + q_p1_u + q_san) + muro_total), 0.51, 0.90),
}
print("\nZapatas corridas casas (N_k incluye +10 %; B en m; h rigido en m):")
print(f"  {'Elemento':36s} {'N_k kN/m':>9s}  " + "  ".join(f"s={s/1000:.2f}MPa B / h" for s in SIGMAS_KPA))
for nombre, (n, c, bmin) in lineas.items():
    nk = n * K_ZAP
    cols = []
    for s in SIGMAS_KPA:
        B = max(bmin, ceil05(nk / s))
        h = canto_rigido(B, c)
        cols.append(f"{B:5.2f} / {h:4.2f}      ")
    print(f"  {nombre:36s} {nk:9.1f}  " + "  ".join(cols))

# ---------------------------------------------------------------- pilares y zapatas bloque
def pilar(A, k, fach_len, c_min, pp):
    nk_sup = k * A * (2 * q_tipo_m + q_cub_m) + FACH * fach_len * 2 + PETO * fach_len + pp
    nk_zap = nk_sup + A * q_san + FACH * fach_len
    nd = (k * A * (2 * (1.35 * g_tipo_m + 1.5 * Q_VIV) + (1.35 * g_cub_m + 1.5 * Q_CUB))
          + 1.35 * (FACH * fach_len * 2 + PETO * fach_len + pp))
    return nk_sup, nk_zap, nd


tipos = {
    # nombre: (A trib m2, k continuidad, long. fachada m, lado menor pilar m, PP pilar kN, nº)
    "Interior B2-B6 (40x40)": (37.5, 1.2, 0.0, 0.40, 0.40 * 0.40 * 25 * 9, 5),
    "Fachada A2-A6, C2-C6 (30x40)": (18.75, 1.0, 6.25, 0.30, 0.30 * 0.40 * 25 * 9, 10),
    "Testero B1, B7 (30x40)": (18.75, 1.2, 6.0, 0.30, 0.30 * 0.40 * 25 * 9, 2),
    "Esquina A1, A7, C1, C7 (30x30)": (9.375, 1.0, 6.125, 0.30, 0.30 * 0.30 * 25 * 9, 4),
}
SIG_EFF = 0.8 * (0.85 * 25 / 1.5 + 0.01 * 400)   # MPa, con 20 % de reduccion
print("\nPilares y zapatas aisladas del bloque (N en kN; B lado de zapata cuadrada en m; h rigido):")
total = 0.0
for nombre, (A, k, fl, c, pp, n) in tipos.items():
    nk_sup, nk_zap, nd = pilar(A, k, fl, c, pp)
    total += n * nk_zap
    ac = nd * 1000 / SIG_EFF
    cols = []
    for s in SIGMAS_KPA:
        B = ceil05(math.sqrt(nk_zap * K_ZAP / s))
        h = canto_rigido(B, c)
        cols.append(f"{B:4.2f}/{h:4.2f}")
    print(f"  {nombre:32s} Nk_pilar={nk_sup:7.1f} Nk_zap={nk_zap:7.1f} Nd={nd:7.1f} "
          f"Ac_min={ac/100:6.0f} cm2 (lado {math.sqrt(ac):4.0f} mm) | " + "  ".join(cols))

area_losa = 13.0 * 38.5
p_media = total / area_losa + 0.60 * 25
print(f"\n  Suma N_k a cimentacion: {total:.0f} kN | losa 13,0 x 38,5 m, canto 0,60: "
      f"presion media ~ {p_media:.1f} kPa ({p_media/1000:.3f} MPa)")

# ---------------------------------------------------------------- punzonamiento
d = 0.25
c = 0.40
Vd = 1.2 * 37.5 * (1.35 * g_tipo_m + 1.5 * Q_VIV)
u1 = 4 * c + 4 * math.pi * d
tau = 1.15 * Vd * 1000 / (u1 * 1000 * d * 1000)
xi = 1 + math.sqrt(200 / (d * 1000))
rho = 0.008
trd = max(0.18 / 1.5 * xi * (100 * rho * 25) ** (1 / 3), 0.075 / 1.5 * xi ** 1.5 * math.sqrt(25))
print("\nPunzonamiento pilar interior (losa 0,30, d=0,25, pilar 40x40, rho=0,8 %, beta=1,15):")
print(f"  V_d = {Vd:.1f} kN, u1 = {u1:.3f} m, tau_sd = {tau:.3f} MPa, tau_rd = {trd:.3f} MPa -> "
      + ("CUMPLE sin armadura" if tau <= trd else "NECESITA armadura de punzonamiento"))
print(f"  Zona sin huecos alrededor del pilar (6d): {6 * d:.2f} m desde la cara del pilar")
