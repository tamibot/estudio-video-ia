# Entrenar un estilo y editar con él

Método de Joseph (Ultimate Editors) en su tutorial *How to Edit VIRAL Talking Head Videos Using
ONLY Claude! (New Minimal Style)*, oct-2026, adaptado a este estudio. Él lo usa con el estilo de
Arthur Brooks; sirve para cualquier creador. El estilo ya entrenado de ese ejemplo está en la skill
`estilo-minimal-premium` y la plantilla `plantillas/minimal-premium/`.

> Si no sabes por qué un video está bien editado, la IA solo te va a ayudar a hacer videos malos más
> rápido. Primero se entiende el estilo como editor; después se le enseña a Claude.

## Parte 1 · Entrenar (una vez por estilo)

| Paso | Quién | Qué |
|---|---|---|
| 1 | persona | Junta **hasta 20 videos** del creador, los más cuidados (mínimo 5 para un estilo serio, 3 para una idea). |
| 2 | estudio | Los desarma: `referencia.py` (transcripción palabra por palabra, cuadro por cuadro, ritmo). |
| 3 | estudio | Por cada escena que se ve bien pregunta **por qué**: por qué esta escena acá, este diseño, estos colores, estos efectos, esta animación. |
| 4 | estudio + persona | **Tablero en Figma**: una captura de cada escena buena (salen ~100-150), agrupadas por principio (tipo de escena). En cada grupo se amplía una y se anota qué la compone: fuentes, colores, tamaños, patrones, movimiento. |
| 5 | estudio | Estudia videos + tablero y escribe **la skill del estilo** (`.claude/skills/estilo-<nombre>/`) y la **biblioteca de animaciones** (`perfil/biblioteca/`). |

Los videos enseñan **la lógica** (dónde va cada animación respecto del guion, cuánto dura, cómo se
siente); el tablero enseña **el diseño**. Juntos, Claude domina el estilo.

El estudio de los videos mira tres cosas, siempre:
1. **Dónde** se pone cada animación respecto del guion (qué frase la dispara).
2. **Cómo** está compuesto el diseño y qué elementos lo forman.
3. **La lógica de la animación**: cuánto dura, cómo entra y sale, qué se siente.

### La biblioteca de animaciones

Una carpeta por animación encontrada, nombrada `V<video>-A<n> <qué es>`
(`V01-A06 Cortina, la línea lleva al cerebro`), con:
- `diseno.jpg`: el cuadro donde se ve completa (≤ 768 px).
- `cuadros.jpg`: la tira de cuadros clave de su movimiento (`referencia.py transicion`).
- `ficha.md`: tipo de escena (principio), qué frase del guion la dispara, duración, cómo entra y
  sale, sonido, y cómo se construiría en HyperFrames o Remotion.

En el ejemplo de Joseph salieron 225 animaciones de 20 videos. La biblioteca es lo que después
permite recomendar diseños «como los usa el creador» en el documento de planificación.

### La skill del estilo

`SKILL.md` con: los principios (tipos de escena) y cuándo se usa cada uno, tokens medidos (colores,
fuentes, tamaños), lógica del texto, texturas, números de ritmo, reglas de planificación, sonido y
correcciones típicas. Modelo a seguir: `.claude/skills/estilo-minimal-premium/SKILL.md`.

## Parte 2 · Editar un video con el estilo

| Paso | Tiempo de referencia | Qué |
|---|---|---|
| 1 | — | Modelo potente y esfuerzo alto; el clip en bruto entra al chat (arrastrado). |
| 2 | 15 min | **Transcripción palabra por palabra al milisegundo** y **silencios fuera dejando 30 ms** de aire. |
| 3 | (mismo) | **Documento de planificación** (`scripts/plan_edicion.py`): guion de cada tramo con su pedazo de clip a la derecha, y a la izquierda 2-3 diseños recomendados sacados de la biblioteca («visto en las referencias») más una caja para notas. |
| 4 | 15 min | **La persona planifica.** Es el paso más importante: sin un buen plan, las animaciones no arman un buen video. La IA sola no es lo bastante creativa en el plan. |
| 5 | — | «Copiar plan» → se pega en el chat → el estudio construye. |
| 6 | 60 min | Lista de assets → búsqueda (pinturas de dominio público, B-roll de stock, fotos) → fuentes → subtítulos del A-roll → escena por escena → render v1. |
| 7 | 10 min | El v1 queda al **60-70 %**. La persona lo mira y pide correcciones concretas (con segundo y qué cambiar). |
| 8 | 15 min | Con la imagen aprobada, recién **diseño sonoro**: música y efectos según cómo los usa el creador. Render final. |

Total del ejemplo: ~2 h para un reel de 1 minuto, con 15 min de trabajo de la persona en el plan.

### Reglas de planificación del ejemplo

- Abrir en la cara con subtítulos: el espectador conecta antes de que pase nada.
- **Cuando anuncia algo nuevo, se ve su cara; cuando lo describe, se muestra.**
- El primer visual es el gancho: algo que se entiende solo (un gráfico que sube con cada «arriba»).
- Si la frase cambia de idea a la mitad, la escena también.
- Balance: que el video fluya y sea fácil de mirar, no un catálogo de efectos.

### Las correcciones del ejemplo (revisar antes de mostrar el v1)

Diseño de texto pobre en la primera escena · corte brusco entre dos animaciones · textura pesada que
no se mueve con la animación · corte a destiempo en un segundo puntual · una escena que se va antes de
poder leerla · faltaban las comillas en la escena final.
