---
name: nuevo-video
description: Producción completa de un video nuevo con el equipo de agentes — brief, guion con hooks, plan de edición, audio con ritmo, construcción en HyperFrames o Remotion, revisión y render final — con un OK de la persona en cada etapa. Usar cuando dice «hagamos un video», «nuevo video», «un anuncio de…», «un reel sobre…», «edita este material», o tras terminar las referencias.
---

# Nuevo video: de la idea al MP4

Antes de empezar lee `perfil/PERFIL.md`, `perfil/ESTILO.md`, `perfil/APRENDIZAJES.md` (si existe)
y `guias/lecciones.md`. Crea `proyectos/<AAAA-MM-DD-slug>/`. Cada etapa termina con algo que la
persona ve y aprueba; no avances sin ese OK.

## 0. Brief (tú, en la conversación)

Pregunta solo lo que falte (con opciones cuando se pueda) y guarda `brief.md`:
objetivo de este video · plataforma y formato · duración · mensaje central en una frase ·
público · CTA · material disponible (rutas) · qué referencia seguir más · fecha de entrega.
Si trae material grabado, desármalo primero: `python3 scripts/referencia.py <archivo> proyectos/<v>/material/<nombre>`
(planos, transcripción y ritmo de su propio material).

## 1. Guion (agente `guionista`)

Pásale las rutas de perfil, estilo, brief y aprendizajes. Devuelve `guion.md` con 5 hooks y el
guion por bloques. Muéstrale a la persona los hooks y la recomendación; que elija y apruebe el guion.

## 2. Plan de edición (tú)

Escribe `plan.md`, una fila por escena:

| # | tiempo | visual (qué se ve y qué se mueve) | texto en pantalla | transición de salida | sonido |

Y debajo:
- **Motor:** HyperFrames (por defecto) o Remotion, con la razón (`guias/motores.md`).
- **Assets:** qué hay, qué falta. Imágenes a generar = **un lote**: lista con prompt de cada una,
  tamaño y costo aproximado. Voz IA, efectos y música = otro lote (los arma el sonidista).
- Cada escena tiene acción propia: nada de fotos quietas con zoom lento como única idea.

Muestra el plan (o un storyboard rápido en HTML si ayuda) y pide OK. Con el OK de los lotes que
cuestan, corre `puerta.py permitir …` y genera tú (`imagen.py`, `eleven.py`).

## 3. Audio primero (agente `sonidista`)

La línea de tiempo se amarra al audio. El sonidista prepara `audio/pedidos.md` (voz, efectos,
música con prompts y costo), tú lo ejecutas tras el OK, y él arma `audio/cues.json`: tiempos de
cada palabra, beats, cortes sugeridos sobre el beat, efectos en cada transición y la mezcla.
Si la persona graba su voz: pídele el archivo, se limpia y se transcribe con tiempos.

## 4. Construcción (agente `editor`)

Pásale plan, cues, estilo, assets y motor. Construye en `video/`, revisa con las herramientas del
motor y deja hoja de contacto + avance (`out/avance-v1.mp4` en calidad borrador o la URL del preview).

## 5. Revisión (agente `revisor`, luego la persona)

El revisor mira el avance contra brief, estilo, guion, aprendizajes y reglas; devuelve
`revision.md` por gravedad. El editor corrige. Recién entonces **muéstrale el avance a la persona**
(hoja de contacto o video) y anota sus comentarios. Repite 4-5 hasta que apruebe.
Si cambia algo a mitad de una ronda, la ronda vieja queda obsoleta: aplica y revisa la nueva.

## 6. Entrega

- Render final en calidad de entrega (`guias/plataformas.md`: H.264, yuv420p, AAC 48 kHz,
  −14 LUFS, pico ≤ −1 dB). Verifica duración con `ffprobe` y mira cuadros del archivo final.
- Entrega `out/<slug>-final.mp4` (y versiones por formato si se pidieron) + la portada (primer
  cuadro o uno elegido).
- Anota en `perfil/APRENDIZAJES.md`: fecha, video, qué gustó, qué rechazó, qué regla sale de ahí.
- Limpieza: `node_modules`, `.cache`, avances superados, `rm -rf "$TMPDIR"/remotion-webpack-bundle-*`
  si se usó Remotion y no hay otro render corriendo.
