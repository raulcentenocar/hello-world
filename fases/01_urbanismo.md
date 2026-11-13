# F1 — Análisis urbanístico · Parcela UA-03-01, Sector-1 "Los Pocillos" (Villanueva de la Cañada, Madrid)

Agente: urbanismo · Fecha de redacción: 2026-11-13 · **Revisión 1** (relanzamiento de F1 con las decisiones del arquitecto tomadas en la PAUSA F1)

> **Cambios de esta revisión.** Se han incorporado las decisiones del arquitecto (apartado 1.7): mezcla de unifamiliar y multifamiliar, 34 viviendas, ZV-02 tratada como lindero con retranqueo, superficie oficial para todos los cálculos, aparcamiento sobre rasante sin sótano, sin estudio geotécnico y sin programa del cliente. También se han actualizado las secciones 2, 4, 5 y 6. Las decisiones aparecen marcadas como **"decisión del arquitecto (PAUSA F1)"**. La salida del script de la sección 3, ejecutado por el coordinador, se conserva sin cambios.

---

## 1. Datos de la parcela y fuentes consultadas

### 1.1 Fuentes

| Fuente | Estado | Uso |
|--------|--------|-----|
| `datos/UA 03 01.pdf`: cédula urbanística de la parcela UA-03-01, Proyecto de Reparcelación del Sector-1 "Los Pocillos" (redactor: GIS Gestión Integral del Suelo, S.L.), fecha **marzo de 2024**. Es un PDF escaneado de 1 página. | **Leída de nuevo en esta revisión. Es la única fuente de los parámetros de este documento.** | Todos los parámetros |
| `datos/LEEME.md`, `CLAUDE.md`, `scripts/LEEME_volumetria.md` (versión actualizada, con `superficie_oficial_m2`, `viviendas_max`, `atico` y `computo`), `scripts/ejemplos/ejemplo_ficticio.json` | Leídos | Reglas del estudio y formato JSON |
| `datos/parcela.md`, `datos/programa.md` | **No existen.** No hay programa del cliente (decisión del arquitecto (PAUSA F1)) | — |
| Normativa Urbanística de la Modificación del Plan Parcial del Sector-1: [05_DN-NU_NORMATIVA URBANISTICA.pdf](https://ayto-villacanada.es/sites/default/files/files/05_DN-NU_NORMATIVA%20URBANISTICA.pdf) (localizada con WebSearch en la versión anterior; versión de aprobación inicial, julio de 2018) | **NO consultada.** **Decisión del arquitecto (PAUSA F1): la aportará el arquitecto más adelante.** Mientras tanto se trabaja solo con la cédula. | — |
| BOCM relacionado con la Modificación del Plan Parcial: [BOCM-20220105-68](https://www.bocm.es/boletin/CM_Orden_BOCM/2022/01/05/BOCM-20220105-68.PDF) | NO consultado (dominio no accesible desde la sesión anterior; pendiente de la normativa que aporte el arquitecto) | — |
| Anuncio de la aprobación definitiva de la reparcelación: [ayto-villacanada.es (julio de 2025)](https://www.ayto-villacanada.es/wp-content/uploads/2025/07/Publicación-anuncio-Aprobación-definitiva-reparcelacion.pdf) | NO consultado | — |

> Ningún parámetro de este documento procede de fuentes distintas de la cédula. Todo lo que no figura en ella sigue como **FALTA DATO** hasta que el arquitecto aporte la normativa del Plan Parcial.

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

Lado *i* (base 0) = del vértice *i+1* al *i+2* de la tabla anterior. **El coordinador ha comprobado los índices con `python3 scripts/volumetria_generador.py <entrada> --lados`**: 0 = UA-03-02 (E), 1 = Avda. de la Dehesa (S), 2 = Calle Floristas (O), 3, 4 y 5 = ZV-02 (N). Las cuerdas de la tabla son mi cálculo manual de la versión anterior.

| Lado (base 0) | Vértices | Lindero | Tratamiento (decisión del arquitecto (PAUSA F1)) | Tipo (cédula) | Longitud cédula | Cuerda entre vértices (manual) | Radio en el plano |
|---|---|---|---|---|---|---|---|
| 0 | 1 → 2 | Este: parcela **UA-03-02** | Lindero | recta | 71,30 m | 72,76 m (**no coincide**, +1,46 m) | — |
| 1 | 2 → 3 | Sur: **Avenida de la Dehesa** (vía pública) | **Fachada** | **curva** | 92,02 m | ≈ 91,85 m | **R = 433** |
| 2 | 3 → 4 | Oeste: **Calle Floristas** (vía pública, acceso) | **Fachada** | recta | 101,65 m | ≈ 101,65 m (coincide) | — |
| 3 | 4 → 5 | Norte: **Zona Verde ZV-02** (tramo 1) | **Lindero con retranqueo** | **curva** | 29,30 m | ≈ 29,20 m | **R = 100** |
| 4 | 5 → 6 | Norte: **Zona Verde ZV-02** (tramo 2) | **Lindero con retranqueo** | **curva** | 76,12 m | ≈ 76,08 m | **R = 669,75** |
| 5 | 6 → 1 | Norte: **Zona Verde ZV-02** (tramo 3) | **Lindero con retranqueo** | **curva** | 20,26 m | ≈ 20,26 m | **R = 500** |

- **Cuatro de los seis linderos son curvos**: los tres tramos a la ZV-02 y el de la Avenida de la Dehesa. Por eso **el polígono de 6 vértices es solo una aproximación por cuerdas** de la parcela real.
- He comprobado la lectura de los radios, que en el escaneo tienen letra pequeña. Para cuerda *c* y radio *R*, el arco vale ≈ *c* + *c*³/(24*R*²): 91,85 → 92,02 (R433), 76,08 → 76,12 (R669,75) y 29,20 → 29,30 (R100). Coinciden con las longitudes de arco de la cédula, así que la lectura de los radios es coherente.
- El plano no permite asegurar hacia qué lado es convexo cada arco (si invade la parcela o sale de ella). Flecha aproximada de cada arco (*c*²/8*R*): Avda. de la Dehesa ≈ 2,4 m; ZV-02 tramo 2 ≈ 1,1 m; ZV-02 tramo 1 ≈ 1,1 m; ZV-02 tramo 3 ≈ 0,1 m.
- En la esquina SE (vértice 2) el plano dibuja un pequeño elemento macizo, posiblemente un centro de transformación o una arqueta. **Sigue sin identificar: FALTA DATO** (decisión del arquitecto (PAUSA F1)).

### 1.6 Superficie del polígono frente a la oficial

- Polígono de vértices: **9.022,15 m²** (comprobado por el coordinador con el script de volumetría; mi cálculo manual de la versión anterior daba ≈ 9.022 m²).
- Superficie oficial (cédula): **8.839 m²**.
- Diferencia: **+183,15 m² (+2,1 %)**.

Posibles causas: (a) los segmentos circulares de los arcos, del orden de ±150 m² en la Avda. de la Dehesa, ±55 m² en el tramo de 76,12 m y ±21 m² en el de 29,3 m, con signo según la convexidad; (b) la discrepancia del lindero este (cuerda de 72,76 m frente a 71,30 m en la cédula); (c) un posible elemento excluido en la esquina SE.

**Decisión del arquitecto (PAUSA F1): todos los cálculos se hacen con la superficie oficial de 8.839 m². El polígono de vértices se usa solo como geometría aproximada.** En el JSON del generador se indica con la clave `parcela.superficie_oficial_m2` (sección 6).

### 1.7 Decisiones del arquitecto (PAUSA F1) incorporadas en esta revisión

| # | Decisión del arquitecto (PAUSA F1) | Efecto en este documento |
|---|-------------------------------|--------------------------|
| 1 | **Tipología: mezcla** de unifamiliar y multifamiliar en la parcela | Cada parte usa sus parámetros de la cédula (sección 2.3). La compatibilidad de la mezcla **no está confirmada** (riesgo 4.1) |
| 2 | **Nº de viviendas: el máximo, 34** | 34 viviendas en total, entre las dos partes |
| 3 | La **normativa del Plan Parcial** la aportará el arquitecto más adelante | Solo se usa la cédula. Lo que no figura en ella sigue como FALTA DATO |
| 4 | **ZV-02 = lindero con retranqueo**: 3 m unifamiliar / 5 m multifamiliar. Índices: 0 = UA-03-02 (E), 1 = Avda. de la Dehesa (S), 2 = Calle Floristas (O), 3-5 = ZV-02 (N). `fachadas` = [1, 2] | Lados 3, 4 y 5 con `retranqueo_linderos_m` |
| 5 | **Superficie oficial, 8.839 m²**, para todos los cálculos. Polígono (9.022,15 m²) solo como geometría aproximada | `superficie_oficial_m2` = 8839 |
| 6 | **Aparcamiento sin planta bajo rasante.** 68 plazas (2 × 34) sobre rasante | Riesgo de consumo de ocupación o edificabilidad (riesgo 4.5) |
| 7 | **No se hará estudio geotécnico** | FALTA DATO y riesgo para F3 (CTE DB SE-C) (riesgo 4.6) |
| 8 | Elemento de la esquina SE sin identificar | FALTA DATO |
| 9 | **No hay programa del cliente** | F2 trabajará con el reparto entre tipos como hipótesis |

---

## 2. Tabla principal de parámetros

La cédula fija valores distintos para **uso unifamiliar** y **uso multifamiliar**. Por decisión del arquitecto (PAUSA F1), la parcela tendrá una **mezcla de los dos**. En F1, la columna "Propuesto" recoge el máximo aprovechable o el valor que se aplica a cada parte. El reparto de suelo, techo y viviendas entre las dos partes se hará en F2.

### 2.1 Parámetros comunes a toda la parcela (se reparten entre las dos partes)

| Parámetro | Permitido (norma) | Propuesto (F1) | Fuente |
|-----------|-------------------|----------------|--------|
| Superficie de parcela | 8.839 m²s | **8.839 m²s** (oficial, para todos los cálculos; decisión del arquitecto (PAUSA F1)) | Cédula UA-03-01 |
| Clasificación del suelo | Suelo urbano | — | Cédula |
| Calificación / ordenanza | Residencial Unifamiliar Adosada (UA) | — | Cédula ("Normativa específica") |
| Uso principal | Vivienda en categoría 1ª y 2ª | Vivienda unifamiliar + multifamiliar (mezcla; decisión del arquitecto (PAUSA F1)) | Cédula. **La definición de las categorías 1ª y 2ª: FALTA DATO** |
| Edificabilidad máxima (principal) | 5.100 m²c | **5.100 m²c en total**, a repartir entre unifamiliar y multifamiliar en F2 | Cédula |
| Edificabilidad asociada | 0 m²c | 0 m²c | Cédula |
| Edificabilidad unitaria derivada | 5.100 / 8.839 = 0,5769884 m²/m² (derivada, no figura en la cédula) | 0,5769884 m²/m² sobre la parcela completa | Derivado de la cédula |
| Nº máximo de viviendas | 34 viviendas | **34 viviendas en total** (decisión del arquitecto (PAUSA F1)); ≈150 m²c por vivienda de media (derivado: 5.100 / 34) | Cédula |
| Plazas de aparcamiento | 2 plazas por vivienda | **68 plazas** (34 × 2), **todas sobre rasante** (decisión del arquitecto (PAUSA F1)) | Cédula |
| Condiciones de adosamiento | "Según proyecto. Mínimo de 8 viviendas por promoción" | ≥ 8 viviendas por promoción. Nº de promociones: **pendiente** (decisión 5.2) | Cédula |
| Parcela mínima | **FALTA DATO** | — | No figura en la cédula |
| Frente mínimo | **FALTA DATO** | — | No figura en la cédula |
| Fondo edificable | **FALTA DATO** | — | No figura en la cédula |
| Separación entre edificios / hileras / bloques (y entre la parte unifamiliar y la multifamiliar) | **FALTA DATO** | — | No figura en la cédula |
| Longitud máxima de hilera / bloque | **FALTA DATO** | — | No figura en la cédula |
| Condiciones estéticas | **FALTA DATO** | — | No figura en la cédula |
| Áticos / bajo cubierta / cómputo de superficies | **FALTA DATO** | — | No figura en la cédula |
| Cómputo del aparcamiento sobre rasante (en superficie o cubierto) en ocupación y edificabilidad | **FALTA DATO** | — | No figura en la cédula |
| Usos prohibidos | **FALTA DATO** | — | No figura en la cédula |
| Obligaciones y servidumbres | Casilla en blanco | — | Cédula. Conviene confirmar que no hay servidumbres (ver el elemento de la esquina SE, FALTA DATO) |

### 2.2 Parámetros según el uso: UNIFAMILIAR y MULTIFAMILIAR

| Parámetro | Permitido UNIFAMILIAR | Permitido MULTIFAMILIAR | Propuesto (F1) | Fuente |
|-----------|----------------------|-------------------------|----------------|--------|
| Nº máximo de plantas | **2 plantas** | **3 plantas** | Máximo de cada uso en su parte | Cédula, "Altura máxima, nº de plantas" |
| Altura máxima de cornisa | **7,5 m** | **10 m** | Máximo de cada uso en su parte | Cédula, "Altura máxima, metros" |
| Altura máxima de coronación | **10,5 m** | **13 m** | Máximo de cada uso en su parte | Cédula |
| Ocupación máxima sobre parcela | **60 %** | **45 %** | Ver 2.3 (aplicación en la mezcla: **FALTA DATO**) | Cédula |
| Retranqueo a alineación exterior (lados 1 y 2) | **3 m** | **5 m** | Mínimo de cada uso | Cédula, "Retranqueos, alineación exterior" |
| Retranqueo a linderos (lado 0, UA-03-02) | **0 m (3 m en extremo de hilera)** | **5 m** | Uni: 3 m al lindero con terceros (0 m solo entre viviendas de la misma hilera). Multi: 5 m | Cédula, "Retranqueos, linderos" |
| Retranqueo a la ZV-02 (lados 3, 4 y 5) | Tratada como lindero: **3 m** | Tratada como lindero: **5 m** | **Decisión del arquitecto (PAUSA F1)** | Cédula (valores de lindero/testero) + decisión del arquitecto |
| Retranqueo a testeros | **3 m** | **5 m** | Mínimo de cada uso | Cédula, "Retranqueos, testeros" |
| Retranqueo de la planta bajo rasante | **3 m a calle** | **5 m a calle** | **No aplica: no se proyecta planta bajo rasante** (decisión del arquitecto (PAUSA F1)) | Cédula, "Retranqueos, planta bajo rasante" |

### 2.3 Qué parámetros se aplican a cada parte en la mezcla

Decisión del arquitecto (PAUSA F1): mezcla de unifamiliar y multifamiliar en la parcela. **No está confirmado que la normativa del Plan Parcial lo admita en una misma parcela o promoción** (riesgo 4.1). Con lo que dice la cédula:

| Parte | Parámetros propios (cédula) | Parámetros compartidos con la otra parte |
|-------|-----------------------------|------------------------------------------|
| **Unifamiliar** (adosada en hileras) | 2 plantas; cornisa 7,5 m; coronación 10,5 m; ocupación 60 %; retranqueo de 3 m a alineación exterior (Avda. de la Dehesa, Calle Floristas), a UA-03-02 y a ZV-02; 0 m entre viviendas de la misma hilera y 3 m en extremos de hilera y testeros; usos compatibles de "vivienda unifamiliar" (o de "unifamiliar en régimen de división horizontal", si se organiza así) | 5.100 m²c; 34 viviendas; 2 plazas por vivienda; ≥ 8 viviendas por promoción |
| **Multifamiliar** | 3 plantas; cornisa 10 m; coronación 13 m; ocupación 45 %; retranqueo de 5 m a alineación exterior, a UA-03-02 y a ZV-02 (linderos y testeros); usos compatibles de "vivienda multifamiliar" | Ídem |

Puntos que la cédula **no resuelve** y que quedan como FALTA DATO (no se suponen):

- **Aplicación de la ocupación en la mezcla.** La cédula da el porcentaje "sobre parcela" para cada uso, pero no dice cómo se aplica si conviven los dos: si cada porcentaje se aplica a la superficie que se asigne a cada parte, si la parcela debe dividirse o no, o si hay otra regla. Como referencia numérica, sin que sea una interpretación adoptada: 45 % de 8.839 m² = 3.977,55 m² y 60 % = 5.303,40 m² (sección 3). Cualquier reparto estará entre esos dos valores si se ponderan las superficies asignadas, pero esa regla de ponderación **no figura en la cédula**.
- **Retranqueo o separación entre la parte unifamiliar y la multifamiliar** dentro de la misma parcela. Si no hay división de parcela, no existe lindero entre ellas y se aplicaría la separación entre edificios: **FALTA DATO**.
- **Reparto de la edificabilidad (5.100 m²c) y de las 34 viviendas** entre las dos partes: es **decisión de diseño de F2** (hipótesis, al no haber programa del cliente).

### 2.4 Usos compatibles (transcripción de la cédula)

| Régimen | Usos compatibles |
|---------|------------------|
| **Vivienda unifamiliar** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo; espacios libres y zonas verdes; servicios urbanos e infraestructuras; oficina; educativo; sanitario. |
| **Vivienda multifamiliar** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo (al servicio de la edificación); espacios libres y zonas verdes; servicios urbanos e infraestructuras. |
| **Vivienda unifamiliar en régimen de división horizontal** | Garaje-aparcamiento (en planta baja, semisótano y sótano); deportivo (al servicio de la edificación); espacios libres y zonas verdes; servicios urbanos e infraestructuras. |
| Usos prohibidos | **FALTA DATO**. La cédula no los enumera. Se entiende, sin confirmar, que lo que no es principal ni compatible no está permitido, pero hay que verificarlo en la normativa del Plan Parcial. |

- Con 5.100 m²c de edificabilidad asociada a 0 m²c, el uso compatible terciario (oficina, educativo, sanitario) **no dispone de techo propio**. Si se implanta, consumiría techo de los 5.100 m²c. Esto es una interpretación y está **por confirmar**.
- La cédula sitúa el garaje-aparcamiento "en planta baja, semisótano y sótano". **No menciona el aparcamiento al aire libre en superficie.** Con la decisión de no hacer planta bajo rasante, las 68 plazas pueden ir en planta baja (cubiertas) o en superficie. Si la segunda opción está admitida y cómo computa: **FALTA DATO** (riesgo 4.5).

---

## 3. Techo y huella máximos (script `scripts/urbanismo_calculo.py`)

Comandos (ejecutados por el coordinador desde la raíz del repositorio; en mi sesión no tengo herramienta de ejecución de comandos):

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

En los dos usos **manda la edificabilidad (5.100 m²c)**, y también el tope de **34 viviendas**. La ocupación y las plantas tienen holgura de sobra. Estos valores no tienen en cuenta retranqueos, fondo, superficies no computables ni el suelo que ocupen las 68 plazas sobre rasante.

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

**Para la mezcla** (decisión del arquitecto (PAUSA F1)), las dos ejecuciones anteriores son las envolventes de "toda la parcela unifamiliar" y "toda la parcela multifamiliar". El techo máximo de la mezcla sigue siendo **5.100 m²c** en cualquier reparto, porque es un valor absoluto de la cédula. La huella máxima de la mezcla depende de cómo se aplique la ocupación a cada parte (**FALTA DATO**, sección 2.3). Cuando F2 fije un reparto de suelo como hipótesis, podrá ejecutar el script por separado para cada parte con su superficie asignada. Esas ejecuciones serán de F2, no de F1.

---

## 4. Riesgos y ambigüedades de interpretación

1. **Mezcla de unifamiliar y multifamiliar en una ordenanza "UA" (NO RESUELTO).** La cédula define la ordenanza como **"Residencial Unifamiliar Adosada (UA)"** y describe la parcela como "calificada como residencial unifamiliar adosada", pero da parámetros para **multifamiliar** (3 plantas, 45 %, retranqueos de 5 m) y usos compatibles para "vivienda multifamiliar". La decisión del arquitecto (PAUSA F1) es mezclar los dos tipos. **Hay que confirmar con la normativa del Plan Parcial** (a) si el multifamiliar está admitido en esta parcela, (b) si se pueden mezclar unifamiliar y multifamiliar en una misma parcela o promoción, y (c) con qué condiciones (división de parcela, proporciones, separaciones). No se da por resuelto.
2. **Aplicación de la ocupación, la separación y los retranqueos en la mezcla.** La cédula no dice cómo se aplican los porcentajes de ocupación (60 % / 45 %) cuando conviven los dos usos ni qué separación debe haber entre la parte unifamiliar y la multifamiliar (sección 2.3). FALTA DATO.
3. **Mínimo de 8 viviendas por promoción.** Si la parte unifamiliar y la multifamiliar fueran promociones distintas, cada una tendría que tener al menos 8 viviendas. El nº de promociones no está decidido (5.2).
4. **ZV-02 como lindero con retranqueo** (decisión del arquitecto (PAUSA F1)). La cédula no dice si el borde con la zona verde es alineación exterior o lindero. En esta parcela los valores coinciden (3 m / 5 m en ambos casos), así que la decisión no cambia la distancia. Sí cambia los índices de `fachadas` y, por tanto, la orientación de las hileras en el generador y la definición de "frente" a efectos de un posible fondo edificable (FALTA DATO). Hay que confirmarlo con la normativa del Plan Parcial.
5. **Aparcamiento sobre rasante (NO RESUELTO).** Por decisión del arquitecto (PAUSA F1) no hay planta bajo rasante y las 68 plazas van sobre rasante. La cédula **no aclara si el aparcamiento en superficie o cubierto consume ocupación o edificabilidad**, y solo cita el garaje-aparcamiento "en planta baja, semisótano y sótano". **FALTA DATO, pendiente de la normativa.** Si el aparcamiento cubierto computa, reduce el techo disponible para vivienda (5.100 m²c) o la huella. Si va al aire libre, consume suelo libre de parcela que compite con los retranqueos (3 m / 5 m), los espacios libres y la huella edificable.
6. **Geotecnia (NO RESUELTO, riesgo para F3).** Por decisión del arquitecto (PAUSA F1) no se hará estudio geotécnico. **El CTE DB SE-C (apartado 3, "Estudio geotécnico") exige el reconocimiento del terreno** como base del proyecto de cimentación. Sin él, el agente de estructura de F3 no tendrá datos del terreno (tensión admisible, nivel freático, agresividad, expansividad). Queda como FALTA DATO y se traslada a F3. Este documento no lo resuelve.
7. **Categorías de vivienda 1ª y 2ª.** No se definen en la cédula. No se supone a qué tipología corresponde cada una.
8. **"Linderos" y "testeros".** En unifamiliar, la cédula da 0 m a linderos (3 m en extremo de hilera) y 3 m a testeros. El significado de "testero" no viene en la cédula. Como en unifamiliar el extremo de hilera y el testero valen 3 m, y en multifamiliar todo vale 5 m, las dos lecturas dan el mismo valor en el generador (sección 6). El 0 m solo se aplica a la medianera entre viviendas de la misma hilera. Esto es una interpretación por confirmar.
9. **Linderos curvos.** El polígono de 6 vértices es una aproximación por cuerdas, con diferencias de hasta ≈2,4 m de flecha en la Avda. de la Dehesa. Los retranqueos medidos sobre el polígono pueden no ser exactos en los linderos curvos.
10. **Superficie.** La del polígono (9.022,15 m²) supera en un 2,1 % a la oficial (8.839 m²). Además, el lindero este mide 72,76 m entre vértices frente a los 71,30 m de la cédula. Por decisión del arquitecto (PAUSA F1) se usa la oficial para todos los cálculos. La geometría del generador es aproximada.
11. **Altura de cornisa y coronación.** La cédula da dos alturas (7,5 m / 10,5 m y 10 m / 13 m). Lo que puede ir entre cornisa y coronación (cubierta, bajo cubierta habitable o no, castilletes, áticos) depende de la normativa del Plan Parcial: **FALTA DATO**.
12. **Edificabilidad unitaria.** La cédula fija la edificabilidad en **m²c absolutos (5.100)**, no en m²/m². El 0,5769884 m²/m² se deriva de la superficie oficial. Si en F2 se trabaja con subparcelas para cada parte, **prevalece el valor absoluto de 5.100 m²c para el conjunto**.
13. **Elemento en la esquina SE** (posible CT): FALTA DATO. Si es una servidumbre o una superficie excluida, afecta a la ocupación, a los retranqueos y a la ubicación de accesos y aparcamiento.
14. **Normativa no consultada.** Este análisis se basa solo en la cédula. La ordenanza completa del Plan Parcial, que aportará el arquitecto, puede tener condiciones que no aparecen en ella y que obliguen a revisar F1 y F2.

---

## 5. Datos que faltan y preguntas para el arquitecto

### 5.1 FALTA DATO

| # | Dato | Dónde obtenerlo | Estado |
|---|------|-----------------|--------|
| 1 | Texto de la ordenanza UA y normas generales de la Modificación del Plan Parcial del Sector-1 (versión de aprobación definitiva) | Arquitecto | **Lo aportará el arquitecto más adelante** (decisión del arquitecto (PAUSA F1)) |
| 2 | Admisión del multifamiliar en esta parcela y **posibilidad de mezclar unifamiliar y multifamiliar** en una misma parcela o promoción | Normativa del Plan Parcial | Pendiente |
| 3 | Regla de aplicación de la ocupación (60 % / 45 %) en la mezcla; si hace falta dividir la parcela | Normativa del Plan Parcial | Pendiente |
| 4 | Parcela mínima y frente mínimo (de parcela y de vivienda adosada) | Normativa del Plan Parcial | Pendiente |
| 5 | Fondo edificable | Normativa del Plan Parcial | Pendiente |
| 6 | Separación mínima entre edificios / hileras / bloques, incluida la separación entre la parte unifamiliar y la multifamiliar | Normativa del Plan Parcial | Pendiente |
| 7 | Longitud máxima de hilera / bloque | Normativa del Plan Parcial | Pendiente |
| 8 | Definición de las categorías de vivienda 1ª y 2ª | Normativa del Plan Parcial | Pendiente |
| 9 | Usos prohibidos | Normativa del Plan Parcial | Pendiente |
| 10 | Cómputo de superficies edificadas (porches, terrazas, bajo cubierta, etc.) | Normativa del Plan Parcial | Pendiente |
| 11 | Áticos, bajo cubierta, castilletes, construcciones entre cornisa y coronación | Normativa del Plan Parcial | Pendiente |
| 12 | Condiciones estéticas (materiales, cubiertas, cerramientos de parcela, vuelos) | Normativa del Plan Parcial | Pendiente |
| 13 | **Aparcamiento sobre rasante**: si se admite al aire libre; si consume ocupación o edificabilidad (en superficie o cubierto); plazas de visitantes / PMR; dimensiones de plaza y calles de rodadura | Normativa del Plan Parcial | Pendiente |
| 14 | Topografía (levantamiento con cotas y rasantes de las calles) | Arquitecto / topógrafo | Pendiente |
| 15 | **Estudio geotécnico** | Arquitecto / laboratorio | **El arquitecto indica que no se hará** (decisión del arquitecto (PAUSA F1)). Riesgo para F3 (CTE DB SE-C) |
| 16 | Programa del cliente (superficies objetivo por tipo, presupuesto) | Cliente | **No hay** (decisión del arquitecto (PAUSA F1)). F2 trabajará con el reparto entre tipos como hipótesis |
| 17 | Servicios urbanos existentes y puntos de acometida | Proyecto de urbanización / compañías | Pendiente |
| 18 | **Naturaleza del elemento de la esquina SE** y servidumbres | Proyecto de reparcelación / urbanización | Sigue sin identificar (decisión del arquitecto (PAUSA F1)) |
| 19 | Geometría exacta de los linderos curvos (centros, sentido de la curvatura) y explicación de la diferencia 71,30 / 72,76 m del lindero este | Proyecto de reparcelación (DXF/GML) o Catastro | Pendiente. Mientras tanto, polígono aproximado + superficie oficial |
| 20 | Referencia catastral (para descargar el GML con `scripts/catastro_parcela.py`) | Arquitecto / Catastro | Pendiente |

Datos de la versión anterior que **ya están resueltos** por decisión del arquitecto (PAUSA F1): tipología (mezcla), nº de viviendas (34), tratamiento de la ZV-02 (lindero con retranqueo), superficie de cálculo (8.839 m²) y bajo rasante (no se proyecta).

### 5.2 Decisiones que necesita el arquitecto

1. **Reparto entre unifamiliar y multifamiliar.** Opciones: (a) que F2 proponga el reparto de suelo, techo (5.100 m²c) y viviendas (34) como hipótesis, que es lo previsto al no haber programa; (b) que el arquitecto fije de antemano un reparto (por ejemplo, nº de viviendas de cada tipo o zona de la parcela para cada uno).
2. **Nº de promociones**: una sola promoción mixta o dos promociones (cada una con ≥ 8 viviendas, según la cédula).
3. **Forma del aparcamiento sobre rasante**: (a) plazas al aire libre en superficie; (b) plazas cubiertas (marquesinas o pérgolas); (c) garaje en planta baja de las viviendas o del bloque; (d) combinación. El efecto en ocupación y edificabilidad queda pendiente de la normativa (FALTA DATO).
4. **Geotecnia**: el arquitecto indica que no se hará estudio. ¿Confirma que F3 trabaje sin datos del terreno, marcando la cimentación como FALTA DATO, sabiendo que el CTE DB SE-C exige el reconocimiento del terreno? ¿O se reconsidera?
5. **Normativa del Plan Parcial**: ¿cuándo se aporta? Hasta entonces F2 trabajará con parámetros incompletos (sin separación entre edificios, fondo, longitud de hilera, cómputo ni áticos), y es posible que haya que revisar F1 y F2.
6. **Topografía y elemento de la esquina SE**: ¿cuándo se aportan o identifican?
7. **Referencia catastral o geometría exacta** de la reparcelación, para sustituir el polígono aproximado.

---

## 6. Parámetros para el generador de volumetrías

Se usan las claves de `scripts/ejemplos/ejemplo_ficticio.json` y de `scripts/LEEME_volumetria.md` (versión actualizada). Los bloques no se han copiado todavía a `datos/`: lo hará el coordinador si el arquitecto lo aprueba.

**Criterios de asignación:**

- `parcela.coordenadas` = los 6 vértices UTM de la cédula, en orden. Es una **aproximación por cuerdas**: los linderos curvos no se representan.
- `parcela.superficie_oficial_m2` = **8839** (decisión del arquitecto (PAUSA F1)). El generador calcula los parámetros sobre la oficial y la geometría sobre el polígono (9.022,15 m², +2,1 %), y lo avisa.
- `fachadas` = **[1, 2]** (Avenida de la Dehesa y Calle Floristas). **Índices comprobados por el coordinador con `--lados`.** Los lados 0 (UA-03-02) y 3, 4 y 5 (ZV-02) son linderos y usan `retranqueo_linderos_m` (decisión del arquitecto (PAUSA F1)).
- `edificabilidad_m2m2` = 5.100 / 8.839 = **0.5769884** (aplicada sobre la superficie oficial da 5.100 m²c).
- `altura_max_m` = **altura de cornisa** (7,5 m / 10 m). La coronación (10,5 m / 13 m) no tiene clave en el generador y se anota aquí.
- `retranqueo_fachada_m` = retranqueo a **alineación exterior** (3 m / 5 m).
- `retranqueo_linderos_m`:
  - **Unifamiliar: 3 m.** El generador usa un único valor como distancia mínima de cualquier punto del edificio al lindero de la parcela. A UA-03-02 y ZV-02 llegan los extremos de hilera (3 m) o los testeros (3 m). El 0 m de la cédula solo se aplica a la medianera entre viviendas de la misma hilera, que el generador ya resuelve al adosar.
  - **Multifamiliar: 5 m** (linderos = testeros = 5 m).
- `viviendas_max` = **34** (cédula y decisión del arquitecto (PAUSA F1)).
- `fondo_edificable_m`, `separacion_edificios_m`, `longitud_max_bloque_m` = **null → FALTA DATO** (no figuran en la cédula). Las tipologías `unifamiliar_adosada`, `bloque_abierto` y `torre` necesitan la separación entre edificios, así que no se pueden generar completas hasta tener ese dato.
- `atico` y `computo` = **null**: no figuran en la cédula. El generador no genera ático y computa al 100 % cualquier concepto no computable que F2 declare como hipótesis, que es lo conservador.
- No se incluye bloque `hipotesis`, porque son parámetros de diseño de F2.

**Mezcla (decisión del arquitecto (PAUSA F1)).** Se mantienen **dos bloques**, uno por uso, cada uno sobre **la parcela completa**. Son las envolventes de cada tipo y **no representan la mezcla**. Al ser una mezcla, **F2 tendrá que repartir la parcela, la edificabilidad (5.100 m²c en total) y las viviendas (34 en total) entre los dos tipos**. Eso es una decisión de diseño, no de urbanismo. Si F2 ejecuta cada bloque sobre una subparcela, tendrá que ajustar `coordenadas`, `superficie_oficial_m2`, `edificabilidad_m2m2` y `viviendas_max` de cada bloque para que **la suma no supere 5.100 m²c ni 34 viviendas**. También tendrá que declarar como hipótesis la regla de ocupación y la separación entre las dos partes, que son FALTA DATO (sección 2.3). Si cada bloque se ejecuta tal cual, el generador limitará a 34 viviendas **cada uno**, no la suma.

### 6.1 UNIFAMILIAR (envolvente sobre la parcela completa)

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
    ],
    "superficie_oficial_m2": 8839
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
    "longitud_max_bloque_m": null,
    "viviendas_max": 34,
    "atico": null,
    "computo": null
  },
  "tipologias": ["unifamiliar_adosada", "unifamiliar_aislada"]
}
```

### 6.2 MULTIFAMILIAR (envolvente sobre la parcela completa)

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
    ],
    "superficie_oficial_m2": 8839
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
    "longitud_max_bloque_m": null,
    "viviendas_max": 34,
    "atico": null,
    "computo": null
  },
  "tipologias": ["bloque_abierto", "torre"]
}
```

