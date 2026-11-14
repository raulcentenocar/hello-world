# F2 — Diseño preliminar · Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Cañada)

Agente: diseño preliminar (arquitecto proyectista) · Fecha: 2026-11-14 · Base: `fases/01_urbanismo.md` **rev. 2 (aprobada)**, `datos/UA 03 01.pdf`, resultados del generador de volumetrías ejecutado por el coordinador.

> **Aviso de método.** En esta sesión **no tengo herramienta de ejecución de comandos (Bash)**. Por eso:
> - Uso solo los resultados del generador que **ya ejecutó el coordinador** (envolventes de la parcela completa).
> - He dejado escritos los JSON de cada parte de cada variante en `planos/volumetrias/v{1,2,3}_{unifamiliar,multifamiliar}.json`, con los comandos exactos en el apartado 7. **Sus resultados no se han calculado y no se inventan.**
> - Las cifras de este documento (posiciones, distancias, superficies, plazas) son **mediciones manuales** sobre el polígono de vértices de la cédula, hechas en un sistema local. Así se indica en cada caso. Cuando el coordinador ejecute los JSON, sus resultados deberán contrastarse con estas cifras.

---

## 0. Resumen

- Se proponen **tres variantes de mezcla** sobre la parcela completa (una sola promoción). Todas suman **34 viviendas y como máximo 5.100 m²c**, y en todas las hileras van en dirección E-O, con la fachada principal y el jardín al sur:

| Variante | Reparto (hipótesis) | Idea | Aparcamiento (68 plazas en superficie) |
|---|---|---|---|
| **V1 "Calle de casas"** | **24 unifamiliares + 10 pisos** (1 bloque) | Calle interior E-O desde Floristas con hileras a ambos lados. Bloque de 3 plantas al NO, mirando a la ZV-02 | **Junto a cada vivienda** (2 plazas delante de cada casa) + bolsa pequeña para el bloque |
| **V2 "Calle-aparcamiento central"** | **16 unifamiliares + 18 pisos** (2 bloques) | Dos filas de casas al sur, una calle-aparcamiento E-O en el centro y dos bloques escalonados al norte, frente a la ZV-02. Interior peatonal | **Bolsa común lineal** (calle-aparcamiento) |
| **V3 "Parque central"** | **8 unifamiliares + 26 pisos** (3 bloques) | Una fila de casas a la Avda. de la Dehesa, bolsa compacta junto a Floristas y tres bloques en arco al norte y al este alrededor de un parque central | **Bolsa común compacta** junto a Floristas |

- Las tres variantes cumplen la ocupación **incluso con la lectura más restrictiva** (45 % sobre toda la parcela): ocupan entre el 22 % y el 26 %. La duda de F1 sobre cómo se aplica la ocupación cuando conviven los dos usos (riesgo 4.2) **no condiciona ninguna variante en lo que se refiere a la edificación**. Sí puede condicionarla si el aparcamiento computa (apartado 5).
- Separación de 6 m: se cumple en todas, con la medición manual. Las hileras de una misma agrupación quedan **exactamente a 6 m**: es el punto más sensible si la normativa da otro valor.
- **Recomendación:** **V1**, con V2 como alternativa (apartado 6). **Decide el arquitecto.**

---

## 1. Datos de partida, hipótesis comunes y criterios

### 1.1 Datos urbanísticos (de F1, sin cambios)

5.100 m²c y 34 viviendas en total · 8.839 m²s (superficie oficial) · Unifamiliar: 2 plantas, cornisa 7,5 m (coronación 10,5 m), ocupación 60 %, retranqueos de 3 m a fachada, a UA-03-02 y a ZV-02 · Multifamiliar: 3 plantas, cornisa 10 m (coronación 13 m), ocupación 45 %, retranqueos de 5 m · Separación entre edificios de 6 m (**dato PROVISIONAL del arquitecto**) · 2 plazas por vivienda, 68 en superficie · Una sola promoción · Agrupación de 8 en 8, partible en hileras (interpretación del arquitecto) · Sin sótano, sin estudio geotécnico y sin programa del cliente.

Siguen como **FALTA DATO** (F1, 5.1): fondo edificable, longitud máxima de hilera o bloque, cómputo de superficies, áticos y bajo cubierta, castilletes, regla de ocupación en la mezcla, cómputo y posición del aparcamiento en superficie, dimensiones de plaza y viario de la ordenanza, topografía, geotecnia, servicios urbanos, elemento de la esquina SE y geometría exacta de los arcos.

### 1.2 Resultados del generador (envolventes, ejecutadas por el coordinador)

Comandos citados (ejecutados por el coordinador desde la raíz del repositorio):

```bash
python3 scripts/volumetria_generador.py planos/volumetrias/entrada_unifamiliar.json
python3 scripts/volumetria_generador.py planos/volumetrias/entrada_unifamiliar.json --json --sin-dxf
python3 scripts/volumetria_generador.py planos/volumetrias/entrada_multifamiliar.json
python3 scripts/volumetria_generador.py planos/volumetrias/entrada_multifamiliar.json --json --sin-dxf
```

| Envolvente (parcela completa, un solo uso) | Huella m² | Ocup. % | Pl. | Construida / computable m²c | Viv. | Orientación | Nº edificios |
|---|---|---|---|---|---|---|---|
| `unifamiliar_adosada` | 4.515,0 | 51,1 | 2 | 5.100 / 5.100 | 34 (geométricas 73) | 108° (paralelas a Floristas) | 6 hileras |
| `unifamiliar_aislada` | 5.303,4 | 60,0 | 2 | 5.100 / 5.100 | 1 | — | 1 |
| `bloque_abierto` | 3.240,0 | 36,7 | 3 | 5.100 / 5.100 | 34 (geométricas 51) | 0,5° (E-O) | 3 bloques |
| `torre` | 2.400,0 | 27,1 | 3 | 5.100 / 5.100 | 34 (geométricas 51) | 60° | 6 torres |

(Hipótesis por defecto del generador: altura de planta 3,0 m, fondo de bloque 12 m, adosada de 6 × 10 m, 100 m²c por vivienda. Ninguna tipología sale `FALTA DATO` ni `NO CABE`.)

Lectura para el diseño, **como referencia de capacidad y no como opciones de proyecto**:

1. **Sobra capacidad geométrica.** La parcela admite unas 73 adosadas o 51 pisos con huella de sobra. **Mandan la edificabilidad (5.100 m²c) y el tope de 34 viviendas.** Queda suelo libre para el aparcamiento en superficie, que el generador no modela.
2. **Orientación.** El generador coloca las adosadas paralelas a la fachada más larga, que es Calle Floristas (lado 2, 101,65 m). Así las hileras quedan en dirección NNO-SSE, con las fachadas a ENE y OSO. **En las tres variantes giro las hileras a E-O**, con la fachada principal a sur, por soleamiento. Por eso, en los JSON de cada parte (apartado 7), la fachada más larga de la subparcela unifamiliar es la de la Avda. de la Dehesa, y el generador debería orientar las hileras a unos 0,5° (por confirmar al ejecutarlo). El bloque abierto ya sale E-O (0,5°), coherente con las variantes.
3. Ni los 3 bloques del `bloque_abierto` ni las 6 hileras del `unifamiliar_adosada` respetan la agrupación de 8, porque el generador no la modela (riesgo 4.15 d). Se comprueba a mano en cada variante.

### 1.3 Sistema de medición manual

