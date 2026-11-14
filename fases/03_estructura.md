# F3 — Estructura · Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Cañada) · Variante V1 "Calle de casas"

Agente: estructura · Fecha: 2026-11-14 · Base: `fases/01_urbanismo.md` rev. 2 (aprobada), `fases/02_diseno.md` (**V1 aprobada por el arquitecto**, con las hipótesis de F2 sin cambios: hilera de 52 m, separación de 6 m, plazas de 2,50 × 5,00 m, agrupaciones de al menos 8 viviendas, sin ático ni bajo cubierta, aparcamiento en superficie, sin sótano), `datos/` (solo la cédula; **no hay estudio geotécnico ni topografía**).

> **Aviso de método.**
> - Este documento es un **predimensionado de anteproyecto**. **No sustituye al cálculo estructural** del proyecto de ejecución (CTE DB SE, DB SE-AE, DB SE-C, DB SE-F, Código Estructural RD 470/2021).
> - Las cifras se han obtenido con reglas fijas de predimensionado. Las he calculado a mano y las he dejado programadas en `scripts/estructura_predim.py`. **En esta sesión no tengo herramienta de ejecución (Bash)**, así que el script **no se ha ejecutado**. El coordinador debe ejecutarlo y contrastar su salida con las tablas de los apartados 4 y 5:
>   ```bash
>   python3 scripts/estructura_predim.py
>   ```
> - Todo valor que no esté en `datos/` es **HIPÓTESIS** (con la norma de referencia citada) o **FALTA DATO**.
> - Al empezar no existían `fases/03_instalaciones.md` ni `fases/03_normativa.md`. Al cerrar este documento ya existían, junto con sus conflictos I-1 a I-9 y N-1 a N-4. **Respondo a los que afectan a estructura en el apartado 6.3.**

---

## 0. Resumen

| Parte | Sistema propuesto | Luz máxima | Forjado / losa | Cimentación (condicionada, sin geotecnia) |
|---|---|---|---|---|
| **24 casas adosadas** (hileras de 8 y de 4) | **Muros de carga de fábrica cerámica de 24 cm en las medianeras** (cada 6,50 m) + forjado unidireccional de viguetas pretensadas en dirección E-O. Fachadas norte y sur no portantes | 6,50 m (a ejes) | **25+5 = 30 cm**, continuo sobre las medianeras (reserva de 35 cm, ver 4.1) | Zapatas corridas bajo medianeras y testeros, atadas por las zapatas o vigas de fachada. **FALTA DATO: estudio geotécnico** |
| **Bloque de 10 pisos** (12,0 × 37,5 m, PB + 2) | **Pórticos de hormigón armado: pilares + losa maciza sin vigas de cuelgue** | 6,25 m (6,0 × 6,25 en la retícula de F2; 5,75 × 6,17 en la retícula ajustada, ver 2.2) | **Losa maciza de 30 cm** (26-28 cm si se justifica la flecha) | Zapatas aisladas atadas, o **losa de cimentación** si σ_adm < ≈ 0,15 MPa. **FALTA DATO: estudio geotécnico** |

- **Junta de dilatación:** **una sola**, en la hilera A-oeste de 8 casas (52 m), entre las viviendas 4 y 5. Todas las demás piezas miden menos de 40 m (CTE DB SE-AE 3.4.1).
- **Sin sótano.** **Forjado sanitario** ventilado en todas las piezas. Fosos de ascensor locales en el bloque.
- **Zona sísmica: FALTA DATO** (NCSE-02; no he podido comprobar la aceleración básica del municipio).
- **Riesgo principal:** se proyecta la cimentación **sin estudio geotécnico**, en contra de lo que exige el CTE DB SE-C (apartado 3). Ver apartado 5 y 7.
- Conflictos nuevos anotados en `fases/conflictos.md`: **E1 a E6** (apartado 8).

---

## 1. Sistema estructural y justificación

### 1.1 Casas adosadas (tipo U-V1: 6,50 × 12,00 m, PB + 1)

**Sistema propuesto: estructura de muros de carga de fábrica + forjados unidireccionales.**

| Elemento | Solución | Justificación |
|---|---|---|
| Muros de medianera (N-S, cada 6,50 m) | **Muro de carga de una hoja de 24 cm** de bloque cerámico aligerado o ladrillo perforado, con trasdosados autoportantes a ambas caras. Es el tipo "hoja única con trasdosados" de DB HR; la solución acústica la debe confirmar normativa | Separa viviendas y a la vez soporta los forjados: un solo elemento cumple estructura, fuego (medianera) y masa acústica. Es la solución más económica para PB + 1 con una tipología repetida 24 veces (F2, 2.6) |
| Testeros (extremos de hilera) | Muro de carga de 24 cm + aislamiento + trasdosado | Igual que la medianera, con la mitad de carga |
| Forjados (sanitario, P1 y cubierta) | **Unidireccional de viguetas pretensadas y bovedilla, 25+5 cm, en dirección E-O**, apoyado en las medianeras, **continuo sobre ellas** con armadura de negativos | Las viguetas van paralelas a las fachadas. Así **las fachadas norte y sur no son portantes** y admiten los huecos grandes del salón (F2) |
| Fachadas norte y sur | Cerramiento de fábrica no portante. En cada forjado lleva un **zuncho de borde de HA** que recoge la hoja de la planta superior (ver 4.1) | Libertad de huecos |
| Encadenados | Zuncho de HA en cada forjado, sobre todos los muros (DB SE-F) | Atado del conjunto y reparto de cargas |
| Escalera | Losa inclinada de HA apoyada en el forjado sanitario y en el brochal de P1. **No se empotra en la medianera** (ruido de impacto, DB HR) | — |
| Arriostramiento E-O | **Hace falta un elemento rígido en dirección E-O en cada vivienda** (ver conflicto E2) | Las medianeras solo arriostran en dirección N-S |

**Alternativa B (pórticos de HA):** pilares de 25 × 25 / 30 × 30 cm en las medianeras (ejes A, B y C) con vigas planas N-S y el mismo forjado E-O. Es más flexible y resuelve sin muros el arriostramiento E-O, porque los pórticos trabajan en las dos direcciones. Es más cara y necesita una medianera acústica aparte. Se recomienda si:
- la NCSE-02 resultara de aplicación con aceleraciones que limiten la fábrica;
- o el arquitecto no acepta el muro arriostrante E-O del conflicto E2.

### 1.2 Bloque multifamiliar M-V1 (12,0 × 37,5 m, PB + 2, 2 portales)

**Sistema propuesto: pórticos de hormigón armado con pilares y losa maciza bidireccional sin vigas de cuelgue.**

