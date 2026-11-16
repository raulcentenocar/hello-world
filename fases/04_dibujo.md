# F4 — Dibujo DXF · Parcela UA-03-01, Sector-1 "Los Pocillos" · Variante V1 «Calle de casas»

Agente: dibujo · Fecha: 2026-11-16 · Base: `01_urbanismo.md` (rev. 2), `02_diseno.md` (V1), `03_estructura.md`, `03_instalaciones.md`, `03_normativa.md`, `conflictos.md` y `planos/esquema_V1.svg`.

**Alcance (cambio del arquitecto, comunicado por el coordinador):** solo DXF. No se generan el IFC ni el DXF 3D. El `ifcopenshell` que se instaló al principio de la sesión se ha desinstalado sin llegar a usarse. En `planos/` no queda nada de IFC ni de 3D.

## 1. Archivos generados (`planos/`)

| Archivo | Contenido | Coordenadas / escala |
|---|---|---|
| `V1_implantacion.dxf` | Parcela (6 vértices de la cédula), retranqueos de 3 y 5 m, 24 casas numeradas con medianeras, testeros y junta, bloque (contorno, ejes y 21 pilares), viario, 69 plazas + 1 accesible, jardines privados, pasos peatonales, cotas principales, textos, leyenda y capa **CONFLICTOS_F3** | **UTM ETRS89 30N (EPSG:25830)**, 1:500 |
| `V1_casa_tipo.dxf` | Casa U-V1 de 6,50 × 12,00 m: planta baja y planta primera con las estancias y superficies de F2, el patinillo PU de 0,80 × 0,40 m (E5), los ejes y las cotas | Local de la casa, 1:50 |
| `V1_bloque_planta_tipo.dxf` | Bloque M-V1: planta tipo (P1 y P2, 4 viviendas M-V1-a) y PB esquemática (2 M-V1-b y comunes), con la retícula ajustada 2 × 5,75 × 6 × 6,17 m, los pilares, los núcleos, los patinillos PB-1 a PB-4, la zona 6d y los portales | Local F2 (origen en el vértice 3), 1:100 |

Los tres DXF están en metros (`$INSUNITS` = 6). Las cotas usan coma decimal y todos los planos llevan un cajetín con la leyenda «PENDIENTE DE VALIDAR POR EL ARQUITECTO».

## 2. Scripts y comandos (desde la raíz del repositorio)

```bash
python3 scripts/dibujo_v1.py             # genera los 3 DXF
python3 scripts/comprobar_dibujo_v1.py   # los abre, audita y comprueba (sale con código 1 si algo falla)
```

Dependencias: `ezdxf` 1.4.5 y `shapely` 2.2 (`scripts/requirements.txt`). Todos los datos están al principio de `scripts/dibujo_v1.py`, con su fuente citada. Los retranqueos se calculan con un offset interior de shapely sobre las cuerdas.

## 3. Capas

`U-PARCELA`, `U-RETRANQUEO`, `U-VIARIO`, `U-PLAZA`, `U-PLAZA-ACCESIBLE`, `U-JARDIN`, `U-PEATONAL`, `A-CASA`, `A-CASA-NUM`, `A-MURO`, `A-TABIQUE`, `A-CARPINTERIA`, `A-BLOQUE`, `S-EJE`, `S-PILAR`, `S-VIGA`, `I-PATINILLO`, `A-COTA`, `A-TEXTO`, `A-CAJETIN`, **`POSICION_APROXIMADA`** (todo lo que no tiene cota en los entregables) y **`CONFLICTOS_F3`**.

`A-CARPINTERIA` está vacía porque F2 no define huecos. `S-VIGA` solo contiene una nota: no hay vigas de cuelgue (03_estructura 1.2 y 4.2).

## 4. Comprobaciones (`python3 scripts/comprobar_dibujo_v1.py` → **TODO CORRECTO**)