- Origen local en el **vértice 3** (esquina Avda. de la Dehesa / Calle Floristas). **x** hacia el este, **y** hacia el norte, en metros. UTM = (414.896,93 + x ; 4.478.781,24 + y).
- Vértices en coordenadas locales: V1 (91,85 ; 73,52) · V2 (91,85 ; 0,76) · V3 (0 ; 0) · V4 (−31,45 ; 96,66) · V5 (−2,47 ; 93,07) · V6 (71,90 ; 77,05). Por el método de Gauss da 9.022,15 m², igual que el script.
- Bordes aproximados (cuerdas):
  - sur, y ≈ 0,0083·x;
  - este, x = 91,85;
  - Floristas, la distancia de un punto a la recta vale d = 0,9509·x + 0,3094·y;
  - ZV-02 tramo 2 (V5-V6), y = 93,07 − 0,2154·(x + 2,47);
  - ZV-02 tramo 3 (V6-V1), y = 77,05 − 0,177·(x − 71,9);
  - ZV-02 tramo 1 (V4-V5), y = 96,66 − 0,124·(x + 31,45).
- Las superficies de las subparcelas se pasan a superficie oficial con el factor 8.839 / 9.022,15 = **0,9797** (decisión del arquitecto (PAUSA F1): se calcula sobre la oficial).

### 1.4 Hipótesis de diseño comunes (declaradas; no son datos)

| Código | Hipótesis | Justificación / norma de referencia |
|---|---|---|
| H-REP | Reparto unifamiliar / multifamiliar y superficie de cada vivienda: el que se indica en cada variante | No hay programa del cliente (decisión del arquitecto (PAUSA F1)) |
| H-AGR | La regla "de 8 en 8" se lee como **agrupaciones de al menos 8 viviendas**. Se aplica a las unifamiliares, que se agrupan de 8 exactamente (4 + 4 o 8). Los pisos se agrupan por edificio, con al menos 8 viviendas por edificio. Las **2 viviendas que quedan fuera de 4 × 8 van siempre en la parte multifamiliar** (riesgo 4.15 c) | Con la lectura "exactamente 8 en todas las viviendas", **ninguna variante puede cumplir**, porque 34 no es múltiplo de 8 (riesgo 4.15 a). **Pendiente de confirmar** |
| H-SEP | Los 6 m provisionales se aplican como **distancia mínima entre dos edificios cualesquiera**: entre hileras de una misma agrupación, entre agrupaciones, entre bloques y entre unifamiliar y multifamiliar (riesgo 4.16). Esquina con esquina se mide la distancia real | Mismo criterio que el generador ("separación entre edificios", un único valor) |
| H-OCU | Ocupación en la mezcla: se comprueba **con dos lecturas**. (A) Cada porcentaje sobre la subparcela asignada a su uso. (B) La más restrictiva: 45 % sobre la parcela completa para toda la edificación. | La regla real es **FALTA DATO** (F1 2.3). Se comprueban las dos para no depender de ella |
| H-LIN | La línea interior entre la parte unifamiliar y la multifamiliar no es un lindero. Solo se usa para ejecutar el generador por partes (apartado 7). Allí se trata como lindero: 3 m por el lado unifamiliar y 5 m por el multifamiliar, lo que da 8 m ≥ 6 m | Lado de la seguridad |
| H-ALT | Altura de planta 3,00 m de suelo a suelo. Cota de planta baja +0,30 m sobre la rasante. Canto de cubierta y peto ≈ 0,35-0,45 m. Cornisa estimada: unifamiliar ≈ 6,6 m (≤ 7,5 ✔) y multifamiliar ≈ 9,7 m (≤ 10 ✔) | Por defecto del generador. **Topografía y criterio de medición de la altura: FALTA DATO**. El multifamiliar queda con poco margen (≈ 0,3 m) |
| H-CUB | Sin bajo cubierta habitable ni ático. Cubierta plana o inclinada **por debajo de la cornisa**. Castillete de ascensor y escalera sobre la cubierta del multifamiliar, **pendiente** de que la normativa lo admita entre cornisa y coronación (FALTA DATO) | Cédula: áticos y bajo cubierta FALTA DATO |
| H-COM | **Toda la superficie construida sobre rasante computa al 100 %**: `computo` = null en F1, que es lo conservador. No se proyectan porches ni terrazas cubiertas fuera del techo computado. Las terrazas, si las hay, se meten dentro de los m²c de cada vivienda | `scripts/LEEME_volumetria.md` (cómputo sin coeficiente = 100 %) |
| H-APA-1 | Plaza en batería a 90°: **2,50 × 5,00 m**. Calle de maniobra o rodadura con batería: **6,00 m** (doble sentido) | **La ordenanza municipal o del Plan Parcial que fija estas dimensiones es FALTA DATO.** Los valores adoptados son holgados respecto de los mínimos habituales en las ordenanzas municipales. Se revisarán cuando se aporte la normativa |
| H-APA-2 | Plaza accesible: 5,00 × 2,50 m + espacio de transferencia lateral de 1,20 m (anchura total 3,70 m). **Se reservan 2 plazas accesibles** en V2 y V3 y 1 en V1, dentro de las 68 | CTE DB SUA, Anejo A ("plaza de aparcamiento accesible") y SUA 9. **El número exigible depende del nº de viviendas accesibles: FALTA DATO** |
| H-APA-3 | **Las plazas quedan fuera de las bandas de retranqueo**: 5 m a Floristas y 3-5 m al resto de linderos. Solo los accesos rodados cruzan esas bandas | F1 riesgo 4.5: si pueden ir en la banda de retranqueo es FALTA DATO. Se elige lo conservador |
| H-APA-4 | Recogida de residuos y servicios (camión) **desde Calle Floristas**, con un punto de contenedores junto a cada acceso. Los viales interiores son solo para turismos | Evita el radio de giro de camiones en fondos de saco. La ordenanza sobre fondos de saco es FALTA DATO |
| H-SOL | Latitud ≈ 40,45° N (derivada de las coordenadas UTM de la cédula). Altura solar a mediodía en el solsticio de invierno ≈ 26,1°, así que la sombra mide ≈ 2,04 veces la altura del edificio: ≈ 13,5 m detrás de una hilera de 2 plantas y ≈ 19,8 m detrás de un bloque de 3 | Cálculo astronómico simple. No sustituye a un estudio de soleamiento |
| H-UTI | Superficie útil ≈ 0,77-0,82 de la construida privativa (estimación de anteproyecto) | Orientativo |
| H-EST | Retícula y luces orientativas para F3. **Sin datos del terreno** (F1 riesgo 4.6) | CTE DB SE-C exige el estudio geotécnico. Queda para F3 |

**Agrupación por zonas húmedas (todas las variantes):**
- Unifamiliar: cocina, aseo y lavadero en planta baja, en la crujía de entrada (norte o calle). Los baños de la planta 1 van encima, en la misma crujía, con un patinillo vertical de 0,60 × 0,40 m por vivienda junto a la medianera, para bajantes, ventilación (CTE DB HS 3) y la previsión de aerotermia.
- Multifamiliar: los baños y las cocinas de cada planta quedan pegados al núcleo de escalera y ascensor. Se reserva **un patinillo registrable de ≈ 1,20 × 0,60 m por cada 2 viviendas y planta** junto al rellano, para bajantes, ventilación y montantes, y un cuarto de contadores e instalaciones en planta baja.

---

## 2. Variante V1 — "Calle de casas" (24 unifamiliares + 10 pisos)

### 2.1 Idea y volumetría

