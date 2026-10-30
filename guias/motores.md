# HyperFrames o Remotion

Los dos renderizan código a MP4 de forma determinista. Elegir uno por proyecto y decirlo en `plan.md`.

| | HyperFrames (por defecto) | Remotion |
|---|---|---|
| Qué es | HTML + CSS + GSAP renderizado a video | React renderizado a video |
| Mejor para | motion graphics, texto cinético, anuncios, explicativos, interfaces, overlays | mucho material propio que cortar, plantillas con datos, series de videos iguales |
| Ventajas | registro de ~450 bloques (transiciones, subtítulos, títulos), `check` y `snapshot` para que el agente vea, `audio` y `beats` integrados, estudio visual | ecosistema React, `@remotion/transitions`, `@remotion/captions`, `@remotion/sfx`, Studio con recarga en vivo |
| Arranque | `npx hyperframes init video` | `npx create-video@latest --yes --blank --no-tailwind video` |
| Skills | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | `remotion-best-practices`, `remotion-create`, `remotion-captions` |

Si la persona ya tiene algo en Remotion y quiere pasarlo: skill `remotion-to-hyperframes`.

## Ciclo HyperFrames

1. `npx hyperframes init video` dentro de `proyectos/<v>/`.
2. Escribir; `npx hyperframes lint` tras cada cambio de estructura.
3. `npx hyperframes check --json` y arreglar todo (contraste, layout, nada estático 3 s).
4. `npx hyperframes snapshot --at 0.5,3,7.2` → mirar los PNG de `.hyperframes/artifacts/snapshots/`.
5. `npx hyperframes preview --background` para que la persona lo vea en vivo.
6. `npx hyperframes render --quality draft --output ../out/avance-v1.mp4` (avances);
   `--quality delivery` para el final. Verificar duración con `ffprobe` y mirar cuadros.

## Ciclo Remotion

1. `npx create-video@latest --yes --blank --no-tailwind video` y `npm i`.
2. Escenas en `<TransitionSeries>`; tiempos desde `audio/cues.json` (segundos × fps).
3. `npx remotion studio` para la persona; `npx remotion still <id> --frame=N` para mirar cuadros.
4. `npx remotion render <id> ../out/avance-v1.mp4`.
5. Al terminar: `rm -rf "$TMPDIR"/remotion-webpack-bundle-*` (cada render deja ~0,7 GB) si no
   hay otro render corriendo.

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
