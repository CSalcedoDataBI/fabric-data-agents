[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](08-lifecycle-and-sunset.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](08-lifecycle-and-sunset.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 08 · Ciclo de vida y la caducidad 2026

## Qué es

Un agente no se entrega una vez; se **mantiene** — y una de sus dependencias tiene una fecha de
caducidad dura. Dos piezas móviles definen su ciclo de vida:

- **Runtime.** Todo Data Agent corre sobre un runtime que lleva su lógica de orquestación, ruteo y
  generación de consultas. **Standard** es el runtime GA (estable, actualizaciones infrecuentes);
  **Preview** es donde aterriza el nuevo comportamiento de ruteo/generación antes de graduarse. La
  elección de runtime **no** cambia qué LLM usa el agente — las mejoras de modelo aplican a ambos.
- **La superficie de consumo**, donde vive la fecha límite. Históricamente, los clientes externos
  consumían un Data Agent publicado a través de la **OpenAI Assistants API** (`beta.assistants`,
  `beta.threads`, `beta.threads.runs`). **OpenAI retira la Assistants API el 2026-08-26.** El código
  construido sobre ella sigue funcionando hasta esa fecha y se detiene después.

## Por qué importa — la ventaja evergreen

Esta es la sección que caduca más rápido, que es exactamente por qué se gana su lugar en una
referencia pensada para ser citada: **la fecha límite es real, fechada, y la mayoría del material la
ignora.**

- **Qué se rompe:** cualquier cosa que consuma un Data Agent con el patrón de Assistants API — los
  ejemplos más viejos de cliente externo y de notebook que llaman a `beta.threads.runs`.
- **Qué *no* se rompe:** el Data Agent en sí, sus fuentes, sus instrucciones, su endpoint publicado. El
  agente está bien; lo que caduca es el *protocolo de cliente*.
- **Los destinos de migración:**
  - **MCP endpoint** — el reemplazo recomendado por Microsoft para el consumo programático (el Data
    Agent expuesto como servidor Model Context Protocol). Este es el camino evergreen.
  - **Foundry Agent Service** — consume el agente como un `FabricTool` bajo identidad On-Behalf-Of,
    para escenarios orquestados/multi-agente ([06](06-direct-vs-orchestrator.es.md)).
  - **Responses API** — donde estabas usando la OpenAI Assistants API directamente, su sucesor para
    flujos con estado y llamadas a herramientas.

Nombrar la fecha y las salidas convierte una caída latente en una migración planeada — la diferencia
entre una referencia y un post de blog que se pudre.

## Cómo escribirla bien

- **Fecha cada afirmación sensible a versión.** "A 2026, las fuentes Graph y Ontología son preview"
  envejece con gracia; "Graph es preview" no.
- **Elige el runtime Standard para producción**, Preview solo para probar comportamiento por venir — y
  fija de cuál dependes, para que un cambio de ruteo no te sorprenda.
- **Audita ya el código de consumo buscando la Assistants API.** Si algún cliente llama a
  `beta.assistants` / `beta.threads`, tiene caducidad 2026-08-26; agenda la migración a MCP / Foundry /
  Responses antes de esa fecha, no después.
- **Re-corre tu conjunto de evaluación tras cualquier cambio de runtime, modelo o migración** — los
  eventos de ciclo de vida son precisamente cuando aparecen las regresiones silenciosas de precisión.
- **Mantén la config en Git** ([07](07-provisioning.es.md)) para que una migración sea un diff
  revisable con rollback, no una reconstrucción.

## Anti-patrón

**Construir el consumo sobre la Assistants API en 2026 sin plan de migración** — enviar directo a una
superficie con fecha de apagado publicada. **Afirmaciones de versión sin fecha** que se vuelven falsas
calladamente conforme las funciones preview se gradúan y las fechas pasan. **Vivir en el runtime
Preview en producción**, y luego sorprenderse cuando el comportamiento de ruteo cambia bajo tus pies.
Y **migrar el cliente sin re-validar respuestas**, asumiendo que cambiar de protocolo es neutral al
comportamiento cuando un cambio de ciclo de vida es el momento más probable de que la calidad se mueva.

## El ejemplo Contoso

Las [instrucciones](../../examples/contoso-vendor-spend/instructions.md) de Contoso cierran con una
**nota de ciclo de vida** explícita en vez de dejar la fecha límite implícita:

> Si este agente se consume programáticamente a través de la OpenAI Assistants API, esa superficie
> **cierra el 2026-08-26** — migra a la Responses API / Azure AI Foundry OBO.

Las partes *autoradas* del agente — identidad, fuentes, instrucciones, glosario — son independientes
del protocolo y siguen adelante intactas; solo el cliente de consumo tiene fecha. Ese es el punto
entero de construir bien la anatomía: cuando la superficie cambia, re-apuntas el cliente al MCP
endpoint o a Foundry y el agente sigue respondiendo. Todo lo que lo hizo *correcto* sobrevive a la API
que casualmente cargó sus respuestas.

---
_Esta es la última sección. Vuelve al [Índice](../../README.es.md) · ve el ejemplo completo
[Contoso Vendor Spend](../../examples/contoso-vendor-spend/README.es.md)._
