[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](06-direct-vs-orchestrator.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](06-direct-vs-orchestrator.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 06 · Directo vs. orquestador

## Qué es

Dos arquitecturas responden una pregunta con un Data Agent:

- **Directo** — el usuario (o app) habla con **un solo Fabric Data Agent**, que internamente rutea
  entre sus (hasta cinco) fuentes y devuelve una respuesta anclada en datos. El ruteo entre fuentes es
  la lógica de orquestación/planeación *propia* del agente, fijada por su **runtime** (Standard = GA,
  Preview = últimos cambios de ruteo/generación-de-consultas).
- **Orquestador** — un **agente externo** (Foundry Agent Service, Microsoft 365 Copilot, Copilot
  Studio, Teams, una app multi-agente propia) trata al Fabric Data Agent como **una herramienta entre
  varias**. El agente externo decide *cuándo* llamarlo, y luego mezcla su resultado con otras
  herramientas y su propio razonamiento. La autorización fluye **On-Behalf-Of (OBO)**: el data agent
  sigue corriendo bajo la identidad del usuario final, así que RLS se respeta a través del salto.

Una costura clave: en el patrón orquestador el modelo externo hace el *ruteo y la redacción*, pero
**no cambia el modelo que el Data Agent usa para NL2SQL/DAX/KQL** — los dos son independientes.

## Por qué importa

La elección fija el límite de responsabilidad y los modos de fallo que heredas:

- **Directo** es el contrato más ajustado. Un artefacto, un conjunto de instrucciones, un solo lugar
  para probar y gobernar. Es el default correcto cuando las preguntas viven enteramente dentro de tus
  datos de Fabric, y es la superficie que toda esta referencia optimiza.
- **Orquestador** compra alcance — combinar datos gobernados de Fabric con conocimiento no
  estructurado, APIs externas o acciones — al costo de una segunda capa que puede *re-interpretar* la
  salida del agente. Bajo Microsoft 365 Copilot, por ejemplo, el orquestador anfitrión razona sobre
  los datos devueltos y puede resumirlos o reformularlos; puedes amortiguarlo con la descripción de
  publicación (`description_for_model`) pero no eliminarlo.
- **La gobernanza se preserva de cualquier forma** — OBO significa que el data agent nunca excede los
  permisos de quien pregunta, envuelva la arquitectura que sea — pero el límite de cumplimiento y el
  manejo de datos de la capa *externa* pasan a ser tuyos de responder una vez que los resultados salen
  de Fabric.

## Cómo escribirla bien

- **Por defecto, directo** mientras las preguntas tengan forma de Fabric; recurre a un orquestador
  solo cuando una clase real de preguntas necesite herramientas que el Data Agent no tiene.
- **Mantén el Data Agent de solo lectura y de un solo propósito** — una herramienta limpia para que un
  orquestador la llame es una bien acotada, no un agente que hace de todo.
- **Escríbele al agente externo una descripción de herramienta nítida** — "para preguntas de ventas,
  margen y clientes, usa la herramienta Fabric" — y considera `tool_choice` /
  invocación forzada cuando la herramienta deba correr siempre.
- **Publica antes de integrar.** Solo un Data Agent *publicado* expone el endpoint
  (`.../groups/<workspace-id>/aiskills/<artifact-id>`) al que un orquestador se conecta.
- **Prueba la costura, no solo el agente** — verifica que el orquestador no distorsione números
  correctos, y añade una instrucción de "emitir tal cual" donde la fidelidad importe.

## Anti-patrón

**Recurrir a un orquestador multi-agente cuando un solo agente directo respondería todo** — añades una
capa de re-interpretación, un segundo límite de cumplimiento y más piezas móviles sin ganar cobertura.
Lo inverso: **meter dominios no relacionados en un solo Data Agent** para evitar un orquestador, hasta
que sus cinco fuentes y reglas de ruteo chocan. Y **dejar que el anfitrión reformule en silencio
números gobernados** — enviar una integración de Copilot sin revisar si el orquestador resume las
cifras en algo sutilmente erróneo.

## El ejemplo Contoso

El agente Contoso está autorado **directo**: una fuente de modelo semántico, un conjunto de
instrucciones, probable en aislamiento — el contrato más simple que responde bien las preguntas de
ventas retail. Su diseño también lo vuelve una *buena herramienta de orquestador* el día que
haga falta: es de solo lectura, de un solo dominio, y su rol ("analista de ventas retail …
ventas, rentabilidad, clientes, productos, tiendas") se lee casi textual como la descripción de
herramienta que un agente Foundry o Copilot externo usaría para decidir cuándo llamarlo. Nada de la
construcción directa hay que deshacer para promoverlo a un flujo orquestado — publícalo, entrega el
endpoint al agente externo, y el flujo de identidad OBO mantiene RLS intacto.

---
_Siguiente: [07 · Aprovisionamiento →](07-provisioning.es.md)_