| Elemento | Solución | Justificación |
|---|---|---|
| Soportes | Pilares de HA (21 en la retícula 3 × 7) | La retícula casi cuadrada (≈ 6,0 × 6,25 m) es la ideal para una losa bidireccional |
| Forjados P1, P2 y cubierta | **Losa maciza de HA de 30 cm**, sin vigas de cuelgue. Zunchos de borde y brochales de huecos **embebidos en el canto** | Intradós plano: los falsos techos y conductos pasan en cualquier dirección (instalaciones). Pocas piezas y fácil de ejecutar |
| Núcleos (ejes 2-3 y 5-6) | Escalera de losa de HA. Caja de ascensor de fábrica, o de HA de 20 cm si se quiere rigidizar (ver E4) | Los muros de HA del núcleo pueden **absorber los pilares B2, B3, B5 y B6**. Así se evita el punzonamiento en la zona donde van los patinillos |
| Planta baja | Forjado sanitario de viguetas 25+5 sobre vigas de atado o muretes | Sin sótano (decisión del arquitecto). Ver 1.4 |
| Estabilidad horizontal | Pórticos losa-pilar en las dos direcciones (3 plantas). Si la NCSE-02 aplica, los núcleos de HA serán pantallas | Viento moderado (apartado 3) |

**Alternativa:** forjado unidireccional 25+5 en dirección E-O con **vigas planas** N-S de 30 cm de canto en los ejes 1 a 7. Pesa menos (≈ 3,5 frente a 7,5 kN/m²) y alivia la cimentación. A cambio:
- reparte peor las cargas;
- los huecos grandes de patinillos cortan viguetas;
- obliga a llevar los conductos en paralelo a las vigas planas, aunque estas sean de canto igual al forjado y no cuelguen.

### 1.3 Juntas de dilatación

| Pieza | Longitud | ¿Junta? | Criterio |
|---|---|---|---|
| **Hilera A-oeste (8 casas)** | **52,0 m** | **Sí, 1 junta**, en la medianera entre las viviendas 4 y 5 (x ≈ 28,0 en coordenadas locales de F2). Quedan 2 tramos de 26,0 m | CTE DB SE-AE 3.4.1: en edificios de hormigón o acero pueden no considerarse las acciones térmicas si **no hay elementos continuos de más de 40 m** |
| Hilera A-este (4) | 26,0 m | No | < 40 m |
| Banda B, 3 hileras de 4 | 3 × 26,0 m (separadas 6 m) | No | Son edificios independientes |
| Bloque | 37,5 m | No (justo) | < 40 m. Sin margen: si el bloque se alarga, habrá que poner junta |
| Alternativa F2 4 + 4 + 4 (frente de 6,30 m) | 25,2 m | No | Elimina la junta y el conflicto E1 |

**Cómo es la junta:**
- **Doble muro de medianera**, cada hoja portante de su propio forjado: 2 × 24 cm + 3 cm de junta con relleno compresible y sellado en fachada y cubierta, es decir, ≈ 0,51 m frente a los 0,24 m de una medianera normal. **Afecta al diseño (conflicto E1).**
- La junta de dilatación **no corta la cimentación**: zapata corrida común para los dos muros (4.3).
- Si el reconocimiento del terreno detectara heterogeneidad o rellenos, se convertiría en **junta de asiento** y se cortaría también la zapata.

**Juntas de movimiento de la fábrica de fachada.** Son distintas de la junta estructural. Las fachadas norte y sur son paños de fábrica continuos de 26-52 m. CTE DB SE-F, apartado 2.2 (tabla 2.1): la distancia máxima entre juntas de movimiento de la fábrica cerámica depende de la retracción del mortero y de la expansión por humedad de la pieza, y está entre ≈ 8 y 30 m. **Propuesta:** hacerlas coincidir con las medianeras, cada 2 viviendas (13 m) o cada 3 (19,5 m), según el ladrillo que se elija (**FALTA DATO: características de la pieza**).

### 1.4 Forjado sanitario y sótano

- **Sótano: no hay** (decisión del arquitecto, F1). No se proyectan muros de contención. Si la topografía (FALTA DATO) da desniveles importantes, puede que hagan falta muros de contención o de sótano parcial (riesgo R7).
- **Forjado sanitario en todas las piezas.** Es la solución que se recomienda **sin geotecnia**: no apoya en el terreno, así que no le afectan ni la expansividad ni los asientos de rellenos bajo la solera. Además ventila la cámara (CTE DB HS 1, suelos, y DB HS 6, radón; la zona de radón del municipio la debe comprobar normativa).
  - Casas: viguetas 25+5 de medianera a medianera (luz 6,50 m), apoyadas en muretes sobre las zapatas corridas.
  - Bloque: viguetas 25+5 apoyadas en muretes sobre las vigas de atado y las zapatas.
  - **Cámara libre ≥ 0,35 m.** Si el saneamiento va colgado y registrable dentro de la cámara, **≥ 0,45-0,50 m**.
- **Conflicto de cotas (E3).** Con la PB a +0,30 sobre la rasante (H-ALT de F2), la cámara queda **bajo rasante**. Hay dos opciones:
  - ventilarla con **conductos o periscopios** hasta rejillas en el zócalo. Hay que excavar ≈ 0,5-0,7 m en toda la huella y drenar. Es arriesgado si el nivel freático está alto (FALTA DATO);
  - ventilarla con rejillas directas en el zócalo. Entonces la PB sube a **≈ +0,60-0,70 m**, y la cornisa del bloque pasaría de 10 m (ver E3).
- **Solera sobre el terreno con cámara de cúpulas de plástico** (tipo "caviti"): **no se recomienda sin geotecnia**, porque apoya en el terreno. Solo se admitiría si el estudio descarta la expansividad y los rellenos.

---

## 2. Retícula y luces

Coordenadas locales de F2 (origen en el vértice 3, x hacia el este, y hacia el norte).

### 2.1 Casas

