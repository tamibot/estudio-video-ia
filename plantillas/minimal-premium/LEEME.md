# Plantilla «minimal premium» (HyperFrames)

Cinco escenas del estilo `estilo-minimal-premium` (tokens, tipos y tiempos en su `SKILL.md`), en
1080×1920 a 30 fps. Cada escena vive sola en `compositions/` para copiarla sin lo demás.
`index.html` es solo una demo: las 5 seguidas con corte seco, 3 s cada una (15 s).

| Archivo | Escena de la skill | Qué hace |
|---|---|---|
| `texto-cinematico.html` | 1 · A-roll + subtítulos | Capa transparente sobre el video del orador. La palabra clave va grande al centro y el resto, chico en los huecos, palabra por palabra. |
| `texto-comillas.html` | 6 · Texto con comillas | Fondo azul rugoso (o papel), dos comillas grandes, frase escrita palabra por palabra y acercamiento lento. |
| `linea-texto.html` | 4 · Línea + texto | Fondo oscuro con renglones. La línea azul se dibuja, cada frase la corta y la línea sigue. La cámara la acompaña. |
| `grafico.html` | 10 · Gráfico | Cuadrícula blanca que brilla. La bola azul dibuja una escalera que sube y la cámara la sigue. |
| `ilustracion-central.html` | 7 · Ilustración central | Papel con círculos azules de pincel y halo, revelado rugoso desde abajo y texto arriba. |
| `aroll-demo.html` | — | Solo para la demo: un degradado en lugar de la cara. No se copia. |

## Qué se edita

- **Texto y tiempos**: en el HTML de cada escena. Cada línea lleva `data-t` con un segundo por
  palabra, contado desde el inicio de la escena. Con `0`, la palabra ya está en el cuadro 1.
  Si sacas los tiempos de `npx hyperframes transcribe voz.wav --model small --language es`, réstales
  el `data-start` del host.
- **Jerarquía**: `.clave` es la palabra grande (Inter 800). Agrégale `serif` para Playfair Bold
  Italic. `.chica izq` / `.chica der` alinean las palabras chicas al borde de la clave. Si la clave
  no entra en el 80 % del ancho, se achica sola.
- `texto-cinematico`: una `.frase` por grupo, con `data-sale` (el segundo en que se corta).
  `--centro-y` fija la altura.
- `texto-comillas`: la clase `azul` o `papel` en `.escena`.
- `linea-texto`: agrega o quita `.frase`. Arriba del script están `LINEA_Y`, `TRAMOS`, `AIRE`,
  `DERIVA_FINAL` y `DURACION`.
- `grafico`: arriba del script están `PUNTOS` (la escalera, en un mundo de 1080×2700),
  `DIBUJO`, `CAMARA_Y` y `DURACION`.
- `ilustracion-central`: cambia lo que hay en `<g class="figura">` por cualquier trazo con
  `stroke="currentColor"`. Textura, halo y revelado se aplican solos. `REVELADO` fija los tiempos.

## Copiar una escena a un proyecto

1. Copia `compositions/<escena>.html` a `proyectos/<v>/video/compositions/`, y `assets/fuentes/`
   y `assets/texturas/` a `proyectos/<v>/video/assets/`.
2. Móntala en el `index.html` del proyecto, igual que en esta demo:
   `<div id="grafico" data-composition-id="grafico" data-composition-src="compositions/grafico.html" data-start="9" data-duration="3" data-track-kind="graphics" data-width="1080" data-height="1920"></div>`.
   Para `texto-cinematico`, el `<video>` del orador va debajo (z-index menor).
3. Para usar la misma escena dos veces, cópiala con otro nombre y cambia el id en el host, en
   `data-composition-id` del root, en el `querySelector` del script y en `window.__timelines["…"]`.
4. Si el host no dura 3 s, ajusta `DURACION` y los tiempos.

## Límites conocidos

- Texturas: SVG con semilla fija (`assets/texturas/`), estables cuadro a cuadro. Van dentro de la
  cámara, así que se mueven con lo que cubren. El azul y el papel están medidos con una variación
  de luz de ±6 % como máximo (grano fino y viñeta leve): si subes la opacidad de `.rugoso` o
  `.grano`, el fondo se ve nublado. El filtro de pincel de la ilustración se recalcula
  en cada cuadro, así que esa escena es la más lenta de renderizar.
- El runtime oculta con `display:none` las escenas que no están en pantalla. Por eso cada escena
  se muestra un instante para medirse (`medir()`): no lo quites. El bloque «común» es igual en
  las 5 escenas, así que si lo cambias en una, cópialo en todas.
- `linea-texto` es solo horizontal. Si las frases son largas, la cámara corre más rápido.
- `grafico`: la bola va a velocidad constante y no sube un escalón por cada palabra. Eso se
  ajusta a mano con `PUNTOS` y `DIBUJO`.
- No hay sonido (clic, trazo, whoosh): se agrega en el proyecto.
- Las fuentes son Inter y Playfair Display Italic, solo el subconjunto latino (licencia en
  `assets/fuentes/OFL.txt`).
- Al abrir el preview, Studio agrega `data-hf-id` a las etiquetas y crea `.thumbnails/`. Quítalos
  antes de subir cambios a esta plantilla.
- No uses `npx hyperframes clean`: borra las capturas de **todos** los proyectos que HyperFrames
  recuerda, no solo los de esta carpeta. Limpia con `bash scripts/kit.sh limpiar <carpeta>`.
