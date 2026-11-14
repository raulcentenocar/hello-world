#!/usr/bin/env python3
"""
Prueba de casos de referencia (patrones/casos/*.json) — sin IA.

Para cada caso, genera las variantes de su estrategia sobre su parcela y comprueba
que alguna alcanza las cifras del ejemplo real dentro de la tolerancia del caso.

Uso:
  python3 scripts/prueba_casos.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import variantes_generador as vg  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def probar(ruta: Path) -> bool:
    caso = json.loads(ruta.read_text(encoding="utf-8"))
    ctx = vg.cargar((ruta.parent / caso["entrada"]).resolve())
    ctx["hip"].update(caso.get("hipotesis") or {})
    ctx["barrido"]["estrategias"] = [caso["estrategia"]]
    rs = vg.barrer(ctx)
    tol = caso["tolerancia"]
    buenas = [r for r in rs if r["viviendas"] >= tol["viviendas_min"]
              and (not tol.get("plazas_deben_cumplir") or r["comprobaciones"]["plazas"])]
    mejor = max(rs, key=lambda r: (r["cumple"], r["viviendas"]))
    ok = bool(buenas)
    print(f"Caso {caso['caso']} ({caso['patron']}, {caso['estrategia']}): "
          f"{'OK' if ok else 'NO REPRODUCE'} · ejemplo {caso['cifras_leidas_estimadas']['casas']} casas · "
          f"motor {mejor['viviendas']} viv, {mejor['plazas']}/{mejor['plazas_necesarias']} plazas, "
          f"cumple={mejor['cumple']} · {len(buenas)} de {len(rs)} variantes dentro de tolerancia")
    return ok


def main() -> int:
    casos = sorted((RAIZ / "patrones" / "casos").glob("caso_*.json"))
    resultados = [probar(c) for c in casos]
    print(f"{sum(resultados)}/{len(resultados)} casos reproducidos")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
