#!/usr/bin/env python3
"""ElevenLabs por la puerta: voz, efectos de sonido y música.

Lo que cuesta (tts, sfx, musica) necesita permiso por lote: el director dice al usuario qué va a generar,
cuántas llamadas y el costo; con su OK corre `puerta.py permitir elevenlabs N`. Los subagentes nunca lo corren.
Cada audio deja al lado el texto o prompt que lo produjo, para editar y regenerar solo lo que cambia.

  python3 scripts/eleven.py saldo                                   créditos usados / límite (gratis)
  python3 scripts/eleven.py voces [texto]                           voces de la cuenta (gratis)
  python3 scripts/eleven.py biblioteca 'peruano narrador' carpeta   voces públicas + muestras para escuchar (gratis)
  python3 scripts/eleven.py tts VOICE_ID guion.txt salida           salida.mp3 + salida.json (tiempos por carácter)
  python3 scripts/eleven.py sfx 'whoosh corto y seco' 1.5 salida.mp3
  python3 scripts/eleven.py musica prompt.txt 30 salida.mp3         instrumental salvo EL_LETRA=1

Entorno opcional: EL_MODEL (por defecto eleven_multilingual_v2), EL_SETTINGS (JSON de voice_settings).
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import puerta  # noqa: E402

API = 'https://api.elevenlabs.io/v1'


def llamar(ruta, cuerpo=None, cobra=True, crudo=False):
    key = puerta.clave('ELEVENLABS_API_KEY')  # antes de gastar: sin key no se descuenta nada
    puerta.gastar('elevenlabs', cobra)
    req = urllib.request.Request(API + ruta, data=json.dumps(cuerpo).encode() if cuerpo is not None else None,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            datos = r.read()
    except urllib.error.HTTPError as e:
        cuerpo_error = e.read()[:300]
        if e.code in (401, 403, 429):
            puerta.bloquear('elevenlabs', f'{e.code} {cuerpo_error!r}')
        raise SystemExit(f'ElevenLabs {e.code}: {cuerpo_error!r}')
    return datos if crudo else json.loads(datos)


def main():
    a = sys.argv[1:] or ['-h']
    if a[0] == 'saldo':
        s = llamar('/user/subscription', cobra=False)
        print(s.get('tier'), s.get('character_count'), '/', s.get('character_limit'), 'caracteres')
    elif a[0] == 'voces':
        for v in llamar('/voices', cobra=False)['voices']:
            linea = f"{v['voice_id']} | {v['name']} | {json.dumps(v.get('labels', {}), ensure_ascii=False)}"
            if len(a) < 2 or a[1].lower() in linea.lower():
                print(linea)
    elif a[0] == 'biblioteca' and len(a) == 3:
        carpeta = Path(a[2])
        carpeta.mkdir(parents=True, exist_ok=True)
        r = llamar('/shared-voices?' + urllib.parse.urlencode({'search': a[1], 'page_size': 10}), cobra=False)
        for v in r.get('voices', []):
            print(v.get('voice_id'), '|', v.get('public_owner_id'), '|', v.get('name'), '|', v.get('accent'), '|',
                  v.get('gender'), '|', v.get('age'), '|', (v.get('description') or '')[:80])
            if v.get('preview_url'):  # muestra pública en su CDN: no pasa por la API
                with urllib.request.urlopen(v['preview_url'], timeout=60) as pr:
                    (carpeta / f"{v['voice_id']}.mp3").write_bytes(pr.read())
        print(f'muestras en {carpeta}/ — compáralas a ciegas antes de elegir')
    elif a[0] == 'tts' and len(a) == 4:
        texto, out = Path(a[2]).read_text().strip(), Path(a[3])
        ajustes = json.loads(os.environ.get('EL_SETTINGS') or '{"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "speed": 1.0}')
        r = llamar(f'/text-to-speech/{a[1]}/with-timestamps?output_format=mp3_44100_128',
                   {'text': texto, 'model_id': os.environ.get('EL_MODEL', 'eleven_multilingual_v2'), 'voice_settings': ajustes})
        out.with_suffix('.mp3').write_bytes(base64.b64decode(r['audio_base64']))
        out.with_suffix('.json').write_text(json.dumps(r['alignment'], ensure_ascii=False))
        out.with_suffix('.txt').write_text(f'voz {a[1]} · {os.environ.get("EL_MODEL", "eleven_multilingual_v2")} · {json.dumps(ajustes)}\n\n{texto}\n')
        print(out.with_suffix('.mp3'), len(texto), 'caracteres')
    elif a[0] == 'sfx' and len(a) == 4:
        Path(a[3]).write_bytes(llamar('/sound-generation', {'text': a[1], 'duration_seconds': float(a[2]),
                                                            'prompt_influence': 0.5}, crudo=True))
        Path(a[3]).with_suffix('.txt').write_text(f'{a[1]}\n{a[2]} s\n')
        print(a[3], '— recórtalo por energía: los SFX no respetan silencios ni golpes pedidos')
    elif a[0] == 'musica' and len(a) == 4:
        prompt = Path(a[1]).read_text().strip()
        Path(a[3]).write_bytes(llamar('/music?output_format=mp3_44100_128', {
            'prompt': prompt, 'music_length_ms': int(float(a[2]) * 1000), 'model_id': 'music_v1',
            'force_instrumental': os.environ.get('EL_LETRA') != '1'}, crudo=True))
        Path(a[3]).with_suffix('.txt').write_text(f'{prompt}\n{a[2]} s\n')
        print(a[3])
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
