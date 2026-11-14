#!/usr/bin/env python3
"""
Generador de VARIANTES de ordenación con reglas fijas (sin IA) — herramienta interna.

Explora muchas ordenaciones de una misma parcela combinando:
  1. Zonificación: la parcela se parte en una zona UNIFAMILIAR (adosadas en
     hilera) y una zona MULTIFAMILIAR (bloques), con distintos repartos.
  2. Viario y aparcamiento: calles de casas con plazas en batería delante de
     cada vivienda, remate de la calle (fondo de saco, martillo o lazo), acera
     opcional y bolsa de aparcamiento para el resto de plazas.
  3. Comprobación y ranking: viviendas, techo, plazas, ocupación (dos
     lecturas), longitud de fondo de saco (DB-SI SI 5), itinerario peatonal.

Salidas en planos/variantes/<nombre>/:
  ranking.txt / ranking.json   tabla comparativa de todas las variantes
  lamina.svg                   las mejores variantes en una lámina
  Vnnn.svg                     planta de cada variante de la lámina
  Vnnn.dxf                     con --dxf Vnnn

Uso:
  python3 scripts/variantes_generador.py planos/variantes/entrada_UA-03-01.json
  python3 scripts/variantes_generador.py <entrada> --top 12
  python3 scripts/variantes_generador.py <entrada> --dxf V007

Principios (CLAUDE.md §7): los parámetros urbanísticos ('comun',
'unifamiliar', 'multifamiliar') no tienen valor por defecto: si falta uno, se
detiene con FALTA DATO. Los de diseño ('hipotesis') tienen valor por defecto
y se listan siempre en la salida.
"""

import argparse
import itertools
import json
import math
import re
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.prepared import prep

sys.path.insert(0, str(Path(__file__).resolve().parent))
from volumetria_generador import (  # noqa: E402
    FALTA, _limpia, _polys, _rumbo_txt, _tramos_en_franja, bloques_lineales, lados,
    leer_gml, zona_retranqueos,
)

REQ_COMUN = ["edificabilidad_m2m2", "viviendas_max", "plazas_por_vivienda", "separacion_edificios_m"]
REQ_USO = ["ocupacion_pct", "plantas_max", "retranqueo_fachada_m", "retranqueo_linderos_m"]

HIPOTESIS_DEFECTO = {
    # Vivienda unifamiliar adosada
    "fondo_casa_m": 12.0,
    "ancho_casa_m": 6.5,
    "sup_casa_m2": 156.0,              # construidos por casa
    "casas_min_hilera": 3,
    "casas_max_hilera": 8,
    "jardin_trasero_m": 6.0,           # fondo mínimo de jardín trasero por casa
    # Vivienda en bloque
    "fondo_bloque_m": 12.0,
    "longitud_min_bloque_m": 15.0,
    "longitud_max_bloque_m": 40.0,     # < 40 m evita junta de dilatación (DB SE-AE 3.4.1)
    "sup_piso_m2": 135.0,              # construidos por piso, con parte de comunes
    "altura_planta_m": 3.0,
    # Viario y aparcamiento
    "calzada_m": 6.0,
    "plaza_ancho_m": 2.5,
    "plaza_fondo_m": 5.0,
    "paso_peatonal_casa_m": 1.5,       # paso entre plazas hasta la puerta de cada casa
    "acera_m": 1.5,
    "martillo_largo_m": 12.0,          # brazo total del martillo de giro (hipótesis)
    "fondo_saco_max_m": 20.0,          # DB-SI SI 5 1.2: vía sin salida > 20 m → espacio de maniobra
    "distancia_aparcamiento_edificio_m": 2.0,
    "aparcamiento_fuera_retranqueo": True,  # hipótesis H-APA de F2 (cómputo en retranqueo: FALTA DATO)
    # Búsqueda
    "paso_rejilla_m": 0.5,
    "paso_fase_m": 2.0,
}

BARRIDO_DEFECTO = {
    "angulo_hileras": "fachadas",      # o lista de grados
    "pct_zona_unifamiliar": [0, 30, 40, 50, 60, 70, 80, 100],
    "unifamiliar_en": ["abajo", "arriba"],
    "remate": ["fondo_saco", "martillo", "lazo"],
    "acera": [False, True],
}