- **Calle interior E-O** de 6 m, desde Calle Floristas (y = 26-32) hasta el lindero este (x ≈ 88). Es un fondo de saco de ≈ 98 m. A cada lado hay una banda de 5 m con **2 plazas delante de cada casa**.
- **Banda A (sur):** viviendas en y = 9,0-21,0, con el **jardín privado al sur** (≈ 8,3 m de fondo, hacia la Avda. de la Dehesa) y la entrada y las plazas al norte. Hilera de 8 (x = 2,0-54,0) + hueco de 6 m + hilera de 4 (x = 60,0-86,0). Longitud total 84 m.
- **Banda B (norte de la calle):** viviendas en y = 37,0-49,0, con la entrada y las plazas al sur y el jardín al norte (6 m). Tres hileras de 4: x = −2,5 a 23,5 / 29,5 a 55,5 / 61,5 a 87,5. Longitud total 90 m.
- **Bloque multifamiliar** de 12,0 × 37,5 m, 3 plantas, con eje E-O, en x = 19,5-57,0 e y = 61,0-73,0. Fachada sur a los jardines y fachada norte a la ZV-02, con vistas al parque. Al estar al norte de las casas, **no les da sombra**.
- **Bolsa del bloque** de 22 plazas (20 del bloque + 2 de reserva o visitantes), con acceso propio desde Floristas: calle de maniobra E-O en y = 62-68 y filas de plazas en y = 57-62 y 68-73, de x ≈ −13 / −17 a 13,5.
- **Zonas libres:** jardines comunes al este del bloque y entre el bloque y la ZV-02, y la esquina SE (elemento sin identificar, FALTA DATO) libre.
- **Accesos:**
  - rodados: 2 desde Calle Floristas, la calle de casas y la bolsa del bloque;
  - peatonales: el hueco de 6 m entre hileras de la banda A (hacia la Avda. de la Dehesa) y los de la banda B (hacia los jardines comunes del norte).

**Agrupaciones (H-AGR):** Ag-1 = hilera A-oeste de 8 · Ag-2 = las dos hileras oeste de B (4 + 4) · Ag-3 = la hilera A-este de 4 y la hilera B-este de 4, enfrentadas al otro lado de la calle (4 + 4) · Bloque de 10 pisos (≥ 8).

### 2.2 Tipologías y distribución por plantas

**U-V1, unifamiliar adosada de 6,50 × 12,00 m, 2 plantas, 156 m²c, 3 dormitorios** (hipótesis)

| Planta | Estancia | Útil m² |
|---|---|---|
| PB | Salón-comedor (fachada sur, con salida al jardín) | 28,0 |
| PB | Cocina (fachada norte, hacia la entrada) | 12,0 |
| PB | Vestíbulo | 5,0 |
| PB | Aseo (zona húmeda en la crujía norte) | 3,0 |
| PB | Lavadero y despensa (zona húmeda) | 4,0 |
| PB | Escalera (de un tramo, junto a la medianera) | 5,5 |
| PB | Distribuidor | 3,0 |
| P1 | Dormitorio principal (sur) | 15,0 |
| P1 | Vestidor | 3,0 |
| P1 | Baño principal (encima de la zona húmeda de PB) | 5,0 |
| P1 | Dormitorio 2 (sur) | 11,0 |
| P1 | Dormitorio 3 (norte) | 10,0 |
| P1 | Baño 2 (encima de la zona húmeda de PB) | 4,5 |
| P1 | Distribuidor | 6,0 |
| P1 | Escalera (hueco) | 5,5 |
| | **Total útil** | **≈ 120,5** |
| | Construida: PB 78,0 + P1 78,0 | **156,0** |

Patinillo de 0,60 × 0,40 m junto a la medianera, en la crujía norte. Exterior privativo: jardín sur de ≈ 54 m² (banda A) o jardín norte de ≈ 39 m² (banda B), más 2 plazas delante de la casa.

**Bloque M-V1** de 12,00 × 37,50 m = 450 m² por planta, 3 plantas, **2 portales** (uno en cada mitad). Cada portal tiene escalera y ascensor y da servicio a **1 vivienda en PB y 2 en cada planta alta**, que son **pasantes norte-sur**.

| Tipo | Ubicación | Nº | Construida privativa m² | Programa | Útil m² (estimada) |
|---|---|---|---|---|---|
| M-V1-a | P1 y P2 | 8 | 98,5 | Salón-comedor 25,0 · cocina 10,0 · dorm. principal 13,0 · dorm. 2 10,0 · dorm. 3 8,5 · baño 4,5 · baño 3,5 · vestíbulo y distribuidor 6,0 | **80,5** |
| M-V1-b | PB, con jardín privativo al sur | 2 | 156,0 | Salón-comedor 32,0 · cocina 13,0 · dorm. principal 15,0 + baño 5,0 · dorm. 2 11,0 · dorm. 3 10,5 · dorm. 4 9,5 · baño 4,5 · aseo 2,5 · vestíbulo y distribuidor 10,0 · lavadero 4,5 · almacén 4,0 | **121,5** |

Elementos comunes por portal: núcleo de escalera, ascensor y rellano de ≈ 28 m² por planta. En PB, además: portal de 18 m², cuarto de contadores e instalaciones de 8 m², y cuarto de bicicletas y basuras de 15 m².

### 2.3 Cuadro de superficies V1

| Parte | Planta | Construida m² | Computable m²c | No computable m² |
|---|---|---|---|---|
| Unifamiliar (24 × 78,0) | PB | 1.872,0 | 1.872,0 | 0 |
| Unifamiliar (24 × 78,0) | P1 | 1.872,0 | 1.872,0 | 0 |
| **Subtotal unifamiliar** | | **3.744,0** | **3.744,0** | 0 |
| Bloque (12,0 × 37,5) | PB | 450,0 (viviendas 312 + comunes 138) | 450,0 | 0 |
| Bloque | P1 | 450,0 (viviendas 394 + comunes 56) | 450,0 | 0 |
| Bloque | P2 | 450,0 (viviendas 394 + comunes 56) | 450,0 | 0 |
| **Subtotal multifamiliar** | | **1.350,0** | **1.350,0** | 0 |
| **TOTAL V1** | | **5.094,0** | **5.094,0** (99,9 % de 5.100) | **0** (H-COM: el cómputo es FALTA DATO, todo computa) |

Útil total estimada: unifamiliar 24 × 120,5 = 2.892 m² · pisos 8 × 80,5 + 2 × 121,5 = 887 m² · comunes ≈ 210 m².

### 2.4 Comprobación urbanística V1 (medición manual)

| Comprobación | Valor V1 | Límite | |
|---|---|---|---|
| Edificabilidad total | 5.094,0 m²c | 5.100 m²c | ✔ |
| Viviendas | 24 + 10 = 34 | 34 | ✔ |
| Ocupación, lectura A: unifamiliar | 1.872 / 5.397,1 m² (subparcela sur, y < 55) = 34,7 % | 60 % | ✔ |
| Ocupación, lectura A: multifamiliar | 450 / 3.441,9 m² (subparcela norte) = 13,1 % | 45 % | ✔ |
| Ocupación, lectura B (toda la edificación sobre la parcela completa) | 2.322 / 8.839 = 26,3 % | 45 % | ✔ |
| Plantas y cornisa unifamiliar | 2 pl. y ≈ 6,6 m | 2 pl. y 7,5 m | ✔ |
| Plantas y cornisa multifamiliar | 3 pl. y ≈ 9,7 m | 3 pl. y 10 m | ✔ (margen ≈ 0,3 m; topografía FALTA DATO) |
| Retranqueo de la banda A a la Avda. de la Dehesa | ≥ 8,27 m | 3 m | ✔ |
| Retranqueo de la banda A a Floristas (esquina 2,0 ; 9,0) | 4,69 m | 3 m | ✔ |
| Retranqueo de A y B a UA-03-02 | 5,85 / 4,35 m | 3 m | ✔ |
| Retranqueo de la banda B a Floristas (esquina −2,5 ; 37,0) | 9,07 m | 3 m | ✔ |
| Retranqueo del bloque a Floristas (esquina 19,5 ; 61) | ≫ 5 m | 5 m | ✔ |
| Retranqueo del bloque a la ZV-02 (esquina 57,0 ; 73,0) | ≈ 7,1 m (≈ 6,4 m si el arco entra en la parcela) | 5 m | ✔ |
| Separación entre hileras de la misma banda | 6,0 m | 6 m (prov.) | ✔ (justo) |
| Separación banda A – banda B (frente a frente) | 16,0 m | 6 m | ✔ |
| Separación banda B – bloque | 12,0 m | 6 m | ✔ |
| Agrupaciones de 8 (H-AGR) | 3 × 8 unifamiliares + 1 edificio de 10 | ≥ 8 | ✔ con H-AGR / ✘ con "exactamente 8" en todas |
| Longitud de hilera | **52 m** (hilera A-oeste de 8) | **FALTA DATO** | ⚠ Riesgo. Si el máximo es menor, ver la alternativa en 2.7 |

