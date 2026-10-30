---
name: instalar
description: Instala y verifica todo lo que el estudio de video necesita (ffmpeg, yt-dlp, whisper y su modelo, Node 22+, HyperFrames, skills de Remotion, guion, marketing, sonido y find-skills) y configura las keys opcionales de ElevenLabs y OpenAI. Usar al abrir el repo por primera vez, cuando el estado marca ✗, o cuando la persona dice «instala», «configura», «no funciona», «falta algo».
---

# Instalar el estudio

1. Corre `bash scripts/kit.sh estado` y cuéntale a la persona en 3-4 líneas qué falta.
2. Si el estado avisa **menos de 20 GB libres**, díselo antes de seguir: el modelo de whisper pesa
   ~0,6 GB y cada render deja ~0,7 GB temporales. Con su OK, `bash scripts/kit.sh instalar --si`;
   si hay espacio, `bash scripts/kit.sh instalar`. Corre en segundo plano si tarda más de 2 minutos.
3. Si falta Homebrew (Mac) o algo en Linux, el script dice qué instalar a mano: pásale el comando
   exacto en su propio bloque para que lo copie. No pidas su contraseña.
4. Vuelve a correr el estado y confirma con ✓ lo que quedó.

## Keys (opcionales)

Sin keys el estudio funciona: su voz grabada, sonidos libres (HyperFrames trae efectos y música
local) y cero imágenes generadas. Con keys:

- **ElevenLabs**: voz IA, efectos y música. https://elevenlabs.io/app/settings/api-keys
- **OpenAI**: imágenes puntuales. https://platform.openai.com/api-keys

Pídele que abra `.env` (ya existe, copiado de `.env.example`) y pegue ahí cada key. **Nunca en el
chat**; si la pega en el chat, dile que quedó registrada en la conversación y que la rote.
Verifica sin gastar: `python3 scripts/eleven.py saldo` (gratis). OpenAI no tiene llamada gratis
de prueba: se verifica con la primera imagen aprobada.

## Qué instala y para qué (por si pregunta)

| Pieza | Para qué |
|---|---|
| ffmpeg, ffprobe | cortar, medir, sacar cuadros, mezclar |
| yt-dlp | bajar referencias de YouTube, Instagram y TikTok |
| whisper.cpp + modelo large-v3-turbo | transcribir con tiempos, local y gratis |
| Node 22+ / HyperFrames | motor principal de edición; trae `audio` (beats, secciones), `snapshot`, `check` |
| Remotion (skills) | segundo motor, React; se crea por proyecto con `npx create-video` |
| skills de guion | copywriting, storybrand-messaging, made-to-stick, scriptwriting, ad-hook-analyzer, ugc-ad-scripts |
| skills de marketing | video, social, ad-creative, marketing-psychology, content-strategy |
| skills de sonido | text-to-speech, sound-effects, music (ElevenLabs) |
| skills de animación | gsap, animation-vocabulary, cinetic |
| find-skills | buscar más skills: `npx skills find <tema>` |

Al terminar sigue con `/referencias`: «Para empezar, pásame tus referencias».