| Concepto | Valor | Nota |
|---|---|---|
| Ejes de medianera (N-S) | Cada **6,50 m** | Hilera A-oeste: ejes 1 a 9 en x = 2,0 / 8,5 / 15,0 / 21,5 / **28,0 (junta)** / 34,5 / 41,0 / 47,5 / 54,0. Las demás hileras, igual cada 6,50 m desde su testero oeste |
| Criterio de cotas | 6,50 m **entre ejes de medianera**. En testeros y fachadas, 6,50 y 12,00 m son **caras exteriores** | Coherente con 78 m² construidos por planta (F2). La estructura queda **dentro** de la envolvente de F2 |
| Ejes longitudinales | A = fachada sur (banda A: y = 9,0), C = fachada norte (banda A: y = 21,0) y B intermedio (y ≈ 15) **sin muro portante**, solo zunchos de escalera y el muro arriostrante de E2. Banda B: A = y 37,0 y C = y 49,0 (simétrica: entrada al sur) | — |
| **Luz máxima de forjado** | **6,50 m** a ejes (luz libre ≈ 6,26 m) | Viviendas de extremo: algo menos (testero de 24 cm + aislamiento dentro de la envolvente) |
| Luz de los zunchos de borde de fachada | 6,50 m (de medianera a medianera) | Recogen la hoja de fábrica de la planta superior |
| Voladizos | **No previstos** en F2 | Si se quisieran vuelos en las fachadas norte o sur, como el forjado es paralelo a ellas, harían falta una losa en vuelo anclada o un cambio de dirección del forjado. Máximo recomendado ≈ 1,0 m. Computarían m²c (H-COM) |
| Alternativa 4 + 4 + 4 (F2 2.7) | Luz de 6,30 m | Canto mínimo algo menor. Sin junta |

### 2.2 Bloque

| Concepto | Retícula F2 (nominal) | **Retícula ajustada propuesta** | Nota |
|---|---|---|---|
| Ejes longitudinales A (sur) – B – C (norte) | 2 crujías de 6,00 m (y = 61,0 / 67,0 / 73,0) | **2 × 5,75 m** (ejes de fachada a 0,25 m por dentro de la cara exterior) | Si los ejes de los pilares de fachada coincidieran con la envolvente de 12,00 × 37,50 m, el cerramiento pasaría por fuera y la planta crecería ≈ 0,3 m por lado: **≈ +30 m² por planta y ≈ +90 m²c en total**. El margen de V1 es de solo 6 m²c (5.094 / 5.100). **La envolvente exterior de F2 se mantiene; los ejes se ajustan hacia dentro** |
| Ejes transversales 1 a 7 | 6 vanos de 6,25 m (x = 19,5 … 57,0) | **6 vanos de ≈ 6,17 m** (37,00 m entre ejes extremos) | Ídem |
| Luces de cálculo del predimensionado | **6,00 × 6,25 m** | — | Se calcula con la retícula nominal, que queda del lado de la seguridad |
| Núcleos | Entre los ejes 2-3 (portal 1) y 5-6 (portal 2) | Ídem | Pilares B2, B3, B5 y B6 junto al núcleo (ver E4) |
| Pilares | 21 (3 × 7) | Ídem | 5 interiores (B2-B6), 10 de fachada larga (A2-A6, C2-C6), 2 de testero (B1, B7) y 4 de esquina |
| Voladizos | **No previstos** | — | Si se quieren terrazas voladas: losa en vuelo ≤ 1,50 m (L/d ≤ 8, tabla 50.2.2.1.a). Computan m²c |

---

## 3. Acciones (CTE DB SE-AE) — hipótesis declaradas

### 3.1 Cargas permanentes (características)

| Concepto | Valor | Referencia / hipótesis |
|---|---|---|
| Forjado unidireccional 25+5, viguetas pretensadas | **3,5 kN/m²** | DB SE-AE Anejo C, tabla C.5 (3,0 kN/m² para canto ≤ 0,28 m). Se sube por el canto de 30 cm y la luz de 6,5 m. **Hipótesis**; el valor real lo da la ficha del fabricante |
| Losa maciza de HA de 30 cm | **7,5 kN/m²** | 25 kN/m³ × 0,30 (DB SE-AE tabla C.1) |
| Pavimento + recrecido, o suelo radiante (≤ 0,10 m) | **1,5 kN/m²** | Tabla C.5 (1,0 para un pavimento < 0,08 m). Se sube por un posible suelo radiante (aerotermia), que es **hipótesis pendiente de instalaciones** |
| Tabiquería | **1,0 kN/m²** | DB SE-AE 2.1 (viviendas) |
| Falso techo + instalaciones colgadas | 0,2 kN/m² | Hipótesis |
| Cubierta plana invertida con grava (pendientes, impermeabilización, aislamiento y grava) | **2,5 kN/m²** | Tabla C.5 |
| Cerramiento de fachada (fábrica + aislamiento + trasdosado) | **8,0 kN/m** por planta (≈ 3,0 kN/m² × 2,70 m) | Hipótesis |
| Peto de cubierta | 3,0 kN/m | Hipótesis |
| Fábrica de medianera de 24 cm | 15 kN/m³ → 3,6 kN/m², + 0,3 kN/m² por trasdosado | Tabla C.1 (ladrillo perforado). Con bloque aligerado sería menos |

### 3.2 Acciones variables

| Acción | Valor | Referencia / hipótesis |
|---|---|---|
| Uso en viviendas (A1) | **2,0 kN/m²** / 2 kN concentrada | DB SE-AE tabla 3.1 |
| Zonas comunes del bloque (portal, escalera, rellanos) | **3,0 kN/m²** | Tabla 3.1: en la categoría A se suma 1 kN/m² en los accesos y zonas de evacuación |
| Balcones volados (si los hubiera) | Uso de la zona contigua + 2 kN/m en el borde | DB SE-AE 3.1.1 |
| Cubierta solo accesible para conservación (G1, < 20°) | **1,0 kN/m²**, no concomitante con otras variables | Tabla 3.1. Si la cubierta del bloque es transitable privada (F): 1,0 kN/m² más el solado |
| Zona de equipos en cubierta (aerotermia, ACS) | **Hipótesis: 3,0 kN/m²** en una bancada, o el peso real del equipo | **Pendiente de instalaciones** |
| **Nieve** | q_n = μ · s_k con μ = 1 (cubierta plana, DB SE-AE 3.5.3). **s_k: FALTA DATO**, porque depende de la altitud (sin topografía) y de la zona climática de invierno (Anejo E, figura E.2 y tabla E.2). **Hipótesis provisional: s_k = 0,6 kN/m²**, valor de la tabla 3.8 para Madrid capital (660 m), **por confirmar** con la altitud real | En cubierta plana manda la G1 (1,0 kN/m²) mientras s_k ≤ 1,0 kN/m², así que la hipótesis no condiciona el predimensionado |
| **Viento** | q_e = q_b · c_e · c_p. **q_b = 0,5 kN/m²**, el valor simplificado que admite DB SE-AE 3.3.2 para todo el territorio, conservador; no se fija la zona del Anejo D. **Grado de aspereza III** (hipótesis conservadora: parcela en el borde, frente a la ZV-02 y la Avda. de la Dehesa). c_e (tabla 3.4): ≈ 2,1 en las casas (z ≈ 7 m) y ≈ 2,4 en el bloque (z ≈ 10 m). c_p + \|c_s\| (tabla 3.5): ≈ 1,1 en las casas (esbeltez ≈ 0,55) y ≈ 1,3 en el bloque (≈ 0,8) | **q_e global ≈ 1,2 kN/m² (casas) y ≈ 1,6 kN/m² (bloque)**. Bloque, viento N-S: ≈ 1,6 × 37,5 × 9,7 ≈ 580 kN en total, que absorben 7 pórticos |
| Acciones térmicas | No se consideran **si hay juntas cada ≤ 40 m** | DB SE-AE 3.4.1 (apartado 1.3) |
| Impacto de vehículos | Las plazas en batería llegan a la fachada de entrada de las casas (bandas A y B). Sin protección, DB SE-AE 4.3.2 obliga a una fuerza estática equivalente de 50 kN sobre los elementos expuestos | **Se propone poner topes de rueda** y no calcular el impacto (conflicto E6) |

