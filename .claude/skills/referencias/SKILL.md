---
name: referencias
description: Paso 1 · Referencias. Pide a la persona sus videos de referencia (links de Instagram, TikTok, YouTube o archivos), los desarma con scripts/referencia.py (planos, cortes, transiciones, ritmo contra la música, transcripción), lanza analistas en paralelo y consolida la biblia de estilo en perfil/ESTILO.md. Usar cuando dice «dame tus referencias», «mira este video», «quiero que se vea como esto», «analiza este reel», o pega un link de video.
---

# Paso 1 · Referencias → biblia de estilo

Es lo primero que se hace en el estudio: con sus videos a la vista, el objetivo, el estilo y el
ritmo se entienden solos, y la entrevista de `/empezar` queda corta.

## 1. Pedir

«Para empezar, pásame tus referencias: de 3 a 5 videos que te gusten (links de Instagram, TikTok
o YouTube, o archivos). Por cada uno dime qué te gusta: el ritmo, las transiciones, los textos,
el sonido, el gancho…»
Si solo pasa links sin decir qué le gusta, pregunta una vez; si no sabe, el análisis lo propone.

## 2. Desarmar (por la puerta, máximo 3 a la vez)

Por cada video, una carpeta `referencias/<plataforma>-<id-o-nombre>`:

```bash
python3 scripts/referencia.py '<url o archivo>' referencias/<slug>
python3 scripts/referencia.py '<url>' referencias/<slug> --inicio 1:20 --fin 2:05   # solo un tramo de un video largo
```

- Uno por vez o hasta 3 en segundo plano. La puerta espacia las descargas por plataforma.
- **429, 403 o STOP:** parar todas las descargas, no reintentar, avisar. Sugerir que pase los
  archivos descargados a mano mientras tanto.
- **Instagram pide login:** ofrecer dos caminos: que baje el reel y pase el archivo, o (con su OK
  explícito) `--cookies-navegador chrome`, que lee las cookies de su navegador.

## 3. Analizar (subagentes en paralelo, hasta 3)

Lanza un agente `analista-referencias` por video con: la carpeta, lo que a la persona le gusta de
ese video y la ruta de `perfil/PERFIL.md` si ya existe. Cada uno escribe `referencias/<slug>/ANALISIS.md`.

## 4. Consolidar `perfil/ESTILO.md`

Lee todos los ANALISIS.md y escribe la biblia, con números y no con adjetivos:

```markdown
# Biblia de estilo  (fuentes: referencias/…)
## En una línea
## Ritmo        plano medio X s · cambios/min · cortes en el beat N % · hook: qué pasa en 0-3 s
## Estructura   hook → … → CTA, con segundos
## Transiciones las 3-5 que se repiten: cuándo, cuánto duran, sonido, cómo se hacen (HyperFrames / Remotion)
## Texto        fuente aproximada, peso, tamaño, color, posición, cómo entra, palabras por pantalla
## Subtítulos   estilo, resaltado, posición (zona segura)
## Imagen       encuadres, movimiento de cámara, color/look, grano, fondos
## Sonido       música (género, bpm, energía, dónde sube), efectos (en qué momentos), voz (ritmo, palabras/s)
## Sí / No      lo que vamos a copiar del estilo y lo que no (contenido ajeno, logos, audio)
```

Muéstrale el resumen en 8-10 líneas con la pregunta: «¿Esto es lo que te gusta? ¿Algo que
cambiarías?». Ajusta y guarda. Luego, si no hay `perfil/PERFIL.md`: «Ahora cuéntame de ti y de
tus videos» → `/empezar`. Si ya hay perfil: «Listo. ¿Qué video hacemos?» → `/nuevo-video`.
Más referencias después: se agregan igual y se actualiza `ESTILO.md`.

## Cerrar

`referencias/<slug>/video.mp4` pesa: bórralo cuando el ANALISIS.md esté aprobado
(`rm referencias/*/video.mp4`), salvo que la persona quiera conservarlo. Láminas, ritmo y análisis
se quedan.
