# Plataformas: formatos, zonas seguras y exportación

## Formatos

| Destino | Tamaño | Duración que funciona |
|---|---|---|
| Reels, TikTok, Shorts, historias | 1080×1920 (9:16), 30 fps | 7–30 s; hasta 60–90 s si retiene |
| Feed Instagram / Facebook | 1080×1350 (4:5) | 15–45 s |
| YouTube | 1920×1080 (16:9), 30 fps (60 si hay pantalla con scroll) | lo que pida el tema |
| LinkedIn | 1080×1350 o 1920×1080 | 30–90 s |
| Anuncios Meta / TikTok | 9:16 y 4:5 del mismo video | 15–30 s; el mensaje en los primeros 3 s |

Un video vertical bien hecho se adapta a 4:5 recortando arriba y abajo: dejar lo esencial en el centro.

## Zona segura vertical (1080×1920)

- Lo esencial (textos, caras, producto, subtítulos) entre **y ≈ 260 y y ≈ 1480**.
- Entre y ≈ 900 y y ≈ 1480 no pasar de **x ≈ 944**: ahí van los botones de la app (me gusta,
  comentar, compartir).
- Arriba de y ≈ 260 y abajo de y ≈ 1480 solo lo decorativo: lo tapan el nombre de la cuenta,
  la descripción y la barra.
- Subtítulos alrededor de y ≈ 1100–1250, nunca pegados abajo.

## Lo que pide el formato corto

- Algo pasa en el cuadro 1. El primer cuadro funciona como portada.
- Subtítulos siempre (la mayoría mira sin sonido), cortos, 2–4 palabras por pantalla.
- Un solo mensaje y un solo CTA. El CTA se queda en pantalla al menos 2 s.
- En anuncios, el producto o el resultado aparece en los primeros 3 s.

## Exportación de entrega

```
H.264 (High), yuv420p, 30 fps constantes, bitrate ~10–16 Mbps en 1080p
AAC 48 kHz estéreo 192 kbps · −14 LUFS integrados · pico real ≤ −1 dB
-movflags +faststart
```

Con ffmpeg, si hay que reempaquetar:
`ffmpeg -i in.mp4 -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -crf 18 -c:a aac -ar 48000 -b:a 192k -movflags +faststart out.mp4`

Volumen a −14 LUFS sin tocar la imagen:
`ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k out.mp4`

Verificar siempre: `ffprobe` (duración, tamaño, fps) y mirar cuadros del archivo final, no del preview.
