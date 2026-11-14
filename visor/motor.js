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

  var HIPOTESIS_DEFECTO = {
    fondo_casa_m: 12.0, ancho_casa_m: 6.5, sup_casa_m2: 156.0, casas_min_hilera: 3, casas_max_hilera: 8,
    jardin_trasero_m: 6.0, fondo_bloque_m: 12.0, longitud_min_bloque_m: 15.0, longitud_max_bloque_m: 40.0,
    sup_piso_m2: 135.0, altura_planta_m: 3.0, calzada_m: 6.0, plaza_ancho_m: 2.5, plaza_fondo_m: 5.0,
    paso_peatonal_casa_m: 1.5, acera_m: 1.5, martillo_largo_m: 12.0, fondo_saco_max_m: 20.0,
    distancia_aparcamiento_edificio_m: 2.0, aparcamiento_fuera_retranqueo: true,
    paso_rejilla_m: 0.5, paso_fase_m: 2.0
  };
  var BARRIDO_DEFECTO = {
    angulo_hileras: "fachadas",
    pct_zona_unifamiliar: [0, 30, 40, 50, 60, 70, 80, 100],
    unifamiliar_en: ["abajo", "arriba"],
    remate: ["fondo_saco", "martillo", "lazo"],
    acera: [false, true]
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
      if (a > mejorA) { mejor = rects; mejorA = a; }
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
    return { nombre: cfg.nombre || "parcela", pts: pts, poly: poly, sup: sup, f_sup: sup / poly.getArea(), ccw: ccw,
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
  function variante(ctx, p) {
    var ang = p.ang, pct = p.pct, uniEn = p.uni_en, remate = p.remate, acera = !!p.acera;
    var hip = ctx.hip, com = ctx.comun, sep = +com.separacion_edificios_m, c = ctx.centro;
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
          lista.push({ casa: casa, plazas: toca ? null : b });
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

    // 3. Reparto
    var Emax = ctx.sup * com.edificabilidad_m2m2, vmax = Math.floor(com.viviendas_max);
    var plM = Math.floor(ctx.multi.plantas_max);
    if ("altura_max_m" in ctx.multi) plM = Math.min(plM, Math.floor(ctx.multi.altura_max_m / hip.altura_planta_m + 1e-9));
    var cand = [];
    if (!M.isEmpty()) {
      cand = bloquesLineales0(M, hip.fondo_bloque_m, sep, hip.longitud_min_bloque_m, hip.longitud_max_bloque_m, hip.paso_rejilla_m);
      cand.sort(function (a, b) { var ya = (a[1] + a[3]) / 2, yb = (b[1] + b[3]) / 2; return ya - yb || ((a[0] + a[2]) / 2 - (b[0] + b[2]) / 2); });
    }
    var huellaMaxM = Zm.isEmpty() ? 0 : ctx.multi.ocupacion_pct / 100 * Zm.getArea() * ctx.f_sup;
    function colocarBloques(pisosObj) {
      var bl = [];
      if (!pisosObj || !cand.length) return [bl, 0];
      var falta = Math.min(pisosObj * hip.sup_piso_m2 / plM, huellaMaxM);
      for (var i = 0; i < cand.length; i++) {
        if (falta <= 1) break;
        var b = cand[i], fondo = b[3] - b[1];
        var largo = Math.min(b[2] - b[0], Math.ceil(falta / fondo / 0.5) * 0.5);
        if (largo < hip.longitud_min_bloque_m) largo = (b[2] - b[0]) >= hip.longitud_min_bloque_m ? hip.longitud_min_bloque_m : 0;
        if (largo <= 0) continue;
        bl.push([b[0], b[1], b[0] + largo, b[3]]);
        falta -= largo * fondo;
      }
      var cap = bl.reduce(function (s, r) { return s + areaR(r); }, 0) * plM;
      return [bl, Math.min(pisosObj, Math.floor(cap / hip.sup_piso_m2 + 1e-6))];
    }
    var tope = Math.min(lista.length, vmax, Math.floor(Emax / hip.sup_casa_m2)), best = null;
    for (var nn = tope; nn > Math.max(-1, tope - 16); nn--) {
      var pObj = Math.max(0, Math.min(vmax - nn, Math.floor((Emax - nn * hip.sup_casa_m2) / hip.sup_piso_m2)));
      var cb = colocarBloques(pObj);
      var clave = [nn + cb[1], nn * hip.sup_casa_m2 + cb[1] * hip.sup_piso_m2];
      if (!best || clave[0] > best.clave[0] || (clave[0] === best.clave[0] && clave[1] > best.clave[1]))
        best = { clave: clave, n: nn, bl: cb[0], np: cb[1], pObj: pObj };
    }
    var nCasas = best.n, bloques = best.bl, nPisos = best.np;
    if (nCasas < lista.length) notas.push("Se colocan " + nCasas + " de " + lista.length + " casas posibles para maximizar viviendas y techo.");
    if (best.pObj && nPisos < best.pObj) notas.push("La zona multifamiliar solo admite " + nPisos + " de " + best.pObj + " pisos.");
    var casas = lista.slice(0, nCasas).map(function (x) { return x.casa; });
    var plazasU = lista.slice(0, nCasas).filter(function (x) { return x.plazas; }).map(function (x) { return x.plazas; });
    var nPlazasU = plazasU.length * porCasa, techoU = nCasas * hip.sup_casa_m2;
    var hilerasN = recuentoHileras(casas);

    // Bolsa
    var viv = nCasas + nPisos, necesarias = Math.floor(com.plazas_por_vivienda) * viv;
    var faltaPl = Math.max(0, necesarias - nPlazasU), bolsas = [], vialesBolsa = [], nBolsa = 0, largoBolsa = 0;
    if (faltaPl) {
      var P = hip.plaza_fondo_m, W = 2 * P + Cz;
      var ocupado = union(casas.map(R).concat(bloques.map(R), plazasU.map(R), mods.map(function (m) { return m.calzada; }), remates, aceras.map(R)));
      var da = hip.distancia_aparcamiento_edificio_m;
      var base = hip.aparcamiento_fuera_retranqueo ? (!M.isEmpty() ? M : U) : (!Zm.isEmpty() ? Zm : Zu);
      var libre = limpia(base.intersection(poly).difference(ocupado.isEmpty() ? vacio() : ocupado.buffer(da, QS)));
      if (corteG && !Zm.isEmpty()) libre = limpia(libre.difference(corteG));
      var bl2 = libre.isEmpty() ? [0, 0, 0, 0] : lim(libre), y = bl2[1], pa = hip.plaza_ancho_m;
      var dmaxAcc = Math.max(ctx.uni.retranqueo_fachada_m, ctx.multi.retranqueo_fachada_m, ctx.uni.retranqueo_linderos_m, ctx.multi.retranqueo_linderos_m) + 3.0;
      var accCx = acc.getCentroid().getX();
      while (faltaPl > 0 && !libre.isEmpty() && y + W <= bl2[3]) {
        var trs = tramosEnFranja(libre, bl2[0], bl2[2], y, W, 0.0, 2 * pa, null, hip.paso_rejilla_m)
          .map(function (r) { return { r: r, d: R(r).distance(acc) }; })
          .sort(function (a, b) { return a.d - b.d; });
        var usado = false;
        for (var q = 0; q < trs.length; q++) {
          if (trs[q].d > dmaxAcc) continue;
          var r = trs[q].r, x1 = r[0], y1 = r[1], x2 = r[2], y2 = r[3];
          var nMax = 2 * Math.floor((x2 - x1) / pa);
          var nb = Math.min(nMax, faltaPl + (faltaPl % 2));
          var largo = Math.ceil(nb / 2) * pa;
          var cercaIzq = Math.abs(x1 - accCx) < Math.abs(x2 - accCx);
          var rr = cercaIzq ? [x1, y1, x1 + largo, y2] : [x2 - largo, y1, x2, y2];
          bolsas.push(rr);
          var vx1 = cercaIzq ? bp[0] - 1 : rr[2], vx2 = cercaIzq ? rr[0] : bp[2] + 1;
          var vial = piezaQueToca(poly.intersection(caja(vx1, y1 + P, vx2, y1 + P + Cz)), acc);
          if (vial) vialesBolsa.push(vial);
          nBolsa += nb;
          largoBolsa = Math.max(largoBolsa, largo + (vial ? vial.getLength() / 2 - Cz : 0));
          faltaPl -= nb;
          usado = true;
          if (faltaPl <= 0) break;
        }
        y += usado ? W : 1.0;
      }
    }

    // 4. Comprobaciones
    var huellaU = casas.reduce(function (s, r) { return s + areaR(r); }, 0);
    var huellaM = bloques.reduce(function (s, r) { return s + areaR(r); }, 0);
    var techo = techoU + nPisos * hip.sup_piso_m2, plazas = nPlazasU + nBolsa;
    var ocAu = Zu.isEmpty() ? 0 : 100 * huellaU / (Zu.getArea() * ctx.f_sup);
    var ocAm = Zm.isEmpty() ? 0 : 100 * huellaM / (Zm.getArea() * ctx.f_sup);
    var ocB = 100 * (huellaU + huellaM) / ctx.sup;
    var fondoSaco = Math.max.apply(null, mods.map(function (m) { return m.largo; }).concat([0]));
    var chk = {
      hay_viviendas: viv > 0, viviendas: viv <= vmax, techo: techo <= Emax + 0.5, plazas: plazas >= necesarias,
      ocupacion_A: ocAu <= ctx.uni.ocupacion_pct + 1e-6 && ocAm <= ctx.multi.ocupacion_pct + 1e-6,
      fondo_saco_SI5: fondoSaco <= hip.fondo_saco_max_m + 1e-6, itinerario_peatonal: acera || !mods.length
    };
    if (!chk.plazas) avisos.push("Faltan " + (necesarias - plazas) + " plazas.");
    if (!chk.fondo_saco_SI5) avisos.push("Calle sin salida de " + Math.round(fondoSaco) + " m sin espacio de maniobra (DB-SI SI 5, revisar).");
    if (!chk.itinerario_peatonal) avisos.push("Calle de casas sin acera: itinerario peatonal por la calzada (DB-SUA 9, revisar).");
    if (largoBolsa > hip.fondo_saco_max_m) notas.push("La bolsa de aparcamiento es un fondo de saco de ≈ " + Math.round(largoBolsa) + " m (revisar).");
    if (hilerasN.length) notas.push("Hileras: " + hilerasN.join(" + ") + " casas.");

    function back(g) { return rotar(g, ang, c); }
    var geo = {
      parcela: back(poly), zona_uni: back(Zu), zona_multi: back(Zm), edif_uni: back(U), edif_multi: back(M),
      casas: casas.map(function (r) { return back(R(r)); }), plazas_casas: plazasU.map(function (r) { return back(R(r)); }),
      calzadas: mods.map(function (m) { return back(m.calzada); }).concat(remates.map(back), vialesBolsa.map(back)),
      bolsas: bolsas.map(function (r) { return back(R(r)); }), bloques: bloques.map(function (r) { return back(R(r)); }),
      aceras: aceras.map(function (r) { return back(R(r)); }),
      corte: corteG ? back(linea([bp[0] - 1, yc], [bp[2] + 1, yc]).intersection(poly)) : null
    };
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    var ok = Object.keys(chk).every(function (k) { return chk[k]; });
    return {
      angulo_hileras: r1(((ang % 180) + 180) % 180), pct_zona_unifamiliar: pct,
      unifamiliar_en: (pct > 0 && pct < 100) ? ladoTxt(ang, uniEn) : (pct >= 100 ? "todo" : "—"),
      uni_en_marco: uniEn, remate: remate, acera: acera,
      casas: nCasas, pisos: nPisos, viviendas: viv, bloques: bloques.length, plantas_bloque: plM,
      plantas_casa: Math.floor(ctx.uni.plantas_max),
      techo_m2: r1(techo), aprovechamiento_pct: r1(100 * techo / Emax), plazas: plazas, plazas_necesarias: necesarias,
      plazas_casas: nPlazasU, plazas_bolsa: nBolsa, huella_m2: r1(huellaU + huellaM),
      ocupacion_A_uni_pct: r1(ocAu), ocupacion_A_multi_pct: r1(ocAm), ocupacion_B_pct: r1(ocB),
      fondo_saco_m: r1(fondoSaco), comprobaciones: chk, cumple: ok, avisos: avisos, notas: notas, hileras: hilerasN,
      geo: geo
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
    var b = ctx.barrido, out = [];
    angulos(ctx).forEach(function (ang) {
      b.pct_zona_unifamiliar.forEach(function (pct) {
        b.unifamiliar_en.forEach(function (ue) {
          b.remate.forEach(function (rem) {
            b.acera.forEach(function (ac) {
              if ((pct === 0 || pct === 100) && ue !== b.unifamiliar_en[0]) return;
              if (pct <= 0 && (rem !== b.remate[0] || ac !== b.acera[0])) return;
              out.push({ ang: ang, pct: pct, uni_en: ue, remate: rem, acera: ac });
            });
          });
        });
      });
    });
    return out;
  }
  function ordenar(rs) {
    function suma(r) { return Object.keys(r.comprobaciones).filter(function (k) { return r.comprobaciones[k]; }).length; }
    var key = function (r) { return [r.cumple ? 0 : 1, -suma(r), -r.viviendas, -r.techo_m2, -((r.plazas - r.plazas_necesarias >= 0) ? 1 : 0), r.ocupacion_B_pct]; };
    rs.forEach(function (r, i) { r._k = key(r); r._i = i; });
    rs.sort(function (a, b) {
      for (var i = 0; i < a._k.length; i++) if (a._k[i] !== b._k[i]) return a._k[i] - b._k[i];
      return a._i - b._i;
    });
    rs.forEach(function (r, i) { r.id = "V" + String(i + 1).padStart(3, "0"); });
    return rs;
  }
  function barrer(ctx, onProgreso) {
    var comb = combinaciones(ctx), res = [], vistos = {};
    comb.forEach(function (p, i) {
      var r = variante(ctx, p);
      var clave = [r.angulo_hileras, p.pct, r.unifamiliar_en, r.remate, p.acera, r.casas, r.pisos, r.plazas].join("|");
      if (!vistos[clave]) { vistos[clave] = 1; r.params = p; res.push(r); }
      if (onProgreso) onProgreso(i + 1, comb.length);
    });
    return ordenar(res);
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
    pctDesdePunto: pctDesdePunto, lineaCorte: lineaCorte,
    HIPOTESIS_DEFECTO: HIPOTESIS_DEFECTO, BARRIDO_DEFECTO: BARRIDO_DEFECTO, FALTA: FALTA,
    cargar: cargar, variante: variante, barrer: barrer, combinaciones: combinaciones, ordenar: ordenar,
    angulos: angulos, lados: lados, polys: polys, lim: lim
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
