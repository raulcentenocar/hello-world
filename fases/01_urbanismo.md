# F1 — Análisis urbanístico · Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Cañada, Madrid)

Agente: urbanismo · Fecha de redacción: 2026-11-13

---

## 1. Datos de la parcela y fuentes consultadas

### 1.1 Fuentes

| Fuente | Estado | Uso |
|--------|--------|-----|
| `datos/UA 03 01.pdf`: cédula urbanística de la parcela UA-03-01, Proyecto de Reparcelación del Sector-1 "Los Pocillos" (redactor: GIS Gestión Integral del Suelo, S.L.), fecha **marzo de 2024**. Es un PDF escaneado de 1 página. | **Leída. Es la única fuente de los parámetros de este documento.** | Todos los parámetros |
| `datos/LEEME.md`, `CLAUDE.md`, `scripts/LEEME_volumetria.md`, `scripts/ejemplos/ejemplo_ficticio.json` | Leídos | Reglas del estudio y formato JSON |
| `datos/parcela.md`, `datos/programa.md` | **No existen** | — |
| Normativa Urbanística de la Modificación del Plan Parcial del Sector-1 (localizada con WebSearch): [05_DN-NU_NORMATIVA URBANISTICA.pdf](https://ayto-villacanada.es/sites/default/files/files/05_DN-NU_NORMATIVA%20URBANISTICA.pdf). Según el índice del buscador, la ordenanza "Residencial Unifamiliar Adosada (UA)" está en torno a la pág. 56 de la versión de **aprobación inicial (julio de 2018)**. | **NO consultada.** El dominio `ayto-villacanada.es` no es accesible desde esta sesión (ENOTFOUND). | — |
| Publicación en el BOCM relacionada con la Modificación del Plan Parcial del Sector-1: [BOCM-20220105-68](https://www.bocm.es/boletin/CM_Orden_BOCM/2022/01/05/BOCM-20220105-68.PDF) | **NO consultada.** El dominio `www.bocm.es` no es accesible desde esta sesión (ENOTFOUND). | — |
| Anuncio de la aprobación definitiva de la reparcelación: [ayto-villacanada.es (julio de 2025)](https://www.ayto-villacanada.es/wp-content/uploads/2025/07/Publicación-anuncio-Aprobación-definitiva-reparcelacion.pdf) | NO consultado (mismo dominio bloqueado) | — |

> Para leer la ordenanza UA completa (parcela mínima, frente, fondo, separación entre edificios, áticos, condiciones estéticas, cómputo de superficies) hay que permitir en la configuración de red de la sesión los dominios **`ayto-villacanada.es`** y **`www.bocm.es`**, o que el arquitecto deje el texto de la ordenanza en `datos/`. Ningún parámetro de este documento procede de esas fuentes.

### 1.2 Identificación (transcripción de la cédula)

| Campo | Valor en la cédula |
|-------|--------------------|
| Parcela | **UA-03-01** |
| Fecha de la cédula | Marzo de 2024 |
| Término municipal | Villanueva de la Cañada (Madrid) |
| Situación | Unidad de Ejecución Única del Sector-1 "Los Pocillos" |
| Calle de acceso | Calle Floristas nº 2 |
| Clase de suelo | Suelo urbano |
| Planeamiento | Mod. del Plan Parcial de Ordenación del Sector-1 "Los Pocillos" |
| Normativa específica (ordenanza/zona) | **Residencial Unifamiliar Adosada (UA)** |
| Superficie de la parcela | **8.839 m²s** |
| Obligaciones y servidumbres | (casilla en blanco en la cédula) |

### 1.3 Descripción literal de linderos (cédula)

> "La parcela calificada como residencial unifamiliar adosada linda al norte con la Zona Verde ZV-02 con unas longitudes en línea curva de 29,3, 76,12 y 20,26 metros. Al este linda con la parcela UA-03-02 con una longitud en línea recta de 71,3 metros. Al sur linda con Avenida de la Dehesa con una longitud en línea curva de 92,02 metros. Al oeste linda con la vía denominada como Calle Floristas con una longitud en línea recta de 101,65 metros."

En el plano de definición (escala 1:1.000) aparece además la **Calle Bordadoras** al norte, al otro lado de la ZV-02. La parcela **no linda** con ella.

### 1.4 Vértices geométricos (ETRS89 / UTM huso 30N), transcritos tal como figuran

| Nº | X | Y |
|----|---|---|
| 1 | 414.988,78 | 4.478.854,76 |
| 2 | 414.988,78 | 4.478.782,00 |
| 3 | 414.896,93 | 4.478.781,24 |
| 4 | 414.865,48 | 4.478.877,90 |
| 5 | 414.894,46 | 4.478.874,31 |
| 6 | 414.968,83 | 4.478.858,29 |

Las filas 7 a 50 de la tabla de la cédula están vacías.

### 1.5 Lados del polígono y linderos

Lado *i* = del vértice *i* al vértice *i+1*. El índice base 0 es el que probablemente usará el generador (**hay que comprobarlo con `--lados`**). Las cuerdas las he calculado a mano con las coordenadas y conviene revisarlas.

| Lado (base 0) | Vértices | Lindero | Tipo (cédula) | Longitud cédula | Cuerda entre vértices (manual) | Radio en el plano |
|---|---|---|---|---|---|---|
| 0 | 1 → 2 | Este: parcela **UA-03-02** | recta | 71,30 m | 72,76 m (**no coincide**, +1,46 m) | — |
| 1 | 2 → 3 | Sur: **Avenida de la Dehesa** (vía pública) | **curva** | 92,02 m | ≈ 91,85 m | **R = 433** |
| 2 | 3 → 4 | Oeste: **Calle Floristas** (vía pública, acceso) | recta | 101,65 m | ≈ 101,65 m (coincide) | — |
| 3 | 4 → 5 | Norte: **Zona Verde ZV-02** (tramo 1) | **curva** | 29,30 m | ≈ 29,20 m | **R = 100** |
| 4 | 5 → 6 | Norte: **Zona Verde ZV-02** (tramo 2) | **curva** | 76,12 m | ≈ 76,08 m | **R = 669,75** |
| 5 | 6 → 1 | Norte: **Zona Verde ZV-02** (tramo 3) | **curva** | 20,26 m | ≈ 20,26 m | **R = 500** |

- **Cuatro de los seis linderos son curvos**: los tres tramos a la ZV-02 y el de la Avenida de la Dehesa. Por eso **el polígono de 6 vértices es solo una aproximación por cuerdas** de la parcela real.
- He comprobado la lectura de los radios, que en el escaneo tienen letra pequeña. Para cuerda *c* y radio *R*, el arco vale ≈ *c* + *c*³/(24*R*²): 91,85 → 92,02 (R433), 76,08 → 76,12 (R669,75) y 29,20 → 29,30 (R100). Coinciden con las longitudes de arco de la cédula, así que la lectura de los radios es coherente.
- El plano no permite asegurar hacia qué lado es convexo cada arco (si invade la parcela o sale de ella). Flecha aproximada de cada arco (*c*²/8*R*): Avda. de la Dehesa ≈ 2,4 m; ZV-02 tramo 2 ≈ 1,1 m; ZV-02 tramo 1 ≈ 1,1 m; ZV-02 tramo 3 ≈ 0,1 m.
- En la esquina SE (vértice 2) el plano dibuja un pequeño elemento macizo, posiblemente un centro de transformación o una arqueta. No está identificado en la cédula: **FALTA DATO**.

### 1.6 Superficie del polígono frente a la oficial

Área de Gauss (fórmula del lazada), **calculada a mano** con origen local (414.800; 4.478.780):

- Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ) = −18.044,31 → **A_polígono ≈ 9.022 m²** (los vértices van en sentido horario).
- Superficie oficial (cédula): **8.839 m²**.
- Diferencia: **≈ +183 m² (+2,1 %)**. El polígono de cuerdas es mayor que la superficie oficial.

Posibles causas: (a) los segmentos circulares de los arcos, del orden de ±150 m² en la Avda. de la Dehesa, ±55 m² en el tramo de 76,12 m y ±21 m² en el de 29,3 m, con signo según la convexidad; (b) la discrepancia del lindero este (cuerda de 72,76 m frente a 71,30 m en la cédula); (c) un posible elemento excluido en la esquina SE.

**Hay que comprobarlo**: el coordinador o el script de volumetría deben recalcular el área de forma reproducible. **Todos los cálculos de techo y huella usan la superficie oficial de 8.839 m².**

---

## 2. Tabla principal de parámetros

La cédula fija valores distintos para **uso unifamiliar** y **uso multifamiliar**. En F1, la columna "Propuesto" recoge el máximo aprovechable. Se ajustará en F2 cuando el arquitecto elija la tipología.

### 2.1 Parámetros comunes

| Parámetro | Permitido (norma) | Propuesto (F1) | Fuente |
|-----------|-------------------|----------------|--------|
| Superficie de parcela | 8.839 m²s | 8.839 m²s | Cédula UA-03-01 |
| Clasificación del suelo | Suelo urbano | — | Cédula |
| Calificación / ordenanza | Residencial Unifamiliar Adosada (UA) | — | Cédula ("Normativa específica") |
| Uso principal | Vivienda en categoría 1ª y 2ª | Vivienda (la categoría depende de la tipología que se elija) | Cédula. **La definición de las categorías 1ª y 2ª: FALTA DATO** (está en la normativa del Plan Parcial, no consultada) |
| Edificabilidad máxima (principal) | 5.100 m²c | 5.100 m²c | Cédula |
| Edificabilidad asociada | 0 m²c | 0 m²c | Cédula |
| Edificabilidad unitaria derivada | 5.100 / 8.839 = 0,576988 m²/m² (derivada, no figura en la cédula) | 0,576988 m²/m² | Derivado de la cédula |
| Nº máximo de viviendas | 34 viviendas | 34 viviendas (≈150 m²c por vivienda de media, derivado) | Cédula |
| Plazas de aparcamiento | 2 plazas por vivienda | 68 plazas (34 × 2) | Cédula |
| Condiciones de adosamiento | "Según proyecto. Mínimo de 8 viviendas por promoción" | ≥ 8 viviendas por promoción | Cédula |
| Parcela mínima | **FALTA DATO** | — | No figura en la cédula |
| Frente mínimo | **FALTA DATO** | — | No figura en la cédula |
| Fondo edificable | **FALTA DATO** | — | No figura en la cédula |
| Separación entre edificios / hileras | **FALTA DATO** | — | No figura en la cédula |
| Condiciones estéticas | **FALTA DATO** | — | No figura en la cédula |
| Áticos / bajo cubierta / cómputo de superficies | **FALTA DATO** | — | No figura en la cédula |
| Obligaciones y servidumbres | Casilla en blanco | — | Cédula. Conviene confirmar que no hay servidumbres (ver el elemento de la esquina SE) |

### 2.2 Parámetros según el uso: UNIFAMILIAR y MULTIFAMILIAR

| Parámetro | Permitido UNIFAMILIAR | Permitido MULTIFAMILIAR | Propuesto (F1) | Fuente |
|-----------|----------------------|-------------------------|----------------|--------|
| Nº máximo de plantas | **2 plantas** | **3 plantas** | Máximo de cada uso | Cédula, "Altura máxima, nº de plantas" |
| Altura máxima de cornisa | **7,5 m** | **10 m** | Máximo de cada uso | Cédula, "Altura máxima, metros" |
| Altura máxima de coronación | **10,5 m** | **13 m** | Máximo de cada uso | Cédula |
| Ocupación máxima sobre parcela | **60 %** | **45 %** | Máximo de cada uso | Cédula |
| Retranqueo a alineación exterior | **3 m** | **5 m** | Mínimo de cada uso | Cédula, "Retranqueos, alineación exterior" |
| Retranqueo a linderos | **0 m (3 m en extremo de hilera)** | **5 m** | Uni: 0 m entre viviendas de la hilera y 3 m en los extremos. Multi: 5 m | Cédula, "Retranqueos, linderos" |
| Retranqueo a testeros | **3 m** | **5 m** | Mínimo de cada uso | Cédula, "Retranqueos, testeros" |
| Retranqueo de la planta bajo rasante | **3 m a calle** | **5 m a calle** | Mínimo de cada uso | Cédula, "Retranqueos, planta bajo rasante" |

### 2.3 Usos compatibles (transcripción de la cédula)

| Régimen | Usos compatibles |
|---------|------------------|
| **Vivienda unifamiliar** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo; espacios libres y zonas verdes; servicios urbanos e infraestructuras; oficina; educativo; sanitario. |
| **Vivienda multifamiliar** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo (al servicio de la edificación); espacios libres y zonas verdes; servicios urbanos e infraestructuras. |
| **Vivienda unifamiliar en régimen de división horizontal** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo (al servicio de la edificación); espacios libres y zonas verdes; servicios urbanos e infraestructuras. |
| Usos prohibidos | **FALTA DATO**. La cédula no los enumera. Se entiende, sin confirmar, que lo que no es principal ni compatible no está permitido, pero hay que verificarlo en la normativa del Plan Parcial. |

Con 5.100 m²c de edificabilidad asociada a 0 m²c, el uso compatible terciario (oficina, educativo, sanitario) **no dispone de techo propio**. Si se implanta, consumiría techo de los 5.100 m²c. Esto es una interpretación y está **por confirmar**.

---

## 3. Techo y huella máximos (script `scripts/urbanismo_calculo.py`)

**No he podido ejecutar el script**: en esta sesión no tengo herramienta de ejecución de comandos. **El coordinador debe ejecutar estos comandos** desde la raíz del repositorio y pegar aquí la salida.

```bash
# UNIFAMILIAR (2 plantas, 60 %)
python3 scripts/urbanismo_calculo.py --parcela 8839 --edificabilidad 0.5769884 --ocupacion 60 --plantas 2

# MULTIFAMILIAR (3 plantas, 45 %)
python3 scripts/urbanismo_calculo.py --parcela 8839 --edificabilidad 0.5769884 --ocupacion 45 --plantas 3
```

(Edificabilidad = 5.100 m²c / 8.839 m²s = 0,5769884 m²/m². Con 7 decimales, el techo por edificabilidad sale ≈ 5.100,00 m².)

**Valores de control** (multiplicaciones directas para contrastar la salida del script; **no sustituyen al script**):

| Uso | Huella máxima | Techo por edificabilidad | Techo por ocupación × plantas | Techo máximo | Limitante |
|-----|---------------|--------------------------|-------------------------------|--------------|-----------|
| Unifamiliar | 8.839 × 0,60 = 5.303,40 m² | 5.100 m² | 10.606,80 m² | **5.100 m²** | edificabilidad |
| Multifamiliar | 8.839 × 0,45 = 3.977,55 m² | 5.100 m² | 11.932,65 m² | **5.100 m²** | edificabilidad |

En los dos usos **manda la edificabilidad (5.100 m²c)**, y también el tope de **34 viviendas**. La ocupación y las plantas tienen holgura de sobra. Estos valores no tienen en cuenta retranqueos, fondo ni superficies no computables.

> Resultado del script (ejecutado por el coordinador; coincide con los valores de control):

Unifamiliar:

```
CÁLCULO URBANÍSTICO (reglas fijas, sin IA)
  Superficie de parcela ........    8839.00 m²
  Edificabilidad ...............      0.577 m²/m²
  Ocupación máxima .............      60.00 %
  Nº de plantas ................          2
  ---------------------------------------------
  Huella máxima ................    5303.40 m²
  Techo por edificabilidad .....    5100.00 m²
  Techo por ocupación×plantas ..   10606.80 m²
  TECHO MÁXIMO .................    5100.00 m²
  Parámetro limitante .......... edificabilidad
```

Multifamiliar:

```
CÁLCULO URBANÍSTICO (reglas fijas, sin IA)
  Superficie de parcela ........    8839.00 m²
  Edificabilidad ...............      0.577 m²/m²
  Ocupación máxima .............      45.00 %
  Nº de plantas ................          3
  ---------------------------------------------
  Huella máxima ................    3977.55 m²
  Techo por edificabilidad .....    5100.00 m²
  Techo por ocupación×plantas ..   11932.65 m²
  TECHO MÁXIMO .................    5100.00 m²
  Parámetro limitante .......... edificabilidad
```

> Comprobación de superficie (coordinador, `python3 scripts/volumetria_generador.py <entrada> --lados`): polígono de vértices = **9.022,15 m²** (+2,1 % sobre la oficial), lo que confirma el cálculo manual de la sección 1.6.

---

## 4. Riesgos y ambigüedades de interpretación

1. **Unifamiliar o multifamiliar en una ordenanza "UA".** La ordenanza se llama "Residencial Unifamiliar Adosada", pero la cédula da parámetros de multifamiliar (3 plantas, 45 %, 5 m) y usos compatibles para "vivienda multifamiliar" y para "unifamiliar en régimen de división horizontal". Hay que confirmar en la normativa del Plan Parcial si el multifamiliar está admitido en esta parcela y con qué condiciones. Es una decisión del arquitecto.
2. **Categorías de vivienda 1ª y 2ª.** No se definen en la cédula. No se supone a qué tipología corresponde cada una.
3. **"Linderos" y "testeros".** En unifamiliar, la cédula da 0 m a linderos (3 m en extremo de hilera) y 3 m a testeros. El significado de "testero" no viene en la cédula. Puede ser el frente lateral o extremo de la hilera, o el lindero trasero opuesto a la fachada. Como en unifamiliar el extremo de hilera y el testero valen **3 m** y en multifamiliar todo vale **5 m**, en esta parcela las dos lecturas dan el mismo valor a efectos del generador (ver la sección 6). El 0 m solo aplica a la medianera entre viviendas de la misma hilera, no a los linderos de la parcela UA-03-01 con terceros. Esto es una interpretación por confirmar.
4. **¿El lindero con la Zona Verde ZV-02 es "alineación exterior"?** Una zona verde pública suele delimitarse por alineación exterior, pero la cédula no lo dice. En unifamiliar no cambia nada (3 m en ambos casos). En multifamiliar tampoco (5 m en ambos casos). Sí afecta a la elección de fachadas en el generador y a la orientación de las hileras.
5. **Linderos curvos.** El polígono de 6 vértices es una aproximación por cuerdas, con diferencias de hasta ≈2,4 m de flecha en la Avda. de la Dehesa. Los retranqueos que se midan sobre el polígono pueden no ser exactos en los linderos curvos.
6. **Superficie.** La del polígono (≈9.022 m², cálculo manual) supera en un ≈2,1 % a la oficial (8.839 m²). Además, el lindero este mide 72,76 m entre vértices frente a los 71,30 m de la cédula. Para los cálculos se usa la superficie oficial.
7. **Altura de cornisa y coronación.** La cédula da dos alturas (7,5 m / 10,5 m y 10 m / 13 m). Lo que puede ir entre cornisa y coronación (cubierta, bajo cubierta habitable o no, castilletes) depende de la normativa del Plan Parcial: **FALTA DATO**.
8. **Edificabilidad unitaria.** La cédula fija la edificabilidad en **m²c absolutos (5.100)**, no en m²/m². El 0,576988 m²/m² se deriva de la superficie oficial. Si la superficie cambiara, prevalece el valor absoluto de 5.100 m²c.
9. **Planta bajo rasante.** El retranqueo "a calle" (3 m / 5 m) no aclara si el sótano puede ocupar hasta los linderos con terceros (UA-03-02, ZV-02).
10. **Elemento en la esquina SE** (posible CT). Si es una servidumbre o una superficie excluida, afecta a la ocupación y a los retranqueos.
11. **Normativa no consultada.** Este análisis se basa solo en la cédula. La ordenanza completa del Plan Parcial puede tener condiciones que no aparecen en ella.

---

## 5. Datos que faltan y preguntas para el arquitecto

### 5.1 FALTA DATO

| # | Dato | Dónde obtenerlo |
|---|------|-----------------|
| 1 | Texto de la ordenanza UA de la Modificación del Plan Parcial del Sector-1 (versión de aprobación definitiva) | Ayuntamiento / BOCM (dominios bloqueados en la sesión) |
| 2 | Parcela mínima y frente mínimo (de parcela y de vivienda adosada) | Ordenanza UA |
| 3 | Fondo edificable | Ordenanza UA |
| 4 | Separación mínima entre edificios / hileras | Ordenanza UA |
| 5 | Longitud máxima de hilera / bloque | Ordenanza UA |
| 6 | Definición de las categorías de vivienda 1ª y 2ª | Ordenanza / normas generales del Plan Parcial |
| 7 | Usos prohibidos | Ordenanza UA |
| 8 | Cómputo de superficies edificadas (sótanos, porches, terrazas, bajo cubierta) | Normas generales del Plan Parcial / PGOU |
| 9 | Áticos, bajo cubierta, castilletes, construcciones por encima de la cornisa | Ordenanza UA |
| 10 | Condiciones estéticas (materiales, cubiertas, cerramientos de parcela, vuelos) | Ordenanza UA |
| 11 | Dotación de plazas: ¿2 por vivienda dentro de la parcela? ¿plazas de visitantes / PMR? | Ordenanza UA / normas generales |
| 12 | Topografía (levantamiento con cotas y rasantes de las calles) | Arquitecto / topógrafo |
| 13 | Estudio geotécnico | Arquitecto / laboratorio |
| 14 | Programa del cliente (tipología, nº de viviendas, superficies objetivo, presupuesto) | Cliente (`datos/programa.md`) |
| 15 | Servicios urbanos existentes y puntos de acometida | Proyecto de urbanización / compañías |
| 16 | Naturaleza del elemento de la esquina SE y servidumbres | Proyecto de reparcelación / urbanización |
| 17 | Geometría exacta de los linderos curvos (centros, sentido de la curvatura) y explicación de la diferencia 71,30 / 72,76 m del lindero este | Proyecto de reparcelación (DXF/GML) o Catastro |
| 18 | Referencia catastral (para descargar el GML con `scripts/catastro_parcela.py`) | Arquitecto / Catastro |

### 5.2 Decisiones que necesita el arquitecto

1. **Tipología**: (a) unifamiliar adosada en hileras (2 plantas, 60 %, retranqueos de 3 m, 0 m entre viviendas); (b) multifamiliar (3 plantas, 45 %, retranqueos de 5 m), si la ordenanza lo admite en esta parcela; (c) unifamiliar en régimen de división horizontal (con zonas comunes, según los usos compatibles de la cédula).
2. **Nº de viviendas** previsto (máximo 34; mínimo 8 por promoción) y una o varias promociones.
3. ¿Se aprovecha el **bajo rasante** (garaje común en sótano o garaje individual en planta baja/semisótano)?
4. ¿Se considera la **ZV-02** como alineación exterior (fachada) o como lindero?
5. ¿Autoriza permitir el acceso a `ayto-villacanada.es` y `www.bocm.es`, o aporta la ordenanza UA en `datos/`?
6. Topografía, geotecnia y programa: ¿cuándo se aportan?

---

## 6. Parámetros para el generador de volumetrías

Se usan las claves de `scripts/ejemplos/ejemplo_ficticio.json`. Ninguno de los dos bloques se ha copiado todavía a `datos/`: lo hará el coordinador si el arquitecto lo aprueba.

**Criterios de asignación:**

- `edificabilidad_m2m2` = 5.100 / 8.839 = **0.5769884**.
- `altura_max_m` = **altura de cornisa** (7,5 m / 10 m). La coronación (10,5 m / 13 m) no tiene clave en el generador y se anota aquí.
- `retranqueo_fachada_m` = retranqueo a **alineación exterior** (3 m / 5 m).
- `retranqueo_linderos_m`, con **asignación de testeros**:
  - **Unifamiliar: 3 m.** El generador usa un único valor como distancia mínima de cualquier punto del edificio al lindero de la parcela. Los linderos con terceros (UA-03-02 y, si no se considera fachada, la ZV-02) los tocan los extremos de hilera (3 m) o los testeros (3 m). El valor de 0 m de la cédula solo se aplica a la medianera entre viviendas de la misma hilera, que es interna y que el generador ya hace al adosar. Por eso no se introduce 0.
  - **Multifamiliar: 5 m**. Linderos y testeros coinciden en 5 m.
- `separacion_edificios_m`, `fondo_edificable_m`, `longitud_max_bloque_m` = **null → FALTA DATO** (no figuran en la cédula). El generador marcará FALTA DATO. Las tipologías `unifamiliar_adosada`, `bloque_abierto` y `torre` necesitan la separación entre edificios, así que no se pueden generar completas hasta tener ese dato.
- `parcela.coordenadas` = los 6 vértices UTM de la cédula, en orden. Es una **aproximación por cuerdas**: los linderos curvos no se representan.
- `fachadas` = **[1, 2]** (Avenida de la Dehesa y Calle Floristas). Son índices **provisionales en base 0**, que hay que **comprobar con** `python3 scripts/volumetria_generador.py datos/volumetria.json --lados`. No incluyen la ZV-02 (pendiente de la decisión 4).
- La planta bajo rasante (3 m / 5 m a calle) y el máximo de 34 viviendas no tienen clave en el generador. Los aplicará el diseño en F2.
- No se incluye bloque `hipotesis`, porque son parámetros de diseño de F2. El generador usará sus valores por defecto y los listará.

### 6.1 UNIFAMILIAR

```json
{
  "nombre": "UA-03-01 Sector-1 Los Pocillos (Villanueva de la Cañada) - UNIFAMILIAR",
  "parcela": {
    "coordenadas": [
      [414988.78, 4478854.76],
      [414988.78, 4478782.00],
      [414896.93, 4478781.24],
      [414865.48, 4478877.90],
      [414894.46, 4478874.31],
      [414968.83, 4478858.29]
    ]
  },
  "fachadas": [1, 2],
  "urbanismo": {
    "edificabilidad_m2m2": 0.5769884,
    "ocupacion_pct": 60,
    "plantas_max": 2,
    "altura_max_m": 7.5,
    "retranqueo_fachada_m": 3,
    "retranqueo_linderos_m": 3,
    "fondo_edificable_m": null,
    "separacion_edificios_m": null,
    "longitud_max_bloque_m": null
  },
  "tipologias": ["unifamiliar_adosada", "unifamiliar_aislada"]
}
```

### 6.2 MULTIFAMILIAR

```json
{
  "nombre": "UA-03-01 Sector-1 Los Pocillos (Villanueva de la Cañada) - MULTIFAMILIAR",
  "parcela": {
    "coordenadas": [
      [414988.78, 4478854.76],
      [414988.78, 4478782.00],
      [414896.93, 4478781.24],
      [414865.48, 4478877.90],
      [414894.46, 4478874.31],
      [414968.83, 4478858.29]
    ]
  },
  "fachadas": [1, 2],
  "urbanismo": {
    "edificabilidad_m2m2": 0.5769884,
    "ocupacion_pct": 45,
    "plantas_max": 3,
    "altura_max_m": 10.0,
    "retranqueo_fachada_m": 5,
    "retranqueo_linderos_m": 5,
    "fondo_edificable_m": null,
    "separacion_edificios_m": null,
    "longitud_max_bloque_m": null
  },
  "tipologias": ["bloque_abierto", "torre"]
}
```

| Clave | Unifamiliar | Multifamiliar | Origen |
|-------|-------------|---------------|--------|
| edificabilidad_m2m2 | 0.5769884 | 0.5769884 | Derivado: 5.100 m²c / 8.839 m²s (cédula) |
| ocupacion_pct | 60 | 45 | Cédula |
| plantas_max | 2 | 3 | Cédula |
| altura_max_m | 7.5 (coronación 10,5) | 10.0 (coronación 13) | Cédula (cornisa) |
| retranqueo_fachada_m | 3 | 5 | Cédula (alineación exterior) |
| retranqueo_linderos_m | 3 (extremo de hilera = testero = 3; 0 solo entre viviendas) | 5 (linderos = testeros = 5) | Cédula, asignación explicada arriba |
| separacion_edificios_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| fondo_edificable_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| longitud_max_bloque_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |

PENDIENTE DE VALIDAR POR EL ARQUITECTO
