# HyperFrames o Remotion

Los dos renderizan código a MP4 de forma determinista. Elegir uno por proyecto y decirlo en `plan.md`.

| | HyperFrames (por defecto) | Remotion |
|---|---|---|
| Qué es | HTML + CSS + GSAP renderizado a video | React renderizado a video |
| Mejor para | motion graphics, texto cinético, anuncios, explicativos, interfaces, overlays | mucho material propio que cortar, plantillas con datos, series de videos iguales |
| Ventajas | registro de ~450 bloques (transiciones, subtítulos, títulos), `check` y `snapshot` para que el agente vea, `audio` y `beats` integrados, estudio visual | ecosistema React, `@remotion/transitions`, `@remotion/captions`, `@remotion/sfx`, Studio con recarga en vivo |
| Arranque | `npx hyperframes init video --non-interactive --resolution portrait` | `npx create-video@latest --yes --blank --no-tailwind video` |
| Skills | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | `remotion-best-practices`, `remotion-create`, `remotion-captions` |
| Licencia | libre | libre para personas y equipos de hasta 3; empresas más grandes, licencia de pago (remotion.pro/license) |

Si la persona ya tiene algo hecho en Remotion (u otra herramienta) y quiere pasarlo: skill `remotion-to-hyperframes`.

## Antes del motor: material grabado (auto-editor)

Para un talking head, una clase o una grabación de pantalla, primero se limpia el material con
`auto-editor` (local, gratis; skills `auto-editor`, `auto-editor-effects`, `auto-editor-export`,
`auto-editor-transcribe`). Nunca pisa el original: escribe un archivo nuevo.

| Para | Comando |
|---|---|
| Quitar silencios dejando aire natural | `auto-editor in.mp4 --edit audio:threshold=0.04 --margin 0.2s -o material/limpio.mp4 --no-open` |
| Acelerar en vez de cortar | `… --when-silent speed:4` (ver la skill `auto-editor-effects`) |
| Cortar por lo que se dice (quitar «eh», una frase repetida) | skill `auto-editor-transcribe` |
| Llevar el corte a Premiere, Resolve o Final Cut | `auto-editor in.mp4 --edit audio --export premiere -o proyecto.xml --no-open` (o `resolve`, `final-cut-pro`) |

Probado: 6 s con 4 s de silencio → 2,2 s. Mostrar el resultado antes de seguir: a veces corta
respiraciones que daban ritmo; subir `--margin` a 0,3–0,4 s si suena atropellado.

## Ciclo HyperFrames

1. Dentro de `proyectos/<v>/`: `npx hyperframes init video --non-interactive --resolution portrait`
   (`landscape`, `square`; sin `--resolution` sale 1920x1080). Con material grabado:
   `--video <archivo>` lo convierte a H.264 y lo transcribe. Crea su propio `CLAUDE.md` con el
   contrato de render: léelo.
2. Escribir; `npx hyperframes lint` tras cada cambio de estructura (escenas con contenido adentro
   van como subcomposiciones, `data-composition-src`).
3. `npx hyperframes check --json` y arreglar todo (contraste, layout, movimiento, cierre legible).
4. `npx hyperframes snapshot --review` (inicio y medio de cada escena, cada corte, vista de
   celular) o `--at 0.5,3,7.2` → quedan en `.hyperframes/artifacts/snapshots/<id>/` con
   `contact-sheet.jpg`. Salen de ~1800 px: achicar a ≤ 768 px antes de mirar.
5. `npx hyperframes preview --background` para que la persona lo vea en vivo (`--stop` al terminar).
6. `npx hyperframes render --quality draft --output ../out/avance-v1.mp4` (avances, ~25 s por
   4 s de video); `--quality delivery` para el final. Verificar duración con `ffprobe` y mirar cuadros.
7. Al entregar: `bash scripts/kit.sh limpiar proyectos/<v>` (usa además `npx hyperframes clean`).

## Ciclo Remotion

