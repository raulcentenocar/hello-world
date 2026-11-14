# F3 — Instalaciones · Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Cañada) · Variante V1 «Calle de casas»

Agente: instalaciones · Fecha: 2026-11-14 · Base: `fases/01_urbanismo.md` (rev. 2, aprobada), `fases/02_diseno.md` (aprobada; **V1** elegida por el arquitecto con sus hipótesis tal cual), `fases/conflictos.md`, `datos/UA 03 01.pdf`.

> **Aviso de método.**
> - `datos/` solo contiene la cédula urbanística. **No hay ningún dato de acometidas, servicios urbanos, compañías suministradoras, presiones, cotas de alcantarillado ni topografía.** Todo eso es **FALTA DATO** y no se supone.
> - Cuando empecé, `fases/03_estructura.md` y `fases/03_normativa.md` **no existían** (los tres agentes trabajan en paralelo). La coordinación con estructura parte de la retícula orientativa de F2 (2.7). Los cruces se anotan en `fases/conflictos.md`.
> - En esta sesión **no tengo herramienta de ejecución de comandos** y en `scripts/` no hay ningún script de instalaciones. Las cifras de este documento son **valores de tabla de la norma citada** o **estimaciones manuales de anteproyecto**, marcadas como tales. **Propuesta:** crear `scripts/instalaciones_calculo.py` (caudales HS 4 con simultaneidad, UD de HS 5, caudales HS 3, previsión de cargas ITC-BT-10) para que estas cifras sean reproducibles antes del proyecto básico.
> - Todas las hipótesis se identifican con un código **H-I…** y la norma de referencia.

---

## 0. Resumen

| Instalación | Unifamiliares (24 casas U-V1) | Bloque M-V1 (10 pisos, 2 portales) |
|---|---|---|
| **Fontanería** (DB-HS 4) | Acometida general desde Calle Floristas (FALTA DATO) · red comunitaria enterrada bajo la calle interior · contador individual en hornacina de la fachada de cada casa | Batería de contadores divisionarios en el cuarto de instalaciones de cada portal · montantes por patinillo registrable desde el rellano |
| **ACS** (DB-HE 4) | Aerotermia individual con depósito de ≈ 200 L en el lavadero | **Opción A (base):** aerotermia individual con unidad exterior en cubierta y módulo interior de ≈ 0,8-1,0 m² por piso · **Opción B:** producción centralizada en cubierta. Decide el arquitecto |
| **Saneamiento** (DB-HS 5) | **Red interior separativa** (obligatoria aunque la municipal sea unitaria). Tipo de red municipal: **FALTA DATO**. 1 bajante de fecales Ø110 por casa, en el patinillo · colectores enterrados hasta los colectores comunitarios bajo la calle interior | 2 bajantes de fecales Ø110 por portal · 4 bajantes de pluviales · colectores hasta Floristas por la bolsa del bloque |
| **Ventilación** (DB-HS 3) | **Mecánica de simple flujo higrorregulable** (base). Doble flujo como alternativa (ver alturas libres). Campana con conducto exclusivo hasta cubierta | Ídem, con conducto colectivo de extracción por patinillo y aspirador en cubierta; conducto individual de campana por vivienda |
| **Climatización** (RITE, DB-HE 0/1) | Aerotermia aire-agua + suelo radiante-refrescante | Ídem (opción A) o centralizada (opción B) |
| **Contribución renovable** | ACS: ≥ 60 % de la demanda con la aerotermia (HE 4). FV en cubierta como previsión; **obligación por HE 5: la debe confirmar normativa** | Ídem; FV en la cubierta del bloque para servicios comunes o autoconsumo colectivo |
| **Electricidad** (REBT) | Electrificación **elevada** (9,2 kW). CPM en la fachada de cada casa, desde una red de BT de la compañía bajo la calle interior (por confirmar con la compañía) | Electrificación **elevada**. CGP → LGA → centralización en armario por portal (≤ 16 contadores) |
| **Recarga VE** (ITC-BT-52, DB-HE 6) | 48 plazas: punto de recarga en la plaza de cada casa, con circuito propio desde el cuadro de la vivienda | Bolsa de 22 plazas: conducción principal comunitaria y preinstalación en el 100 % de las plazas |
| **ICT** (RD 346/2011) | Aplica si el conjunto queda en régimen de propiedad horizontal o conjunto inmobiliario (régimen: **FALTA DATO**). Canalización enterrada bajo la calle interior hasta un registro en cada casa | RITI/RITU en PB y RITS en el castillete |
| **Previsión de cargas** | **≈ 240 kW** para el conjunto (estimación manual, ITC-BT-10). **Supera los 100 kW**: es probable que la compañía exija **reservar un local para centro de transformación** | |

**Puntos críticos** (detalle en el apartado 10 y en `fases/conflictos.md`):
1. Posible **centro de transformación** necesario y sin espacio reservado en V1. Relación con el elemento sin identificar de la esquina SE (**FALTA DATO**).
2. **Equipos en cubierta** (aerotermia, FV, salidas de ventilación, antenas, castillete) por encima de la cornisa. Que se admitan entre cornisa y coronación es **FALTA DATO**, y el bloque tiene solo ≈ 0,3 m de margen de cornisa.
3. **Alturas libres** justas con 3,00 m de suelo a suelo y suelo radiante. No se puede subir la altura de planta del bloque.
4. **Patinillo unifamiliar de 0,60 × 0,40 m insuficiente**. Se propone 0,80 × 0,40 m.
5. **Espacio para el módulo interior de aerotermia** en los pisos M-V1-a, que no tienen lavadero.
6. **Cotas de saneamiento**: colector de ≈ 100 m hasta Floristas sin topografía ni cota de la red municipal. Riesgo de bombeo.

---

## 1. Datos de partida y hipótesis

### 1.1 Datos de V1 usados (de F2, sin cambios)

- **24 unifamiliares U-V1** de 6,50 × 12,00 m, PB + P1, 156 m²c y 3 dormitorios.
  - **Banda A** (sur de la calle): entrada y plazas al norte, zona húmeda en la crujía norte (calle).
  - **Banda B** (norte de la calle): entrada y plazas al sur, zona húmeda en la crujía sur (calle).
  - En los dos casos **la zona húmeda y el patinillo quedan del lado de la calle interior**, lo que acorta acometidas y colectores.
- **Calle interior** E-O de 6 m (y = 26-32), con bandas de plazas de 5 m a cada lado (y = 21-26 y 32-37). Fondo de saco de ≈ 98 m desde Floristas.
- **Bloque M-V1**: 12,0 × 37,5 m, PB + 2, en x = 19,5-57,0 / y = 61-73. **2 portales**, cada uno con 1 vivienda en PB (M-V1-b, 156 m², 4 dormitorios, con lavadero) y 2 por planta alta (M-V1-a, 98,5 m², 3 dormitorios, **sin lavadero ni tendedero**).
  - Por portal en PB: portal de 18 m², cuarto de contadores e instalaciones de 8 m², cuarto de bicicletas y basuras de 15 m².
  - Losa de ≈ 6,0 × 6,25 m. Núcleos entre los ejes 2-3 y 5-6.
