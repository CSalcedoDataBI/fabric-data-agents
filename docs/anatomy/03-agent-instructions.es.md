[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](03-agent-instructions.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](03-agent-instructions.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 03 · Instrucciones a nivel agente

## Qué es

Las instrucciones a nivel agente son las **reglas globales** que aplican a cada pregunta, sin importar
qué fuente responda. Viven en el mismo campo de Data agent instructions que la identidad
([01](01-identity-and-role.es.md)) — el presupuesto compartido de **15.000 caracteres** — pero donde
la identidad dice *quién es el agente*, estas dicen *cómo debe comportarse*: disciplina de aditividad,
desambiguación, manejo de nulos, forma de salida y lo que nunca debe hacer.

Mantenlas distintas de las instrucciones **a nivel de fuente**
([04](04-source-instructions-and-fewshots.es.md)), que le enseñan al agente cómo consultar *una fuente
específica*. Las reglas a nivel agente son comportamiento agnóstico de la fuente; las reglas de fuente
son oficio de consulta.

## Por qué importa

La mayoría de las respuestas erróneas de un Data Agent no son fallos de traducción — el SQL o el DAX
es válido — son fallos **de comportamiento** que el modelo cometería por defecto y que solo una regla
explícita evita:

- **Aditividad.** Un modelo con gusto hará `SUM` de un porcentaje o promediará una tasa entre filas.
  Sumar una medida no aditiva es aritméticamente sin sentido, y nada lo detiene a menos que lo digas.
- **Adivinar en silencio.** Ante "muéstrame el gasto" sin periodo ni grano, el default es elegir uno y
  responder como si se hubiera pedido — ocultando el supuesto. Una regla de desambiguación lo
  convierte en un supuesto declarado o una pregunta aclaratoria de una línea.
- **Ratios per cápita.** "Ventas por cliente" está mal si el denominador es la población
  equivocada. Una regla que obliga al agente a *nombrar el denominador* hace el número auditable.
- **Límites de gobernanza.** Las instrucciones operan *por debajo* de la intención organizacional y
  por rol; RLS se respeta lo menciones o no. Decir "respondes bajo la identidad de quien pregunta;
  nunca razones alrededor de permisos" fija la expectativa con honestidad en vez de implicar que el
  agente vigila el acceso él mismo.

## Cómo escribirla bien

- **Haz las reglas verificables e imperativas.** "Solo las medidas aditivas pueden sumarse; nunca
  totalices un %, una tasa o un promedio entre filas" es comprobable; "sé preciso" no.
- **Fuerza la desambiguación sobre la adivinanza.** Exige que el agente declare el supuesto que hace,
  o haga una pregunta aclaratoria corta, cuando falte periodo o grano.
- **Nombra denominadores.** Todo ratio por unidad debe etiquetar su denominador y su población.
- **Prefiere tablas con unidades** para desgloses, rankings y respuestas de varias medidas — la prosa
  esconde los números.
- **Codifica el "nunca inventar".** Ni medidas, ni dimensiones, ni valores que no estén en la fuente.
- **Dale al usuario timón, no un laberinto.** Un vocabulario de comandos pequeño y documentado (un
  conjunto ayuda/catálogo/validar) es más descubrible que un muro de prosa — ver los comandos `::` de
  Contoso abajo.
- **Respeta el presupuesto de caracteres.** Identidad + reglas globales comparten 15k caracteres;
  empuja los ejemplos de consulta específicos de fuente hacia
  [04](04-source-instructions-and-fewshots.es.md).

## Anti-patrón

La **instrucción "sé útil y preciso"** — aspiracional, no verificable y vacía de comportamiento: no
previene ninguno de los fallos de arriba. Su opuesto es la **novela de casos borde** que revienta el
presupuesto de caracteres y entierra las tres reglas que de verdad importan. Un tercer anti-patrón es
**instruir alrededor de la gobernanza** — decirle al agente que "muestre todos los datos" con la
esperanza de saltarse RLS; no puede, y la instrucción solo confunde a quien la lea después.

## El ejemplo Contoso

Las [instrucciones de Contoso](../../examples/contoso-retail/data-agent/instructions.md) son un conjunto
compacto de reglas globales, cada una apuntando a un modo de fallo real:

1. **Usa medidas definidas** — nunca re-agregues una columna cruda cuando existe una medida.
2. **Respeta la aditividad** — solo las medidas aditivas (de volumen) pueden sumarse; nunca totalices
   un %, tasa o promedio entre filas.
3. **Reporta medidas compañeras juntas** — cuando una medida declara `ALSO REPORT WITH IT: …`,
   devuelve las compañeras para el mismo periodo y filtros, salvo que el usuario diga "solo".
4. **Los ratios per cápita nombran su denominador** — `[Sales per Customer]` divide entre *Distinct
   Customers* (clientes que compraron en el periodo); etiquétalo ("por cliente (Distinct Customers =
   N)"), nunca impliques la base total de clientes.
5. **Prefiere tablas**, **6. RLS respetado automáticamente**, **7. Desambigua antes de adivinar.**

También trae un pequeño **vocabulario de comandos** `>` (`>help`, `>about`) para que los usuarios
timoneen el agente explícitamente — los comandos empiezan con `>` en vez de `/` precisamente porque
los asistentes anfitriones interceptan una barra inicial. Son a nivel agente porque valen para cada
pregunta, independientemente de qué fuente (aquí, una sola) responda.

---
_Siguiente: [04 · Instrucciones de fuente y few-shots →](04-source-instructions-and-fewshots.es.md)_