# --------------------------------------------------------------------------- #
# Entrada
# --------------------------------------------------------------------------- #
def cargar(ruta: Path) -> dict:
    cfg = json.loads(ruta.read_text(encoding="utf-8"))
    par = cfg.get("parcela") or {}
    if "coordenadas" in par:
        pts = [tuple(p) for p in par["coordenadas"]]
    elif "gml" in par:
        pts = leer_gml(Path(par["gml"]))
    else:
        raise ValueError("La parcela necesita 'coordenadas' o 'gml'.")
    poly = Polygon(pts)
    if not poly.is_valid:
        raise ValueError("La geometría de la parcela no es válida.")
    faltan = []
    comun = {k: v for k, v in (cfg.get("comun") or {}).items() if v is not None}
    faltan += [f"comun.{k}" for k in REQ_COMUN if k not in comun]
    usos = {}
    for uso in ("unifamiliar", "multifamiliar"):
        u = {k: v for k, v in (cfg.get(uso) or {}).items() if v is not None}
        faltan += [f"{uso}.{k}" for k in REQ_USO if k not in u]
        usos[uso] = u
    if not cfg.get("fachadas"):
        faltan.append("fachadas")
    if not cfg.get("accesos"):
        faltan.append("accesos (lados por los que puede entrar el viario)")
    if faltan:
        raise ValueError(f"{FALTA}: " + ", ".join(faltan))
    hip = dict(HIPOTESIS_DEFECTO)
    hip.update(cfg.get("hipotesis") or {})
    barr = dict(BARRIDO_DEFECTO)
    barr.update(cfg.get("barrido") or {})
    sup = float(par.get("superficie_oficial_m2") or poly.area)
    return {
        "nombre": cfg.get("nombre", "parcela"), "pts": pts, "poly": poly, "sup": sup,
        "f_sup": sup / poly.area, "ccw": poly.exterior.is_ccw,
        "fachadas": set(cfg["fachadas"]), "accesos": set(cfg["accesos"]),
        "comun": comun, "uni": usos["unifamiliar"], "multi": usos["multifamiliar"],
        "hip": hip, "barrido": barr,
    }


# --------------------------------------------------------------------------- #
# Utilidades geométricas
# --------------------------------------------------------------------------- #
def _rot_pts(pts, ang, c):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [((x - c.x) * ca - (y - c.y) * sa + c.x, (x - c.x) * sa + (y - c.y) * ca + c.y) for x, y in pts]


def _corte(poly, frac, abajo=True):
    """Corta el polígono por una horizontal y = yc tal que el área de abajo sea frac·A."""
    minx, miny, maxx, maxy = poly.bounds
    objetivo = frac * poly.area
    lo, hi = miny, maxy
    for _ in range(50):
        mid = (lo + hi) / 2
        if poly.intersection(box(minx - 1, miny - 1, maxx + 1, mid)).area < objetivo:
            lo = mid
        else:
            hi = mid
    yc = (lo + hi) / 2
    inf = _limpia(poly.intersection(box(minx - 1, miny - 1, maxx + 1, yc)))
    sup = _limpia(poly.intersection(box(minx - 1, yc, maxx + 1, maxy + 1)))
    return yc, (inf, sup) if abajo else (sup, inf)


def _pieza_que_toca(g, toque):
    for p in _polys(g):
        if p.intersects(toque):
            return p
    return None


