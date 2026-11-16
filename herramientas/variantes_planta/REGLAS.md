# Reglas de distribución de vivienda

Base de conocimiento que aplica el generador de variantes (`variantes_planta.html`) y que puede consultar cualquier agente del estudio al proponer distribuciones. Es la "memoria" del estudio: lo que aquí se fija se aplica igual a cualquier envolvente.

**Todos los valores son hipótesis de partida editables** (panel de la herramienta). Proceden de medidas de referencia habituales en manuales de dimensionado (Neufert y similares), de la práctica española y del CTE. **Comprueba siempre el decreto de habitabilidad autonómico y las ordenanzas municipales del encargo**, que prevalecen sobre estos valores.

Unidades: metros y m². Superficies útiles.

---

## 1. Cómo se aplica una regla

Cada planta candidata pasa por cinco filtros en este orden. Si falla uno, se descarta, y la herramienta cuenta cuántas se descartan en cada filtro.

| # | Filtro | Qué comprueba |
|---|--------|---------------|
| 1 | Superficie y proporción | Superficie útil mínima, lado menor y proporción largo/ancho de cada estancia |
| 2 | Accesos | Cada estancia se alcanza desde salón o pasillo con una puerta que cabe en el tabique; baño en suite solo desde un dormitorio; al menos un baño común; entrada por la fachada indicada |
| 3 | Luz y ventilación | Superficie de hueco, ventilación natural, profundidad desde fachada, huecos que no coinciden con pilares |
| 4 | Mobiliario y pilares | Cada pieza obligatoria cabe con su holgura, sin chocar con puertas, pilares, huecos ni otras piezas; pasillo libre de pilares; puertas que no caen sobre un pilar |
| 5 | Diversidad | Entre las válidas se eligen las más distintas entre sí y las de mejor puntuación |

### Cuerpos y holguras

Cada mueble se modela con dos rectángulos:

- **Cuerpo**: lo que ocupa físicamente. No puede solaparse con otros cuerpos, con holguras de otras piezas, con el barrido de puertas, con pilares ni con la zona de entrada.
- **Holgura (zona de uso)**: el espacio libre necesario para usarlo (paso junto a la cama, frente de armario, frente de cocina…). No puede contener cuerpos, pero **sí puede compartirse** con otras holguras y con el barrido de puertas, igual que en un dimensionado manual.

Las piezas "de pared" (cama, armario, sofá, encimera, sanitarios) deben apoyarse en un tramo de tabique o muro real: no en un hueco de puerta ni en el borde abierto entre cocina y salón. El armario, por su altura, tampoco puede ir delante de una ventana.

La opción **Zonas de uso** de la lámina dibuja las holguras con trazo discontinuo para revisarlas.

---

## 2. Estancias

| Estancia | Sup. útil mín. | Lado menor mín. | Proporción máx. | Luz natural |
|---|---|---|---|---|
| Salón (estar-comedor) | 16,0 | 3,00 | 2,6 | Obligatoria (≥ 1,20 m de fachada) |
| Cocina abierta | 6,0 | 1,60 | 4,0 | Propia o a través del salón |
| Cocina cerrada | 6,0 | 1,80 | 3,2 | Obligatoria si se marca "Cocina cerrada con luz natural" |
| Dormitorio principal | 10,0 | 2,50 | 2,2 | Obligatoria |
| Otros dormitorios | 8,0 | 2,20 | 2,2 | Obligatoria |
| Baño | 3,5 (máx. 9,0) | 1,40 | 2,8 | No; sin fachada lleva extracción mecánica (CTE DB-HS3) |
| Pasillo | — | ancho libre ≥ 0,90 (1,10 accesible) | — | No |

Programa: como máximo un baño más que dormitorios. El dormitorio 1 es el principal (cama doble).

---

## 3. Mobiliario mínimo por estancia y holguras

### Dormitorio principal
| Pieza | Cuerpo | Holgura |
|---|---|---|
| Cama doble | 1,50 × 2,00 con cabecero contra pared | Paso lateral 0,70 a ambos lados (0,90 accesible) y 0,60 a los pies |
| Mesillas (si caben) | 0,45 × 0,40 a cada lado | — |
| Armario | 1,50 × 0,60 | Frente libre 0,70 |