### 3.3 Sismo

- **Norma:** NCSE-02 (RD 997/2002). Las viviendas son construcciones de **importancia normal**.
- **Aceleración sísmica básica a_b de Villanueva de la Cañada: FALTA DATO.** No he podido comprobarla en el mapa (figura 2.1) ni en el Anejo 1 de la NCSE-02. No se supone.
  - Si a_b < 0,04 g, la norma **no es de aplicación obligatoria** a construcciones de importancia normal (art. 1.2.3).
  - Si a_b ≥ 0,04 g, se aplica: acero B500SD, detalles de ductilidad, comprobación de la fábrica portante y del sistema losa-pilar (ductilidad baja), y vigas de atado de la cimentación.
- **Se pide a normativa o al arquitecto que lo confirme.**

### 3.4 Combinaciones y límites

- **ELU** (DB SE 4.2.2, situación persistente): γ_G = 1,35 y γ_Q = 1,50.
- **ELS:**
  - flecha relativa activa ≤ 1/500 con tabiques frágiles o sobre fábrica de fachada, 1/400 con tabiques ordinarios y 1/300 en el resto (DB SE 4.3.3.1);
  - desplome ≤ 1/500 de la altura total y ≤ 1/250 de la planta.
- **Resistencia al fuego (orientativa; la confirma normativa):** DB SI 6, tabla 3.1. Vivienda unifamiliar R 30. Residencial vivienda con altura de evacuación ≤ 15 m (bloque) R 60. Los recubrimientos y dimensiones mínimas de la losa de 30 cm y los pilares de ≥ 30 cm son compatibles con R 60 (DB SI Anejo C; comprobar).
- **Materiales (hipótesis):**
  - HA-25, en elementos interiores (XC1) y en cimentación (XC2), si el terreno no es agresivo. **Agresividad química (XA): FALTA DATO**; si existe, HA-30 o superior y cemento resistente a sulfatos (Código Estructural, clases de exposición);
  - acero B500S, o B500SD si aplica la NCSE-02;
  - fábrica portante: pieza cerámica con f_b ≥ 10-15 N/mm², mortero M7,5 y f_k ≥ 4 N/mm² (DB SE-F, tabla 4.4; hipótesis por confirmar con el fabricante).

---

## 4. Predimensionado

> **Este predimensionado se obtiene con reglas habituales y NO sustituye al cálculo.** Comando de comprobación: `python3 scripts/estructura_predim.py` (sin ejecutar; ver el aviso inicial).

### 4.1 Casas adosadas

**Cargas totales características (permanentes + variables):**
- P1: 3,5 + 1,5 + 1,0 + 0,2 + 2,0 = **8,2 kN/m²**;
- cubierta: 3,5 + 2,5 + 0,2 + 1,0 = **7,2 kN/m²**;
- forjado sanitario: 3,5 + 1,5 + 1,0 + 2,0 = **8,0 kN/m²**.

**Canto mínimo de forjado sin comprobar flecha** (Código Estructural, art. 50.2.2.1, que reproduce el criterio de la EHE-08): h_min = δ1 · δ2 · L / C, con δ1 = √(q/7) = 1,082 y δ2 = (L/6)^¼ = 1,020, L = 6,50 m. Para viguetas pretensadas con tabiquería, los valores de C que manejo son 19 (tramo aislado), 23 (extremo) y 26 (interior). **Hay que verificarlos en la tabla 50.2.2.1.b vigente.**

| Situación del vano | C | h_min |
|---|---|---|
| Tramo aislado (forjado interrumpido en cada medianera) | 19 | 0,378 m |
| Tramo extremo (vivienda junto al testero o a la junta) | 23 | 0,312 m |
| Tramo interior (forjado continuo en las dos medianeras) | 26 | 0,276 m |

| Elemento | Dimensión propuesta | Criterio |
|---|---|---|
| **Forjados P1, cubierta y sanitario** | **Unidireccional 25+5 = 30 cm**, intereje 70 cm, **continuo sobre las medianeras** | Cumple la esbeltez en los vanos interiores (0,276 m). En los **vanos extremos** (0,312 m) hay que **calcular la flecha explícitamente** (DB SE 4.3.3), o subir esos vanos o toda la hilera a **30+5 = 35 cm**. **Si la medianera fuera doble** por acústica, con el forjado interrumpido (tramos aislados, 0,378 m): **35 cm con cálculo de flecha**, o **losa alveolar pretensada** de 20-25 cm + capa de compresión según las tablas del fabricante |
| **Muro de medianera** | **24 cm** de fábrica cerámica portante, h ≈ 2,70 m por planta | Esbeltez h/t = 2,70 / 0,24 ≈ 11 ≤ 27 (DB SE-F). N_d en la base de PB ≈ **169 kN/m → σ_d ≈ 0,70 N/mm²**. Con f_k ≥ 4 N/mm², γ_M ≈ 2,5 y un factor de reducción por excentricidad y esbeltez de ≈ 0,6-0,7, la capacidad es ≈ 1,0-1,1 N/mm². **Margen ≈ 1,4-1,6** |
| Muro de testero | 24 cm (+ aislamiento + trasdosado) | La mitad de la carga de la medianera |
| Junta de dilatación (eje 5 de la hilera A-oeste) | **2 × 24 cm + 3 cm ≈ 0,51 m** | Ver 1.3 y E1 |
| **Muro arriostrante E-O** (uno por vivienda y planta) | Fábrica de 24 cm (o de 14 cm portante si basta), **longitud ≥ 2,5 m**, en el eje B, junto a la escalera | Rigidez longitudinal de la hilera (viento sobre los testeros, sismo si aplica). **Conflicto E2** |
| Encadenado sobre los muros | Zuncho de HA de 24 × 30 cm (ancho del muro × canto del forjado), 4 Ø12 + estribos | DB SE-F |
| **Zuncho de borde de fachada** (norte y sur, luz 6,50 m, recoge 8 kN/m de fábrica) | **Viga plana de 40 × 30 cm**, embebida en el forjado; o **dintel descolgado de 25 × 40-45 cm** sobre los huecos grandes | M_d ≈ 1,35 × 8 × 6,5² / 8 ≈ 57 kN·m, resistente con 30 × 30. Lo que manda es la **flecha activa ≤ 1/500** (fábrica frágil encima). Hay que coordinarlo con los capialzados de persiana (diseño) |
| Brochales y zunchos del hueco de escalera (≈ 1,0 × 4,6 m, a definir por diseño) | Vigas planas embebidas de 40 × 30 cm | Luz ≤ 5 m |
| Escalera | Losa inclinada de HA de **20 cm** (proyección ≈ 4,5 m y desarrollo ≈ 5,4 m, L/25-L/27) | Apoyada en el forjado sanitario y el brochal de P1 |
| Cargaderos de huecos ≤ 3 m | Cargadero prefabricado o de HA de 20-25 cm de canto | — |