1. `npx create-video@latest --yes --blank --no-tailwind video` (ya instala dependencias, ~0,3 GB)
   y `npx remotion add @remotion/transitions @remotion/captions` (mismas versiones que remotion).
2. El blank sale 1280x720: en `<Composition>` fija `width={1080} height={1920} fps={30}` (o el
   formato del plan) y `durationInFrames` = `duracion × fps` de `cues.json`.
3. Escenas en `<TransitionSeries>` con la fórmula de `guias/ritmo-y-transiciones.md` (la transición
   resta cuadros); el `<Audio>` fuera de la serie.
4. `npx remotion studio` para la persona; `npx remotion still <id> out/f60.png --frame=60` para mirar cuadros.
5. `npx remotion render <id> ../out/avance-v1.mp4`.
6. Al terminar: `bash scripts/kit.sh limpiar proyectos/<v>` (borra `node_modules` y los paquetes
   temporales de Remotion, ~0,7 GB por render).

## Más herramientas de HyperFrames (locales y gratis)

Con una cuenta gratis de HeyGen (`npx hyperframes auth login`, con OK de la persona) `media-use`
también busca en un catálogo grande de música, imágenes e íconos; generar con ella sí gasta créditos.

| Para | Comando |
|---|---|
| Medir un video (cortes, eventos, luz, cara, sincronía labios-voz) | `npx hyperframes measure <cuts · events --map · look · face · sync> <video> --json` |
| Comparar nuestro render con una referencia cuadro a cuadro | `npx hyperframes diff referencia.mp4 out/avance-v1.mp4` · `snapshot --against referencia.mp4` |
| Voz IA local (Kokoro) | `bash scripts/kit.sh voz …` (envuelve `npx hyperframes tts`) |
| Transcribir con tiempos por palabra / exportar SRT | `npx hyperframes transcribe voz.wav --language es --model small` · `--to srt` |
| Quitar el fondo de un video o imagen | `npx hyperframes remove-background persona.mp4` |
| Igualar volumen entre pistas | `npx hyperframes normalize-audio` |
| Elegir un look de color | `npx hyperframes grade-compare` |
| Grabar una web para usarla en el video | `npx hyperframes capture <url>` |
| Revisar el sistema / limpiar disco | `npx hyperframes doctor` · `npx hyperframes clean --snapshots` |
| No mandar estadísticas de uso | `npx hyperframes telemetry disable` |

**Cuestan o publican (solo con OK de la persona, la configuración del repo pregunta):** `publish`,
`cloud`, `lambda`, `cloudrun`, `auth`, `billing`, `media-use generate` (HeyGen),
`transcribe --engine heygen`, `audio --quality best`. En Remotion: `lambda` y `cloudrun`.

## Trampas conocidas

- **Fuentes**: medir y ajustar tamaños de texto recién después de que cargan
  (`document.fonts.ready` / `delayRender` hasta `fonts.load`). Si no, se mide con la fuente de
  reemplazo y los títulos quedan cortados.
- **Tildes en máscaras**: en entradas con máscara, la tilde asoma por encima; ocultar el texto
  hasta que empiece a subir.
- **Contorno**: `color: transparent` con `-webkit-text-stroke: currentColor` sale invisible; usar
  el color explícito.
- **Sacudón de cámara**: el fondo de la página tiene que ser el color de la escena, o asoma el borde.
- **Animación ligada al tiempo**: todo se calcula desde el tiempo del cuadro (render(t) puro).
  Nada de `setTimeout`, `Math.random()` sin semilla ni animaciones CSS libres.
- **npm**: si `npm i` falla con 404 de `electron-to-chromium`, fijar una versión anterior en
  `overrides` del package.json.
- **ffmpeg 7+** ya no acepta `-vsync` (usar `-fps_mode`); el de Homebrew no trae `drawtext`
  (los textos van en el motor, no en ffmpeg).
- **macOS**: no existe `timeout`; `sed -i` pide sufijo (`sed -i ''`).
- **Nube**: archivos de iCloud/Dropbox «solo en la nube» cuelgan Chrome y ffmpeg sin error.
  Trabajar en una carpeta local.
