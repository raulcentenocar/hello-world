#!/usr/bin/env python3
"""Alerta de pisos en Sevilla.

Consulta los portales configurados, filtra los anuncios por precio,
dormitorios y zona, y avisa por Telegram (y/o email) de los anuncios nuevos.
Guarda los anuncios ya vistos en data/vistos.json para no repetir avisos.

Uso:
    python alerta_pisos.py            # ejecución normal
    python alerta_pisos.py --demo     # prueba con datos de ejemplo, sin red
    python alerta_pisos.py --dry-run  # consulta los portales pero no envía avisos

Solo usa la biblioteca estándar de Python (3.11+).
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import smtplib
import sys
import tomllib
import unicodedata
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONFIG = BASE / "config.toml"
VISTOS = BASE / "data" / "vistos.json"
DEMO = BASE / "data" / "demo_anuncios.json"


# --------------------------------------------------------------------------
# Modelo
# --------------------------------------------------------------------------
@dataclass
class Anuncio:
    id: str
    fuente: str
    url: str
    precio: float
    dormitorios: int
    superficie: float | None = None
    direccion: str = ""
    barrio: str = ""
    distrito: str = ""
    planta: str = ""
    lat: float | None = None
    lon: float | None = None
    ascensor: bool | None = None
    exterior: bool | None = None
    foto: str = ""
    zona: str = field(default="", compare=False)

    @property
    def clave(self) -> str:
        return f"{self.fuente}:{self.id}"


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, para comparar nombres de barrios."""
    texto = unicodedata.normalize("NFD", texto or "")
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.lower().replace("-", " ").split())