**Alturas libres resultantes (casas),** con el suelo radiante de 0,12 m de instalaciones (H-I9):
- altura de planta 3,00 m (H-ALT de F2) − forjado 0,30 − suelo radiante 0,12 ≈ **2,58 m**;
- bajo falso techo de 0,25 m (baños, distribuidor): ≈ **2,33 m**;
- con forjado de 35 cm: **2,53 m** y 2,28 m.

Con ≤ 0,35 m se respeta el límite que pide instalaciones (I-5). La altura libre mínima exigible es FALTA DATO (normativa).

> Sensibilidad: si el suelo radiante con su mortero pesa ≈ 1,8 kN/m² en lugar de 1,5, las cargas suben ≈ 3-4 %. Las dimensiones de este apartado y del 5 no cambian, salvo redondeos de +0,05 m en alguna zapata.

### 4.2 Bloque multifamiliar

**Cargas totales características:**
- planta tipo: 7,5 + 1,5 + 1,0 + 0,2 + 2,0 = **12,2 kN/m²**;
- cubierta: 7,5 + 2,5 + 0,2 + 1,0 = **11,2 kN/m²**;
- forjado sanitario: **8,0 kN/m²**.

En los pilares del eje B, segundo apoyo de dos vanos continuos, se aplica un **coeficiente de continuidad de 1,2** (hipótesis).

| Elemento | Dimensión propuesta | Criterio |
|---|---|---|
| **Losa de P1, P2 y cubierta** | **Losa maciza de 30 cm** (d ≈ 0,25 m) | Código Estructural, tabla 50.2.2.1.a, placa sin vigas (K = 1,2), L/d = 24 con ρ = 0,5 %: d ≥ 6,25 / 24 = 0,26 m → **h ≈ 0,30 m sin comprobar la flecha**. Con cálculo de flecha podría bajar a **26-28 cm** (lo que alivia el conflicto E3) |
| **Pilar interior B2-B6** (A_trib = 6,0 × 6,25 = 37,5 m²) | **40 × 40 cm** | N_d ≈ **2.245 kN**. A_c ≥ N_d / [0,8 · (0,85 · f_cd + ρ · f_yd)] = 2.245 kN / 14,5 MPa ≈ 1.545 cm², es decir, ≈ 39 × 39 cm |
| **Punzonamiento en el pilar interior** | **Necesita armadura de punzonamiento** (horquillas o conectores), o capitel, o un pilar integrado en pantalla del núcleo | Código Estructural, art. 46: V_d ≈ 755 kN por planta, u_1 = 4 · 0,40 + 4π · 0,25 = 4,74 m y τ_sd = 1,15 · V_d / (u_1 · d) ≈ **0,73 MPa** > τ_rd ≈ **0,65 MPa** (ρ = 0,8 %, HA-25). **Zona sin huecos alrededor del pilar: 6d ≈ 1,50 m desde su cara** (ver 6.2 y E4) |
| Pilar de fachada larga A2-A6, C2-C6 (18,75 m² + fachada) | **30 × 40 cm**, con el lado de 40 perpendicular a la fachada | N_d ≈ 1.112 kN, A_c mínima ≈ 28 × 28 cm. Se amplía por los momentos de borde y el punzonamiento excéntrico (β ≈ 1,4) |
| Pilar de testero B1, B7 | **30 × 40 cm** | N_d ≈ 1.289 kN (≈ 30 × 30 estricto) |
| Pilar de esquina | **30 × 30 cm** | N_d ≈ 642 kN. Mínimo constructivo de 25 cm (Código Estructural) y 30 cm por fuego y por los momentos de esquina |
| Zunchos de borde en fachada | 30 × 30 cm, embebidos | Recogen el cerramiento (8 kN/m) entre pilares (≈ 6,2 m) |
| Brochales de los huecos de escalera y ascensor | Vigas planas embebidas de 40-50 × 30 cm | Sin cuelgue |
| Losa de escalera | **18 cm** (tramos de ≈ 3,5-4 m, L/22-L/25) | — |
| Caja de ascensor (opcional, estructural) | Muros de HA de **20 cm** | Integran los pilares B2/B3 y B5/B6. Ver E4 |
| Forjado sanitario de PB | Unidireccional 25+5 = 30 cm sobre muretes o vigas de atado (luz ≤ 6,25 m) | Igual que en las casas |

**Alturas libres (bloque):**
- 3,00 − 0,30 − 0,12 ≈ **2,58 m**;
- bajo falso techo de 0,30 m, con el colectivo Ø200 en zonas de paso: ≈ **2,28 m**.

Instalaciones calculó con 0,28 m. Con losa de 28 cm y cálculo de flecha, se recuperan esos 2 cm.

**Resistencia al fuego** (normativa, SI 6): R 30 en las casas, R 60 en el bloque y **REI 90 en el forjado sobre los cuartos de contadores y de basuras**. Con la losa de 30 cm y los pilares de ≥ 30 cm se alcanza R 90 con recubrimientos adecuados (DB SI Anejo C, a comprobar en proyecto). En las casas: forjado de 30 cm con revestimiento inferior y fábrica de 24 cm, ≥ R 30 y ≥ EI 120.

**Cornisa:** ver E3. Con PB a +0,30 m y el paquete de cubierta más el peto (≈ 0,50-0,65 m sobre la losa), el peto queda a **≈ +9,75-9,85 m**. El límite es 10 m y el criterio de medición es FALTA DATO.

---

## 5. Cimentación orientativa (CTE DB SE-C)

### 5.1 Situación de partida

