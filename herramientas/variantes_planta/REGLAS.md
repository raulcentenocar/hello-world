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

## 7. Cómo ampliar las reglas

Para enseñar una regla nueva al estudio:
1. Añádela a este documento (valor, motivo y referencia normativa si la hay).
2. Si es una medida, añade el campo al panel y al objeto `DEF` de `variantes_planta.html`; si es una pieza, añádela en `piecesFor()` con su cuerpo y su holgura.
3. Regenera y revisa en la pestaña **Comprobación** que la regla aparece y se cumple.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