### 2.5 Aparcamiento V1 (68 plazas)

| Zona | Disposición | Plazas |
|---|---|---|
| Delante de cada casa (bandas A y B) | 2 plazas en batería de 2,50 × 5,00 m por cada 6,50 m de frente. Queda un paso peatonal de 1,50 m hasta la puerta. La calle de 6 m sirve de calle de maniobra | **48** (24 × 2) |
| Bolsa del bloque, junto a Floristas | Fila sur y = 57-62 (x −13,3 a 13,5 = 26,8 m): 9 + 1 accesible de 3,70 m = 10. Fila norte y = 68-73 (x −16,9 a 13,5 = 30,4 m): 12. Calle de maniobra de 6 m con acceso directo desde Floristas | **22** (incluye 1 accesible y 2 de reserva) |
| **Total** | | **70 ≥ 68 ✔** |

- Superficie aproximada de viario y aparcamiento: plazas ≈ 880 m², calle ≈ 590 m², maniobra de la bolsa ≈ 180 m². En total **≈ 1.650 m²**.
- Puntos débiles:
  - un fondo de saco de ≈ 98 m sin martillo (H-APA-4). Si la ordenanza exige zona de giro (FALTA DATO), se pierde una vivienda del par este o hay que estrechar los frentes;
  - **2 accesos rodados a Floristas** (vados: FALTA DATO).

### 2.6 Ventajas e inconvenientes V1

| | |
|---|---|
| ✔ | **La más coherente con la ordenanza "Residencial Unifamiliar Adosada"**: 71 % de las viviendas son unifamiliares. Es la variante que **menos depende del riesgo 4.1** (que se admita el multifamiliar): si no se admite, solo hay que rehacer un bloque de 10 viviendas |
| ✔ | Aparcamiento a la puerta, que es lo que espera el mercado de la adosada. Recorridos cortos |
| ✔ | Soleamiento: las 24 casas tienen fachada sur. Distancia de A a B de 16 m, mayor que la sombra de invierno (≈ 13,5 m), así que no hay sombra de una banda sobre otra. El bloque no da sombra a nadie |
| ✔ | Ventilación cruzada norte-sur en todas las viviendas: casas y pisos pasantes |
| ✔ | Economía constructiva: una sola tipología repetida 24 veces, forjados entre medianeras, un único bloque pequeño |
| ✘ | Mucho pavimento rodado (≈ 1.650 m²) en el centro de la parcela. Poco espacio libre común (≈ 3.800 m², sobre todo al norte) |
| ✘ | Las casas de la banda B tienen el jardín al norte y la fachada sur dando a la calle, ocupada por coches |
| ✘ | Hilera de 52 m (longitud máxima FALTA DATO). Separación de solo 6 m entre hileras (si la normativa la aumenta, la banda B de 90 m no cabe) |
| ✘ | Pisos de 3 dormitorios algo compactos (≈ 80 m² útiles) frente a las casas |
| ✘ | Flexibilidad baja: la estructura de calle y bandas es rígida |

### 2.7 Retícula estructural orientativa V1 (para F3)

- **Unifamiliar:**
  - muros de carga o pórticos en las **medianeras, cada 6,50 m** (ejes 1, 2, 3... a lo largo de cada hilera);
  - forjado unidireccional que salva **6,50 m entre medianeras**, sin vigas intermedias, con las fachadas sur y norte libres;
  - fondo de 12,00 m: ejes de fachada A (sur) y C (norte), y eje B intermedio solo para el zuncho de la escalera.
  - **Junta de dilatación** en la hilera de 8 (52 m), entre las viviendas 4 y 5: CTE DB SE-AE 3.4.1, sin elementos continuos de más de 40 m.
- **Bloque:**
  - ejes longitudinales A-B-C: **2 crujías de 6,00 m**;
  - ejes transversales 1 a 7: **6 vanos de 6,25 m** (37,5 m, sin junta, < 40 m);
  - núcleos de escalera y ascensor entre los ejes 2-3 y 5-6;
  - losa maciza o reticular, con luces ≈ 6,0 × 6,25 m.
- **Cimentación: FALTA DATO** (sin geotecnia).
- **Alternativa si la longitud máxima de hilera es menor de 52 m:** frente de 6,30 m y banda A en 4 + 4 + 4 (87,6 m, ✔ en el ancho disponible de 88,6 m). En ese caso queda un paso peatonal de 1,30 m junto a las plazas: hay que validarlo.

---

## 3. Variante V2 — "Calle-aparcamiento central" (16 unifamiliares + 18 pisos)

### 3.1 Idea y volumetría

- **Calle-aparcamiento E-O** de 16 m (plazas 5 + calle 6 + plazas 5) en y = 44-60. Tiene **un único acceso** desde Floristas y un fondo de saco con zona de giro de 6 × 16 m en el extremo este (x = 80,85-86,85). **Todo el aparcamiento está aquí, y el resto de la parcela es peatonal.**
- **Unifamiliares al sur (16):**
  - **Fila 1**, y = 8,0-20,0: 4 + 4 (x = 24-52 y 58-86), con el **jardín al sur** (≈ 7,3 m) hacia la Avda. de la Dehesa y la entrada al norte por un paseo peatonal (y = 20-23).
  - **Fila 2**, y = 29,0-41,0: 4 + 4 (mismos x), con jardín delantero al sur (y = 23-29) y entrada desde el paseo peatonal de y = 41-44, junto a la calle-aparcamiento.
- **Pisos al norte (18):** **dos bloques de 13,0 × 30,8 m, 3 plantas, escalonados** siguiendo la curva de la ZV-02. Bloque 1 en x = −15,5 a 15,3, y = 66-79. Bloque 2 en x = 21,3 a 52,1, y = 63-76. Fachada sur a la calle-aparcamiento y a las casas, y fachada norte a la ZV-02.
- **Zonas libres:**
  - plaza ajardinada en la esquina Floristas / Avda. de la Dehesa (x < 18, y < 41), que es la imagen de la promoción;
  - jardín común en el NE (x > 55, y > 60), abierto visualmente a la ZV-02;
  - esquina SE libre.

**Agrupaciones:** Ag-1 = fila 1 (4 + 4) · Ag-2 = fila 2 (4 + 4) · Bloques de 9 + 9 (≥ 8).

### 3.2 Tipologías y distribución por plantas

**U-V2, unifamiliar de 7,00 × 12,00 m, 2 plantas, 168 m²c, 4 dormitorios**

| Planta | Estancia | Útil m² |
|---|---|---|
| PB | Salón-comedor (sur) | 32,0 |
| PB | Cocina (norte) | 13,0 |
| PB | Vestíbulo | 5,0 |
| PB | Aseo (zona húmeda en la crujía norte) | 3,0 |
| PB | Lavadero (zona húmeda) | 4,0 |
| PB | Escalera | 5,5 |
| PB | Distribuidor | 4,5 |
| P1 | Dormitorio principal (sur) | 14,0 |
| P1 | Baño principal (encima de la zona húmeda) | 5,0 |
| P1 | Dormitorio 2 (sur) | 10,0 |
| P1 | Dormitorio 3 (norte) | 10,0 |
| P1 | Dormitorio 4 (norte) | 8,5 |
| P1 | Baño 2 (encima de la zona húmeda) | 4,5 |
| P1 | Distribuidor | 6,5 |
| P1 | Escalera | 5,5 |
| | **Total útil** | **≈ 131,0** |
| | Construida: PB 84,0 + P1 84,0 | **168,0** |

