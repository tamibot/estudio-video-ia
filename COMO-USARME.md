# Cómo usarme

Soy un estudio de edición de video que vive dentro de Claude Code. Me hablas como a un editor:
me pasas videos que te gustan, me cuentas qué quieres lograr y yo escribo el guion, armo el audio,
edito el video y te muestro avances hasta que quede como lo quieres.

No necesitas saber de edición ni de programación. Lo único técnico es instalarme la primera vez,
y eso también lo hago yo.

---

## 1. Lo que necesitas

- Una **Mac** (o Linux). En Windows todavía no funciono.
- **Claude Code**: viene en la app de Claude (claude.com/download) con un plan Pro o Max, o en la
  terminal (`npm install -g @anthropic-ai/claude-code`).
- **~20 GB libres** en el disco. Las herramientas ocupan ~3 GB y cada video, algo más mientras se arma.
- **20 minutos** la primera vez, para instalar.
- Opcional: keys de **ElevenLabs** (voz IA, efectos y música) y de **OpenAI** (imágenes puntuales).
  Sin ellas también funciono: con tu voz o una voz guía gratis, sonidos libres y sin imágenes generadas.

## 2. Instalarme

**Opción fácil, desde la app de Claude.** Abre Claude Code en cualquier carpeta y pega:

> Clona https://github.com/tamibot/estudio-video-ia en ~/Developer/estudio-video-ia

Luego abre una **sesión nueva** con la carpeta `~/Developer/estudio-video-ia` y escribe «hola».

**Opción terminal:**

```bash
git clone https://github.com/tamibot/estudio-video-ia.git ~/Developer/estudio-video-ia
```

```bash
cd ~/Developer/estudio-video-ia && claude
```

Lo que vas a ver la primera vez:

1. Claude Code pregunta si confías en la carpeta: **sí** (así puedo revisar qué falta al abrir).
2. Si tu Mac nunca instaló herramientas de desarrollo, aparece una ventana de Apple: **Instalar** y esperar.
3. Te digo qué falta y lo instalo con `/instalar`. Si hace falta Homebrew, te paso dos comandos para
   pegar en la app **Terminal**; te pide la contraseña de tu Mac, que nunca me tienes que dar a mí.
4. Algunas acciones me piden permiso (instalar, gastar, publicar). Lee qué es y aprueba.

Guárdalo en una carpeta local como `~/Developer`, **no** en iCloud, Dropbox ni Drive: los archivos
que viven en la nube cuelgan los programas de video sin avisar.

## 3. Cómo trabajamos: cuatro pasos

### Paso 1 · Tus referencias (`/referencias`)

Te voy a pedir **de 3 a 5 videos que te gusten**. Pueden ser links de Instagram, TikTok o YouTube,
o archivos (arrástralos a la ventana del chat). Por cada uno dime qué te gusta:

> Este reel por cómo corta con la música. Este otro por los subtítulos amarillos.
> Y este por el gancho del inicio.

Los desarmo cuadro a cuadro: cuántos cortes tiene, si caen en el beat, cómo son las transiciones,
qué dice, cómo se ve. Con eso armo tu **biblia de estilo** y te la muestro para que la confirmes.

**¿Quieres editar exactamente como un creador?** Dime «entrena el estilo de <creador>» y pásame
hasta 20 de sus mejores videos. Armo un tablero en Figma con cada tipo de escena y qué la compone
(lo puedes corregir), una biblioteca con cada animación que usa y una skill de su estilo.

**¿Te gusta el estilo minimal premium?** (cara del orador, papel, texto de dos fuentes, pinturas,
líneas azules). Ya viene entrenado: dime «usa el estilo minimal premium».

### Paso 2 · Te conozco (`/empezar`)

Te hago preguntas cortas, casi todas con opciones: para qué son tus videos (anuncios, contenido,
marca personal), dónde los publicas, quién eres, a quién le hablas, qué quieres que haga la gente
al final, tu tono, tus colores y tu logo. Lo guardo y no te lo vuelvo a preguntar.

### Paso 3 · Un video nuevo (`/nuevo-video`)

Dime qué video quieres:

> Hagamos un reel de 30 segundos sobre los 3 errores más comunes al vender por WhatsApp.

A partir de ahí avanzamos por etapas y en cada una te muestro algo antes de seguir:

| Etapa | Lo que recibes | Lo que haces tú |
|---|---|---|
| Brief | resumen de lo que vamos a hacer | corriges o apruebas |
| Guion | 5 ganchos y el guion por bloques | eliges gancho y apruebas |
| Plan | escena por escena: qué se ve, qué texto, qué sonido, y qué cuesta | apruebas (y el gasto, si hay) |
| Audio | voz, música y efectos con los cortes sobre el ritmo | escuchas y apruebas |
| Avance | un MP4 borrador que se abre en tu Mac | me dices qué cambiar |
| Final | el video listo para subir | lo publicas |

**Si traes tu propia grabación** (hablas a cámara, una clase, un podcast) el camino cambia:

| Etapa | Lo que recibes | Lo que haces tú |
|---|---|---|
| Limpieza | tu clip sin silencios y la transcripción palabra por palabra | escuchas que no quede atropellado |
| **Plan** | un documento: a la derecha lo que dices en cada momento con su pedazo de video; a la izquierda 2-3 diseños recomendados | eliges uno por momento o escribes el tuyo, y aprietas **Copiar plan** y lo pegas en el chat |
| Avance | el video armado (queda al 60-70 %) | me dices qué cambiar |
| Sonido | música y efectos, recién con la imagen aprobada | escuchas y apruebas |
| Final | el video listo | lo publicas |

El plan es tuyo y es lo que más pesa en el resultado: la regla de oro es que **cuando anuncias algo
se ve tu cara y cuando lo describes se muestra**.

### Paso 4 · Rondas de cambios

Lo normal son **4 o 5 rondas**. La forma más rápida de pedir cambios es decir **el segundo y qué
cambiar**:

> 0:04 el texto más grande · 0:10 corta antes · la música más baja · el final más largo

También sirve una captura o «esto no me gusta porque…». Lo que no te gusta lo anoto y no lo repito
en el próximo video.

## 4. Frases que entiendo

| Quieres… | Dime… |
|---|---|
| saber qué sigue | «¿qué sigue?» o `/ayuda` |
| analizar un video | «mira este video: <link>» |
| copiar a un creador | «entrena el estilo de <creador>» |
| editar tu grabación | «edita esta grabación en estilo minimal premium» (arrastra el archivo) |
| sumar referencias | «agrega esta referencia a mi estilo» |
| un video nuevo | «hagamos un anuncio de 15 s para…» |
| usar tu material | «edita esta grabación» (arrastra el archivo) |
| otro formato | «hazlo también en horizontal para YouTube» |
| tu voz en vez de IA | «uso mi voz» (te digo cómo grabarla) |
| saber el costo | «¿cuánto cuesta esto?» |
| cambiar tu perfil | «cambié de objetivo» o «otra marca» |
| liberar espacio | «limpia el disco» |

## 5. Dónde queda cada cosa

```
perfil/        quién eres, tu biblia de estilo y lo que aprendí de tus gustos
referencias/   el análisis de cada video que me pasaste
proyectos/<fecha-nombre>/
  guion.md, plan.md, revision.md
  out/<nombre>-final.mp4   ← tu video terminado
```

Al terminar te abro la carpeta donde quedó el video. Todo esto vive solo en tu computadora: no
se sube a ningún lado.

## 6. Costos

- **Gratis:** analizar referencias, transcribir, editar en HyperFrames, la voz guía (Kokoro, local),
  los efectos de sonido libres y los renders en tu Mac.
- **Cuesta (con tu key):** voz, música y efectos de ElevenLabs; imágenes de OpenAI. Antes de cada
  lote te digo qué voy a generar, cuántas llamadas y el costo aproximado, y espero tu OK.
- **Remotion** (el segundo motor) es gratis para personas y equipos de hasta 3; empresas más
  grandes necesitan su licencia.
- Las funciones en la nube de HyperFrames (publicar, renders en la nube, avatares) son de pago:
  no las uso sin preguntarte.

**Tus keys:** te abro el archivo `.env` y las pegas ahí. **Nunca en el chat**; si pasa, crea una key
nueva en la página del servicio y borra la anterior.

## 7. Actualizarme

```bash
bash ~/Developer/estudio-video-ia/scripts/kit.sh actualizar
```

O dime «actualízate». Eso trae la última versión del estudio y de sus skills (viven dentro de la
carpeta del estudio, no se mezclan con otras). Tu perfil, tus referencias y tus proyectos no se tocan.

## 8. Si algo falla

| Pasa esto | Hacemos esto |
|---|---|
| Instagram pide iniciar sesión | bajas el reel y lo arrastras al chat, o me autorizas a leer tu sesión de Chrome (macOS te pide «Permitir») |
| «STOP» o «429» al bajar videos | la plataforma nos frenó: paramos y esperamos; mientras, pasa los archivos a mano |
| Instalé Homebrew y sigue diciendo que falta | cierra y vuelve a abrir Claude Code |
| La key no funciona | revisa que esté completa en `.env`, sin espacios ni comillas |
| Poco espacio en el disco | «limpia el disco»: borro dependencias y temporales de los videos entregados |
| El video no se parece a la referencia | dime el segundo y qué es distinto; también puedo comparar los dos cuadro a cuadro |
| Me perdí | `/ayuda` |

## 9. Para que salgan mejores

- Referencias **del mismo tipo** de video que quieres hacer (si quieres anuncios, pásame anuncios).
- Si grabas: celular a la altura de los ojos, luz de frente, sin ruido de fondo, a un palmo del micrófono.
- **Un mensaje y un llamado a la acción** por video.
- Mira cada avance en el celular: ahí lo va a ver tu público.
