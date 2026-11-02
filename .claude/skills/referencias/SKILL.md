---
name: referencias
description: Paso 1 · Referencias y entrenamiento de estilo. Pide a la persona sus videos de referencia (links de Instagram, TikTok, YouTube o archivos), los desarma con scripts/referencia.py (planos, cortes, transiciones, ritmo contra la música, transcripción), lanza analistas en paralelo y consolida la biblia de estilo en perfil/ESTILO.md; en modo «entrenar» (hasta 20 videos de un creador) arma además el tablero en Figma, la biblioteca de animaciones y una skill del estilo. Usar también cuando dice «entrena este estilo», «quiero editar como <creador>». Usar cuando dice «dame tus referencias», «mira este video», «quiero que se vea como esto», «analiza este reel», o pega un link de video.
---

# Paso 1 · Referencias → biblia de estilo

Es lo primero que se hace en el estudio: con sus videos a la vista, el objetivo, el estilo y el
ritmo se entienden solos, y la entrevista de `/empezar` queda corta.

## 1. Pedir

«Para empezar, pásame tus referencias: de 3 a 5 videos que te gusten (links de Instagram, TikTok
o YouTube, o archivos). Por cada uno dime qué te gusta: el ritmo, las transiciones, los textos,
el sonido, el gancho…»
Si solo pasa links sin decir qué le gusta, pregunta una vez; si no sabe, el análisis lo propone.

Dos profundidades (método completo en `guias/entrenar-un-estilo.md`):
- **Rápida** (3-5 videos de lo que le gusta): termina en `perfil/ESTILO.md`.
- **Entrenar** (quiere editar *como un creador puntual*): pídele **hasta 20 videos** de ese creador,
  los más cuidados (mínimo 5). Termina además en el tablero de Figma, la biblioteca de animaciones y
  la skill `estilo-<creador>`.
- **Atajo:** si lo que trae es un talking head educativo minimal (fondos de papel, texto de dos
  fuentes, pinturas, líneas azules), el estilo ya está entrenado: skill `estilo-minimal-premium` y
  `plantillas/minimal-premium/`. Muéstrale el resumen de la skill y pregúntale si es eso.

## 2. Desarmar (por la puerta, máximo 3 a la vez)

Por cada video, una carpeta `referencias/<plataforma>-<id-o-nombre>`:

```bash
python3 scripts/referencia.py '<url o archivo>' referencias/<slug>
python3 scripts/referencia.py '<url>' referencias/<slug> --inicio 1:20 --fin 2:05   # solo un tramo de un video largo
```

- Uno por vez o hasta 3 en segundo plano. La puerta espacia las descargas por plataforma.
- **429, 403 o STOP:** parar todas las descargas, no reintentar, avisar. Sugerir que pase los
  archivos descargados a mano mientras tanto.
- **Instagram pide login** (sin sesión, a veces lo dice como «rate-limit… anonymously»; no es un
  bloqueo): ofrecer dos caminos: que baje el reel y **arrastre el archivo a esta ventana** (llega
  como ruta), o (con su OK explícito) `--cookies-navegador chrome`, que lee la sesión de su
  navegador; macOS muestra un aviso del Llavero («Chrome Safe Storage»): tiene que darle a «Permitir».

## 3. Analizar (subagentes en paralelo, hasta 3)

Lanza un agente `analista-referencias` por video con: la carpeta, lo que a la persona le gusta de
ese video, la ruta de `perfil/PERFIL.md` si ya existe y, en modo entrenar, el número de video
(`V01`…`V20`) y la orden de llenar la biblioteca. Cada uno escribe `referencias/<slug>/ANALISIS.md`
(y en modo entrenar, sus carpetas en `perfil/biblioteca/`).

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
## Imagen       encuadres, movimiento de cámara, color/look (renglón «Imagen» de ritmo.md: luz, contraste, saturación, temperatura), grano, fondos
## Sonido       música (género, bpm, energía, dónde sube), efectos (en qué momentos), voz (ritmo, palabras/s)
## Sí / No      lo que vamos a copiar del estilo y lo que no (contenido ajeno, logos, audio)
```

Muéstrale el resumen en 8-10 líneas con la pregunta: «¿Esto es lo que te gusta? ¿Algo que
cambiarías?». Ajusta y guarda. Luego, si no hay `perfil/PERFIL.md`: «Ahora cuéntame de ti y de
tus videos» → `/empezar`. Si ya hay perfil: «Listo. ¿Qué video hacemos?» → `/nuevo-video`.
Más referencias después: se agregan igual y se actualiza `ESTILO.md`.

## 5. Solo en modo entrenar: tablero en Figma y skill del estilo

**Tablero.** Si Figma está conectado (herramientas `figma`; carga la skill `figma-use` antes de
cualquier `use_figma`): crea un archivo «Tablero de estilo · <creador>» en el equipo de la persona,
sube una captura de cada escena buena (de `laminas/`, `zoom/` y `perfil/biblioteca/*/diseno.jpg`),
agrúpalas por principio (tipo de escena) y anota en cada grupo qué la compone: fuentes, colores,
tamaños, patrón, movimiento, cuándo se usa. Pocas llamadas grandes, no muchas chicas (Figma limita
la cuota); ante un límite, parar y avisar. Muéstrale el enlace: la persona corrige el tablero, que es
la parte más importante del entrenamiento. Sin Figma, sigue con la biblioteca y la skill.
Las capturas son de otro creador: el tablero queda privado, nunca en git.

**Skill.** Escribe `.claude/skills/estilo-<creador>/SKILL.md` siguiendo el modelo de
`estilo-minimal-premium`: principios y cuándo se usa cada uno, tokens medidos, lógica del texto,
texturas, números de ritmo, reglas de planificación, sonido y correcciones típicas. Queda fuera de
git (es suyo). En `ESTILO.md`, una línea que apunte a la skill y a la biblioteca.

## Cerrar

`referencias/<slug>/video.mp4` pesa: bórralo cuando el ANALISIS.md esté aprobado
(`rm referencias/<slug>/video.mp4`, uno por uno según se aprueban), salvo que la persona quiera
conservarlo. Láminas, ritmo y análisis
se quedan.