**FALTA DATO: estudio geotécnico.** Es una decisión del arquitecto (F1, PAUSA): no se encarga. Tampoco hay topografía.

**Riesgo frente a DB SE-C:**
- El **CTE DB SE-C, apartado 3**, establece el estudio geotécnico como base obligada del proyecto de cimentación. La Parte I del CTE (Anejo I, contenido del proyecto) lo incluye en la documentación del proyecto.
- Sin él **no se puede fijar la tensión admisible, el asiento, el nivel freático, la agresividad, la expansividad ni la profundidad del firme**. La cimentación de este documento es solo un **abanico de alternativas condicionadas**.
- **En la práctica, además, es necesario para el seguro decenal (LOE, art. 19) y para el control técnico (OCT).** Sin estudio, previsiblemente no se podrá contratar el seguro de una promoción de viviendas.
- **Recomiendo encarecidamente reconsiderar la decisión.**

**Clasificación según DB SE-C, tabla 3.1** (lo que sí se puede decir sin terreno):
- **Tipo de construcción C-1**: menos de 4 plantas y más de 300 m² construidos por pieza. Hilera A-oeste ≈ 1.248 m², hileras de 4 ≈ 624 m² y bloque 1.350 m².
- **Grupo de terreno (T-1 / T-2 / T-3): FALTA DATO.**
- Campaña mínima orientativa, para cuando se encargue (DB SE-C, tablas 3.3 y 3.4; la define el geotécnico):
  - distancia máxima entre puntos d_max ≈ 30-35 m;
  - profundidad orientativa de 6 m (T-1) a 18 m (T-2);
  - **mínimo de 3 puntos**. Sobre el trazado de V1 (banda A de 84 m, banda B de 90 m y bloque de 37,5 m) calculo **del orden de 7-9 puntos**, combinando sondeos y penetrómetros dinámicos. Es una estimación propia;
  - ensayos: identificación, **expansividad** (Lambe e hinchamiento), **sulfatos y agresividad** al hormigón, **nivel freático**, y resistencia y deformabilidad.
- En la Comunidad de Madrid hay formaciones con arcillas expansivas o con yesos. **No supongo que existan en esta parcela**: el estudio debe descartarlas o confirmarlas.

### 5.2 Tensión admisible

**σ_adm: FALTA DATO.** Para dar órdenes de magnitud se usan **tres escenarios de hipótesis**, sin adoptar ninguno: **0,10 / 0,20 / 0,30 MPa**. El **escenario base del predimensionado, 0,20 MPa, es HIPÓTESIS NO VERIFICADA**.

- **Profundidad mínima de apoyo:** hipótesis de **≥ 0,80 m bajo la rasante final**, por helada y zona activa, **y siempre en terreno natural**, por debajo de rellenos o tierra vegetal.
- **Cota de firme: FALTA DATO.**

### 5.3 Casas: zapatas corridas bajo medianeras y testeros

N_k por metro lineal: cubierta + P1 + forjado sanitario + muro, **+10 % de peso propio de zapata y tierras**. B es el ancho de la zapata y h el canto de zapata rígida (vuelo ≤ 2h, mínimo 0,40 m).

| Elemento | N_k (kN/m) | σ = 0,10 MPa: B / h | **σ = 0,20 MPa: B / h** | σ = 0,30 MPa: B / h |
|---|---|---|---|---|
| Medianera interior (tributario 6,50 m) | 194,6 | 1,95 / 0,45 | **1,00 / 0,40** | 0,65 / 0,40 |
| Testero / extremo de hilera (tributario 3,25 m) | 111,0 | 1,15 / 0,40 | **0,60 / 0,40** | 0,60 / 0,40 (mínimo) |
| Junta (dos muros, zapata común) | 222,0 | 2,25 / 0,45 | **1,15 / 0,40** | 0,90 / 0,40 (mínimo) |
| Fachadas N y S (no portantes) | ≈ 20-25 | — | **Zapata corrida o viga de atado de 0,50 × 0,40 m**, que ata las zapatas de medianera | — |

- **Alternativa con σ ≤ 0,10 MPa o terreno heterogéneo:** **losa de cimentación por hilera** (o por tramo de junta) de **35-40 cm**. La presión media es ≈ 0,04 MPa: ≈ 2.330 kN por vivienda sobre 78 m², más la propia losa.
- **Alternativa con firme profundo** (rellenos de más de 2-3 m): **pozos de cimentación** de hormigón en masa bajo las zapatas, hasta el firme.
- **Alternativa con arcillas expansivas:** apoyo por debajo de la zona activa (pozos o micropilotes) con vigas de atado separadas del terreno y forjado sanitario (que ya está previsto). **Nunca solera.**

### 5.4 Bloque: zapatas aisladas atadas, o losa

N_k a cimentación, con forjado sanitario y fachada de PB, **+10 %**. Zapata cuadrada de lado B; canto rígido h.

| Pilar | N_k a zapata (kN) | σ = 0,10 MPa: B / h | **σ = 0,20 MPa: B / h** | σ = 0,30 MPa: B / h |
|---|---|---|---|---|
| Interior B2-B6 (×5) | 1.938 (2.132 con el +10 %) | 4,65 / 1,10 ⚠ | **3,30 / 0,75** | 2,70 / 0,60 |
| Fachada larga A2-A6, C2-C6 (×10) | 1.013 (1.115) | 3,35 / 0,80 | **2,40 / 0,55** | 1,95 / 0,45 |
| Testero B1, B7 (×2) | 1.140 (1.254) | 3,55 / 0,85 | **2,55 / 0,60** | 2,05 / 0,45 |
| Esquina (×4) | 594 (654) | 2,60 / 0,60 | **1,85 / 0,40** | 1,50 / 0,40 |

- **Vigas de atado** entre todas las zapatas, de **40 × 50 cm** como orientación. Sirven también de apoyo de los muretes del forjado sanitario.
- **Con σ = 0,10 MPa las zapatas interiores (4,65 m) casi se tocan con las de fachada** (ejes a 6,0 m): **no es viable con zapatas aisladas → losa de cimentación.**
- **Losa de cimentación:** 13,0 × 38,5 m (0,5 m de vuelo), **60-70 cm de canto** (punzonamiento de los pilares interiores). **Presión media ≈ 0,065 MPa** (N_k total ≈ 24.500 kN). Es la solución recomendable si σ_adm < ≈ 0,15 MPa, si hay asientos diferenciales significativos o si el terreno es heterogéneo.
- **Fosos de ascensor (2):** profundidad ≈ 1,0-1,2 m bajo PB (**FALTA DATO: modelo de ascensor**). Losa de foso de 30 cm y muros de 20-25 cm de HA, impermeabilizados. **Si el nivel freático está alto (FALTA DATO), hay riesgo de entrada de agua.** Se integran en una zapata combinada con los pilares del núcleo, o en la losa.

