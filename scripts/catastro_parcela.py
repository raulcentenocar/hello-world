#!/usr/bin/env python3
"""
Descarga la geometría de una parcela del Catastro (servicio INSPIRE, sin IA).

Guarda el GML oficial (coordenadas ETRS89 / UTM 30N, EPSG:25830, válido para
Madrid) y muestra la superficie gráfica calculada a partir del contorno.

Uso:
  python3 scripts/catastro_parcela.py 9872023VH5797S
  python3 scripts/catastro_parcela.py 9872023VH5797S --salida datos/parcela.gml

Después, en el JSON de volumetría:
  "parcela": {"gml": "parcela.gml"}

La referencia catastral de parcela son los 14 primeros caracteres.
Nota: la superficie gráfica del Catastro puede no coincidir con la registral ni
con la de un levantamiento topográfico; manda el dato que figure en datos/.
"""

import argparse
import sys
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx"


def descargar(refcat: str, srs: str = "EPSG::25830") -> str:
    refcat = refcat.strip().upper()[:14]
    if len(refcat) != 14:
        raise ValueError("La referencia catastral de parcela debe tener 14 caracteres.")
    q = urllib.parse.urlencode({
        "service": "wfs", "version": "2", "request": "getfeature",
        "STOREDQUERIE_ID": "GetParcel", "refcat": refcat, "srsname": srs,
    })
    with urllib.request.urlopen(f"{URL}?{q}", timeout=30) as r:
        texto = r.read().decode("utf-8", errors="replace")
    if "posList" not in texto:
        raise ValueError("El Catastro no ha devuelto geometría para esa referencia:\n" + texto[:500])
    return texto


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Descarga la parcela catastral en GML.")
    p.add_argument("refcat", help="Referencia catastral (14 o 20 caracteres)")
    p.add_argument("--salida", type=Path, default=None, help="Ruta del GML (por defecto datos/<refcat>.gml)")
    args = p.parse_args(argv)
    try:
        texto = descargar(args.refcat)
    except Exception as e:  # red, HTTP o respuesta sin geometría
        print(f"Error: {e}", file=sys.stderr)
        return 1
    salida = args.salida or Path("datos") / f"{args.refcat.strip().upper()[:14]}.gml"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto, encoding="utf-8")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from shapely.geometry import Polygon
    from volumetria_generador import leer_gml
    pts = leer_gml(salida)
    print(f"GML guardado en {salida}")
    print(f"  Vértices: {len(pts)}  ·  Superficie gráfica: {Polygon(pts).area:.2f} m²")
    return 0


if __name__ == "__main__":
    sys.exit(main())
