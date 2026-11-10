import { USOS, INTERVENCIONES, ESTRUCTURAS, FASES, ESTRUCTURA_MEMORIA, AVISO_LEGAL } from "./normativa.js";
import { comprobaciones, normativaAplicable, normalizar, resumenTexto } from "./checker.js";
import { SYSTEM_REDACTOR, SYSTEM_CONSULTOR, bloqueProyecto, peticionApartado } from "./prompts.js";
import { generar, describirError } from "./claude.js";

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const CLAVE_ESTADO = "memoria-proyecto:estado";
const CLAVE_API = "memoria-proyecto:apikey";

// ---------------- Almacenamiento seguro ----------------
const almacen = {
  leer(k) { try { return localStorage.getItem(k); } catch { return null; } },
  escribir(k, v) { try { localStorage.setItem(k, v); } catch { /* sin almacenamiento */ } },
  borrar(k) { try { localStorage.removeItem(k); } catch { /* sin almacenamiento */ } },
};

let apiKeySesion = almacen.leer(CLAVE_API) || "";

// ---------------- Definición del formulario ----------------
const opciones = (obj) => Object.entries(obj).map(([v, t]) => [v, typeof t === "string" ? t : t.nombre]);

const FORM = [
  { leyenda: "Identificación", campos: [
    { id: "nombre", et: "Denominación del proyecto", ancho: true, ph: "Edificio de 12 viviendas, garaje y trasteros" },
    { id: "fase", et: "Fase", tipo: "select", ops: opciones(FASES) },
    { id: "promotor", et: "Promotor" },
    { id: "arquitecto", et: "Arquitecto/a redactor/a" },
    { id: "colegiado", et: "Colegio y nº de colegiado" },
    { id: "otrosTecnicos", et: "Otros técnicos (estructura, instalaciones, CSS)", ancho: true },
  ]},
  { leyenda: "Emplazamiento", campos: [
    { id: "direccion", et: "Dirección / parcela" },
    { id: "municipio", et: "Municipio" },
    { id: "provincia", et: "Provincia" },
    { id: "ccaa", et: "Comunidad autónoma" },
    { id: "refCatastral", et: "Referencia catastral" },
    { id: "planeamiento", et: "Planeamiento y calificación", ph: "PGOU 2010 · Residencial intensiva R2" },
    { id: "parametrosUrb", et: "Parámetros urbanísticos (edificabilidad, ocupación, alturas, retranqueos…)", tipo: "area", ancho: true },
    { id: "zonaClimatica", et: "Zona climática (DB HE)", ph: "D3", pista: "Anejo B DB HE" },
    { id: "ab", et: "Aceleración sísmica básica ab (g)", tipo: "number", paso: "0.01", pista: "Anejo 1 NCSE-02" },
    { id: "zonaRadon", et: "Zona de radón (DB HS 6)", tipo: "select", ops: [["", "Sin comprobar"], ["0", "No incluido"], ["I", "Zona I"], ["II", "Zona II"]] },
    { id: "supParcela", et: "Superficie de parcela (m²)", tipo: "number" },
  ]},
  { leyenda: "Intervención y uso", campos: [
    { id: "intervencion", et: "Tipo de intervención", tipo: "select", ops: opciones(INTERVENCIONES) },
    { id: "uso", et: "Uso característico", tipo: "select", ops: opciones(USOS) },
    { id: "otrosUsos", et: "Otros usos (garaje, local comercial, trasteros…)" },
    { id: "programa", et: "Programa de necesidades", tipo: "area", ancho: true, ph: "12 viviendas de 2 y 3 dormitorios, local en PB, garaje de 14 plazas en sótano, trasteros…" },
    { id: "descripcion", et: "Descripción general / antecedentes / condicionantes", tipo: "area", ancho: true },
  ]},
  { leyenda: "Dimensiones", campos: [
    { id: "supConstruida", et: "Superficie construida total (m²)", tipo: "number" },
    { id: "supUtil", et: "Superficie útil total (m²)", tipo: "number" },
    { id: "plantasSobre", et: "Plantas sobre rasante", tipo: "number" },
    { id: "plantasBajo", et: "Plantas bajo rasante", tipo: "number" },
    { id: "alturaEvacuacion", et: "Altura de evacuación descendente (m)", tipo: "number", paso: "0.01", pista: "Cota última planta habitable − cota salida" },
    { id: "alturaEvacuacionAsc", et: "Altura de evacuación ascendente (m)", tipo: "number", paso: "0.01" },
    { id: "desnivelMax", et: "Desnivel máximo a proteger (m)", tipo: "number", paso: "0.01", pista: "Balcones, terrazas, huecos" },
    { id: "numViviendas", et: "Nº de viviendas", tipo: "number" },
    { id: "personasVivienda", et: "Ocupantes por vivienda (ACS)", tipo: "number", pista: "Por defecto 3" },
    { id: "ocupacionManual", et: "Ocupación de cálculo (personas)", tipo: "number", pista: "Vacío = cálculo automático" },
    { id: "plazasAparcamiento", et: "Plazas de aparcamiento", tipo: "number" },
    { id: "supAparcamiento", et: "Superficie de aparcamiento (m²)", tipo: "number" },
    { id: "cuadroSuperficies", et: "Cuadro de superficies por planta / dependencia", tipo: "area", ancho: true },
  ]},
  { leyenda: "Sistemas constructivos e instalaciones", campos: [
    { id: "estructura", et: "Sistema estructural", tipo: "select", ops: opciones(ESTRUCTURAS) },
    { id: "cimentacion", et: "Cimentación y terreno", ph: "Losa / zapatas; datos del estudio geotécnico" },
    { id: "envolvente", et: "Envolvente (fachadas, cubiertas, carpinterías)", tipo: "area", ancho: true },
    { id: "compartimentacion", et: "Compartimentación y acabados", tipo: "area", ancho: true },
    { id: "instalaciones", et: "Instalaciones (climatización, ACS, ventilación, renovables, gas…)", tipo: "area", ancho: true },
    { id: "demandaACS", et: "Demanda de ACS (l/día)", tipo: "number", pista: "Vacío = estimación" },
  ]},
  { leyenda: "Obra", campos: [
    { id: "pem", et: "Presupuesto de ejecución material (€)", tipo: "number" },
    { id: "duracionDias", et: "Duración (días laborables)", tipo: "number" },
    { id: "trabajadoresMax", et: "Trabajadores simultáneos (máx.)", tipo: "number" },
    { id: "jornadas", et: "Volumen de mano de obra (jornadas)", tipo: "number" },
    { id: "notas", et: "Otras notas para la redacción", tipo: "area", ancho: true },
  ]},
];

