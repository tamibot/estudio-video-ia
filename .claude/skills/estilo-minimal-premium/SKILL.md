---
name: estilo-minimal-premium
description: Estilo de edición «minimal premium» para talking heads educativos (el de los reels de Arthur Brooks) — 10 tipos de escena (subtítulos cinemáticos, B-roll con texto, pinturas, línea y texto, línea e ilustraciones, escena de texto con comillas, ilustración central, ilustración lateral, objeto y texto, gráficos), tokens de color y tipografía medidos, texturas, tiempos, reglas de planificación y diseño sonoro. Usar cuando la persona pida ese estilo, «minimal», «premium», «como Arthur Brooks», un talking head educativo o filosófico, o cuando su biblia de estilo apunte a él.
---

# Estilo minimal premium

Talking head educativo que alterna la cara del orador con escenas artísticas sobre papel: texto
cinemático de dos fuentes, pinturas, líneas azules que guían la mirada, ilustraciones con textura y
gráficos que brillan. Se siente caro, artístico y adictivo. Fuente del análisis: el tutorial de
Joseph (Ultimate Editors, oct-2026) sobre el estilo de Arthur Brooks, más la medición de su reel
final con `scripts/referencia.py`.

Se copia **el estilo**, nunca el contenido: ni sus textos, ni su audio, ni sus imágenes.

## Números del reel de referencia (57,5 s)

| Dato | Valor |
|---|---|
| Planos | 28 · plano medio 2,05 s · mediana 1,75 s · de 0,8 a 4,2 s |
| Entre escenas | **corte seco siempre**; el movimiento va dentro de cada escena |
| Cortes sobre un golpe de sonido | 56 % |
| Habla | 4,1 palabras/s, sin silencios (cortados con 30 ms de margen) |
| Imagen | luz 103/255 · contraste 53 · saturación 0,24 · fría |

## Tokens

| Token | Valor | Uso |
|---|---|---|
| `--papel` | `#EEEBEF` (va de `#E4E1E7` a `#F4F1F4`) | fondo claro, siempre con grano |
| `--tinta` | `#08080A` | fondo oscuro con grano; texto sobre papel |
| `--azul` | `#1B42D3` | línea guía, figuras, palabra serif destacada, fondo de escena de texto |
| `--azul-noche` | `#0E1A4C` | fondo oscuro azulado (escena de texto, cierre) |
| `--blanco` | `#F5F4F2` | texto sobre oscuro y sobre A-roll |
| texto secundario | el color del texto al 75-85 % | palabras chicas alrededor de la clave |

**Tipografía** (Google Fonts, se descargan al proyecto):
- **Inter** 400 / 700 / 800 — texto principal; las palabras clave en 800 con tracking −0,03 em.
- **Playfair Display Italic** 400 / 700 — la palabra especial (emoción, concepto, nombre propio),
  a menudo en `--azul` sobre papel o en blanco sobre oscuro.

## Texto cinemático (la base de todo)

1. Una línea de guion = **5 palabras o menos** en pantalla.
2. Elige 1-2 palabras importantes: van **grandes y al centro**, en Inter 800 o Playfair Bold Italic
   (alternar entre escenas, no dentro de la misma palabra). Tamaño clave ≈ 120-170 px en 1080x1920.
3. El resto de la línea va **chico** (≈ 28-34 % del tamaño clave, Inter 400-500) en los huecos de
   arriba o abajo de la clave, alineado a su borde o centrado; nunca compitiendo.
4. Sin patrón fijo: se reacomoda según la forma de la frase, pero siempre clave al centro.
5. En A-roll: en el tercio medio-bajo del cuadro, sobre el pecho; sombra suave para leerse.
6. Entrada: aparece palabra por palabra al ritmo de la voz (la clave con un leve empuje de escala
   0,96 → 1 en 6-8 cuadros); nada rebota ni vibra.

## Las 10 escenas