| Archivo | Entidades | Auditoría | Comprobaciones |
|---|---|---|---|
| Implantación | 387 (A-CASA 24, A-CASA-NUM 24, A-MURO 30, U-PLAZA 69, U-PLAZA-ACCESIBLE 3, S-PILAR 21, S-EJE 30, CONFLICTOS_F3 38, POSICION_APROXIMADA 24, U-RETRANQUEO 4…) | 0 errores | **24 casas** de 6,50 × 12,00, numeradas del 1 al 24 · 6 vértices UTM idénticos a la cédula · 10 códigos de conflicto presentes (13 círculos) · 48 + 21 plazas ordinarias + 1 accesible · 21 pilares |
| Casa tipo | 142 | 0 errores | Patinillo PU de 0,80 (E-O) × 0,40 (N-S) en PB y P1 · estancias de F2 rotuladas |
| Bloque | 242 | 0 errores | **10 viviendas** (4 M-V1-a × 2 plantas + 2 M-V1-b en PB) · 21 pilares por planta · 4 patinillos por planta |

También se han revisado a ojo las vistas previas renderizadas con `python3 -m ezdxf draw`.

## 5. Conflictos dibujados (no se ha resuelto ninguno)

- **Implantación:** N-1, N-2, E1, E3, E4/I-3/N-4 (en los 2 núcleos), E6, I-8, I-9 (2 portales), NC-1 (2 portales) y NC-5.
- **Casa tipo:** E5/I-1/I-2, E2, N-3 e I-5.
- **Bloque:** E4/I-3/N-4 (más los recuadros de la zona 6d alrededor de B2, B3, B5 y B6), I-9, NC-1, I-7, E3 e I-5.

Se ha dibujado lo último aprobado:
- la junta de E1 con doble muro centrado en x = 28,0, sin cambiar la envolvente;
- **1 plaza accesible**, como en el trazado de F2 (NC-5 sigue abierto);
- fondo de saco sin martillo;
- sin acera ni rampa.

## 6. Limitaciones (FALTA DATO o posición aproximada)

- **Linderos curvos:** se dibujan las cuerdas, porque el sentido y los centros de los arcos son FALTA DATO.
- **Sin cotas verticales:** no hay topografía ni rasantes. Es solo planta.
- **Elemento SE:** marcado como FALTA DATO.
- **Casa tipo:**
  - los rectángulos de las estancias son esquemáticos y las superficies rotuladas son las de F2. La suma de útiles de F2 (60,5 m² en PB) es menor que el interior con muros de 24 cm; la diferencia queda en blanco;
  - espesor de fachada: FALTA DATO (se representa con 0,24);
  - lado de la escalera y simetría de cada hilera: FALTA DATO (se dibuja la escalera al oeste);
  - posición N-S del patinillo: aproximada.
- **Bloque:**
  - núcleos, patinillos, portales y límites de las viviendas: aproximados;
  - la distribución de la PB no está definida en F2;
  - PE/PT, AC y CI no tienen posición en F3 y no se dibujan.
- **Elementos no dibujados por no estar decididos:** CT (I-8), topes de rueda (E6) y muro arriostrante E-O (E2).

## 7. Incoherencias encontradas

- **D-1 (nueva, anotada en `conflictos.md`):** con los ejes de fachada a 0,25 m, los pilares de 30 × 40 quedan a 0,05 m de la cara exterior del bloque. El cerramiento no cabe por delante de ellos sin salirse de la envolvente de 12,00 × 37,50 m.
- **NC-1 y NC-5** están en `03_normativa.md` pero **no tienen fila en la tabla de `conflictos.md`**. Se dibujan igualmente. Lo señalo para que el coordinador decida si se añaden.

## 8. Decisiones pendientes para el arquitecto

1. D-1: retícula del bloque frente al cerramiento: (a) meter más los ejes, (b) cerramiento entre pilares o (c) girar los pilares de fachada.
2. Los conflictos abiertos de F3 (sección 5). Al decidirlos habrá que regenerar los DXF; en particular NC-5 (2.ª plaza accesible), N-1/N-2 (trazado de la calle) y E1.
3. Geometría exacta de los arcos y topografía, para pasar de las cuerdas y del dibujo solo en planta a la geometría definitiva.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