- **Bolsa del bloque**: 22 plazas (1 accesible) junto a Floristas, en y = 57-73.
- **Altura de planta 3,00 m** de suelo a suelo; cota de PB +0,30 m. Cornisa del bloque ≈ 9,7 m (límite 10 m) y de las casas ≈ 6,6 m (límite 7,5 m). **Sin sótano, sin ático ni bajo cubierta.**
- Residuos: recogida desde Calle Floristas (dato del encargo). Por la calle interior solo circulan turismos.

### 1.2 FALTA DATO que condiciona esta fase

Servicios urbanos existentes y puntos de acometida (agua, saneamiento, BT/MT, telecomunicaciones) · compañías suministradoras y sus normas particulares · presión de la red de agua · tipo de red de alcantarillado (separativa o unitaria) y su cota · topografía y rasantes · **naturaleza del elemento de la esquina SE** · régimen jurídico del conjunto (propiedad horizontal, conjunto inmobiliario o división horizontal tumbada) · ordenanza municipal de alturas libres y de vertidos · zona de radón del municipio (DB-HS 6) · normativa del Plan Parcial sobre instalaciones en cubierta.

### 1.3 Hipótesis técnicas declaradas

| Código | Hipótesis | Norma de referencia |
|---|---|---|
| H-I1 | **Zona climática D3**, por la altitud aproximada del municipio (≈ 600-650 m), **sin topografía**. Hay que confirmarla con la cota real | CTE DB-HE, Anejo B (Madrid: D3 entre 550 y 750 m) |
| H-I2 | Ocupación para ACS: 3 dormitorios → 4 personas; 4 dormitorios → 5 personas. **28 L/día·persona a 60 °C** | DB-HE 4, Anejo F |
| H-I3 | Caudales instantáneos mínimos por aparato según la tabla de la norma. Simultaneidad con UNE 149201, **pendiente de calcular con script** | DB-HS 4, tabla 2.1; UNE 149201 |
| H-I4 | Caudales de ventilación de **caudal constante** según la tabla 2.1. No se usa la opción de caudal variable por CO₂ | DB-HS 3 (2019), tabla 2.1 |
| H-I5 | Intensidad pluviométrica **i = 90 mm/h** (Madrid: zona A, isoyeta 30). **A verificar en el mapa del Anejo B** | DB-HS 5, Anejo B |
| H-I6 | Potencia térmica orientativa de anteproyecto: ≈ 40 W/m² útil en calefacción (casa ≈ 5-6 kW; piso ≈ 4 kW). **Predimensionado**, no cálculo de cargas | RITE IT 1.2; UNE-EN 12831 en proyecto |
| H-I7 | Grado de electrificación **elevado** (9.200 W) en todas las viviendas, por la previsión de bomba de calor (calefacción y aire acondicionado eléctricos) | REBT ITC-BT-10, 2.1 y 2.2 |
| H-I8 | Canto de forjado: casas ≈ 0,30 m (unidireccional de 6,50 m de luz); bloque ≈ 0,28 m (losa de 6,0 × 6,25 m). **Lo fija estructura**: es solo un valor de comprobación | Estimación L/22-L/25 |
| H-I9 | Paquete de suelo radiante (aislamiento, tubo, mortero y acabado): **0,12 m** | UNE-EN 1264 (orden de magnitud) |
| H-I10 | Altura libre mínima de referencia: **2,50 m en estancias y 2,20 m en baños, pasillos y zonas de paso**. **La norma aplicable (ordenanza municipal o de la Comunidad de Madrid) es FALTA DATO** | Valores habituales; por confirmar por normativa |
| H-I11 | Sin red de gas: edificio todo eléctrico (aerotermia y cocina de inducción) | Decisión técnica propuesta, coherente con HE 0 |

---

## 2. Fontanería (DB-HS 4)

### 2.1 Criterio de diseño

- **Una sola acometida general** para la promoción, desde la red de Calle Floristas (punto, diámetro y presión: **FALTA DATO**). En la entrada de la calle interior se coloca el **armario del contador general** o de la llave de registro, en el límite de la parcela, según las normas de la compañía. Previsiblemente es el Canal de Isabel II, **a confirmar**.
- **Red comunitaria enterrada** de PE-100 en anillo o en ramal bajo la franja de plazas de cada banda (no bajo la rodadura), con una derivación a cada casa y otra al bloque.
- **Contadores divisionarios**:
  - **Casas:** en una **hornacina en la fachada de entrada** de cada casa, junto a la CPM eléctrica (HC-U, apartado 8), accesible desde el paso peatonal de 1,50 m entre plazas. **El criterio de la compañía sobre contadores en vial privado: FALTA DATO.** Si exige que todos los contadores sean accesibles desde la vía pública, habría que **agruparlos en baterías en la entrada desde Floristas**. Esa opción da derivaciones de hasta ≈ 90 m y pide un armario de ≈ 3-4 m de frente en el límite de la parcela.
  - **Bloque:** **batería de contadores en el cuarto de instalaciones** de cada portal (5 viviendas + 1 de servicios comunes por portal). La batería debe tener sumidero y desagüe (HS 4, 3.2.1.2).
  - Contadores adicionales para **riego** de zonas comunes y **servicios comunes**.
- **Presión.** Con PB + 2 y aparatos a ≤ 6,5 m sobre la rasante, previsiblemente **no hace falta grupo de presión**. Pero la presión de la red es **FALTA DATO**: si en el punto más desfavorable es inferior a 100 kPa (grifos) o 150 kPa (fluxores y calentadores), según HS 4 2.1.3, hace falta un grupo en el cuarto del bloque, de ≈ 1,5 m² más. Si supera 500 kPa, hacen falta **reductoras de presión**.
- **Separación AFS/ACS** y aislamiento según RITE IT 1.2.4.2.1. Las tuberías de agua fría, a ≥ 4 cm de las calientes y por debajo de ellas (HS 4, 5.1.2).
- **Hidrante exterior.** DB-SI 4 (tabla 1.1) exige 1 hidrante en uso residencial vivienda entre 5.000 y 10.000 m² construidos. V1 suma **5.094 m²**, pero en **edificios independientes de menos de 5.000 m²**. Si es exigible, o si basta con los hidrantes públicos de la urbanización, lo debe confirmar el **agente de normativa**. Si lo es, se conecta a la acometida general antes del contador, con su propia válvula.

### 2.2 Caudales instantáneos (H-I3, tabla 2.1 de HS 4)

| Vivienda | Aparatos (hipótesis según el programa de F2) | Σ AF l/s | Σ ACS l/s |
|---|---|---|---|
| U-V1 (casa) | Aseo (lavabo, inodoro) · cocina (fregadero, lavavajillas) · lavadero (lavadora) · baño principal (lavabo, inodoro, ducha) · baño 2 (lavabo, inodoro, ducha) | 1,55 | 0,50 |
| M-V1-a (piso) | Cocina (fregadero, lavavajillas, lavadora) · baño (lavabo, inodoro, ducha) · baño 2 (lavabo, inodoro, ducha) | 1,15 | 0,33 |
| M-V1-b (piso PB) | Como U-V1, con aseo | 1,55 | 0,50 |

