// Pruebas de la revisión normativa: npm test
import { test } from "node:test";
import assert from "node:assert/strict";
import { comprobaciones, normativaAplicable, normalizar, calcularOcupacion } from "../js/checker.js";

const base = {
  uso: "vivienda_plurifamiliar", intervencion: "nueva", estructura: "hormigon", fase: "basico_ejecucion",
  supConstruida: "1800", supUtil: "1450", plantasSobre: "6", plantasBajo: "1", alturaEvacuacion: "15.5",
  numViviendas: "20", ab: "0.05", zonaRadon: "I", pem: "1500000", plazasAparcamiento: "22", supAparcamiento: "650",
  municipio: "Madrid", zonaClimatica: "D3",
};
const buscar = (lista, t) => lista.find((c) => c.titulo.includes(t));

test("ocupación vivienda 20 m²/persona", () => {
  assert.equal(calcularOcupacion(normalizar(base)).total, Math.ceil(1450 / 20));
});

test("plurifamiliar 6 plantas: escalera protegida, ascensor, sin columna seca", () => {
  const c = comprobaciones(base);
  assert.match(buscar(c, "Protección de escaleras").detalle, /escalera protegida/);
  assert.equal(buscar(c, "Ascensor accesible").estado, "aviso");
  assert.equal(buscar(c, "Columna seca").estado, "ok");
  assert.equal(buscar(c, "Ascensor de emergencia").estado, "ok");
  assert.match(buscar(c, "Resistencia al fuego").detalle, /R 90/);
  assert.match(buscar(c, "Barreras").detalle, /1,10/);
});

test("altura > 28 m exige columna seca, ascensor de emergencia y escalera especialmente protegida", () => {
  const c = comprobaciones({ ...base, alturaEvacuacion: "30", plantasSobre: "11" });
  assert.equal(buscar(c, "Columna seca").estado, "aviso");
  assert.equal(buscar(c, "Ascensor de emergencia").estado, "aviso");
  assert.match(buscar(c, "Protección de escaleras").detalle, /especialmente protegida/);
  assert.equal(buscar(c, "Número de salidas").estado, "aviso");
});

test("estudio de seguridad y salud por PEM", () => {
  assert.equal(buscar(comprobaciones(base), "Estudio de Seguridad").estado, "aviso");
  assert.equal(buscar(comprobaciones({ ...base, pem: "200000" }), "Estudio de Seguridad").estado, "info");
});

test("HE 4, HE 5, HE 6 y radón", () => {
  const c = comprobaciones(base);
  assert.equal(buscar(c, "HE 4").estado, "aviso");
  assert.equal(buscar(c, "HE 5").estado, "aviso");
  assert.match(buscar(c, "HE 6").detalle, /100 %/);
  assert.equal(buscar(c, "radón").estado, "aviso");
  assert.equal(buscar(c, "Aparcamiento como sector").estado, "aviso");
});

test("unifamiliar pequeña: sin SUA 9 ni HE 5", () => {
  const c = comprobaciones({ uso: "vivienda_unifamiliar", intervencion: "nueva", estructura: "hormigon",
    supConstruida: "180", plantasSobre: "2", alturaEvacuacion: "3", numViviendas: "1", ab: "0.02", personasVivienda: "3" });
  assert.equal(buscar(c, "Accesibilidad (SUA 9)").estado, "info");
  assert.equal(buscar(c, "HE 5").estado, "ok");
  assert.equal(buscar(c, "HE 4").estado, "ok"); // 3 × 28 = 84 l/día
  assert.equal(buscar(c, "sismorresistente").estado, "ok");
});

test("normativa aplicable según uso", () => {
  const ind = normativaAplicable(normalizar({ uso: "industrial", intervencion: "nueva", estructura: "acero" })).map((n) => n.id);
  assert.ok(ind.includes("RSCIEI") && ind.includes("CE") && ind.includes("DB-SE-A"));
  assert.ok(!ind.includes("DB-HR") && !ind.includes("HAB"));
  const viv = normativaAplicable(normalizar(base)).map((n) => n.id);
  assert.ok(viv.includes("ICT") && viv.includes("HAB") && viv.includes("NCSE") && viv.includes("ITC-BT-52"));
  const sinSismo = normativaAplicable(normalizar({ ...base, ab: "0.03" })).map((n) => n.id);
  assert.ok(!sinSismo.includes("NCSE"));
});

test("reforma parcial sin estructura no aplica DB SE", () => {
  const ids = normativaAplicable(normalizar({ ...base, intervencion: "reforma_parcial", estructura: "sin_intervencion" })).map((n) => n.id);
  assert.ok(!ids.includes("DB-SE") && !ids.includes("CE"));
});
