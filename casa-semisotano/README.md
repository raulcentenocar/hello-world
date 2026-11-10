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
- **Espacio de trabajo de ordenación** (inspirado en TestFit y Giraffe): barra superior de herramientas con iconos,
  panel izquierdo de elementos (viales, hileras), usos del suelo con superficies y capas; panel derecho de
  propiedades del elemento seleccionado, tipos de implantación y generación; barra inferior de resultados con
  barras de uso. Deshacer/rehacer (Ctrl+Z / Ctrl+Y), atajos (V, L, C, S, E, O, T), puntos «+» para insertar
  vértices, eliminar punto y mapa base claro con colores por uso.
- **Colmatación automática**: el botón *Colmatar automáticamente* genera viario y lotes sin dibujar nada. Prueba
  estructuras automáticas (anillo perimetral que sigue el lindero, con calles paralelas, transversales o malla) y
  las plantillas clásicas, y se queda con la que mete más viviendas. Los lotes se adaptan: lindes laterales
  perpendiculares al vial (abanico en curvas), lotes que se ensanchan hasta que cabe la vivienda y absorción de
  restos para no dejar huecos. Agrupación adosada, pareada o aislada, parcela mínima y lote tipo editable
  arrastrando (ancho de vivienda, acceso, jardín mínimo y separación lateral).
- **Lotes hasta el fondo de manzana** (como TestFit): cada lote se extiende hasta el lindero, otro vial, una zona
  libre o la mitad entre frentes (con fondo máximo), y se recorta con la forma de la parcela. *Lote tipo* editable
  (acceso, vivienda, jardín mínimo, fondo máximo). *Zonas libres* (parques) que se dibujan, mueven y redimensionan
  con cotas, y los lotes se rehacen alrededor. Estilo *Parcelario* y tarjeta de resultados en 3D con la
  excavación de los semisótanos.
- **Tipos de implantación**: hileras paralelas, calle curva, peine a 90° con fondos de saco, anillo con patio
  central, plazoletas en racimo, malla ortogonal, bucle y patio común con garaje. Viales rectos o curvos (spline),
  modo 90°, anillos cerrados y fondos de saco redondos con viviendas alrededor.
- **Lados con parcelas por vial**: al dibujar se elige si el vial lleva parcelas a ambos lados, solo a la
  izquierda, solo a la derecha o ninguna; después se cambia en el panel del vial o con la herramienta *Lados*
  (clic a un lado del vial). Los lados se marcan en el plano (I/D, verde con parcelas, rojo sin ellas).
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
