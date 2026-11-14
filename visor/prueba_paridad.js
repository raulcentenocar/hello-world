// Prueba de paridad: motor JS (visor/motor.js) frente a la referencia en Python.
// Uso (desde la raíz del repositorio):
//   python3 scripts/variantes_generador.py planos/variantes/entrada_UA-03-01.json
//   node visor/prueba_paridad.js <ruta a jsts.min.js> planos/variantes/entrada_UA-03-01.json planos/variantes/UA-03-01_Los_Pocillos/ranking.json
const vm = require("vm"), fs = require("fs");
const [jstsPath, entrada, rankingPy] = process.argv.slice(2);
const ctx = {}; ctx.self = ctx; ctx.window = ctx; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(jstsPath, "utf8"), ctx);
vm.runInContext(fs.readFileSync(__dirname + "/motor.js", "utf8"), ctx);
const M = ctx.Motor;
const norm = (r) => { r.mix = JSON.stringify(Object.keys(r.mix_pisos || {}).sort().map((t) => [t, r.mix_pisos[t]])); return r; };

const t0 = Date.now();
ctx.__txt = fs.readFileSync(entrada, "utf8");
const c = M.cargar(vm.runInContext("JSON.parse(__txt)", ctx));
const js = M.barrer(c);
const t = (Date.now() - t0) / 1000;
const py = JSON.parse(fs.readFileSync(rankingPy, "utf8")).variantes.map(norm);
js.forEach(norm);
const campos = ["casas", "pisos", "plazas", "techo_m2", "cumple", "ocupacion_B_pct", "fondo_saco_m", "portales", "plazas_accesibles", "mix"];
const k = (r) => [r.angulo_hileras, r.pct_zona_unifamiliar, r.unifamiliar_en, r.remate, r.acera].join("|");
const pyPor = {};
py.forEach((r) => (pyPor[k(r)] = pyPor[k(r)] || []).push(r));
let iguales = 0, distintas = [];
js.forEach((r) => {
  const cand = pyPor[k(r)] || [];
  const ok = cand.some((p) => campos.every((f) => (typeof p[f] === "number" ? Math.abs(p[f] - r[f]) <= 0.15 : p[f] === r[f])));
  if (ok) iguales++;
  else distintas.push({ clave: k(r), js: campos.map((f) => r[f]).join(" "), py: cand.map((p) => campos.map((f) => p[f]).join(" ")).join(" || ") });
});
const top = (rs) => rs.slice(0, 10).map(k).join("\n  ");
console.log(`Motor JS: ${js.length} variantes en ${t.toFixed(1)} s · Python: ${py.length}`);
console.log(`Coinciden: ${iguales}/${js.length}`);
distintas.slice(0, 15).forEach((d) => console.log("  ≠", d.clave, "\n     JS:", d.js, "\n     PY:", d.py));
console.log("Top 10 JS:\n  " + top(js));
console.log("Top 10 PY:\n  " + top(py));
process.exit(distintas.length || js.length !== py.length ? 1 : 0);
