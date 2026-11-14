# Catálogo de patrones de implantación

Aquí guarda el estudio lo que aprende de promociones reales: planos, fotos aéreas, renders o proyectos propios. Cada ejemplo se convierte en dos cosas.

1. **Un patrón** (`Pnn_*.md`): una forma de ordenar la parcela descrita con reglas fijas (orientación de hileras, viario, aparcamiento, zonas comunes), con sus parámetros y con lo que hay que revisar de normativa. Si el patrón está programado, el motor (`scripts/variantes_generador.py` y el visor) lo genera como una estrategia más.
2. **Un caso de referencia** (`casos/caso_nn_*.json` + imagen): las cifras del ejemplo (viviendas, plazas, accesos, zonas comunes). La prueba `scripts/prueba_casos.py` comprueba que el motor es capaz de reproducirlo.

Así, cada foto nueva amplía lo que el motor sabe hacer y queda como prueba para no perderlo en cambios futuros.

## Cómo añadir un ejemplo

1. Guarda la imagen en `casos/` y pásamela en la conversación.
2. Lo analizo y escribo su caso (`caso_nn_*.json`): parcela, cifras leídas del ejemplo y patrón al que corresponde. Las cifras leídas de una imagen se marcan como **estimadas**.
3. Si el patrón no existe, se crea su ficha y se programa en el motor.
4. Se ejecuta `python3 scripts/prueba_casos.py`: el motor debe acercarse al ejemplo dentro de la tolerancia del caso.

## Patrones

| Código | Patrón | Origen | Estado en el motor |
|---|---|---|---|
| P01 | Calles paralelas (peine): hileras en una dirección, calles desde la fachada de acceso, bloques en otra zona | Motor inicial | Programado (`calles_paralelas`) |
| P02 | Hileras perimetrales + calle interior en anillo + zona común central | Caso 01 (foto de la UA-03-01) | Programado (`perimetral`) |
| P03 | Lazo con hileras a ambos lados y zona común en el centro del lazo | Patrón habitual (Radburn) | Pendiente |
| P04 | Peine con fondos de saco cortos desde un vial colector | Patrón habitual | Pendiente |
| P05 | Manzana con bloque perimetral y patio común | Patrón habitual en ensanches | Pendiente |
| P06 | Bloques lineales con zona común central y aparcamiento perimetral | Patrón habitual | Pendiente |
| P07 | Mixto: casas perimetrales y bloque en la fachada principal | Patrón habitual | Pendiente |

Los patrones «habituales» proceden de tipologías generales de ordenación residencial (hileras, manzana perimetral, bloque lineal, lazo y fondo de saco). Se concretarán cuando haya un ejemplo real del estudio que sirva de caso.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