(Valores unitarios de la tabla 2.1: lavabo 0,10 / 0,065; inodoro con cisterna 0,10; ducha 0,20 / 0,10; fregadero doméstico 0,20 / 0,10; lavavajillas doméstico 0,15; lavadora doméstica 0,20. Se toma la lavadora y el lavavajillas solo con AF.)

**Caudal punta y diámetros:** con UNE 149201, **pendiente de script**. Orden de magnitud manual para una casa: ≈ 0,7 l/s, que da una alimentación de vivienda de DN 25-32. El diámetro de la acometida general depende de la presión y de las normas de la compañía: **FALTA DATO**.

### 2.3 Recorrido general

- **Casas:** acometida → contador en la hornacina de fachada → llave de paso a la entrada (HS 4, 3.2.1.3) → montante por el patinillo PU → derivaciones a cocina y aseo (PB) y a los baños (P1), todos en la misma crujía. **Recorrido interior muy corto.** El depósito de ACS va en el lavadero (2.4).
- **Bloque:** acometida → batería (cuarto CI-1 / CI-2) → **montantes individuales** por los patinillos PB-1 a PB-4, registrables desde el rellano (zona común, HS 4, 3.2.1.2.6) → llave de paso a la entrada de cada vivienda.

### 2.4 Producción de ACS (ver también el apartado 5)

| | Demanda (H-I2) | Producción |
|---|---|---|
| Casa U-V1 | 4 pers. × 28 = **112 L/día** | Bomba de calor aire-agua individual. **Depósito de 180-200 L** (bomba de calor + depósito, o módulo con depósito integrado), en el lavadero de PB (≈ 0,6 × 0,7 m de planta, h ≈ 1,9 m). Cabe en los 4 m² de lavadero y despensa, aunque reduce la despensa |
| Piso M-V1-a | 112 L/día | **Opción A:** módulo interior con depósito integrado en un **armario de ≈ 0,8-1,0 m²** dentro de la vivienda. **No está en el programa de F2** (conflicto, apartado 10) · **Opción B:** central en cubierta y **estación de transferencia o contador de energía** por vivienda (≈ 0,6 × 0,2 m en pared) |
| Piso M-V1-b | 5 pers. × 28 = **140 L/día** | Como la casa, en su lavadero de 4,5 m² |
| **Total conjunto** | 24 × 112 + 8 × 112 + 2 × 140 = **3.864 L/día** | < 5.000 L/día → **contribución renovable mínima del 60 %** (HE 4, 3.1) |

Prevención de legionelosis: acumulación a ≥ 60 °C con ciclo de choque en la opción B (instalación colectiva, RD 487/2022). En las instalaciones individuales, programación antilegionela del equipo como buena práctica.

---

## 3. Saneamiento (DB-HS 5)

### 3.1 Criterio de diseño

- **Tipo de red municipal (separativa o unitaria): FALTA DATO.** Por ser un sector de urbanización reciente (reparcelación de 2024) es posible que sea separativa, pero **no se da por hecho**.
- **La red interior se proyecta separativa en cualquier caso** (fecales y pluviales). Si la red municipal es unitaria, las dos se unen en una **arqueta final antes de la acometida** (HS 5, 3.3.1.1). Así la red interior no cambia sea cual sea el dato.
- **Acometidas a Floristas:** una de fecales y otra de pluviales, con **pozo o arqueta general de registro** en el interior de la parcela, junto al límite (HS 5, 3.3.1.5). Se proponen **dos puntos de vertido** (calle de casas y bolsa del bloque) o uno solo con un colector perimetral. Lo decide la cota de la red municipal (**FALTA DATO**).
- **Cotas, riesgo principal.** El colector de la calle interior mide ≈ 100 m (desde la casa más al este, x ≈ 87, hasta Floristas). Con una pendiente del 1,5-2 % y un arranque a −0,60 m, llega a Floristas a una profundidad de **≈ −2,1 a −2,6 m**. **Sin topografía ni cota del alcantarillado no se puede comprobar el vertido por gravedad.** Si la red municipal está más alta, hará falta un **pozo de bombeo** (≈ 2 × 2 m) en la zona libre, junto a Floristas. Hay que pedir las cotas cuanto antes.
- **Pluviales de viario:** ≈ 1.650 m² de calle y plazas (F2). Rejillas lineales o imbornales con colector propio. **Laminación o retención (aljibe o SUDS)** si la ordenanza municipal de vertidos lo exige: **FALTA DATO**. Se recomienda pavimento drenante en las plazas para reducir el caudal punta, a decidir por el arquitecto.

### 3.2 Unidades de desagüe y bajantes (HS 5, tablas 4.1 y 4.4)

| Vivienda | UD (uso privado) | Bajante de fecales | Ventilación |
|---|---|---|---|
| U-V1 | Aseo 5 + cocina 6 + lavadero 3 + baño principal 7 + baño 2 7 = **28 UD** | **1 × Ø110** (mínimo Ø100 por el inodoro) en el patinillo PU | **Primaria**: la bajante se prolonga 1,30 m sobre la cubierta no transitable (2,0 m si es transitable). Basta con primaria en edificios de menos de 7 plantas (HS 5, 3.3.3.1) |
| Portal del bloque | 2 columnas: (P1 + P2) × 17 UD + PB (≈ 28 UD repartidas) | **2 × Ø110** por portal (una por patinillo húmedo) | Primaria en cubierta |

Si alguna salida de ventilación primaria no puede ir a cubierta, se admite una **válvula de aireación** registrable en el patinillo.

### 3.3 Pluviales (H-I5, i = 90 mm/h; HS 5, tablas 4.6 y 4.8, f = 0,9)

| Cubierta | Superficie en planta | Sumideros (si es plana) | Bajantes |
|---|---|---|---|
| Casa (78 m²) | 78 m² | 2 (< 100 m²) | **1 × Ø75** (admite ≈ 197 m² con f = 0,9). Por la fachada de la calle, exterior o empotrada; no ocupa patinillo |
| Bloque (450 m²) | 450 m² | 4 (200-500 m²) | **4 × Ø75** (2 por fachada) o 2 × Ø90. Exteriores o en rozas de fachada, fuera de los patinillos |

### 3.4 Colectores y arquetas

