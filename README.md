# Estudio de video con IA

Un repositorio que convierte a Claude Code en un estudio de edición de video: te entrevista,
estudia tus videos de referencia, escribe el guion, arma el audio al ritmo de la música, construye
el video con **HyperFrames** o **Remotion** y lo revisa antes de entregártelo.

- Edición, animación, subtítulos y mezcla: HyperFrames (HTML + GSAP) y Remotion (React).
- Imágenes generadas con OpenAI solo cuando un plano lo necesita.
- Voz, efectos y música con ElevenLabs si tienes key; si no, tu voz y sonidos libres.

## Empezar

```bash
git clone <este repo> ~/Developer/estudio-video-ia
```

```bash
cd ~/Developer/estudio-video-ia && claude
```

Escribe «hola». Claude revisa qué falta y te lleva paso a paso:

1. **`/instalar`** — ffmpeg, yt-dlp, whisper, HyperFrames y las skills (una sola vez).
2. **`/referencias`** — «Pásame tus referencias»: 3 a 5 videos que te gusten (Instagram, TikTok,
   YouTube o archivos). Los desarma cuadro a cuadro, mide el ritmo contra la música y arma tu
   biblia de estilo.
3. **`/empezar`** — el Director te entrevista: para qué son tus videos, dónde se publican, qué
   estilo seguimos (partiendo de tus referencias), quién eres y a quién le hablas.
4. **`/nuevo-video`** — brief → guion con hooks → plan → audio → construcción → revisión → MP4.
   Te pide OK en cada etapa y antes de gastar.

Clónalo en una carpeta local (no en iCloud, Dropbox ni Drive). Requisitos: macOS o Linux, ~2 GB
libres para herramientas y el modelo de whisper, más espacio para renders.

## El equipo

| Agente | Hace |
|---|---|
| Director (la conversación) | entrevista, plan, aprobaciones, gasto |
| `analista-referencias` | mira láminas y transiciones de cada referencia y escribe la receta |
| `guionista` | hooks y guion con StoryBrand, Made to Stick y copywriting |
| `sonidista` | voz, música, efectos, cortes sobre el beat, mezcla a −14 LUFS |
| `editor` | construye en HyperFrames o Remotion y entrega avances |
| `revisor` | revisa cuadros reales contra el brief, el estilo y tus rechazos |

## Herramientas propias (`scripts/`)

| Script | Para |
|---|---|
| `kit.sh` | `estado` (qué falta) e `instalar` |
| `referencia.py` | desarma un video: planos, cortes secos y animados, láminas, transcripción, bpm, beats, % de cortes en el beat |
| `eleven.py` | voz, efectos y música con ElevenLabs |
| `imagen.py` | imágenes puntuales con OpenAI, con el prompt guardado al lado |
| `puerta.py` | contador compartido de cuotas: espacia descargas, frena ante 429 y exige permiso por lote para lo que cuesta |

## Guías (`guias/`)

`estilos.md` · `ritmo-y-transiciones.md` · `audio.md` · `motores.md` · `plataformas.md` ·
`lecciones.md` (todo lo que ya costó una ronda de corrección).

## Tus datos y tus keys

`perfil/`, `referencias/`, `proyectos/` y `.env` quedan en tu máquina: están en `.gitignore`.
Las keys van en `.env` (copiado de `.env.example`), nunca en el chat.

## Costos

Todo es local y gratis salvo ElevenLabs y OpenAI. Antes de cada lote Claude te dice qué va a
generar, cuántas llamadas y el costo aproximado, y espera tu OK (`puerta.py permitir`).

## Referencias externas

- HyperFrames: https://github.com/heygen-com/hyperframes
- Remotion: https://www.remotion.dev
- Skills: https://skills.sh (buscar más con `npx skills find <tema>`)
- Otro kit de la comunidad: [Claude Code Video Toolkit](https://github.com/wilwaldon/Claude-Code-Video-Toolkit)
