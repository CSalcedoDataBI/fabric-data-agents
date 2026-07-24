[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](tooling.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](tooling.es.md)

# Herramientas — qué instalar antes de redactar

Esta referencia te dice *qué* escribir. Esta página lista las herramientas que ayudan a *escribirlo
bien*. Se limita a propósito a **apoyos de redacción** — cosas que ayudan a producir mejores
instrucciones y a verificarlas. El aprovisionamiento, la CI y la automatización de orquestación
quedan fuera; eso es [07 · Aprovisionamiento](anatomy/07-provisioning.es.md).

Nada de esto hace falta para *leer* este repositorio. Hace falta solo si quieres *hacer* el trabajo
con asistencia.

---

## Oficial — Microsoft

### `microsoft/skills-for-fabric`

La colección propia de Microsoft de Agent Skills y servidores MCP para operar Microsoft Fabric desde
CLI, VS Code o Claude. Trae perfiles para **revisión de modelo semántico**, **Fabric apps** y
**data agents** — este último es directamente relevante para todo lo de este repositorio.

| | |
|---|---|
| Repo | <https://github.com/microsoft/skills-for-fabric> |
| Publica | Microsoft (oficial) |
| Licencia | MIT |
| Tipo | Plugin de Claude Code (marketplace) |

```bash
claude plugin marketplace add microsoft/skills-for-fabric
```

Úsalo para la superficie operativa: explorar workspaces, inspeccionar modelos semánticos, correr el
Fabric CLI y manejar un Data Agent desde tu editor.

---

## Apoyos de redacción — escribir mejores instrucciones

Lo de mayor palanca que puedes mejorar es el texto que le das al agente y al modelo. La disciplina
que importa es la **verificación**: una instrucción que suena plausible pero es falsa es peor que
ninguna, porque dirige activamente al agente hacia el error.

Y no es teoría. Al redactar las instrucciones de Contoso Retail, un borrador le decía al agente que
*"convirtiera monedas usando `DimCurrencyExchange`"* — sonaba razonable y era **falso**: las 126.524
filas de hechos son `MXN` y esa tabla está desconectada. Contrastarlo con los datos convirtió una
instrucción dañina en una correcta. Ver
[`examples/contoso-retail/model/prep-for-ai/ai-instructions.md`](../examples/contoso-retail/model/prep-for-ai/ai-instructions.md),
que documenta cómo se verificó **cada** línea.

### `verified-ai-instructions` *(nuestra — incluida en este repo)*

Redacta instrucciones *Prep for AI* en formato Microsoft y **verificadas contra los datos** para un
modelo semántico de Power BI / Fabric, y las escribe directamente en el TMDL en disco. Cada
afirmación se prueba contra la estructura del modelo y sus datos reales *antes* de escribirse.

Qué incluye:

- el formato de autoría de Microsoft (contexto de negocio primero, secciones temáticas, nombrar
  `Tabla[Columna]` explícitamente, el límite de 10.000 caracteres);
- un protocolo de verificación que separa cada afirmación en **estructural** (comprobable contra
  TMDL) y **de datos** (requiere consulta), y exige que ambas pasen;
- `apply-instructions.py`, que escribe el texto en la cadena JSON `CustomInstructions` dentro de
  `definition/cultures/<culture>.tmdl`, escapándolo bien y re-parseándolo para validar. Editar ese
  valor a mano es la forma número uno de corromper el archivo — un solo salto de línea crudo en vez
  de `\n` invalida el JSON y Power BI descarta las instrucciones en silencio.

Se distribuye **en este repositorio**, bajo la misma licencia MIT:

```bash
cp -r skills/verified-ai-instructions ~/.claude/skills/
```

→ [`skills/verified-ai-instructions/`](../skills/verified-ai-instructions/)

Es la herramienta que produjo las instrucciones verificadas de este repositorio, así que el *método*
también se puede reproducir a mano desde
[`examples/contoso-retail/model/prep-for-ai/ai-instructions.md`](../examples/contoso-retail/model/prep-for-ai/ai-instructions.md),
cuya tabla de verificación muestra exactamente qué se comprobó y cómo.

---

## Deliberadamente aún no listado

La automatización — aprovisionar agentes por REST, CI/CD de la config del agente, baterías de
evaluación contra el endpoint MCP — es real y se usa en este proyecto, pero es otro tipo de
herramienta, con otros modos de fallo, y no es lo que hace que un agente responda bien. Se
documentará aparte cuando esté lo bastante estable para recomendarla. El método de medición que esas
baterías implementan ya está escrito en
[`examples/contoso-retail/data-agent/ablation-test-design.md`](../examples/contoso-retail/data-agent/ablation-test-design.md),
así que hoy puedes reproducir la evaluación a mano.