---

## 6. Huecos y pasos reservados para instalaciones

### 6.1 Casas

| Código | Paso | Dimensión y posición | Condición estructural |
|---|---|---|---|
| **H-U1 (= PU de instalaciones)** | Patinillo vertical por vivienda. F2 lo daba de 0,60 × 0,40 m; **instalaciones propone 0,80 × 0,40 m** (I-1), en la crujía de la calle, junto a la medianera opuesta a la escalera | **0,80 m en E-O (perpendicular a la medianera, paralelo a las viguetas) × 0,40 m en N-S** (máximo 0,50 m), separado **≥ 0,10 m** de la cara del muro (zuncho de apoyo). Alineado en vertical en el forjado sanitario, P1 y cubierta | **Cabe entre dos viguetas sin cortarlas** (intereje de 70 cm, hueco libre ≈ 0,58 m) **siempre que la dimensión N-S sea ≤ 0,50 m**. Basta con quitar bovedillas y reforzar con armadura de borde la capa de compresión y los negativos de esa franja. **No hace falta brochal** (responde a I-2). Si se gira el patinillo, con 0,80 m en N-S, se corta una vigueta y hace falta brochal (E5). El replanteo de las viguetas se fija en la tipología, que es la misma en las 24 casas |
| H-U2 | Hueco de escalera (≈ 1,0 × 4,6 m, a definir por diseño) | Junto a la medianera | Brochales y zunchos embebidos (4.1) |
| H-U3 | Pasatubos sueltos en el forjado (Ø ≤ 125 mm) | En la zona de bovedilla | **No cortar viguetas** ni perforar el zuncho de apoyo |
| H-U4 | Pasos horizontales | **No se perforan las medianeras portantes** (estructura, fuego y acústica). Por los zunchos de fachada: pasatubos de Ø ≤ 1/3 del canto, en el centro del canto y previstos en los planos | — |
| H-U5 | Cámara sanitaria | Saneamiento colgado o enterrado bajo la cámara. Las **acometidas entran por el murete o la viga de fachada del lado de la calle**, con pasatubos previstos, **nunca a través de las zapatas** | Altura de la cámara: ver E3 |
| H-U6 | Cubierta | Salidas de ventilación HS 3 y líneas de aerotermia por el patinillo H-U1. Si la unidad exterior va en cubierta, **bancada sobre el muro de medianera o cerca de él** | Carga del equipo, pendiente de instalaciones |
| — | Vigas de cuelgue | **No hay**: el forjado apoya en muros. El falso techo queda libre en las dos direcciones. Únicos descuelgues posibles: los dinteles de fachada de 40-45 cm sobre los huecos grandes (4.1) | — |

### 6.2 Bloque

| Código | Paso | Dimensión y posición | Condición estructural |
|---|---|---|---|
| **H-M1 (= PB-1 a PB-4 de instalaciones)** | Patinillos: **4 de 1,00 × 0,60 m**, uno a cada lado de cada núcleo (ejes 2-3 y 5-6), junto al rellano | **Opción recomendada:** pilares B2, B3, B5 y B6 **integrados en pantallas de HA del núcleo** (muros de 20-25 cm), con los patinillos adosados a las pantallas. **Si los pilares quedan exentos**, los patinillos deben estar **a ≥ 1,50 m (6d) de la cara de cualquier pilar**. Alineados en vertical | Huecos de 1,00 m: armadura de refuerzo en los bordes y zuncho embebido en el lado largo. **Uno a cada lado del núcleo significa, previsiblemente, sobre los ejes 2 y 3**, justo en la línea de los pilares B2 y B3: dentro de la zona de 6d **invalidan el perímetro crítico de punzonamiento** de una losa que ya necesita armadura de punzonamiento (4.2). Ver E4 (responde a I-3) |
| H-M2 | Hueco y foso de ascensor | ≈ 1,7 × 1,8 m por núcleo (**FALTA DATO: modelo**). Foso ≈ 1,0-1,2 m | Brochales embebidos. Foso en la cimentación (5.4) |
| H-M3 | Hueco de escalera | ≈ 2,5 × 5,0 m por núcleo (a definir por diseño) | Brochales embebidos |
| H-M4 | Pasatubos sueltos | Ø ≤ 160 mm o ≤ 0,30 × 0,30 m: **libres fuera de la banda de soportes** y fuera de la zona de 6d. Entre 0,30 y 1,0 m: con armadura de refuerzo en los bordes y aprobación de estructura. Más de 1,0 m: con zunchos | Los grupos de pasatubos alineados cuentan como un solo hueco |
| — | Vigas de cuelgue | **Ninguna** (losa con zunchos embebidos). Falso techo libre en todas las direcciones | — |
| H-M5 | Cuarto de contadores e instalaciones en PB (F2: 8 m²) y acometidas | Sobre el forjado sanitario. Pasatubos en los muretes o vigas de atado, **no en las zapatas** | — |
| H-M6 | Cubierta: bancada de equipos (ACS, aerotermia) | **Sobre pilares o junto a ellos.** Carga de hipótesis de 3,0 kN/m² (3.2), o el peso real del equipo | Castillete sobre la cubierta: pendiente de normativa (H-CUB). Si se construye, carga adicional sobre la losa y los pilares del núcleo |

### 6.3 Respuesta a los conflictos de instalaciones y normativa que afectan a estructura

