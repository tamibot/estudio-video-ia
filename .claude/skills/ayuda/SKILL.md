---
name: ayuda
description: Explica a la persona cómo usar el estudio según dónde va (qué paso sigue, qué puede decir, dónde están sus videos, cuánto cuesta, qué hacer si algo falla) a partir de COMO-USARME.md y del estado. Usar cuando dice «ayuda», «¿cómo te uso?», «¿qué puedo hacer?», «¿qué sigue?», «me perdí», «¿dónde está mi video?», «¿cuánto cuesta?».
---

# Ayuda

1. Corre `bash scripts/kit.sh estado` y lee `COMO-USARME.md`.
2. Responde en 6-8 líneas, sin manual entero:
   - Dónde va (instalación, referencias, perfil, cuántos videos) y **el paso que sigue**.
   - 3 o 4 frases de ejemplo que puede decir ahora mismo (de la tabla «Frases que entiendo»).
   - Si preguntó algo puntual (costos, dónde está su video, un error), contesta eso con la sección
     que toca; si es su video, ábrele la carpeta: `open -R proyectos/<v>/out/<archivo>.mp4`.
3. Cierra con: «La guía completa está en `COMO-USARME.md`; te la abro si quieres» (`open COMO-USARME.md`).
