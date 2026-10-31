---
name: instalar
description: Instala y verifica todo lo que el estudio de video necesita (ffmpeg, yt-dlp, whisper y su modelo, Node 22+, HyperFrames, voz local Kokoro, skills de Remotion, guion, marketing, sonido y find-skills) y configura las keys opcionales de ElevenLabs y OpenAI. Usar al abrir el repo por primera vez, cuando el estado marca ✗, o cuando la persona dice «instala», «configura», «no funciona», «falta algo».
---

# Instalar el estudio

1. Corre `bash scripts/kit.sh estado` y cuéntale a la persona en 3-4 líneas qué falta y que la
   instalación completa ocupa ~3 GB y tarda de 10 a 20 minutos la primera vez.
2. Si el estado avisa **menos de 20 GB libres**, díselo antes de seguir: herramientas y modelos
   ocupan ~3 GB y cada render deja temporales. Con su OK, `bash scripts/kit.sh instalar --si`;
   si hay espacio, `bash scripts/kit.sh instalar`. **Siempre en segundo plano** (Homebrew tarda) y
   avísale en una línea mientras tanto.
3. Si el script se detiene pidiendo algo a mano, pásale los comandos que imprime, cada uno en su
   propio bloque, y dile: «ábrelos en la app **Terminal** (pide la contraseña de tu Mac, que no
   me tienes que dar); cuando termine, cierra y vuelve a abrir Claude Code y escríbeme *listo*».
   En una Mac nueva suele pasar dos veces:
   - Herramientas de Apple: `xcode-select --install` → aceptar la ventana y esperar.
   - Homebrew:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
     ```bash
     echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
     ```
   Nunca pidas su contraseña ni la escribas tú.
4. Vuelve a correr el estado y confirma con ✓ lo que quedó.

## Keys (opcionales)

Sin keys el estudio funciona: su voz grabada, sonidos libres (HyperFrames trae efectos y música
local) y cero imágenes generadas. Con keys:

- **ElevenLabs**: voz IA, efectos y música. https://elevenlabs.io/app/settings/api-keys
- **OpenAI**: imágenes puntuales. https://platform.openai.com/api-keys

Pídele que abra `.env` (ya existe, copiado de `.env.example`; es un archivo oculto) con
`open -e .env` (lo abres tú y se abre en TextEdit), pegue cada key después del `=`, guarde y te
avise. **Nunca en el chat**; si la pega en el chat, dile que quedó registrada en la conversación y
que la rote (que cree una nueva en la página del servicio y borre la vieja).
Verifica sin gastar: `python3 scripts/eleven.py saldo` (gratis). OpenAI no tiene llamada gratis
de prueba: se verifica con la primera imagen aprobada.

## Qué instala y para qué (por si pregunta)

| Pieza | Para qué |
|---|---|
| ffmpeg, ffprobe | cortar, medir, sacar cuadros, mezclar |
| yt-dlp | bajar referencias de YouTube, Instagram y TikTok |
| whisper.cpp + modelo large-v3-turbo | transcribir con tiempos, local y gratis |
| uv + Kokoro (`kit.sh voz`) | voz IA guía, local y gratis (español: ef_dora, em_alex) |
| VAD Silero para whisper | que whisper no invente texto en silencios o en música |
| auto-editor (+ 4 skills) | quitar silencios de grabaciones y exportar a Premiere, Resolve o Final Cut |
| Node 22+ / HyperFrames | motor principal de edición; trae `audio` (beats, secciones), `snapshot`, `check` |
| Remotion (skills) | segundo motor, React; se crea por proyecto con `npx create-video` |
| skills de guion | copywriting, storybrand-messaging, made-to-stick, scriptwriting, ad-hook-analyzer, ugc-ad-scripts |
| skills de marketing | video, social, ad-creative, marketing-psychology, content-strategy |
| skills de sonido | text-to-speech, sound-effects, music (ElevenLabs) |
| skills de animación | gsap-core, gsap-timeline, animation-vocabulary, cinetic |
| find-skills | buscar más skills: `npx skills find <tema>` |

Todas las skills quedan **dentro del proyecto**, en `.claude/skills/` (fuera de git, anotadas en
`skills-lock.json`): no se mezclan con las de otros proyectos de la persona ni dependen de lo que
tenga instalado en su usuario. Para traerlas a su última versión: `bash scripts/kit.sh actualizar`.

Al terminar sigue con `/referencias`: «Para empezar, pásame tus referencias».
