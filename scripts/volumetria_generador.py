#!/usr/bin/env python3
"""
Generador de volumetrías con reglas fijas (sin IA) — herramienta interna.

A partir de la geometría de la parcela y de los parámetros de la ficha
urbanística, genera una volumetría por tipología y calcula huella, plantas,
techo, aprovechamiento y viviendas estimadas. Exporta cada opción a DXF
(planta 2D + volumen 3D por espesor) en planos/volumetrias/.

Tipologías:
  entre_medianeras     Banda de fondo edificable desde las fachadas indicadas.
  manzana_cerrada      Banda de fondo edificable desde TODOS los lados (manzana
                       completa) con patio de manzana central.
  bloque_abierto       Bloques lineales paralelos dentro de la zona de
                       retranqueos, con separación mínima entre bloques.
  torre                Bloques en punto (planta cuadrada) en retícula.
  unifamiliar_aislada  Una vivienda dentro de la zona de retranqueos.
  unifamiliar_adosada  Hileras de viviendas paralelas a la fachada principal.

Principios (CLAUDE.md §7):
  - Los parámetros URBANÍSTICOS no tienen valor por defecto. Si falta uno que
    la tipología necesita, la tipología se marca como FALTA DATO y no se genera.
  - Los parámetros de DISEÑO (fondo de bloque, altura de planta, superficie de
    vivienda…) son HIPÓTESIS: tienen valor por defecto, se pueden cambiar en el
    archivo de entrada y siempre se listan en la salida.

Uso:
  python3 scripts/volumetria_generador.py datos/volumetria.json
  python3 scripts/volumetria_generador.py datos/volumetria.json --lados
  python3 scripts/volumetria_generador.py datos/volumetria.json --json --sin-dxf

  --lados    Lista los lados de la parcela (índice, longitud, orientación) para
             decidir cuáles son fachada.

Superficies computables y ático (opcional, ver LEEME_volumetria.md):
  urbanismo.atico          {"permitido", "retranqueo_m", "computa"}   (de la ficha)
  urbanismo.computo        {"concepto": coeficiente 0..1}             (de la normativa)
  urbanismo.viviendas_max  nº máximo de viviendas                      (de la ficha)
  hipotesis.no_computables {"concepto": % de la sup. construida}      (de diseño)

Formato de entrada (JSON): ver scripts/ejemplos/ejemplo_ficticio.json.
Dependencias: shapely, ezdxf (ver scripts/requirements.txt).
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString, MultiPolygon, Polygon, box
from shapely.ops import unary_union
from shapely.prepared import prep

sys.path.insert(0, str(Path(__file__).resolve().parent))
from urbanismo_calculo import calcular  # noqa: E402

TIPOLOGIAS = [
    "entre_medianeras",
    "manzana_cerrada",
    "bloque_abierto",
    "torre",
    "unifamiliar_aislada",
    "unifamiliar_adosada",
]

# Parámetros urbanísticos que necesita cada tipología (además de los comunes).
COMUNES = ["edificabilidad_m2m2", "ocupacion_pct", "plantas_max"]
REQUISITOS = {
    "entre_medianeras": ["fondo_edificable_m", "retranqueo_fachada_m"],
    "manzana_cerrada": ["fondo_edificable_m", "retranqueo_fachada_m"],
    "bloque_abierto": ["retranqueo_fachada_m", "retranqueo_linderos_m", "separacion_edificios_m"],
    "torre": ["retranqueo_fachada_m", "retranqueo_linderos_m", "separacion_edificios_m"],
    "unifamiliar_aislada": ["retranqueo_fachada_m", "retranqueo_linderos_m"],
    "unifamiliar_adosada": ["retranqueo_fachada_m", "retranqueo_linderos_m", "separacion_edificios_m"],
}
NECESITA_FACHADAS = {"entre_medianeras", "unifamiliar_adosada"}

# Hipótesis de diseño (no urbanísticas). Se declaran siempre en la salida.
HIPOTESIS_DEFECTO = {
    "altura_planta_m": 3.0,            # suelo a suelo, residencial
    "fondo_bloque_m": 12.0,            # bloque lineal de doble crujía
    "longitud_min_bloque_m": 15.0,     # tramo mínimo útil de bloque
    "lado_torre_m": 20.0,              # planta cuadrada del bloque en punto
    "fondo_adosada_m": 10.0,
    "ancho_adosada_m": 6.0,            # fachada por vivienda adosada
    "plantas_unifamiliar": 2,
    "sup_construida_vivienda_m2": 100.0,
    "paso_rejilla_m": 0.5,             # resolución de búsqueda geométrica
    "paso_angulo_grados": 5,           # orientaciones probadas para bloques
}

FALTA = "FALTA DATO"


# --------------------------------------------------------------------------- #
# Entrada
# --------------------------------------------------------------------------- #
def leer_gml(ruta: Path) -> list:
    """Lee el contorno exterior de una parcela en GML (INSPIRE / Catastro)."""
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<gml:exterior>.*?<gml:posList[^>]*>(.*?)</gml:posList>", texto, re.S)
    if not m:
        m = re.search(r"<gml:posList[^>]*>(.*?)</gml:posList>", texto, re.S)
    if not m:
        raise ValueError(f"No encuentro gml:posList en {ruta}")
    nums = [float(v) for v in m.group(1).split()]
    pts = [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    return pts


def cargar(ruta: Path) -> dict:
    cfg = json.loads(ruta.read_text(encoding="utf-8"))
    par = cfg.get("parcela") or {}
    if "coordenadas" in par:
        pts = [tuple(p) for p in par["coordenadas"]]
    elif "gml" in par:
        gml = Path(par["gml"])
        if not gml.is_absolute():
            gml = (ruta.parent / gml) if (ruta.parent / gml).exists() else gml
        pts = leer_gml(gml)
    else:
        raise ValueError("La parcela necesita 'coordenadas' o 'gml'.")
    poly = Polygon(pts)
    if not poly.is_valid or poly.area <= 0:
        raise ValueError("La geometría de la parcela no es un polígono válido.")
    # Se respeta el orden de vértices de la entrada (lado i = vértice i → i+1),
    # sea horario o antihorario, para que los índices coincidan con la ficha.
    cfg["_pts"] = pts
    cfg["_poly"] = poly
    cfg["_ccw"] = poly.exterior.is_ccw
    # Superficie de cálculo: la oficial de la ficha si existe; si no, la del polígono.
    oficial = par.get("superficie_oficial_m2")
    cfg["_sup"] = float(oficial) if oficial else poly.area
    if oficial:
        dif = 100 * (poly.area - oficial) / oficial
        if abs(dif) > 1:
            cfg["_aviso_sup"] = (f"El polígono mide {poly.area:.2f} m² y la superficie oficial {oficial:.2f} m² "
                                 f"({dif:+.1f} %). Los parámetros se calculan sobre la oficial; la geometría, "
                                 f"sobre el polígono.")
    hip = dict(HIPOTESIS_DEFECTO)
    hip.update(cfg.get("hipotesis") or {})
    cfg["_hip"] = hip
    cfg["_urb"] = {k: v for k, v in (cfg.get("urbanismo") or {}).items() if v is not None}
    return cfg


def lados(pts: list, ccw: bool = True) -> list:
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        # Normal exterior: (dy, -dx) si el polígono es antihorario; opuesta si es horario.
        nx, ny = (dy, -dx) if ccw else (-dy, dx)
        rumbo = (math.degrees(math.atan2(nx, ny)) + 360) % 360  # 0 = norte, 90 = este
        out.append({
            "indice": i,
            "longitud_m": round(math.hypot(dx, dy), 2),
            "mira_a": _rumbo_txt(rumbo),
            "rumbo_normal_grados": round(rumbo, 1),
            "_seg": LineString([a, b]),
            "_angulo": math.degrees(math.atan2(dy, dx)),
        })
    return out


def _rumbo_txt(r: float) -> str:
    nombres = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return nombres[int(((r + 22.5) % 360) // 45)]


# --------------------------------------------------------------------------- #
# Geometría
# --------------------------------------------------------------------------- #
def zona_retranqueos(poly, ls, fachadas, r_fachada, r_linderos):
    """Parcela menos la franja de retranqueo de cada lado (distancia mínima)."""
    franjas = []
    for l in ls:
        r = r_fachada if l["indice"] in fachadas else r_linderos
        if r > 0:
            franjas.append(l["_seg"].buffer(r))
    if not franjas:
        return poly
    return _limpia(poly.difference(unary_union(franjas)))


def banda_fondo(poly, ls, fachadas, fondo, r_fachada):
    """Franja entre el retranqueo de fachada y el fondo edificable."""
    segs = [l["_seg"] for l in ls if l["indice"] in fachadas]
    exterior = unary_union([s.buffer(fondo, cap_style="flat", join_style="mitre") for s in segs])
    zona = poly.intersection(exterior)
    if r_fachada > 0:
        zona = zona.difference(unary_union([s.buffer(r_fachada) for s in segs]))
    return _limpia(zona)


def _limpia(g):
    g = g.buffer(0)
    if g.is_empty:
        return g
    if isinstance(g, MultiPolygon):
        g = MultiPolygon([p for p in g.geoms if p.area > 1.0])
    elif not isinstance(g, Polygon):
        polys = [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon) and p.area > 1.0]
        g = MultiPolygon(polys) if polys else Polygon()
    return g


def ajusta_por_bisección(constructor, lo, hi, area_max, iteraciones=40):
    """Busca el mayor parámetro t en [lo, hi] con area(constructor(t)) <= area_max."""
    g = constructor(hi)
    if g.area <= area_max:
        return g, hi
    for _ in range(iteraciones):
        mid = (lo + hi) / 2
        if constructor(mid).area <= area_max:
            lo = mid
        else:
            hi = mid
    return constructor(lo), lo


def bloques_lineales(zona, angulo, fondo, separacion, l_min, l_max, paso, fases=4):
    """Bloques rectangulares paralelos (dirección `angulo`) totalmente dentro de `zona`.

    Devuelve la mejor colocación (más superficie) probando varios desfases.
    """
    if zona.is_empty:
        return []
    c = zona.centroid
    zr = affinity.rotate(zona, -angulo, origin=c)
    pz = prep(zr)
    minx, miny, maxx, maxy = zr.bounds
    mejor, mejor_area = [], 0.0
    modulo = fondo + separacion
    for f in range(fases):
        y = miny + modulo * f / fases
        rects = []
        while y + fondo <= maxy + 1e-9:
            rects += _tramos_en_franja(pz, minx, maxx, y, fondo, separacion, l_min, l_max, paso)
            y += modulo
        area = sum(r.area for r in rects)
        if area > mejor_area:
            mejor, mejor_area = rects, area
    return [affinity.rotate(r, angulo, origin=c) for r in mejor]


def _tramos_en_franja(pz, minx, maxx, y, fondo, separacion, l_min, l_max, paso):
    n = int(math.ceil((maxx - minx) / paso))
    dentro = [pz.contains(box(minx + i * paso, y, minx + (i + 1) * paso, y + fondo)) for i in range(n)]
    tramos, i = [], 0
    while i < n:
        if dentro[i]:
            j = i
            while j < n and dentro[j]:
                j += 1
            tramos.append([minx + i * paso, minx + j * paso])
            i = j
        else:
            i += 1
    # Separación mínima entre tramos de la misma franja: si no se cumple,
    # se recorta el inicio del tramo siguiente.
    ok = []
    for a, b in tramos:
        if ok and a - ok[-1][1] < separacion:
            a = ok[-1][1] + separacion
        if b - a >= l_min:
            ok.append([a, b])
    rects = []
    for a, b in ok:
        if l_max:
            # Partir en tramos <= l_max separados por `separacion`.
            while b - a > l_max:
                rects.append(box(a, y, a + l_max, y + fondo))
                a += l_max + separacion
            if b - a >= l_min:
                rects.append(box(a, y, b, y + fondo))
        else:
            rects.append(box(a, y, b, y + fondo))
    return rects


def torres(zona, angulo, lado, separacion, fases=4):
    if zona.is_empty:
        return []
    c = zona.centroid
    zr = affinity.rotate(zona, -angulo, origin=c)
    pz = prep(zr)
    minx, miny, maxx, maxy = zr.bounds
    modulo = lado + separacion
    mejor = []
    for fx in range(fases):
        for fy in range(fases):
            sel = []
            y = miny + modulo * fy / fases
            while y + lado <= maxy:
                x = minx + modulo * fx / fases
                while x + lado <= maxx:
                    b = box(x, y, x + lado, y + lado)
                    if pz.contains(b):
                        sel.append(b)
                    x += modulo
                y += modulo
            if len(sel) > len(mejor):
                mejor = sel
    return [affinity.rotate(b, angulo, origin=c) for b in mejor]


def angulos_candidatos(ls, paso):
    angs = set(range(0, 180, int(paso)))
    for l in ls:
        angs.add(round(l["_angulo"] % 180, 2))
    return sorted(angs)


def recorta_a_ocupacion(piezas, area_max):
    """Quita piezas (de menor a mayor) hasta cumplir la ocupación máxima."""
    piezas = sorted(piezas, key=lambda p: p.area, reverse=True)
    while piezas and sum(p.area for p in piezas) > area_max + 1e-6:
        piezas.pop()
    return piezas


# --------------------------------------------------------------------------- #
# Tipologías
# --------------------------------------------------------------------------- #
def generar(tip, cfg, ls):
    urb, hip, poly = cfg["_urb"], cfg["_hip"], cfg["_poly"]
    fachadas = set(cfg.get("fachadas") or [])
    faltan = [k for k in COMUNES + REQUISITOS[tip] if k not in urb]
    if tip in NECESITA_FACHADAS and not fachadas:
        faltan.append("fachadas (índices de lado)")
    if faltan:
        return {"tipologia": tip, "estado": FALTA, "faltan": faltan}

    sup = cfg["_sup"]
    base = calcular(sup, urb["edificabilidad_m2m2"], urb["ocupacion_pct"], int(urb["plantas_max"]))["resultado"]
    huella_max = base["huella_maxima_m2"]
    techo_max = base["techo_por_edificabilidad_m2"]

    plantas = int(urb["plantas_max"])
    notas = []
    if "altura_max_m" in urb:
        por_altura = int(math.floor(urb["altura_max_m"] / hip["altura_planta_m"] + 1e-9))
        if por_altura < plantas:
            notas.append(f"Altura máxima {urb['altura_max_m']} m limita a {por_altura} plantas "
                         f"(hipótesis altura de planta {hip['altura_planta_m']} m).")
        plantas = min(plantas, por_altura)
    else:
        notas.append("Sin altura máxima en metros: solo se aplica el nº máximo de plantas.")
    if tip.startswith("unifamiliar"):
        plantas = min(plantas, int(hip["plantas_unifamiliar"]))

    zona_ref = None
    piezas, extra = [], {}
    if tip in ("entre_medianeras", "manzana_cerrada"):
        fach = fachadas if tip == "entre_medianeras" else {l["indice"] for l in ls}
        fondo = urb["fondo_edificable_m"]
        rf = urb["retranqueo_fachada_m"]
        g, fondo_usado = ajusta_por_bisección(
            lambda t: banda_fondo(poly, ls, fach, t, rf), rf, fondo, huella_max)
        piezas = [g] if not g.is_empty else []
        zona_ref = banda_fondo(poly, ls, fach, fondo, rf)
        extra["fondo_aplicado_m"] = round(fondo_usado, 2)
        if fondo_usado < fondo - 0.01:
            notas.append(f"La ocupación máxima obliga a reducir el fondo de {fondo} a {fondo_usado:.2f} m.")
        if tip == "manzana_cerrada":
            notas.append("Se considera la parcela como manzana completa: todos los lados son alineación.")
    elif tip == "unifamiliar_aislada":
        zona = zona_retranqueos(poly, ls, fachadas, urb["retranqueo_fachada_m"], urb["retranqueo_linderos_m"])
        zona_ref = zona
        if zona.is_empty:
            piezas = []
        else:
            r_lim = math.sqrt(zona.area)
            g, d = ajusta_por_bisección(lambda t: _limpia(zona.buffer(-(r_lim - t), join_style="mitre")),
                                        0.0, r_lim, huella_max)
            piezas = [g] if not g.is_empty else []
            if r_lim - d > 0.01:
                notas.append("La huella se ha reducido desde la zona de retranqueos para cumplir la ocupación.")
        extra["viviendas"] = 1 if piezas else 0
    else:
        zona = zona_retranqueos(poly, ls, fachadas, urb["retranqueo_fachada_m"], urb["retranqueo_linderos_m"])
        zona_ref = zona
        sep = urb["separacion_edificios_m"]
        if tip == "torre":
            angs = angulos_candidatos(ls, hip["paso_angulo_grados"])
            cand = [(a, recorta_a_ocupacion(torres(zona, a, hip["lado_torre_m"], sep), huella_max)) for a in angs]
        else:
            if tip == "bloque_abierto":
                fondo_b, lmin, lmax = hip["fondo_bloque_m"], hip["longitud_min_bloque_m"], urb.get("longitud_max_bloque_m")
                angs = angulos_candidatos(ls, hip["paso_angulo_grados"])
            else:  # adosadas: paralelas a la fachada más larga
                fondo_b, lmin, lmax = hip["fondo_adosada_m"], 2 * hip["ancho_adosada_m"], urb.get("longitud_max_bloque_m")
                principal = max((l for l in ls if l["indice"] in fachadas), key=lambda l: l["longitud_m"])
                angs = [principal["_angulo"]]
            cand = [(a, recorta_a_ocupacion(
                bloques_lineales(zona, a, fondo_b, sep, lmin, lmax, hip["paso_rejilla_m"]), huella_max))
                for a in angs]
        # Mejor orientación: más techo materializable; a igualdad, menos huella.
        def clave(item):
            h = sum(p.area for p in item[1])
            return (round(min(h * plantas, techo_max), 1), -h)
        ang, piezas = max(cand, key=clave) if cand else (0, [])
        extra["orientacion_bloques_grados"] = round(ang % 180, 1)
        extra["n_edificios"] = len(piezas)
        if tip == "unifamiliar_adosada":
            ancho = hip["ancho_adosada_m"]
            extra["viviendas"] = sum(int(_largo(p) // ancho) for p in piezas)

    huella = sum(p.area for p in piezas)
    if huella <= 0:
        return {"tipologia": tip, "estado": "NO CABE",
                "motivo": "Con estos parámetros no cabe ningún edificio de esta tipología.",
                "_zona": zona_ref, "_piezas": []}

    # --- Ático (solo si la ficha lo regula) ------------------------------- #
    fach_atico = (fachadas if tip == "entre_medianeras"
                  else {l["indice"] for l in ls} if tip == "manzana_cerrada" else None)
    at = atico(piezas, ls, fach_atico, urb, plantas, hip, notas)
    sup_atico = sum(p.area for p in at["piezas"])

    # --- Cómputo de superficies ------------------------------------------ #
    sup_plantas = huella * plantas
    construida_geo = sup_plantas + sup_atico
    factor, desglose = factor_computo(urb, hip, notas)
    computable_geo = sup_plantas * factor + (sup_atico * factor if at["computa"] else 0.0)
    # Si lo computable supera la edificabilidad, se reduce la construida en proporción.
    escala = min(1.0, techo_max / computable_geo) if computable_geo > 0 else 0.0
    construida = construida_geo * escala
    computable = computable_geo * escala
    if escala < 1.0 - 1e-6:
        sobra = construida_geo - construida
        notas.append(f"La superficie computable geométrica ({computable_geo:.0f} m²) supera la "
                     f"edificabilidad ({techo_max:.0f} m²): sobran {sobra:.0f} m² construidos "
                     f"(reducir ático, plantas o fondo).")

    # --- Viviendas -------------------------------------------------------- #
    viviendas = extra.pop("viviendas", None)
    if viviendas is None:
        viviendas = int(construida // hip["sup_construida_vivienda_m2"])
        criterio = (f"sup. construida / {hip['sup_construida_vivienda_m2']} m² construidos "
                    f"por vivienda (hipótesis)")
    else:
        criterio = "por unidades de parcela" if tip == "unifamiliar_aislada" else \
            f"longitud de hilera / {hip['ancho_adosada_m']} m (hipótesis)"
    if "viviendas_max" in urb and viviendas > urb["viviendas_max"]:
        notas.append(f"Viviendas limitadas por la ficha: {viviendas} → {int(urb['viviendas_max'])}.")
        viviendas = int(urb["viviendas_max"])

    return {
        "tipologia": tip,
        "estado": "OK",
        "huella_m2": round(huella, 2),
        "ocupacion_pct": round(100 * huella / sup, 2),
        "plantas": plantas,
        "atico_m2": round(sup_atico, 2),
        "sup_construida_geometrica_m2": round(construida_geo, 2),
        "sup_construida_materializable_m2": round(construida, 2),
        "sup_computable_m2": round(computable, 2),
        "sup_no_computable_m2": round(construida - computable, 2),
        "factor_computo": round(factor, 4),
        "desglose_no_computables": desglose,
        # Compatibilidad: 'techo' = superficie computable (la que consume edificabilidad).
        "techo_materializable_m2": round(computable, 2),
        "aprovechamiento_pct": round(100 * computable / techo_max, 1) if techo_max else 0,
        "viviendas_estimadas": viviendas,
        "criterio_viviendas": criterio,
        **extra,
        "notas": notas,
        "_zona": zona_ref,
        "_piezas": piezas,
        "_atico": at["piezas"],
        "_altura_m": plantas * hip["altura_planta_m"],
    }


def atico(piezas, ls, fachadas, urb, plantas, hip, notas):
    """Planta ático retranqueada sobre la última planta, si la ficha la regula.

    urbanismo.atico = {"permitido": bool, "retranqueo_m": float, "computa": bool}
    Retranqueo desde las fachadas a vía pública (medianeras / manzana) o desde
    todo el perímetro del edificio (resto de tipologías).
    """
    cfg = urb.get("atico")
    if cfg is None:
        notas.append("Ático: no regulado en la entrada (no se genera). Si la ficha lo permite, añada 'atico'.")
        return {"piezas": [], "computa": True}
    if not cfg.get("permitido", False):
        return {"piezas": [], "computa": True}
    faltan = [k for k in ("retranqueo_m", "computa") if cfg.get(k) is None]
    if faltan:
        notas.append(f"Ático: {FALTA} ({', '.join('atico.' + k for k in faltan)}); no se genera.")
        return {"piezas": [], "computa": True}
    r = float(cfg["retranqueo_m"])
    if "altura_max_m" in urb and (plantas + 1) * hip["altura_planta_m"] > urb["altura_max_m"] + 1e-9:
        notas.append("Ático: con la hipótesis de altura de planta supera la altura máxima en metros; "
                     "compruebe cómo mide la ficha la altura del ático.")
    res = []
    for p in piezas:
        if fachadas is not None:
            rf = urb.get("retranqueo_fachada_m", 0) or 0
            corte = unary_union([l["_seg"].buffer(rf + r) for l in ls if l["indice"] in fachadas])
            g = _limpia(p.difference(corte))
        else:
            g = _limpia(p.buffer(-r, join_style="mitre"))
        res += _polys(g)
    return {"piezas": res, "computa": bool(cfg["computa"])}


def factor_computo(urb, hip, notas):
    """Fracción computable de la superficie construida sobre rasante.

    hipotesis.no_computables = {"concepto": % de la sup. construida}   (diseño)
    urbanismo.computo        = {"concepto": coeficiente 0..1}         (normativa)
    factor = 1 - Σ %_i · (1 - coef_i). Un concepto sin coeficiente en la
    normativa se computa al 100 % (del lado de la seguridad) y se marca FALTA DATO.
    """
    elementos = hip.get("no_computables") or {}
    coefs = urb.get("computo") or {}
    factor, desglose = 1.0, []
    for nombre, pct in elementos.items():
        c = coefs.get(nombre)
        if c is None:
            notas.append(f"Cómputo de '{nombre}': {FALTA} (coeficiente de la normativa); se computa al 100 %.")
            c = 1.0
        factor -= (pct / 100.0) * (1.0 - c)
        desglose.append({"concepto": nombre, "pct_sup_construida": pct, "coef_computo": c})
    if factor <= 0:
        raise ValueError("El factor de cómputo resulta <= 0: revise 'no_computables' y 'computo'.")
    return factor, desglose


def _largo(p):
    r = p.minimum_rotated_rectangle
    xs = list(r.exterior.coords)
    d = [math.dist(xs[i], xs[i + 1]) for i in range(4)]
    return max(d)


# --------------------------------------------------------------------------- #
# Salida
# --------------------------------------------------------------------------- #
def exportar_dxf(cfg, res, carpeta: Path):
    import ezdxf
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = re.sub(r"[^\w-]+", "_", cfg.get("nombre", "parcela")).strip("_")
    ruta = carpeta / f"{nombre}_{res['tipologia']}.dxf"
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.M
    for capa, color in [("PARCELA", 7), ("ZONA_EDIFICABLE", 3), ("HUELLA", 1), ("ATICO", 6), ("VOLUMEN_3D", 5), ("TEXTO", 2)]:
        doc.layers.add(capa, color=color)
    msp = doc.modelspace()
    msp.add_lwpolyline(cfg["_pts"], close=True, dxfattribs={"layer": "PARCELA"})
    for g in _polys(res.get("_zona")):
        msp.add_lwpolyline(list(g.exterior.coords), close=True, dxfattribs={"layer": "ZONA_EDIFICABLE", "linetype": "DASHED"})
    h = res["_altura_m"]
    for g in res["_piezas"]:
        for p in _polys(g):
            coords = list(p.exterior.coords)
            msp.add_lwpolyline(coords, close=True, dxfattribs={"layer": "HUELLA"})
            msp.add_lwpolyline(coords, close=True, dxfattribs={"layer": "VOLUMEN_3D", "thickness": h})
            for hueco in p.interiors:
                msp.add_lwpolyline(list(hueco.coords), close=True, dxfattribs={"layer": "HUELLA"})
                msp.add_lwpolyline(list(hueco.coords), close=True, dxfattribs={"layer": "VOLUMEN_3D", "thickness": h})
    hp = cfg["_hip"]["altura_planta_m"]
    for p in res.get("_atico", []):
        coords = list(p.exterior.coords)
        msp.add_lwpolyline(coords, close=True, dxfattribs={"layer": "ATICO", "elevation": h})
        msp.add_lwpolyline(coords, close=True, dxfattribs={"layer": "VOLUMEN_3D", "elevation": h, "thickness": hp})
    minx, miny, maxx, maxy = cfg["_poly"].bounds
    lineas = [
        f"{cfg.get('nombre', '')} - {res['tipologia']}",
        f"Huella {res['huella_m2']} m2 ({res['ocupacion_pct']} %) - {res['plantas']} plantas",
        f"Atico {res['atico_m2']} m2 - Construida {res['sup_construida_materializable_m2']} m2 - "
        f"Computable {res['sup_computable_m2']} m2 - {res['viviendas_estimadas']} viv. (estimadas)",
        "Generado con reglas fijas (sin IA). PENDIENTE DE VALIDAR POR EL ARQUITECTO",
    ]
    alto = max(0.5, (maxx - minx) / 60)
    for i, t in enumerate(lineas):
        msp.add_text(t, height=alto, dxfattribs={"layer": "TEXTO"}).set_placement((minx, miny - (i + 2) * alto * 1.8))
    doc.saveas(ruta)
    return ruta


def _polys(g):
    if g is None or g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    return [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]


def publico(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def imprimir(cfg, resultados, hip_usadas):
    print("GENERADOR DE VOLUMETRÍAS (reglas fijas, sin IA)")
    print(f"  Parcela: {cfg.get('nombre', '')} — superficie de cálculo {cfg['_sup']:.2f} m² "
          f"(polígono {cfg['_poly'].area:.2f} m²)")
    if cfg.get("_aviso_sup"):
        print(f"  AVISO: {cfg['_aviso_sup']}")
    print()
    cab = (f"  {'Tipología':<22}{'Estado':<12}{'Huella m²':>11}{'Ocup.%':>8}{'Pl.':>5}{'Ático m²':>10}"
           f"{'Constr. m²':>12}{'Comput. m²':>12}{'Aprov.%':>9}{'Viv.':>6}")
    print(cab)
    print("  " + "-" * (len(cab) - 2))
    for r in resultados:
        if r["estado"] == "OK":
            print(f"  {r['tipologia']:<22}{'OK':<12}{r['huella_m2']:>11.1f}{r['ocupacion_pct']:>8.1f}"
                  f"{r['plantas']:>5d}{r['atico_m2']:>10.1f}{r['sup_construida_materializable_m2']:>12.1f}"
                  f"{r['sup_computable_m2']:>12.1f}{r['aprovechamiento_pct']:>9.1f}"
                  f"{r['viviendas_estimadas']:>6d}")
        else:
            print(f"  {r['tipologia']:<22}{r['estado']:<12}")
    print()
    for r in resultados:
        if r["estado"] == FALTA:
            print(f"  · {r['tipologia']}: {FALTA} → {', '.join(r['faltan'])}")
        elif r["estado"] != "OK":
            print(f"  · {r['tipologia']}: {r['motivo']}")
        else:
            for n in r["notas"]:
                print(f"  · {r['tipologia']}: {n}")
            if r.get("dxf"):
                print(f"  · {r['tipologia']}: DXF → {r['dxf']}")
    print()
    print("  Hipótesis de diseño usadas (modificables en 'hipotesis'):")
    for k, v in hip_usadas.items():
        print(f"    - {k} = {v}")
    print()
    print("PENDIENTE DE VALIDAR POR EL ARQUITECTO")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Volumetrías por tipología con reglas fijas (sin IA).")
    p.add_argument("entrada", type=Path, help="Archivo JSON de entrada")
    p.add_argument("--lados", action="store_true", help="Listar los lados de la parcela y salir")
    p.add_argument("--json", action="store_true", help="Salida en JSON")
    p.add_argument("--sin-dxf", action="store_true", help="No exportar DXF")
    p.add_argument("--salida", type=Path, default=Path("planos/volumetrias"), help="Carpeta de DXF")
    args = p.parse_args(argv)

    try:
        cfg = cargar(args.entrada)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    ls = lados(cfg["_pts"], cfg["_ccw"])

    if args.lados:
        print(f"Lados de la parcela (superficie {cfg['_poly'].area:.2f} m²):")
        if cfg.get("_aviso_sup"):
            print(f"  AVISO: {cfg['_aviso_sup']}")
        for l in ls:
            print(f"  lado {l['indice']:>2}: {l['longitud_m']:>8.2f} m, mira a {l['mira_a']:<2} "
                  f"({l['rumbo_normal_grados']}°)")
        return 0

    pedidas = cfg.get("tipologias") or TIPOLOGIAS
    desconocidas = [t for t in pedidas if t not in TIPOLOGIAS]
    if desconocidas:
        print(f"Error: tipologías desconocidas {desconocidas}. Válidas: {TIPOLOGIAS}", file=sys.stderr)
        return 1
    resultados = [generar(t, cfg, ls) for t in pedidas]
    if not args.sin_dxf:
        for r in resultados:
            if r["estado"] == "OK":
                r["dxf"] = str(exportar_dxf(cfg, r, args.salida))

    if args.json:
        print(json.dumps({
            "parcela": {"nombre": cfg.get("nombre"), "superficie_calculo_m2": round(cfg["_sup"], 2),
                        "superficie_poligono_m2": round(cfg["_poly"].area, 2)},
            "lados": [{k: v for k, v in l.items() if not k.startswith("_")} for l in ls],
            "hipotesis": cfg["_hip"],
            "resultados": [publico(r) for r in resultados],
            "aviso": "PENDIENTE DE VALIDAR POR EL ARQUITECTO",
        }, ensure_ascii=False, indent=2))
    else:
        imprimir(cfg, resultados, cfg["_hip"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