| Clave | Unifamiliar | Multifamiliar | Origen |
|-------|-------------|---------------|--------|
| parcela.superficie_oficial_m2 | 8839 | 8839 | Cédula; decisión del arquitecto (PAUSA F1) |
| fachadas | [1, 2] | [1, 2] | Decisión del arquitecto (PAUSA F1); índices comprobados por el coordinador con `--lados` |
| edificabilidad_m2m2 | 0.5769884 | 0.5769884 | Derivado: 5.100 m²c / 8.839 m²s (cédula). **Total compartido** en la mezcla |
| ocupacion_pct | 60 | 45 | Cédula. Aplicación en la mezcla: FALTA DATO |
| plantas_max | 2 | 3 | Cédula |
| altura_max_m | 7.5 (coronación 10,5) | 10.0 (coronación 13) | Cédula (cornisa) |
| retranqueo_fachada_m | 3 | 5 | Cédula (alineación exterior; lados 1 y 2) |
| retranqueo_linderos_m | 3 (UA-03-02 y ZV-02; extremo de hilera = testero = 3; 0 solo entre viviendas) | 5 (UA-03-02 y ZV-02; linderos = testeros = 5) | Cédula + decisión del arquitecto (PAUSA F1) para la ZV-02 |
| viviendas_max | 34 | 34 | Cédula; decisión del arquitecto (PAUSA F1). **Total compartido** en la mezcla |
| separacion_edificios_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| fondo_edificable_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| longitud_max_bloque_m | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| atico | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |
| computo | null, **FALTA DATO** | null, **FALTA DATO** | No figura en la cédula |

PENDIENTE DE VALIDAR POR EL ARQUITECTO