// ---------------- Estado ----------------
function estadoInicial() {
  return {
    proyecto: { fase: "basico_ejecucion", intervencion: "nueva", uso: "vivienda_plurifamiliar", estructura: "hormigon" },
    memoria: {},   // id -> { texto, notas, fuentes }
    seleccion: ESTRUCTURA_MEMORIA.map((a) => a.id),
    chat: [],
  };
}
let estado = cargarEstado();

function cargarEstado() {
  try {
    const s = JSON.parse(almacen.leer(CLAVE_ESTADO) || "null");
    if (s && s.proyecto) return { ...estadoInicial(), ...s };
  } catch { /* estado corrupto */ }
  return estadoInicial();
}
let tGuardar;
function guardar() {
  clearTimeout(tGuardar);
  tGuardar = setTimeout(() => almacen.escribir(CLAVE_ESTADO, JSON.stringify(estado)), 300);
}

// ---------------- Utilidades ----------------
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.add("visible");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove("visible"), 3500);
}
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function renderMd(md) {
  const html = window.marked ? window.marked.parse(md || "") : `<pre>${esc(md)}</pre>`;
  const limpio = window.DOMPurify ? window.DOMPurify.sanitize(html) : esc(md);
  return limpio.replace(/\[(COMPLETAR|VERIFICAR|REVISAR)([^\]]*)\]/g, '<mark class="marcador">[$1$2]</mark>');
}
function descargar(nombre, contenido, tipo) {
  const url = URL.createObjectURL(new Blob([contenido], { type: tipo }));
  const a = Object.assign(document.createElement("a"), { href: url, download: nombre });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function slug() {
  return (estado.proyecto.nombre || "proyecto").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "proyecto";
}
function obtenerApiKey() {
  if (apiKeySesion) return apiKeySesion;
  abrirAjustes();
  toast("Introduzca su clave de API de Anthropic para generar contenido.");
  return null;
}

// ---------------- Pestañas ----------------
function mostrarPestana(id) {
  for (const b of $$(".pestanas button")) b.setAttribute("aria-selected", String(b.dataset.tab === id));
  for (const p of $$(".panel")) p.hidden = p.id !== `tab-${id}`;
  if (id === "revision") pintarRevision();
  if (id === "memoria") pintarMemoria();
  if (id === "consulta") pintarChat();
}

// ---------------- Formulario ----------------
function pintarFormulario() {
  const f = $("#form-proyecto");
  f.innerHTML = FORM.map((g) => `
    <fieldset><legend>${g.leyenda}</legend><div class="rejilla">
      ${g.campos.map((c) => {
        const v = estado.proyecto[c.id] ?? "";
        let ctl;
        if (c.tipo === "select") ctl = `<select name="${c.id}">${c.ops.map(([ov, ot]) => `<option value="${ov}"${String(v) === ov ? " selected" : ""}>${esc(ot)}</option>`).join("")}</select>`;
        else if (c.tipo === "area") ctl = `<textarea name="${c.id}" rows="3" placeholder="${esc(c.ph || "")}">${esc(v)}</textarea>`;
        else ctl = `<input name="${c.id}" ${c.tipo === "number" ? `type="number" inputmode="decimal" step="${c.paso || "any"}" min="0"` : 'type="text"'} value="${esc(v)}" placeholder="${esc(c.ph || "")}">`;
        return `<label class="${c.ancho ? "ancho" : ""}">${esc(c.et)}${ctl}${c.pista ? `<span class="pista">${esc(c.pista)}</span>` : ""}</label>`;
      }).join("")}
    </div></fieldset>`).join("");
}

// ---------------- Revisión ----------------
function pintarRevision() {
  const lista = comprobaciones(estado.proyecto);
  const cuenta = { incumple: 0, aviso: 0, ok: 0, info: 0 };
  for (const c of lista) cuenta[c.estado]++;
  const etiquetas = { incumple: "Bloqueantes", aviso: "Requieren atención", ok: "Cumplen", info: "Informativas" };
  $("#resumen-revision").innerHTML = Object.entries(cuenta).filter(([, n]) => n)
    .map(([k, n]) => `<span class="chip ${k}">${n} ${etiquetas[k]}</span>`).join("");
  const nombreEstado = { ok: "OK", aviso: "Atención", incumple: "Falta", info: "Info" };
  $("#lista-comprobaciones").innerHTML = lista.map((c) => `
    <div class="comprobacion">
      <span class="estado ${c.estado}">${nombreEstado[c.estado]}</span>
      <div class="tit">${esc(c.titulo)} <span class="area">· ${esc(c.area)}</span> ${c.ref ? `<span class="ref">— ${esc(c.ref)}</span>` : ""}</div>
      <div class="det">${esc(c.detalle)}</div>
    </div>`).join("");

  const norm = normativaAplicable(normalizar(estado.proyecto));
  const grupos = {};
  for (const n of norm) (grupos[n.grupo] ||= []).push(n);
  $("#lista-normativa").innerHTML = Object.entries(grupos).map(([g, ns]) => `
    <div class="grupo-normativa"><h4>${esc(g)}</h4><ul>
      ${ns.map((n) => `<li>${esc(n.titulo)}${n.matiz ? ` <span class="matiz">— ${esc(n.matiz)}</span>` : ""}</li>`).join("")}
    </ul></div>`).join("");
}

// ---------------- Memoria ----------------
let controlador = null;

function pintarMemoria() {
  const cont = $("#lista-apartados");
  let capActual = "";
  let html = "";
  for (const a of ESTRUCTURA_MEMORIA) {
    if (a.cap !== capActual) { capActual = a.cap; html += `<h3 class="capitulo">${esc(a.cap)}</h3>`; }
    const m = estado.memoria[a.id] || {};
    const sel = estado.seleccion.includes(a.id);
    html += `
      <article class="apartado${m.texto ? "" : " sin-texto"}" data-id="${a.id}">
        <header>
          <input type="checkbox" class="sel" ${sel ? "checked" : ""} aria-label="Seleccionar ${esc(a.titulo)}">
          <span class="nombre">${a.id} ${esc(a.titulo)} ${a.basico ? "<small>· básico</small>" : ""}</span>
          <span class="estado-gen"></span>
          <button type="button" class="sec mini" data-acc="notas">Indicaciones</button>
          <button type="button" class="sec mini" data-acc="editar" ${m.texto ? "" : "hidden"}>Editar</button>
          <button type="button" class="mini" data-acc="generar">${m.texto ? "Regenerar" : "Generar"}</button>
        </header>
        <div class="cuerpo">
          <div class="notas" ${m.notas ? "" : "hidden"}>
            <label>Indicaciones para este apartado
              <textarea rows="2" class="txt-notas" placeholder="Ej.: justificar por opción simplificada; fachada ventilada con aislamiento de lana mineral 10 cm…">${esc(m.notas || "")}</textarea>
            </label>
          </div>
          <div class="md">${m.texto ? renderMd(m.texto) : `<p class="vacio">${esc(a.guia)}</p>`}</div>
          ${m.fuentes?.length ? `<p class="fuentes">Fuentes consultadas: ${m.fuentes.map((f) => `<a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.title)}</a>`).join(" · ")}</p>` : ""}
        </div>
      </article>`;
  }
  cont.innerHTML = html;
}

function apartadoEl(id) { return $(`.apartado[data-id="${CSS.escape(id)}"]`); }

async function generarApartado(id, signal) {
  const apiKey = obtenerApiKey();
  if (!apiKey) return false;
  const a = ESTRUCTURA_MEMORIA.find((x) => x.id === id);
  const el = apartadoEl(id);
  const md = $(".md", el);
  const est = $(".estado-gen", el);
  const m = (estado.memoria[id] ||= {});
  const previos = ESTRUCTURA_MEMORIA.filter((x) => x.id !== id && estado.memoria[x.id]?.texto).map((x) => `${x.id} ${x.titulo}`);

  el.classList.add("generando");
  el.classList.remove("sin-texto");
  est.textContent = "Redactando…";
  md.innerHTML = "";
  let acumulado = "";
  let pendiente = false;
  const pintar = () => { pendiente = false; md.innerHTML = renderMd(acumulado); };
  try {
    const { texto, fuentes } = await generar({
      apiKey,
      system: SYSTEM_REDACTOR,
      contexto: bloqueProyecto(estado.proyecto, resumenTexto(estado.proyecto)),
      mensajes: [{ role: "user", content: peticionApartado(a, m.notas, previos) }],
      busqueda: $("#chk-busqueda").checked,
      esfuerzo: $("#sel-esfuerzo").value,
      signal,
      onTexto: (t) => {
        acumulado += t;
        if (!pendiente) { pendiente = true; requestAnimationFrame(pintar); }
      },
    });
    m.texto = texto.trim();
    m.fuentes = fuentes;
    guardar();
    return true;
  } catch (e) {
    toast(describirError(e));
    return false;
  } finally {
    el.classList.remove("generando");
    pintarMemoria();
  }
}

async function generarSeleccionados() {
  const ids = ESTRUCTURA_MEMORIA.map((a) => a.id).filter((id) => estado.seleccion.includes(id));
  if (!ids.length) return toast("Seleccione al menos un apartado.");
  if (!obtenerApiKey()) return;
  controlador = new AbortController();
  $("#btn-generar-sel").disabled = true;
  $("#btn-cancelar").hidden = false;
  try {
    for (const id of ids) {
      if (controlador.signal.aborted) break;
      apartadoEl(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
      const ok = await generarApartado(id, controlador.signal);
      if (!ok) break;
    }
  } finally {
    controlador = null;
    $("#btn-generar-sel").disabled = false;
    $("#btn-cancelar").hidden = true;
  }
}

function memoriaMarkdown() {
  const p = estado.proyecto;
  const partes = [
    `# ${p.nombre || "[COMPLETAR: denominación del proyecto]"}`,
    `**${FASES[p.fase] || ""}** · ${[p.direccion, p.municipio, p.provincia].filter(Boolean).join(", ")}`,
    p.promotor ? `Promotor: ${p.promotor}` : "",
    p.arquitecto ? `Arquitecto/a: ${p.arquitecto}${p.colegiado ? ` (${p.colegiado})` : ""}` : "",
    "",
  ];
  let cap = "";
  for (const a of ESTRUCTURA_MEMORIA) {
    const t = estado.memoria[a.id]?.texto;
    if (!t) continue;
    if (a.cap !== cap) { cap = a.cap; partes.push(`\n# ${cap}\n`); }
    partes.push(t, "");
  }
  return partes.filter((x) => x !== null).join("\n");
}

function exportarWord() {
  const html = window.DOMPurify.sanitize(window.marked.parse(memoriaMarkdown()));
  const doc = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${esc(estado.proyecto.nombre || "Memoria")}</title>
<style>body{font-family:Arial,sans-serif;font-size:10.5pt;line-height:1.4}h1{font-size:15pt}h2{font-size:12.5pt}h3{font-size:11pt}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;padding:3pt 5pt;vertical-align:top}th{background:#eee}</style></head><body>${html}</body></html>`;
  descargar(`memoria-${slug()}.doc`, doc, "application/msword");
}

// ---------------- Consulta ----------------
function pintarChat() {
  $("#chat").innerHTML = estado.chat.map((m) =>
    `<div class="msg ${m.role === "user" ? "usuario" : "asistente"}">${m.role === "user" ? esc(m.content).replace(/\n/g, "<br>") : `<div class="md">${renderMd(m.content)}</div>`}</div>`).join("");
}

async function consultar(e) {
  e.preventDefault();
  const pregunta = $("#txt-consulta").value.trim();
  if (!pregunta) return;
  const apiKey = obtenerApiKey();
  if (!apiKey) return;
  const historial = [...estado.chat, { role: "user", content: pregunta }];
  estado.chat = historial;
  $("#txt-consulta").value = "";
  pintarChat();
  const burbuja = document.createElement("div");
  burbuja.className = "msg asistente";
  burbuja.innerHTML = '<div class="md"><p class="vacio">Consultando…</p></div>';
  $("#chat").append(burbuja);
  $("#btn-consultar").disabled = true;
  let acumulado = "";
  try {
    const { texto, fuentes } = await generar({
      apiKey,
      system: SYSTEM_CONSULTOR,
      contexto: bloqueProyecto(estado.proyecto, resumenTexto(estado.proyecto)),
      mensajes: historial.map((m) => ({ role: m.role, content: m.content })),
      busqueda: $("#chk-busqueda-consulta").checked,
      esfuerzo: "high",
      onTexto: (t) => { acumulado += t; $(".md", burbuja).innerHTML = renderMd(acumulado); },
    });
    const conFuentes = fuentes.length ? `${texto}\n\n**Fuentes:** ${fuentes.map((f) => `[${f.title}](${f.url})`).join(" · ")}` : texto;
    estado.chat.push({ role: "assistant", content: conFuentes });
    guardar();
  } catch (err) {
    estado.chat.pop();
    toast(describirError(err));
  } finally {
    $("#btn-consultar").disabled = false;
    pintarChat();
  }
}

// ---------------- Ajustes ----------------
function abrirAjustes() {
  $("#inp-apikey").value = apiKeySesion;
  $("#dlg-ajustes").showModal();
}

// ---------------- Eventos ----------------
function iniciar() {
  for (const el of $$("[data-aviso]")) el.textContent = AVISO_LEGAL;
  pintarFormulario();
  $("#form-proyecto").addEventListener("input", (e) => {
    if (!e.target.name) return;
    estado.proyecto[e.target.name] = e.target.value;
    guardar();
  });

  for (const b of $$(".pestanas button")) b.addEventListener("click", () => mostrarPestana(b.dataset.tab));
  $("#btn-ir-revision").addEventListener("click", () => mostrarPestana("revision"));
  $("#btn-ajustes").addEventListener("click", abrirAjustes);
  $("#btn-guardar-ajustes").addEventListener("click", () => {
    apiKeySesion = $("#inp-apikey").value.trim();
    if ($("#chk-recordar").checked && apiKeySesion) almacen.escribir(CLAVE_API, apiKeySesion);
    else almacen.borrar(CLAVE_API);
    toast(apiKeySesion ? "Clave guardada." : "Clave eliminada.");
  });

  $("#btn-nuevo").addEventListener("click", () => {
    if (!confirm("¿Empezar un proyecto nuevo? Se perderán los datos no guardados en archivo.")) return;
    estado = estadoInicial();
    guardar();
    pintarFormulario();
    mostrarPestana("proyecto");
  });
  $("#btn-exportar-json").addEventListener("click", () =>
    descargar(`${slug()}.json`, JSON.stringify(estado, null, 2), "application/json"));
  $("#inp-importar").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    try {
      const s = JSON.parse(await f.text());
      if (!s.proyecto) throw new Error("formato");
      estado = { ...estadoInicial(), ...s };
      guardar();
      pintarFormulario();
      mostrarPestana("proyecto");
      toast("Proyecto cargado.");
    } catch {
      toast("El archivo no es un proyecto válido.");
    }
    e.target.value = "";
  });

  $("#btn-copiar-revision").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(resumenTexto(estado.proyecto)); toast("Informe copiado."); }
    catch { toast("No se pudo copiar al portapapeles."); }
  });

  // Memoria
  $("#btn-generar-sel").addEventListener("click", generarSeleccionados);
  $("#btn-cancelar").addEventListener("click", () => controlador?.abort());
  $$("[data-sel]").forEach((b) => b.addEventListener("click", () => {
    const modo = b.dataset.sel;
    estado.seleccion = ESTRUCTURA_MEMORIA.filter((a) => modo === "todo" || (modo === "basico" && a.basico)).map((a) => a.id);
    guardar();
    pintarMemoria();
  }));
  $("#lista-apartados").addEventListener("change", (e) => {
    const art = e.target.closest(".apartado");
    if (!art) return;
    const id = art.dataset.id;
    if (e.target.classList.contains("sel")) {
      estado.seleccion = e.target.checked ? [...new Set([...estado.seleccion, id])] : estado.seleccion.filter((x) => x !== id);
      guardar();
    }
  });
  $("#lista-apartados").addEventListener("input", (e) => {
    const art = e.target.closest(".apartado");
    if (!art) return;
    const m = (estado.memoria[art.dataset.id] ||= {});
    if (e.target.classList.contains("txt-notas")) m.notas = e.target.value;
    if (e.target.classList.contains("editor")) m.texto = e.target.value;
    guardar();
  });
  $("#lista-apartados").addEventListener("click", async (e) => {
    const b = e.target.closest("button[data-acc]");
    if (!b) return;
    const art = b.closest(".apartado");
    const id = art.dataset.id;
    if (b.dataset.acc === "notas") {
      const n = $(".notas", art);
      n.hidden = !n.hidden;
      if (!n.hidden) $("textarea", n).focus();
    } else if (b.dataset.acc === "editar") {
      const md = $(".md", art);
      if (b.textContent === "Editar") {
        md.innerHTML = `<textarea class="editor">${esc(estado.memoria[id]?.texto || "")}</textarea>`;
        b.textContent = "Ver";
      } else {
        pintarMemoria();
      }
    } else if (b.dataset.acc === "generar") {
      if (controlador) return toast("Ya hay una generación en curso.");
      controlador = new AbortController();
      $("#btn-cancelar").hidden = false;
      try { await generarApartado(id, controlador.signal); }
      finally { controlador = null; $("#btn-cancelar").hidden = true; }
    }
  });
  $("#btn-md").addEventListener("click", () => descargar(`memoria-${slug()}.md`, memoriaMarkdown(), "text/markdown"));
  $("#btn-doc").addEventListener("click", exportarWord);
  $("#btn-imprimir").addEventListener("click", () => { mostrarPestana("memoria"); window.print(); });

  // Consulta
  $("#form-consulta").addEventListener("submit", consultar);
  $("#txt-consulta").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) $("#form-consulta").requestSubmit();
  });
}

iniciar();
