// Cliente de la API de Claude (SDK oficial de Anthropic) ejecutado en el navegador.
// La clave de API la introduce el usuario y solo se guarda en su navegador.
import Anthropic from "https://cdn.jsdelivr.net/npm/@anthropic-ai/sdk@1.3.0/+esm";

export const MODELO = "claude-opus-5-5";

// Búsqueda web restringida a fuentes oficiales para contrastar la vigencia de la normativa.
const BUSQUEDA_OFICIAL = {
  type: "web_search_20260209",
  name: "web_search",
  max_uses: 6,
  allowed_domains: ["boe.es", "codigotecnico.org", "mivau.gob.es", "idae.es"],
};

function cliente(apiKey) {
  return new Anthropic({ apiKey, dangerouslyAllowBrowser: true });
}

/**
 * Genera texto en streaming.
 * @param {object} o
 * @param {string} o.apiKey
 * @param {string} o.system      instrucciones estables (se cachean)
 * @param {string} o.contexto    datos del proyecto (se cachean entre apartados)
 * @param {Array}  o.mensajes    [{role, content}] mensajes posteriores
 * @param {boolean} o.busqueda   habilita búsqueda web en fuentes oficiales
 * @param {string} o.esfuerzo    low | medium | high | xhigh | max
 * @param {(t:string)=>void} o.onTexto  recibe cada fragmento de texto
 * @param {AbortSignal} o.signal
 * @returns {Promise<{texto:string, fuentes:Array<{url:string,title:string}>}>}
 */
export async function generar({ apiKey, system, contexto, mensajes, busqueda, esfuerzo = "high", onTexto, signal }) {
  const client = cliente(apiKey);
  const historial = [
    {
      role: "user",
      content: [
        { type: "text", text: contexto, cache_control: { type: "ephemeral" } },
        ...(typeof mensajes[0].content === "string" ? [{ type: "text", text: mensajes[0].content }] : mensajes[0].content),
      ],
    },
    ...mensajes.slice(1),
  ];

  let texto = "";
  const fuentes = new Map();

  // Los turnos con herramientas de servidor pueden pausarse (pause_turn): se reanudan.
  for (let intento = 0; intento < 4; intento++) {
    const stream = client.beta.messages.stream(
      {
        model: MODELO,
        max_tokens: 64000,
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default",
        thinking: { type: "adaptive" },
        output_config: { effort: esfuerzo },
        system: [{ type: "text", text: system, cache_control: { type: "ephemeral" } }],
        tools: busqueda ? [BUSQUEDA_OFICIAL] : undefined,
        messages: historial,
      },
      { signal },
    );

    for await (const ev of stream) {
      if (ev.type === "content_block_delta" && ev.delta.type === "text_delta") {
        texto += ev.delta.text;
        onTexto?.(ev.delta.text);
      }
    }
    const final = await stream.finalMessage();

    for (const b of final.content) {
      if (b.type === "web_search_tool_result" && Array.isArray(b.content)) {
        for (const r of b.content) if (r.url) fuentes.set(r.url, { url: r.url, title: r.title || r.url });
      }
    }

    if (final.stop_reason === "refusal") {
      throw new Error("La solicitud fue rechazada por el modelo. Reformule el contenido o revise los datos introducidos.");
    }
    if (final.stop_reason === "pause_turn") {
      historial.push({ role: "assistant", content: final.content });
      continue;
    }
    if (final.stop_reason === "max_tokens") {
      const aviso = "\n\n> [El texto se ha cortado por longitud. Genere de nuevo el apartado con indicaciones más concretas.]";
      texto += aviso;
      onTexto?.(aviso);
    }
    break;
  }
  return { texto, fuentes: [...fuentes.values()] };
}

export function describirError(e) {
  if (e?.name === "AbortError" || e instanceof Anthropic.APIUserAbortError) return "Generación cancelada.";
  if (e instanceof Anthropic.AuthenticationError) return "Clave de API no válida. Revísela en Ajustes.";
  if (e instanceof Anthropic.PermissionDeniedError) return "La clave de API no tiene permisos para este modelo o función.";
  if (e instanceof Anthropic.RateLimitError) return "Límite de uso alcanzado. Espere unos segundos e inténtelo de nuevo.";
  if (e instanceof Anthropic.BadRequestError) return `Solicitud no válida: ${e.message}`;
  if (e instanceof Anthropic.APIError && e.status) return `Error del servicio (${e.status}): ${e.message}`;
  if (e instanceof Anthropic.APIConnectionError) return "No se pudo conectar con la API. Compruebe su conexión.";
  return e?.message || String(e);
}
