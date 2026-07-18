[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)

# Contoso Vendor Spend — ejemplo trabajado

Un Fabric Data Agent completo y **sanitizado** que se usa a lo largo de [Anatomía de un Fabric Data Agent](../../README.es.md).
Está autorado limpio (no extraído de un cliente) — ver [SANITIZATION.md](../../SANITIZATION.md).

## El escenario

**Contoso** opera una fuerza laboral contingente: contrata personal temporal a través de proveedores
de staffing. Cada línea de factura llega a un modelo semántico de Power BI, **Contoso Vendor Spend
(SM)**. Los usuarios de negocio quieren preguntar en lenguaje natural: *"¿Top 5 proveedores por gasto
el año pasado?"*, *"¿Split SOW vs Staff Augmentation?"*, *"¿Qué impulsó el alza del gasto?"* — sin
escribir DAX.

## Los archivos (las cuatro partes que escribes)

| Archivo | Parte de la anatomía | Qué contiene |
|---|---|---|
| [`agent.config.json`](agent.config.json) | 01, 07 | Identidad + IDs de recursos Fabric (placeholders) |
| [`data-sources.yaml`](data-sources.yaml) | 02 | La fuente modelo-semántico (NL2DAX) |
| [`instructions.md`](instructions.md) | 03 | Rol, reglas de aditividad, regla de medidas compañeras, comandos `::` |
| [`example-queries.json`](example-queries.json) | 04 | Few-shots que fijan medida/periodo/grano/breakdown |

## Patrones que demuestra este ejemplo

- **Medidas compañeras reportadas juntas** — pides *Total Spend* y también recibes *Invoiced Workers*
  y *Assignments*, salvo que digas "solo".
- **Disciplina aditiva vs. no-aditiva** — *Total Spend* se puede sumar; *Average Invoice* y
  *% of Total Spend* nunca.
- **Defaults por dimensiones de liderazgo** — un "desglósalo" sin calificar usa Business Unit /
  Job Family / Country / Spend Type.
- **Caveat del denominador en ratios per cápita** — *Spend per Invoiced Worker* siempre nombra su
  denominador, para que nadie lo confunda con gasto por empleado activo.
- **Comandos de dirección `::`** — `::about`, `::catalog`, `::improve`, `::validate`, `::drivers`
  dejan al usuario manejar el agente sin re-escribir prompts largos.

## El modelo de un vistazo

- **Fact:** `factspend` (grano: Fecha × Business Unit × Job Family × Country × Spend Type)
- **Medidas:** Total Spend, Invoiced Workers, Suppliers with Spend, Assignments, Average Invoice,
  Spend per Invoiced Worker, % of Total Spend
- **Dims de liderazgo:** Business Unit, Job Family, Country, Spend Type
- **Periodo:** 2023–2024 · **Proveedores (ejemplos):** Fabrikam, Northwind Traders, Adventure Works

> Cada ID en `agent.config.json` y `data-sources.yaml` es un `<placeholder>`. Complétalos con tus
> propios GUIDs de workspace/modelo/agente al aprovisionar — ver
> [07 · Aprovisionamiento](../../docs/anatomy/07-provisioning.es.md).
