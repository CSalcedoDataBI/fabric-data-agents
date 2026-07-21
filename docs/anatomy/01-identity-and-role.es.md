[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](01-identity-and-role.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](01-identity-and-role.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 01 · Identidad y rol

## Qué es

La **identidad** es el bloque de instrucciones a nivel agente que enmarca *quién es el agente* antes
de mirar una sola fila: su dominio, su audiencia, los datos que representa y cómo debe comportarse. En
Microsoft Fabric vive en el panel **Data agent instructions** — un único campo en lenguaje natural de
hasta **15.000 caracteres** que el orquestador del agente lee primero, en cada turno, por delante de
cualquier regla específica de fuente.

No es un system prompt que afinas con trucos de jailbreak, y no es el lugar para la sintaxis de
consulta. Es el **brief de rol y ruteo**: para qué sirve el agente, qué significa una "fila" de su
mundo, qué fuente responde qué tipo de pregunta, y qué hacer cuando una petición es vaga o está fuera
de alcance.

## Por qué importa

La identidad es el texto de mayor palanca que escribes, porque todo lo de abajo hereda su encuadre:

- **Alcance.** Un rol nombrado ("analista de gasto de proveedores para Contoso") le dice al agente qué
  está *dentro* de su mundo y, por omisión, qué no — así declina o redirige en vez de alucinar una
  respuesta desde la tabla equivocada.
- **Ruteo.** Con hasta cinco fuentes de datos en un agente, la identidad es donde dices *manda las
  preguntas de métricas financieras al modelo semántico, las de registros crudos al lakehouse, las de
  logs a la base KQL*. El orquestador usa exactamente esto para elegir fuente.
- **Valores por defecto.** El tono, la forma de salida (tablas sobre prosa) y la postura de
  desambiguación se fijan aquí una vez y aplican en todas partes.

También vive dentro de un **modelo de precedencia**. De mayor a menor: intención organizacional
(política del tenant) → intención por rol (gobernanza del workspace, RLS) → **intención del
desarrollador (esta identidad)** → intención del usuario (la pregunta). Tu identidad puede moldear el
comportamiento, pero nunca puede pasar por encima de la gobernanza — útil saberlo para no intentar
instruir alrededor de un límite de permisos.

## Cómo escribirla bien

- **Nombra el rol y la audiencia** en la primera frase. "Eres un *analista de gasto de proveedores*
  para Contoso" le gana a "Eres un asistente de datos útil".
- **Declara el grano.** Di qué representa una fila y por qué dimensiones puede cortarse, para que el
  agente oriente bien un "desglósalo" vago (ver [05 · Ontología](05-ontology-and-glossary.es.md)).
- **Escribe las reglas de ruteo** cuando el agente tenga más de una fuente: una línea por fuente,
  anclada al *tipo* de pregunta, no al nombre de la tabla.
- **Fija los valores por defecto de comportamiento**: preferir tablas etiquetadas, desambiguar antes
  de adivinar, nunca inventar medidas ni números.
- **Deja la mecánica de consulta fuera.** Cómo hacer un join, qué medida DAX, cómo filtrar una fecha —
  eso es instrucción a nivel de fuente, cubierta en [04](04-source-instructions-and-fewshots.es.md).
  Mezclarla en la identidad infla el presupuesto de 15k y acopla la persona al esquema de una fuente.

## Anti-patrón

La identidad **"asistente útil" en blanco** — sin dominio, sin grano, sin ruteo — que hace que el
agente trate cada fuente como igual de válida para cada pregunta y responda con seguridad desde la que
el modelo eligió al azar. Su gemela es la **identidad sobrecargada**: páginas de reglas DAX y JOIN
pegadas en el campo de rol, que pertenecen a las instrucciones de fuente y que desplazan el encuadre
que de verdad guía el ruteo. Una tercera trampa es **prometer datos que el agente no puede ver**
("conoces nuestro headcount") cuando no existe tal fuente o medida — el agente lo intentará, y
fabricará.

## El ejemplo Contoso

El [agente Contoso Vendor Spend](../../examples/contoso-vendor-spend/instructions.md) abre con un rol
ajustado y un grano explícito, y nada más disfrazado de identidad:

> Eres un analista de gasto de proveedores para **Contoso**. Respondes preguntas sobre el gasto en
> fuerza laboral contingente (proveedores de staffing, asignaciones, facturas) usando el modelo
> semántico **Contoso Vendor Spend (SM)**. […] Nunca inventas números, medidas ni dimensiones que no
> estén en el modelo.

Luego declara el grano (`CALENDAR[Date] × Business Unit × Job Family × Country × Spend Type`), el
periodo de reporte y las dimensiones de desglose por defecto — la orientación que el router necesita —
mientras deja *cómo escribir el DAX* a las reglas de fuente. Como este agente tiene una sola fuente,
su brief de ruteo es trivial; la misma identidad sobre cinco fuentes llevaría una línea de ruteo por
cada una.

---
_Siguiente: [02 · Fuentes de datos →](02-data-sources.es.md)_
