// Base de conocimiento normativo (España).
// IMPORTANTE: los valores y umbrales son orientativos y deben contrastarse
// con el texto vigente publicado en el BOE / codigotecnico.org. La herramienta
// es una ayuda a la redacción: la responsabilidad del proyecto es del técnico.

export const USOS = {
  vivienda_unifamiliar: { nombre: "Residencial Vivienda (unifamiliar)", grupo: "vivienda", densidad: 20 },
  vivienda_plurifamiliar: { nombre: "Residencial Vivienda (plurifamiliar)", grupo: "vivienda", densidad: 20 },
  residencial_publico: { nombre: "Residencial Público", grupo: "residencial_publico", densidad: 20 },
  administrativo: { nombre: "Administrativo", grupo: "administrativo", densidad: 10 },
  comercial: { nombre: "Comercial", grupo: "comercial", densidad: 2 },
  docente: { nombre: "Docente", grupo: "docente", densidad: 1.5 },
  hospitalario: { nombre: "Hospitalario", grupo: "hospitalario", densidad: 15 },
  publica_concurrencia: { nombre: "Pública Concurrencia", grupo: "publica_concurrencia", densidad: 1.5 },
  aparcamiento: { nombre: "Aparcamiento", grupo: "aparcamiento", densidad: 15 },
  industrial: { nombre: "Industrial / Almacén", grupo: "industrial", densidad: 40 },
};

export const INTERVENCIONES = {
  nueva: "Obra nueva",
  ampliacion: "Ampliación",
  reforma_integral: "Reforma / rehabilitación integral",
  reforma_parcial: "Reforma parcial",
  cambio_uso: "Cambio de uso",
  rehabilitacion_energetica: "Rehabilitación energética de envolvente / instalaciones",
  urbanizacion: "Urbanización / obra civil",
};

export const ESTRUCTURAS = {
  hormigon: "Hormigón armado",
  acero: "Acero",
  madera: "Madera",
  fabrica: "Fábrica (muros de carga)",
  mixta: "Mixta",
  sin_intervencion: "Sin intervención estructural",
};

export const FASES = {
  basico: "Proyecto básico",
  ejecucion: "Proyecto de ejecución",
  basico_ejecucion: "Proyecto básico y de ejecución",
};

const esVivienda = (p) => USOS[p.uso]?.grupo === "vivienda";
const esNuevaOAmpl = (p) => ["nueva", "ampliacion"].includes(p.intervencion);
const esIntegral = (p) => ["nueva", "ampliacion", "reforma_integral", "cambio_uso"].includes(p.intervencion);
const tocaEstructura = (p) => esNuevaOAmpl(p) || (p.estructura && p.estructura !== "sin_intervencion");
const esEdificacion = (p) => p.intervencion !== "urbanizacion";