**Bloques M-V2**: 13,00 × 30,80 m = 400,4 m² por planta, 3 plantas, **1 portal**, **3 viviendas por planta**, todas pasantes norte-sur. El núcleo va en la fachada norte, en el centro, y la vivienda central lo rodea por el sur.

| Tipo | Ubicación | Nº (2 bloques) | Construida privativa m² | Programa | Útil m² |
|---|---|---|---|---|---|
| M-V2-a | P1 y P2 | 12 | 124,1 | Salón-comedor 30,0 · cocina 12,0 · dorm. principal 14,0 + baño 5,0 · dorm. 2 11,0 · dorm. 3 10,0 · baño 4,5 · vestíbulo y distribuidor 9,0 · tendedero 4,5 | **100,0** |
| M-V2-b | PB, con jardín privativo | 6 | 114,1 | Salón-comedor 27,0 · cocina 11,0 · dorm. principal 14,0 + baño 5,0 · dorm. 2 11,0 · dorm. 3 9,0 · baño 4,5 · vestíbulo y distribuidor 8,0 · lavadero 3,0 | **92,5** |

Comunes por bloque: núcleo de 28 m² por planta. En PB, además: portal, contadores, bicicletas y basuras, ≈ 30 m².

### 3.3 Cuadro de superficies V2

| Parte | Planta | Construida m² | Computable m²c | No computable m² |
|---|---|---|---|---|
| Unifamiliar (16 × 84,0) | PB | 1.344,0 | 1.344,0 | 0 |
| Unifamiliar | P1 | 1.344,0 | 1.344,0 | 0 |
| **Subtotal unifamiliar** | | **2.688,0** | **2.688,0** | 0 |
| 2 bloques (2 × 400,4) | PB | 800,8 (viviendas 684,8 + comunes 116) | 800,8 | 0 |
| 2 bloques | P1 | 800,8 (viviendas 744,8 + comunes 56) | 800,8 | 0 |
| 2 bloques | P2 | 800,8 (viviendas 744,8 + comunes 56) | 800,8 | 0 |
| **Subtotal multifamiliar** | | **2.402,4** | **2.402,4** | 0 |
| **TOTAL V2** | | **5.090,4** | **5.090,4** (99,8 %) | **0** (H-COM) |

Útil estimada: unifamiliar 16 × 131,0 = 2.096 m² · pisos 12 × 100,0 + 6 × 92,5 = 1.755 m².

### 3.4 Comprobación urbanística V2 (medición manual)

| Comprobación | Valor V2 | Límite | |
|---|---|---|---|
| Edificabilidad total | 5.090,4 m²c | 5.100 | ✔ |
| Viviendas | 16 + 18 = 34 | 34 | ✔ |
| Ocupación A: unifamiliar | 1.344 / 5.076,0 (y < 52) = 26,5 % | 60 % | ✔ |
| Ocupación A: multifamiliar | 800,8 / 3.763,0 = 21,3 % | 45 % | ✔ |
| Ocupación B | 2.144,8 / 8.839 = 24,3 % | 45 % | ✔ |
| Plantas y cornisa | Unifamiliar 2 / ≈ 6,6 m · multifamiliar 3 / ≈ 9,7 m | 2 / 7,5 · 3 / 10 | ✔ |
| Retranqueo de la fila 1 a la Avda. de la Dehesa / a UA-03-02 | ≥ 7,27 m / 5,85 m | 3 m | ✔ (≥ 4,9 m si el arco de la Dehesa, de flecha 2,4 m, entra en la parcela) |
| Retranqueo del bloque 1 a Floristas (esquina −15,5 ; 66) | ≈ 5,7 m | 5 m | ✔ (justo) |
| Retranqueo del bloque 2 a la ZV-02 (esquina 52,1 ; 76) | ≈ 5,2 m sobre la cuerda | 5 m | ✔ sobre la cuerda / **✘ si el arco del tramo 2 entra en la parcela** (≈ 4,4 m). Mitigación: bajar el bloque 2 1,0 m, dejando 2 m hasta las plazas, o acortarlo |
| Separación entre hileras | 6,0 m | 6 m | ✔ (justo) |
| Separación fila 1 – fila 2 | 9,0 m | 6 m | ✔ |
| Separación entre bloques (esquina con esquina) | ≥ 6,0 m | 6 m | ✔ (justo) |
| Separación unifamiliar – multifamiliar | 22 m | 6 m | ✔ |
| Agrupaciones | 2 × 8 unifamiliares + 9 + 9 | ≥ 8 | ✔ con H-AGR |
| Longitud de hilera / bloque | 28 m / 30,8 m | FALTA DATO | ⚠ Probable ✔ (cortas) |

### 3.5 Aparcamiento V2 (68 plazas)

| Fila | Tramo útil (fuera de los 5 m de retranqueo; ver H-APA-3) | Plazas |
|---|---|---|
| Sur (y = 44-49) | x −9,0 a 80,85 = 89,85 m, con 1 paso peatonal de 2,5 m y 1 plaza accesible | 34 |
| Norte (y = 55-60) | x −12,6 a 80,85 = 93,45 m, con 1 paso peatonal y 1 plaza accesible | 35 |
| **Total** | | **69 ≥ 68 ✔** (2 accesibles) |

- Superficie de la calle-aparcamiento ≈ **1.590 m²**. Recorrido máximo de la plaza a la vivienda ≈ 45 m (casas de la fila 1).
- Puntos débiles:
  - margen de solo 1 plaza;
  - el bloque 2 queda a 3 m de las plazas (paso peatonal con seto).

### 3.6 Ventajas e inconvenientes V2

| | |
|---|---|
| ✔ | **Interior sin coches**: paseos peatonales, plaza en la esquina de acceso y jardín común al NE. Un solo acceso rodado |
| ✔ | Mezcla equilibrada (47 % de unifamiliares). Hileras cortas (28 m) y bloques de 9 viviendas, que dan una escala doméstica |
| ✔ | Los pisos tienen vistas a la ZV-02 y no dan sombra a las casas, porque están al norte y a 22 m |
| ✔ | Viviendas más amplias que en V1 (casas de 4 dormitorios y pisos de ≈ 100 m² útiles) |
| ✔ | Economía: el aparcamiento se concentra en una sola franja, con menos viario por plaza que en V1 |
| ✘ | Entre la fila 1 y la fila 2 hay 9 m, menos que la sombra de invierno (≈ 13,5 m): la PB de la fila 2 queda parcialmente en sombra en diciembre y enero |
| ✘ | La calle-aparcamiento corta la parcela en dos. Las casas de la fila 1 quedan a ≈ 45 m del coche |
| ✘ | El bloque 2 está al límite del retranqueo a la ZV-02 si el arco entra en la parcela (geometría exacta FALTA DATO) |
| ✘ | Depende más del riesgo 4.1: 18 viviendas multifamiliares |

### 3.7 Retícula estructural orientativa V2

- **Unifamiliar:** muros o pórticos en las medianeras **cada 7,00 m**. Forjado de 7,00 m de luz (en el límite razonable del unidireccional; alternativa: viga intermedia en el eje B a 6,0 m de la fachada sur). Fondo de 12,0 m (ejes A-B-C de 6,0 + 6,0). Hileras de 28 m, sin junta.
- **Bloques:**
  - ejes A-B-C: **2 crujías de 6,50 m**;
  - ejes 1 a 6: **5 vanos de 6,16 m** (30,8 m, sin junta);
  - núcleo entre los ejes 3 y 4, en la crujía norte;
  - losa ≈ 6,2 × 6,5 m.
