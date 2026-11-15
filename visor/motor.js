/*
 * Motor de variantes de ordenación (reglas fijas, sin IA) — versión JavaScript.
 *
 * Es una traducción de scripts/variantes_generador.py (y de las funciones que usa
 * de scripts/volumetria_generador.py). El motor en Python es la REFERENCIA:
 * visor/prueba_paridad.js compara las dos versiones variante a variante.
 *
 * Requiere jsts (https://github.com/bjornharrtell/jsts) cargado como global `jsts`.
 * Funciona en el navegador y en node (dentro de un contexto con `jsts`).
 */
(function (root) {
  "use strict";
  var J = root.jsts;
  var gf = new J.geom.GeometryFactory();
  var AT = J.geom.util.AffineTransformation;
  var QS = 16; // segmentos por cuadrante en los offsets (igual que shapely)

  var FALTA = "FALTA DATO";
  var REQ_COMUN = ["edificabilidad_m2m2", "viviendas_max", "plazas_por_vivienda", "separacion_edificios_m"];
  var REQ_USO = ["ocupacion_pct", "plantas_max", "retranqueo_fachada_m", "retranqueo_linderos_m"];
  var REQ_ECONOMIA = ["precio_venta_casa_eur_m2c", "precio_venta_piso_eur_m2c", "coste_construccion_casa_eur_m2c",
    "coste_construccion_piso_eur_m2c", "coste_urbanizacion_eur_m2", "coste_plaza_superficie_eur", "coste_suelo_eur", "gastos_generales_pct"];
  function rumboVector(dx, dy) { return (Math.atan2(dx, dy) * 180 / Math.PI + 360) % 360; }
  function indicadores(viv, rumbos, viario, hip) {
    var n = rumbos.length, sur = rumbos.filter(function (r) { return r >= 112.5 && r < 247.5; }).length, por = {};
    rumbos.forEach(function (r) { var k = rumboTxt(r); por[k] = (por[k] || 0) + 1; });
    var orden = {}; Object.keys(por).sort().forEach(function (k) { orden[k] = por[k]; });
    var prog = hip.programa_zona_comun.filter(function (e) { return viv >= e[2]; });
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    return { jardines_a_sur_pct: n ? r1(100 * sur / n) : 0, orientacion_jardines: orden, viario_m2: r1(viario),
      viario_m2_por_vivienda: viv ? r1(viario / viv) : 0, zona_comun_programa_m2: prog.reduce(function (s, e) { return s + e[1]; }, 0),
      zona_comun_programa: prog.map(function (e) { return e[0]; }) };
  }
  function cuentaResultados(eco, techoCasas, techoPisos, plazas, sup, huella) {
    var faltan = REQ_ECONOMIA.filter(function (k) { return !(k in eco); });
    if (faltan.length) return { estado: FALTA, faltan: faltan };
    var ingresos = techoCasas * eco.precio_venta_casa_eur_m2c + techoPisos * eco.precio_venta_piso_eur_m2c;
    var construccion = techoCasas * eco.coste_construccion_casa_eur_m2c + techoPisos * eco.coste_construccion_piso_eur_m2c;
    var urbanizacion = Math.max(0, sup - huella) * eco.coste_urbanizacion_eur_m2;
    var aparcamiento = plazas * eco.coste_plaza_superficie_eur;
    var gastos = (construccion + urbanizacion + aparcamiento) * eco.gastos_generales_pct / 100;
    var coste = construccion + urbanizacion + aparcamiento + gastos + eco.coste_suelo_eur, beneficio = ingresos - coste;
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    return { estado: "OK", ingresos_eur: Math.round(ingresos), coste_construccion_eur: Math.round(construccion),
      coste_urbanizacion_eur: Math.round(urbanizacion), coste_aparcamiento_eur: Math.round(aparcamiento),
      gastos_generales_eur: Math.round(gastos), coste_suelo_eur: Math.round(eco.coste_suelo_eur), coste_total_eur: Math.round(coste),
      beneficio_eur: Math.round(beneficio), margen_sobre_ventas_pct: ingresos ? r1(100 * beneficio / ingresos) : 0,
      rentabilidad_sobre_coste_pct: coste ? r1(100 * beneficio / coste) : 0 };
  }

  var HIPOTESIS_DEFECTO = {
    fondo_casa_m: 12.0, ancho_casa_m: 6.5, sup_casa_m2: 156.0, casas_min_hilera: 3, casas_max_hilera: 8,
    jardin_trasero_m: 6.0, fondo_bloque_m: 12.0, longitud_min_bloque_m: 15.0, longitud_max_bloque_m: 40.0,
    tipos_piso: { "2D": { construida_m2: 85.0 }, "3D": { construida_m2: 105.0 }, "4D": { construida_m2: 125.0 } },
    mix_pisos_pct: { "2D": 30, "3D": 50, "4D": 20 }, nucleo_ancho_m: 5.0,
    plazas_accesibles: 2, transferencia_accesible_m: 1.2, altura_planta_m: 3.0, calzada_m: 6.0, plaza_ancho_m: 2.5, plaza_fondo_m: 5.0,
    paso_peatonal_casa_m: 1.5, acera_m: 1.5, plataforma_unica_m: 7.0, martillo_largo_m: 12.0, fondo_saco_max_m: 20.0,
    distancia_aparcamiento_edificio_m: 2.0, aparcamiento_fuera_retranqueo: true,
    paso_rejilla_m: 0.5, paso_fase_m: 2.0, zona_comun_min_m2: 400.0, tolerancia_frente_grados: 15.0,
    programa_zona_comun: [["piscina adultos + playa", 150, 1], ["piscina infantil", 30, 1], ["juegos infantiles", 80, 1],
      ["estancia ajardinada", 200, 1], ["sala comunitaria o gimnasio", 80, 40], ["pista de pádel", 230, 80]]
  };
  var BARRIDO_DEFECTO = {
    angulo_hileras: "fachadas",
    pct_zona_unifamiliar: [0, 30, 40, 50, 60, 70, 80, 100],
    unifamiliar_en: ["abajo", "arriba"],
    remate: ["fondo_saco", "martillo", "lazo"],
    acera: [false, true, "plataforma"],
    producto: "todo", estrategias: ["calles_paralelas", "perimetral"], acceso_pos: [0.3, 0.5, 0.7], interior: ["zona_comun", "casas"]
  };

  // ------------------------------------------------------------------ geometría
  function C(x, y) { return new J.geom.Coordinate(x, y); }
  function poligono(pts) {
    var cs = pts.map(function (p) { return C(p[0], p[1]); });
    cs.push(C(pts[0][0], pts[0][1]));
    return gf.createPolygon(gf.createLinearRing(cs), []);
  }
  function caja(x1, y1, x2, y2) { return poligono([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]); }
  function vacio() { return gf.createPolygon(); }
  function linea(a, b) { return gf.createLineString([C(a[0], a[1]), C(b[0], b[1])]); }
  function lim(g) { // bounds [minx, miny, maxx, maxy]
    var e = g.getEnvelopeInternal();
    return [e.getMinX(), e.getMinY(), e.getMaxX(), e.getMaxY()];
  }
  function polys(g) {
    if (!g || g.isEmpty()) return [];
    var t = g.getGeometryType();
    if (t === "Polygon") return [g];
    var out = [];
    for (var i = 0; i < g.getNumGeometries(); i++) out = out.concat(polys(g.getGeometryN(i)));
    return out;
  }
  function limpia(g) {
    if (!g || g.isEmpty()) return vacio();
    g = g.buffer(0);
    var ps = polys(g).filter(function (p) { return p.getArea() > 1.0; });
    if (!ps.length) return vacio();
    if (ps.length === 1) return ps[0];
    return gf.createMultiPolygon(ps);
  }
  function union(gs) {
    gs = gs.filter(function (g) { return g && !g.isEmpty(); });
    if (!gs.length) return vacio();
    var col = gf.createGeometryCollection(gs);
    return col.union();
  }
  function rotar(g, grados, c) {
    if (!g || g.isEmpty()) return g;
    return AT.rotationInstance(grados * Math.PI / 180, c[0], c[1]).transform(g);
  }
  function rotPts(pts, ang, c) {
    var a = ang * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    return pts.map(function (p) {
      return [(p[0] - c[0]) * ca - (p[1] - c[1]) * sa + c[0], (p[0] - c[0]) * sa + (p[1] - c[1]) * ca + c[1]];
    });
  }
  function piezaQueToca(g, toque) {
    var ps = polys(g);
    for (var i = 0; i < ps.length; i++) if (ps[i].intersects(toque)) return ps[i];
    return null;
  }

  // Comprobación rápida "rectángulo dentro de zona" (equivale a prep(zona).contains(caja)).
  var cachePrep = new WeakMap();
  function prep(zona) {
    if (cachePrep.has(zona)) return cachePrep.get(zona);
    var segs = [];
    polys(zona).forEach(function (p) {
      var anillos = [p.getExteriorRing()];
      for (var k = 0; k < p.getNumInteriorRing(); k++) anillos.push(p.getInteriorRingN(k));
      anillos.forEach(function (r) {
        var cs = r.getCoordinates();
        for (var i = 0; i + 1 < cs.length; i++) {
          var x1 = cs[i].x, y1 = cs[i].y, x2 = cs[i + 1].x, y2 = cs[i + 1].y;
          segs.push([x1, y1, x2, y2, Math.min(y1, y2), Math.max(y1, y2)]);
        }
      });
    });
    var pz = { segs: segs };
    cachePrep.set(zona, pz);
    return pz;
  }
  function segCortaInterior(s, rx1, ry1, rx2, ry2) {
    var eps = 1e-7;
    rx1 += eps; ry1 += eps; rx2 -= eps; ry2 -= eps;
    var x1 = s[0], y1 = s[1], dx = s[2] - x1, dy = s[3] - y1, t0 = 0, t1 = 1;
    var p = [-dx, dx, -dy, dy], q = [x1 - rx1, rx2 - x1, y1 - ry1, ry2 - y1];
    for (var i = 0; i < 4; i++) {
      if (p[i] === 0) { if (q[i] < 0) return false; }
      else {
        var r = q[i] / p[i];
        if (p[i] < 0) { if (r > t1) return false; if (r > t0) t0 = r; }
        else { if (r < t0) return false; if (r < t1) t1 = r; }
      }
    }
    return t1 - t0 > 1e-12;
  }
  function tramosEnFranja(zona, minx, maxx, y, fondo, separacion, lMin, lMax, paso) {
    var pz = prep(zona);
    var S = pz.segs.filter(function (s) { return s[5] >= y && s[4] <= y + fondo; });
    var n = Math.ceil((maxx - minx) / paso);
    var cy = y + fondo / 2;
    var dentro = new Array(n);
    for (var i = 0; i < n; i++) {
      var x1 = minx + i * paso, x2 = minx + (i + 1) * paso, cx = (x1 + x2) / 2, ok = true, cruces = 0;
      for (var k = 0; k < S.length; k++) {
        var s = S[k];
        var fuera = (s[0] >= x2 && s[2] >= x2) || (s[0] <= x1 && s[2] <= x1);
        if (!fuera && segCortaInterior(s, x1, y, x2, y + fondo)) { ok = false; break; }
        if ((s[1] > cy) !== (s[3] > cy)) {
          var xi = s[0] + (cy - s[1]) * (s[2] - s[0]) / (s[3] - s[1]);
          if (xi < cx) cruces++;
        }
      }
      dentro[i] = ok && (cruces % 2 === 1);
    }
    var tramos = [];
    i = 0;
    while (i < n) {
      if (dentro[i]) {
        var j = i;
        while (j < n && dentro[j]) j++;
        tramos.push([minx + i * paso, minx + j * paso]);
        i = j;
      } else i++;
    }
    var ok2 = [];
    tramos.forEach(function (t) {
      var a = t[0], b = t[1];
      if (ok2.length && a - ok2[ok2.length - 1][1] < separacion) a = ok2[ok2.length - 1][1] + separacion;
      if (b - a >= lMin) ok2.push([a, b]);
    });
    var rects = [];
    ok2.forEach(function (t) {
      var a = t[0], b = t[1];
      if (lMax) {
        while (b - a > lMax) { rects.push([a, y, a + lMax, y + fondo]); a += lMax + separacion; }
        if (b - a >= lMin) rects.push([a, y, b, y + fondo]);
      } else rects.push([a, y, b, y + fondo]);
    });
    return rects; // rectángulos como [x1, y1, x2, y2]
  }
  function R(r) { return caja(r[0], r[1], r[2], r[3]); }
  function areaR(r) { return (r[2] - r[0]) * (r[3] - r[1]); }

  function rumboTxt(r) {
    var n = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"];
    return n[Math.floor((((r + 22.5) % 360) + 360) % 360 / 45)];
  }
  function lados(pts, ccw) {
    var out = [], n = pts.length;
    for (var i = 0; i < n; i++) {
      var a = pts[i], b = pts[(i + 1) % n], dx = b[0] - a[0], dy = b[1] - a[1];
      var nx = ccw ? dy : -dy, ny = ccw ? -dx : dx;
      var rumbo = (Math.atan2(nx, ny) * 180 / Math.PI + 360) % 360;
      out.push({ indice: i, longitud_m: Math.round(Math.hypot(dx, dy) * 100) / 100, mira_a: rumboTxt(rumbo),
        rumbo_normal_grados: Math.round(rumbo * 10) / 10, seg: linea(a, b), a: a, b: b,
        angulo: Math.atan2(dy, dx) * 180 / Math.PI });
    }
    return out;
  }
  function zonaRetranqueos(poly, ls, fachadas, rF, rL) {
    var franjas = [];
    ls.forEach(function (l) {
      var r = fachadas.has(l.indice) ? rF : rL;
      if (r > 0) franjas.push(l.seg.buffer(r, QS));
    });
    if (!franjas.length) return poly;
    return limpia(poly.difference(union(franjas)));
  }
  function bloquesLineales0(zona, fondo, separacion, lMin, lMax, paso, fases) {
    // Equivale a bloques_lineales(zona, 0.0, …): bloques paralelos al eje x del marco.
    if (zona.isEmpty()) return [];
    fases = fases || 4;
    var b = lim(zona), mejor = [], mejorA = 0, modulo = fondo + separacion;
    for (var f = 0; f < fases; f++) {
      var y = b[1] + modulo * f / fases, rects = [];
      while (y + fondo <= b[3] + 1e-9) {
        rects = rects.concat(tramosEnFranja(zona, b[0], b[2], y, fondo, separacion, lMin, lMax, paso));
        y += modulo;
      }
      var a = rects.reduce(function (s, r) { return s + areaR(r); }, 0);
      if (a > mejorA + 1e-6) { mejor = rects; mejorA = a; }
    }
    return mejor;
  }

  // ------------------------------------------------------------------ entrada
  function cargar(cfg) {
    var par = cfg.parcela || {};
    if (!par.coordenadas) throw new Error("La parcela necesita 'coordenadas'.");
    var pts = par.coordenadas.map(function (p) { return [p[0], p[1]]; });
    var poly = poligono(pts);
    if (!poly.isValid()) throw new Error("La geometría de la parcela no es válida.");
    var faltan = [];
    function sinNulos(o) { var r = {}; Object.keys(o || {}).forEach(function (k) { if (o[k] !== null && o[k] !== undefined) r[k] = o[k]; }); return r; }
    var comun = sinNulos(cfg.comun);
    REQ_COMUN.forEach(function (k) { if (!(k in comun)) faltan.push("comun." + k); });
    var usos = {};
    ["unifamiliar", "multifamiliar"].forEach(function (uso) {
      var u = sinNulos(cfg[uso]);
      REQ_USO.forEach(function (k) { if (!(k in u)) faltan.push(uso + "." + k); });
      usos[uso] = u;
    });
    if (!cfg.fachadas || !cfg.fachadas.length) faltan.push("fachadas");
    if (!cfg.accesos || !cfg.accesos.length) faltan.push("accesos (lados por los que puede entrar el viario)");
    if (faltan.length) throw new Error(FALTA + ": " + faltan.join(", "));
    var hip = Object.assign({}, HIPOTESIS_DEFECTO, cfg.hipotesis || {});
    var barr = Object.assign({}, BARRIDO_DEFECTO, cfg.barrido || {});
    var sup = +(par.superficie_oficial_m2 || poly.getArea());
    var ccw = J.algorithm.Orientation.isCCW(poly.getExteriorRing().getCoordinates());
    var cen = poly.getCentroid();
    var eco = {}; Object.keys(cfg.economia || {}).forEach(function (k) { if (cfg.economia[k] !== null && cfg.economia[k] !== undefined) eco[k] = +cfg.economia[k]; });
    return { economia: eco, nombre: cfg.nombre || "parcela", pts: pts, poly: poly, sup: sup, f_sup: sup / poly.getArea(), ccw: ccw,
      centro: [cen.getX(), cen.getY()], fachadas: new Set(cfg.fachadas), accesos: new Set(cfg.accesos),
      comun: comun, uni: usos.unifamiliar, multi: usos.multifamiliar, hip: hip, barrido: barr, cfg: cfg };
  }

  // ------------------------------------------------------------------ zona unifamiliar
  function corte(poly, frac, abajo) {
    var b = lim(poly), objetivo = frac * poly.getArea(), lo = b[1], hi = b[3];
    for (var i = 0; i < 50; i++) {
      var mid = (lo + hi) / 2;
      if (poly.intersection(caja(b[0] - 1, b[1] - 1, b[2] + 1, mid)).getArea() < objetivo) lo = mid; else hi = mid;
    }
    var yc = (lo + hi) / 2;
    var inf = limpia(poly.intersection(caja(b[0] - 1, b[1] - 1, b[2] + 1, yc)));
    var sup = limpia(poly.intersection(caja(b[0] - 1, yc, b[2] + 1, b[3] + 1)));
    return { yc: yc, zonas: abajo ? [inf, sup] : [sup, inf] };
  }
  function filasCasas(U, y0, h, hip, sep, prohibido) {
    var zona = (!prohibido || prohibido.isEmpty()) ? U : limpia(U.difference(prohibido));
    if (zona.isEmpty()) return [];
    var b = lim(zona), a = hip.ancho_casa_m;
    var tr = tramosEnFranja(zona, b[0], b[2], y0, h, sep, hip.casas_min_hilera * a, hip.casas_max_hilera * a, hip.paso_rejilla_m);
    var hileras = [];
    tr.forEach(function (r) {
      var n = Math.floor((r[2] - r[0] + 1e-6) / a);
      if (n >= hip.casas_min_hilera) {
        n = Math.min(n, hip.casas_max_hilera);
        var h1 = [];
        for (var i = 0; i < n; i++) h1.push([r[0] + i * a, y0, r[0] + (i + 1) * a, y0 + h]);
        hileras.push(h1);
      }
    });
    return hileras;
  }
  function modulos(U, Z, acc, hip, sep, acera, fase) {
    var F = hip.fondo_casa_m, P = hip.plaza_fondo_m, Cz = hip.calzada_m, a_ = acera ? hip.acera_m : 0;
    var g = Math.max(sep, 2 * hip.jardin_trasero_m);
    var bz = lim(Z), bu = lim(U), mods = [], y = bu[1] + fase;
    while (true) {
      var dobles = y + 2 * F + 2 * (P + a_) + Cz, yc, filas, nxt;
      if (dobles <= bu[3] + 1e-6) { yc = y + F + P + a_; filas = [[y, "abajo"], [yc + Cz + P + a_, "arriba"]]; nxt = dobles + g; }
      else if (y + F + P + a_ + Cz <= bz[3] + 1e-6) { yc = y + F + P + a_; filas = [[y, "abajo"]]; nxt = null; }
      else break;
      var calz = piezaQueToca(Z.intersection(caja(bz[0] - 1, yc, bz[2] + 1, yc + Cz)), acc);
      if (calz) {
        var tr = tramosEnFranja(Z, bz[0], bz[2], yc, Cz, 0.0, Cz, null, hip.paso_rejilla_m)
          .map(function (r) { return { r: r, d: R(r).distance(acc) }; })
          .filter(function (t) { return t.d <= Cz; });
        if (tr.length) {
          var t = tr.reduce(function (m, x) { return x.d < m.d ? x : m; });
          var izq = calz.intersection(acc).getCentroid().getX() < calz.getCentroid().getX();
          var xLim = izq ? t.r[2] : t.r[0];
          var bc = lim(calz);
          var x1 = izq ? bz[0] - 1 : xLim, x2 = izq ? xLim : bz[2] + 1;
          calz = limpia(calz.intersection(caja(x1, yc, x2, yc + Cz)));
          mods.push({ yc: yc, filas: filas, calz_full: calz, x_lim: xLim, izq: izq });
        }
      }
      if (nxt === null) break;
      y = nxt;
    }
    return mods;
  }
  function resolverModulo(m, U, acc, hip, sep, prohibido) {
    var F = hip.fondo_casa_m, Cz = hip.calzada_m, calz = m.calz_full;
    if (!calz || calz.isEmpty()) return null;
    var cx = calz.intersects(acc) ? calz.intersection(acc.buffer(0.01, QS)).getCentroid().getX() : lim(calz)[0];
    var izq = ("izq" in m) ? m.izq : cx < calz.getCentroid().getX();
    var xLim = ("x_lim" in m) ? m.x_lim : (izq ? lim(calz)[2] : lim(calz)[0]);
    var hileras = [];
    m.filas.forEach(function (f) {
      filasCasas(U, f[0], F, hip, sep, prohibido).forEach(function (h) {
        h = h.filter(function (c) { return izq ? c[2] <= xLim + 1e-6 : c[0] >= xLim - 1e-6; });
        if (h.length >= hip.casas_min_hilera) hileras.push([f[1], h]);
      });
    });
    var casas = [];
    hileras.forEach(function (lh) { casas = casas.concat(lh[1]); });
    if (!casas.length) return null;
    var xe = izq ? Math.max.apply(null, casas.map(function (c) { return c[2]; }))
                 : Math.min.apply(null, casas.map(function (c) { return c[0]; }));
    var bc = lim(calz);
    var x1 = izq ? bc[0] - 1 : xe, x2 = izq ? xe : bc[2] + 1;
    var calzada = limpia(calz.intersection(caja(x1, m.yc, x2, m.yc + Cz)));
    return { yc: m.yc, hileras: hileras, calzada: calzada, izq: izq, xe: xe, largo: Math.abs(xe - cx), x_lim: xLim };
  }
  function plazasCasa(c, lado, yc, hip) {
    var P = hip.plaza_fondo_m, Cz = hip.calzada_m;
    return lado === "abajo" ? [c[0], yc - P, c[2], yc] : [c[0], yc + Cz, c[2], yc + Cz + P];
  }
  function secuenciaMix(n, mix) {
    var tipos = Object.keys(mix), tot = tipos.reduce(function (s, t) { return s + mix[t]; }, 0) || 1, cnt = {}, out = [];
    tipos.forEach(function (t) { cnt[t] = 0; });
    for (var i = 1; i <= n; i++) {
      var mejor = null, mv = null;
      tipos.forEach(function (t, j) {
        var v = mix[t] / tot * i - cnt[t];
        if (mejor === null || v > mv) { mejor = t; mv = v; }
      });
      cnt[mejor]++; out.push(mejor);
    }
    return out;
  }
  function colocarPortales(cand, seq, tipos, hip, huellaMax) {
    var F = hip.fondo_bloque_m, nw = hip.nucleo_ancho_m, bloques = [], pisos = [], nucleos = [], k = 0, huella = 0;
    for (var i = 0; i < cand.length && k < seq.length; i++) {
      var b = cand[i], x1 = b[0], y1 = b[1], x2 = b[2], x = x1;
      while (k < seq.length) {
        var wl = tipos[seq[k]].construida_m2 / F, fin;
        if (k + 1 < seq.length) {
          var wr = tipos[seq[k + 1]].construida_m2 / F;
          fin = x + wl + nw + wr;
          if (fin <= x2 + 1e-6 && huella + (fin - x1) * F <= huellaMax + 1e-6) {
            pisos.push([[x, y1, x + wl, y1 + F], seq[k]], [[x + wl + nw, y1, fin, y1 + F], seq[k + 1]]);
            nucleos.push([x + wl, y1, x + wl + nw, y1 + F]);
            x = fin; k += 2; continue;
          }
        }
        fin = x + wl + nw;
        if (fin <= x2 + 1e-6 && huella + (fin - x1) * F <= huellaMax + 1e-6) {
          pisos.push([[x, y1, x + wl, y1 + F], seq[k]]);
          nucleos.push([x + wl, y1, fin, y1 + F]);
          x = fin; k += 1; continue;
        }
        break;
      }
      if (x > x1 + 1e-6) { bloques.push([x1, y1, x, y1 + F]); huella += (x - x1) * F; }
    }
    var techo = pisos.reduce(function (s, p) { return s + tipos[p[1]].construida_m2; }, 0) + nucleos.length * nw * F;
    return [bloques, pisos, nucleos, k, techo];
  }
  function recuentoHileras(casas) {
    var filas = {};
    casas.forEach(function (c) { var k = c[1].toFixed(2); (filas[k] = filas[k] || []).push(c); });
    var out = [];
    Object.keys(filas).sort(function (a, b) { return +a - +b; }).forEach(function (k) {
      var bs = filas[k].slice().sort(function (a, b) { return a[0] - b[0]; }), n = 1;
      for (var i = 0; i + 1 < bs.length; i++) { if (bs[i + 1][0] - bs[i][2] > 0.01) { out.push(n); n = 1; } else n++; }
      out.push(n);
    });
    return out;
  }
  function ladoTxt(ang, uniEn) {
    var a = ang * Math.PI / 180, dy0 = uniEn === "abajo" ? -1 : 1;
    var dx = -Math.sin(a) * dy0, dy = Math.cos(a) * dy0;
    return rumboTxt((Math.atan2(dx, dy) * 180 / Math.PI + 360) % 360);
  }

  // ------------------------------------------------------------------ una variante
  function tipoCalle(hip, acera) {
    if (acera === "plataforma") return { hip: Object.assign({}, hip, { calzada_m: hip.plataforma_unica_m }), banda: false, itinerario: true };
    var banda = acera === true || acera === "acera";
    return { hip: hip, banda: banda, itinerario: banda };
  }
  function variante(ctx, p) {
    var ang = p.ang, pct = p.pct, uniEn = p.uni_en, remate = p.remate, aceraIn = p.acera;
    var tc = tipoCalle(ctx.hip, aceraIn), acera = tc.banda, itinerario = tc.itinerario;
    var hip = tc.hip, com = ctx.comun, sep = +com.separacion_edificios_m, c = ctx.centro;
    var pts = rotPts(ctx.pts, -ang, c), poly = poligono(pts), ls = lados(pts, ctx.ccw);
    var acc = union(ls.filter(function (l) { return ctx.accesos.has(l.indice); }).map(function (l) { return l.seg; })).buffer(0.5, QS);
    var notas = [], avisos = [], Cz = hip.calzada_m;

    // 1. Zonificación
    var Zu, Zm, yc = null, corteG = null;
    if (pct >= 100) { Zu = poly; Zm = vacio(); }
    else if (pct <= 0) { Zu = vacio(); Zm = poly; }
    else { var k = corte(poly, pct / 100, uniEn === "abajo"); yc = k.yc; Zu = k.zonas[0]; Zm = k.zonas[1]; }
    var bp = lim(poly);
    if (!Zu.isEmpty() && !Zm.isEmpty()) corteG = caja(bp[0] - 1, yc - sep / 2, bp[2] + 1, yc + sep / 2);
    function edificable(Z, uso) {
      if (Z.isEmpty()) return vacio();
      var u = ctx[uso];
      var E = zonaRetranqueos(poly, ls, ctx.fachadas, u.retranqueo_fachada_m, u.retranqueo_linderos_m);
      E = limpia(E.intersection(Z));
      return corteG ? limpia(E.difference(corteG)) : E;
    }
    var U = edificable(Zu, "uni"), M = edificable(Zm, "multi");

    // 2. Zona unifamiliar
    var mods = [];
    if (!U.isEmpty()) {
      var mejor = [], mejorN = -1, g = Math.max(sep, 2 * hip.jardin_trasero_m);
      var periodo = 2 * hip.fondo_casa_m + 2 * hip.plaza_fondo_m + hip.calzada_m + g;
      for (var f = 0.0; f < periodo; f += hip.paso_fase_m) {
        var res = modulos(U, Zu, acc, hip, sep, acera, f).map(function (m) { return resolverModulo(m, U, acc, hip, sep); })
          .filter(function (r) { return r; });
        var n = 0;
        res.forEach(function (r) { r.hileras.forEach(function (h) { n += h[1].length; }); });
        if (n > mejorN) { mejor = res; mejorN = n; }
      }
      mods = mejor;
    }

    // Remates
    var remates = [];
    if (mods.length) {
      var remateMod = new Map();
      if (remate === "lazo") {
        var pares = [], resto = [], orden = mods.slice().sort(function (a, b) { return a.yc - b.yc; }), i = 0;
        while (i < orden.length) {
          if (i + 1 < orden.length && orden[i].izq === orden[i + 1].izq) { pares.push([orden[i], orden[i + 1]]); i += 2; }
          else { resto.push(orden[i]); i += 1; }
        }
        pares.forEach(function (pr) {
          var m1 = pr[0], m2 = pr[1];
          var xe = m1.izq ? Math.min(m1.xe, m2.xe) : Math.max(m1.xe, m2.xe);
          var x1 = m1.izq ? xe - Cz : xe, x2 = m1.izq ? xe : xe + Cz;
          remates.push(limpia(caja(x1, m1.yc, x2, m2.yc + Cz).intersection(poly)));
          m1.largo = 0; m2.largo = 0;
        });
        if (resto.length) notas.push("Lazo: un módulo de calle sin pareja → se remata con martillo.");
        if (!pares.length) remate = "martillo";
        resto.forEach(function (m) { remateMod.set(m, "martillo"); });
      } else mods.forEach(function (m) { remateMod.set(m, remate); });
      var Lm = hip.martillo_largo_m;
      mods.forEach(function (m) {
        if (remateMod.get(m) === "martillo") {
          var xe = m.xe, x1 = m.izq ? xe - Cz : xe, x2 = m.izq ? xe : xe + Cz;
          remates.push(limpia(caja(x1, m.yc + Cz / 2 - Lm / 2, x2, m.yc + Cz / 2 + Lm / 2).intersection(poly)));
          m.largo = 0;
        }
      });
      if (remates.length) {
        var prohib = union(remates).buffer(0.01, QS), nuevos = [];
        mods.forEach(function (m) {
          var vistos = {}, filas = [];
          m.hileras.forEach(function (lh) { var key = lh[1][0][1] + "|" + lh[0]; if (!vistos[key]) { vistos[key] = 1; filas.push([lh[1][0][1], lh[0]]); } });
          filas.sort(function (a, b) { return a[0] - b[0] || (a[1] < b[1] ? -1 : 1); });
          var r = resolverModulo({ yc: m.yc, filas: filas, calz_full: m.calzada, izq: m.izq, x_lim: m.x_lim }, U, acc, hip, sep, prohib);
          if (r) { r.largo = m.largo; nuevos.push(r); }
        });
        mods = nuevos;
      }
    }

    var lista = [], aceras = [];
    var remG = remates.map(function (r) { return r; });
    mods.forEach(function (m) {
      m.hileras.forEach(function (lh) {
        lh[1].forEach(function (casa) {
          var b = plazasCasa(casa, lh[0], m.yc, hip), bg = R(b);
          var toca = remG.some(function (r) { return bg.intersects(r); });
          lista.push({ casa: casa, plazas: toca ? null : b, lado: lh[0] });
        });
      });
      if (acera) {
        var lad = {};
        m.hileras.forEach(function (lh) { if (lh[1].length) lad[lh[0]] = 1; });
        var bc = lim(m.calzada), P = hip.plaza_fondo_m, a_ = hip.acera_m;
        if (lad.abajo) aceras.push([bc[0], m.yc - P - a_, bc[2], m.yc - P]);
        if (lad.arriba) aceras.push([bc[0], m.yc + Cz + P, bc[2], m.yc + Cz + P + a_]);
      }
    });
    lista.forEach(function (x) { x.d = R(x.casa).distance(acc); });
    lista.sort(function (a, b) { return a.d - b.d; });
    var porCasa = Math.floor((hip.ancho_casa_m - hip.paso_peatonal_casa_m) / hip.plaza_ancho_m);

    // 3. Reparto (programa de pisos por portales) con el aparcamiento reservado primero
    var Emax = ctx.sup * com.edificabilidad_m2m2, vmax = Math.floor(com.viviendas_max);
    var plM = Math.floor(ctx.multi.plantas_max);
    if ("altura_max_m" in ctx.multi) plM = Math.min(plM, Math.floor(ctx.multi.altura_max_m / hip.altura_planta_m + 1e-9));
    var huellaMaxM = Zm.isEmpty() ? 0 : ctx.multi.ocupacion_pct / 100 * Zm.getArea() * ctx.f_sup;
    var tipos = hip.tipos_piso, mix = {};
    Object.keys(hip.mix_pisos_pct).forEach(function (t) { if (hip.mix_pisos_pct[t] > 0 && tipos[t]) mix[t] = hip.mix_pisos_pct[t]; });
    var hayMix = Object.keys(mix).length > 0;
    var P = hip.plaza_fondo_m, pa = hip.plaza_ancho_m, da = hip.distancia_aparcamiento_edificio_m;
    var calles = mods.map(function (m) { return m.calzada; }).concat(remates);
    var red = calles.length ? union(calles).buffer(1.0, QS) : vacio();
    var dmaxAcc = Math.max(ctx.uni.retranqueo_fachada_m, ctx.multi.retranqueo_fachada_m, ctx.uni.retranqueo_linderos_m, ctx.multi.retranqueo_linderos_m) + 3.0;
    var baseAp = hip.aparcamiento_fuera_retranqueo ? (!M.isEmpty() ? M : U) : (!Zm.isEmpty() ? Zm : Zu);
    var accCx = acc.getCentroid().getX();

    function bolsa(libre, faltaPl, nAcc) {
      var out = { bolsas: [], viales_bolsa: [], n_bolsa: 0, largo_bolsa: 0, accesibles: [], falta: 0 }, accPend = nAcc;
      var lb = libre.isEmpty() ? [0, 0, 0, 0] : lim(libre), y = lb[1];
      while (faltaPl > 0 && !libre.isEmpty() && y + P + Cz <= lb[3]) {
        var doble = y + 2 * P + Cz <= lb[3], W = doble ? 2 * P + Cz : P + Cz, ladosPl = doble ? 2 : 1;
        var trs = tramosEnFranja(libre, lb[0], lb[2], y, W, 0.0, 2 * pa, null, hip.paso_rejilla_m)
          .map(function (r) { var g = R(r); return { r: r, d: g.distance(acc), red: !red.isEmpty() && g.distance(red) <= 0.01 }; })
          .sort(function (a, b) { return a.d - b.d; });
        var usado = false;
        for (var q = 0; q < trs.length; q++) {
          if (trs[q].d > dmaxAcc && !trs[q].red) continue;
          var r = trs[q].r, x1 = r[0], y1 = r[1], x2 = r[2], y2 = r[3];
          var anchoAcc = accPend * pa + Math.ceil(accPend / 2) * hip.transferencia_accesible_m;
          var cap = ladosPl === 1 ? Math.floor((x2 - x1 - anchoAcc) / pa) + accPend
                                  : 2 * Math.floor((x2 - x1) / pa) - Math.ceil(anchoAcc / pa) + accPend;
          if (cap <= 0) continue;
          var nb = Math.min(cap, faltaPl + (faltaPl % ladosPl));
          var largo = Math.min(anchoAcc + Math.ceil(Math.max(0, nb - accPend) / ladosPl) * pa, x2 - x1);
          var cercaIzq = Math.abs(x1 - accCx) < Math.abs(x2 - accCx);
          var rr = cercaIzq ? [x1, y1, x1 + largo, y2] : [x2 - largo, y1, x2, y2];
          out.bolsas.push(rr);
          if (accPend) {
            var ax = cercaIzq ? rr[0] : rr[2] - anchoAcc;
            out.accesibles.push([ax, y1, ax + anchoAcc, y1 + P]);
            accPend = 0;
          }
          if (!trs[q].red) {
            var vx1 = cercaIzq ? bp[0] - 1 : rr[2], vx2 = cercaIzq ? rr[0] : bp[2] + 1, ya = y1 + (doble ? P : 0);
            var vial = piezaQueToca(poly.intersection(caja(vx1, ya, vx2, ya + Cz)), acc);
            if (vial) { out.viales_bolsa.push(vial); out.largo_bolsa = Math.max(out.largo_bolsa, largo + vial.getLength() / 2 - Cz); }
          }
          out.n_bolsa += nb; faltaPl -= nb; usado = true;
          if (faltaPl <= 0) break;
        }
        y += usado ? W : 1.0;
      }
      out.falta = Math.max(0, faltaPl);
      return out;
    }
    function solucion(n, u) {
      var cs = lista.slice(0, n), casasN = cs.map(function (x) { return x.casa; });
      var plazasN = cs.filter(function (x) { return x.plazas; }).map(function (x) { return x.plazas; });
      var nPlU = plazasN.length * porCasa, nPis = u * plM;
      var nec = Math.floor(com.plazas_por_vivienda) * (n + nPis), nAcc = nPis ? Math.floor(hip.plazas_accesibles) : 0;
      var falta = Math.max(0, nec - nPlU, nAcc);
      var ap = { bolsas: [], viales_bolsa: [], n_bolsa: 0, largo_bolsa: 0, accesibles: [], falta: 0 };
      if (falta && !baseAp.isEmpty()) {
        var ocupado = union(casasN.map(R).concat(plazasN.map(R), calles, aceras.map(R)));
        var libre = limpia(baseAp.intersection(poly).difference(ocupado.isEmpty() ? vacio() : ocupado.buffer(da, QS)));
        if (corteG && !Zm.isEmpty()) libre = limpia(libre.difference(corteG));
        ap = bolsa(libre, falta, nAcc);
      } else if (falta) ap.falta = falta;
      var lay = [[], [], [], 0, 0];
      if (u && !M.isEmpty()) {
        var ocAp = union(ap.bolsas.map(R).concat(ap.viales_bolsa));
        var Mlib = ocAp.isEmpty() ? M : limpia(M.difference(ocAp.buffer(da, QS)));
        var cand = Mlib.isEmpty() ? [] : bloquesLineales0(Mlib, hip.fondo_bloque_m, sep, hip.longitud_min_bloque_m, hip.longitud_max_bloque_m, hip.paso_rejilla_m);
        cand.sort(function (a, b) { var ya = (a[1] + a[3]) / 2, yb = (b[1] + b[3]) / 2; return ya - yb || ((a[0] + a[2]) / 2 - (b[0] + b[2]) / 2); });
        lay = colocarPortales(cand, secuenciaMix(u, mix), tipos, hip, huellaMaxM);
      }
      var okPl = nPlU + ap.n_bolsa >= nec && !(nAcc && !ap.accesibles.length);
      return { n: n, u: u, lay: lay, casas: casasN, plazas_u: plazasN, n_plazas_u: nPlU, n_pisos: nPis, necesarias: nec,
        n_acc: nAcc, ap: ap, ok_pl: okPl, completo: lay[3] === u };
    }
    function mayor(a, b) { for (var i = 0; i < a.length; i++) { if (a[i] > b[i]) return true; if (a[i] < b[i]) return false; } return false; }
    var tope = Math.min(lista.length, vmax, Math.floor(Emax / hip.sup_casa_m2)), elegido = null, mejorClave = null, respaldo = null;
    for (var nn = tope; nn > Math.max(-1, tope - 16); nn--) {
      var limViv = vmax - nn, limTecho = Emax - nn * hip.sup_casa_m2;
      var uMax = (hayMix && !M.isEmpty()) ? Math.floor(limViv / plM) : 0;
      if (mejorClave && nn + uMax * plM < mejorClave[0]) continue;
      if (nn && Math.min.apply(null, recuentoHileras(lista.slice(0, nn).map(function (x) { return x.casa; }))) < hip.casas_min_hilera) continue;
      for (var u = uMax; u >= 0; u--) {
        var seq = secuenciaMix(u, mix);
        if (plM * seq.reduce(function (s, t) { return s + tipos[t].construida_m2; }, 0) > limTecho + 1e-6) continue;
        if (mejorClave && nn + u * plM < mejorClave[0]) break;
        var so = solucion(nn, u);
        if (!respaldo) respaldo = so;
        if (!so.completo || plM * so.lay[4] > limTecho + 1e-6) continue;
        var plSol = so.n_plazas_u + so.ap.n_bolsa, deficit = Math.max(0, so.necesarias - plSol);
        if (so.n_acc && !so.ap.accesibles.length) deficit = Math.max(deficit, so.n_acc);
        var ppv = Math.max(1, Math.floor(com.plazas_por_vivienda));
        var clave = [nn + u * plM - Math.ceil(deficit / ppv), nn + u * plM, nn * hip.sup_casa_m2 + plM * so.lay[4]];
        if (!mejorClave || mayor(clave, mejorClave)) { elegido = so; mejorClave = clave; }
        if (so.ok_pl) break;
      }
    }
    if (!elegido) {
      elegido = respaldo || solucion(Math.min(tope, lista.length), 0);
      notas.push("Ningún reparto encaja completo: se muestra el primero probado.");
    }
    var nCasas = elegido.n, nPisos = elegido.n_pisos;
    var bloques = elegido.lay[0], pisosGeo = elegido.lay[1], nucleos = elegido.lay[2], uPlanta = elegido.lay[3], techoPlanta = elegido.lay[4];
    if (nCasas < lista.length) notas.push("Se colocan " + nCasas + " de " + lista.length + " casas posibles para maximizar viviendas y techo.");
    var casas = elegido.casas, plazasU = elegido.plazas_u, nPlazasU = elegido.n_plazas_u;
    var techoU = nCasas * hip.sup_casa_m2, techoM = plM * techoPlanta;
    var hilerasN = recuentoHileras(casas);
    var mixReal = {};
    pisosGeo.forEach(function (p) { mixReal[p[1]] = (mixReal[p[1]] || 0) + plM; });
    if (nPisos) notas.push("Pisos: " + uPlanta + " por planta × " + plM + " plantas en " + nucleos.length + " portales (" +
      Object.keys(mixReal).sort().map(function (k) { return k + " " + mixReal[k]; }).join(", ") + ").");
    var viv = nCasas + nPisos, necesarias = elegido.necesarias, nAccR = elegido.n_acc;
    var bolsas = elegido.ap.bolsas, vialesBolsa = elegido.ap.viales_bolsa, nBolsa = elegido.ap.n_bolsa;
    var largoBolsa = elegido.ap.largo_bolsa, accesibles = elegido.ap.accesibles;

    // Espacio libre comunitario de la zona de bloques
    var zonaComunM = vacio();
    if (nPisos && !Zm.isEmpty()) {
      var ocM = union(bloques.map(R).concat(bolsas.map(R), vialesBolsa, accesibles.map(R), mods.map(function (m) { return m.calzada; }), remates));
      zonaComunM = ocM.isEmpty() ? Zm : limpia(Zm.difference(ocM.buffer(hip.distancia_aparcamiento_edificio_m, QS)));
      if (corteG) zonaComunM = limpia(zonaComunM.difference(corteG));
    }
    if (mods.length && aceraIn === "plataforma") notas.push("Calle de plataforma única de " + hip.calzada_m.toFixed(1) + " m (coexistencia, sin acera separada).");

    // 4. Comprobaciones
    var huellaU = casas.reduce(function (s, r) { return s + areaR(r); }, 0);
    var huellaM = bloques.reduce(function (s, r) { return s + areaR(r); }, 0);
    var techo = techoU + techoM, plazas = nPlazasU + nBolsa;
    var ocAu = Zu.isEmpty() ? 0 : 100 * huellaU / (Zu.getArea() * ctx.f_sup);
    var ocAm = Zm.isEmpty() ? 0 : 100 * huellaM / (Zm.getArea() * ctx.f_sup);
    var ocB = 100 * (huellaU + huellaM) / ctx.sup;
    var fondoSaco = Math.max.apply(null, mods.map(function (m) { return m.largo; }).concat([0]));
    var chk = {
      hay_viviendas: viv > 0, viviendas: viv <= vmax, techo: techo <= Emax + 0.5, plazas: plazas >= necesarias && !(nAccR && !accesibles.length),
      ocupacion_A: ocAu <= ctx.uni.ocupacion_pct + 1e-6 && ocAm <= ctx.multi.ocupacion_pct + 1e-6,
      fondo_saco_SI5: fondoSaco <= hip.fondo_saco_max_m + 1e-6, itinerario_peatonal: itinerario || !mods.length
    };
    if (!chk.plazas) avisos.push(plazas < necesarias ? "Faltan " + (necesarias - plazas) + " plazas." : "Faltan las plazas accesibles.");
    if (!chk.fondo_saco_SI5) avisos.push("Calle sin salida de " + Math.round(fondoSaco) + " m sin espacio de maniobra (DB-SI SI 5, revisar).");
    if (!chk.itinerario_peatonal) avisos.push("Calle de casas sin acera: itinerario peatonal por la calzada (DB-SUA 9, revisar).");
    if (largoBolsa > hip.fondo_saco_max_m) notas.push("La bolsa de aparcamiento es un fondo de saco de ≈ " + Math.round(largoBolsa) + " m (revisar).");
    if (hilerasN.length) notas.push("Hileras: " + hilerasN.join(" + ") + " casas.");

    var aR = ang * Math.PI / 180;
    var rumbos = lista.slice(0, nCasas).map(function (x) { var dy0 = x.lado === "abajo" ? -1 : 1; return rumboVector(-Math.sin(aR) * dy0, Math.cos(aR) * dy0); });
    var viarioG = mods.map(function (m) { return m.calzada; }).concat(remates, vialesBolsa, aceras.map(R));
    var ind = indicadores(viv, rumbos, viarioG.length ? union(viarioG).getArea() : 0, hip);
    function back(g) { return rotar(g, ang, c); }
    var geo = {
      parcela: back(poly), zona_uni: back(Zu), zona_multi: back(Zm), edif_uni: back(U), edif_multi: back(M),
      casas: casas.map(function (r) { return back(R(r)); }), plazas_casas: plazasU.map(function (r) { return back(R(r)); }),
      calzadas: mods.map(function (m) { return back(m.calzada); }).concat(remates.map(back), vialesBolsa.map(back)),
      bolsas: bolsas.map(function (r) { return back(R(r)); }), bloques: bloques.map(function (r) { return back(R(r)); }),
      aceras: aceras.map(function (r) { return back(R(r)); }),
      pisos: pisosGeo.map(function (p) { return back(R(p[0])); }), nucleos: nucleos.map(function (r) { return back(R(r)); }),
      accesibles: accesibles.map(function (r) { return back(R(r)); }), zona_comun: back(zonaComunM),
      corte: corteG ? back(linea([bp[0] - 1, yc], [bp[2] + 1, yc]).intersection(poly)) : null
    };
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    var ok = Object.keys(chk).every(function (k) { return chk[k]; });
    return {
      angulo_hileras: r1(((ang % 180) + 180) % 180), pct_zona_unifamiliar: pct,
      unifamiliar_en: (pct > 0 && pct < 100) ? ladoTxt(ang, uniEn) : (pct >= 100 ? "todo" : "—"),
      estrategia: "calles_paralelas", uni_en_marco: uniEn, remate: remate, acera: aceraIn,
      casas: nCasas, pisos: nPisos, viviendas: viv, bloques: bloques.length, plantas_bloque: plM, portales: nucleos.length,
      pisos_por_planta: uPlanta, mix_pisos: mixReal, tipos_pisos_planta: pisosGeo.map(function (p) { return p[1]; }),
      plazas_accesibles: accesibles.length ? nAccR : 0, techo_casas_m2: r1(techoU), techo_pisos_m2: r1(techoM),
      economia: cuentaResultados(ctx.economia, techoU, techoM, plazas, ctx.sup, huellaU + huellaM),
      zona_comun_m2: zonaComunM.isEmpty() ? 0 : r1(zonaComunM.getArea()),
      jardines_a_sur_pct: ind.jardines_a_sur_pct, orientacion_jardines: ind.orientacion_jardines, viario_m2: ind.viario_m2,
      viario_m2_por_vivienda: ind.viario_m2_por_vivienda, zona_comun_programa_m2: ind.zona_comun_programa_m2, zona_comun_programa: ind.zona_comun_programa,
      plantas_casa: Math.floor(ctx.uni.plantas_max),
      techo_m2: r1(techo), aprovechamiento_pct: r1(100 * techo / Emax), plazas: plazas, plazas_necesarias: necesarias,
      plazas_casas: nPlazasU, plazas_bolsa: nBolsa, huella_m2: r1(huellaU + huellaM),
      ocupacion_A_uni_pct: r1(ocAu), ocupacion_A_multi_pct: r1(ocAm), ocupacion_B_pct: r1(ocB),
      fondo_saco_m: r1(fondoSaco), comprobaciones: chk, cumple: ok, avisos: avisos, notas: notas, hileras: hilerasN,
      geo: geo
    };
  }

  // ------------------------------------------------------------------ P02 perimetral
  function difAng(a, b) { return Math.abs((((a - b + 180) % 360) + 360) % 360 - 180); }
  function frentes(pts, ccw, tol) {
    var ls = lados(pts, ccw), n = ls.length, ini = 0;
    for (var i = 0; i < n; i++) if (difAng(ls[i].angulo, ls[(i - 1 + n) % n].angulo) > tol) { ini = i; break; }
    var grupos = [], act = [ls[ini]];
    for (var k = 1; k < n; k++) {
      var l = ls[(ini + k) % n];
      if (difAng(l.angulo, act[act.length - 1].angulo) <= tol) act.push(l); else { grupos.push(act); act = [l]; }
    }
    grupos.push(act);
    return grupos.map(function (g) {
      var a = g[0].a, b = g[g.length - 1].b, dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
      var nrm = ccw ? [-dy / L, dx / L] : [dy / L, -dx / L];
      return { lados: g, indices: new Set(g.map(function (l) { return l.indice; })), a: a, b: b, largo: L, normal: nrm,
        segs: union(g.map(function (l) { return l.seg; })), linea: linea(a, b) };
    });
  }
  function filasEnFrente(zona, f, y0, h, hip, sep, c) {
    var giro = 90.0 - Math.atan2(f.normal[1], f.normal[0]) * 180 / Math.PI;
    var zr = limpia(rotar(zona, giro, c));
    if (zr.isEmpty()) return { hileras: [], giro: giro, ye: null };
    var ab = rotPts([f.a, f.b], giro, c), ye = (ab[0][1] + ab[1][1]) / 2, a_ = hip.ancho_casa_m, b = lim(zr);
    var tr = tramosEnFranja(zr, b[0], b[2], ye + y0, h, sep, hip.casas_min_hilera * a_, hip.casas_max_hilera * a_, hip.paso_rejilla_m);
    var hileras = [];
    tr.forEach(function (r) {
      var n = Math.min(Math.floor((r[2] - r[0] + 1e-6) / a_), hip.casas_max_hilera);
      if (n >= hip.casas_min_hilera) { var hh = []; for (var i = 0; i < n; i++) hh.push([r[0] + i * a_, r[0] + (i + 1) * a_]); hileras.push(hh); }
    });
    return { hileras: hileras, giro: giro, ye: ye };
  }
  function variantePerimetral(ctx, accesoPos, interior, aceraIn) {
    var tc = tipoCalle(ctx.hip, aceraIn), acera = tc.banda, itinerario = tc.itinerario;
    var hip = tc.hip, com = ctx.comun, sep = +com.separacion_edificios_m, poly = ctx.poly, c = ctx.centro;
    var ls = lados(ctx.pts, ctx.ccw);
    var F = hip.fondo_casa_m, P = hip.plaza_fondo_m, Cz = hip.calzada_m, Jd = hip.jardin_trasero_m, a_ = acera ? hip.acera_m : 0;
    var u = ctx.uni, U = zonaRetranqueos(poly, ls, ctx.fachadas, u.retranqueo_fachada_m, u.retranqueo_linderos_m);
    var fs = frentes(ctx.pts, ctx.ccw, hip.tolerancia_frente_grados);
    fs.forEach(function (f) {
      var r = Math.max.apply(null, Array.from(f.indices).map(function (i) { return ctx.fachadas.has(i) ? u.retranqueo_fachada_m : u.retranqueo_linderos_m; }));
      f.d = Math.max(r, Jd); f.D = f.d + F + P + a_;
    });
    var notas = [], avisos = [];
    function interiorA(dist) { return limpia(poly.difference(union(fs.map(function (f) { return f.linea.buffer(dist(f), QS); })))); }
    var I1 = interiorA(function (f) { return f.D; }), I2 = interiorA(function (f) { return f.D + Cz; });
    var anillo = limpia(I1.difference(I2));
    var aceras = acera ? [limpia(interiorA(function (f) { return f.D - a_; }).difference(I1))] : [];
    var fa = fs.filter(function (f) { return Array.from(f.indices).some(function (i) { return ctx.accesos.has(i); }); })[0];
    var conector = vacio();
    if (fa) {
      var giroA = 90.0 - Math.atan2(fa.normal[1], fa.normal[0]) * 180 / Math.PI;
      var ab = rotPts([fa.a, fa.b], giroA, c), xc = ab[0][0] + accesoPos * (ab[1][0] - ab[0][0]), yeA = (ab[0][1] + ab[1][1]) / 2;
      conector = limpia(rotar(caja(xc - Cz / 2, yeA - 2.0, xc + Cz / 2, yeA + fa.D + Cz / 2), -giroA, c).intersection(poly));
    }
    var casas = [], colocadas = vacio(), plazasCol = vacio();
    fs.slice().sort(function (x, y) { return y.largo - x.largo; }).forEach(function (f) {
      var prohib = union([anillo, conector.isEmpty() ? vacio() : conector.buffer(1.0, QS), colocadas.isEmpty() ? vacio() : colocadas.buffer(sep, QS), plazasCol]);
      var zona = limpia(U.difference(prohib));
      var fe = filasEnFrente(zona, f, f.d, F, hip, sep, c);
      fe.hileras.forEach(function (h, k) {
        var grupo = [], grupos = [];
        h.forEach(function (xx) {
          var x1 = xx[0], x2 = xx[1];
          var casa = rotar(caja(x1, fe.ye + f.d, x2, fe.ye + f.d + F), -fe.giro, c);
          var plaza = rotar(caja(x1, fe.ye + f.d + F, x2, fe.ye + f.d + F + P), -fe.giro, c);
          var pin = plaza.buffer(-0.01, QS);
          var libre = plaza.intersection(poly).getArea() >= plaza.getArea() - 0.5 && plaza.intersection(anillo).getArea() < 0.5 &&
            !pin.intersects(conector) && !pin.intersects(colocadas);
          if (libre) {
            var jardin = limpia(rotar(caja(x1, fe.ye, x2, fe.ye + f.d), -fe.giro, c).intersection(poly));
            grupo.push({ casa: casa, plaza: plaza, jardin: jardin, rumbo: rumboVector(-f.normal[0], -f.normal[1]) });
          } else { grupos.push(grupo); grupo = []; }
        });
        grupos.push(grupo);
        grupos.forEach(function (g) {
          if (g.length >= hip.casas_min_hilera) {
            var hid = "P" + casas.length + "-" + k;
            g.forEach(function (x) { x.hilera = hid; });
            casas = casas.concat(g);
            colocadas = union([colocadas].concat(g.map(function (x) { return x.casa; })));
            plazasCol = union([plazasCol].concat(g.map(function (x) { return x.plaza; })));
          }
        });
      });
    });
    if (interior === "casas" && !I2.isEmpty()) {
      polys(I2).forEach(function (pi) {
        var cs = pi.getExteriorRing().getCoordinates().map(function (q) { return [q.x, q.y]; }).slice(0, -1);
        if (cs.length < 3) return;
        var ipoly = poligono(cs), iccw = J.algorithm.Orientation.isCCW(ipoly.getExteriorRing().getCoordinates());
        var fi = frentes(cs, iccw, hip.tolerancia_frente_grados), colI = vacio();
        fi.slice().sort(function (x, y) { return y.largo - x.largo; }).forEach(function (f) {
          var prohib = union(fi.filter(function (g) { return g !== f; }).map(function (g) { return g.segs.buffer(P, QS); })
            .concat(colI.isEmpty() ? [] : [colI.buffer(Math.max(sep, 2 * Jd), QS)]));
          var zona = limpia(ipoly.difference(prohib));
          var fe = filasEnFrente(zona, f, P, F, hip, sep, c);
          fe.hileras.forEach(function (h, k) {
            var hid = "I" + casas.length + "-" + k;
            h.forEach(function (xx) {
              var x1 = xx[0], x2 = xx[1];
              casas.push({ casa: rotar(caja(x1, fe.ye + P, x2, fe.ye + P + F), -fe.giro, c), plaza: rotar(caja(x1, fe.ye, x2, fe.ye + P), -fe.giro, c),
                jardin: limpia(rotar(caja(x1, fe.ye + P + F, x2, fe.ye + P + F + Jd), -fe.giro, c).intersection(ipoly)), hilera: hid,
                rumbo: rumboVector(f.normal[0], f.normal[1]) });
            });
            colI = union([colI].concat(casas.filter(function (x) { return x.hilera === hid; }).map(function (x) { return x.casa; })));
          });
        });
      });
    }
    var porCasa = Math.floor((hip.ancho_casa_m - hip.paso_peatonal_casa_m) / hip.plaza_ancho_m);
    var todas = casas.length ? union(casas.map(function (x) { return x.casa; })) : vacio();
    casas.forEach(function (x) {
      var pin = x.plaza.buffer(-0.01, QS);
      x.plazas_ok = x.plaza.intersection(poly).getArea() >= x.plaza.getArea() - 0.5 && !pin.intersects(todas) && !pin.intersects(conector);
      x.d = conector.isEmpty() ? 0 : x.casa.distance(conector);
    });
    var Emax = ctx.sup * com.edificabilidad_m2m2, vmax = Math.floor(com.viviendas_max);
    casas = casas.map(function (x, i) { x._i = i; return x; }).sort(function (a, b) { return a.d - b.d || a._i - b._i; });
    var tope = Math.min(casas.length, vmax, Math.floor(Emax / hip.sup_casa_m2)), n = tope;
    while (n > 0) {
      var cuenta = {};
      casas.slice(0, n).forEach(function (x) { cuenta[x.hilera] = (cuenta[x.hilera] || 0) + 1; });
      if (Math.min.apply(null, Object.keys(cuenta).map(function (k) { return cuenta[k]; })) >= hip.casas_min_hilera) break;
      n--;
    }
    if (n < casas.length) notas.push("Se colocan " + n + " de " + casas.length + " casas posibles (edificabilidad / nº máximo de viviendas).");
    var eleg = casas.slice(0, n), ids = {};
    eleg.forEach(function (x) { ids[x.hilera] = (ids[x.hilera] || 0) + 1; });
    var hilerasN = Object.keys(ids).sort().map(function (k) { return ids[k]; });
    var plazas = eleg.filter(function (x) { return x.plazas_ok; }).length * porCasa;
    var interiores = [];
    eleg.forEach(function (x) { if (x.hilera.charAt(0) === "I") interiores.push(x.casa, x.plaza, x.jardin); });
    var zonaComun = interiores.length ? limpia(I2.difference(union(interiores))) : I2;
    var huella = eleg.reduce(function (s, x) { return s + x.casa.getArea(); }, 0), techo = n * hip.sup_casa_m2;
    var necesarias = Math.floor(com.plazas_por_vivienda) * n, zc = zonaComun.isEmpty() ? 0 : zonaComun.getArea();
    var chk = { hay_viviendas: n > 0, viviendas: n <= vmax, techo: techo <= Emax + 0.5, plazas: plazas >= necesarias,
      ocupacion_A: 100 * huella / ctx.sup <= u.ocupacion_pct + 1e-6, fondo_saco_SI5: !anillo.isEmpty(), itinerario_peatonal: itinerario,
      zona_comun: zc >= hip.zona_comun_min_m2 };
    if (!chk.plazas) avisos.push("Faltan " + (necesarias - plazas) + " plazas.");
    if (!chk.fondo_saco_SI5) avisos.push("No se forma el anillo de calle: revisar el fondo de saco (DB-SI SI 5).");
    if (!chk.itinerario_peatonal) avisos.push("Calle interior sin acera: itinerario peatonal por la calzada (DB-SUA 9, revisar).");
    if (!chk.zona_comun) avisos.push("Zona común de " + Math.round(zc) + " m², menor que el mínimo de " + Math.round(hip.zona_comun_min_m2) + " m².");
    notas.push("Zona común: " + Math.round(zc) + " m². Calle interior en anillo con un acceso.");
    if (hilerasN.length) notas.push("Hileras: " + hilerasN.join(" + ") + " casas.");
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    var ok = Object.keys(chk).every(function (k) { return chk[k]; });
    var viarioP = [anillo, conector].filter(function (g) { return !g.isEmpty(); }).concat(aceras.filter(function (g) { return !g.isEmpty(); }));
    var indP = indicadores(n, eleg.map(function (x) { return x.rumbo; }), viarioP.length ? union(viarioP).getArea() : 0, hip);
    return {
      estrategia: "perimetral", angulo_hileras: -1.0, pct_zona_unifamiliar: 100, unifamiliar_en: "perímetro", uni_en_marco: "abajo",
      remate: "anillo", acera: aceraIn, acceso_pos: accesoPos, interior: interior,
      casas: n, pisos: 0, viviendas: n, bloques: 0, plantas_bloque: 0, plantas_casa: Math.floor(u.plantas_max), portales: 0,
      pisos_por_planta: 0, mix_pisos: {}, tipos_pisos_planta: [], plazas_accesibles: 0,
      techo_m2: r1(techo), aprovechamiento_pct: r1(100 * techo / Emax), plazas: plazas, plazas_necesarias: necesarias,
      plazas_casas: plazas, plazas_bolsa: 0, huella_m2: r1(huella), ocupacion_A_uni_pct: r1(100 * huella / ctx.sup),
      ocupacion_A_multi_pct: 0, ocupacion_B_pct: r1(100 * huella / ctx.sup), fondo_saco_m: 0, zona_comun_m2: r1(zc),
      comprobaciones: chk, cumple: ok, techo_casas_m2: r1(techo), techo_pisos_m2: 0,
      economia: cuentaResultados(ctx.economia, techo, 0, plazas, ctx.sup, huella),
      jardines_a_sur_pct: indP.jardines_a_sur_pct, orientacion_jardines: indP.orientacion_jardines, viario_m2: indP.viario_m2,
      viario_m2_por_vivienda: indP.viario_m2_por_vivienda, zona_comun_programa_m2: indP.zona_comun_programa_m2, zona_comun_programa: indP.zona_comun_programa,
      avisos: avisos, notas: notas, hileras: hilerasN,
      geo: { parcela: poly, zona_uni: poly, zona_multi: vacio(), edif_uni: U, edif_multi: vacio(),
        casas: eleg.map(function (x) { return x.casa; }), plazas_casas: eleg.filter(function (x) { return x.plazas_ok; }).map(function (x) { return x.plaza; }),
        calzadas: [anillo, conector].filter(function (g) { return !g.isEmpty(); }), bolsas: [], bloques: [],
        aceras: aceras.filter(function (g) { return !g.isEmpty(); }), pisos: [], nucleos: [], accesibles: [],
        jardines: eleg.filter(function (x) { return !x.jardin.isEmpty(); }).map(function (x) { return x.jardin; }), zona_comun: zonaComun, corte: null }
    };
  }

  // ------------------------------------------------------------------ barrido
  function angulos(ctx) {
    var a = ctx.barrido.angulo_hileras;
    if (a === "fachadas") {
      var ls = lados(ctx.pts, ctx.ccw), s = {};
      ls.forEach(function (l) { if (ctx.fachadas.has(l.indice)) s[Math.round((((l.angulo % 180) + 180) % 180) * 100) / 100] = 1; });
      return Object.keys(s).map(Number).sort(function (x, y) { return x - y; });
    }
    return a.map(Number);
  }
  function combinaciones(ctx) {
    var b = ctx.barrido, out = [], prod = b.producto || "todo";
    var pcts = prod === "adosadas" ? [100] : prod === "bloques" ? [0]
      : prod === "mezcla" ? b.pct_zona_unifamiliar.filter(function (x) { return x > 0 && x < 100; }) : b.pct_zona_unifamiliar;
    var angs = angulos(ctx);
    if (prod === "bloques") {
      var st = {}; angs.forEach(function (a) { st[a] = 1; st[Math.round(((a + 90) % 180) * 100) / 100] = 1; });
      angs = Object.keys(st).map(Number).sort(function (x, y) { return x - y; });
    }
    if (b.estrategias.indexOf("calles_paralelas") >= 0) angs.forEach(function (ang) {
      pcts.forEach(function (pct) {
        b.unifamiliar_en.forEach(function (ue) {
          b.remate.forEach(function (rem) {
            b.acera.forEach(function (ac) {
              if ((pct === 0 || pct === 100) && ue !== b.unifamiliar_en[0]) return;
              if (pct <= 0 && (rem !== b.remate[0] || ac !== b.acera[0])) return;
              out.push({ estrategia: "calles_paralelas", ang: ang, pct: pct, uni_en: ue, remate: rem, acera: ac });
            });
          });
        });
      });
    });
    if (b.estrategias.indexOf("perimetral") >= 0 && (prod === "todo" || prod === "adosadas")) b.acceso_pos.forEach(function (pos) {
      b.interior.forEach(function (inter) {
        b.acera.forEach(function (ac) { out.push({ estrategia: "perimetral", acceso_pos: pos, interior: inter, acera: ac }); });
      });
    });
    return out;
  }
  function calcular(ctx, p) {
    return p.estrategia === "perimetral" ? variantePerimetral(ctx, p.acceso_pos, p.interior, p.acera) : variante(ctx, p);
  }
  function claveDup(r, p) {
    return p.estrategia === "perimetral"
      ? ["perimetral", p.acera, r.casas, r.plazas, Math.round(r.zona_comun_m2), Math.round(r.huella_m2)].join("|")
      : [r.angulo_hileras, p.pct, r.unifamiliar_en, r.remate, p.acera, r.casas, r.pisos, r.plazas].join("|");
  }
  var OBJETIVOS = {
    viviendas: function (r) { return [-r.viviendas, -r.techo_m2]; }, techo: function (r) { return [-r.techo_m2, -r.viviendas]; },
    casas: function (r) { return [-r.casas, -r.viviendas]; }, ocupacion: function (r) { return [r.ocupacion_B_pct, -r.viviendas]; },
    beneficio: function (r) { return [-(r.economia.beneficio_eur !== undefined ? r.economia.beneficio_eur : -1e18), -r.viviendas]; },
    orientacion: function (r) { return [-r.jardines_a_sur_pct, -r.viviendas]; },
    viario: function (r) { return [r.viviendas ? r.viario_m2_por_vivienda : 1e9, -r.viviendas]; }
  };
  function ordenar(rs, objetivo) {
    function fallos(r) { return Object.keys(r.comprobaciones).filter(function (k) { return !r.comprobaciones[k]; }).length; }
    var key = (!objetivo || objetivo === "ranking")
      ? function (r) { return [r.cumple ? 0 : 1, fallos(r), -r.viviendas, -r.techo_m2, -((r.plazas - r.plazas_necesarias >= 0) ? 1 : 0), r.ocupacion_B_pct]; }
      : function (r) { return [r.cumple ? 0 : 1].concat(OBJETIVOS[objetivo](r)); };
    rs.forEach(function (r, i) { r._k = key(r); r._i = i; });
    rs.sort(function (a, b) {
      for (var i = 0; i < a._k.length; i++) if (a._k[i] !== b._k[i]) return a._k[i] - b._k[i];
      return a._i - b._i;
    });
    rs.forEach(function (r, i) { r.id = "V" + String(i + 1).padStart(3, "0"); });
    return rs;
  }
  function barrer(ctx, onProgreso, objetivo) {
    var comb = combinaciones(ctx), res = [], vistos = {};
    comb.forEach(function (p, i) {
      var r = calcular(ctx, p);
      var clave = claveDup(r, p);
      if (!vistos[clave]) { vistos[clave] = 1; r.params = p; res.push(r); }
      if (onProgreso) onProgreso(i + 1, comb.length);
    });
    return ordenar(res, objetivo);
  }

  // ------------------------------------------------------------------ ayudas del visor
  // (no intervienen en el cálculo: sirven para arrastrar la línea de reparto)
  function aMarco(ctx, ang, x, y) { return rotPts([[x, y]], -ang, ctx.centro)[0]; }
  function pctDesdePunto(ctx, ang, uniEn, x, y) {
    var pts = rotPts(ctx.pts, -ang, ctx.centro), poly = poligono(pts), b = lim(poly);
    var yr = Math.max(b[1], Math.min(b[3], aMarco(ctx, ang, x, y)[1]));
    var abajo = poly.intersection(caja(b[0] - 1, b[1] - 1, b[2] + 1, yr)).getArea() / poly.getArea();
    return 100 * (uniEn === "abajo" ? abajo : 1 - abajo);
  }
  function lineaCorte(ctx, ang, x, y) {
    var pts = rotPts(ctx.pts, -ang, ctx.centro), poly = poligono(pts), b = lim(poly);
    var yr = Math.max(b[1], Math.min(b[3], aMarco(ctx, ang, x, y)[1]));
    var l = linea([b[0] - 1, yr], [b[2] + 1, yr]).intersection(poly);
    return rotar(l, ang, ctx.centro);
  }

  root.Motor = {
    pctDesdePunto: pctDesdePunto, lineaCorte: lineaCorte, calcular: calcular, claveDup: claveDup, variantePerimetral: variantePerimetral,
    HIPOTESIS_DEFECTO: HIPOTESIS_DEFECTO, BARRIDO_DEFECTO: BARRIDO_DEFECTO, FALTA: FALTA,
    cargar: cargar, variante: variante, barrer: barrer, combinaciones: combinaciones, ordenar: ordenar,
    angulos: angulos, lados: lados, polys: polys, lim: lim
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