### Dormitorio individual
| Pieza | Cuerpo | Holgura |
|---|---|---|
| Cama individual | 0,90 × 1,90 contra pared | Paso lateral 0,70 en un lado (0,90 accesible) |
| Armario | 1,00 × 0,60 | Frente libre 0,70 |

### Salón
| Pieza | Cuerpo | Holgura |
|---|---|---|
| Sofá | 2,10 × 0,90 contra pared | Zona libre de 1,80 hasta el mueble de TV |
| Mueble TV | 1,60 × 0,45 | — |
| Mesa de comedor | 2 personas: 0,80 × 0,80 · 4 personas: 1,20 × 0,80 · 6 personas: 1,60 × 0,90 | Zona de silla de 0,70 alrededor de toda la mesa |

Nº de comensales = 2 + 1 por cada dormitorio adicional al principal. Si la mesa no cabe en el salón, se prueba en la cocina (cocina-comedor).

### Cocina
| Pieza | Cuerpo | Holgura |
|---|---|---|
| Encimera (lineal o en L) | Fondo 0,60; longitud ≥ 2,40 m (hasta 1 dormitorio) + 0,40 m por cada dormitorio extra | Frente libre 1,10 |

La longitud incluye fregadero, placa y frigorífico en el mismo frente. En L se cuenta una sola vez la esquina.

### Baño
| Pieza | Cuerpo | Holgura |
|---|---|---|
| Ducha | 0,80 × 1,20 | — |
| Inodoro | 0,40 × 0,65 | 0,20 a cada lado y 0,60 por delante (accesible: 0,80 de transferencia en un lado) |
| Lavabo | 0,60 × 0,50 | Frente libre 0,70 |

### Vivienda accesible (opción)
- Círculo de giro libre de obstáculos de Ø 1,50 en salón, cocina, dormitorios y baños (referencia: CTE DB-SUA, Anejo A). La herramienta lo comprueba con un cuadrado de 1,50 de lado, criterio más exigente que el círculo.
- Paso de 0,90 a ambos lados de la cama doble y en un lado de la individual; transferencia lateral de 0,80 al inodoro; pasillo ≥ 1,10.
- Al activarla, las superficies objetivo de dormitorios, cocina y baños aumentan para que quepa el giro.

### Puertas
- Paso libre 0,80. La hoja abre hacia el local privado y su barrido (0,80 × 0,80) no puede contener muebles.
- La puerta se coloca a 0,15 de una esquina; se prueban los dos extremos del tabique y se queda la que permite amueblar.
- En el lado común (salón o pasillo) se reserva una zona libre de 0,80 delante de cada puerta, de 1,00 en el paso salón-pasillo y de 1,20 × (puerta + 0,30) en la entrada.

---

## 4. Iluminación y ventilación

| Regla | Valor por defecto |
|---|---|
| Superficie de hueco ≥ % de la superficie útil del local | 12,5 % (1/8) |
| Ventilación natural ≥ % de la superficie útil | 8,3 % (1/12); se toma el hueco como practicable |
| Altura de hueco para calcular la superficie | 1,50 |
| Profundidad máxima del local desde la fachada con hueco | 7,00 |
| Separación de huecos a esquinas | ≥ 0,30 |
| Separación de huecos a pilares de fachada | ≥ 0,10 |

- Salón y dormitorios necesitan hueco a una fachada con luz. La cocina abierta sin fachada propia se ilumina a través del salón: el hueco del salón se calcula sobre salón + cocina y la profundidad se mide hasta el fondo de la cocina.
- Baños y cocinas sin fachada: ventilación mecánica con extracción (CTE DB-HS3). Se agrupan las zonas húmedas para compartir bajantes y patinillos (criterio de puntuación, no eliminatorio).

---

## 5. Estructura

- Retícula de pilares de 0,30 × 0,30 según las luces indicadas, igual en todas las variantes ("mismos muros, misma estructura").
- Un pilar que entra más de 6 cm en un local es un obstáculo para el mobiliario.
- Ninguna puerta, ventana ni entrada puede coincidir con un pilar.
- Un pilar dentro del pasillo solo se admite si deja el ancho libre mínimo.

