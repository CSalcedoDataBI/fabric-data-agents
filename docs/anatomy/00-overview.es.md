[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](00-overview.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](00-overview.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 00 · Panorama

## Qué es un Fabric Data Agent

Un **Microsoft Fabric Data Agent** es una interfaz de lenguaje natural gobernada sobre tus datos. Un
usuario pregunta en lenguaje natural; el agente elige una fuente de datos, genera una consulta en el
lenguaje de esa fuente — **SQL** (lakehouse/warehouse), **DAX** (modelo semántico de Power BI),
**KQL** (Eventhouse) o **GQL** (grafo, preview) — la ejecuta **bajo la identidad de quien pregunta**
(así se respetan Row-Level Security y permisos), y devuelve una respuesta anclada en datos.

*No* es un chatbot con datos pegados en un prompt, y *no* es un modelo afinado (fine-tuned). Es una
capa de **generación-y-ejecución de consultas** cuya precisión controlas por configuración, no por entrenamiento.

## El modelo mental: cuatro partes que escribes

Todo lo que puedes influir sobre el comportamiento del agente vive en cuatro partes autoradas. Toda
esta referencia se organiza alrededor de ellas:

```
                 ┌──────────────────────────────────────────────────┐
   usuario   ───▶│  IDENTIDAD Y ROL       (01)  quién soy            │
   pregunta      │  FUENTES DE DATOS      (02)  qué puedo ver        │──▶ SQL / DAX / KQL / GQL
                 │  INSTRUCCIONES AGENTE  (03)  cómo me comporto     │──▶ ejecuta como quien pregunta
                 │  INSTRUCCIONES FUENTE  (04)  cómo consulto        │──▶ respuesta anclada
                 │  + FEW-SHOTS                 cada fuente          │
                 └──────────────────────────────────────────────────┘
```

- **[01 · Identidad y rol](01-identity-and-role.es.md)** enmarca *quién es el agente* y para qué sirve.
- **[02 · Fuentes de datos](02-data-sources.es.md)** decide *qué puede ver* y en qué lenguaje de consulta.
- **[03 · Instrucciones a nivel agente](03-agent-instructions.es.md)** son las *reglas globales*
  (aditividad, RLS, desambiguación) que mantienen correctas las respuestas.
- **[04 · Instrucciones de fuente y few-shots](04-source-instructions-and-fewshots.es.md)** le enseñan
  *cómo consultar bien cada fuente* — la mayor palanca de precisión.

Tres partes más las rodean: **[05 · Ontología y glosario](05-ontology-and-glossary.es.md)** (lenguaje
de negocio → campos del modelo), **[06 · Directo vs. orquestador](06-direct-vs-orchestrator.es.md)**
(un agente o un router sobre varios), y los extremos operativos
**[07 · Aprovisionamiento](07-provisioning.es.md)** y **[08 · Ciclo de vida y la caducidad 2026](08-lifecycle-and-sunset.es.md)**.

## Por qué existe esta referencia

La mayoría del material se detiene en "haz clic en Crear y elige un lakehouse". La parte difícil y no
documentada es lograr que el agente responda *correcta y consistentemente*: no sumar un porcentaje,
resolver un "desglósalo" vago hacia las dimensiones correctas, nombrar el denominador de un ratio per
cápita, desambiguar en vez de adivinar. Esos comportamientos vienen de las partes de arriba, y esta
guía muestra exactamente cómo escribirlas — ancladas en el ejemplo
**[Contoso Retail](../../examples/contoso-retail/README.es.md)**.

## Cómo leerla

Cada sección es auto-contenida y sigue la misma forma:

> **Qué es · Por qué importa · Cómo escribirla bien · Anti-patrón · El ejemplo Contoso**

Léela de corrido para el modelo mental completo, o salta a la parte que estés escribiendo ahora. Los
hechos sensibles a versión están fechados; las funciones en preview y la caducidad 2026 están marcadas
donde importan.

## Prerrequisitos (versión corta)

| Requisito | Detalle |
|---|---|
| Capacidad Fabric | SKU de pago F2+ (o Power BI Premium P1+ con Fabric habilitado) |
| Tenant settings | *Fabric data agent* + cross-geo processing/storing for AI habilitados |
| Acceso a datos | Al menos Read en el lakehouse / warehouse / modelo semántico / KQL DB objetivo |
| Fuentes modelo semántico | XMLA endpoints habilitados; **Prep for AI configurado en el modelo** (ver 04) |

El detalle completo de aprovisionamiento está en **[07 · Aprovisionamiento](07-provisioning.es.md)**.

---
_Siguiente: [01 · Identidad y rol →](01-identity-and-role.es.md)_
