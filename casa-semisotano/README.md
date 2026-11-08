# Vivienda Semisótano 150

Herramienta web paramétrica (un solo archivo, sin dependencias) para diseñar una vivienda unifamiliar
de **150 m² construidos computables (PB + P1)** sobre un **semisótano que no computa edificabilidad**,
con una planta tipo que sirve igual para vivienda **aislada, pareada o adosada**.

Abrir `index.html` en el navegador (o vía GitHub Pages en `/casa-semisotano/`).

## Qué genera
- **Plantas** de semisótano, planta baja y planta primera con muros, medianeras rayadas, carpinterías,
  puertas, escalera en U, cotas y superficies útiles por estancia.
- **Sección longitudinal** con rasante, límite de cota del semisótano, rampa de garaje, patio inglés,
  cotas de planta y altura a cornisa frente a la máxima.
- **Agrupación**: pareadas en espejo o hilera de N adosadas, con parcelas, retranqueos y rampas.
- **Cuadro de superficies** (útil / construida, computable / no computable).
- **Comprobaciones**: edificabilidad, semisótano no computable, ocupación, altura, fondo, frente y fondo
  de parcela, rampa y plazas de garaje, escalera (CTE DB SUA 1, uso restringido) y mínimos de habitabilidad.
- **Exportación** a DXF R12 (metros, por capas), SVG y JSON de parámetros.

## Esquema de proyecto
Tres crujías longitudinales: escalera junto a una medianera, distribuidor central al que abren todas las
piezas y crujía húmeda junto a la otra medianera. Todas las estancias ventilan a fachada delantera o trasera,
así que los laterales pueden ser ciegos y la vivienda se puede adosar. Las unidades alternan en espejo para
que escaleras y baños de viviendas vecinas queden espalda con espalda.

Los valores normativos son orientativos y editables: ajústalos al PGOU y a la normativa autonómica de cada caso.
