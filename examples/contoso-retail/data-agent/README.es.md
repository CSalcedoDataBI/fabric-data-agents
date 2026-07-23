[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)

# Contoso Retail — Data Agent (ejemplo trabajado)

Un Fabric Data Agent completo y **sanitizado** sobre el [modelo semántico Contoso Retail](../model/),
usado a lo largo de [Anatomía de un Fabric Data Agent](../../README.es.md). Está redactado limpio (no
extraído de un cliente) — ver [SANITIZATION.md](../../SANITIZATION.md).

## El escenario

**Contoso** opera un negocio retail. Cada línea de pedido cae en un modelo semántico de Power BI,
**ContosoRetail** (ventas, costo, margen, clientes, productos, tiendas, canales). Los usuarios de
negocio quieren preguntar, en lenguaje natural: *"¿Ventas por categoría?"*, *"¿Margen % por país?"*,
*"¿Split Online vs Store?"*, *"¿Qué movió el cambio interanual?"* — sin escribir DAX.

## Qué va dónde (la lección clave)

Un Fabric Data Agent tiene una **capa de agente** y una **capa de fuente**. Para una fuente
**semantic-model**, el generador NL2DAX se apoya **únicamente** en los metadatos del modelo + su
**Prep-for-AI** — así que la sustancia que da forma al DAX se configura en el **modelo**, y en el
agente solo vive el enrutamiento/tono/steering.

| Qué redactas | Dónde vive | Archivo |
|---|---|---|
| Identidad + IDs de recursos Fabric | Agente | [`agent.config.json`](agent.config.json) |
| La fuente semantic-model (NL2DAX) | Agente | [`data-sources.yaml`](data-sources.yaml) |
| Rol, alcance, tono, formato de salida, comandos `::` | Agente | [`instructions.md`](instructions.md) |
| Aditividad, semántica de medidas, breakdown y regla de moneda | **Modelo** (Prep-for-AI) | [`../model/prep-for-ai/ai-instructions.md`](../model/prep-for-ai/ai-instructions.md) |
| Visibilidad de tablas/columnas/medidas + sinónimos | **Modelo** (Prep-for-AI) | [`../model/prep-for-ai/ai-data-schema.json`](../model/prep-for-ai/ai-data-schema.json) |
| Few-shots Pregunta→DAX gobernados y probados | **Modelo** (Verified Answers) | [`verified-answers.md`](verified-answers.md) · espejo en [`example-queries.json`](example-queries.json) |

> Esta es la corrección que distingue a este ejemplo: **las instrucciones de fuente y las consultas
> de ejemplo puestas a nivel de *agente* se ignoran** para una fuente semantic-model. Esa sustancia
> va en el modelo, donde el generador realmente la lee. Ver
> [04 · Instrucciones de fuente y few-shots](../../docs/anatomy/04-source-instructions-and-fewshots.es.md).

## Patrones que demuestra este ejemplo

- **Disciplina aditivo vs no-aditivo** — *Total Sales* / *Gross Margin* se pueden sumar; *Margin %*,
  *Average Order Value*, *% of Total Sales*, *Sales YoY %* nunca.
- **Semi-aditividad de conteos distintos** — *Orders* y *Distinct Customers* no se suman entre periodos.
- **Salvedad del denominador en ratios por cliente** — *Sales per Customer* siempre nombra su denominador.
- **Regla de moneda única (verificada)** — todo es MXN; *DimCurrencyExchange* está desconectada y no
  debe usarse. Se eliminó una instrucción plausible de "convertir monedas" tras revisar los datos —
  el punto de todo el ejemplo.
- **Valores de dimensión en español** — categorías y otras etiquetas están en español; al agente se le dice.
- **Comandos de steering `::`** — `::about`, `::catalog`, `::improve`, `::validate`, `::drivers`.

## El modelo de un vistazo

- **Hecho:** `FactSales` (grano: una línea de pedido; Fecha × Categoría × País × Canal)
- **Medidas (15):** Total Sales, Total Quantity, Total Cost, Gross Margin, Orders, Distinct
  Customers, Margin %, Average Order Value, Average Selling Price, Units per Order, Sales per
  Customer, % of Total Sales, Sales YTD, Sales PY, Sales YoY %
- **Dims de breakdown por defecto:** Categoría de Producto, País de Tienda, País de Cliente, Canal
- **Periodo:** 2023-01-01 → 2024-12-31 · **Moneda:** solo MXN · **Canales:** Online, Store

> Todo ID en `agent.config.json` y `data-sources.yaml` es un `<placeholder>`. Rellénalos con tus
> propios GUIDs de workspace/modelo/agente al aprovisionar — ver
> [07 · Aprovisionamiento](../../docs/anatomy/07-provisioning.es.md). El modelo publicado se llama
> `ContosoRetail` en tu workspace.
