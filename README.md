# Memoria de Proyecto

Herramienta web para **revisar la normativa aplicable** a un proyecto de arquitectura en España y **redactar la memoria** con el criterio de un arquitecto. La redacción la hace Claude (API de Anthropic).

Funciona directamente en el navegador. No hay servidor ni nada que instalar, así que se puede publicar con GitHub Pages.

## Qué hace

1. **Datos del proyecto.** Un formulario recoge la identificación, el emplazamiento, el uso, el tipo de intervención, las superficies, las alturas, los sistemas constructivos, el PEM y los datos de obra.
2. **Revisión normativa preliminar.** Es automática e inmediata y no usa IA.
   - Lista la normativa aplicable según el uso y la intervención: LOE, CTE y sus DB, Código Estructural, NCSE-02, RITE, REBT, RIPCI, ICT, RSCIEI, RD 1627/1997, RD 105/2008, RD 390/2021, accesibilidad, habitabilidad, ruido, etc.
   - Hace comprobaciones rápidas:
     - Ocupación.
     - Sectores de incendio y salidas de planta.
     - Protección de escaleras.
     - Columna seca y ascensor de emergencia.
     - Resistencia al fuego (R).
     - Barreras de protección y ascensor accesible.
     - Radón.
     - HE 4, HE 5 y HE 6.
     - NCSE-02.
     - Estudio geotécnico.
     - Estudio (básico) de seguridad y salud.
     - Estudio de gestión de RCD.
3. **Redacción de la memoria.** Sigue la estructura del Anejo I de la Parte I del CTE:
   - Memoria descriptiva.
   - Memoria constructiva.
   - Cumplimiento de cada DB.
   - Otros reglamentos.
   - Anejos: RCD, seguridad y salud, control de calidad, uso y mantenimiento.

   Funcionamiento:
   - Cada apartado se genera por separado. A cada uno se le pueden dar indicaciones propias, y el texto se puede editar a mano.
   - Los datos que faltan aparecen marcados como `[COMPLETAR: …]`. Los valores que conviene contrastar aparecen como `[VERIFICAR]`. No se inventan datos del proyecto.
   - Hay una opción para contrastar la vigencia de la normativa con búsqueda web, limitada a fuentes oficiales: BOE, codigotecnico.org, MIVAU e IDAE.
   - La memoria se exporta a Markdown o Word, o se imprime / guarda como PDF.
4. **Consulta normativa.** Un chat para hacer preguntas sobre el proyecto. Las respuestas citan la norma, el apartado y la tabla.

Los proyectos se guardan automáticamente en el navegador y se pueden exportar o importar como archivo `.json`.

## Uso

1. Publique el repositorio con GitHub Pages (Settings → Pages → rama principal), o abra `index.html` con un servidor local, por ejemplo `python3 -m http.server`.
2. En **Ajustes**, introduzca su clave de API de Anthropic (se obtiene en console.anthropic.com).
   - La clave solo se guarda en su navegador.
   - Desde el navegador se envía directamente a la API de Anthropic.
3. Rellene los datos del proyecto y revise la pestaña **Revisión normativa**.
4. En **Memoria**, seleccione los apartados (o use «básico») y pulse **Generar**.

## Estructura del código

| Archivo | Contenido |
|---|---|
| `js/normativa.js` | Catálogo de normativa con reglas de aplicación y estructura de la memoria (Anejo I CTE). |
| `js/checker.js` | Comprobaciones normativas automáticas. |
| `js/prompts.js` | Instrucciones del «arquitecto redactor» y del consultor normativo. |
| `js/claude.js` | Llamadas a la API de Claude (streaming y búsqueda web en fuentes oficiales). |
| `js/app.js` | Interfaz. |
| `tests/` | Pruebas de las comprobaciones (`npm test`, requiere Node 18+). |

Para ampliar la herramienta, por ejemplo con normativa autonómica, nuevas comprobaciones o nuevos usos:

- Añada entradas a `CATALOGO` en `js/normativa.js`.
- Añada las reglas nuevas en `comprobaciones()` de `js/checker.js`.

## Aviso

Esta herramienta genera **borradores de trabajo**:

- Los umbrales y las referencias normativas son orientativos.
- Hay que verificarlos siempre con el texto vigente (BOE, codigotecnico.org) y con la normativa autonómica y municipal.
- La responsabilidad del proyecto corresponde al técnico que lo firma.
