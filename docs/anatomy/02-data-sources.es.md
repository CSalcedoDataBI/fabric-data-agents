[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](02-data-sources.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](02-data-sources.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 02 · Fuentes de datos

## Qué es

Una fuente de datos es un almacén gobernado que el agente puede consultar, más la **selección de
tablas** dentro de él que el agente tiene permitido ver. Un solo Fabric Data Agent soporta **hasta
cinco fuentes en cualquier combinación**, y cada tipo de fuente trae su propio traductor de lenguaje
natural a consulta:

| Categoría | Artefactos | Lenguaje | Traductor |
|---|---|---|---|
| **SQL** | Lakehouse, Warehouse, SQL Database, Mirrored Database | T-SQL | NL2SQL |
| **Eventhouse** | Base KQL | KQL | NL2KQL |
| **Modelo semántico** | Modelo semántico de Power BI | DAX | NL2DAX |
| **Graph** _(preview)_ | Modelo de grafo | GQL | NL2GQL |
| **Ontología** _(preview)_ | Fabric Ontology | nativo de ontología | — |
| **Azure AI Search** _(preview)_ | Índice de búsqueda | lenguaje natural | recuperación |

_Nota de versión (2026): las fuentes SQL, Eventhouse y modelo semántico están en disponibilidad
general; Graph, Ontología y Azure AI Search están en preview — confirma el estado actual antes de
depender de ellas._

El agente ejecuta cada consulta **bajo la identidad de quien pregunta**, así que Row-Level Security y
los permisos de objeto se respetan automáticamente. Nota: solo necesitas **Read** sobre un modelo
semántico para añadirlo; Write solo hace falta para *modificar* el modelo o configurar Prep for AI
(ver [04](04-source-instructions-and-fewshots.es.md)).

## Por qué importa

La fuente que eliges decide el lenguaje de consulta, la forma de la respuesta y dónde vive la lógica
de negocio:

- **Modelo semántico (DAX)** — responde en el lenguaje de las *medidas gobernadas*. El modelo ya
  codifica aditividad, moneda, filtros e inteligencia de tiempo, así que el agente hereda lógica de
  negocio correcta en vez de reinventarla en SQL. Lo mejor cuando existe un modelo curado.
- **SQL (lakehouse / warehouse)** — responde sobre tablas relacionales o Delta crudas. Máximo alcance
  y detalle, pero el agente debe armar los joins y agregaciones él mismo, así que la corrección recae
  en tu selección de esquema y tus consultas de ejemplo.
- **KQL (Eventhouse)** — analítica de series de tiempo y logs/eventos, consultada en su lugar sin
  mover datos. Fomenta filtros de tiempo para mantenerla rápida.

Seleccionar **solo las tablas relevantes** es una palanca de precisión de primera clase, no un
formalismo: un esquema inflado es más superficie para que el traductor se equivoque. Menos tablas,
bien nombradas → menos joins erróneos y menos columnas ambiguas.

## Cómo escribirla bien

- **Prefiere un modelo semántico cuando exista** y las preguntas tengan forma de métrica — obtienes
  medidas gobernadas gratis y esquivas toda una clase de bugs de re-agregación.
- **Recorta la selección de tablas** a lo que las preguntas del agente realmente necesitan. Para
  lakehouses, selecciona *tablas*, no archivos — ingesta primero los archivos a tablas.
- **Rutea por tipo de pregunta, no por conveniencia** — declara en la identidad
  ([01](01-identity-and-role.es.md)) qué fuente es dueña de qué tipo de pregunta.
- **Combina fuentes deliberadamente.** Cinco fuentes multiplican la ambigüedad de ruteo; añade una
  fuente solo cuando una clase de preguntas de verdad la necesite, y dale al router una regla clara.
- **Cuida el grano por fuente** y exponlo en las instrucciones para que el agente no mezcle granos
  incompatibles en una respuesta.

## Anti-patrón

**Apuntar el agente a tablas crudas cuando un modelo semántico gobernado ya codifica las métricas.**
El agente entonces re-deriva "gasto total" con un `SUM` sobre una columna de hechos, divergiendo en
silencio de la medida oficial del modelo (que puede filtrar, convertir moneda o manejar nulos).
Igual de común: **seleccionar todas las tablas "por si acaso"**, que inunda al traductor con columnas
parecidas y produce joins erróneos con seguridad. Y **mezclar cinco fuentes sin reglas de ruteo**, de
modo que la misma pregunta se resuelve contra una fuente distinta corrida a corrida.

## El ejemplo Contoso

Contoso usa una **única fuente de modelo semántico**, declarada en
[`data-sources.yaml`](../../examples/contoso-vendor-spend/data-sources.yaml):

```yaml
sources:
  - type: semantic-model          # NL -> DAX
    name: "Contoso Vendor Spend (SM)"
    id: "<semantic-model-id>"     # placeholder — el valor real es un GUID
    tables: [factspend, CALENDAR, dimbusinessunit, dimjobfamily,
             dimlocation, dimspendtype, dimsupplier, dimcostcenter]
```

Un modelo curado, ocho tablas nombradas — no todo el workspace. Como es un modelo semántico, el agente
responde en DAX contra **medidas definidas** (`[Total Spend]`, `[Invoiced Workers]`, …) en vez de
sumar columnas de `factspend`, así que la lógica de negocio se queda donde la puso el modelador. El
brief de ruteo es una sola línea en la identidad; una segunda fuente (digamos un lakehouse de facturas
crudas para búsquedas a nivel de registro) se ganaría su propia regla de ruteo antes de añadirse.

---
_Siguiente: [03 · Instrucciones a nivel agente →](03-agent-instructions.es.md)_