// Catálogo: cada entrada tiene una función `aplica(p)` que devuelve
// false | true | string (motivo / matiz de aplicación).
export const CATALOGO = [
  // ---------- Marco general ----------
  { id: "LOE", grupo: "Marco general", titulo: "Ley 38/1999, de Ordenación de la Edificación (LOE)",
    aplica: (p) => esEdificacion(p) },
  { id: "CTE", grupo: "Marco general", titulo: "RD 314/2006, Código Técnico de la Edificación (CTE), Parte I y modificaciones (RD 732/2019, RD 450/2022)",
    aplica: (p) => esEdificacion(p) },
  { id: "URB", grupo: "Marco general", titulo: "Planeamiento urbanístico municipal (PGOU / NNSS / ordenanzas) y legislación urbanística autonómica",
    aplica: () => true },
  { id: "HAB", grupo: "Marco general", titulo: "Normativa autonómica de habitabilidad / diseño de viviendas",
    aplica: (p) => esVivienda(p) ? "Verificar decreto vigente en la comunidad autónoma" : false },
  { id: "ACC", grupo: "Marco general", titulo: "RDL 1/2013 (derechos de las personas con discapacidad), Orden TMA/851/2021 (espacios públicos urbanizados) y normativa autonómica de accesibilidad",
    aplica: () => true },

  // ---------- CTE: Documentos Básicos ----------
  { id: "DB-SE", grupo: "CTE", titulo: "DB SE Seguridad Estructural (SE, SE-AE, SE-C)",
    aplica: (p) => tocaEstructura(p) || false },
  { id: "DB-SE-A", grupo: "CTE", titulo: "DB SE-A Acero",
    aplica: (p) => ["acero", "mixta"].includes(p.estructura) },
  { id: "DB-SE-F", grupo: "CTE", titulo: "DB SE-F Fábrica",
    aplica: (p) => ["fabrica", "mixta"].includes(p.estructura) },
  { id: "DB-SE-M", grupo: "CTE", titulo: "DB SE-M Madera",
    aplica: (p) => ["madera", "mixta"].includes(p.estructura) },
  { id: "DB-SI", grupo: "CTE", titulo: "DB SI Seguridad en caso de Incendio",
    aplica: (p) => p.uso === "industrial" ? "Solo zonas de uso no industrial; el establecimiento industrial se rige por el RSCIEI" : esEdificacion(p) },
  { id: "DB-SUA", grupo: "CTE", titulo: "DB SUA Seguridad de Utilización y Accesibilidad",
    aplica: (p) => esEdificacion(p) },
  { id: "DB-HS", grupo: "CTE", titulo: "DB HS Salubridad (HS1 a HS6)",
    aplica: (p) => esEdificacion(p) },
  { id: "DB-HR", grupo: "CTE", titulo: "DB HR Protección frente al Ruido",
    aplica: (p) => {
      if (p.uso === "industrial") return false;
      if (p.intervencion === "reforma_parcial") return "Solo si la reforma afecta a elementos de separación o es rehabilitación integral";
      return esEdificacion(p);
    } },
  { id: "DB-HE", grupo: "CTE", titulo: "DB HE Ahorro de Energía (HE0 a HE6)",
    aplica: (p) => esEdificacion(p) },

  // ---------- Estructuras ----------
  { id: "CE", grupo: "Estructuras", titulo: "RD 470/2021, Código Estructural (hormigón y acero)",
    aplica: (p) => ["hormigon", "acero", "mixta"].includes(p.estructura) },
  { id: "NCSE", grupo: "Estructuras", titulo: "RD 997/2002, Norma de Construcción Sismorresistente NCSE-02",
    aplica: (p) => {
      if (!tocaEstructura(p)) return false;
      const ab = Number(p.ab);
      if (!Number.isFinite(ab) || p.ab === "" || p.ab == null) return "Indicar aceleración sísmica básica (ab) del municipio (Anejo 1 NCSE-02)";
      if (ab < 0.04) return false;
      if (ab < 0.08) return "Exenta si es de importancia normal con pórticos bien arriostrados en todas direcciones (art. 1.2.3); comprobar";
      return true;
    } },

  // ---------- Instalaciones ----------
  { id: "RITE", grupo: "Instalaciones", titulo: "RD 1027/2007, Reglamento de Instalaciones Térmicas en los Edificios (RITE)",
    aplica: (p) => esEdificacion(p) },
  { id: "REBT", grupo: "Instalaciones", titulo: "RD 842/2002, Reglamento Electrotécnico para Baja Tensión (REBT) e ITC-BT",
    aplica: () => true },
  { id: "ITC-BT-52", grupo: "Instalaciones", titulo: "ITC-BT-52 Infraestructura para la recarga de vehículos eléctricos",
    aplica: (p) => Number(p.plazasAparcamiento) > 0 },
  { id: "RIPCI", grupo: "Instalaciones", titulo: "RD 513/2017, Reglamento de Instalaciones de Protección contra Incendios (RIPCI)",
    aplica: (p) => p.uso !== "vivienda_unifamiliar" ? true : "Si se disponen instalaciones de protección contra incendios" },
  { id: "ICT", grupo: "Instalaciones", titulo: "RDL 1/1998 y RD 346/2011, Infraestructuras Comunes de Telecomunicaciones (ICT)",
    aplica: (p) => {
      if (p.uso === "vivienda_plurifamiliar") return true;
      if (["residencial_publico", "administrativo", "comercial"].includes(p.uso)) return "Si el edificio está en régimen de propiedad horizontal o arrendamiento > 1 año";
      return false;
    } },
  { id: "ASC", grupo: "Instalaciones", titulo: "RD 203/2016 (ascensores) y RD 88/2013 ITC AEM 1",
    aplica: (p) => Number(p.plantasSobre) + Number(p.plantasBajo || 0) > 1 ? "Si se instalan ascensores" : false },
  { id: "GAS", grupo: "Instalaciones", titulo: "RD 919/2006, Reglamento técnico de distribución y utilización de combustibles gaseosos",
    aplica: (p) => /gas/i.test(p.instalaciones || "") },

  // ---------- Energía ----------
  { id: "CEE", grupo: "Energía", titulo: "RD 390/2021, Procedimiento básico para la certificación de la eficiencia energética de los edificios",
    aplica: (p) => {
      if (esIntegral(p)) return true;
      if (p.intervencion === "rehabilitacion_energetica" || p.intervencion === "reforma_parcial") return "Si se reforma > 25 % de la envolvente, se amplía > 25 % o se reforman las instalaciones térmicas";
      return false;
    } },

  // ---------- Usos específicos ----------
  { id: "RSCIEI", grupo: "Usos específicos", titulo: "RD 2267/2004, Reglamento de Seguridad contra Incendios en Establecimientos Industriales",
    aplica: (p) => p.uso === "industrial" },
  { id: "LT", grupo: "Usos específicos", titulo: "RD 486/1997, disposiciones mínimas de seguridad y salud en los lugares de trabajo",
    aplica: (p) => ["administrativo", "comercial", "docente", "hospitalario", "industrial", "publica_concurrencia"].includes(p.uso) },
  { id: "DOC", grupo: "Usos específicos", titulo: "RD 132/2010, requisitos mínimos de los centros docentes",
    aplica: (p) => p.uso === "docente" ? "Según tipo de enseñanza; más normativa autonómica" : false },
  { id: "SAN", grupo: "Usos específicos", titulo: "RD 1277/2003 (centros sanitarios) y normativa autonómica sanitaria",
    aplica: (p) => p.uso === "hospitalario" },
  { id: "ESP", grupo: "Usos específicos", titulo: "Normativa autonómica de espectáculos públicos y actividades recreativas",
    aplica: (p) => p.uso === "publica_concurrencia" },
  { id: "PISC", grupo: "Usos específicos", titulo: "RD 742/2013, criterios técnico-sanitarios de las piscinas",
    aplica: (p) => /piscina/i.test(`${p.programa || ""} ${p.descripcion || ""}`) },
  { id: "ACT", grupo: "Usos específicos", titulo: "Ordenanza municipal de actividades / licencia de actividad y normativa ambiental autonómica",
    aplica: (p) => !esVivienda(p) },

  // ---------- Medio ambiente ----------
  { id: "RUIDO", grupo: "Medio ambiente", titulo: "Ley 37/2003 del Ruido, RD 1367/2007 y ordenanza municipal de ruido",
    aplica: (p) => esVivienda(p) ? "Comprobar zonificación acústica del emplazamiento" : true },
  { id: "RCD", grupo: "Medio ambiente", titulo: "RD 105/2008 (residuos de construcción y demolición) y Ley 7/2022 de residuos",
    aplica: () => true },

  // ---------- Obra ----------
  { id: "SYS", grupo: "Seguridad y salud", titulo: "RD 1627/1997, disposiciones mínimas de seguridad y salud en las obras",
    aplica: () => true },
  { id: "CC", grupo: "Control de calidad", titulo: "Plan de control de calidad (CTE Parte I, art. 6 y 7; normativa autonómica de control de calidad)",
    aplica: (p) => p.fase !== "basico" },
];

