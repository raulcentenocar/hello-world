# Criterios de proyecto para implantaciones residenciales

Son los criterios que aplica un arquitecto al ordenar una promoción, sacados del análisis de promociones de los estudios y promotoras de referencia (ver «Referencias» al final). Cada criterio indica cómo lo usa el motor: **regla** (obligatorio al generar), **indicador** (se mide y sirve para comparar) o **pendiente**.

## 1. Producto que construye el mercado (promotoras)

- **Urbanización cerrada con un único acceso controlado** (garita o control automático). Es el estándar en las unifamiliares de Neinor (Torrejón Park Homes), Metrovacesa y Kronos. → *Regla en P02: un solo acceso.*
- **Zona común central** con piscina de adultos e infantil, solárium, juegos infantiles y zonas ajardinadas. En las promociones medianas se añade una sala comunitaria o un gimnasio; en las grandes, pádel, coworking o club social (Kronos Nolita, AEDAS/Cano y Escario Piteas). → *Indicador: m² de zona común frente a un programa tipo según el número de viviendas.*
- **Adosados con jardín privado y aparcamiento propio**, en la parcela (Neinor Virentia: aparcamiento en parcela) o en sótano privado bajo la vivienda (Villas del Támesis, de Hombre de Piedra para Metrovacesa: 158 m² en 2 plantas + sótano con garaje). → *Regla en P02: plazas en la parcela. El sótano privado es el patrón P08 (pendiente).*
- **Tipologías mezcladas** en un mismo conjunto (Kronos Mirage en Los Pocillos: unifamiliares de 3 y 4 dormitorios con plurifamiliares de 2 y 3; Cano y Escario en Montegancedo: 360 plurifamiliares + 150 unifamiliares). → *P01 (casas + bloques) y P07 (mixto, pendiente).*
- **«Libre de tráfico rodado»** como argumento comercial (Torrejón Park Homes III): coches en la periferia o bajo rasante e interior peatonal. → *Patrón P08 (pendiente).*

## 2. Criterios de arquitectura (estudios)

- **Orientación.** Estancias y jardines privados a sur, sureste o suroeste. → *Indicador: % de casas con el jardín a S, SE o SO.*
- **Viviendas pasantes**, con doble orientación y ventilación cruzada (Bakpak, propuesta JANO). → *Regla en P01: portales con una vivienda pasante a cada lado.*
- **Adaptación al terreno** con bloques escalonados planta a planta (Morph, Prado Pozuelo). → *Pendiente: necesita topografía (FALTA DATO).*
- **Zonas comunes alejadas de los bloques**, para dar privacidad (Morph, Prado Pozuelo). → *Indicador futuro: distancia de la zona común a las fachadas.*
- **Implantación que sigue el terreno y conserva el arbolado** (L35, Village Verde Sotogrande). → *Pendiente: necesita topografía y arbolado.*
- **Industrialización** con CLT y semisótano de hormigón (Hombre de Piedra). → *Fuera del alcance del motor de implantación; pasa a estructura.*

## 3. Criterios de urbanización (coste y normativa)

- **Poco viario por vivienda.** El viario interior es coste de urbanización que no se vende. → *Indicador: m² de calzada + acera por vivienda.*
- **Sin fondos de saco largos.** Lazo o anillo, o fondo de saco ≤ 20 m o con espacio de maniobra (DB-SI SI 5). → *Comprobación.*
- **Itinerario peatonal accesible** hasta cada vivienda: acera o plataforma única (DB-SUA 9). → *Comprobación.*
- **Franja verde junto a las calles públicas.** El retranqueo se trata como jardín o seto. → *Regla: en P02 el jardín trasero cubre el retranqueo.*
- **Hileras de 3 a 8 casas** con pasos entre ellas. → *Regla (`casas_min_hilera`, `casas_max_hilera`).*

## Programa tipo de zona común (hipótesis para comparar, no normativa)

| Elemento | m² orientativos | A partir de |
|---|---|---|
| Piscina de adultos + playa | 150 | 1 vivienda |
| Piscina infantil | 30 | 1 vivienda |
| Juegos infantiles | 80 | 1 vivienda |
| Estancia ajardinada | 200 | 1 vivienda |
| Sala comunitaria o gimnasio | 80 | 40 viviendas |
| Pista de pádel (con bandas) | 230 | 80 viviendas |

Las superficies son orientativas, para dimensionar en fase de implantación. Las fija el arquitecto.

## Referencias consultadas

- Metrovacesa, Villas del Tíber (31 adosados en 4 hileras con zona central): [metrovacesa.com](https://metrovacesa.com/en/blog/metrovacesa-obtains-planning-permission-for-villas-del-tiber-31-townhouses-with-solarium-and-garden), [brainsre.news](https://brainsre.news/?p=182223)
- Metrovacesa y Hombre de Piedra, Villas del Támesis: [metrovacesa.com](https://metrovacesa.com/en/blog/metrovacesa-obtains-building-permission-for-50-single-family-homes-in-palmas-altas-the-villas-del-tamesis-development)
- Neinor, Torrejón Park Homes: [estrategiasdeinversion.com](https://www.estrategiasdeinversion.com/actualidad/noticias/empresas/neinor-homes-lanza-la-tercera-fase-de-torrejon-n-746451), [brainsre.news](https://brainsre.news/neinor-homes-torrejon-park-homes-iii-36-viviendas-torrejon-ardoz-madrid/), [hcparquitectos.com](https://hcparquitectos.com/projects/torrejon-park-homes-en/)
- Kronos, Mirage (Los Pocillos): [kronoshomes.com](https://www.kronoshomes.com/en/projects/madrid/mirage), [brainsre.news](https://brainsre.news/kronos-destina-80-millones-villanueva-canada-mirage/); sector Los Pocillos: [brainsre.news](https://brainsre.news/los-pocillos-2975-viviendas-villanueva-canada-madrid/)
- Kronos, zonas comunes (Nolita, Bloom…): [brainsre.news](https://brainsre.news/kronos-homes-nolita-valladolid-residencial/)
- AEDAS y Cano y Escario, Piteas (Pozuelo): [aedashomes.com](https://www.aedashomes.com/pisos-obra-nueva-piteas-pozuelo-de-alarcon), [alimarket.es](https://www.alimarket.es/construccion/noticia_amp/313859/pozuelo-aprueba-el-desarrollo-de-mas-de-1-000-viviendas)
- Morph Estudio, Prado Pozuelo: [proarquitectura.es](https://proarquitectura.es/pdf/PM-135%203-min.pdf)
- L35, Village Verde Sotogrande: [sotogrande.com](https://sotogrande.com/destination/l35-architects-the-vision-behind-village-verde-and-their-commitment-to-sotogrande/), [archeyes.com](https://archeyes.com/village-verde-sotogrande-apartments-by-l35-architects/)
- Bakpak, JANO (Madrid 0,0): [metalocus.es](https://www.metalocus.es/es/noticias/bakpak-architects-segundo-premio-de-madrid-00)
- Cano Lasso, 87 VPO en Vallecas: [divisare.com](https://divisare.com/projects/222583-estudio-cano-lasso-arquitectos-87-vpo-en-vallecas)
- Hombre de Piedra: [archello.com](https://archello.com/es/brand/hombre-de-piedra-arquitectos)

**Límite de este análisis:** desde la sesión no se pueden abrir los planos ni las imágenes de estas promociones; las reglas salen de las descripciones publicadas. Los planos o fotos de implantación que me pases (como el caso 01) son lo que permite fijar dimensiones reales.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