- **Sin sótano.** Los colectores interiores van **enterrados bajo la solera o la cámara sanitaria** (lo define estructura), con pendiente ≥ 2 %. A pie de cada bajante, una **arqueta a pie de bajante** fuera del edificio. Arquetas en cada encuentro, cambio de dirección y tramo largo, según HS 5, 3.3.1.4-5.
- **Casas:** arqueta a pie de bajante en la franja de entrada → ramal de ≈ 6-8 m bajo la plaza → **colector comunitario de fecales** (Ø200-250 PVC-U SN4 o PP corrugado SN8) y **colector de pluviales** (Ø250-315) **bajo la calle interior**, con pozos de registro cada 30-50 m y en los cambios de dirección. Tapas **D400** (UNE-EN 124) en la rodadura.
- Los **jardines privados** (sur en la banda A, norte en la B) no llevan pluviales a la red, salvo una rejilla en la salida al jardín si la pendiente lo exige.
- **Bloque:** colectores enterrados en PB → arquetas en la fachada sur → colector bajo la bolsa (y ≈ 62-68) → arqueta general junto a Floristas.

### 3.5 Sección tipo de servicios de la calle interior (propuesta)

Banda de 16 m (plazas 5 + calle 6 + plazas 5):
- **bajo la calle (6 m):** colector de pluviales en el eje y colector de fecales a ≥ 1,0 m, más profundo;
- **bajo cada banda de plazas (5 m):** agua (≥ 0,20 m de la red de BT), red de BT, telecomunicaciones (ICT) y alumbrado exterior y recarga VE.

Separaciones según las normas de las compañías: **FALTA DATO**. El ancho es suficiente.

---

## 4. Ventilación (DB-HS 3)

### 4.1 Sistema

- **Base: ventilación mecánica de simple flujo, con extracción higrorregulable.**
  - **Admisión** por aireadores en la carpintería o el cajón de persiana de los locales secos.
  - **Paso** por la holgura de las puertas (≥ 70 cm² u 8·qvp).
  - **Extracción** en cocina, baños, aseo y lavadero.
- **Se descarta como base el doble flujo con recuperador**, aunque mejora el HE 0, porque obliga a llevar conductos de impulsión a todos los locales secos por falso techo, y las alturas libres no lo permiten (apartado 9).
- **Alternativa:** doble flujo con impulsión solo por falso techo de pasillos y distribuidores, y toberas de largo alcance hacia los dormitorios. Hay que validarla con el cálculo de HE 0 y con la altura libre definitiva.
- **Cocina:** campana con extracción mecánica **independiente** de la ventilación general y **conducto exclusivo hasta cubierta**. Caudal de referencia de **50 l/s** (HS 3, 3.1.1). Compuerta antirretorno.
- **Expulsión por cubierta.** Las bocas a ≥ 1 m sobre la cubierta y a las distancias de HS 3, 3.2.4. Por eso los conductos ocupan el patinillo y cruzan todos los forjados.

### 4.2 Caudales por vivienda (H-I4, tabla 2.1 de HS 3, l/s)

| Vivienda | Admisión en secos | Extracción en húmedos | Caudal de diseño (equilibrado) | Campana |
|---|---|---|---|---|
| U-V1 (3 dorm.) | Dorm. principal 8 + dorm. 2 4 + dorm. 3 4 + salón-comedor 10 = **26** | 5 locales húmedos × 8 = 40 ≥ 33 → **40** | **40 l/s (144 m³/h)**. La admisión se reparte en proporción hasta 40 | 50 |
| M-V1-a (3 dorm.) | 8 + 4 + 4 + 10 = **26** | 3 × 8 = 24 < 33 → **33** | **33 l/s (119 m³/h)** | 50 |
| M-V1-b (4 dorm.) | 8 + 4 + 4 + 4 + 10 = **30** | 5 × 8 = 40 → **40** | **40 l/s (144 m³/h)** | 50 |

**Locales comunes del bloque:** almacén de residuos (parte del cuarto de 15 m² de bicicletas y basuras): **10 l/s·m²** (tabla 2.1). La superficie destinada a residuos no está definida en F2: con la hipótesis de ≈ 5 m² salen 50 l/s, con extracción a cubierta o a fachada según HS 3, 3.1.2. Cuarto de contadores: ventilación natural según la compañía.

### 4.3 Secciones de conducto (HS 3, 4.2.2: S ≥ 2,50·qv cm², con ventilación mecánica)

- Extracción individual de 40 l/s: S ≥ 100 cm² → **Ø125**.
- Conducto colectivo por columna del bloque (≈ 3 viviendas, ≈ 110 l/s): S ≥ 275 cm² → **Ø200**.
- Campana de 50 l/s: S ≥ 125 cm² → **Ø150** (recomendado, por el ruido).

### 4.4 Equipos y recorrido

- **Casas:** extractor individual (≈ 0,35 × 0,35 × 0,25 m) en el falso techo del baño de P1, junto al patinillo, o extractor de cubierta. Los conductos de PB (cocina, aseo, lavadero) suben por el patinillo PU. Un conducto Ø125 de extracción general y otro Ø150 de campana, los dos hasta cubierta.
- **Bloque:** un **conducto colectivo Ø200** por patinillo húmedo, con **aspirador mecánico en cubierta**, más bocas higrorregulables y compuertas de cada vivienda. **Conducto individual Ø150 de campana por vivienda**, también por el patinillo. En el tramo más cargado (PB) caben hasta 3 campanas por patinillo.

---

## 5. Climatización y ACS (RITE, DB-HE 0/1/4/5)

### 5.1 Sistema propuesto

- **Generación: bomba de calor aire-agua (aerotermia)** para calefacción, refrigeración y ACS.
  - Equipo **monobloc con refrigerante natural (R290)** o split con hidrokit. El monobloc lleva agua y no refrigerante por el patinillo, con protección antihielo.
  - Potencia orientativa (H-I6): casa **6-8 kW**; piso **4-6 kW**.
- **Emisión:** **suelo radiante-refrescante** en PB y P1, con control de punto de rocío en refrigeración. Se recomienda **preinstalación de split o fancoil en el salón**, porque el suelo refrescante tiene una potencia frigorífica limitada (opción para el arquitecto).
  - Colector de suelo radiante por planta, en un armario empotrado de ≈ 0,8 × 0,15 m.
  - En la casa, en PB junto a la escalera y en P1 en el distribuidor. En el piso, en el vestíbulo.
- **Control y contabilización:** termostato por estancia principal (RITE IT 1.2.4.3). En la opción B, contador de energía por vivienda (RITE IT 1.2.4.4).

### 5.2 Ubicación de las unidades exteriores

| Edificio | Propuesta | Alternativa | Observaciones |
|---|---|---|---|
| Casa | **En cubierta** (≈ 1,1 × 0,45 × 0,95 m + espacio libre ≈ 1,5 m²) | En el jardín junto a la fachada, sobre bancada antivibratoria y a ≥ 1,5-2 m de la medianera | En cubierta sobresale de la cornisa (≈ 6,6 + 1,0 m = 7,6 m > 7,5 m, **aunque por debajo de la coronación de 10,5 m**). Admisibilidad: **FALTA DATO**. En el jardín: ruido hacia el vecino y pérdida de jardín |
| Bloque, opción A | **10 unidades en la cubierta del bloque**, agrupadas en una **zona de equipos de ≈ 20-25 m²** junto a los castilletes | Patio de instalaciones en la planta baja, en la zona libre al norte (≈ 25 m², vallado) | En cubierta: 9,7 + 1,0 m > 10 m de cornisa (coronación 13 m). Admisibilidad: **FALTA DATO** |
| Bloque, opción B | **Central de producción en cubierta**: 2 bombas de calor en cascada de ≈ 30 kW cada una (suma < 70 kW, así que **no requiere sala de máquinas** según RITE IT 1.3.4.1.2) + depósito de ACS de ≈ 1.000 L con factor de centralización de HE 4, Anejo F, en un recinto de cubierta de ≈ 8 m² | En el cuarto de PB, ampliado a ≈ 12 m² | Reduce el espacio dentro de las viviendas, pero requiere comunidad de gestión, contadores de energía y recirculación de ACS |

