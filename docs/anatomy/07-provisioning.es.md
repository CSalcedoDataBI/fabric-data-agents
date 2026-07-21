[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](07-provisioning.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](07-provisioning.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 07 · Aprovisionamiento

## Qué es

El aprovisionamiento es cómo el agente se **crea, configura, versiona y publica** — la costura
operativa alrededor del contenido que autoran las secciones anteriores. Hay tres superficies:

- **Portal** — la UI de autoría en Fabric. Lo mejor para diseño e iteración: añadir fuentes, elegir
  tablas, escribir instrucciones, probar, publicar.
- **Config-as-code (integración con Git)** — la configuración del agente serializada a archivos, para
  que viva en control de código y se mueva por el ALM como cualquier ítem de Fabric.
- **SDK / REST** — el Fabric Data Agent Python SDK (`fabric-data-agent-sdk`) para construir, evaluar y
  automatizar agentes en notebooks, más REST para pipelines de CI/CD.

Los prerrequisitos son los mismos en las tres: una **capacidad de pago F2+** (o Power BI Premium P1+
con Fabric habilitado), los tenant settings de **cross-geo processing/storing for AI** habilitados, y
**Read** sobre al menos una fuente de datos.

## Por qué importa

El portal es donde un agente *nace*, pero config-as-code es donde se vuelve un **producto
mantenible**. Serializar la configuración convierte al agente en un artefacto revisable, diffeable y
desplegable — la diferencia entre "alguien armó esto a clics en prod" y "este cambio pasó por un PR".
El layout de Git hace que la revisión sea significativa porque mapea uno-a-uno con la anatomía:

| Archivo / carpeta | Contiene | Sección de anatomía |
|---|---|---|
| `stage_config.json` → `aiInstructions` | Instrucciones a nivel agente | [01](01-identity-and-role.es.md) · [03](03-agent-instructions.es.md) |
| `<fuente>/datasource.json` | `dataSourceInstructions`, `displayName`, `elements` (mapa de esquema) | [02](02-data-sources.es.md) · [04](04-source-instructions-and-fewshots.es.md) |
| `<fuente>/fewshots.json` | Pares de consulta de ejemplo (fuentes SQL/KQL) | [04](04-source-instructions-and-fewshots.es.md) |

Las carpetas de fuente llevan prefijo por tipo (`lakehouse-tables-…`, `warehouse-tables-…`,
`kusto-…`, `semantic-model-…`, `ontology-…`), y hay carpetas separadas de **draft** y **published** —
el límite draft/publicado es explícito en el árbol. Una fuente de modelo semántico **no tiene
`fewshots.json`**, porque sus ejemplos viven en Prep for AI sobre el modelo (ver
[04](04-source-instructions-and-fewshots.es.md)) — el propio layout de archivos codifica esa
asimetría.

## Cómo escribirla bien

- **Autora en el portal, gobierna en Git.** Itera visualmente, luego commitea la config serializada
  para que cada cambio siguiente sea un diff, no un misterio.
- **Revisa la config contra la anatomía.** Un PR que cambia `aiInstructions` es un cambio de
  identidad/comportamiento; un cambio en `datasource.json.elements` es un cambio de selección de
  esquema — léelos como tales.
- **Publica deliberadamente.** Draft es donde iteras; solo un agente *publicado* expone el endpoint que
  usan los consumidores y orquestadores ([06](06-direct-vs-orchestrator.es.md)).
- **Automatiza la evaluación, no solo el despliegue.** Usa el harness de evaluación del SDK (un
  conjunto de verdad de pares pregunta→respuesta-esperada) como gate de calidad antes de publicar —
  aprovisionar sin un chequeo de regresión envía caídas silenciosas de precisión.
- **No dupliques secretos ni IDs al repo.** Los identificadores de workspace, ítem y modelo semántico
  son GUIDs específicos del entorno — mantenlos como parámetros/placeholders, nunca hard-coded (ver
  [SANITIZATION.md](../../SANITIZATION.md)).

## Anti-patrón

**Solo-portal, solo-prod** — cada cambio hecho a mano en el agente publicado, sin historial de
versión, sin revisión y sin forma de hacer rollback. Su imagen espejo es **automatizar el despliegue
sin evaluación**, de modo que un cambio de config sale rápido *y* regresiona en silencio la calidad de
respuesta. Y **hard-codear GUIDs de entorno** en la config commiteada, lo que a la vez filtra
identificadores y rompe en el momento en que el agente se promueve a otro workspace.

## El ejemplo Contoso

Este repositorio *es* la vista config-as-code del agente Contoso, mantenida vendor-neutral:

- [`agent.config.json`](../../examples/contoso-vendor-spend/agent.config.json) lleva los
  identificadores de Fabric como **placeholders** — `<workspace-id>`, `<agent-id>`,
  `<semantic-model-id>` — nunca GUIDs reales (el guard de sanitización rompe el build si aparece un
  GUID).
- [`data-sources.yaml`](../../examples/contoso-vendor-spend/data-sources.yaml) es el análogo legible de
  `datasource.json` — la única fuente de modelo semántico y sus ocho tablas seleccionadas — y, por ser
  modelo semántico, deliberadamente no lleva **`fewshots.json`**.
- [`instructions.md`](../../examples/contoso-vendor-spend/instructions.md) es el payload de
  `aiInstructions` en forma humana.

Leídos juntos muestran la forma que toma la carpeta Git de un agente real — los mismos archivos que un
revisor diffearía en un PR — con cada valor específico de entorno parametrizado afuera.

---
_Siguiente: [08 · Ciclo de vida y la caducidad 2026 →](08-lifecycle-and-sunset.es.md)_