- **Cimentación: FALTA DATO.**

---

## 4. Variante V3 — "Parque central" (8 unifamiliares + 26 pisos)

### 4.1 Idea y volumetría

- **Una sola agrupación unifamiliar** (4 + 4) a la Avda. de la Dehesa: y = 8,5-21,0, x = 20-50 y 56-86, con el **jardín al sur** (≈ 7,8 m) y la entrada al norte desde un paseo junto a la bolsa.
- **Bolsa común compacta** junto a Floristas, en y = 26-58 y x de ≈ −12 a 44. Tiene **dos calles de maniobra E-O** (y = 31-37 y 47-53) conectadas en el extremo este por un tramo N-S (x = 38-44), que forman un **lazo** con entrada por una calle y salida por la otra, las dos a Floristas. Hay 4 filas de plazas.
- **Pisos (26) en tres bloques de 3 plantas y 13,0 m de fondo, dispuestos en arco:**
  - **A** (9 viviendas, 13,0 × 32,0 m): x −15,0 a 17,0, y 64-77, al NO junto a la ZV-02;
  - **B** (9 viviendas, 13,0 × 32,0 m): x 23,0 a 55,0, y 62-75, al norte junto a la ZV-02;
  - **C** (8 viviendas, 13,0 × 28,2 m): x 58,65 a 86,85, y 44-57, al este.
- **Parque central común** de ≈ 2.000 m² (x 44-88, y 21-44, que se prolonga entre B, C y la ZV-02). Es soleado y está abierto visualmente hacia la zona verde.

**Agrupaciones:** Ag-1 = 4 + 4 unifamiliares · bloques de 9 + 9 + 8 (≥ 8; el bloque C tiene exactamente 8).

### 4.2 Tipologías y distribución por plantas

**U-V3, unifamiliar de 7,50 × 12,50 m, 2 plantas, 187,5 m²c, 4 dormitorios + despacho**

| Planta | Estancia | Útil m² |
|---|---|---|
| PB | Salón-comedor (sur) | 34,0 |
| PB | Cocina (norte) | 15,0 |
| PB | Vestíbulo | 6,0 |
| PB | Aseo (zona húmeda) | 3,0 |
| PB | Lavadero (zona húmeda) | 4,5 |
| PB | Despacho | 5,0 |
| PB | Escalera | 5,5 |
| P1 | Dormitorio principal (sur) | 15,0 |
| P1 | Vestidor | 4,0 |
| P1 | Baño principal | 6,0 |
| P1 | Dormitorio 2 (sur) | 11,0 |
| P1 | Dormitorio 3 | 10,5 |
| P1 | Dormitorio 4 | 9,0 |
| P1 | Baño 2 | 5,0 |
| P1 | Distribuidor | 7,0 |
| P1 | Escalera | 5,5 |
| | **Total útil** | **≈ 146,0** |
| | Construida: PB 93,75 + P1 93,75 | **187,5** |

**Bloques M-V3** (1 portal por bloque, núcleo de 28 m² por planta y comunes de PB de ≈ 30 m²)

| Tipo | Ubicación | Nº | Construida privativa m² | Programa | Útil m² |
|---|---|---|---|---|---|
| M-V3-a | A y B, P1 y P2 (3 por planta) | 12 | 129,3 | Salón-comedor 31,0 · cocina 12,5 · dorm. principal 14,5 + baño 5,0 · dorm. 2 11,0 · dorm. 3 10,5 · baño 4,5 · vestíbulo y distribuidor 9,5 · tendedero 4,5 | **103,0** |
| M-V3-b | A y B, PB (3 por planta) | 6 | 119,3 | Salón-comedor 29,0 · cocina 12,0 · dorm. principal 14,0 + baño 5,0 · dorm. 2 11,0 · dorm. 3 10,0 · baño 4,5 · vestíbulo y distribuidor 8,5 · lavadero 3,0 | **97,0** |
| M-V3-c | C, P1 y P2 (3 por planta) | 6 | 112,9 | Salón-comedor 27,0 · cocina 11,0 · dorm. principal 13,5 + baño 4,5 · dorm. 2 10,5 · dorm. 3 9,0 · baño 4,0 · vestíbulo y distribuidor 8,0 | **87,5** |
| M-V3-d | C, PB (2, con jardín) | 2 | 154,3 | Como M-V1-b (4 dormitorios) | **≈ 120,0** |

### 4.3 Cuadro de superficies V3

| Parte | Planta | Construida m² | Computable m²c | No computable m² |
|---|---|---|---|---|
| Unifamiliar (8 × 93,75) | PB | 750,0 | 750,0 | 0 |
| Unifamiliar | P1 | 750,0 | 750,0 | 0 |
| **Subtotal unifamiliar** | | **1.500,0** | **1.500,0** | 0 |
| Bloques A + B (2 × 416,0) | PB / P1 / P2 | 832,0 / 832,0 / 832,0 | 2.496,0 | 0 |
| Bloque C (366,6) | PB / P1 / P2 | 366,6 / 366,6 / 366,6 | 1.099,8 | 0 |
| **Subtotal multifamiliar** | | **3.595,8** (viviendas 3.253,8 + comunes 342) | **3.595,8** | 0 |
| **TOTAL V3** | | **5.095,8** | **5.095,8** (99,9 %) | **0** (H-COM) |

### 4.4 Comprobación urbanística V3 (medición manual)

| Comprobación | Valor V3 | Límite | |
|---|---|---|---|
| Edificabilidad total | 5.095,8 m²c | 5.100 | ✔ |
| Viviendas | 8 + 26 = 34 | 34 | ✔ |
| Ocupación A: unifamiliar | 750 / 2.217,3 (y < 24) = 33,8 % | 60 % | ✔ |
| Ocupación A: multifamiliar | 1.198,6 / 6.621,7 = 18,1 % | 45 % | ✔ |
| Ocupación B | 1.948,6 / 8.839 = 22,0 % | 45 % | ✔ |
| Plantas y cornisa | Igual que V1 y V2 | | ✔ (multifamiliar con margen de ≈ 0,3 m) |
| Retranqueo del bloque A a Floristas (esquina −15,0 ; 64) | ≈ 5,5 m | 5 m | ✔ (justo) |
| Retranqueo del bloque B a la ZV-02 (esquina 55,0 ; 75) | ≈ 5,6 m sobre la cuerda | 5 m | ✔ sobre la cuerda / **✘ si el arco entra en la parcela** (≈ 4,8 m). Mitigación: bajar B 0,5-1,0 m |
| Retranqueo del bloque C a UA-03-02 / a la ZV-02 | 5,0 m / ≈ 17 m | 5 m | ✔ (justo al este) |
| Retranqueo de la fila unifamiliar a la Avda. de la Dehesa / a UA-03-02 | ≥ 7,8 m / 5,85 m | 3 m | ✔ |
| Separación A–B / B–C (esquina con esquina) / unifamiliar–C | 6,0 / 6,2 / 23,0 m | 6 m | ✔ (justo en A–B y B–C) |
| Agrupaciones | 1 × 8 unifamiliares + 9 + 9 + 8 | ≥ 8 | ✔ con H-AGR (es la única variante en la que **todas** las agrupaciones son de 8 o más con edificios de 8-9) |
| Longitud de hilera / bloque | 30 m / 32 m | FALTA DATO | ⚠ Probable ✔ |

### 4.5 Aparcamiento V3 (68 plazas)

