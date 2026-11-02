#!/usr/bin/env bash
# Kit del estudio de video.
#   bash scripts/kit.sh estado          qué está listo y qué falta (Claude lo corre solo al abrir el repo)
#   bash scripts/kit.sh instalar [--si] herramientas, modelo de whisper, voz local y skills; se puede repetir sin miedo
#   bash scripts/kit.sh voz <texto|guion.txt> <salida.wav> [voz]   voz IA local y gratis (Kokoro; es: ef_dora, em_alex)
#   bash scripts/kit.sh limpiar <proyectos/carpeta>                borra dependencias, cachés y temporales de un video entregado
#   bash scripts/kit.sh actualizar      trae la última versión del estudio y de sus skills (perfil y proyectos no se tocan)
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"  # Homebrew recién instalado aún no está en el PATH de Claude
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

# repo de skills | qué instalar ('*' = todas) | cuáles mirar para saber si ya está
SKILLS=(
  "heygen-com/hyperframes|*|hyperframes hyperframes-cli hyperframes-registry media-use remotion-to-hyperframes"
  "remotion-dev/skills|*|remotion-best-practices remotion-create remotion-captions"
  "vercel-labs/skills|find-skills|find-skills"
  "coreyhaines31/marketingskills|copywriting copy-editing video social ad-creative marketing-psychology content-strategy marketing-ideas|copywriting video social ad-creative marketing-psychology"
  "wondelai/skills|storybrand-messaging made-to-stick|storybrand-messaging made-to-stick"
  "gtmagents/gtm-agents|scriptwriting|scriptwriting"
  "mbfinotti/advertising-skills|ad-hook-analyzer ugc-ad-scripts ad-creative-brief|ad-hook-analyzer ugc-ad-scripts"
  "elevenlabs/skills|text-to-speech sound-effects music|text-to-speech sound-effects"
  "greensock/gsap-skills|gsap-core gsap-plugins gsap-timeline|gsap-core gsap-timeline"
  "emilkowalski/skills|animation-vocabulary|animation-vocabulary"
  "Leonxlnx/cinetic|cinetic|cinetic"
  "WyattBlue/auto-editor|*|auto-editor-export auto-editor-transcribe"
)
MODELO_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin"
VAD_URL="https://huggingface.co/ggml-org/whisper-vad/resolve/main/ggml-silero-v5.1.2.bin"
VAD="$HOME/modelos-whisper/vad-silero-v5.1.2.bin"  # sin prefijo ggml-: modelo_whisper() no lo confunde

