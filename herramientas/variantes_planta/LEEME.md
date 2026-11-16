# Generador de variantes de planta

Herramienta de presentación para **pisos de una planta** y **adosados de planta baja + primera** (por defecto, el piloto UA-03-01). A partir de una envolvente fija (mismos muros, misma estructura) genera N distribuciones distintas, cada una con su lámina numerada (`07 / 24`), su cuadro de superficies útiles y un mosaico final de todas las variantes.

Es **determinista, sin IA**: misma semilla + mismos parámetros = mismas plantas.

Cada variante **cumple las reglas de [`REGLAS.md`](REGLAS.md)**: superficies y proporciones, accesos, iluminación y ventilación natural, y mobiliario mínimo con sus holguras (cama, armario, sofá, mesa, encimera, sanitarios), sin chocar con puertas ni pilares. La pestaña **Comprobación** muestra, estancia por estancia, qué se ha comprobado.

## Uso

Abre `index.html` en el navegador (doble clic). No necesita servidor ni instalación.

- **Tipología**: adosado (2 plantas, escalera común a ambas, medianeras ciegas) o piso.
- **Adosado**: tipo y lado de la escalera, ancho de tramo, altura entre plantas, contrahuella, huella, aseo y dormitorio en planta baja, plazas de garaje, edificabilidad por vivienda.
- **Envolvente**: ancho y fondo exteriores, muro, tabique, fachadas con huecos y fachada de acceso.
- **Programa**: rango de dormitorios y baños, cocina abierta/cerrada, con/sin pasillo, vivienda accesible.
- **Luz, ventilación y normativa**: % de hueco, % de ventilación, altura de hueco, profundidad máxima, puertas, pasillo.
- **Mobiliario y holguras**: medidas de cada pieza y su espacio de uso.
- **Superficies mínimas**: hipótesis editables. Ajústalas a la normativa de habitabilidad aplicable.
- **Estructura**: retícula de pilares (luces E-O y N-S), que se repite en todas las variantes.
- **Lámina**: formato 16:9 o 4:5, textos, color de papel, mobiliario, rótulos y cotas.

Teclado: ← → cambia de variante, `M` alterna lámina/mosaico.

## Exportación

| Botón | Salida |
|---|---|
| PNG lámina | Lámina actual (o mosaico) a 2× |
| ZIP completo | Todas las láminas PNG + mosaico + `superficies.csv` + `variantes.json` |
| JSON | Parámetros + geometría de cada estancia (para enlazar con Hectar u otro programa) |
| CSV superficies | Cuadro de superficies por uso (separador `;`, coma decimal) |
| Cargar JSON | Restaura los parámetros de un JSON exportado |

Coordenadas del JSON: metros desde la esquina interior Noroeste, x hacia el Este, y hacia el Sur.

## Cómo genera las plantas

1. Para cada combinación de dormitorios × baños reparte superficies objetivo (con variación aleatoria).
2. Particiona el rectángulo interior en árboles de corte (guillotina), agrupando por afinidad (salón-cocina, zonas húmedas juntas…). Con pasillo: zona de día + zona de noche con pasillo lateral o central.
3. Descarta las que no cumplen las reglas de `REGLAS.md` (superficie, accesos, luz y ventilación, mobiliario con holguras, pilares). La línea de estado dice cuántas se descartan por cada motivo.
4. Elige las N mejores maximizando la diversidad entre ellas.

## Archivos

- `variantes_planta.html`: código fuente (fragmento publicado también como Artifact).
- `index.html`: el mismo código con la cabecera HTML completa, para abrirlo en local. Se regenera con:
  `(printf '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n'; cat variantes_planta.html; printf '\n</body></html>\n') > index.html`

Superficies útiles: se descuenta medio tabique por cada lado interior. Material de presentación: PENDIENTE DE VALIDAR POR EL ARQUITECTO.
