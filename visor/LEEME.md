# Visor de tanteo (herramienta interna)

Página web interactiva para explorar ordenaciones de una parcela, al estilo de Hektar, con las reglas fijas del estudio.

- `index.html`: la interfaz (planta, axonometría, cifras, banco de variantes y comparación).
- `motor.js`: el motor de cálculo en JavaScript. Es una traducción de `scripts/variantes_generador.py`.
- `prueba_paridad.js`: compara el motor JavaScript con el de Python, variante a variante.

## Cómo comprobar que el visor y los scripts coinciden

```bash
python3 scripts/variantes_generador.py planos/variantes/entrada_UA-03-01.json
node visor/prueba_paridad.js <ruta a jsts.min.js> planos/variantes/entrada_UA-03-01.json planos/variantes/UA-03-01_Los_Pocillos/ranking.json
```

Para obtener `jsts.min.js`: `npm install jsts@2.11.3` (está en `node_modules/jsts/dist/`).
Último resultado: **134/134 variantes iguales y el mismo ranking**.

## Del visor al DXF

El botón «Copiar orden para DXF» copia una orden como esta:

```bash
python3 scripts/variantes_generador.py planos/variantes/entrada_UA-03-01.json --parametros '{"ang":0.47,"pct":50,...}'
```

La orden escribe `visor.dxf` y `visor.svg` en `planos/variantes/<parcela>/`. El DXF se calcula con el motor de Python, que es la referencia.

## Datos

- La parcela UA-03-01 va incluida en la página, tomada de `planos/variantes/entrada_UA-03-01.json`. Si cambia ese archivo, hay que volver a incluirla y publicar de nuevo.
- Se puede cargar otra parcela pegando su JSON de entrada en el propio visor.
- Las hipótesis de diseño se pueden cambiar en el visor. Los datos urbanísticos solo se cambian cargando otro JSON.

PENDIENTE DE VALIDAR POR EL ARQUITECTO
