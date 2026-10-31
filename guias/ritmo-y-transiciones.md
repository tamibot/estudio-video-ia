# Ritmo y transiciones

## El audio manda

Primero se fija el audio (voz + música); después se cortan las imágenes encima. Nunca al revés.

1. Voz con tiempos por palabra (alineación de ElevenLabs o whisper con `-ml 1 -sow -oj`).
2. Música con beats, downbeats, secciones y golpes:
   `npx -y hyperframes audio musica.mp3 --only bpm,beats,downbeats,sections,onsets --json`.
   Si dice «no steady beat», usa los golpes fuertes (`onsets` con fuerza alta) en vez de beats.
3. Cada corte va al final de una idea hablada **y** sobre el beat o golpe más cercano.
   Si no coinciden, manda la voz: nunca cortes a mitad de palabra.

## Números que funcionan

| | Tranquilo | Medio | Frenético |
|---|---|---|---|
| Plano medio | 3–5 s | 1,5–3 s | 0,4–1 s |
| Cambio visual (aunque no haya corte) | cada 4 s | cada 2–3 s | cada 0,5–1 s |
| Transición animada | 0,6–1 s | 0,25–0,5 s | 2–6 cuadros o corte seco |

- **Hook**: algo pasa en el cuadro 1 (no en el 10). Los primeros 3 s llevan el ritmo más alto del video.
- **Corte en el beat**: el corte cae en el beat o 1 cuadro antes (el ojo va un poco adelantado al oído).
- **Whoosh**: empieza 3–6 cuadros antes del corte y su pico cae en el corte. Golpe (hit) en el corte.
- **Downbeat** (el 1 del compás): para los cambios grandes (de sección, de idea, el CTA).
- **Silencio de la música** antes del remate: 0,3–0,6 s de hueco hacen que el golpe pese.
- **Corte J / L**: el audio de la escena siguiente entra antes (J) o el de la anterior sigue un
  poco (L). Suaviza los cortes en talking head.

## Catálogo de transiciones

| Transición | Cuándo | HyperFrames | Remotion |
|---|---|---|---|
| Corte seco | casi siempre; el default | cambiar de clip en el tiempo exacto | `<Series>` o `<Sequence>` |
| Match cut | misma forma o texto en los dos planos | `match-cut`, `text-match-cut`, `type-match-cut` | a mano: misma posición/escala en el corte |
| Whip pan | cambio de lugar o de tema con energía | `whip-pan-cut`, `whip-pan`, `cut-the-curve` | `slide()` corto + desenfoque de movimiento |
| Push / slide | listas, pasos, carrusel | `transitions-push`, `transitions-cover` | `slide({direction})` |
| Zoom / punch-in | énfasis, entrar a un detalle | `cinematic-zoom`, `parallax-zoom`, `parallax-device-dive` | `scale` animado con `spring` |
| Cortina / wipe | cambio de sección; diagonal = más dinámica | `transitions-radial`, `hw-scribble-transition`, `torn-paper-rip` | `wipe()`, `clockWipe()` |
| Iris / máscara | revelar algo | `iris-reveal`, `sdf-iris` | `iris()` |
| Flash | golpe, cambio brusco | `flash-through-white`, `editorial-flash-overlay` | capa blanca 2–3 cuadros |
| Glitch | tecnología, error, humor | `glitch`, `chromatic-radial-split` | capa con desplazamiento RGB |
| Fundido | tiempo que pasa, cierre emotivo | `fade-through`, `transitions-dissolve` | `fade()` |
| Objeto que tapa | algo cruza la cámara y al salir hay otro plano | se monta a mano con el objeto encima | igual |

Notas:
- `npx hyperframes catalog --tag transition` lista todas (son ~50); `npx hyperframes add <nombre> --no-clipboard`.
- En Remotion, `<TransitionSeries>` **resta** la duración de cada transición al total. Para que cada
  transición arranque justo en su corte de `cues.json` y el total quede igual a `duracion × fps`:
  duración de la escena *i* = (corte<sub>i+1</sub> − corte<sub>i</sub>) × fps + T<sub>salida i</sub>
  (los cuadros de la transición que sale de ella). El `<Audio>` va fuera del `<TransitionSeries>`.
  Ejemplo probado: escenas de 45 y 45 cuadros con una transición de 9 = 81 cuadros.
- Una transición vistosa por sección como mucho; el resto, cortes secos. Si todas son vistosas,
  ninguna se nota.
- Toda transición animada lleva sonido (whoosh, golpe, pop) salvo en el estilo minimal.

## Lo que mide `referencia.py` y cómo leerlo

- **corte**: salto brusco de un cuadro al siguiente (tiempo exacto).
- **animada**: el cuadro cambia mucho en 0,5 s sin un salto brusco (cortina, push, zoom, fundido).
  Tiempo aproximado ±0,2 s: mírala con `transicion`.
- **ráfaga**: varios saltos en menos de 0,25 s (flash, glitch, stickers que aparecen).
- **% en el beat / en un golpe**: cuántos cambios caen a ±80 ms. Más de 60 % = el editor corta
  a la música a propósito.