| # | Escena | Cómo se ve | Movimiento | Cuándo |
|---|---|---|---|---|
| 1 | **A-roll + subtítulos** | la cara del orador con el texto cinemático | zoom-out lento del encuadre, cortes secos entre frases | apertura, cuando anuncia algo nuevo, cuando conecta |
| 2 | **B-roll + texto** | video de archivo que muestra literalmente lo que dice; grano de papel suave, bordes oscurecidos y algo desenfocados | deriva lenta de cámara | cuando describe una acción o escena |
| 3 | **Pintura** | pintura clásica que cuenta la idea, con textura de pintura y papel rugoso; texto cinemático alrededor del sujeto | entrada rápida de cámara deslizándose (slide-in 10-14 cuadros) y deriva | historias personales, emociones, ideas filosóficas |
| 4 | **Línea + texto** | fondo negro o papel con grano; una línea `--azul` lleva al texto, el texto la interrumpe y la línea sigue hacia otra frase | la línea se dibuja y la cámara la sigue | enumerar ideas conectadas («llamado, agilidad, coraje») |
| 5 | **Línea + ilustraciones** | misma línea que lleva a ilustraciones: horizontal con un punto blanco que marca el objeto, o en zigzag con objetos a ambos lados | cámara paneando a lo largo de la línea | fases, progresión, «primero… después…» |
| 6 | **Texto con comillas** | fondo papel o `--azul` con textura muy rugosa; dos comillas grandes y el texto cinemático al centro | el texto se escribe palabra por palabra | frases memorables, cierre del video |
| 7 | **Ilustración central** | figura en `--azul` con textura pintada y ruidosa sobre papel; ocupa la mitad inferior y se funde hacia arriba con bordes abstractos; texto cinemático arriba. Variantes: cerebro visto desde arriba, patrón circular de líneas finas, perfil con textura de tela | revelado rugoso desde abajo + deriva | el concepto central, describir a una persona o una idea |
| 8 | **Ilustración lateral + texto** | la figura o medio círculo con textura de tela a un lado, el texto al otro (a veces girando alrededor) | rotación lenta o revelado lateral | mostrar dos cosas a la vez, opciones |
| 9 | **Objeto + texto** | un solo elemento (foto, objeto) sobre papel con texto alrededor | revelado rugoso | anécdotas con un objeto o foto concreta |
| 10 | **Gráfico** | fondo oscuro plano con textura, cuadrícula de líneas blancas finas que brillan, una bola `--azul` que dibuja la curva | la cámara sigue a la bola | números, crecimiento, comparaciones (sube un escalón por cada «arriba») |

## Texturas y acabado

- **Grano de papel** en todo fondo plano (claro u oscuro). Debe ser estable cuadro a cuadro: ruido con
  semilla fija (SVG `feTurbulence` con `seed`) o una imagen de textura, nunca `Math.random()`.
- **La textura se mueve con lo que cubre**: si la cámara se desliza, la pintura y su textura se
  deslizan juntas (fue una corrección real: «la textura pesaba y no se movía con la animación»).
- **Viñeta** en B-roll y pinturas (bordes −25 a −40 % de luz) y desenfoque leve de bordes.
- **Ilustraciones** a partir de fotos: recortar el fondo (`npx hyperframes remove-background`),
  pasar a duotono `--azul` sobre papel, sumar ruido/pincel y fundir el borde inferior.
- Pinturas: más contraste suave y textura de lienzo; nunca filtros que las vuelvan plásticas.

## Planificar como el editor (antes de construir)

El plan lo decide la persona con el documento de planificación (`/nuevo-video`), con estas reglas:

1. **Abrir en A-roll con subtítulos**: el espectador conecta con la cara antes de que pase nada.
2. **Cuando anuncia algo nuevo, se ve su cara. Cuando lo describe, se muestra.**
3. El primer visual fuerte va pronto (≤ 5 s) y es el gancho: un gráfico o una pintura.
4. Una escena por idea; no repetir el mismo tipo dos veces seguidas; equilibrar cara y escenas
   (en el reel de referencia, ~1/3 de los planos son A-roll).
5. Si una idea ocupa media frase, partir: A-roll la primera mitad y escena la segunda.
6. Cerrar con escena de texto con comillas o una ilustración que resuma.
7. Escenas que necesitan tiempo para leerse (espiral, gráfico) se quedan ≥ 2,5 s.

## Construir

- Motor: Remotion (como el tutorial) o HyperFrames; cada escena es un componente/subcomposición.
- Fuentes descargadas al proyecto desde Google Fonts antes de medir textos.
- Assets: pinturas de dominio público (Wikimedia Commons), B-roll de stock (Pexels), fotos del orador
  con licencia. Lista de assets primero, después se buscan (`python3 scripts/assets.py`).
- El primer render queda al 60-70 %: se esperan 5-6 correcciones puntuales.

## Correcciones típicas (revisar antes de mostrar)

- Diseño de texto pobre en la primera escena o una palabra clave que debía ir junta.
- Corte brusco entre dos animaciones (cortar en un golpe o en el fin de palabra).
- Textura demasiado pesada o quieta mientras la escena se mueve.
- Un corte mal puesto a mitad de palabra.
- Una escena compleja que se va antes de poder leerla.
- Faltan las comillas en la escena de texto final.

## Sonido (al final, con la imagen aprobada)

- Música: cinematográfica suave (piano, cuerdas, pulso leve), 12-18 dB por debajo de la voz.
- **Click** sutil cuando aparece cada bloque de texto.
- **Highlighter / trazo** cuando se dibuja una línea o un gráfico.
- **Whoosh** en entradas de cámara y slide-ins.
- Golpe suave en las palabras clave y en los cortes fuertes (más de la mitad de los cortes caen en uno).
- Mezcla final −14 LUFS, pico ≤ −1 dB.