| Conflicto | Respuesta de estructura |
|---|---|
| **I-1 / I-2** (patinillo PU de 0,80 × 0,40 m en las casas) | **Compatible sin brochal** si el lado de 0,80 m va en E-O (paralelo a las viguetas) y el de 0,40 m en N-S (H-U1). Se acepta la posición junto a la medianera opuesta a la escalera. Así el hueco de escalera y el patinillo quedan en vanos de vigueta distintos. Solo si se gira el patinillo hace falta brochal (E5) |
| **I-3 / N-4** (patinillos PB-1 a PB-4 junto a los núcleos) | Propuesta: **integrar los pilares B2, B3, B5 y B6 en pantallas de HA del núcleo**, o separar los patinillos ≥ 1,50 m de las caras de pilar (E4). Los registros y el sellado EI de N-4 no afectan a la estructura |
| **I-4** (colectores enterrados frente a zapatas y riostras) | **Los colectores no atraviesan zapatas.** Los cruces con vigas de atado y muretes se hacen con **pasatubos previstos en los planos**, de Ø ≤ 1/3 del canto, a media altura. En las casas, el colector de cada vivienda sale por la fachada de la calle: **cruza solo la viga o zapata de fachada** (0,50 × 0,40 m), no las zapatas de medianera. Las arquetas a pie de bajante van fuera de la huella de las zapatas. Hay que bajar la cara superior de la cimentación por debajo de la cota de los colectores (topografía: FALTA DATO) |
| **I-5** (alturas libres) | Forjado de las casas de **30 cm** (35 cm como máximo, solo si la flecha no cumple o si la medianera es doble). Losa del bloque de **30 cm**, que se puede reducir a 26-28 cm con cálculo de flecha. Alturas libres en 4.1 y 4.2 |
| **I-6** (equipos en cubierta) | Bancadas de equipos **sobre las medianeras** (casas) o **sobre los pilares o junto a ellos** (bloque). Carga de hipótesis de 3,0 kN/m², o el peso real del equipo (H-U6 y H-M6) |
| **N-3** (medianera de carga única frente a DB HR y DB SI) | La solución base de estructura es la que propone normativa como primera opción: **hoja única portante de 24 cm de masa elevada con trasdosados** y forjado continuo (4.1). **EI 120** con fábrica cerámica de 24 cm: se alcanza (DB SI Anejo F, a comprobar con la pieza elegida). Si la justificación de DB HR obliga a una **doble hoja con forjados independientes**: los vanos pasan a "tramo aislado" y el forjado sube a **35 cm** con cálculo de flecha, o se usa losa alveolar. La altura libre queda en 2,53 m (I-5: cumple por 3 cm). La doble hoja también resolvería de forma natural la junta de E1. **Decide el arquitecto, con normativa** |

---

## 7. Riesgos y datos que faltan

### 7.1 FALTA DATO

| # | Dato | Afecta a | Quién lo aporta |
|---|---|---|---|
| D1 | **Estudio geotécnico** (σ_adm, asientos, cota de firme, expansividad, agresividad, nivel freático) | Toda la cimentación, el forjado sanitario y los fosos de ascensor | Arquitecto o laboratorio. **Decisión actual: no se encarga** |
| D2 | **Topografía** (cotas, rasantes de las calles, desniveles) | Cota de PB, cornisa, muros de contención, profundidad de la cimentación y altitud (nieve) | Arquitecto o topógrafo |
| D3 | **Aceleración sísmica básica a_b** (NCSE-02, Anejo 1 / figura 2.1) | Aplicación de la NCSE-02, fábrica portante, ductilidad y atado | Normativa o arquitecto |
| D4 | Altitud y zona climática de invierno (DB SE-AE Anejo E) | Carga de nieve s_k (hipótesis provisional: 0,6 kN/m²) | Topografía |
| D5 | Modelo de ascensor (foso, huecos, cargas) | Fosos y huecos del núcleo | Instalaciones o diseño |
| D6 | Pieza cerámica y mortero de la fábrica portante (f_b, f_k, expansión por humedad) | Comprobación de los muros y distancia entre juntas de fachada (DB SE-F) | Proyecto de ejecución |
| D7 | Criterio de medición de la altura de cornisa (Plan Parcial) | Margen del bloque (E3) | Normativa del Plan Parcial (la aportará el arquitecto) |
| D8 | Necesidades reales de instalaciones: secciones de patinillos, equipos en cubierta, suelo radiante | Huecos H-U1 y H-M1, cargas de cubierta y pavimento | `fases/03_instalaciones.md` |
| D9 | Zona de radón del municipio (DB HS 6) | Solución de la cámara sanitaria | Normativa |

### 7.2 Riesgos

| # | Riesgo | Nivel | Mitigación |
|---|---|---|---|
| R1 | **Cimentación sin estudio geotécnico**, en contra de DB SE-C 3. Hay riesgo de asientos, de expansividad no detectada y de no poder contratar el seguro decenal ni el control técnico | **Alto** | Encargar el estudio (5.1). Mientras tanto, las soluciones de este documento son solo alternativas condicionadas |
| R2 | Nivel freático desconocido: fosos de ascensor, cámara sanitaria bajo rasante (E3, opción a) y excavaciones | Medio-alto | Geotécnico. Si no lo hay, catas en obra antes de cerrar el proyecto |
| R3 | NCSE-02 no comprobada | Medio | Confirmar a_b (D3). Si aplica, revisar la fábrica portante (alternativa B de pórticos) |
| R4 | Cornisa del bloque al límite (E3) | Medio | Ver las opciones de E3 |
| R5 | Bloque de 37,5 m sin junta, a 2,5 m del límite de 40 m | Bajo | No alargar el bloque. Si se alarga, junta o cálculo térmico |
| R6 | Retícula del bloque y edificabilidad: margen de 6 m²c | Medio | Ejes ajustados hacia dentro (2.2). Diseño y dibujo (F4) deben mantener la envolvente de 12,00 × 37,50 m a cara exterior |
| R7 | Topografía desconocida: posibles muros de contención o escalonamiento de las hileras de 52 m y 90 m | Medio | Topografía (D2). Si hay pendiente E-O, escalonar las hileras en la junta o en las medianeras |
| R8 | Forjado de 30 cm en los vanos extremos sin margen de esbeltez | Bajo | Cálculo de flecha o 35 cm (4.1) |
| R9 | Punzonamiento en los pilares interiores del bloque | Bajo (se resuelve con armadura) | Armadura de punzonamiento y huecos fuera de 6d |
| R10 | Impacto de vehículos sobre las fachadas de entrada de las casas | Bajo | Topes de rueda (E6) |

---

## 8. Conflictos anotados en `fases/conflictos.md`

Se numeran **E1 a E6** (prefijo E = estructura) para no chocar con las entradas que añadan a la vez instalaciones y normativa.

| Nº | Resumen |
|---|---|
| E1 | Junta de dilatación en la hilera A-oeste (52 m): el doble muro (≈ 0,51 m) se come ≈ 0,27 m del interior de las viviendas 4 y 5 |
| E2 | Arriostramiento E-O de las casas: hace falta un muro E-O de ≥ 2,5 m por vivienda y planta, o machones de fachada |
| E3 | Cota de PB, forjado sanitario ventilado y cubierta frente a la cornisa del bloque (margen de 0,3 m) |
| E4 | Patinillos PB-1 a PB-4 del bloque frente a la zona de punzonamiento de los pilares B2, B3, B5 y B6 (respuesta a I-3) |
| E5 | Patinillo PU de las casas: máximo 0,50 m en dirección N-S para no cortar viguetas (respuesta a I-1 e I-2) |
| E6 | Plazas en batería contra la fachada de entrada de las casas: impacto de vehículos |

PENDIENTE DE VALIDAR POR EL ARQUITECTO
