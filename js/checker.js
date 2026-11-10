// Revisión normativa preliminar: determina la normativa aplicable y realiza
// comprobaciones rápidas a partir de los datos del proyecto.
// Los umbrales son orientativos: verificar con el texto vigente.

import { CATALOGO, USOS } from "./normativa.js";

const num = (v) => {
  if (v === "" || v == null) return null;
  const n = Number(String(v).replace(",", "."));
  return Number.isFinite(n) ? n : null;
};

const fmt = (n, d = 0) =>
  n == null ? "—" : n.toLocaleString("es-ES", { maximumFractionDigits: d, minimumFractionDigits: 0 });

export function normalizar(p) {
  const q = { ...p };
  for (const k of ["supConstruida", "supUtil", "supParcela", "plantasSobre", "plantasBajo", "alturaEvacuacion",
    "alturaEvacuacionAsc", "numViviendas", "ocupacionManual", "desnivelMax", "ab", "pem", "duracionDias",
    "trabajadoresMax", "jornadas", "demandaACS", "personasVivienda", "plazasAparcamiento", "supAparcamiento"]) {
    q[k] = num(p[k]);
  }
  return q;
}

export function normativaAplicable(p) {
  return CATALOGO.map((n) => {
    const r = n.aplica(p);
    return { id: n.id, grupo: n.grupo, titulo: n.titulo, aplica: r !== false, matiz: typeof r === "string" ? r : "" };
  }).filter((n) => n.aplica);
}

export function calcularOcupacion(p) {
  if (p.ocupacionManual) return { total: p.ocupacionManual, metodo: "Ocupación indicada por el proyectista" };
  const uso = USOS[p.uso];
  if (!uso) return { total: null, metodo: "" };
  const util = p.supUtil ?? (p.supConstruida != null ? p.supConstruida * 0.8 : null);
  if (util == null) return { total: null, metodo: "Falta superficie" };
  const total = Math.ceil(util / uso.densidad);
  const est = p.supUtil == null ? " (sup. útil estimada = 0,80 × construida)" : "";
  return { total, metodo: `${fmt(util)} m² útiles / ${uso.densidad} m²/persona (DB SI 3, tabla 2.1)${est}` };
}

function item(lista, area, titulo, estado, detalle, ref) {
  lista.push({ area, titulo, estado, detalle, ref });
}

