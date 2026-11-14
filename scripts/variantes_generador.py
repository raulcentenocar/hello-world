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
# Cuenta de resultados: solo se calcula si están TODOS (los valores los da el arquitecto; no hay defectos).
REQ_ECONOMIA = ["precio_venta_casa_eur_m2c", "precio_venta_piso_eur_m2c", "coste_construccion_casa_eur_m2c",
                "coste_construccion_piso_eur_m2c", "coste_urbanizacion_eur_m2", "coste_plaza_superficie_eur",
                "coste_suelo_eur", "gastos_generales_pct"]


def cuenta_resultados(eco, techo_casas, techo_pisos, plazas, sup, huella):
    """Ingresos, costes y beneficio. Devuelve FALTA DATO si falta algún valor."""
    faltan = [k for k in REQ_ECONOMIA if k not in eco]
    if faltan:
        return {"estado": FALTA, "faltan": faltan}
    ingresos = techo_casas * eco["precio_venta_casa_eur_m2c"] + techo_pisos * eco["precio_venta_piso_eur_m2c"]
    construccion = techo_casas * eco["coste_construccion_casa_eur_m2c"] + techo_pisos * eco["coste_construccion_piso_eur_m2c"]
    urbanizacion = max(0.0, sup - huella) * eco["coste_urbanizacion_eur_m2"]
    aparcamiento = plazas * eco["coste_plaza_superficie_eur"]
    gastos = (construccion + urbanizacion + aparcamiento) * eco["gastos_generales_pct"] / 100
    coste = construccion + urbanizacion + aparcamiento + gastos + eco["coste_suelo_eur"]
    beneficio = ingresos - coste
    return {"estado": "OK", "ingresos_eur": round(ingresos), "coste_construccion_eur": round(construccion),
            "coste_urbanizacion_eur": round(urbanizacion), "coste_aparcamiento_eur": round(aparcamiento),
            "gastos_generales_eur": round(gastos), "coste_suelo_eur": round(eco["coste_suelo_eur"]),
            "coste_total_eur": round(coste), "beneficio_eur": round(beneficio),
            "margen_sobre_ventas_pct": round(100 * beneficio / ingresos, 1) if ingresos else 0.0,
            "rentabilidad_sobre_coste_pct": round(100 * beneficio / coste, 1) if coste else 0.0}

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
    # Programa de pisos (hipótesis de producto; sin programa del cliente)
    "tipos_piso": {"2D": {"construida_m2": 85.0}, "3D": {"construida_m2": 105.0}, "4D": {"construida_m2": 125.0}},
    "mix_pisos_pct": {"2D": 30, "3D": 50, "4D": 20},
    "nucleo_ancho_m": 5.0,             # escalera + ascensor a lo largo del bloque (por portal)
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
    "aparcamiento_fuera_retranqueo": True,
    "plazas_accesibles": 2,
    "repartos_probados": 8,            # repartos casas/pisos que se prueban con su aparcamiento            # decisión del arquitecto (F2/F3); su número normativo: FALTA DATO
    "transferencia_accesible_m": 1.2,  # DB-SUA Anejo A: zona de transferencia lateral ≥ 1,20 m  # hipótesis H-APA de F2 (cómputo en retranqueo: FALTA DATO)
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
    eco = {k: v for k, v in (cfg.get("economia") or {}).items() if v is not None}
    return {
        "economia": eco,
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


def secuencia_mix(n, mix):
    """n viviendas cuyo reparto se acerca en cada paso al % objetivo (mayor déficit primero)."""
    tipos = list(mix.keys())
    tot = float(sum(mix.values())) or 1.0
    cnt = {t: 0 for t in tipos}
    out = []
    for i in range(1, n + 1):
        t = max(tipos, key=lambda t: (mix[t] / tot * i - cnt[t], -tipos.index(t)))
        cnt[t] += 1
        out.append(t)
    return out


def colocar_portales(cand, seq, tipos, hip, huella_max):
    """Coloca una planta tipo: portales con núcleo y una vivienda pasante a cada lado.

    Devuelve (bloques, [(vivienda, tipo)], núcleos, nº colocadas, m²c por planta).
    """
    F, nw = hip["fondo_bloque_m"], hip["nucleo_ancho_m"]
    bloques, pisos, nucleos = [], [], []
    k, huella = 0, 0.0
    for b in cand:
        if k >= len(seq):
            break
        x1, y1, x2, _ = b.bounds
        x = x1
        while k < len(seq):
            wl = tipos[seq[k]]["construida_m2"] / F
            if k + 1 < len(seq):
                wr = tipos[seq[k + 1]]["construida_m2"] / F
                fin = x + wl + nw + wr
                if fin <= x2 + 1e-6 and huella + (fin - x1) * F <= huella_max + 1e-6:
                    pisos += [(box(x, y1, x + wl, y1 + F), seq[k]), (box(x + wl + nw, y1, fin, y1 + F), seq[k + 1])]
                    nucleos.append(box(x + wl, y1, x + wl + nw, y1 + F))
                    x, k = fin, k + 2
                    continue
            fin = x + wl + nw
            if fin <= x2 + 1e-6 and huella + (fin - x1) * F <= huella_max + 1e-6:
                pisos.append((box(x, y1, x + wl, y1 + F), seq[k]))
                nucleos.append(box(x + wl, y1, fin, y1 + F))
                x, k = fin, k + 1
                continue
            break
        if x > x1 + 1e-6:
            bloques.append(box(x1, y1, x, y1 + F))
            huella += (x - x1) * F
    techo = sum(tipos[t]["construida_m2"] for _, t in pisos) + len(nucleos) * nw * F
    return bloques, pisos, nucleos, k, techo


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

    # 3. Reparto de techo y viviendas (programa de pisos por portales)
    Emax = ctx["sup"] * com["edificabilidad_m2m2"]
    vmax = int(com["viviendas_max"])
    pl_m = int(ctx["multi"]["plantas_max"])
    if "altura_max_m" in ctx["multi"]:
        pl_m = min(pl_m, int(ctx["multi"]["altura_max_m"] // hip["altura_planta_m"] + 1e-9))
    huella_max_m = ctx["multi"]["ocupacion_pct"] / 100 * Zm.area * ctx["f_sup"] if not Zm.is_empty else 0
    tipos = hip["tipos_piso"]
    mix = {t: v for t, v in hip["mix_pisos_pct"].items() if v > 0 and t in tipos}
    P, pa = hip["plaza_fondo_m"], hip["plaza_ancho_m"]
    da = hip["distancia_aparcamiento_edificio_m"]
    calles = [m["calzada"] for m in mods] + remates
    red = unary_union(calles).buffer(1.0) if calles else Polygon()
    dmax_acc = max(ctx["uni"]["retranqueo_fachada_m"], ctx["multi"]["retranqueo_fachada_m"],
                   ctx["uni"]["retranqueo_linderos_m"], ctx["multi"]["retranqueo_linderos_m"]) + 3.0
    if hip["aparcamiento_fuera_retranqueo"]:
        base_ap = M if not M.is_empty else U
    else:
        base_ap = Zm if not Zm.is_empty else Zu

    def bolsa(libre, falta_pl, n_acc):
        """Bandas de aparcamiento de doble o simple crujía, conectadas al acceso o a la calle de casas."""
        bolsas, viales, n_bolsa, largo_bolsa, accesibles = [], [], 0, 0.0, []
        acc_pend = n_acc
        y = libre.bounds[1] if not libre.is_empty else 0
        while falta_pl > 0 and not libre.is_empty and y + P + C <= libre.bounds[3]:
            doble = y + 2 * P + C <= libre.bounds[3]
            W = 2 * P + C if doble else P + C
            lados_pl = 2 if doble else 1
            tramos = _tramos_en_franja(prep(libre), libre.bounds[0], libre.bounds[2], y, W, 0.0,
                                       2 * pa, None, hip["paso_rejilla_m"])
            usado = False
            for r in sorted(tramos, key=lambda r: r.distance(acc)):
                conectado_red = not red.is_empty and r.distance(red) <= 0.01
                if r.distance(acc) > dmax_acc and not conectado_red:
                    continue
                x1, y1, x2, y2 = r.bounds
                ancho_acc = acc_pend * pa + math.ceil(acc_pend / 2) * hip["transferencia_accesible_m"]
                if lados_pl == 1:
                    cap = int((x2 - x1 - ancho_acc) // pa) + acc_pend
                else:
                    cap = 2 * int((x2 - x1) // pa) - math.ceil(ancho_acc / pa) + acc_pend
                if cap <= 0:
                    continue
                nb = min(cap, falta_pl + (falta_pl % lados_pl))
                largo = min(ancho_acc + math.ceil(max(0, nb - acc_pend) / lados_pl) * pa, x2 - x1)
                cerca_izq = abs(x1 - acc.centroid.x) < abs(x2 - acc.centroid.x)
                rr = box(x1, y1, x1 + largo, y2) if cerca_izq else box(x2 - largo, y1, x2, y2)
                bolsas.append(rr)
                if acc_pend:
                    ax = rr.bounds[0] if cerca_izq else rr.bounds[2] - ancho_acc
                    accesibles.append(box(ax, y1, ax + ancho_acc, y1 + P))
                    acc_pend = 0
                if not conectado_red:
                    vx1, vx2 = (poly.bounds[0] - 1, rr.bounds[0]) if cerca_izq else (rr.bounds[2], poly.bounds[2] + 1)
                    ya = y1 + (P if doble else 0)
                    vial = _pieza_que_toca(poly.intersection(box(vx1, ya, vx2, ya + C)), acc)
                    if vial is not None:
                        viales.append(vial)
                        largo_bolsa = max(largo_bolsa, largo + vial.length / 2 - C)
                n_bolsa += nb
                falta_pl -= nb
                usado = True
                if falta_pl <= 0:
                    break
            y += W if usado else 1.0
        return {"bolsas": bolsas, "viales_bolsa": viales, "n_bolsa": n_bolsa, "largo_bolsa": largo_bolsa,
                "accesibles": accesibles, "falta": max(0, falta_pl)}

    def solucion(n_casas, u):
        """Casas + aparcamiento reservado primero + portales en el suelo que queda."""
        casas = [c for c, _ in lista[:n_casas]]
        plazas_u = [b for _, b in lista[:n_casas] if b is not None]
        n_plazas_u = len(plazas_u) * por_casa
        n_pisos = u * pl_m
        necesarias = int(com["plazas_por_vivienda"]) * (n_casas + n_pisos)
        n_acc = int(hip["plazas_accesibles"]) if n_pisos else 0
        falta_pl = max(0, necesarias - n_plazas_u, n_acc)
        ocupado = unary_union(casas + plazas_u + calles + aceras)
        ap = {"bolsas": [], "viales_bolsa": [], "n_bolsa": 0, "largo_bolsa": 0.0, "accesibles": [], "falta": 0}
        if falta_pl and not base_ap.is_empty:
            libre = _limpia(base_ap.intersection(poly).difference(ocupado.buffer(da) if not ocupado.is_empty else Polygon()))
            if corte is not None and not Zm.is_empty:
                libre = _limpia(libre.difference(corte))
            ap = bolsa(libre, falta_pl, n_acc)
        elif falta_pl:
            ap["falta"] = falta_pl
        lay = ([], [], [], 0, 0.0)
        if u and not M.is_empty:
            ocupa_ap = unary_union(ap["bolsas"] + ap["viales_bolsa"])
            Mlib = _limpia(M.difference(ocupa_ap.buffer(da))) if not ocupa_ap.is_empty else M
            cand = bloques_lineales(Mlib, 0.0, hip["fondo_bloque_m"], sep, hip["longitud_min_bloque_m"],
                                    hip["longitud_max_bloque_m"], hip["paso_rejilla_m"]) if not Mlib.is_empty else []
            cand.sort(key=lambda b: (b.centroid.y, b.centroid.x))
            lay = colocar_portales(cand, secuencia_mix(u, mix), tipos, hip, huella_max_m)
        ok_pl = n_plazas_u + ap["n_bolsa"] >= necesarias and not (n_acc and not ap["accesibles"])
        return {"n": n_casas, "u": u, "lay": lay, "casas": casas, "plazas_u": plazas_u, "n_plazas_u": n_plazas_u,
                "n_pisos": n_pisos, "necesarias": necesarias, "n_acc": n_acc, "ap": ap, "ok_pl": ok_pl,
                "completo": lay[3] == u}

    # Búsqueda del reparto: más viviendas, después más techo; debe caber entero (pisos y plazas).
    tope = min(len(lista), vmax, int(Emax // hip["sup_casa_m2"]))
    elegido, mejor_clave, respaldo = None, None, None
    for n in range(tope, max(-1, tope - 16), -1):
        lim_viv, lim_techo = vmax - n, Emax - n * hip["sup_casa_m2"]
        u_max = (lim_viv // pl_m) if (mix and not M.is_empty) else 0
        if mejor_clave is not None and n + u_max * pl_m < mejor_clave[0]:
            continue
        if n and min(_recuento_hileras([c for c, _ in lista[:n]], sep)) < hip["casas_min_hilera"]:
            continue   # quitar casas no puede dejar hileras por debajo del mínimo
        for u in range(u_max, -1, -1):
            seq = secuencia_mix(u, mix)
            if pl_m * sum(tipos[t]["construida_m2"] for t in seq) > lim_techo + 1e-6:
                continue
            if mejor_clave is not None and n + u * pl_m < mejor_clave[0]:
                break
            sol = solucion(n, u)
            if respaldo is None:
                respaldo = sol
            if not sol["completo"] or pl_m * sol["lay"][4] > lim_techo + 1e-6:
                continue
            if sol["ok_pl"]:
                clave = (n + u * pl_m, n * hip["sup_casa_m2"] + pl_m * sol["lay"][4])
                if mejor_clave is None or clave > mejor_clave:
                    elegido, mejor_clave = sol, clave
                break
    if elegido is None:
        elegido = respaldo if respaldo is not None else solucion(min(tope, len(lista)), 0)
        notas.append("Ningún reparto cabe con todas sus plazas: se muestra el de más viviendas.")
    sol = elegido
    n_casas, n_pisos = sol["n"], sol["n_pisos"]
    bloques, pisos_geo, nucleos, u_planta, techo_planta = sol["lay"]
    ap = sol["ap"]
    ap.update({"casas": sol["casas"], "plazas_u": sol["plazas_u"], "n_plazas_u": sol["n_plazas_u"],
               "viv": n_casas + n_pisos, "necesarias": sol["necesarias"], "n_acc": sol["n_acc"]})
    if n_casas < len(lista):
        notas.append(f"Se colocan {n_casas} de {len(lista)} casas posibles para maximizar viviendas y techo.")
    casas, plazas_u, n_plazas_u = ap["casas"], ap["plazas_u"], ap["n_plazas_u"]
    techo_u = n_casas * hip["sup_casa_m2"]
    techo_m = pl_m * techo_planta
    hileras_n = _recuento_hileras(casas, sep)
    mix_real = {}
    for _, t in pisos_geo:
        mix_real[t] = mix_real.get(t, 0) + pl_m
    if n_pisos:
        notas.append(f"Pisos: {u_planta} por planta × {pl_m} plantas en {len(nucleos)} portales ("
                     + ", ".join(f"{k} {v}" for k, v in sorted(mix_real.items())) + ").")

    viv, necesarias, n_acc = ap["viv"], ap["necesarias"], ap["n_acc"]
    bolsas, viales_bolsa, n_bolsa = ap["bolsas"], ap["viales_bolsa"], ap["n_bolsa"]
    largo_bolsa, accesibles = ap["largo_bolsa"], ap["accesibles"]

    # 4. Comprobaciones
    huella_u = sum(c.area for c in casas)
    huella_m = sum(b.area for b in bloques)
    techo = techo_u + techo_m
    plazas = n_plazas_u + n_bolsa
    ocA_u = 100 * huella_u / (Zu.area * ctx["f_sup"]) if not Zu.is_empty else 0
    ocA_m = 100 * huella_m / (Zm.area * ctx["f_sup"]) if not Zm.is_empty else 0
    ocB = 100 * (huella_u + huella_m) / ctx["sup"]
    fondo_saco = max([m["largo"] for m in mods] + [0.0])
    chk = {
        "hay_viviendas": viv > 0,
        "viviendas": viv <= vmax,
        "techo": techo <= Emax + 0.5,
        "plazas": plazas >= necesarias and not (n_acc and not accesibles),
        "ocupacion_A": ocA_u <= ctx["uni"]["ocupacion_pct"] + 1e-6 and ocA_m <= ctx["multi"]["ocupacion_pct"] + 1e-6,
        "fondo_saco_SI5": fondo_saco <= hip["fondo_saco_max_m"] + 1e-6,
        "itinerario_peatonal": acera or not mods,
    }
    if not chk["plazas"]:
        avisos.append(f"Faltan {necesarias - plazas} plazas." if plazas < necesarias else "Faltan las plazas accesibles.")
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
        "pisos": [g for g, _ in pisos_geo], "nucleos": nucleos, "accesibles": accesibles,
    }
    geo = {k: ([affinity.rotate(g, ang, origin=c) for g in v] if isinstance(v, list)
               else affinity.rotate(v, ang, origin=c)) for k, v in geo.items()}
    return {
        "angulo_hileras": round(ang % 180, 1),
        "pct_zona_unifamiliar": pct,
        "unifamiliar_en": _lado_txt(ang, uni_en) if 0 < pct < 100 else ("todo" if pct >= 100 else "—"),
        "remate": remate, "acera": acera,
        "casas": n_casas, "pisos": n_pisos, "viviendas": viv,
        "bloques": len(bloques), "plantas_bloque": pl_m, "portales": len(nucleos),
        "pisos_por_planta": u_planta, "mix_pisos": mix_real, "tipos_pisos_planta": [t for _, t in pisos_geo],
        "plazas_accesibles": n_acc if accesibles else 0,
        "techo_m2": round(techo, 1), "aprovechamiento_pct": round(100 * techo / Emax, 1),
        "plazas": plazas, "plazas_necesarias": necesarias, "plazas_casas": n_plazas_u, "plazas_bolsa": n_bolsa,
        "huella_m2": round(huella_u + huella_m, 1),
        "ocupacion_A_uni_pct": round(ocA_u, 1), "ocupacion_A_multi_pct": round(ocA_m, 1),
        "ocupacion_B_pct": round(ocB, 1),
        "fondo_saco_m": round(fondo_saco, 1),
        "comprobaciones": chk, "cumple": all(chk.values()),
        "techo_casas_m2": round(techo_u, 1), "techo_pisos_m2": round(techo_m, 1),
        "economia": cuenta_resultados(ctx["economia"], techo_u, techo_m, plazas, ctx["sup"], huella_u + huella_m),
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


OBJETIVOS = {
    "ranking": lambda r: (-r["viviendas"], -r["techo_m2"]),
    "viviendas": lambda r: (-r["viviendas"], -r["techo_m2"]),
    "techo": lambda r: (-r["techo_m2"], -r["viviendas"]),
    "casas": lambda r: (-r["casas"], -r["viviendas"]),
    "ocupacion": lambda r: (r["ocupacion_B_pct"], -r["viviendas"]),
    "beneficio": lambda r: (-(r["economia"].get("beneficio_eur") or -1e18), -r["viviendas"]),
}


def barrer(ctx, objetivo="ranking"):
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
    if objetivo == "ranking":
        res.sort(key=lambda r: (not r["cumple"], -sum(r["comprobaciones"].values()), -r["viviendas"],
                                -r["techo_m2"], -(r["plazas"] - r["plazas_necesarias"] >= 0), r["ocupacion_B_pct"]))
    else:
        res.sort(key=lambda r: (not r["cumple"],) + OBJETIVOS[objetivo](r))
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
    "pisos": ("#b8c9de", "#2c3e55", 0.08), "nucleos": ("#6f86a3", "#2c3e55", 0.08),
    "accesibles": ("#cfe0f5", "#2c5d9a", 0.1),
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
    for capa in ["zona_uni", "zona_multi", "calzadas", "bolsas", "accesibles", "plazas_casas", "aceras", "casas",
                 "bloques", "pisos", "nucleos", "edif_uni", "edif_multi", "parcela"]:
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
             "aceras": ("ACERAS", 30), "casas": ("CASAS", 1), "bloques": ("BLOQUES", 5),
             "pisos": ("PISOS", 150), "nucleos": ("NUCLEOS", 250), "accesibles": ("PLAZAS_ACCESIBLES", 140)}
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


def escribir_csv(rs, ruta: Path):
    """Medición de cada variante para hoja de cálculo (separador ';', decimales con coma)."""
    import csv
    cols = ["id", "cumple", "pct_zona_unifamiliar", "unifamiliar_en", "remate", "acera", "casas", "pisos", "viviendas",
            "portales", "pisos_por_planta", "mix_pisos", "techo_casas_m2", "techo_pisos_m2", "techo_m2",
            "aprovechamiento_pct", "plazas", "plazas_necesarias", "plazas_casas", "plazas_bolsa", "plazas_accesibles",
            "huella_m2", "ocupacion_B_pct", "fondo_saco_m", "beneficio_eur", "margen_sobre_ventas_pct"]
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cols)
        for r in rs:
            fila = dict(r)
            fila["mix_pisos"] = " ".join(f"{k}:{v}" for k, v in sorted(r["mix_pisos"].items()))
            fila["beneficio_eur"] = r["economia"].get("beneficio_eur", "FALTA DATO")
            fila["margen_sobre_ventas_pct"] = r["economia"].get("margen_sobre_ventas_pct", "FALTA DATO")
            w.writerow([str(fila.get(c, "")).replace(".", ",") if isinstance(fila.get(c), float) else fila.get(c, "")
                        for c in cols])


def publico(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Variantes de ordenación con reglas fijas (sin IA).")
    p.add_argument("entrada", type=Path)
    p.add_argument("--top", type=int, default=9, help="Variantes en la lámina (por defecto 9)")
    p.add_argument("--salida", type=Path, default=None, help="Carpeta (por defecto planos/variantes/<nombre>)")
    p.add_argument("--dxf", default=None, help="Exportar a DXF la variante indicada (p. ej. V001)")
    p.add_argument("--objetivo", default="ranking", choices=sorted(OBJETIVOS),
                   help="Criterio de orden tras el cumplimiento (por defecto: ranking)")
    p.add_argument("--parametros", default=None,
                   help="JSON con una variante concreta (lo copia el visor): "
                        '{"ang":0.5,"pct":60,"uni_en":"abajo","remate":"martillo","acera":true,"hipotesis":{...}}. '
                        "Calcula solo esa variante y exporta su DXF y SVG.")
    args = p.parse_args(argv)
    try:
        ctx = cargar(args.entrada)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    carpeta = args.salida or Path("planos/variantes") / re.sub(r"[^\w-]+", "_", ctx["nombre"]).strip("_")
    carpeta.mkdir(parents=True, exist_ok=True)

    if args.parametros:
        q = json.loads(args.parametros)
        ctx["hip"].update(q.get("hipotesis") or {})
        ctx["economia"].update({k: v for k, v in (q.get("economia") or {}).items() if v is not None})
        if "separacion_edificios_m" in q:
            ctx["comun"]["separacion_edificios_m"] = q["separacion_edificios_m"]
        r = variante(ctx, float(q["ang"]), float(q["pct"]), q.get("uni_en", "abajo"), q.get("remate", "fondo_saco"),
                     bool(q.get("acera", False)))
        r["id"] = "VISOR"
        exportar_dxf(r, ctx, carpeta / "visor.dxf")
        (carpeta / "visor.svg").write_text(svg_variante(r, ctx), encoding="utf-8")
        print(json.dumps(publico(r), ensure_ascii=False, indent=2))
        print(f"DXF: {carpeta / 'visor.dxf'} · SVG: {carpeta / 'visor.svg'}")
        print("PENDIENTE DE VALIDAR POR EL ARQUITECTO")
        return 0

    rs = barrer(ctx, args.objetivo)
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

    escribir_csv(rs, carpeta / "ranking.csv")
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