tiene_skill() {  # solo las del proyecto: el estudio no depende de lo que haya instalado en ~/.claude
  [ -f "$RAIZ/.claude/skills/$1/SKILL.md" ]
}
faltan_skills() {  # imprime los repos con alguna skill ausente
  for e in "${SKILLS[@]}"; do
    for s in ${e##*|}; do tiene_skill "$s" || { echo "${e%%|*}"; break; }; done
  done
}
modelo_whisper() { [ -n "${WHISPER_MODEL:-}" ] && [ -f "$WHISPER_MODEL" ] && echo "$WHISPER_MODEL" && return; ls "$HOME"/modelos-whisper/ggml-*.bin 2>/dev/null | head -1; }
libres_gb() { df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}'; }  # sin python3: en una Mac nueva es un stub que abre un diálogo
key() { grep -qE "^$1=.+" "$RAIZ/.env" 2>/dev/null || [ -n "$(printenv "$1")" ]; }
valor() { printenv "$1" || sed -n "s/^$1=//p" "$RAIZ/.env" 2>/dev/null | head -1; }
voz_venv() { local v; v="$(valor VOZ_LOCAL)"; echo "${v:-$HOME/.local/share/estudio-video-ia/voz}"; }
tiene_voz() { "$(voz_venv)/bin/python" -c 'import kokoro_onnx, soundfile' 2>/dev/null; }

estado() {
  local falta=0
  echo "ESTUDIO DE VIDEO IA · estado ($(date +%d-%m-%Y))"
  echo "Herramientas:"
  for c in ffmpeg ffprobe yt-dlp whisper-cli auto-editor node npx python3 git; do
    command -v "$c" >/dev/null && printf '  ✓ %s\n' "$c" || { printf '  ✗ %s\n' "$c"; falta=1; }
  done
  if command -v node >/dev/null && [ "$(node -v | sed 's/v//;s/\..*//')" -lt 22 ]; then
    echo "  ✗ node 22+ (hay $(node -v); HyperFrames lo pide)"; falta=1
  fi
  [ -n "$(modelo_whisper)" ] && echo "  ✓ modelo whisper: $(basename "$(modelo_whisper)")" || { echo "  ✗ modelo de whisper"; falta=1; }
  [ -f "$VAD" ] && echo "  ✓ VAD de whisper (silencios sin texto inventado)" || { echo "  ✗ VAD de whisper"; falta=1; }
  tiene_voz && echo "  ✓ voz local gratis (Kokoro: kit.sh voz)" || { echo "  ✗ voz local (Kokoro)"; falta=1; }
  local repos; repos="$(faltan_skills)"
  [ -z "$repos" ] && echo "  ✓ skills en el proyecto, .claude/skills (HyperFrames, Remotion, guion, marketing, sonido, find-skills)" \
    || { echo "  ✗ skills sin instalar de: $(echo $repos)"; falta=1; }
  echo "Keys en .env (opcionales; nunca en el chat):"
  key ELEVENLABS_API_KEY && echo "  ✓ ElevenLabs (voz, efectos, música)" || echo "  · ElevenLabs sin configurar: tu voz o la voz guía local, sonidos libres"
  key OPENAI_API_KEY && echo "  ✓ OpenAI (imágenes puntuales)" || echo "  · OpenAI sin configurar: sin imágenes generadas"
  key PEXELS_API_KEY && echo "  ✓ Pexels (B-roll de stock)" || echo "  · Pexels sin configurar: B-roll propio o de otra fuente"
  ls "$HOME"/.cache/estudio-video-ia/STOP-* >/dev/null 2>&1 && echo "  ! STOP activo: $(cd "$HOME/.cache/estudio-video-ia" && ls STOP-* | tr '\n' ' ')— no reintentar, avisar"
  local gb; gb="$(libres_gb)"
  [ "$gb" -lt 20 ] && echo "  ! disco: quedan $gb GB (<20): avisar antes de instalar o renderizar"
  case "$RAIZ" in
    *"Mobile Documents"*|*Dropbox*|*OneDrive*|*"Google Drive"*|"$HOME/Desktop"*|"$HOME/Documents"*)
      echo "  ! el repo está en una carpeta que puede sincronizar la nube: mejor en ~/Developer (los archivos en la nube cuelgan ffmpeg y Chrome)";;
  esac
  echo "Tu trabajo:"
  local nref; nref=$(ls "$RAIZ"/referencias/*/ANALISIS.md 2>/dev/null | wc -l | tr -d ' ')
  local nproy; nproy=$(ls -d "$RAIZ"/proyectos/*/ 2>/dev/null | wc -l | tr -d ' ')
  [ -f "$RAIZ/perfil/PERFIL.md" ] && echo "  ✓ perfil" || echo "  · sin perfil"
  echo "  · referencias analizadas: $nref"
  [ -f "$RAIZ/perfil/ESTILO.md" ] && echo "  ✓ biblia de estilo" || echo "  · sin biblia de estilo"
  echo "  · videos en proyectos/: $nproy"
  printf 'SIGUIENTE PASO: '
  if [ $falta = 1 ]; then echo "/instalar (falta instalar lo marcado con ✗)"
  elif [ ! -f "$RAIZ/perfil/ESTILO.md" ]; then echo "/referencias — «Pásame tus referencias»: pedir sus videos de referencia"
  elif [ ! -f "$RAIZ/perfil/PERFIL.md" ]; then echo "/empezar — el Director entrevista: objetivo, estilo, perfil"
  else echo "/nuevo-video — preguntar qué video hacemos hoy"
  fi
}