export function comprobaciones(pIn) {
  const p = normalizar(pIn);
  const out = [];
  const uso = USOS[p.uso];
  const grupo = uso?.grupo;
  const h = p.alturaEvacuacion;
  const plantas = p.plantasSobre ?? 1;
  const esUnifam = p.uso === "vivienda_unifamiliar";
  const obraNueva = ["nueva", "ampliacion"].includes(p.intervencion);
  const integral = ["nueva", "ampliacion", "reforma_integral", "cambio_uso"].includes(p.intervencion);

  if (!uso) {
    item(out, "General", "Uso del edificio", "incumple", "Seleccione el uso característico para poder evaluar la normativa.", "");
    return out;
  }
  if (p.intervencion === "urbanizacion") {
    item(out, "General", "Proyecto de urbanización", "info",
      "Las comprobaciones automáticas se centran en edificación. Revise Orden TMA/851/2021, ordenanzas municipales y normativa sectorial de servicios.", "");
    return out;
  }

  // --------- DB SI ---------
  const oc = calcularOcupacion(p);
  if (oc.total != null) {
    item(out, "DB SI", "Ocupación de cálculo", "info", `${fmt(oc.total)} personas. ${oc.metodo}.`, "DB SI 3, ap. 2");
  }

  // SI 1 Sectores
  if (p.supConstruida != null && !esUnifam && grupo !== "industrial") {
    const lim = { docente: 4000, hospitalario: 1500 }[grupo] ?? 2500;
    const porPlanta = p.supConstruida / Math.max(1, plantas + (p.plantasBajo ?? 0));
    const est = porPlanta > lim ? "aviso" : "ok";
    item(out, "DB SI", "Superficie máxima de sector de incendio", est,
      `Límite orientativo para uso ${uso.nombre}: ${fmt(lim)} m²${grupo === "hospitalario" ? " (plantas de hospitalización: al menos dos sectores ≤ 1.500 m²)" : ""}. ` +
      `Superficie media por planta: ${fmt(porPlanta)} m². ${est === "aviso" ? "Prever compartimentación en varios sectores o justificar excepción (p. ej. rociadores)." : "Cada planta puede constituir un sector si se compartimentan las plantas entre sí."}`,
      "DB SI 1, tabla 1.1");
  }
  if (p.supAparcamiento != null && p.supAparcamiento > 100 && p.uso !== "aparcamiento") {
    item(out, "DB SI", "Aparcamiento como sector independiente", "aviso",
      `Aparcamiento de ${fmt(p.supAparcamiento)} m² > 100 m²: debe constituir un sector de incendio diferenciado, con vestíbulo de independencia en las comunicaciones con el resto del edificio.`,
      "DB SI 1, tabla 1.1");
  }

  // SI 3 Salidas y recorridos
  if (oc.total != null && !esUnifam) {
    const ocPlanta = Math.ceil(oc.total / Math.max(1, plantas));
    const variasPorOcupacion = ocPlanta > 100;
    const variasPorAltura = h != null && h > 28;
    const varias = variasPorOcupacion || variasPorAltura;
    item(out, "DB SI", "Número de salidas de planta", varias ? "aviso" : "ok",
      varias
        ? `Se requieren al menos dos salidas de planta (${variasPorOcupacion ? `ocupación media por planta ${ocPlanta} > 100 personas` : ""}${variasPorOcupacion && variasPorAltura ? "; " : ""}${variasPorAltura ? `altura de evacuación ${fmt(h, 2)} m > 28 m` : ""}). Recorrido máximo hasta alguna salida: 50 m (35 m en zonas de hospitalización / 75 m con rociadores, según caso).`
        : `Ocupación media por planta ${ocPlanta} ≤ 100 personas: admisible una única salida de planta, con recorrido de evacuación ≤ 25 m (50 m si la salida da a espacio exterior seguro y la ocupación ≤ 25 personas).`,
      "DB SI 3, tabla 3.1");
  }

  // SI 3 Protección de escaleras (tabla 5.1)
  if (h != null && !esUnifam) {
    const lims = {
      vivienda: [14, 28], administrativo: [14, 28], docente: [14, 28],
      comercial: [10, 20], publica_concurrencia: [10, 20], residencial_publico: [10, 28],
    }[grupo];
    if (lims) {
      const tipo = h <= lims[0] ? "no protegida" : h <= lims[1] ? "protegida" : "especialmente protegida";
      item(out, "DB SI", "Protección de escaleras de evacuación descendente", tipo === "no protegida" ? "ok" : "aviso",
        `Altura de evacuación ${fmt(h, 2)} m → escalera ${tipo} (umbrales orientativos para ${uso.nombre}: no protegida ≤ ${lims[0]} m, protegida ≤ ${lims[1]} m).`,
        "DB SI 3, tabla 5.1 (verificar)");
    } else {
      item(out, "DB SI", "Protección de escaleras de evacuación", "info",
        `Consultar la tabla 5.1 para uso ${uso.nombre}.`, "DB SI 3, tabla 5.1");
    }
    if (p.plantasBajo) {
      item(out, "DB SI", "Escaleras de evacuación ascendente", "info",
        `Existen ${p.plantasBajo} planta(s) bajo rasante: comprobar protección según altura de evacuación ascendente (${p.alturaEvacuacionAsc != null ? fmt(p.alturaEvacuacionAsc, 2) + " m" : "indicar"}).`,
        "DB SI 3, tabla 5.1");
    }
  }

  // SI 4 Instalaciones
  if (h != null && !esUnifam) {
    item(out, "DB SI", "Columna seca", h > 24 ? "aviso" : "ok",
      h > 24 ? `Altura de evacuación ${fmt(h, 2)} m > 24 m: se requiere columna seca.` : "No exigible por altura (≤ 24 m).",
      "DB SI 4, tabla 1.1");
    item(out, "DB SI", "Ascensor de emergencia", h > 28 ? "aviso" : "ok",
      h > 28 ? `Altura de evacuación ${fmt(h, 2)} m > 28 m: se requiere ascensor de emergencia.` : "No exigible por altura (≤ 28 m).",
      "DB SI 4, tabla 1.1");
  }
  if (!esUnifam) {
    item(out, "DB SI", "Extintores portátiles", "info",
      "Extintores de eficacia 21A-113B a 15 m de recorrido en cada planta desde todo origen de evacuación, y en locales de riesgo especial. Revisar BIE, detección, alarma e hidrantes según uso y superficie.",
      "DB SI 4, tabla 1.1");
  }

  // SI 6 Resistencia al fuego de la estructura
  if (h != null || p.plantasBajo) {
    let r;
    if (esUnifam) r = "R 30";
    else if (["vivienda", "residencial_publico", "docente", "administrativo"].includes(grupo)) r = h == null ? "—" : h <= 15 ? "R 60" : h <= 28 ? "R 90" : "R 120";
    else if (["comercial", "publica_concurrencia", "hospitalario"].includes(grupo)) r = h == null ? "—" : h <= 15 ? "R 90" : h <= 28 ? "R 120" : "R 180";
    else if (grupo === "aparcamiento") r = "R 90 (edificio exclusivo) / R 120 (bajo otro uso)";
    if (r) {
      item(out, "DB SI", "Resistencia al fuego de la estructura principal", "info",
        `Plantas sobre rasante: ${r}.${p.plantasBajo ? " Plantas de sótano: R 120." : ""}`,
        "DB SI 6, tabla 3.1 (verificar)");
    }
  }

  // --------- DB SUA ---------
  const desnivel = p.desnivelMax ?? (plantas > 1 ? h : null);
  if (desnivel != null) {
    if (desnivel > 0.55) {
      item(out, "DB SUA", "Barreras de protección en desniveles", "aviso",
        `Desnivel máximo ${fmt(desnivel, 2)} m > 0,55 m: disponer barreras de protección de altura ≥ ${desnivel > 6 ? "1,10" : "0,90"} m, no escalables (zonas de uso público o residencial vivienda) y con aberturas que no permitan el paso de esfera de 10 cm.`,
        "DB SUA 1, ap. 3.2");
    } else {
      item(out, "DB SUA", "Barreras de protección en desniveles", "ok", "Desniveles ≤ 0,55 m: no se exigen barreras (sí diferenciación visual y táctil a partir de 25 cm en ciertos casos).", "DB SUA 1, ap. 3.1");
    }
  }
  if (!esUnifam) {
    const plantasSalvar = Math.max(0, plantas - 1) + (p.plantasBajo ?? 0);
    if (grupo === "vivienda") {
      const viv = p.numViviendas ?? 0;
      const vivSinEntrada = plantas > 1 ? Math.round((viv * (plantas - 1)) / plantas) : 0;
      const req = plantasSalvar > 2 || vivSinEntrada > 12;
      item(out, "DB SUA", "Ascensor accesible", req ? "aviso" : "ok",
        req
          ? `Se requiere ascensor accesible o rampa accesible (${plantasSalvar > 2 ? `más de dos plantas a salvar (${plantasSalvar})` : `≈ ${vivSinEntrada} viviendas en plantas sin entrada accesible > 12`}).`
          : `No exigible por SUA 9 (plantas a salvar: ${plantasSalvar}; viviendas sin entrada accesible ≈ ${vivSinEntrada}). Debe preverse la posibilidad de instalarlo si hay viviendas en plantas sin entrada accesible. Revise normativa autonómica, que puede ser más exigente.`,
        "DB SUA 9, ap. 1.1.2");
    } else {
      const req = plantasSalvar > 2 || (p.supUtil != null && plantas > 1 && (p.supUtil * (plantas - 1)) / plantas > 200);
      item(out, "DB SUA", "Ascensor accesible", req ? "aviso" : "ok",
        req ? "Se requiere ascensor accesible: más de dos plantas a salvar o más de 200 m² de superficie útil en plantas sin entrada accesible (excluidas zonas de ocupación nula)."
          : "No exigible por SUA 9 con los datos introducidos.",
        "DB SUA 9, ap. 1.1.2");
    }
  } else {
    item(out, "DB SUA", "Accesibilidad (SUA 9)", "info", "Las condiciones de accesibilidad no son exigibles en el interior de viviendas unifamiliares. Revise normativa autonómica.", "DB SUA 9, ap. 1");
  }
  if (Number(p.plazasAparcamiento) > 0) {
    item(out, "DB SUA", "Riesgo causado por vehículos en movimiento", "info",
      "Comprobar SUA 7 (accesos, itinerarios peatonales, protección de recorridos, señalización) y plazas accesibles según SUA 9.", "DB SUA 7 / SUA 9");
  }
  item(out, "DB SUA", "Protección frente al rayo", "info",
    "Calcular frecuencia esperada de impactos Ne y riesgo admisible Na; si Ne > Na se requiere sistema de protección (nivel de eficacia E).", "DB SUA 8");

  // --------- DB HS ---------
  const zr = p.zonaRadon;
  if (zr === "I" || zr === "II") {
    item(out, "DB HS", "Protección frente al radón", "aviso",
      zr === "I"
        ? "Municipio en zona I: barrera de protección frente al radón en contacto con el terreno (o alternativa: espacio de contención ventilado / despresurización)."
        : "Municipio en zona II: barrera de protección + espacio de contención ventilado o sistema de despresurización del terreno.",
      "DB HS 6, ap. 3");
  } else if (zr === "0") {
    item(out, "DB HS", "Protección frente al radón", "ok", "Municipio no incluido en el apéndice B del DB HS 6.", "DB HS 6, apéndice B");
  } else {
    item(out, "DB HS", "Protección frente al radón", "info", "Comprobar si el municipio figura en el apéndice B del DB HS 6 (zona I / II).", "DB HS 6, apéndice B");
  }
  item(out, "DB HS", "Grado de impermeabilidad", "info",
    "Determinar grado de impermeabilidad de muros y suelos (presencia de agua, Ks) y de fachadas (zona pluviométrica, altura, exposición al viento).", "DB HS 1");
  if (grupo === "vivienda") {
    item(out, "DB HS", "Almacén de residuos y espacio de reserva", "info",
      "Prever espacio de almacenamiento inmediato en cada vivienda y, en plurifamiliar, almacén de contenedores o espacio de reserva según sistema de recogida municipal.", "DB HS 2");
  }

  // --------- DB HE ---------
  if (integral) {
    item(out, "DB HE", "HE 0 / HE 1 Consumo energético y demanda", "aviso",
      `Justificar Cep,nren y Cep,tot límite (zona climática ${p.zonaClimatica || "[indicar]"}), coeficiente global de transmisión K, control solar qsol;jul y, en residencial, permeabilidad n50. Requiere herramienta reconocida (p. ej. HULC / CYPETHERM).`,
      "DB HE 0 y HE 1");
  } else {
    item(out, "DB HE", "HE 1 en intervenciones en edificios existentes", "info",
      "Los elementos de la envolvente que se sustituyan, incorporen o modifiquen deben cumplir los valores límite de transmitancia de la tabla 3.1.1.a (anejo E orientativo).", "DB HE 1");
  }
  if (integral && grupo === "vivienda") {
    const personas = p.personasVivienda ?? 3;
    const demanda = p.demandaACS ?? (p.numViviendas ?? (esUnifam ? 1 : 0)) * personas * 28;
    const supera = demanda > 100;
    item(out, "DB HE", "HE 4 Contribución renovable para ACS", supera ? "aviso" : "ok",
      `Demanda de ACS ${p.demandaACS != null ? "" : "estimada "}${fmt(demanda)} l/día${p.demandaACS != null ? "" : ` (${personas} pers./vivienda × 28 l/pers·día; ajustar ocupación según anejo F)`}. ` +
      (supera ? `> 100 l/día: cubrir mediante renovables o calor residual al menos el ${demanda > 5000 ? "70" : "60"} % de la demanda de ACS (incluida piscina si existe).` : "≤ 100 l/día: HE 4 no es de aplicación."),
      "DB HE 4");
  } else if (integral) {
    const d = p.demandaACS;
    item(out, "DB HE", "HE 4 Contribución renovable para ACS", d != null && d > 100 ? "aviso" : "info",
      d != null ? `Demanda de ACS ${fmt(d)} l/día: ${d > 100 ? `contribución renovable mínima ${d > 5000 ? "70" : "60"} %` : "no aplica"}.` : "Indicar la demanda de ACS (l/día) para comprobar si supera 100 l/día.",
      "DB HE 4");
  }
  if (obraNueva && p.supConstruida != null) {
    const aplica = p.supConstruida > 1000;
    item(out, "DB HE", "HE 5 Generación mínima de energía eléctrica", aplica ? "aviso" : "ok",
      aplica ? `Superficie construida ${fmt(p.supConstruida)} m² > 1.000 m²: prever generación eléctrica in situ (potencia mínima según HE 5). Verificar exclusiones por uso en la versión vigente.`
        : `Superficie construida ${fmt(p.supConstruida)} m² ≤ 1.000 m²: no exigible.`,
      "DB HE 5");
  }
  if (Number(p.plazasAparcamiento) > 0 && integral) {
    const plazas = Number(p.plazasAparcamiento);
    const aplica = plazas > 10 || p.uso === "aparcamiento";
    item(out, "DB HE", "HE 6 Infraestructura de recarga de vehículos eléctricos", aplica ? "aviso" : "info",
      aplica
        ? (grupo === "vivienda"
          ? `${plazas} plazas en residencial privado: preinstalación (sistema de conducción de cables) en el 100 % de las plazas.`
          : `${plazas} plazas en uso distinto de residencial privado: preinstalación en ≥ 20 % de las plazas y estaciones de recarga (1 por cada 40 plazas, o por cada 20 en edificios de la Administración). Verificar valores vigentes.`)
        : "Aparcamiento de 10 plazas o menos: comprobar ámbito de aplicación de HE 6.",
      "DB HE 6 / ITC-BT-52");
  }
  if (grupo !== "vivienda") {
    item(out, "DB HE", "HE 3 Instalaciones de iluminación", "info", "Justificar VEEI límite por zona, potencia instalada máxima y sistemas de control y regulación.", "DB HE 3");
  }

  // --------- Estructuras ---------
  if (p.ab != null) {
    const ab = p.ab;
    item(out, "Estructuras", "Norma sismorresistente NCSE-02", ab < 0.04 ? "ok" : "aviso",
      ab < 0.04 ? `ab = ${fmt(ab, 3)} g < 0,04 g: no es obligatoria su aplicación.`
        : ab < 0.08 ? `ab = ${fmt(ab, 3)} g: aplicable salvo construcciones de importancia normal con pórticos bien arriostrados (en edificios de más de siete plantas, aplicable si ac ≥ 0,08 g).`
        : `ab = ${fmt(ab, 3)} g ≥ 0,08 g: aplicación obligatoria; calcular ac y aplicar reglas de diseño y prescripciones constructivas.`,
      "NCSE-02, art. 1.2.3");
  }
  if (["nueva", "ampliacion"].includes(p.intervencion)) {
    item(out, "Estructuras", "Estudio geotécnico", "aviso",
      "Obligatorio. Definir tipo de construcción (C-0 a C-4) y grupo de terreno (T-1 a T-3) para fijar el número mínimo de puntos de reconocimiento.",
      "DB SE-C, ap. 3.2");
  }

  // --------- Seguridad y salud ---------
  const motivosES = [];
  if (p.pem != null && p.pem >= 450759.08) motivosES.push(`PEM ${fmt(p.pem, 2)} € ≥ 450.759,08 €`);
  if (p.duracionDias != null && p.trabajadoresMax != null && p.duracionDias > 30 && p.trabajadoresMax > 20)
    motivosES.push("duración > 30 días laborables con más de 20 trabajadores simultáneos");
  if (p.jornadas != null && p.jornadas > 500) motivosES.push("volumen de mano de obra > 500 jornadas");
  if (/t[uú]nel|galer[ií]a|presa|conducci[oó]n subterr/i.test(p.descripcion || "")) motivosES.push("obra de túneles, galerías, conducciones subterráneas o presas");
  item(out, "Seguridad y salud", "Estudio de Seguridad y Salud", motivosES.length ? "aviso" : "info",
    motivosES.length ? `Se requiere Estudio de Seguridad y Salud (${motivosES.join("; ")}).`
      : (p.pem == null ? "Indicar PEM, duración y trabajadores para determinarlo. " : "") + "Con los datos introducidos basta un Estudio Básico de Seguridad y Salud.",
    "RD 1627/1997, art. 4");

  item(out, "Residuos", "Estudio de gestión de RCD", p.fase === "basico" ? "info" : "aviso",
    "El proyecto de ejecución debe incluir el estudio de gestión de residuos de construcción y demolición.", "RD 105/2008, art. 4");

  // --------- Datos pendientes ---------
  const faltan = [];
  if (!p.municipio) faltan.push("municipio");
  if (p.supConstruida == null) faltan.push("superficie construida");
  if (h == null && !esUnifam) faltan.push("altura de evacuación");
  if (!p.zonaClimatica) faltan.push("zona climática");
  if (p.ab == null) faltan.push("aceleración sísmica ab");
  if (p.pem == null) faltan.push("PEM");
  if (faltan.length) item(out, "General", "Datos pendientes", "aviso", `Completar: ${faltan.join(", ")}.`, "");

  return out;
}

export function resumenTexto(p) {
  const n = normativaAplicable(normalizar(p));
  const c = comprobaciones(p);
  const lineas = ["NORMATIVA APLICABLE (preliminar):"];
  for (const x of n) lineas.push(`- [${x.grupo}] ${x.titulo}${x.matiz ? ` — ${x.matiz}` : ""}`);
  lineas.push("", "COMPROBACIONES PRELIMINARES:");
  for (const x of c) lineas.push(`- (${x.estado.toUpperCase()}) ${x.area} · ${x.titulo}: ${x.detalle}${x.ref ? ` [${x.ref}]` : ""}`);
  return lineas.join("\n");
}