**Recomendación:** la **opción A** por coherencia con las casas, por la gestión individual y por su sencillez. Requiere resolver el armario interior de los pisos M-V1-a (conflicto). **Decide el arquitecto.**

### 5.3 Contribución renovable y cumplimiento de DB-HE

- **HE 4 (ACS).** Contribución renovable mínima del **60 %** de la demanda (< 5.000 L/día). La bomba de calor computa como renovable si su **SCOP o SPF estacional es > 2,5** (energía ambiente según la Decisión 2013/114/UE). Equipos actuales de aerotermia en zona D3: SCOP en ACS ≈ 2,8-3,5, así que se cumple **con la ficha del equipo elegido** (comprobar en proyecto).
- **HE 0 y HE 1.** Con aerotermia, ventilación mecánica higrorregulable y envolvente según HE 1 en zona D3 (H-I1), es previsible cumplir los límites de consumo de energía primaria no renovable y total. **Hay que verificarlo con la herramienta oficial (HULC o equivalente) en el proyecto.** El doble flujo mejora el margen si hiciera falta.
- **HE 5 (generación eléctrica renovable).** Su ámbito y su exigencia para **uso residencial privado** dependen de la versión vigente del CTE (RD 732/2019, modificado por RD 450/2022) y de la superficie construida (bloque de 1.350 m²; conjunto de 5.094 m² en edificios independientes). **No lo doy por resuelto: lo debe confirmar el agente de normativa.** Previsión en cualquier caso:
  - **Bloque:** FV en cubierta de **≈ 10-15 kWp** (≈ 60-90 m² de módulos) para servicios comunes y autoconsumo colectivo (RD 244/2019), compatible con la zona de equipos.
  - **Casas:** FV opcional de ≈ 2-3 kWp por casa en su cubierta (≈ 12-18 m²), o preinstalación con tubo vacío desde la cubierta hasta el cuadro.
  - Mejor **coplanar o con poca inclinación** para no sobrepasar la cornisa (ver conflicto de cubiertas).
- **HE 6 (infraestructura de recarga de VE):** apartado 6.4.

---

## 6. Electricidad (REBT)

### 6.1 Grado de electrificación y previsión de cargas (ITC-BT-10; **estimación manual, pendiente de script**)

| Concepto | Cálculo (ITC-BT-10) | kW |
|---|---|---|
| Viviendas del bloque (10, elevada) | 9,2 kW × coef. 8,5 (n = 10) | 78,2 |
| Servicios generales del bloque (hipótesis) | 2 ascensores × 4,5 kW + alumbrado de zonas comunes ≈ 1 kW + ventilación y aspiradores ≈ 1 kW + grupo de presión (reserva) ≈ 2 kW + ICT ≈ 0,5 kW | ≈ 13,5 |
| Recarga VE, bolsa del bloque (22 plazas) | 3,68 kW × 0,1 × 22, **con SPL** (sistema de protección de la LGA) (ITC-BT-10 en la redacción del RD 1053/2014 e ITC-BT-52; apartado exacto a verificar) | ≈ 8,1 |
| **Total del bloque** | | **≈ 100 kW** |
| Casas (24, elevada) | 9,2 kW × coef. 16,8 (n = 24: 15,3 + 3 × 0,5) | 154,6 |
| Recarga VE en las casas (48 plazas) | 3,68 × 0,1 × 48, con SPL en cada casa | ≈ 17,7 |
| Alumbrado exterior comunitario y riego | Hipótesis | ≈ 3 |
| **Total del conjunto** (34 viviendas con coeficiente conjunto 21,8) | 9,2 × 21,8 = 200,6 + SG 13,5 + VE 25,8 + exterior 3 | **≈ 243 kW** |

> **La previsión del conjunto supera los 100 kW**, el umbral a partir del cual la empresa distribuidora puede exigir al promotor la **reserva de un local para centro de transformación** (ITC-BT-10, 4; RD 1955/2000). **No se da por hecho:** depende de la capacidad de la red existente, que es **FALTA DATO**. Ver 6.5 y el conflicto del apartado 10.

### 6.2 Casas (24 suministros individuales)

- **Opción 1 (recomendada).** La **red de BT de la compañía** entra en la parcela bajo la franja de plazas de la calle interior (con **servidumbre o cesión a favor de la compañía: FALTA DATO**), con **cajas de seccionamiento**. En cada casa, una **CPM** (caja de protección y medida, ITC-BT-13, 2.1) en la hornacina de fachada HC-U → derivación individual corta → cuadro general en el vestíbulo de PB.
- **Opción 2.** Contadores agrupados en armarios en la entrada desde Floristas. Las derivaciones individuales llegan a ≈ 90 m. Con 9,2 kW monofásicos y un 1,5 % de caída de tensión (ITC-BT-15), salen secciones de ≈ 35-50 mm² Cu (estimación manual). **Inviable económicamente**: se descarta salvo que la compañía lo exija.
- **Recarga VE:** circuito de recarga **C13** desde el cuadro de la vivienda (**esquema 4**, ITC-BT-52), hasta un punto de recarga o wallbox en la fachada, junto a las 2 plazas. Tubo enterrado de reserva para la segunda plaza.

### 6.3 Bloque

- **CGP.**
  - **Preferente:** en la **fachada sur del bloque o en un murete junto a la bolsa**, si la compañía lleva su red hasta allí.
  - Si la CGP se queda en el límite de Floristas, la **LGA mide ≈ 50-70 m** hasta los portales. Con ≈ 100 kW y una caída de tensión del 0,5 % (contadores totalmente concentrados, ITC-BT-14) sale **≈ 240 mm² Cu** (estimación manual). Alternativa: **una CGP y una LGA por portal** (≈ 50 kW cada una) o una LGA con una caída admisible del 1 % (centralización parcial).
- **Centralización de contadores:** **un armario por portal** (5 viviendas + servicios generales + línea de recarga VE ≈ 7 módulos). Con ≤ 16 contadores **no hace falta local** (ITC-BT-16, 2.2). El armario va en el **portal** (hornacina de ≈ 1,2-1,5 m de ancho × 0,30 m de fondo × 2,0 m de alto) con **≥ 1,50 m libres delante** (ITC-BT-16, 2.2.2). **Se separa de la batería de agua**: el armario no va dentro del cuarto de agua. **Atención:** el portal es recorrido de evacuación (conflicto, apartado 10).
- **Derivaciones individuales:** por la **canaladura PE-1 / PE-2** de cada núcleo, registrable en cada planta desde el rellano (ITC-BT-15). Para hasta 12 derivaciones: **0,65 × 0,15 m** (una fila).
- **Cuadro de servicios generales** en el cuarto CI-1: ascensores, alumbrado común y de emergencia, aspiradores de ventilación, ICT, alumbrado exterior del bloque y de la bolsa, y la línea principal de recarga VE.