def distancia_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en metros entre dos coordenadas (fórmula de haversine)."""
    r = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def cargar_config(ruta: Path = CONFIG) -> dict:
    with open(ruta, "rb") as f:
        return tomllib.load(f)


# --------------------------------------------------------------------------
# Filtros
# --------------------------------------------------------------------------
def zona_de(anuncio: Anuncio, zonas: list[dict]) -> str | None:
    """Devuelve el nombre de la zona del anuncio, o None si no está en ninguna.

    Primero busca por nombre (barrio/distrito/dirección) y, si no coincide,
    por distancia al centro de cada zona.
    """
    texto = normalizar(f"{anuncio.barrio} | {anuncio.distrito} | {anuncio.direccion}")
    for z in zonas:
        if any(normalizar(n) in texto for n in z.get("nombres", [])):
            return z["nombre"]
    if anuncio.lat is not None and anuncio.lon is not None:
        mejor = None
        for z in zonas:
            d = distancia_m(anuncio.lat, anuncio.lon, z["lat"], z["lon"])
            if d <= z.get("radio_m", 500) and (mejor is None or d < mejor[1]):
                mejor = (z["nombre"], d)
        if mejor:
            return mejor[0]
    return None


ES_BAJO = {"bj", "bajo", "st", "ss", "sotano", "semisotano", "en", "entreplanta"}


def cumple(anuncio: Anuncio, config: dict) -> bool:
    c = config["criterios"]
    if anuncio.precio <= 0 or anuncio.precio > c["precio_max"]:
        return False
    if not (c["dormitorios_min"] <= anuncio.dormitorios <= c["dormitorios_max"]):
        return False
    if c.get("superficie_min") and (anuncio.superficie or 0) < c["superficie_min"]:
        return False
    if c.get("excluir_bajos") and normalizar(anuncio.planta) in ES_BAJO:
        return False
    zona = zona_de(anuncio, config["zonas"])
    if not zona:
        return False
    anuncio.zona = zona
    return True


# --------------------------------------------------------------------------
# Fuentes de anuncios
# --------------------------------------------------------------------------
def _http(url: str, data: bytes | None = None, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def fuente_idealista(config: dict) -> list[Anuncio]:
    """API oficial de idealista (https://developers.idealista.com).

    Necesita las variables de entorno IDEALISTA_API_KEY e IDEALISTA_API_SECRET.
    El plan gratuito tiene un límite de peticiones al mes, así que se pide
    una sola página ordenada por fecha de publicación (lo más reciente primero).
    """
    key = os.environ.get("IDEALISTA_API_KEY")
    secret = os.environ.get("IDEALISTA_API_SECRET")
    if not key or not secret:
        print("[idealista] sin credenciales: se omite esta fuente")
        return []

    auth = base64.b64encode(f"{key}:{secret}".encode()).decode()
    token = _http(
        "https://api.idealista.com/oauth/token",
        data=b"grant_type=client_credentials&scope=read",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
    )["access_token"]

    c, b = config["criterios"], config["busqueda"]
    params = {
        "operation": c.get("operacion", "rent"),
        "propertyType": "homes",
        "center": f"{b['centro_lat']},{b['centro_lon']}",
        "distance": b["radio_m"],
        "maxPrice": c["precio_max"],
        "bedrooms": ",".join(
            str(n) for n in range(c["dormitorios_min"], c["dormitorios_max"] + 1)
        ),
        "maxItems": 50,
        "numPage": 1,
        "order": "publicationDate",
        "sort": "desc",
        "locale": "es",
    }
    if c.get("superficie_min"):
        params["minSize"] = c["superficie_min"]

    resp = _http(
        "https://api.idealista.com/3.5/es/search",
        data=urllib.parse.urlencode(params).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
    )
    return [_idealista_a_anuncio(e) for e in resp.get("elementList", [])]


def _idealista_a_anuncio(e: dict) -> Anuncio:
    return Anuncio(
        id=str(e.get("propertyCode", "")),
        fuente="idealista",
        url=e.get("url", ""),
        precio=float(e.get("price") or 0),
        dormitorios=int(e.get("rooms") or 0),
        superficie=e.get("size"),
        direccion=e.get("address", ""),
        barrio=e.get("neighborhood", ""),
        distrito=e.get("district", ""),
        planta=str(e.get("floor", "")),
        lat=e.get("latitude"),
        lon=e.get("longitude"),
        ascensor=e.get("hasLift"),
        exterior=e.get("exterior"),
        foto=e.get("thumbnail", ""),
    )


def fuente_demo(_config: dict) -> list[Anuncio]:
    with open(DEMO, encoding="utf-8") as f:
        return [_idealista_a_anuncio(e) for e in json.load(f)]


FUENTES = {"idealista": fuente_idealista}


# --------------------------------------------------------------------------
# Avisos
# --------------------------------------------------------------------------
def formatear(a: Anuncio) -> str:
    extras = []
    if a.superficie:
        extras.append(f"{a.superficie:.0f} m²")
    if a.planta:
        extras.append(f"planta {a.planta}")
    if a.ascensor is not None:
        extras.append("con ascensor" if a.ascensor else "sin ascensor")
    if a.exterior is not None:
        extras.append("exterior" if a.exterior else "interior")
    if a.superficie:
        extras.append(f"{a.precio / a.superficie:.1f} €/m²")
    lineas = [
        f"🏠 {a.precio:.0f} €/mes · {a.dormitorios} dorm. · {a.zona}",
        a.direccion or a.barrio,
        " · ".join(extras),
        a.url,
    ]
    return "\n".join(l for l in lineas if l)


def enviar_telegram(texto: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return False
    data = urllib.parse.urlencode(
        {"chat_id": chat, "text": texto, "disable_web_page_preview": "false"}
    ).encode()
    _http(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    return True


def enviar_email(asunto: str, cuerpo: str) -> bool:
    host = os.environ.get("SMTP_HOST")
    usuario = os.environ.get("SMTP_USER")
    clave = os.environ.get("SMTP_PASSWORD")
    destino = os.environ.get("EMAIL_TO") or usuario
    if not (host and usuario and clave and destino):
        return False
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = asunto, usuario, destino
    msg.set_content(cuerpo)
    with smtplib.SMTP_SSL(host, int(os.environ.get("SMTP_PORT", "465"))) as s:
        s.login(usuario, clave)
        s.send_message(msg)
    return True


def avisar(nuevos: list[Anuncio], dry_run: bool) -> None:
    textos = [formatear(a) for a in nuevos]
    if dry_run:
        print("\n\n".join(textos))
        return
    por_telegram = False
    for t in textos:
        por_telegram = enviar_telegram(t) or por_telegram
    asunto = f"{len(nuevos)} piso(s) nuevo(s) en Sevilla"
    por_email = enviar_email(asunto, "\n\n".join(textos))
    if not (por_telegram or por_email):
        print("[aviso] no hay Telegram ni email configurados; muestro los anuncios:")
        print("\n\n".join(textos))


# --------------------------------------------------------------------------
# Estado (anuncios ya vistos)
# --------------------------------------------------------------------------
def cargar_vistos(ruta: Path = VISTOS) -> dict:
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    return {}


def guardar_vistos(vistos: dict, ruta: Path = VISTOS) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(
        json.dumps(vistos, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------
def ejecutar(config: dict, anuncios: list[Anuncio], vistos: dict) -> list[Anuncio]:
    """Filtra y devuelve los anuncios nuevos; marca como vistos los que cumplen."""
    ahora = datetime.now(timezone.utc).isoformat(timespec="minutes")
    nuevos = []
    for a in anuncios:
        if not cumple(a, config):
            continue
        anterior = vistos.get(a.clave)
        # Avisa si es nuevo o si ha bajado de precio desde la última vez.
        if anterior is None or a.precio < anterior.get("precio", a.precio):
            if anterior is not None:
                a.zona += f" (rebajado desde {anterior['precio']:.0f} €)"
            nuevos.append(a)
        vistos[a.clave] = {
            "precio": a.precio,
            "zona": a.zona.split(" (")[0],
            "url": a.url,
            "visto": anterior.get("visto", ahora) if anterior else ahora,
        }
    return nuevos


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--demo", action="store_true", help="usa datos de ejemplo, sin red")
    p.add_argument("--dry-run", action="store_true", help="no envía avisos ni guarda estado")
    args = p.parse_args()

    config = cargar_config()
    if args.demo:
        anuncios, vistos, dry = fuente_demo(config), {}, True
    else:
        anuncios = []
        for nombre, fuente in FUENTES.items():
            try:
                anuncios += fuente(config)
            except Exception as exc:  # una fuente caída no debe parar las demás
                print(f"[{nombre}] error: {exc}", file=sys.stderr)
        vistos, dry = cargar_vistos(), args.dry_run

    nuevos = ejecutar(config, anuncios, vistos)
    print(f"{len(anuncios)} anuncios leídos, {len(nuevos)} nuevos que encajan.")
    if nuevos:
        avisar(nuevos, dry)
    if not args.demo and not args.dry_run:
        guardar_vistos(vistos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