// Estructura de la memoria según el Anejo I de la Parte I del CTE
// (contenido del proyecto). `basico: true` indica que forma parte habitualmente
// del proyecto básico (contenido orientativo; verificar Anejo I y exigencias municipales).
export const ESTRUCTURA_MEMORIA = [
  { id: "1.1", cap: "1. Memoria descriptiva", titulo: "Agentes", basico: true,
    guia: "Promotor, proyectista(s), otros técnicos intervinientes (estructuras, instalaciones, coordinador SyS), dirección facultativa si se conoce." },
  { id: "1.2", cap: "1. Memoria descriptiva", titulo: "Información previa", basico: true,
    guia: "Antecedentes y condicionantes de partida, emplazamiento, entorno físico, datos del solar (superficie, linderos, topografía, servicios urbanísticos), normativa urbanística de aplicación, otras normativas, datos de la edificación existente si la hay." },
  { id: "1.3", cap: "1. Memoria descriptiva", titulo: "Descripción del proyecto", basico: true,
    guia: "Descripción general del edificio, programa de necesidades, uso característico y otros usos previstos, relación con el entorno. Cumplimiento del CTE y otras normativas específicas (resumen). Descripción de la geometría, volumen, superficies útiles y construidas (cuadro de superficies), accesos y evacuación. Descripción general de los parámetros que determinan las previsiones técnicas (sistema estructural, compartimentación, envolvente, acabados, acondicionamiento ambiental, servicios). Ficha / cuadro de cumplimiento urbanístico (parámetro, normativa, proyecto)." },
  { id: "1.4", cap: "1. Memoria descriptiva", titulo: "Prestaciones del edificio", basico: true,
    guia: "Prestaciones por requisitos básicos (seguridad estructural, incendio, utilización y accesibilidad, salubridad, ruido, ahorro de energía; funcionalidad) en relación con las exigencias básicas del CTE. Prestaciones que superan los umbrales del CTE, si las hay. Limitaciones de uso del edificio en su conjunto y de cada dependencia e instalación." },
  { id: "2.1", cap: "2. Memoria constructiva", titulo: "Sustentación del edificio", basico: false,
    guia: "Justificación de las características del suelo y parámetros a considerar para el cálculo de la cimentación (estudio geotécnico)." },
  { id: "2.2", cap: "2. Memoria constructiva", titulo: "Sistema estructural", basico: false,
    guia: "Cimentación, estructura portante y horizontal: datos y las hipótesis de partida, programa de necesidades, bases de cálculo, procedimientos o métodos de cálculo y características de los materiales." },
  { id: "2.3", cap: "2. Memoria constructiva", titulo: "Sistema envolvente", basico: false,
    guia: "Definición constructiva de los subsistemas de la envolvente (fachadas, cubiertas, suelos en contacto con terreno, medianeras, huecos), comportamiento frente a acciones, incendio, seguridad de uso, evacuación de agua, comportamiento frente a la humedad, aislamiento acústico y térmico, y sus bases de cálculo." },
  { id: "2.4", cap: "2. Memoria constructiva", titulo: "Sistema de compartimentación", basico: false,
    guia: "Definición de los elementos de compartimentación con especificación de su comportamiento ante el fuego y su aislamiento acústico, y otras características que sean exigibles." },
  { id: "2.5", cap: "2. Memoria constructiva", titulo: "Sistemas de acabados", basico: false,
    guia: "Relación y características de los acabados en relación con los requisitos de funcionalidad, seguridad y habitabilidad (resbaladicidad, reacción al fuego, etc.)." },
  { id: "2.6", cap: "2. Memoria constructiva", titulo: "Sistemas de acondicionamiento e instalaciones", basico: false,
    guia: "Datos de partida, objetivos, prestaciones y bases de cálculo de: protección contra incendios, anti-intrusión, pararrayos, electricidad, alumbrado, ascensores, transporte, fontanería, evacuación de residuos líquidos y sólidos, ventilación, telecomunicaciones, instalaciones térmicas, suministro de combustibles, ahorro de energía e incorporación de energía solar u otras renovables, recarga de vehículos eléctricos." },
  { id: "2.7", cap: "2. Memoria constructiva", titulo: "Equipamiento", basico: false,
    guia: "Definición de baños, cocinas y lavaderos, equipamiento industrial, etc." },
  { id: "3.1", cap: "3. Cumplimiento del CTE", titulo: "Seguridad Estructural (DB SE)", basico: false, db: "DB-SE",
    guia: "Justificación DB SE, SE-AE, SE-C y DB/normas del material (Código Estructural, SE-A, SE-F, SE-M) y NCSE-02: acciones, combinaciones, coeficientes, materiales, durabilidad, método de cálculo y programa." },
  { id: "3.2", cap: "3. Cumplimiento del CTE", titulo: "Seguridad en caso de Incendio (DB SI)", basico: true, db: "DB-SI",
    guia: "SI 1 Propagación interior (sectores, locales de riesgo especial, espacios ocultos, reacción al fuego); SI 2 Propagación exterior (medianeras, fachadas, cubiertas); SI 3 Evacuación de ocupantes (ocupación, número de salidas y longitud de recorridos, dimensionado, protección de escaleras, puertas, señalización, control de humo, evacuación de personas con discapacidad); SI 4 Instalaciones de protección; SI 5 Intervención de bomberos (aproximación, entorno, accesibilidad por fachada); SI 6 Resistencia al fuego de la estructura. Presentar en tablas exigencia / proyecto." },
  { id: "3.3", cap: "3. Cumplimiento del CTE", titulo: "Seguridad de Utilización y Accesibilidad (DB SUA)", basico: true, db: "DB-SUA",
    guia: "SUA 1 a SUA 9: resbaladicidad, discontinuidades, desniveles y barreras, escaleras y rampas, limpieza de acristalamientos; impacto y atrapamiento; aprisionamiento; alumbrado; alta ocupación; ahogamiento; vehículos en movimiento; rayo (cálculo de Ne/Na); accesibilidad (itinerarios, plazas, servicios higiénicos, alojamientos, dotación de elementos accesibles, señalización)." },
  { id: "3.4", cap: "3. Cumplimiento del CTE", titulo: "Salubridad (DB HS)", basico: false, db: "DB-HS",
    guia: "HS 1 Protección frente a la humedad (grados de impermeabilidad de muros, suelos, fachadas y cubiertas); HS 2 Recogida y evacuación de residuos; HS 3 Calidad del aire interior; HS 4 Suministro de agua; HS 5 Evacuación de aguas; HS 6 Protección frente a la exposición al radón." },
  { id: "3.5", cap: "3. Cumplimiento del CTE", titulo: "Protección frente al Ruido (DB HR)", basico: false, db: "DB-HR",
    guia: "Justificación mediante opción simplificada o general: tabiquería, elementos de separación verticales y horizontales, medianerías, fachadas y cubiertas (índice de ruido día Ld), ruido y vibraciones de instalaciones, tiempo de reverberación cuando proceda. Incluir fichas justificativas K.1 / K.2." },
  { id: "3.6", cap: "3. Cumplimiento del CTE", titulo: "Ahorro de Energía (DB HE)", basico: false, db: "DB-HE",
    guia: "HE 0 Limitación del consumo energético (Cep,nren y Cep,tot); HE 1 Condiciones para el control de la demanda (K, qsol;jul, n50, transmitancias, condensaciones); HE 2 Rendimiento de instalaciones térmicas (remite a RITE); HE 3 Instalaciones de iluminación (VEEI, potencia, control); HE 4 Contribución mínima de energía renovable para ACS; HE 5 Generación mínima de energía eléctrica; HE 6 Infraestructura de recarga de vehículos eléctricos. Zona climática y herramienta de cálculo." },
  { id: "4", cap: "4. Cumplimiento de otros reglamentos y disposiciones", titulo: "Otros reglamentos y disposiciones", basico: true,
    guia: "Justificación del cumplimiento de la normativa urbanística, habitabilidad, accesibilidad autonómica, RITE, REBT, ICT, RIPCI, ruido, residuos, usos específicos y cualquier otra normativa sectorial aplicable identificada." },
  { id: "A.RCD", cap: "Anejos a la memoria", titulo: "Estudio de gestión de residuos de construcción y demolición", basico: false,
    guia: "Contenido del art. 4 RD 105/2008: estimación de cantidades (códigos LER), medidas de prevención, operaciones de reutilización/valorización/eliminación, medidas de separación, planos de instalaciones, prescripciones del pliego, valoración del coste." },
  { id: "A.SYS", cap: "Anejos a la memoria", titulo: "Estudio (básico) de seguridad y salud", basico: false,
    guia: "Según art. 4-6 RD 1627/1997: identificación de riesgos laborales evitables y no evitables, medidas preventivas y protecciones técnicas, por fases de obra. Indicar si procede Estudio o Estudio Básico." },
  { id: "A.CC", cap: "Anejos a la memoria", titulo: "Plan de control de calidad", basico: false,
    guia: "Control de recepción de productos, control de ejecución y control de la obra terminada (CTE Parte I, art. 7), con ensayos y pruebas previstos y su valoración." },
  { id: "A.MANT", cap: "Anejos a la memoria", titulo: "Instrucciones de uso y mantenimiento", basico: false,
    guia: "Instrucciones de uso y mantenimiento del edificio terminado y sus instalaciones (Libro del Edificio)." },
];

export const AVISO_LEGAL =
  "Contenido generado como borrador de trabajo. Los umbrales y referencias normativas son orientativos: " +
  "verifique siempre la versión vigente (BOE, codigotecnico.org) y la normativa autonómica y municipal. " +
  "La responsabilidad del proyecto corresponde al técnico redactor que lo firma.";