### 6.4 Recarga de vehículo eléctrico (ITC-BT-52 y DB-HE 6)

- **Bolsa del bloque (22 plazas):** aparcamiento colectivo exterior adscrito al edificio en propiedad horizontal.
  - **Conducción principal comunitaria** enterrada (tubos de reserva Ø90-110 bajo la fila de plazas, con arquetas cada 4-5 plazas) desde la centralización del bloque, para poder hacer derivaciones hasta cada plaza (ITC-BT-52, 3).
  - **Preinstalación en el 100 % de las plazas**, si es de aplicación el DB-HE 6 a un uso residencial privado con más de 10 plazas. **A confirmar por el agente de normativa** (ámbito de "aparcamiento exterior adscrito").
  - Esquema previsto: **esquema 2** (contador individual por usuario en la centralización) o **esquema 3** (contador principal común y submedida). Decide el arquitecto con la futura comunidad.
  - **SPL** en la LGA para reducir la previsión (factor 0,1).
  - Plaza accesible con punto de recarga a una altura accesible.
- **Plazas de las casas (48):** dependen de cada vivienda (esquema 4, apartado 6.2). **No se integran en la red comunitaria.**
- **Plazas de reserva o visitantes (2):** conducción hasta ellas desde los servicios generales.

### 6.5 Centro de transformación y elemento de la esquina SE (FALTA DATO)

El elemento macizo del plano de la cédula (vértice 2, esquina Avda. de la Dehesa / UA-03-02) **sigue sin identificar**. **No se supone que sea un CT.** Qué implicaría en cada caso:

| Hipótesis | Implicaciones para las instalaciones | Implicaciones para V1 |
|---|---|---|
| **(a) Es un CT de la compañía, existente o previsto en la urbanización** | Podría ser el punto de suministro en BT de la promoción, con salida de líneas a Floristas o directamente a la parcela, **si tiene potencia disponible** (≈ 243 kW, FALTA DATO). Si está dentro de la parcela habría una **servidumbre de paso y acceso permanente** para la compañía, que la cédula no recoge (casilla en blanco) | Acceso para vehículos de la compañía desde la Avda. de la Dehesa. **Distancia a la hilera A-este** (esquina x = 86, y = 9) de ≈ 7-9 m (medición manual). Hay que comprobar el **ruido** (transformador) y los **campos electromagnéticos** (RD 1066/2001; recomendación de alejarlo de los dormitorios). Si es un CT de superficie, ocupa la zona libre SE. Sin reubicación de V1, previsiblemente |
| **(b) Es una arqueta u otro elemento menor** | Sin efecto relevante, salvo una servidumbre de registro | Ninguno |
| **(c) No hay CT y la compañía exige uno para la promoción** | **Local para CT** de ≈ 2,5 × 4-6 m (prefabricado de superficie), **con acceso directo desde la vía pública** las 24 h. Ubicaciones posibles: (1) **esquina SE**, con acceso desde la Avda. de la Dehesa, si el elemento no lo impide; (2) **junto a Floristas**, al sur del acceso a la calle interior, dentro de la banda de retranqueo de 3-5 m (**si se admiten construcciones auxiliares en el retranqueo: FALTA DATO**) | **V1 no reserva este espacio.** Conflicto anotado. Si el CT computa ocupación o edificabilidad: FALTA DATO (normalmente no, pero hay que confirmarlo) |

**Acción:** pedir a la compañía distribuidora un **punto de conexión y las condiciones técnicas** (RD 1955/2000) con la previsión de ≈ 243 kW, e identificar el elemento SE con el proyecto de urbanización.

### 6.6 Alumbrado exterior

Alumbrado de la calle interior, la bolsa y los jardines comunes desde el cuadro de servicios generales del bloque, o desde un suministro comunitario independiente (ITC-BT-09; RD 1890/2008 de eficiencia). Tendido bajo la franja de plazas.

---

## 7. Telecomunicaciones (ICT, RD 346/2011 y Orden ITC/1644/2011)

- **Aplicabilidad.** La ICT es obligatoria en edificios y conjuntos inmobiliarios en régimen de propiedad horizontal (RD-ley 1/1998). Con **una sola promoción** de 34 viviendas, viales y aparcamiento comunes, **es previsible que aplique a todo el conjunto**, pero el **régimen jurídico es FALTA DATO**. Si las casas fueran fincas independientes, la ICT se limitaría al bloque y cada casa tendría una canalización de acceso individual.
- **Esquema propuesto** (34 PAU):
  - **Arqueta de entrada** en el límite de Floristas, junto al acceso de la calle interior (para 21-100 PAU, ≈ 600 × 600 × 800 mm; **comprobar la tabla del Anexo III**);
  - **canalización externa** hasta el registro de enlace;
  - **canalización principal enterrada** bajo la franja de plazas: por la calle interior hasta las 24 casas, con arquetas de registro y un **registro secundario** cada 4-8 casas, y por la bolsa hasta el bloque;
  - **en cada casa:** registro de terminación de red (RTR) en el vestíbulo de PB, más la canalización interior;
  - **en el bloque:** **RITI o RITU** en el cuarto CI-1 (para ≤ 20 PAU puede ser un recinto modular o armario de ≈ 2,00 × 1,00 × 0,50 m) y canalización principal vertical por el registro PT-1 / PT-2 de cada núcleo;
  - **RITS** (cabecera de RTV) en el **castillete del portal 1**, como armario de ≈ 2,00 × 1,00 × 0,50 m. **Antenas en la cubierta del bloque**, que dan servicio también a las casas por la canalización principal.
- Fibra óptica y cable coaxial según el proyecto técnico de ICT, que debe firmar un ingeniero de telecomunicación. Este documento solo **reserva espacios**.

---

## 8. Tabla de patinillos y espacios técnicos

**Patinillos verticales.** Las dimensiones son libres interiores. Los registros de los patinillos que atraviesan forjados deben resolver la **compartimentación EI** entre plantas y viviendas (DB-SI 1), con sellado por planta o registros EI. **Lo confirma el agente de normativa.**

