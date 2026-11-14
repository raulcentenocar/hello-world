# P02 · Hileras perimetrales + calle interior en anillo + zona común central

**Origen:** caso 01, la foto aérea de una implantación sobre la parcela UA-03-01 (`casos/caso_01_UA-03-01_foto.png`).

## Lo que se ve en el ejemplo (lectura sobre la imagen; cifras estimadas)

- **Solo casas adosadas, unas 34:** 7 + 7 en el borde norte, 8 paralelas a la Calle Floristas y 6 + 6 en dos hileras norte-sur al sureste.
- **Cada hilera sigue su lindero.** El jardín privado queda hacia el borde de la parcela y la entrada hacia dentro.
- **Unas 2 plazas por casa dentro de la parcela privada**, delante de la fachada de entrada. No hay bolsa común.
- **Un solo acceso controlado**, desde la Calle Floristas, con garita.
- **Viario interior que reparte a todas las hileras:** una calle bajo la hilera norte, otra paralela a Floristas, un ramal este-oeste y una calle norte-sur con casas a los dos lados.
- **Zona común en el centro:** piscina, juegos infantiles y un pequeño edificio social.
- **Franja ajardinada perimetral** junto a las calles públicas, que coincide con los retranqueos.

## Reglas del patrón en el motor

Para cada lindero, o grupo de linderos casi alineados (menos de 15° de diferencia):

| Franja desde el lindero hacia dentro | Ancho |
|---|---|
| Jardín trasero (incluye el retranqueo) | máx(retranqueo, `jardin_trasero_m`) |
| Casa | `fondo_casa_m` |
| Plazas en la parcela privada, delante de la casa | `plaza_fondo_m` |
| Acera (opcional) | `acera_m` |
| Calle interior (anillo) | `calzada_m` |

- **Anillo.** La calle interior une las franjas de calzada de todos los linderos y forma un anillo, así que no hay vía sin salida. Se conecta al acceso con un vial perpendicular al lindero de acceso. En la barra de parámetros, la posición del acceso va de 0 a 1 a lo largo de ese lindero.
- **Prioridad en las esquinas.** Se colocan primero las hileras de los linderos más largos. Las demás guardan la separación entre edificios con ellas.
- **Interior del anillo.** Hay dos opciones: `zona_comun`, que lo deja todo como zona común, o `casas`, que pone hileras mirando al anillo con jardín hacia el centro y deja el resto como zona común. Se comprueba que la zona común es al menos `zona_comun_min_m2`, una hipótesis de producto.
- **Exceso de casas.** Si caben más casas de las que permiten la edificabilidad o el número máximo de viviendas, se quitan primero las más lejanas al acceso, sin dejar hileras por debajo del mínimo.

## Qué revisar de normativa

- **Anillo:** sin fondos de saco, así que cumple DB-SI SI 5 sin espacio de maniobra. Las calles del ejemplo sin acera necesitan plataforma única o acera (DB-SUA 9).
- **Plazas en la parcela privada:** cuentan para el estándar de 2 por vivienda si la ordenanza lo admite (FALTA DATO).
- **Jardín trasero dentro del retranqueo:** hay que confirmar con la ordenanza que el retranqueo puede ser jardín privado y que el cerramiento cumple las condiciones de vallado.
- **Zona común:** su cómputo y su régimen (elementos comunes de la comunidad) dependen de la promoción.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
