---
name: nuevo-video
description: Producción completa de un video con el equipo de agentes — guion nuevo (brief, hooks, plan, audio, construcción, revisión, render) o material grabado / talking head (silencios fuera, transcripción al milisegundo, documento de planificación que decide la persona, assets, construcción, correcciones y diseño sonoro al final) — con un OK de la persona en cada etapa. Usar cuando dice «hagamos un video», «nuevo video», «un anuncio de…», «un reel sobre…», «edita este material», o tras terminar las referencias.
---

# Nuevo video: de la idea al MP4

Antes de empezar lee `perfil/PERFIL.md`, `perfil/ESTILO.md`, `perfil/APRENDIZAJES.md` (si existe)
y `guias/lecciones.md`. Crea `proyectos/<AAAA-MM-DD-slug>/`. Cada etapa termina con algo que la
persona ve y aprueba; no avances sin ese OK.

Hay dos caminos según el material:

- **Material grabado** (talking head, clase, podcast, entrevista: la voz ya existe) → el camino de
  abajo, «Editar material grabado». Es el método de `guias/entrenar-un-estilo.md` (parte 2).
- **Guion nuevo** (anuncio, explicativo, animación sin grabar) → de la etapa 0 a la 6.

## Editar material grabado (talking head)

1. **Brief corto** (etapa 0) y el clip a `proyectos/<v>/material/bruto.<ext>` (que lo arrastre al chat).
2. **Limpiar y transcribir** (avísale: ~15 min en un clip de 1-3 min):
   - Silencios fuera dejando 30 ms de aire:
     `auto-editor proyectos/<v>/material/bruto.mp4 --edit audio:threshold=0.04 --margin 0.03s -o proyectos/<v>/material/limpio.mp4 --no-open`
     (si suena atropellado, `--margin 0.08s`; muéstrale el resultado).
   - Transcripción palabra por palabra al milisegundo del clip limpio: `ffmpeg -i proyectos/<v>/material/limpio.mp4 -ar 16000 -ac 1 proyectos/<v>/material/limpio.wav`
     y `whisper-cli -m <modelo> -l <idioma> -ml 1 -sow -oj --vad -vm ~/modelos-whisper/vad-silero-v5.1.2.bin -dtw large.v3.turbo -nfa -f proyectos/<v>/material/limpio.wav -of proyectos/<v>/material/palabras`
     (deja `palabras.json`; el `clip` de `plan.json` es `material/limpio.mp4`, relativo a `plan.json`).
     Control: la última palabra debe terminar cerca del final del clip y no debe haber huecos de más
     de 1 s con voz; whisper a veces se salta una frase (sobre todo si se repite): transcribe ese
     tramo aparte (`ffmpeg -ss <a> -to <b>`) y súmalo con su desfase.
3. **Documento de planificación.** Parte el guion en beats (una idea o media frase, 1,5-4 s) y para
   cada uno propone 2-3 diseños del estilo (skill `estilo-…` y su `perfil/biblioteca/`, o
   `estilo-minimal-premium`), con la imagen de referencia (`ref`) y en `visto_en` dónde y por qué el
   creador usa ese diseño. Aplica sus reglas de planificación al ordenar las opciones (la primera es
   la recomendada). Escribe `proyectos/<v>/plan.json` y:
   `python3 scripts/plan_edicion.py proyectos/<v>/plan.json` → `open proyectos/<v>/plan.html`.
4. **La persona planifica** (el paso más importante): en el documento elige un diseño por beat o
   escribe el suyo, y aprieta «Copiar plan». Cuando pegue el plan en el chat, guárdalo en `plan.md`.
   No construyas sin plan: la IA sola planifica peor que la persona.
5. **Lista de assets** en `pedidos.md` (pinturas, B-roll, fotos, ilustraciones, fuentes) y búsqueda:
   `python3 scripts/assets.py pinturas|fotos|broll "<búsqueda en inglés>" proyectos/<v>/assets/<tipo>`
   (gratis; B-roll pide `PEXELS_API_KEY`). Lo que no aparezca: pídeselo a la persona o, si suma y
   con su OK de costo, `imagen.py`. Puedes usar el navegador para buscar, nunca para descargar algo
   con licencia dudosa.