| Id | Ubicación | Dimensiones (libres) | Instalaciones que contiene | Plantas que recorre | Nº |
|---|---|---|---|---|---|
| **PU** | Cada casa U-V1: crujía de la calle (norte en la banda A, sur en la B), **junto a la medianera** y pegado a la zona húmeda (aseo y lavadero en PB, baños en P1), **en la medianera opuesta a la escalera** | **0,80 × 0,40 m propuesto** (F2: 0,60 × 0,40, insuficiente; conflicto) | Bajante de fecales Ø110 + ventilación primaria · conducto de extracción general Ø125 · conducto de campana Ø150 · montante de AFS, ACS y retorno de suelo radiante · ida y retorno de la aerotermia desde la cubierta (2 × Ø28 aislados) · tubo de reserva para FV | PB → cubierta | 24 |
| **PB-1 / PB-2** | Portal 1: junto al rellano, uno a cada lado del núcleo (ejes 2-3), pegados a las cocinas y baños de cada columna de viviendas. **Registrables desde el rellano** | **1,00 × 0,60 m** cada uno (F2: 1,20 × 0,60 por cada 2 viviendas; se propone dividirlo en dos, uno por columna) | Bajante de fecales Ø110 · conducto colectivo de extracción Ø200 · hasta 3 conductos de campana Ø150 · montantes individuales de AF desde la batería (DN 25-32) · líneas de aerotermia (opción A) o ida, retorno y recirculación de ACS (opción B) | PB → cubierta | 2 |
| **PB-3 / PB-4** | Portal 2: ídem, ejes 5-6 | 1,00 × 0,60 m | Ídem | PB → cubierta | 2 |
| **PE-1 / PE-2** | Canaladura eléctrica en cada núcleo, en la pared del rellano, **separada de los patinillos húmedos** | **0,65 × 0,15 m** (ITC-BT-15, ≤ 12 derivaciones, una fila) | Derivaciones individuales de las 5 viviendas del portal · línea de servicios generales a cubierta (aspiradores, ascensor) · reserva | PB → P2 (y cubierta para servicios generales) | 2 |
| **PT-1 / PT-2** | Registro de la ICT en cada núcleo, en el rellano, junto a PE | ≈ 0,45 × 0,15 m (registro secundario y canalización principal). **Dimensiones finales según el proyecto de ICT** | Canalización principal de la ICT (fibra, coaxial, pares o reserva) · enlace RITI-RITS (solo en el portal 1) | PB → cubierta (RITS en el portal 1) | 2 |

**Espacios técnicos en planta y cubierta**

| Id | Ubicación | Dimensiones | Contenido | Observaciones |
|---|---|---|---|---|
| **HC-U** | Fachada de entrada de cada casa, junto a la puerta, en el paso peatonal de 1,50 m entre plazas | Hornacina de ≈ 1,20 × 0,30 × 2,00 m (alto) | CPM eléctrica · contador de agua · registro de telecomunicaciones (RTR exterior o arqueta) | Empotrada en la fachada: **no reduce el paso de 1,50 m**. Criterio de la compañía sobre la accesibilidad: FALTA DATO |
| **LAV-U** | Lavadero de PB de cada casa (4 m²) | ≈ 0,6 × 0,7 m de planta, h 1,9 m | Módulo interior de aerotermia con depósito de ACS de 180-200 L · colector de suelo radiante de PB · cuadro eléctrico (o en el vestíbulo) | Reduce la despensa |
| **CUB-U** | Cubierta de cada casa | ≈ 1,5 m² (unidad exterior) + ≈ 12-18 m² (FV opcional) | Unidad exterior de la aerotermia · salidas de ventilación (Ø125, Ø150) y ventilación primaria Ø110 · FV | Altura sobre cornisa: **conflicto** |
| **CI-1 / CI-2** | PB de cada portal (8 m², F2) | 8 m² (p. ej. 2,0 × 4,0 m), puerta a zona común | Batería de contadores de agua (≈ 6 contadores, ≈ 1,2 m de frente) con sumidero · grupo de presión de reserva (≈ 1,5 m², si hace falta) · cuadro de servicios generales (CI-1) · RITI o RITU modular (CI-1) · arranque de la conducción de recarga VE · cuadro de la ventilación del cuarto de residuos | Ventilación natural o forzada. **No incluye el armario eléctrico de contadores**, que va en el portal. Con la opción B de ACS hay que ampliarlo o llevar la producción a cubierta |
| **AC-1 / AC-2** | Portal de cada portal | Hornacina de ≈ 1,2-1,5 × 0,30 × 2,0 m + 1,50 m libres delante | Centralización de contadores eléctricos (5 viviendas + SG + VE) | **Interfiere con el recorrido de evacuación del portal** (conflicto) |
| **CGP-B** | Fachada sur del bloque o murete junto a la bolsa (o límite con Floristas) | Nicho de ≈ 0,7 × 0,3 × 1,4 m por CGP (según la compañía) | CGP del bloque (1, o 1 por portal) | Ver la LGA en 6.3 |
| **AG-A** | Límite de la parcela con Floristas, junto al acceso de la calle interior | Armario o arqueta de ≈ 1,5 × 0,6 m (según la compañía, FALTA DATO) | Llave de registro, contador general o filtro de la acometida de agua · derivación al hidrante (si es exigible) | |
| **AE-ICT** | Límite con Floristas | Arqueta de ≈ 0,6 × 0,6 × 0,8 m | Arqueta de entrada de la ICT | |
| **PG-F / PG-P** | Interior de la parcela, junto a Floristas (1 o 2 puntos de vertido) | Pozos de registro Ø1,0-1,2 m | Pozo general de fecales y de pluviales · arqueta de unión si la red municipal es unitaria | Cotas: FALTA DATO |
| **BOMB** (solo si hace falta) | Zona libre junto a Floristas | ≈ 2,0 × 2,0 m, h ≈ 3 m enterrado | Pozo de bombeo de fecales o pluviales | Solo si la cota de la red municipal lo exige |
| **LAM** (solo si se exige) | Bajo la bolsa del bloque o en los jardines comunes del norte | Volumen según la ordenanza (FALTA DATO) | Aljibe de laminación de pluviales o SUDS | |
| **CUB-B** | Cubierta del bloque (450 m²) | Zona de equipos de ≈ 20-25 m² + FV ≈ 60-90 m² + castilletes | 10 unidades exteriores de aerotermia (opción A) o la central (opción B, recinto de ≈ 8 m²) · 4 aspiradores de extracción colectiva · 10 salidas de campana · 4 ventilaciones primarias · antenas de la ICT · FV · RITS en el castillete del portal 1 | Altura sobre cornisa y castilletes: **FALTA DATO / conflicto**. Acceso de mantenimiento a la cubierta desde el núcleo (escalera o trampilla) y **protección perimetral** frente a caídas (DB-SUA 1) |
| **CT** (posible) | Esquina SE o junto a Floristas | ≈ 2,5 × 4-6 m + acceso | Centro de transformación de la compañía | **FALTA DATO**. Ver 6.5 |

---

## 9. Comprobación de alturas libres frente a falsos techos y conductos

Datos: altura de suelo a suelo 3,00 m (F2, H-ALT) · forjado (H-I8) · suelo radiante 0,12 m (H-I9) · falso techo para un conducto Ø125-150 con aislamiento y cuelgue ≈ 0,22-0,25 m (Ø200 en el bloque: ≈ 0,30 m).

