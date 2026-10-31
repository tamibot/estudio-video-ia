# Estilos: cómo describirlos y cómo construirlos

Un estilo se describe con **números y nombres de técnicas**, no con adjetivos. «Dinámico» no le
dice nada al editor; «plano medio 1,2 s, corte en el beat, texto de 3 palabras que golpea desde
abajo con escala 1,15 → 1» sí.

## Vocabulario (lo que mide `referencia.py` y lo que se nombra en ESTILO.md)

| Eje | Qué anotar | Ejemplo |
|---|---|---|
| Ritmo | duración media de plano, cambios por minuto, % de cortes en el beat | 1,3 s · 40/min · 70 % en el beat |
| Hook | qué pasa en el primer segundo y en los primeros 3 | pregunta en texto gigante + golpe de sonido en el cuadro 1 |
| Transición | tipo, duración, sonido | push vertical 8 cuadros + whoosh |
| Texto | familia (sans/serif/mono), peso, tamaño relativo al ancho, color, caja, entrada | sans black, 9 % del ancho, blanco con caja amarilla, sube 40 px en 6 cuadros |
| Subtítulos | palabra por palabra o frase, resaltado, posición | 2-3 palabras, palabra activa en color, en y≈1150 |
| Cámara | encuadre, movimiento real o simulado | plano medio, punch-in de 1,0 → 1,12 en cada frase clave |
| Color | look, contraste, grano | contraste alto, negros levantados, grano fino |
| Sonido | género, bpm, efectos y dónde | lo-fi 90 bpm; pop en cada texto; riser antes del CTA |

## Familias de estilo

**Minimal limpio.** Fondo de un color, una tipografía, mucho aire, movimientos suaves con easing
largo (0,6–0,9 s, `power3.out`). Planos de 2,5–4 s. Música tranquila, pocos efectos.
→ HyperFrames: `soft-blur-in`, `fade-through`, `morph-swap`, `text-match-cut`.

**Texto cinético con la música.** El texto es la imagen. Palabras grandes que entran en el beat,
cambian de escala, color o posición en cada golpe. Planos de 0,5–1,5 s.
→ HyperFrames: `caption-kinetic-slam`, `text-match-cut`, `type-match-cut`, `mk-clone-wall-transition`;
cortes de `audio/cues.json` sobre beats y downbeats.

**Talking head dinámico.** Persona a cámara, cortes de silencios, punch-in (zoom de 1,0 a 1,1–1,2)
en las frases clave, subtítulos palabra por palabra, B-roll o pantallas cada 3–5 s, efectos en
cada aparición.
→ Primero `auto-editor` quita silencios y tropiezos del material (ver `guias/motores.md`); después
Remotion si hay mucho material propio que cortar (`remotion-captions` para los subtítulos) o
HyperFrames (`caption-highlight`, `caption-pill-karaoke`, `mk-callout-highlight`) si es corto.

**Cinemático.** Planos largos (3–6 s), movimiento lento y continuo, barras o 2.39:1, grano, look de
color, música que crece, pocos textos y en serif o sans fina.
→ `light-leak`, `organic-light-leak-overlay`, `cinematic-zoom`; el look de color con el comando
`npx hyperframes media-treatment` (no es un bloque) y `npx hyperframes grade-compare` para elegir
entre varios looks sobre un mismo cuadro.

**Meme / brain rot.** Cortes cada 0,3–0,8 s, stickers, zoom bruscos, texto con contorno, efectos
de meme en cada golpe, voz rápida.
→ `caption-emoji-pop`, `glitch`, `editorial-flash-overlay`, `beat-freeze-cut`; efectos de
`@remotion/sfx` o libres.

**Explicativo con íconos y pantallas.** Interfaces reales grabadas o reconstruidas en HTML,
íconos, diagramas que se arman, cursor que hace clic, zoom a la parte que importa.
→ HyperFrames (el HTML es la interfaz): `parallax-device-dive`, `iris-reveal`, `inline-highlight`.

Los nombres con guiones son bloques del registro de HyperFrames: `npx hyperframes catalog <palabras>`
para buscar, `npx hyperframes add <nombre> --no-clipboard` para traerlo editable.

## Imágenes generadas (OpenAI): solo cuando suman

Sirven para un plano clave que no existe (un producto en un ambiente, un fondo, una textura, un
personaje). No para lo que se arma con texto, formas, interfaz o material propio.

Orden: primero el plano (una imagen clave por toma) aprobado; recién después se anima en el motor.
Cada prompt va en su archivo (`imagenes/<nombre>.prompt.txt`) con estas partes:

```
Sujeto: …            Acción: …              Encuadre: plano medio, cámara a la altura de los ojos, vertical 9:16
Luz: …               Estilo: foto real / ilustración plana / 3D …, paleta …
Composición: aire arriba para el título; sujeto en el tercio inferior
NO debe aparecer: texto, logos, marcas de agua, manos deformes, gente de fondo
```

El texto de la imagen siempre se pone en el motor, nunca dentro de la imagen generada.