instalar() {
  local gb; gb="$(libres_gb)"
  if [ "$gb" -lt 20 ] && [ "${1:-}" != "--si" ]; then
    echo "Quedan $gb GB libres (<20). El modelo de whisper pesa ~0,6 GB y cada render temporal ~0,7 GB."
    echo "Pide OK al usuario y corre: bash scripts/kit.sh instalar --si"; exit 2
  fi
  if [ "$(uname)" = Darwin ]; then
    xcode-select -p >/dev/null 2>&1 || { echo "Faltan las herramientas de desarrollo de Apple: corre en Terminal  xcode-select --install  , acepta y espera; luego reabre Claude Code."; exit 1; }
    command -v brew >/dev/null || { echo 'Falta Homebrew. En la app Terminal (pide tu contraseña de la Mac):'
      echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
      echo "  echo 'eval \"\$(/opt/homebrew/bin/brew shellenv)\"' >> ~/.zprofile"
      echo 'Luego cierra y reabre Claude Code y vuelve a pedir /instalar.'; exit 1; }
    for p in ffmpeg yt-dlp whisper-cpp auto-editor node python git uv; do
      brew list --formula "$p" >/dev/null 2>&1 || brew install "$p"
    done
    brew upgrade yt-dlp >/dev/null 2>&1 || true   # un yt-dlp viejo da 403 que parecen bloqueos
  else
    local faltan=0
    for c in ffmpeg yt-dlp whisper-cli auto-editor node python3 git; do
      command -v "$c" >/dev/null || { echo "Falta $c"; faltan=1; }
    done
    [ $faltan = 1 ] && { echo "Linux: ffmpeg python3 git con apt/dnf; node 22 con nvm (nvm install 22); yt-dlp con pipx;"
      echo "whisper-cli compilando whisper.cpp (github.com/ggml-org/whisper.cpp) y copiando build/bin/whisper-cli a ~/.local/bin;"
      echo "auto-editor: binario de github.com/WyattBlue/auto-editor/releases a ~/.local/bin."; exit 1; }
    command -v uv >/dev/null || echo "Falta uv (para la voz local): curl -LsSf https://astral.sh/uv/install.sh | sh"
  fi
  if [ -z "$(modelo_whisper)" ]; then
    mkdir -p "$HOME/modelos-whisper"
    echo "Bajando modelo de whisper (~0,6 GB, una sola vez para todos los proyectos)…"
    local m="$HOME/modelos-whisper/ggml-large-v3-turbo-q5_0.bin"
    curl -L --fail -C - -o "$m.part" "$MODELO_URL" && mv "$m.part" "$m"  # a medias queda .part y no cuenta como listo
  fi
  [ -f "$VAD" ] || { mkdir -p "$HOME/modelos-whisper"; curl -sL --fail -o "$VAD.part" "$VAD_URL" && mv "$VAD.part" "$VAD"; }
  for e in "${SKILLS[@]}"; do
    local repo="${e%%|*}" resto="${e#*|}"; local sel="${resto%%|*}" mira="${resto##*|}" ok=1
    for s in $mira; do tiene_skill "$s" || ok=0; done
    [ $ok = 1 ] && continue
    echo "Instalando skills de $repo…"
    # sin -g: se copian a .claude/skills/ de este repo (fuera de git) y quedan anotadas en skills-lock.json
    if [ "$sel" = "*" ]; then (cd "$RAIZ" && npx -y skills add "$repo" -y -a claude-code --skill '*')
    else (cd "$RAIZ" && npx -y skills add "$repo" -y -a claude-code --skill $sel)
    fi
  done
  if ! tiene_voz && command -v uv >/dev/null; then  # ~0,1 GB; el modelo (~0,3 GB) baja con la primera voz
    echo "Preparando la voz local (Kokoro)…"
    uv venv -q --allow-existing --python 3.12 "$(voz_venv)" && uv pip install -q --python "$(voz_venv)/bin/python" kokoro-onnx soundfile
  fi
  npx -y hyperframes@latest browser ensure >/dev/null 2>&1 || echo "Aviso: HyperFrames no encontró Chrome; corre: npx hyperframes doctor"
  [ -f "$RAIZ/.env" ] || { cp "$RAIZ/.env.example" "$RAIZ/.env"; chmod 600 "$RAIZ/.env"; }
  mkdir -p "$RAIZ/perfil" "$RAIZ/referencias" "$RAIZ/proyectos"
  echo; estado
}

voz() {  # ponytail: una voz por llamada; para varias tomas, varias llamadas
  [ $# -ge 2 ] || { sed -n '5p' "$0"; exit 1; }
  tiene_voz || { echo "Falta la voz local: bash scripts/kit.sh instalar"; exit 1; }
  local v="${3:-ef_dora}"
  HYPERFRAMES_PYTHON="$(voz_venv)/bin/python" npx -y hyperframes@latest tts "$1" --voice "$v" --lang "$( [ "${v:0:1}" = e ] && echo es || echo en-us )" -o "$2" \
    && printf '%s\n' "voz: $v (Kokoro local) · texto: $1" > "${2%.*}.txt"
}

limpiar() {
  local p="${1:-}"
  [ -n "$p" ] && [ -d "$RAIZ/$p" -o -d "$p" ] || { sed -n '6p' "$0"; exit 1; }
  [ -d "$p" ] || p="$RAIZ/$p"
  local antes; antes="$(du -sh "$p" | cut -f1)"
  find "$p" -type d \( -name node_modules -o -name .cache -o -name .remotion -o -name .venv \) -prune -exec rm -rf {} +
  # no `hyperframes clean`: limpia también otros proyectos que HyperFrames recuerda
  find "$p" -type d \( -path '*/.hyperframes/artifacts' -o -name .thumbnails \) -prune -exec rm -rf {} +
  if pgrep -f 'remotion (render|still)|hyperframes(@[0-9.a-z]+)? render' >/dev/null; then
    echo "hay un render en marcha: los temporales de Remotion quedan para después"
  else
    find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'remotion-webpack-bundle-*' -exec rm -rf {} + 2>/dev/null
  fi
  echo "limpio: $p ($antes → $(du -sh "$p" | cut -f1)). Los renders de out/ quedan: borra a mano los avances superados."
}

case "${1:-estado}" in
  estado) estado ;;
  instalar) shift; instalar "$@" ;;
  voz) shift; voz "$@" ;;
  limpiar) shift; limpiar "$@" ;;
  actualizar) git -C "$RAIZ" pull --ff-only && instalar && (cd "$RAIZ" && npx -y skills update -p -y) ;;  # update vuelve a clonar cada repo: tarda
  *) sed -n '2,7p' "$0"; exit 1 ;;
esac
