[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=for-the-badge)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=for-the-badge)](README.es.md)
&nbsp;·&nbsp; [![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-black?style=for-the-badge)](LICENSE)

# Anatomía de un Fabric Data Agent

**Una guía de referencia, neutral de proveedor, sobre *cómo funciona de verdad un Microsoft Fabric Data Agent* — y cómo instruirlo bien.**

Un Fabric Data Agent convierte preguntas en lenguaje natural en consultas gobernadas (SQL / DAX / KQL / GQL) sobre tu lakehouse, warehouse, modelo semántico de Power BI, base KQL o grafo — y responde bajo la identidad de quien pregunta. Lograr que responda *correcta y consistentemente* depende menos de hacer clic en "Crear" y más de las partes que tú escribes: su **rol**, sus **fuentes de datos**, sus **instrucciones** y sus **consultas de ejemplo**.

Este repositorio disecciona cada una de esas partes. Cada sección sigue la misma forma — **Qué es · Por qué importa · Cómo escribirla bien · Anti-patrón · El ejemplo Contoso** — y cada parte se ilustra de punta a punta con un ejemplo trabajado: el **[Contoso Vendor Spend Agent](examples/contoso-vendor-spend/README.es.md)**.

> No es un tutorial de "primeros pasos". Es la referencia que mantienes abierta *mientras* creas el agente, destilada de trabajo real de Data Agents en producción (sanitizado — ver [SANITIZATION.md](SANITIZATION.md)).

## La anatomía

| # | Parte | Qué aprenderás |
|---|-------|----------------|
| 00 | [Panorama](docs/anatomy/00-overview.es.md) | Qué es un Data Agent, el modelo mental y cómo encajan las partes |
| 01 | [Identidad y rol](docs/anatomy/01-identity-and-role.es.md) | El contexto de sistema que enmarca todo lo que hace el agente |
| 02 | [Fuentes de datos](docs/anatomy/02-data-sources.es.md) | SQL · KQL · Modelo Semántico (NL2DAX) · Grafo (NL2GQL) — cuál elegir y por qué |
| 03 | [Instrucciones a nivel agente](docs/anatomy/03-agent-instructions.es.md) | RLS, nulls, desambiguación, aditividad — las reglas que evitan respuestas erróneas |
| 04 | [Instrucciones de fuente y few-shots](docs/anatomy/04-source-instructions-and-fewshots.es.md) | El mayor multiplicador de precisión |
| 05 | [Ontología y glosario de negocio](docs/anatomy/05-ontology-and-glossary.es.md) | Mapear el lenguaje de negocio a campos del modelo |
| 06 | [Directo vs. orquestador](docs/anatomy/06-direct-vs-orchestrator.es.md) | ¿Un agente o varios? Evidencia de tests reales |
| 07 | [Aprovisionamiento](docs/anatomy/07-provisioning.es.md) | Portal · REST · PowerShell — la costura de automatización |
| 08 | [Ciclo de vida y la caducidad 2026](docs/anatomy/08-lifecycle-and-sunset.es.md) | La Assistants API se apaga el **2026-08-26** — planifica tu migración |

## El ejemplo trabajado — Contoso Vendor Spend

Un Data Agent completo y sanitizado sobre un modelo ficticio de gasto de fuerza laboral contingente de **Contoso** (un dataset de "vendor management": proveedores de staffing, asignaciones, facturas). Muestra patrones reales que rara vez se explican: **medidas compañeras reportadas juntas**, **disciplina aditiva vs. no-aditiva**, **defaults por dimensiones de liderazgo**, un **caveat del denominador en ratios per cápita** y **comandos de dirección `::`**.

→ [`examples/contoso-vendor-spend/`](examples/contoso-vendor-spend/README.es.md)

## Para quién es

Ingenieros de BI/analítica que construyen Data Agents en Microsoft Fabric, y cualquiera (humano o asistente de IA) que necesite una referencia precisa y actual de las piezas móviles. Todo está fechado; las partes en preview o con caducidad conocida están marcadas.

## Procedencia y sanitización

Los patrones aquí vienen de Data Agents que se desplegaron para clientes reales. **Ningún dato, nombre, ID o endpoint de cliente aparece en este repositorio.** Cómo se garantiza — el mapa de reemplazos y el guard automatizado — está documentado en **[SANITIZATION.md](SANITIZATION.md)** y se hace cumplir con [`scripts/sanitize-check.sh`](scripts/sanitize-check.sh) en CI.

## Licencia

[MIT](LICENSE) © 2026 Cristóbal Salcedo ([CSalcedoDataBI](https://github.com/CSalcedoDataBI)). Contribuciones bienvenidas — ver [CONTRIBUTING.md](CONTRIBUTING.md).
