# Estudio de video con IA

Convierte a Claude Code en un estudio de edición de video: estudia los videos que te gustan, te
entrevista, escribe el guion, arma el audio al ritmo de la música, edita con **HyperFrames** o
**Remotion** y revisa cada avance cuadro a cuadro antes de mostrártelo.

- Edición, animación, subtítulos y mezcla: HyperFrames (HTML + GSAP) y Remotion (React).
- Imágenes generadas con OpenAI solo cuando un plano lo necesita.
- Voz, efectos y música con ElevenLabs si tienes key; si no, tu voz, una voz guía local gratis y
  sonidos libres.

**¿Primera vez? Lee [COMO-USARME.md](COMO-USARME.md)**: qué necesitas, cómo instalarlo, cómo
pedir videos y cambios, dónde queda cada cosa y qué hacer si algo falla.

## Empezar

Necesitas una Mac (o Linux), [Claude Code](https://claude.com/claude-code) (app de Claude con plan
Pro o Max, o la terminal) y ~20 GB libres.

**Desde la app de Claude:** abre Claude Code en cualquier carpeta y pega

> Clona https://github.com/tamibot/estudio-video-ia en ~/Developer/estudio-video-ia

y abre una **sesión nueva** con la carpeta `~/Developer/estudio-video-ia`. Escribe «hola».

**Desde la terminal:**

```bash
git clone https://github.com/tamibot/estudio-video-ia.git ~/Developer/estudio-video-ia
```

```bash
cd ~/Developer/estudio-video-ia && claude
```

Acepta la confianza en la carpeta (activa la revisión de inicio). Si la Mac pide instalar las
herramientas de desarrollo de Apple, acepta y espera. Guárdalo en una carpeta local, no en iCloud,
Dropbox ni Drive.

## El recorrido

Claude revisa qué falta al abrir y te lleva paso a paso:

1. **`/instalar`** — ffmpeg, yt-dlp, whisper (con VAD), auto-editor, HyperFrames, la voz local y
   las skills. Una sola vez, ~3 GB y 10-20 minutos.
2. **`/referencias`** — «Pásame tus referencias»: 3 a 5 videos que te gusten (Instagram, TikTok,
   YouTube o archivos). Los desarma cuadro a cuadro, mide el ritmo contra la música, la luz y el
   color, y arma tu biblia de estilo. Para copiar a un creador puntual, **modo entrenar**: hasta 20
   videos suyos, tablero en Figma por tipo de escena, biblioteca de animaciones y una skill del estilo.
3. **`/empezar`** — el Director te entrevista: para qué son tus videos, dónde se publican, quién
   eres, a quién le hablas, tu tono y tu identidad.
4. **`/nuevo-video`** — guion nuevo: brief → guion con 5 ganchos → plan → audio → avance → rondas
   de cambios → MP4 final. Con **tu grabación** (talking head): silencios fuera → transcripción al
   milisegundo → **documento de planificación** donde eliges el diseño de cada momento → construcción
   → correcciones → diseño sonoro. Te pide OK en cada etapa y antes de gastar.

Estilo listo para usar: **minimal premium** (talking head educativo con papel, texto de dos
fuentes, pinturas, líneas azules e ilustraciones), en la skill `estilo-minimal-premium` y
`plantillas/minimal-premium/`. El método de entrenar y editar viene del tutorial de Joseph
(Ultimate Editors), [*How to Edit VIRAL Talking Head Videos Using ONLY Claude!*](https://www.youtube.com/watch?v=g9xoKm5DEeU).

`/ayuda` en cualquier momento: dónde vas, qué sigue y qué puedes decir.

## El equipo

| Agente | Hace |
|---|---|
| Director (la conversación) | entrevista, plan, aprobaciones, gasto |
| `analista-referencias` | mira láminas y transiciones de cada referencia y escribe la receta |
| `guionista` | ganchos y guion con StoryBrand, Made to Stick y copywriting |
| `sonidista` | voz, música, efectos, cortes sobre el beat, mezcla a −14 LUFS |
| `editor` | limpia el material, construye en HyperFrames o Remotion y entrega avances |
| `revisor` | revisa cuadros reales contra el brief, el estilo y tus rechazos |

## Herramientas

Propias (`scripts/`):

| Script | Para |
|---|---|
| `kit.sh` | `estado` (qué falta), `instalar`, `voz` (voz guía local), `limpiar` (disco tras una entrega) |
| `referencia.py` | desarma un video: planos, cortes secos y animados, láminas, transcripción, bpm, beats, % de cortes en el beat, luz y color |
| `eleven.py` | voz, efectos y música con ElevenLabs |
| `imagen.py` | imágenes puntuales con OpenAI, con el prompt guardado al lado |
| `plan_edicion.py` | documento de planificación: guion y clip de cada momento, diseños recomendados, tus notas y «Copiar plan» |
| `assets.py` | pinturas y fotos de dominio público (Wikimedia Commons) y B-roll de stock (Pexels), con créditos |
| `puerta.py` | contador compartido de cuotas: espacia descargas, frena ante 429 y exige permiso por lote para lo que cuesta |

Externas que instala: [HyperFrames](https://github.com/heygen-com/hyperframes) (motor, auditoría
`check`, cuadros `snapshot`, `audio`, `measure`, `diff`, `tts`),
[Remotion](https://www.remotion.dev), [auto-editor](https://github.com/WyattBlue/auto-editor)
(silencios y exportación a Premiere/Resolve/Final Cut), [whisper.cpp](https://github.com/ggml-org/whisper.cpp)
con VAD Silero, [yt-dlp](https://github.com/yt-dlp/yt-dlp), ffmpeg y
[Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voz local). Skills: HyperFrames, Remotion,
GSAP, auto-editor, ElevenLabs, copywriting y marketing, StoryBrand, Made to Stick, guiones,
ganchos de anuncios, cinetic y `find-skills` para buscar más (`npx skills find <tema>`). Las skills
se instalan **dentro del proyecto** (`.claude/skills/`, fuera de git): no tocan las de tu usuario.

## Guías (`guias/`)

`entrenar-un-estilo.md` (el método completo) · `estilos.md` · `ritmo-y-transiciones.md` · `audio.md` ·
`motores.md` · `plataformas.md` · `lecciones.md` (todo lo que ya costó una ronda de corrección).

## Tus datos y tus keys

`perfil/`, `referencias/`, `proyectos/` y `.env` quedan en tu máquina: están en `.gitignore`.
Tus videos terminados quedan en `proyectos/<fecha-nombre>/out/<nombre>-final.mp4`.
Las keys van en `.env` (copiado de `.env.example`), nunca en el chat.

## Costos

Local y gratis: analizar, transcribir, limpiar material, editar, la voz guía y renderizar.
Cuestan: ElevenLabs y OpenAI con tu key (antes de cada lote Claude te dice qué va a generar,
cuántas llamadas y el costo aproximado, y espera tu OK), y las funciones en la nube de HyperFrames
(publicar, renders en la nube, avatares), que el repo nunca usa sin preguntar. Remotion es gratis
para personas y equipos de hasta 3; empresas más grandes necesitan [su licencia](https://www.remotion.pro/license).

## Actualizar

```bash
bash ~/Developer/estudio-video-ia/scripts/kit.sh actualizar
```

Tu perfil, tus referencias y tus proyectos no se tocan.
