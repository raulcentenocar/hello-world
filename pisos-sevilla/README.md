# Alerta de pisos en Sevilla

Te avisa por **Telegram** (o por email) cuando aparece un piso que encaja:

- Alquiler de **2 dormitorios**, **≤ 900 €/mes**
- Zonas: **Viapol, Gran Plaza, Nervión, San Pablo, El Porvenir, Felipe II, Tiro de Línea y Bami**
- No repite avisos de pisos ya vistos y **te avisa si alguno baja de precio**
- Cada aviso incluye m², planta, ascensor, exterior/interior y €/m²

Funciona gratis en GitHub Actions: no necesitas tener el ordenador encendido.

```
🏠 850 €/mes · 2 dorm. · Nervión
Calle Luis Montoto
75 m² · planta 3 · con ascensor · exterior · 11.3 €/m²
https://www.idealista.com/inmueble/...
```

## Cómo detecta la zona

El portal se consulta con un círculo de 3,5 km centrado en Nervión. Después cada
anuncio se asigna a una zona de dos maneras:

1. **Por nombre**: si el barrio, el distrito o la dirección contiene alguno de los
   textos de la zona (sin importar tildes ni mayúsculas).
2. **Por distancia**: si sus coordenadas caen dentro del radio de la zona.

Los centros y radios de `config.toml` son aproximados. Si ves que se cuelan o se
escapan pisos de una zona, ajusta `lat`, `lon` o `radio_m` (Google Maps → clic
derecho → copias las coordenadas).

## Puesta en marcha (unos 15 minutos)

### 1. Bot de Telegram

1. En Telegram, abre **@BotFather** → `/newbot` → ponle un nombre. Te da el
   **token**.
2. Escribe cualquier mensaje a tu bot nuevo.
3. Abre `https://api.telegram.org/bot<TOKEN>/getUpdates` en el navegador y copia
   el número de `"chat":{"id": ...}`. Ese es tu **chat id**.

### 2. Acceso a la API de idealista

Pide acceso en <https://developers.idealista.com/access-request> (uso personal).
Te envían una **API key** y un **secret** por email. El plan gratuito tiene un
límite de peticiones al mes, por eso el workflow consulta 3 veces al día.

### 3. Secretos en GitHub

En el repositorio: **Settings → Secrets and variables → Actions → New repository
secret**, y crea:

| Secreto | Valor |
|---|---|
| `IDEALISTA_API_KEY` | API key de idealista |
| `IDEALISTA_API_SECRET` | Secret de idealista |
| `TELEGRAM_BOT_TOKEN` | Token de @BotFather |
| `TELEGRAM_CHAT_ID` | Tu chat id |

Para recibir email en vez de Telegram, o además de Telegram (opcional):
`SMTP_HOST` (p. ej. `smtp.gmail.com`), `SMTP_USER`, `SMTP_PASSWORD` (en Gmail,
una "contraseña de aplicación") y `EMAIL_TO`.

### 4. Activarlo

Haz merge de esta rama a `main`, ya que los workflows programados solo se
ejecutan desde la rama principal. Después, en **Actions → Alerta pisos Sevilla →
Run workflow**, lánzalo una vez para comprobar que llega el primer aviso.

> La primera ejecución te avisará de **todos** los pisos que ya encajan. A partir
> de ahí, solo de los nuevos y de las rebajas.

## Cambiar lo que buscas

Todo está en [`config.toml`](config.toml): precio máximo, dormitorios (p. ej.
`dormitorios_max = 3`), superficie mínima, excluir plantas bajas, y zonas. Para
añadir una zona, copia un bloque `[[zonas]]`.

## Probar en local

```bash
cd pisos-sevilla
python3 alerta_pisos.py --demo     # datos de ejemplo, sin red
python3 -m unittest -v             # tests
python3 alerta_pisos.py --dry-run  # consulta real, sin enviar avisos (requiere claves)
```

Solo necesita Python 3.11 o superior, sin instalar librerías.

## Añadir otros portales

Cada portal es una función que devuelve una lista de `Anuncio`, registrada en
`FUENTES` dentro de `alerta_pisos.py`. Fotocasa, Habitaclia y pisos.com no tienen
API pública y bloquean las consultas automáticas, así que para esos es mejor usar
las alertas propias de sus apps (ver abajo).

## Complemento recomendado: alertas nativas de los portales

La API gratuita de idealista solo permite consultar unas pocas veces al día. En
alquiler en Sevilla, un buen piso a buen precio puede durar horas. Combínalo con
esto:

- **idealista app** → Buscar → "Dibujar zona" en el mapa (traza Nervión–Viapol–
  Porvenir–Bami–Tiro de Línea y otra para San Pablo) → filtros (≤ 900 €,
  2 dormitorios) → **Guardar búsqueda** con **notificaciones inmediatas**.
- **Fotocasa** y **Habitaclia**: igual, con búsqueda guardada y alerta push.

Las alertas push te dan rapidez. Esta herramienta añade el filtrado fino por
zona, el €/m², el aviso de rebajas y el historial de todo lo que ha salido (en
`data/vistos.json`), útil para ver qué precios se mueven en cada barrio.
