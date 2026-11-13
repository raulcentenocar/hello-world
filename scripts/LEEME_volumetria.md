# Generador de volumetrías (herramienta interna, sin IA)

Herramienta propia de encaje volumétrico para estudios de viabilidad. Primer piloto: **Madrid**.
Es un cálculo con reglas fijas y reproducible: la misma entrada da siempre el mismo resultado.

## Flujo de trabajo

1. **Parcela.** Descarga la parcela del Catastro (o dibuja las coordenadas a mano en metros):
   ```bash
   python3 scripts/catastro_parcela.py <REFERENCIA_CATASTRAL>      # → datos/<ref>.gml
   ```
2. **Entrada.** Copia `scripts/ejemplos/ejemplo_ficticio.json` a `datos/volumetria.json`:
   - `parcela`: `{"gml": "<ref>.gml"}` o `{"coordenadas": [[x, y], ...]}`.
   - `urbanismo`: **solo** los valores de la ficha urbanística / norma zonal del PGOUM.
     Lo que no figure en la ficha se deja fuera o en `null`: el script marca `FALTA DATO`.
   - `hipotesis`: parámetros de diseño (fondo de bloque, altura de planta, m² por vivienda…).
     Tienen valor por defecto y salen siempre listados en el resultado.
3. **Fachadas.** Mira qué lados dan a la vía pública y anota sus índices en `fachadas`:
   ```bash
   python3 scripts/volumetria_generador.py datos/volumetria.json --lados
   ```
4. **Generar.**
   ```bash
   python3 scripts/volumetria_generador.py datos/volumetria.json          # tabla + DXF en planos/volumetrias/
   python3 scripts/volumetria_generador.py datos/volumetria.json --json   # para los agentes
   ```

## Tipologías y parámetros urbanísticos que exige cada una

| Tipología | Qué genera | Parámetros de la ficha que necesita (además de edificabilidad, ocupación y nº de plantas) |
|---|---|---|
| `entre_medianeras` | Banda de fondo edificable desde las fachadas | fondo edificable, retranqueo de fachada, `fachadas` |
| `manzana_cerrada` | Banda perimetral con patio de manzana (la parcela es la manzana completa) | fondo edificable, retranqueo de fachada |
| `bloque_abierto` | Bloques lineales paralelos; prueba orientaciones cada 5° y las de los lados | retranqueo de fachada, retranqueo a linderos, separación entre edificios (longitud máxima de bloque, opcional) |
| `torre` | Bloques en punto en retícula | retranqueo de fachada, retranqueo a linderos, separación entre edificios |
| `unifamiliar_aislada` | Una vivienda dentro de la zona de retranqueos | retranqueo de fachada, retranqueo a linderos |
| `unifamiliar_adosada` | Hileras paralelas a la fachada más larga | retranqueo de fachada, retranqueo a linderos, separación entre edificios, `fachadas` |

La altura máxima en metros es opcional. Si está, limita el número de plantas con la hipótesis de altura de planta.

## Reglas aplicadas

- **Retranqueo** = distancia mínima de cualquier punto del edificio al lindero.
- **Fondo edificable** = distancia en perpendicular a la alineación de fachada.
- **Ocupación**: si la huella geométrica la supera, se reduce el fondo (medianeras o manzana), se encoge la huella (aislada) o se quitan edificios, empezando por el más pequeño (bloques y torres).
- **Edificabilidad**: el techo materializable es el menor entre huella × plantas y parcela × edificabilidad. El cálculo base reutiliza `scripts/urbanismo_calculo.py`.
- **Viviendas**: techo ÷ m² construidos por vivienda (hipótesis). En adosadas, longitud de la hilera ÷ ancho de la vivienda.

## Salidas

DXF por tipología en `planos/volumetrias/` con las capas `PARCELA`, `ZONA_EDIFICABLE`, `HUELLA`, `VOLUMEN_3D` (polilíneas con espesor igual a la altura, visibles en 3D en AutoCAD o BricsCAD) y `TEXTO`.

## Qué NO hace todavía

- No lee el PGOUM ni las normas zonales: los parámetros se meten a mano desde la ficha.
- No calcula superficies no computables, áticos, retranqueos de planta, vuelos ni patios interiores mínimos.
- No calcula el soleamiento ni usa la topografía.
- No comprueba el CTE ni el Decreto de habitabilidad de la Comunidad de Madrid.

Instalación: `pip install -r scripts/requirements.txt`

PENDIENTE DE VALIDAR POR EL ARQUITECTO
