# Audio: voz, música, efectos y mezcla

## Voz

**Grabada por la persona.** Celular o micrófono a un palmo, cuarto con cosas blandas (no baño ni
cocina), sin música de fondo. Se limpia con ffmpeg (`highpass=f=80`, `afftdn`, compresión suave)
y se transcribe con tiempos.

**IA con ElevenLabs** (`scripts/eleven.py`, cuesta):
- Elegir voz comparando a ciegas: varias muestras con el mismo texto en un solo archivo, sin decir
  cuál es cuál. `eleven.py biblioteca '<acento estilo>' carpeta` baja muestras públicas gratis.
- Una voz «diseñada» con acento local suele sonar neutra; una voz real de la biblioteca con ese
  acento suele ganar.
- Escribir para el oído: nombres de marca como se pronuncian («Chat Yi Pi Ti», «Clod»); pausas con
  puntos y comas, nunca con «…».
- Ahorro: varios textos en UNA llamada y cortar por la alineación (`salida.json`).
- La alineación se equivoca en los bordes: cortar silencios por energía (≈ −48 dB), no por la
  alineación. Whisper también se salta frases en bordes de segmento.
- Voces lentas (≈2,2 palabras/s) se pueden acelerar ×1,1–1,25 con `rubberband` o `atempo`
  (entrar en float y a −3 dB para que no recorte).

## Música

- Fuente: generada (`eleven.py musica`, instrumental por defecto), propia, o libre con licencia y
  crédito. Nunca la música de una referencia.
- Prompt: género, bpm (el de `ESTILO.md`), energía, instrumentos, estructura («intro suave 4 s,
  sube en el segundo 8, golpe final»), «sin voces».
- Empezar desde el tramo fuerte (coro o drop), no desde el segundo 0. Ubicar el remate por
  energía y hacer que caiga en la última palabra o en el CTA.
- Medir: `npx -y hyperframes audio musica.mp3 --only bpm,beats,downbeats,sections,onsets --json`.

## Efectos

- Kit básico: whoosh (transiciones), hit/golpe (cortes fuertes), pop (texto que aparece),
  riser (antes de una revelación o del CTA), click/tecleo (interfaces).
- Antes de generar, buscar libres: HyperFrames trae ~21 efectos sin conexión
  (`npx hyperframes media-use resolve --type sfx --intent "whoosh" --candidates`); Remotion tiene
  `@remotion/sfx`.
- Los efectos de ElevenLabs no respetan la estructura pedida (silencios, golpes sueltos):
  recortarlos por energía. Los sintetizados con código suenan falsos.

## Mezcla

| Pista | Nivel orientativo |
|---|---|
| Voz | protagonista; ≈ −16 a −14 LUFS de corto plazo |
| Música bajo voz | 12–18 dB por debajo de la voz (ducking) |
| Música sin voz | sube 6–10 dB |
| Efectos | −10 a −6 dB respecto de la voz; que no tapen palabras |
| **Final** | **−14 LUFS integrados, pico real ≤ −1 dB** |

- No empujar la voz +7 dB contra el limitador: aplasta los picos y suena áspera. Mejor bajar el resto.
- Voz con muchas «s»: no realzar agudos; recorte suave arriba de 7 kHz.

## Verificar (números, no oído cansado)

- Volumen: `npx -y hyperframes audio mezcla.wav --only loudness` → −14 ±1 LUFS, pico ≤ −1 dB.
- Inteligibilidad: transcribir la mezcla con whisper y comparar con el guion; no debe faltar
  ninguna frase.
- Voz sobre fondo: ≥ 10 dB entre 300 Hz y 4 kHz en cada frase.
- Escuchar cada corte: que no se coma la primera sílaba ni deje un clic.