| Local | Cálculo | Altura libre | Referencia (H-I10) | Resultado |
|---|---|---|---|---|
| Casa, estancias sin falso techo | 3,00 − 0,30 − 0,12 | **2,58 m** | 2,50 m | ✔ (margen de 8 cm) |
| Casa, baños y distribuidor de P1 con falso techo (extractor y conductos) | 2,58 − 0,25 | **2,33 m** | 2,20 m | ✔ |
| Casa, salón o dormitorio con falso techo (solo con doble flujo) | 2,58 − 0,25 | 2,33 m | 2,50 m | ✘ → **el doble flujo no puede pasar conductos por las estancias** |
| Casa, cocina con conducto de campana | El conducto sube directo al patinillo, sin falso techo | 2,58 m | 2,50 m | ✔ si la campana está junto al patinillo (**condición para el diseño de la cocina**) |
| Bloque, estancias | 3,00 − 0,28 − 0,12 | **2,60 m** | 2,50 m | ✔ |
| Bloque, vestíbulo y baños con conductos Ø150 | 2,60 − 0,25 | 2,35 m | 2,20 m | ✔ |
| Bloque, si el colectivo Ø200 saliera del patinillo por falso techo | 2,60 − 0,30 | 2,30 m | 2,20 m | ✔ en zonas de paso. **No debe cruzar estancias** |
| Bloque, portal y rellanos | 3,00 − 0,28 − pavimento 0,08 − falso techo de instalaciones comunes 0,20 | ≈ 2,44 m | 2,20 m | ✔ |

**Conclusiones:**
- Con las hipótesis de canto, **cabe la solución base** (simple flujo, conductos solo en zonas húmedas y de paso).
- **No hay holgura** para doble flujo con conductos por las estancias ni para cantos mayores. Si estructura da un forjado de 0,35 m en las casas, la altura libre de las estancias baja a **2,53 m** (✔ por 3 cm). Con 0,40 m quedaría en **2,48 m** (✘).
- **En el bloque no se puede subir la altura de planta**: la cornisa queda a ≈ 9,7 m de los 10 m permitidos, sin topografía.
- Se anota como conflicto, a validar con `fases/03_estructura.md` y con la norma de altura libre (FALTA DATO).

---

## 10. Conflictos detectados (anotados en `fases/conflictos.md`)

| Nº en conflictos.md | Resumen |
|---|---|
| I-1 | Patinillo unifamiliar de 0,60 × 0,40 m (F2) insuficiente → se propone 0,80 × 0,40 m. Afecta a la distribución de la zona húmeda (diseño) |
| I-2 | Huecos de los patinillos PU en el forjado unidireccional de las casas (viguetas entre medianeras) → necesitan brochales o zunchos. Coordinar con la posición de la escalera y el zuncho del eje B (estructura) |
| I-3 | Patinillos PB-1 a PB-4 junto a los núcleos del bloque, en losa: los huecos cerca de los pilares reducen el perímetro crítico de punzonamiento (estructura) |
| I-4 | Colectores enterrados y arquetas a pie de bajante frente a la cimentación sin geotecnia (zapatas o vigas riostras): pasatubos y cotas (estructura) |
| I-5 | Alturas libres justas con 3,00 m de suelo a suelo, suelo radiante y falsos techos. Excluye el doble flujo por las estancias. Sin margen para subir la planta del bloque por la cornisa (diseño, estructura, normativa) |
| I-6 | Equipos en cubierta (aerotermia, FV, salidas de ventilación, antenas, RITS) y castilletes por encima de la cornisa. Admisibilidad entre cornisa y coronación: FALTA DATO (diseño, normativa) |
| I-7 | Pisos M-V1-a sin espacio para el módulo interior de aerotermia y el depósito de ACS (≈ 0,8-1,0 m²) (diseño) |
| I-8 | Previsión de ≈ 243 kW > 100 kW: posible local para centro de transformación sin espacio reservado en V1. Relación con el elemento SE (diseño, urbanismo) |
| I-9 | Armario de centralización de contadores eléctricos en el portal, con 1,50 m libres delante, sobre el recorrido de evacuación del portal (diseño, normativa) |

---

## 11. Datos que faltan

| # | Dato | A quién pedirlo | Afecta a |
|---|---|---|---|
| 1 | **Servicios urbanos existentes** en Calle Floristas y en la Avda. de la Dehesa: agua, alcantarillado, BT/MT, telecomunicaciones; puntos de acometida | Proyecto de urbanización del Sector-1 / Ayuntamiento | Todo |
| 2 | **Tipo de red de alcantarillado** (separativa o unitaria) y **cota de los colectores** municipales | Ayuntamiento / gestor del saneamiento | Saneamiento, posible bombeo |
| 3 | **Topografía** y rasantes de las calles | Topógrafo | Saneamiento, zona climática, cornisa |
| 4 | **Presión** de la red de agua y normas de la compañía de agua (contadores en vial privado, batería) | Compañía de agua (previsiblemente Canal de Isabel II, a confirmar) | Fontanería, grupo de presión |
| 5 | **Compañía eléctrica distribuidora**, punto de conexión, capacidad de la red y **exigencia de CT** | Empresa distribuidora (solicitud de punto de conexión) | Electricidad, CT |
| 6 | **Naturaleza del elemento de la esquina SE** (¿CT?) y servidumbres | Proyecto de reparcelación o urbanización | Electricidad, implantación |
| 7 | **Régimen jurídico** del conjunto (propiedad horizontal, conjunto inmobiliario o división horizontal tumbada) | Arquitecto / promotor | ICT, contadores, recarga VE |
| 8 | Ordenanza de **vertidos y laminación** de pluviales | Ayuntamiento | Saneamiento (aljibe o SUDS) |
| 9 | Norma de **altura libre** mínima aplicable | Normativa municipal o autonómica | Falsos techos |
| 10 | Admisibilidad de **instalaciones y castilletes entre cornisa y coronación** | Normativa del Plan Parcial | Cubiertas |
| 11 | Admisibilidad de **construcciones auxiliares** (CT, armarios de compañía) en la banda de retranqueo | Normativa del Plan Parcial | CT, armarios |
| 12 | Zona de **radón** del municipio (DB-HS 6, apéndice B) | Agente de normativa | Solera o cámara sanitaria, barrera |
| 13 | Aplicación de **DB-HE 5** y **DB-HE 6** a este conjunto (residencial privado, edificios independientes, aparcamiento exterior) | Agente de normativa | FV, recarga VE |
| 14 | Exigencia de **hidrante** (DB-SI 4) para 5.094 m² en edificios independientes | Agente de normativa | Fontanería |
| 15 | Canto real de los forjados y tipo de PB (solera o forjado sanitario) | `fases/03_estructura.md` | Alturas libres, colectores |
| 16 | Decisiones del arquitecto: opción A o B de ACS en el bloque · simple o doble flujo · FV en las casas · preinstalación de split · esquema de recarga de la bolsa | Arquitecto | Varias |

PENDIENTE DE VALIDAR POR EL ARQUITECTO