| Fila | Tramo (x desde el retranqueo de 5 m a Floristas hasta x = 38) | Plazas |
|---|---|---|
| P1 (y = 26-31) | 41,2 m | 16 |
| P2 (y = 37-42) | 44,8 m | 17 |
| P3 (y = 42-47) | 46,4 m | 18 |
| P4 (y = 53-58) | 50,0 m | 20 |
| **Total** | Se descuenta 1 plaza por las 2 accesibles de 3,70 m | **≈ 70 ≥ 68 ✔** |

Superficie ≈ **1.730 m²** con el lazo. Recorrido máximo de la plaza al portal ≈ 60 m (bloque C).

### 4.6 Ventajas e inconvenientes V3

| | |
|---|---|
| ✔ | **El mayor espacio libre común** (parque central de ≈ 2.000 m² + franja verde junto a la ZV-02), soleado y sin coches |
| ✔ | Fachada sur casi continua: ninguna sombra relevante entre edificios (unifamiliar–C 23 m; A y B en línea) |
| ✔ | Los pisos aprovechan las vistas a la ZV-02 (A, B) y al parque (C). Las casas, grandes (≈ 146 m² útiles), tienen jardín sur |
| ✔ | Huella más baja (22 %) y la menor longitud de cimentación por m²c |
| ✘ | **Es la que más depende del riesgo 4.1**: el 76 % son pisos en una ordenanza "Residencial Unifamiliar Adosada". Si el multifamiliar no se admite o se limita, la variante no sirve |
| ✘ | La bolsa compacta es la "fachada" a Floristas: hay que tratarla con arbolado o pérgola. Una pérgola cubierta podría computar (FALTA DATO), por lo que solo se propone arbolado |
| ✘ | Dos bloques al límite del retranqueo o de la separación: A con Floristas, B con la ZV-02 y B con C |
| ✘ | Más ascensores y núcleos (3) y comunidad mayor. Mezcla de mercado menos típica en el sector |

### 4.7 Retícula estructural orientativa V3

- **Unifamiliar:** medianeras **cada 7,50 m**. Forjado de 7,50 m (en el límite del unidireccional: se recomienda una viga intermedia en el eje B o una losa). Fondo de 12,5 m (ejes A-B-C de 6,25 + 6,25).
- **Bloques A y B:** ejes A-B-C de **2 × 6,50 m** · ejes 1 a 6, **5 vanos de 6,40 m** (32 m).
- **Bloque C:** ejes A-B-C de 2 × 6,50 m · ejes 1 a 6, **5 vanos de 5,64 m** (28,2 m).
- Ninguna pieza supera los 40 m: sin juntas (CTE DB SE-AE 3.4.1).
- **Cimentación: FALTA DATO.**

---

## 5. Tabla comparativa

| Criterio | V1 "Calle de casas" | V2 "Calle-aparcamiento central" | V3 "Parque central" |
|---|---|---|---|
| Reparto unifamiliar + pisos | 24 + 10 | 16 + 18 | 8 + 26 |
| % de viviendas unifamiliares | 71 % | 47 % | 24 % |
| m²c unifamiliar / multifamiliar | 3.744 / 1.350 | 2.688 / 2.402 | 1.500 / 3.596 |
| **m²c total (≤ 5.100)** | 5.094 ✔ | 5.090 ✔ | 5.096 ✔ |
| **Viviendas (= 34)** | 34 ✔ | 34 ✔ | 34 ✔ |
| Huella total / ocupación B (45 %) | 2.322 m² / 26,3 % ✔ | 2.145 m² / 24,3 % ✔ | 1.949 m² / 22,0 % ✔ |
| Ocupación A (cada parte) | 34,7 % / 13,1 % ✔ | 26,5 % / 21,3 % ✔ | 33,8 % / 18,1 % ✔ |
| **Sensibilidad (FALTA DATO):** si el viario y el aparcamiento computaran ocupación con el 45 % sobre toda la parcela (medición manual) | ≈ 3.970 m² → **≈ 44,9 %**: ✔ al límite | ≈ 3.735 m² → ≈ 42,3 % ✔ | ≈ 3.680 m² → ≈ 41,6 % ✔ |
| Separaciones al mínimo de 6 m | Entre hileras | Entre hileras y entre bloques | Entre bloques (A–B, B–C) |
| Retranqueos justos | No | Bloque 2 a la ZV-02 (arco) | Bloque A a Floristas, bloque B a la ZV-02 (arco), C al este |
| Agrupaciones (H-AGR) | 3 × 8 + 10 ✔ | 2 × 8 + 9 + 9 ✔ | 8 + 9 + 9 + 8 ✔ |
| Longitud máxima de hilera | **52 m** ⚠ | 28 m | 30 m |
| Aparcamiento | 48 a la puerta + 22 en bolsa = 70 | Bolsa lineal de 69 | Bolsa compacta de ≈ 70 |
| Viario y aparcamiento pavimentado | ≈ 1.650 m² | ≈ 1.590 m² | ≈ 1.730 m² |
| Accesos rodados a Floristas | 2 | 1 | 2 (lazo) |
| Soleamiento | Muy bueno (A–B 16 m) | Bueno, con sombra de invierno en la PB de la fila 2 (9 m) | Muy bueno |
| Ventilación cruzada | Todas pasantes | Todas pasantes | Todas pasantes |
| Relación con la ZV-02 | 1 bloque con vistas; jardines comunes al N | 2 bloques con vistas; jardín al NE | 2 bloques con vistas; parque central abierto a la ZV |
| Espacio libre común (aprox.) | ≈ 3.800 m² | ≈ 4.200 m² | ≈ 4.700 m² |
| Economía constructiva | **La mejor**: 1 tipología × 24, 1 bloque, 2 núcleos | Media: 2 núcleos, 16 casas | Menor: 3 bloques, 3 núcleos |
| Dependencia del riesgo 4.1 (¿se admite el multifamiliar?) | **Baja** (10 viviendas) | Media (18) | **Alta** (26) |
| Flexibilidad (cambio de reparto) | Baja (malla de calle rígida) | **Alta**: la franja norte admite bloques o casas | Media |

---

## 6. Recomendación razonada (la elección es del arquitecto)

**Se recomienda V1 "Calle de casas", con V2 como alternativa.**

1. **Riesgo normativo.** La parcela está calificada como "Residencial Unifamiliar Adosada (UA)" y no está confirmado que se admita el multifamiliar ni la mezcla (riesgo 4.1). V1 es la que menos depende de ello. Si la normativa lo prohíbe o lo limita, el bloque de 10 viviendas se puede sustituir por hileras sin rehacer el resto del conjunto.
2. **Producto.** Casa adosada con jardín al sur y dos plazas a la puerta. Es lo que mejor encaja con la ordenanza y con el entorno del sector.
3. **Soleamiento y economía.** Las 24 casas con fachada sur y sin sombras entre bandas. Una sola tipología repetida, forjados entre medianeras y un único bloque pequeño.
4. **Condiciones para recomendarla.**
   - Que la longitud de hilera de 52 m sea admisible. Si no, hay una alternativa de frente de 6,30 m con hileras de 4 (2.7).
   - Que el aparcamiento en superficie no compute ocupación o que se aplique la lectura A. En el caso más desfavorable queda al límite (≈ 44,9 %).
   - Que se admitan 2 accesos rodados y un fondo de saco de ≈ 98 m sin martillo.

   Si cualquiera de estas condiciones falla o el arquitecto prefiere un interior sin coches, **V2** es la alternativa equilibrada y la más flexible, con holgura en ocupación y viario.

V3 tiene el mejor espacio libre, pero su viabilidad depende casi por completo del riesgo 4.1. Solo se recomienda si la normativa del Plan Parcial confirma que el multifamiliar se admite sin limitaciones.

---

