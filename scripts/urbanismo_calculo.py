#!/usr/bin/env python3
"""
Cálculo urbanístico básico con reglas fijas (sin IA).

Calcula, a partir de los parámetros de la ficha urbanística:
  - Techo máximo edificable  = superficie de parcela × edificabilidad (m²/m²)
  - Huella máxima (ocupación) = superficie de parcela × ocupación (%) / 100
  - Techo por ocupación      = huella máxima × nº de plantas
  - Techo máximo efectivo    = mínimo de los dos anteriores (parámetro limitante)

Uso:
  python3 scripts/urbanismo_calculo.py --parcela 500 --edificabilidad 1.2 --ocupacion 60 --plantas 3
  python3 scripts/urbanismo_calculo.py --parcela 500 --edificabilidad 1.2 --ocupacion 60 --plantas 3 --json

Nota: no considera retranqueos, fondo edificable ni superficies no computables;
esos ajustes los justifica el agente de urbanismo en fases/01_urbanismo.md.
"""

import argparse
import json
import sys


def calcular(parcela: float, edificabilidad: float, ocupacion: float, plantas: int) -> dict:
    if parcela <= 0:
        raise ValueError("La superficie de parcela debe ser mayor que 0.")
    if edificabilidad < 0:
        raise ValueError("La edificabilidad no puede ser negativa.")
    if not 0 <= ocupacion <= 100:
        raise ValueError("La ocupación debe estar entre 0 y 100 %.")
    if plantas < 1:
        raise ValueError("El número de plantas debe ser al menos 1.")

    techo_por_edificabilidad = parcela * edificabilidad
    huella_maxima = parcela * ocupacion / 100.0
    techo_por_ocupacion = huella_maxima * plantas
    techo_maximo = min(techo_por_edificabilidad, techo_por_ocupacion)
    limitante = (
        "edificabilidad"
        if techo_por_edificabilidad <= techo_por_ocupacion
        else "ocupación × plantas"
    )

    return {
        "entrada": {
            "superficie_parcela_m2": parcela,
            "edificabilidad_m2_m2": edificabilidad,
            "ocupacion_pct": ocupacion,
            "plantas": plantas,
        },
        "resultado": {
            "huella_maxima_m2": round(huella_maxima, 2),
            "techo_por_edificabilidad_m2": round(techo_por_edificabilidad, 2),
            "techo_por_ocupacion_m2": round(techo_por_ocupacion, 2),
            "techo_maximo_m2": round(techo_maximo, 2),
            "parametro_limitante": limitante,
        },
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Techo y huella máximos de una parcela (sin IA).")
    p.add_argument("--parcela", type=float, required=True, help="Superficie de parcela (m²)")
    p.add_argument("--edificabilidad", type=float, required=True, help="Edificabilidad (m²/m²)")
    p.add_argument("--ocupacion", type=float, required=True, help="Ocupación máxima (%%)")
    p.add_argument("--plantas", type=int, required=True, help="Número máximo de plantas")
    p.add_argument("--json", action="store_true", help="Salida en formato JSON")
    args = p.parse_args(argv)

    try:
        r = calcular(args.parcela, args.edificabilidad, args.ocupacion, args.plantas)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    e, s = r["entrada"], r["resultado"]
    print("CÁLCULO URBANÍSTICO (reglas fijas, sin IA)")
    print(f"  Superficie de parcela ........ {e['superficie_parcela_m2']:>10.2f} m²")
    print(f"  Edificabilidad ............... {e['edificabilidad_m2_m2']:>10.3f} m²/m²")
    print(f"  Ocupación máxima ............. {e['ocupacion_pct']:>10.2f} %")
    print(f"  Nº de plantas ................ {e['plantas']:>10d}")
    print("  ---------------------------------------------")
    print(f"  Huella máxima ................ {s['huella_maxima_m2']:>10.2f} m²")
    print(f"  Techo por edificabilidad ..... {s['techo_por_edificabilidad_m2']:>10.2f} m²")
    print(f"  Techo por ocupación×plantas .. {s['techo_por_ocupacion_m2']:>10.2f} m²")
    print(f"  TECHO MÁXIMO ................. {s['techo_maximo_m2']:>10.2f} m²")
    print(f"  Parámetro limitante .......... {s['parametro_limitante']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
