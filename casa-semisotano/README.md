# Vivienda Semisótano 150

Herramienta web paramétrica (un solo archivo, sin dependencias) para diseñar una vivienda unifamiliar
de **150 m² construidos computables (PB + P1)** sobre un **semisótano que no computa edificabilidad**,
con una planta tipo que sirve igual para vivienda **aislada, pareada o adosada**.

Abrir `index.html` en el navegador (o vía GitHub Pages en `/casa-semisotano/`).

## Qué genera
- **Ficha de parcela editable + lector de cédulas**: la pestaña *Parcela* guarda parámetros urbanísticos,
  vértices UTM y linderos (calle, lindero o zona verde, con arcos y radios). Puede rellenarse a mano, pegando un
  JSON o, dentro de claude.ai, subiendo la cédula en PDF o imagen: Claude la lee (página completa y ampliaciones)
  y propone la ficha para revisarla antes de aplicarla. Fuera de claude.ai se ofrecen unas instrucciones para
  copiar en un chat con Claude y pegar la respuesta. La IA solo se usa para leer el documento: el resto es cálculo.
- **Programa a medida**: en cada planta eliges qué estancia va en cada hueco (dos a calle, dos en el núcleo
  interior y dos a jardín) y su superficie deseada. Dos modos de dimensionado: *Ajustar al objetivo* (escala el
  programa hasta los m² computables fijados) o *Según programa* (respeta tus superficies y calcula lo que ocupa).
  Tabla de deseado / resultado / diferencia y plantas en vivo al lado.
- **Editor de viales (tipo TestFit)**: dibujas los viales sobre la parcela (clic para añadir puntos, doble clic o
  Intro para terminar, arrastrar nodos para moverlos, rueda para acercar) y a ambos lados se generan parcelas privadas
  con vivienda, frente de acceso y jardín. El motor es un algoritmo geométrico determinista que se ejecuta en el
  navegador, sin IA: respeta parcela, retranqueos, viales, martillos de giro en fondos de saco y parcelas ya colocadas.
  Plantillas de partida (una calle, calle + Avenida, dos calles, en L, en bucle, patio común), capas, vista de
  cubiertas o planta baja y 3D, con paneles flotantes al estilo Giraffe.
- **Ordenación UA-03-01 por esquemas**: cuatro esquemas de implantación que se calculan y comparan a la vez
  (patio común con garaje comunitario, una calle interior, calle interior + Avenida, dos calles interiores),
  con viario privado en fondo de saco y martillo de giro, aparcamiento en parcela (2 plazas en el frente o garaje
  con rampa), bloques opcionales, vista de cubiertas, planta baja y modelo 3D (three.js).
- **Ordenación UA-03-01** (Sector 1 «Los Pocillos», Villanueva de la Cañada): parcela real dibujada desde las
  coordenadas UTM de la cédula, hileras paramétricas (sur, norte, central y oeste) con la planta baja del modelo,
  jardines privados, patio común sobre garaje comunitario con una sola rampa desde Calle Floristas y
  comprobación frente a la cédula (34 viviendas, 5.100 m²c, 60 % de ocupación, retranqueos, 2 plazas por vivienda).
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