## 7. Comandos pendientes de ejecutar (generador por partes)

Se han dejado escritos estos archivos de entrada. Cada uno corresponde a la porción de parcela de cada parte, y la línea de reparto es una hipótesis de F2 (H-LIN):

| Archivo | Subparcela (local) | Sup. oficial m² | Edificabilidad m²/m² (= m²c asignados / sup.) | viviendas_max | Hipótesis cambiadas |
|---|---|---|---|---|---|
| `planos/volumetrias/v1_unifamiliar.json` | y < 55 | 5.397,13 | 0,693702 (3.744) | 24 | fondo_adosada 12,0 · ancho_adosada 6,5 |
| `planos/volumetrias/v1_multifamiliar.json` | y > 55 | 3.441,87 | 0,39223 (1.350) | 10 | fondo_bloque 12,0 · 134 m²c/viv |
| `planos/volumetrias/v2_unifamiliar.json` | y < 52 | 5.076,04 | 0,52955 (2.688) | 16 | fondo 12,0 · ancho 7,0 |
| `planos/volumetrias/v2_multifamiliar.json` | y > 52 | 3.762,96 | 0,638435 (2.402,4) | 18 | fondo_bloque 13,0 · 133 m²c/viv |
| `planos/volumetrias/v3_unifamiliar.json` | y < 24 | 2.217,27 | 0,676508 (1.500) | 8 | fondo 12,5 · ancho 7,5 |
| `planos/volumetrias/v3_multifamiliar.json` | y > 24 | 6.621,73 | 0,54303 (3.595,8) | 26 | fondo_bloque 13,0 · 138 m²c/viv |

**Criterios:**
- Superficie oficial de cada parte = polígono de la parte × 0,9797. Las dos partes de cada variante suman 8.839 m².
- Ocupación, plantas, alturas, retranqueos, separación de 6 m y valores `null` sin cambios respecto de F1 6.1 y 6.2.
- Los ajustes de `coordenadas`, `superficie_oficial_m2`, `edificabilidad_m2m2` y `viviendas_max` son los que F1 (sección 6, "Mezcla") indica para ejecutar por partes. La suma de cada variante es ≤ 5.100 m²c y = 34 viviendas.

**Comandos (desde la raíz del repositorio):**

```bash
for f in v1_unifamiliar v1_multifamiliar v2_unifamiliar v2_multifamiliar v3_unifamiliar v3_multifamiliar; do
  python3 scripts/volumetria_generador.py planos/volumetrias/$f.json --lados
  python3 scripts/volumetria_generador.py planos/volumetrias/$f.json > planos/volumetrias/resultado_$f.txt
  python3 scripts/volumetria_generador.py planos/volumetrias/$f.json --json --sin-dxf > planos/volumetrias/resultado_$f.json
done
# Control de techo y huella de cada parte (urbanismo_calculo.py)
python3 scripts/urbanismo_calculo.py --parcela 5397.13 --edificabilidad 0.693702 --ocupacion 60 --plantas 2
python3 scripts/urbanismo_calculo.py --parcela 3441.87 --edificabilidad 0.39223  --ocupacion 45 --plantas 3
python3 scripts/urbanismo_calculo.py --parcela 5076.04 --edificabilidad 0.52955  --ocupacion 60 --plantas 2
python3 scripts/urbanismo_calculo.py --parcela 3762.96 --edificabilidad 0.638435 --ocupacion 45 --plantas 3
python3 scripts/urbanismo_calculo.py --parcela 2217.27 --edificabilidad 0.676508 --ocupacion 60 --plantas 2
python3 scripts/urbanismo_calculo.py --parcela 6621.73 --edificabilidad 0.54303  --ocupacion 45 --plantas 3
```

**Qué comprobar al ejecutarlos** (resultados todavía **NO calculados**):

1. Con `--lados`, que los índices de cada parte coinciden:
   - unifamiliar: 0 = E, 1 = S (Dehesa), 2 = O (Floristas), 3 = línea interior;
   - multifamiliar: 0 = E, 1 = línea interior, 2 = O (Floristas), 3-5 = N (ZV-02).
2. Que la `unifamiliar_adosada` sale orientada a ≈ 0,5° (E-O), paralela a la Dehesa.
3. Que ninguna parte sale `FALTA DATO` ni `NO CABE`.
4. Que el techo computable de cada parte coincide con los m²c asignados.

**Límites del generador:** no modela calles, aparcamiento ni agrupaciones de 8, y rellena la parte con todas las hileras o bloques que caben. Su huella y su número de piezas **no coincidirán** con el trazado de las variantes. Sirven como comprobación de capacidad y de parámetros por parte, no como el proyecto.

---

## 8. Decisiones que necesita el arquitecto

1. **Variante:** V1 (recomendada), V2 o V3, o una combinación (por ejemplo, el trazado de V2 con el reparto de V1).
2. **Reparto y tamaño de las viviendas** (H-REP), según la variante elegida:
   - V1: casas de 156 m²c y 3 dormitorios; pisos de 98,5 y 156 m²c;
   - V2: casas de 168 m²c y 4 dormitorios; pisos de 114-124 m²c;
   - V3: casas de 187,5 m²c; pisos de 113-154 m²c.

   ¿Algún objetivo de producto, como número de dormitorios o superficie máxima de piso?
3. **Agrupación de 8 (riesgo 4.15):** ¿se acepta H-AGR?
   - agrupaciones de al menos 8;
   - la regla de 8 exactos se aplica a las unifamiliares;
   - las 2 viviendas sobrantes van a la parte multifamiliar.

   ¿O se aplica a todos los edificios?
4. **Separación de 6 m (riesgo 4.16):** ¿vale también entre hileras de una misma agrupación y entre bloques? En las tres variantes hay separaciones exactamente de 6 m. Si la normativa exige más, o una distancia ligada a la altura, hay que revisar V1 (banda B) y V3 (bloques).
5. **Aparcamiento** (H-APA-1 a 4):
   - ¿se aceptan las dimensiones de plaza y de calle de maniobra (2,50 × 5,00 m y 6,00 m), a falta de la ordenanza?
   - ¿2 plazas accesibles?
   - ¿plazas fuera de las bandas de retranqueo?
   - ¿fondo de saco sin martillo?
   - ¿recogida de residuos desde Floristas?
   - ¿se admiten 2 accesos rodados a Floristas (V1, V3)?
6. **Longitud de hilera** (V1, 52 m): ¿se mantiene a la espera de la normativa o se pasa ya a la alternativa de 4 + 4 + 4 con frente de 6,30 m?
7. **Geometría de los arcos de la ZV-02 y de la Avda. de la Dehesa** (F1 5.1-19): en V2 y V3 hay bloques que podrían incumplir el retranqueo de 5 m si el arco entra en la parcela. ¿Se aporta la geometría exacta o se desplazan ya los bloques 1,0 m al sur?
8. **Cubierta y castilletes** (H-CUB): ¿se acepta proyectar sin bajo cubierta ni ático, con castillete de ascensor pendiente de la normativa? La cornisa del multifamiliar queda a ≈ 9,7 m de los 10 m permitidos, sin topografía.
9. **Pendientes para F3** (no se resuelven aquí):
   - geotecnia (CTE DB SE-C), que el arquitecto ha decidido no encargar;
   - topografía;
   - servicios urbanos y acometidas;
   - elemento de la esquina SE: se deja libre en las tres variantes;
   - normativa del Plan Parcial.
10. **Ejecución del generador por partes:** que el coordinador ejecute los comandos del apartado 7 y se incorporen sus resultados antes de cerrar F2 o al comienzo de F3.

No se han anotado conflictos en `fases/conflictos.md`: en F2 todavía no hay conflictos entre disciplinas. Los puntos de riesgo para F3 se recogen en el apartado 8.9.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