6. **Construcción** (agente `editor`): fuentes del estilo, subtítulos del A-roll con el texto
   cinemático, luego escena por escena según `plan.md` (copiando de `plantillas/` cuando exista la
   escena) → `out/avance-v1.mp4` y `open`. Dile que el v1 suele quedar al 60-70 %.
7. **Correcciones** (revisor primero, luego la persona, «segundo + qué cambiar»), hasta que diga que
   la imagen está lista.
8. **Diseño sonoro al final** (agente `sonidista`, con la imagen aprobada): música y efectos como los
   usa el estilo (en el minimal premium: click en textos, trazo en líneas y gráficos, whoosh en
   entradas de cámara, golpe suave en palabras clave), mezcla −14 LUFS → etapa 6 (entrega).

## 0. Brief (tú, en la conversación)

Pregunta solo lo que falte (con opciones cuando se pueda) y guarda `brief.md`:
objetivo de este video · plataforma y formato · duración · mensaje central en una frase ·
público · CTA · material disponible (rutas) · qué referencia seguir más · fecha de entrega.
Si trae material grabado, desármalo primero: `python3 scripts/referencia.py <archivo> proyectos/<v>/material/<nombre>`
(planos, transcripción y ritmo de su propio material). Si es un talking head o una grabación con
pausas, propón limpiarlo con `auto-editor` (`guias/motores.md`) y muéstrale el resultado.

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

Muestra el plan (o un storyboard rápido en HTML si ayuda) y pide OK. Los subagentes dejan lo que
haga falta generar en `proyectos/<v>/pedidos.md`. Con el OK de los lotes que cuestan, corre
`puerta.py permitir …` y genera tú (`imagen.py`, `eleven.py`).

## 3. Audio primero (agente `sonidista`)

La línea de tiempo se amarra al audio. El sonidista prepara `audio/pedidos.md` (voz, efectos,
música con prompts y costo), tú lo ejecutas tras el OK, y él arma `audio/cues.json`: tiempos de
cada palabra, beats, cortes sugeridos sobre el beat, efectos en cada transición y la mezcla.
Si la persona graba su voz: pídele el archivo, se limpia y se transcribe con tiempos.

## 4. Construcción (agente `editor`)

Pásale plan, cues, estilo, assets y motor. Construye en `video/`, revisa con las herramientas del
motor y deja hoja de contacto + avance (`out/avance-v1.mp4` en calidad borrador o la URL del preview).
Para mostrarlo: `open proyectos/<v>/out/avance-v1.mp4` (se abre en el reproductor de su Mac).

## 5. Revisión (agente `revisor`, luego la persona)

El revisor mira el avance contra brief, estilo, guion, aprendizajes y reglas; devuelve
`revision.md` por gravedad. El editor corrige. Recién entonces **muéstrale el avance a la persona**
(`open …/avance-vN.mp4` o la hoja de contacto) y explícale cómo pedir cambios: «dime el segundo y
qué cambiar: *0:04 el texto más grande*, *0:10 corta antes*, *la música más baja*». Anota cada
comentario en `revision.md`. Repite 4-5 rondas hasta que apruebe.
Si cambia algo a mitad de una ronda, la ronda vieja queda obsoleta: aplica y revisa la nueva.

## 6. Entrega

- Render final en calidad de entrega (`guias/plataformas.md`: H.264, yuv420p, AAC 48 kHz,
  −14 LUFS, pico ≤ −1 dB). Verifica duración con `ffprobe` y mira cuadros del archivo final.
- Entrega `out/<slug>-final.mp4` (y versiones por formato si se pidieron) + la portada (primer
  cuadro o uno elegido). Muéstrale dónde quedó: `open -R proyectos/<v>/out/<slug>-final.mp4`.
- Anota en `perfil/APRENDIZAJES.md`: fecha, video, qué gustó, qué rechazó, qué regla sale de ahí.
- Limpieza: `bash scripts/kit.sh limpiar proyectos/<v>` (dependencias, cachés y temporales de
  Remotion; no corre si hay otro render en marcha) y borra los avances superados de `out/`.
