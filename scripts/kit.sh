#!/usr/bin/env bash
# Kit del estudio de video.
#   bash scripts/kit.sh estado          qué está listo y qué falta (Claude lo corre solo al abrir el repo)
#   bash scripts/kit.sh instalar [--si] herramientas, modelo de whisper y skills; se puede repetir sin miedo
set -u
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

# repo de skills | qué instalar ('*' = todas) | cuáles mirar para saber si ya está
SKILLS=(
  "heygen-com/hyperframes|*|hyperframes hyperframes-cli hyperframes-registry media-use"
  "remotion-dev/skills|*|remotion-best-practices remotion-create remotion-captions"
  "vercel-labs/skills|find-skills|find-skills"
  "coreyhaines31/marketingskills|copywriting copy-editing video social ad-creative marketing-psychology content-strategy marketing-ideas|copywriting video social ad-creative marketing-psychology"
  "wondelai/skills|storybrand-messaging made-to-stick|storybrand-messaging made-to-stick"
  "gtmagents/gtm-agents|scriptwriting|scriptwriting"
  "mbfinotti/advertising-skills|ad-hook-analyzer ugc-ad-scripts ad-creative-brief|ad-hook-analyzer ugc-ad-scripts"
  "elevenlabs/skills|text-to-speech sound-effects music|text-to-speech sound-effects"
  "greensock/gsap-skills|gsap-core gsap-plugins|gsap-core"
  "emilkowalski/skills|animation-vocabulary|animation-vocabulary"
  "Leonxlnx/cinetic|cinetic|cinetic"
)
MODELO_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin"

tiene_skill() {
  for d in "$HOME/.claude/skills/$1" "$RAIZ/.claude/skills/$1" "$HOME/.agents/skills/$1"; do
    [ -f "$d/SKILL.md" ] && return 0
  done
  return 1
}
faltan_skills() {  # imprime los repos con alguna skill ausente
  for e in "${SKILLS[@]}"; do
    for s in ${e##*|}; do tiene_skill "$s" || { echo "${e%%|*}"; break; }; done
  done
}
modelo_whisper() { [ -n "${WHISPER_MODEL:-}" ] && [ -f "$WHISPER_MODEL" ] && echo "$WHISPER_MODEL" && return; ls "$HOME"/modelos-whisper/ggml-*.bin 2>/dev/null | head -1; }
libres_gb() { python3 -c "import shutil; print(shutil.disk_usage('$HOME').free // 2**30)"; }
key() { grep -qE "^$1=.+" "$RAIZ/.env" 2>/dev/null || [ -n "$(printenv "$1")" ]; }

estado() {
  local falta=0
  echo "ESTUDIO DE VIDEO IA · estado ($(date +%d-%m-%Y))"
  echo "Herramientas:"
  for c in ffmpeg ffprobe yt-dlp whisper-cli node npx python3 git; do
    command -v "$c" >/dev/null && printf '  ✓ %s\n' "$c" || { printf '  ✗ %s\n' "$c"; falta=1; }
  done
  if command -v node >/dev/null && [ "$(node -v | sed 's/v//;s/\..*//')" -lt 22 ]; then
    echo "  ✗ node 22+ (hay $(node -v); HyperFrames lo pide)"; falta=1
  fi
  [ -n "$(modelo_whisper)" ] && echo "  ✓ modelo whisper: $(basename "$(modelo_whisper)")" || { echo "  ✗ modelo de whisper"; falta=1; }
  local repos; repos="$(faltan_skills)"
  [ -z "$repos" ] && echo "  ✓ skills (HyperFrames, Remotion, guion, marketing, sonido, find-skills)" \
    || { echo "  ✗ skills sin instalar de: $(echo $repos)"; falta=1; }
  echo "Keys en .env (opcionales; nunca en el chat):"
  key ELEVENLABS_API_KEY && echo "  ✓ ElevenLabs (voz, efectos, música)" || echo "  · ElevenLabs sin configurar: voz propia y sonidos libres"
  key OPENAI_API_KEY && echo "  ✓ OpenAI (imágenes puntuales)" || echo "  · OpenAI sin configurar: sin imágenes generadas"
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
    command -v brew >/dev/null || { echo "Falta Homebrew: instálalo desde https://brew.sh y vuelve a correr esto."; exit 1; }
    for p in ffmpeg yt-dlp whisper-cpp node python git; do
      brew list --formula "$p" >/dev/null 2>&1 || brew install "$p"
    done
    brew upgrade yt-dlp >/dev/null 2>&1 || true   # un yt-dlp viejo da 403 que parecen bloqueos
  else
    for c in ffmpeg yt-dlp whisper-cli node python3 git; do
      command -v "$c" >/dev/null || echo "Falta $c: instálalo con tu gestor (apt/dnf); yt-dlp con pipx; whisper-cli compilando whisper.cpp"
    done
  fi
  if [ -z "$(modelo_whisper)" ]; then
    mkdir -p "$HOME/modelos-whisper"
    echo "Bajando modelo de whisper (~0,6 GB, una sola vez para todos los proyectos)…"
    curl -L --fail -C - -o "$HOME/modelos-whisper/ggml-large-v3-turbo-q5_0.bin" "$MODELO_URL"
  fi
  for e in "${SKILLS[@]}"; do
    local repo="${e%%|*}" resto="${e#*|}"; local sel="${resto%%|*}" mira="${resto##*|}" ok=1
    for s in $mira; do tiene_skill "$s" || ok=0; done
    [ $ok = 1 ] && continue
    echo "Instalando skills de $repo…"
    if [ "$sel" = "*" ]; then npx -y skills add "$repo" -g -y -a claude-code --skill '*'
    else npx -y skills add "$repo" -g -y -a claude-code --skill $sel
    fi
  done
  npx -y hyperframes@latest browser ensure >/dev/null 2>&1 || echo "Aviso: HyperFrames no encontró Chrome; corre: npx hyperframes doctor"
  [ -f "$RAIZ/.env" ] || { cp "$RAIZ/.env.example" "$RAIZ/.env"; chmod 600 "$RAIZ/.env"; }
  mkdir -p "$RAIZ/perfil" "$RAIZ/referencias" "$RAIZ/proyectos"
  echo; estado
}

case "${1:-estado}" in
  estado) estado ;;
  instalar) shift; instalar "$@" ;;
  *) sed -n '2,4p' "$0"; exit 1 ;;
esac