---

## 6. Criterios de calidad (puntuación, no eliminatorios)

Entre las válidas se priorizan las que tienen:
- Superficies cercanas a las objetivo del programa.
- Estancias poco alargadas (proporción cercana a 1,5).
- Más fachada en salón y dormitorios.
- Menos pasillo respecto a la superficie útil.
- Baños sin apertura directa al salón y dormitorios que no abren al salón cuando hay pasillo.
- Zonas húmedas agrupadas.

---

## 6 bis. Vivienda unifamiliar adosada (planta baja + primera)

Proyecto piloto: **UA-03-01, sector "Los Pocillos", Villanueva de la Cañada** (cédula en `datos/UA 03 01.pdf`). Datos de la cédula que usa la herramienta: 2 plantas, edificabilidad 5.100 m²c / 34 viviendas = **150 m²c por vivienda**, linderos a 0 m (medianeras sin huecos), 2 plazas de aparcamiento por vivienda (en planta baja, semisótano o sótano). **El frente y el fondo de cada vivienda no están en la cédula**: el 6,00 × 12,50 m de la herramienta es un ejemplo (2 × 75 m² = 150 m²c) a confirmar.

### Esquema
- Huella igual en las dos plantas. Huecos solo en fachada delantera (acceso) y trasera; las medianeras son ciegas, salvo en vivienda de extremo de hilera (marcar la fachada lateral con luz).
- La **escalera ocupa la misma posición en las dos plantas**, apoyada en una medianera. Se reparte la planta en tres franjas: delantera, franja de escalera y trasera.
- En la franja de escalera, junto a la escalera, va un distribuidor de ancho mínimo. El resto de esa franja (sin fachada) se aprovecha siempre para baños, aseo, cocina abierta al salón o una pieza auxiliar (lavadero en planta baja, vestidor en planta primera). Así se evitan distribuidores de 15-20 m².
- Si en la franja delantera o trasera hay dos o más piezas con puerta, puede aparecer un pasillo a lo ancho junto a la franja de escalera, con las piezas en batería.
- Planta baja: salón, cocina, aseo (opcional), vestíbulo de entrada (≤ 6 m²), dormitorio en planta baja y garaje (opcionales). El salón da preferentemente a la fachada trasera (jardín).
- Planta primera: dormitorios y baños; al menos un baño accesible desde el distribuidor. El dormitorio principal es siempre el mayor.

### Escalera (uso restringido, CTE DB-SUA 1)
| Parámetro | Valor por defecto |
|---|---|
| Ancho de tramo | 0,90 (mín. 0,80) |
| Contrahuella máxima | 0,185 |
| Huella | 0,27 |
| Altura entre plantas | 3,00 (hipótesis) |
| Recta | 17 contrahuellas → 16 huellas → 4,32 m de largo × 0,90 |
| Ida y vuelta | 2 tramos de 8 huellas + meseta de 0,90 → 3,06 m × 1,90 |

La escalera debe abrir a lo largo de su lado libre al distribuidor; en la planta baja se marca "SUBE" y en la primera "BAJA".

### Garaje
- Plaza de 2,50 × 5,00, apoyada en la fachada de acceso, con puerta de garaje de 2,50-3,00 m que no coincide con pilares. Dos plazas en batería o una junto a otra.
- **Con 6,00 × 12,50 m el garaje dentro de la vivienda no cabe**: la plaza ocupa unos 5,30 m de fondo en la franja delantera y no deja salón, cocina y vestíbulo con sus mínimos. Alternativas: plazas en la parcela, en sótano o semisótano (la cédula lo permite) o mayor frente.

### Edificabilidad
- Superficie construida = 2 × ancho × fondo. La herramienta avisa si supera la edificabilidad por vivienda indicada.

---

## 7. Cómo ampliar las reglas

Para enseñar una regla nueva al estudio:
1. Añádela a este documento (valor, motivo y referencia normativa si la hay).
2. Si es una medida, añade el campo al panel y al objeto `DEF` de `variantes_planta.html`; si es una pieza, añádela en `piecesFor()` con su cuerpo y su holgura.
3. Regenera y revisa en la pestaña **Comprobación** que la regla aparece y se cumple.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