# --------------------------------------------------------------------------- #
# Zona unifamiliar: módulos de calle con casas a uno o dos lados
# --------------------------------------------------------------------------- #
def _filas_casas(U, y0, h, hip, sep, prohibido=None):
    """Hileras de casas (rectángulos) en la franja [y0, y0+h] totalmente dentro de U."""
    zona = U if prohibido is None or prohibido.is_empty else _limpia(U.difference(prohibido))
    if zona.is_empty:
        return []
    minx, _, maxx, _ = zona.bounds
    a = hip["ancho_casa_m"]
    tramos = _tramos_en_franja(prep(zona), minx, maxx, y0, h, sep,
                               hip["casas_min_hilera"] * a, hip["casas_max_hilera"] * a, hip["paso_rejilla_m"])
    hileras = []
    for r in tramos:
        x1, _, x2, _ = r.bounds
        n = int((x2 - x1 + 1e-6) // a)
        if n >= hip["casas_min_hilera"]:
            n = min(n, hip["casas_max_hilera"])
            hileras.append([box(x1 + i * a, y0, x1 + (i + 1) * a, y0 + h) for i in range(n)])
    return hileras


def _modulos(U, Z, acc, hip, sep, acera, fase):
    """Coloca módulos de calle de abajo arriba en la zona unifamiliar.

    U  zona edificable (retranqueos y separación al corte ya aplicados)
    Z  zona unifamiliar completa (por donde puede ir la calzada)
    """
    F, P, C = hip["fondo_casa_m"], hip["plaza_fondo_m"], hip["calzada_m"]
    a_ = hip["acera_m"] if acera else 0.0
    g = max(sep, 2 * hip["jardin_trasero_m"])
    minx, miny, maxx, maxy = Z.bounds
    mods = []
    y = U.bounds[1] + fase
    while True:
        dobles = y + 2 * F + 2 * (P + a_) + C
        if dobles <= U.bounds[3] + 1e-6:
            yc = y + F + P + a_
            filas = [(y, "abajo"), (yc + C + P + a_, "arriba")]
            nxt = dobles + g
        elif y + F + P + a_ + C <= maxy + 1e-6:      # módulo simple: casas abajo, calle arriba
            yc = y + F + P + a_
            filas = [(y, "abajo")]
            nxt = None
        else:
            break
        calz = _pieza_que_toca(Z.intersection(box(minx - 1, yc, maxx + 1, yc + C)), acc)
        if calz is not None:
            # Tramo con el ancho completo de calzada que arranca junto al acceso.
            tr = _tramos_en_franja(prep(Z), minx, maxx, yc, C, 0.0, C, None, hip["paso_rejilla_m"])
            tr = [t for t in tr if t.distance(acc) <= C]
            if tr:
                t = min(tr, key=lambda t: t.distance(acc))
                izq = calz.intersection(acc).centroid.x < calz.centroid.x
                x_lim = t.bounds[2] if izq else t.bounds[0]
                x1, x2 = (minx - 1, x_lim) if izq else (x_lim, maxx + 1)
                calz = _limpia(calz.intersection(box(x1, yc, x2, yc + C)))
                mods.append({"yc": yc, "filas": filas, "calz_full": calz, "x_lim": x_lim, "izq": izq})
        if nxt is None:
            break
        y = nxt
    return mods


def _resolver_modulo(m, U, acc, hip, sep, prohibido=None):
    """Casas, plazas y calzada (desde el acceso hasta la última casa) de un módulo."""
    F, P, C = hip["fondo_casa_m"], hip["plaza_fondo_m"], hip["calzada_m"]
    calz = m["calz_full"]
    cx = calz.intersection(acc.buffer(0.01)).centroid.x if calz.intersects(acc) else calz.bounds[0]
    izq = m.get("izq", cx < calz.centroid.x)
    x_lim = m.get("x_lim", calz.bounds[2] if izq else calz.bounds[0])
    hileras = []
    for y0, lado in m["filas"]:
        for h in _filas_casas(U, y0, F, hip, sep, prohibido):
            # Solo casas con frente a la calzada de ancho completo.
            h = [c for c in h if (c.bounds[2] <= x_lim + 1e-6 if izq else c.bounds[0] >= x_lim - 1e-6)]
            if len(h) >= hip["casas_min_hilera"]:
                hileras.append((lado, h))
    casas = [c for _, h in hileras for c in h]
    if not casas:
        return None
    xe = max(c.bounds[2] for c in casas) if izq else min(c.bounds[0] for c in casas)
    x1, x2 = (calz.bounds[0] - 1, xe) if izq else (xe, calz.bounds[2] + 1)
    calzada = _limpia(calz.intersection(box(x1, m["yc"], x2, m["yc"] + C)))
    largo = abs(xe - cx)
    return {"yc": m["yc"], "hileras": hileras, "calzada": calzada, "izq": izq, "xe": xe, "largo": largo,
            "x_lim": x_lim}


def _plazas_casa(casa, lado, yc, hip, acera):
    """Banda de plazas delante de una casa (entre la casa y la calzada)."""
    P, C = hip["plaza_fondo_m"], hip["calzada_m"]
    x1, _, x2, _ = casa.bounds
    if lado == "abajo":
        return box(x1, yc - P, x2, yc)
    return box(x1, yc + C, x2, yc + C + P)


def _recuento_hileras(casas, sep):
    """Nº de casas por hilera (casas contiguas en la misma franja)."""
    filas = {}
    for c in casas:
        filas.setdefault(round(c.bounds[1], 2), []).append(c.bounds)
    out = []
    for _, bs in sorted(filas.items()):
        bs.sort()
        n = 1
        for a, b in zip(bs, bs[1:]):
            if b[0] - a[2] > 0.01:
                out.append(n)
                n = 1
            else:
                n += 1
        out.append(n)
    return out


def _aceras(mod, hip):
    C, P, a_ = hip["calzada_m"], hip["plaza_fondo_m"], hip["acera_m"]
    x1, _, x2, _ = mod["calzada"].bounds
    return [box(x1, mod["yc"] - P - a_, x2, mod["yc"] - P), box(x1, mod["yc"] + C + P, x2, mod["yc"] + C + P + a_)]


# --------------------------------------------------------------------------- #
# Una variante
# --------------------------------------------------------------------------- #
def variante(ctx, ang, pct, uni_en, remate, acera):
    hip, com = ctx["hip"], ctx["comun"]
    sep = float(com["separacion_edificios_m"])
    c = ctx["poly"].centroid
    pts = _rot_pts(ctx["pts"], -ang, c)
    poly = Polygon(pts)
    ls = lados(pts, ctx["ccw"])
    acc = unary_union([l["_seg"] for l in ls if l["indice"] in ctx["accesos"]]).buffer(0.5)
    notas, avisos = [], []

    # 1. Zonificación
    if pct >= 100:
        Zu, Zm = poly, Polygon()
    elif pct <= 0:
        Zu, Zm = Polygon(), poly
    else:
        yc, (Zu, Zm) = _corte(poly, pct / 100.0, abajo=(uni_en == "abajo"))
    corte = None
    if not Zu.is_empty and not Zm.is_empty:
        corte = box(poly.bounds[0] - 1, yc - sep / 2, poly.bounds[2] + 1, yc + sep / 2)

    def edificable(Z, uso):
        if Z.is_empty:
            return Polygon()
        u = ctx[uso]
        E = zona_retranqueos(poly, ls, ctx["fachadas"], u["retranqueo_fachada_m"], u["retranqueo_linderos_m"])
        E = _limpia(E.intersection(Z))
        return _limpia(E.difference(corte)) if corte is not None else E

    U, M = edificable(Zu, "uni"), edificable(Zm, "multi")

    # 2. Zona unifamiliar: mejor fase de los módulos de calle
    mods = []
    if not U.is_empty:
        mejor, mejor_n = [], -1
        g = max(sep, 2 * hip["jardin_trasero_m"])
        periodo = 2 * hip["fondo_casa_m"] + 2 * hip["plaza_fondo_m"] + hip["calzada_m"] + g
        f = 0.0
        while f < periodo:
            res = [r for r in (_resolver_modulo(m, U, acc, hip, sep)
                               for m in _modulos(U, Zu, acc, hip, sep, acera, f)) if r]
            n = sum(len(h) for r in res for _, h in r["hileras"])
            if n > mejor_n:
                mejor, mejor_n, fase = res, n, f
            f += hip["paso_fase_m"]
        mods = mejor

    # Remates de calle
    remates = []
    C = hip["calzada_m"]
    if mods:
        if remate == "lazo":
            pares, resto = [], []
            orden = sorted(mods, key=lambda m: m["yc"])
            i = 0
            while i < len(orden):
                if i + 1 < len(orden) and orden[i]["izq"] == orden[i + 1]["izq"]:
                    pares.append((orden[i], orden[i + 1]))
                    i += 2
                else:
                    resto.append(orden[i])
                    i += 1
            for m1, m2 in pares:
                # Vial transversal al final de la calle más corta, dentro de la parcela.
                xe = min(m1["xe"], m2["xe"]) if m1["izq"] else max(m1["xe"], m2["xe"])
                x1, x2 = (xe - C, xe) if m1["izq"] else (xe, xe + C)
                remates.append(_limpia(box(x1, m1["yc"], x2, m2["yc"] + C).intersection(poly)))
                for m in (m1, m2):
                    m["largo"] = 0.0   # con lazo no hay vía sin salida
            if resto:
                notas.append("Lazo: un módulo de calle sin pareja → se remata con martillo.")
            if not pares:
                remate = "martillo"   # el lazo no ha sido posible: equivale a martillo
            remate_mod = {id(m): "martillo" for m in resto}
        else:
            remate_mod = {id(m): remate for m in mods}
        Lm = hip["martillo_largo_m"]
        for m in mods:
            if remate_mod.get(id(m)) == "martillo":
                xe = m["xe"]
                x1, x2 = (xe - C, xe) if m["izq"] else (xe, xe + C)
                remates.append(_limpia(box(x1, m["yc"] + C / 2 - Lm / 2, x2, m["yc"] + C / 2 + Lm / 2)
                                       .intersection(poly)))
                m["largo_con_martillo"] = m["largo"]
                m["largo"] = 0.0
        # Recolocar casas evitando los remates
        if remates:
            prohib = unary_union(remates).buffer(0.01)
            nuevos = []
            for m in mods:
                filas = sorted({(h[0].bounds[1], lado) for lado, h in m["hileras"]})
                r = _resolver_modulo({"yc": m["yc"], "filas": filas, "calz_full": m["calzada"],
                                      "izq": m["izq"], "x_lim": m["x_lim"]}, U, acc, hip, sep, prohib)
                if r:
                    r["largo"] = m["largo"]
                    nuevos.append(r)
            mods = nuevos

    lista, aceras, hileras_n = [], [], []      # (casa, banda de plazas o None)
    for m in mods:
        for lado, h in m["hileras"]:
            hileras_n.append(len(h))
            for casa in h:
                b = _plazas_casa(casa, lado, m["yc"], hip, acera)
                lista.append((casa, None if any(b.intersects(r) for r in remates) else b))
        if acera:
            lados_con_casas = {lado for lado, h in m["hileras"] if h}
            ab, ar = _aceras(m, hip)
            aceras += ([ab] if "abajo" in lados_con_casas else []) + ([ar] if "arriba" in lados_con_casas else [])
    # Casas más cercanas al acceso primero: si sobran, se quitan las del fondo de la calle.
    lista.sort(key=lambda cb: cb[0].distance(acc))
    por_casa = int((hip["ancho_casa_m"] - hip["paso_peatonal_casa_m"]) // hip["plaza_ancho_m"])

    # 3. Reparto de techo y viviendas
    Emax = ctx["sup"] * com["edificabilidad_m2m2"]
    vmax = int(com["viviendas_max"])
    pl_m = int(ctx["multi"]["plantas_max"])
    if "altura_max_m" in ctx["multi"]:
        pl_m = min(pl_m, int(ctx["multi"]["altura_max_m"] // hip["altura_planta_m"] + 1e-9))
    cand = []
    if not M.is_empty:
        cand = bloques_lineales(M, 0.0, hip["fondo_bloque_m"], sep, hip["longitud_min_bloque_m"],
                                hip["longitud_max_bloque_m"], hip["paso_rejilla_m"])
        cand.sort(key=lambda b: (b.centroid.y, b.centroid.x))
    huella_max_m = ctx["multi"]["ocupacion_pct"] / 100 * Zm.area * ctx["f_sup"] if not Zm.is_empty else 0

    def colocar_bloques(pisos_obj):
        bl = []
        if not pisos_obj or not cand:
            return bl, 0
        falta = min(pisos_obj * hip["sup_piso_m2"] / pl_m, huella_max_m)
        for b in cand:
            if falta <= 1:
                break
            x1, y1, x2, y2 = b.bounds
            fondo = y2 - y1
            largo = min(x2 - x1, math.ceil(falta / fondo / 0.5) * 0.5)
            if largo < hip["longitud_min_bloque_m"]:
                largo = hip["longitud_min_bloque_m"] if (x2 - x1) >= hip["longitud_min_bloque_m"] else 0
            if largo <= 0:
                continue
            bl.append(box(x1, y1, x1 + largo, y2))
            falta -= largo * fondo
        cap = sum(b.area for b in bl) * pl_m
        return bl, min(pisos_obj, int(cap // hip["sup_piso_m2"] + 1e-6))

    tope = min(len(lista), vmax, int(Emax // hip["sup_casa_m2"]))
    mejor = None
    for n in range(tope, max(-1, tope - 16), -1):
        pisos_obj = max(0, min(vmax - n, int((Emax - n * hip["sup_casa_m2"]) // hip["sup_piso_m2"])))
        bl, n_p = colocar_bloques(pisos_obj)
        clave = (n + n_p, n * hip["sup_casa_m2"] + n_p * hip["sup_piso_m2"])
        if mejor is None or clave > mejor[0]:
            mejor = (clave, n, bl, n_p, pisos_obj)
    _, n_casas, bloques, n_pisos, pisos_obj = mejor
    if n_casas < len(lista):
        notas.append(f"Se colocan {n_casas} de {len(lista)} casas posibles para maximizar viviendas y techo.")
    if pisos_obj and n_pisos < pisos_obj:
        notas.append(f"La zona multifamiliar solo admite {n_pisos} de {pisos_obj} pisos.")
    casas = [c for c, _ in lista[:n_casas]]
    plazas_u = [b for _, b in lista[:n_casas] if b is not None]
    n_plazas_u = len(plazas_u) * por_casa
    techo_u = n_casas * hip["sup_casa_m2"]
    hileras_n = _recuento_hileras(casas, sep)

    # Bolsa de aparcamiento para las plazas que faltan
    viv = n_casas + n_pisos
    necesarias = int(com["plazas_por_vivienda"]) * viv
    falta_pl = max(0, necesarias - n_plazas_u)
    bolsas, viales_bolsa, n_bolsa, largo_bolsa = [], [], 0, 0.0
    if falta_pl:
        P = hip["plaza_fondo_m"]
        W = 2 * P + C
        ocupado = unary_union(casas + bloques + plazas_u + [m["calzada"] for m in mods] + remates + aceras)
        da = hip["distancia_aparcamiento_edificio_m"]
        if hip["aparcamiento_fuera_retranqueo"]:
            base = M if not M.is_empty else U
        else:
            base = Zm if not Zm.is_empty else Zu
        libre = _limpia(base.intersection(poly).difference(ocupado.buffer(da) if not ocupado.is_empty else Polygon()))
        if corte is not None and not Zm.is_empty:
            libre = _limpia(libre.difference(corte))
        y = libre.bounds[1] if not libre.is_empty else 0
        pa = hip["plaza_ancho_m"]
        dmax_acc = max(ctx["uni"]["retranqueo_fachada_m"], ctx["multi"]["retranqueo_fachada_m"],
                       ctx["uni"]["retranqueo_linderos_m"], ctx["multi"]["retranqueo_linderos_m"]) + 3.0
        while falta_pl > 0 and not libre.is_empty and y + W <= libre.bounds[3]:
            tramos = _tramos_en_franja(prep(libre), libre.bounds[0], libre.bounds[2], y, W, 0.0,
                                       2 * pa, None, hip["paso_rejilla_m"])
            usado = False
            for r in sorted(tramos, key=lambda r: r.distance(acc)):
                if r.distance(acc) > dmax_acc:  # sin conexión razonable con el acceso
                    continue
                x1, y1, x2, y2 = r.bounds
                n_max = 2 * int((x2 - x1) // pa)
                n = min(n_max, falta_pl + (falta_pl % 2))
                largo = math.ceil(n / 2) * pa
                cerca_izq = abs(x1 - acc.centroid.x) < abs(x2 - acc.centroid.x)
                rr = box(x1, y1, x1 + largo, y2) if cerca_izq else box(x2 - largo, y1, x2, y2)
                bolsas.append(rr)
                # vial de conexión con el acceso
                vx1, vx2 = (poly.bounds[0] - 1, rr.bounds[0]) if cerca_izq else (rr.bounds[2], poly.bounds[2] + 1)
                vial = _pieza_que_toca(poly.intersection(box(vx1, y1 + P, vx2, y1 + P + C)), acc)
                if vial is not None:
                    viales_bolsa.append(vial)
                n_bolsa += n
                largo_bolsa = max(largo_bolsa, largo + (vial.length / 2 - C if vial is not None else 0))
                falta_pl -= n
                usado = True
                if falta_pl <= 0:
                    break
            y += W if usado else 1.0

    # 4. Comprobaciones
    huella_u = sum(c.area for c in casas)
    huella_m = sum(b.area for b in bloques)
    techo = techo_u + n_pisos * hip["sup_piso_m2"]
    plazas = n_plazas_u + n_bolsa
    ocA_u = 100 * huella_u / (Zu.area * ctx["f_sup"]) if not Zu.is_empty else 0
    ocA_m = 100 * huella_m / (Zm.area * ctx["f_sup"]) if not Zm.is_empty else 0
    ocB = 100 * (huella_u + huella_m) / ctx["sup"]
    fondo_saco = max([m["largo"] for m in mods] + [0.0])
    chk = {
        "hay_viviendas": viv > 0,
        "viviendas": viv <= vmax,
        "techo": techo <= Emax + 0.5,
        "plazas": plazas >= necesarias,
        "ocupacion_A": ocA_u <= ctx["uni"]["ocupacion_pct"] + 1e-6 and ocA_m <= ctx["multi"]["ocupacion_pct"] + 1e-6,
        "fondo_saco_SI5": fondo_saco <= hip["fondo_saco_max_m"] + 1e-6,
        "itinerario_peatonal": acera or not mods,
    }
    if not chk["plazas"]:
        avisos.append(f"Faltan {necesarias - plazas} plazas.")
    if not chk["fondo_saco_SI5"]:
        avisos.append(f"Calle sin salida de {fondo_saco:.0f} m sin espacio de maniobra (DB-SI SI 5, revisar).")
    if not chk["itinerario_peatonal"]:
        avisos.append("Calle de casas sin acera: itinerario peatonal por la calzada (DB-SUA 9, revisar).")
    if largo_bolsa > hip["fondo_saco_max_m"]:
        notas.append(f"La bolsa de aparcamiento es un fondo de saco de ≈ {largo_bolsa:.0f} m (revisar).")
    if any(n > 0 for n in hileras_n) and len(hileras_n):
        notas.append("Hileras: " + " + ".join(str(n) for n in hileras_n) + " casas.")

    geo = {
        "parcela": poly, "zona_uni": Zu, "zona_multi": Zm, "edif_uni": U, "edif_multi": M,
        "casas": casas, "plazas_casas": plazas_u, "calzadas": [m["calzada"] for m in mods] + remates + viales_bolsa,
        "bolsas": bolsas, "bloques": bloques, "aceras": aceras,
    }
    geo = {k: ([affinity.rotate(g, ang, origin=c) for g in v] if isinstance(v, list)
               else affinity.rotate(v, ang, origin=c)) for k, v in geo.items()}
    return {
        "angulo_hileras": round(ang % 180, 1),
        "pct_zona_unifamiliar": pct,
        "unifamiliar_en": _lado_txt(ang, uni_en) if 0 < pct < 100 else ("todo" if pct >= 100 else "—"),
        "remate": remate, "acera": acera,
        "casas": n_casas, "pisos": n_pisos, "viviendas": viv,
        "bloques": len(bloques), "plantas_bloque": pl_m,
        "techo_m2": round(techo, 1), "aprovechamiento_pct": round(100 * techo / Emax, 1),
        "plazas": plazas, "plazas_necesarias": necesarias, "plazas_casas": n_plazas_u, "plazas_bolsa": n_bolsa,
        "huella_m2": round(huella_u + huella_m, 1),
        "ocupacion_A_uni_pct": round(ocA_u, 1), "ocupacion_A_multi_pct": round(ocA_m, 1),
        "ocupacion_B_pct": round(ocB, 1),
        "fondo_saco_m": round(fondo_saco, 1),
        "comprobaciones": chk, "cumple": all(chk.values()),
        "avisos": avisos, "notas": notas, "_geo": geo,
    }


def _lado_txt(ang, uni_en):
    """Rumbo (N, NE…) del lado 'abajo'/'arriba' del marco girado."""
    a = math.radians(ang)
    dy0 = -1.0 if uni_en == "abajo" else 1.0
    dx, dy = -math.sin(a) * dy0, math.cos(a) * dy0
    return _rumbo_txt((math.degrees(math.atan2(dx, dy)) + 360) % 360)


# --------------------------------------------------------------------------- #
# Barrido y ranking
# --------------------------------------------------------------------------- #
def angulos(ctx):
    a = ctx["barrido"]["angulo_hileras"]
    if a == "fachadas":
        # Hileras paralelas a cada fachada. Las paralelas al acceso no pueden
        # conectar su calle con él y quedan al final del ranking.
        ls = lados(ctx["pts"], ctx["ccw"])
        return sorted({round(l["_angulo"] % 180, 2) for l in ls if l["indice"] in ctx["fachadas"]})
    return [float(x) for x in a]


def barrer(ctx):
    b = ctx["barrido"]
    res, vistos = [], set()
    for ang, pct, ue, rem, ac in itertools.product(angulos(ctx), b["pct_zona_unifamiliar"], b["unifamiliar_en"],
                                                    b["remate"], b["acera"]):
        if pct in (0, 100) and ue != b["unifamiliar_en"][0]:
            continue   # sin corte, el lado da igual
        if pct <= 0 and (rem != b["remate"][0] or ac != b["acera"][0]):
            continue   # sin calle de casas
        r = variante(ctx, ang, pct, ue, rem, ac)
        clave = (r["angulo_hileras"], pct, r["unifamiliar_en"], r["remate"], ac, r["casas"], r["pisos"], r["plazas"])
        if clave not in vistos:
            vistos.add(clave)
            res.append(r)
    res.sort(key=lambda r: (not r["cumple"], -sum(r["comprobaciones"].values()), -r["viviendas"],
                            -r["techo_m2"], -(r["plazas"] - r["plazas_necesarias"] >= 0), r["ocupacion_B_pct"]))
    for i, r in enumerate(res, 1):
        r["id"] = f"V{i:03d}"
    return res


# --------------------------------------------------------------------------- #
# Salidas
# --------------------------------------------------------------------------- #
ESTILO = {
    "parcela": ("none", "#222", 0.35), "zona_uni": ("#f3efe2", "none", 0), "zona_multi": ("#e7eef5", "none", 0),
    "edif_uni": ("none", "#8a6d3b", 0.15), "edif_multi": ("none", "#3b5f8a", 0.15),
    "calzadas": ("#bdbdbd", "#888", 0.08), "plazas_casas": ("#e2e2e2", "#999", 0.06),
    "bolsas": ("#e2e2e2", "#999", 0.06), "aceras": ("#f0e0c0", "#b99", 0.05),
    "casas": ("#e6cfa6", "#5a4630", 0.12), "bloques": ("#9fb4cc", "#2c3e55", 0.15),
}


def _path(g, ox, oy):
    d = []
    for p in _polys(g):
        for anillo in [p.exterior, *p.interiors]:
            cs = list(anillo.coords)
            d.append("M" + " L".join(f"{x - ox:.2f},{oy - y:.2f}" for x, y in cs) + " Z")
    return " ".join(d)


def svg_grupo(r, ctx, ox, oy):
    out = []
    for capa in ["zona_uni", "zona_multi", "calzadas", "bolsas", "plazas_casas", "aceras", "casas", "bloques",
                 "edif_uni", "edif_multi", "parcela"]:
        fill, stroke, sw = ESTILO[capa]
        gs = r["_geo"][capa]
        gs = gs if isinstance(gs, list) else [gs]
        dash = ' stroke-dasharray="1,0.8"' if capa.startswith("edif") else ""
        for g in gs:
            if g is None or g.is_empty:
                continue
            out.append(f'<path d="{_path(g, ox, oy)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
    return "\n".join(out)


def _rotulo(r):
    ok = "✔" if r["cumple"] else "✘"
    return (f'{r["id"]} {ok} · {r["casas"]} casas + {r["pisos"]} pisos = {r["viviendas"]} viv',
            f'{r["techo_m2"]:.0f} m²c ({r["aprovechamiento_pct"]} %) · plazas {r["plazas"]}/{r["plazas_necesarias"]} · '
            f'ocup. {r["ocupacion_B_pct"]} %',
            f'uni {r["pct_zona_unifamiliar"]} % ({r["unifamiliar_en"]}) · remate {r["remate"]} · '
            f'acera {"sí" if r["acera"] else "no"}')


def svg_variante(r, ctx):
    minx, miny, maxx, maxy = ctx["poly"].bounds
    m = 6
    w, h = maxx - minx + 2 * m, maxy - miny + 2 * m + 14
    l1, l2, l3 = _rotulo(r)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w * 8:.0f}" '
            f'height="{h * 8:.0f}" font-family="sans-serif">\n<rect width="100%" height="100%" fill="#fff"/>\n'
            f'<g>{svg_grupo(r, ctx, minx - m, maxy + m)}</g>\n'
            f'<text x="{m}" y="{maxy - miny + 2 * m + 3}" font-size="2.6" font-weight="bold">{l1}</text>\n'
            f'<text x="{m}" y="{maxy - miny + 2 * m + 7}" font-size="2.1">{l2}</text>\n'
            f'<text x="{m}" y="{maxy - miny + 2 * m + 10.5}" font-size="2.1">{l3}</text>\n</svg>\n')


def svg_lamina(rs, ctx, cols=3):
    minx, miny, maxx, maxy = ctx["poly"].bounds
    m = 6
    cw, ch = maxx - minx + 2 * m, maxy - miny + 2 * m + 14
    filas = math.ceil(len(rs) / cols)
    W, H = cols * cw, filas * ch + 12
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W * 5:.0f}" '
              f'height="{H * 5:.0f}" font-family="sans-serif">', '<rect width="100%" height="100%" fill="#fff"/>',
              f'<text x="3" y="7" font-size="4" font-weight="bold">{ctx["nombre"]} — mejores variantes '
              f'(reglas fijas, sin IA) · PENDIENTE DE VALIDAR POR EL ARQUITECTO</text>']
    for i, r in enumerate(rs):
        tx, ty = (i % cols) * cw, 12 + (i // cols) * ch
        l1, l2, l3 = _rotulo(r)
        partes.append(f'<g transform="translate({tx:.1f},{ty:.1f})">{svg_grupo(r, ctx, minx - m, maxy + m)}'
                      f'<text x="{m}" y="{ch - 11}" font-size="2.6" font-weight="bold">{l1}</text>'
                      f'<text x="{m}" y="{ch - 7}" font-size="2.1">{l2}</text>'
                      f'<text x="{m}" y="{ch - 3.5}" font-size="2.1">{l3}</text></g>')
    partes.append("</svg>")
    return "\n".join(partes)


def exportar_dxf(r, ctx, ruta: Path):
    import ezdxf
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.M
    capas = {"parcela": ("PARCELA", 7), "edif_uni": ("RETRANQUEO_UNI", 3), "edif_multi": ("RETRANQUEO_MULTI", 4),
             "calzadas": ("VIARIO", 8), "plazas_casas": ("PLAZAS", 9), "bolsas": ("PLAZAS", 9),
             "aceras": ("ACERAS", 30), "casas": ("CASAS", 1), "bloques": ("BLOQUES", 5)}
    for nombre, color in set(capas.values()):
        doc.layers.add(nombre, color=color)
    doc.layers.add("VOLUMEN_3D", color=6)
    msp = doc.modelspace()
    hp = ctx["hip"]["altura_planta_m"]
    alturas = {"casas": int(ctx["uni"]["plantas_max"]) * hp, "bloques": r["plantas_bloque"] * hp}
    for clave, (capa, _) in capas.items():
        gs = r["_geo"][clave]
        for g in (gs if isinstance(gs, list) else [gs]):
            for p in _polys(g):
                msp.add_lwpolyline(list(p.exterior.coords), close=True, dxfattribs={"layer": capa})
                if clave in alturas:
                    msp.add_lwpolyline(list(p.exterior.coords), close=True,
                                       dxfattribs={"layer": "VOLUMEN_3D", "thickness": alturas[clave]})
    doc.saveas(ruta)


def publico(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Variantes de ordenación con reglas fijas (sin IA).")
    p.add_argument("entrada", type=Path)
    p.add_argument("--top", type=int, default=9, help="Variantes en la lámina (por defecto 9)")
    p.add_argument("--salida", type=Path, default=None, help="Carpeta (por defecto planos/variantes/<nombre>)")
    p.add_argument("--dxf", default=None, help="Exportar a DXF la variante indicada (p. ej. V001)")
    args = p.parse_args(argv)
    try:
        ctx = cargar(args.entrada)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    carpeta = args.salida or Path("planos/variantes") / re.sub(r"[^\w-]+", "_", ctx["nombre"]).strip("_")
    carpeta.mkdir(parents=True, exist_ok=True)

    rs = barrer(ctx)
    top = rs[: args.top]
    (carpeta / "lamina.svg").write_text(svg_lamina(top, ctx), encoding="utf-8")
    for r in top:
        (carpeta / f"{r['id']}.svg").write_text(svg_variante(r, ctx), encoding="utf-8")
    if args.dxf:
        sel = [r for r in rs if r["id"] == args.dxf]
        if not sel:
            print(f"Error: no existe la variante {args.dxf}", file=sys.stderr)
            return 1
        exportar_dxf(sel[0], ctx, carpeta / f"{args.dxf}.dxf")
    (carpeta / "ranking.json").write_text(json.dumps({
        "parcela": ctx["nombre"], "superficie_calculo_m2": ctx["sup"],
        "edificabilidad_m2c": round(ctx["sup"] * ctx["comun"]["edificabilidad_m2m2"], 1),
        "hipotesis": ctx["hip"], "barrido": ctx["barrido"],
        "variantes": [publico(r) for r in rs], "aviso": "PENDIENTE DE VALIDAR POR EL ARQUITECTO",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lineas = [f"VARIANTES DE ORDENACIÓN (reglas fijas, sin IA) — {ctx['nombre']}",
              f"Superficie {ctx['sup']:.0f} m² · edificabilidad {ctx['sup'] * ctx['comun']['edificabilidad_m2m2']:.0f} m²c"
              f" · máx. {ctx['comun']['viviendas_max']} viv · {len(rs)} variantes generadas", "",
              f"{'Id':<6}{'OK':<4}{'Uni%':>5} {'Uni en':<7}{'Remate':<11}{'Acera':<6}{'Casas':>6}{'Pisos':>6}"
              f"{'Viv':>5}{'m²c':>7}{'Plazas':>9}{'Ocup.B%':>8}{'F.saco':>7}"]
    for r in rs:
        lineas.append(f"{r['id']:<6}{'✔' if r['cumple'] else '✘':<4}{r['pct_zona_unifamiliar']:>5} "
                      f"{r['unifamiliar_en']:<7}{r['remate']:<11}{'sí' if r['acera'] else 'no':<6}{r['casas']:>6}"
                      f"{r['pisos']:>6}{r['viviendas']:>5}{r['techo_m2']:>7.0f}"
                      f"{str(r['plazas']) + '/' + str(r['plazas_necesarias']):>9}{r['ocupacion_B_pct']:>8.1f}"
                      f"{r['fondo_saco_m']:>7.0f}")
    lineas += ["", "Detalle de las mejores:"]
    for r in top:
        lineas.append(f"  {r['id']}: " + " ".join(r["avisos"] + r["notas"]))
    lineas += ["", "Hipótesis de diseño (modificables en 'hipotesis'):"]
    lineas += [f"  - {k} = {v}" for k, v in ctx["hip"].items()]
    lineas += ["", f"Lámina: {carpeta / 'lamina.svg'}", "", "PENDIENTE DE VALIDAR POR EL ARQUITECTO"]
    (carpeta / "ranking.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas[:4 + min(len(rs), 25)]))
    print("...")
    print("\n".join(lineas[4 + len(rs):]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
