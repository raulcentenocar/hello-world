#!/usr/bin/env python3
"""
Comprobacion de los DXF de F4 (V1), reglas fijas, sin IA.

- Abre cada DXF con ezdxf y ejecuta la auditoria.
- Cuenta entidades por capa.
- Comprueba: 24 casas (polilineas cerradas en A-CASA y numeros 1..24 en A-CASA-NUM),
  10 viviendas en el bloque (rotulos "VIVIENDA ..."; "(P1 y P2)" cuenta 2, "(PB)" cuenta 1),
  existencia de la capa CONFLICTOS_F3 con los codigos pedidos, unidades en metros,
  vertices de la parcela en UTM y aviso del cajetin.

Uso (desde la raiz del repositorio):
    python3 scripts/comprobar_dibujo_v1.py
Devuelve codigo 1 si falla alguna comprobacion.
"""
import os
import re
import sys
from collections import Counter

import ezdxf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda f: os.path.join(RAIZ, "planos", f)
AVISO = "PENDIENTE DE VALIDAR POR EL ARQUITECTO"
fallos = []


def check(cond, msg):
    print(("  OK   " if cond else "  FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def abrir(nombre):
    doc = ezdxf.readfile(P(nombre))
    aud = doc.audit()
    msp = doc.modelspace()
    print(f"\n== {nombre} ==")
    print(f"  versión {doc.dxfversion} · $INSUNITS = {doc.header.get('$INSUNITS')} · "
          f"errores de auditoría: {len(aud.errors)} · corregidos: {len(aud.fixes)}")
    cnt = Counter(e.dxf.layer for e in msp)
    for capa in sorted(cnt):
        print(f"  {capa:<22} {cnt[capa]:>5}")
    print(f"  {'TOTAL':<22} {sum(cnt.values()):>5}")
    textos = [e.dxf.text for e in msp.query("TEXT")]
    check(doc.header.get("$INSUNITS") == 6, "unidades en metros ($INSUNITS = 6)")
    check(len(aud.errors) == 0, "auditoría sin errores")
    check(any(AVISO in t for t in textos), "cajetín con el aviso de validación")
    return doc, msp, cnt, textos


# ---------------------------------------------------------------- implantación
doc, msp, cnt, textos = abrir("V1_implantacion.dxf")
casas = [e for e in msp.query('LWPOLYLINE[layer=="A-CASA"]') if e.closed]
check(len(casas) == 24, f"casas dibujadas = {len(casas)} (esperado 24)")
nums = sorted(int(e.dxf.text) for e in msp.query('TEXT[layer=="A-CASA-NUM"]'))
check(nums == list(range(1, 25)), "numeración de casas 1..24")
anchos = Counter()
for e in casas:
    xs = [p[0] for p in e.get_points("xy")]
    ys = [p[1] for p in e.get_points("xy")]
    anchos[(float(round(max(xs) - min(xs), 2)), float(round(max(ys) - min(ys), 2)))] += 1
check(anchos == Counter({(6.5, 12.0): 24}), f"todas las casas de 6,50 × 12,00 m: {dict(anchos)}")
parc = msp.query('LWPOLYLINE[layer=="U-PARCELA"]')[0]
pts = [tuple(round(c, 2) for c in p) for p in parc.get_points("xy")]
esperado = [(414988.78, 4478854.76), (414988.78, 4478782.00), (414896.93, 4478781.24),
            (414865.48, 4478877.90), (414894.46, 4478874.31), (414968.83, 4478858.29)]
check(pts == esperado, "parcela con los 6 vértices UTM de la cédula")
codigos = set(e.dxf.text for e in msp.query('TEXT[layer=="CONFLICTOS_F3"]'))
pedidos = ["N-1", "N-2", "E1", "E3", "E4/I-3/N-4", "E6", "I-8", "I-9", "NC-1", "NC-5"]
for c in pedidos:
    check(c in codigos, f"conflicto {c} marcado en CONFLICTOS_F3")
circ = len(msp.query('CIRCLE[layer=="CONFLICTOS_F3"]'))
print(f"  círculos de conflicto: {circ}")
plazas = len(msp.query('LWPOLYLINE[layer=="U-PLAZA"]'))
pmr = len(msp.query('LWPOLYLINE[layer=="U-PLAZA-ACCESIBLE"]'))
check(plazas == 48 + 21, f"plazas ordinarias = {plazas} (48 a la puerta + 21 en la bolsa)")
print(f"  plaza accesible: {pmr // 2} (plaza + transferencia = {pmr} polilíneas; F2 dibuja 1, NC-5 abierto)")
check(len(msp.query('LWPOLYLINE[layer=="S-PILAR"]')) == 21, "21 pilares en el bloque")
check(len(msp.query('LWPOLYLINE[layer=="U-RETRANQUEO"]')) == 2, "2 líneas de retranqueo (3 y 5 m)")

# ---------------------------------------------------------------- casa tipo
doc, msp, cnt, textos = abrir("V1_casa_tipo.dxf")
pu = [e for e in msp.query('LWPOLYLINE[layer=="I-PATINILLO"]')]
ok = True
for e in pu:
    xs = [p[0] for p in e.get_points("xy")]
    ys = [p[1] for p in e.get_points("xy")]
    ok &= (round(max(xs) - min(xs), 2), round(max(ys) - min(ys), 2)) == (0.8, 0.4)
check(len(pu) == 2 and ok, "patinillo PU 0,80 (E-O) × 0,40 (N-S) en PB y P1")
for t in ["Salón-comedor", "Cocina", "Dormitorio principal", "Dormitorio 2", "Dormitorio 3", "Baño 2"]:
    check(t in textos, f"estancia rotulada: {t}")

# ---------------------------------------------------------------- bloque
doc, msp, cnt, textos = abrir("V1_bloque_planta_tipo.dxf")
n_viv = 0
for t in textos:
    if t.startswith("VIVIENDA "):
        n_viv += 2 if "(P1 y P2)" in t else 1 if "(PB)" in t else 0
check(n_viv == 10, f"viviendas del bloque = {n_viv} (4 tipo × 2 plantas + 2 en PB; esperado 10)")
check(len(msp.query('LWPOLYLINE[layer=="S-PILAR"]')) == 42, "21 pilares en cada una de las 2 plantas dibujadas")
check(len(msp.query('LWPOLYLINE[layer=="I-PATINILLO"]')) == 8, "4 patinillos PB-1..PB-4 en cada planta")

print("\nRESULTADO:", "TODO CORRECTO" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
