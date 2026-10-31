#!/usr/bin/env python3
"""Imágenes con OpenAI por la puerta. Solo cuando suman: un plano clave, un fondo, un producto, una textura.
Todo lo demás se hace con HyperFrames o Remotion.

Cada imagen necesita permiso por lote: el director dice al usuario qué imágenes, cuántas y el costo;
con su OK corre `puerta.py permitir openai N`. Los subagentes nunca lo corren.

  python3 scripts/imagen.py prompt.txt salida.png [--tamano 1024x1536] [--calidad high] [--ref foto.png ...]

- prompt.txt lleva sujeto, acción, encuadre, luz, estilo y lo que NO debe aparecer (guias/estilos.md).
- Con --ref, las fotos son referencia (producto real, rostro, logo): usa el endpoint de edición.
- Deja salida.png y salida.json con modelo, tamaño, prompt y referencias, para regenerar solo lo que cambia.
- Tamaños: 1024x1024, 1536x1024 (horizontal), 1024x1536 (vertical). OPENAI_IMAGE_MODEL elige el modelo.
"""
import argparse
import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import puerta  # noqa: E402

API = 'https://api.openai.com/v1/images'


def multipart(campos, archivos):
    b = uuid.uuid4().hex
    partes = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in campos.items()]
    for ruta in archivos:
        tipo = mimetypes.guess_type(ruta)[0] or 'image/png'
        partes.append(f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{Path(ruta).name}"\r\n'
                      f'Content-Type: {tipo}\r\n\r\n'.encode() + Path(ruta).read_bytes() + b'\r\n')
    return b''.join(partes) + f'--{b}--\r\n'.encode(), f'multipart/form-data; boundary={b}'


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('prompt', type=Path)
    a.add_argument('salida', type=Path)
    a.add_argument('--tamano', default='1024x1536')
    a.add_argument('--calidad', default='high', choices=['low', 'medium', 'high'])
    a.add_argument('--ref', nargs='*', default=[])
    o = a.parse_args()
    for f in [o.prompt, *o.ref]:
        if not Path(f).exists():
            raise SystemExit(f'no existe: {f}')
    texto = o.prompt.read_text().strip()
    modelo = puerta.clave('OPENAI_IMAGE_MODEL', opcional=True) or 'gpt-image-1'
    campos = {'model': modelo, 'prompt': texto, 'size': o.tamano, 'quality': o.calidad, 'n': 1}

    auth = {'Authorization': f"Bearer {puerta.clave('OPENAI_API_KEY')}"}  # antes de gastar
    puerta.gastar('openai')
    if o.ref:
        cuerpo, tipo = multipart(campos, o.ref)
        req = urllib.request.Request(f'{API}/edits', data=cuerpo, headers={**auth, 'Content-Type': tipo})
    else:
        req = urllib.request.Request(f'{API}/generations', data=json.dumps(campos).encode(),
                                     headers={**auth, 'Content-Type': 'application/json'})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        error = e.read()[:300]
        if e.code == 401:
            raise SystemExit('OpenAI 401: key inválida o vencida. Corrígela en .env (open -e .env); no hace falta desbloquear.')
        if e.code in (403, 429):
            puerta.bloquear('openai', f'{e.code} {error!r}')
        raise SystemExit(f'OpenAI {e.code}: {error!r}')
    o.salida.parent.mkdir(parents=True, exist_ok=True)
    o.salida.write_bytes(base64.b64decode(d['data'][0]['b64_json']))
    o.salida.with_suffix('.json').write_text(json.dumps({
        'modelo': modelo, 'tamano': o.tamano, 'calidad': o.calidad, 'prompt': texto, 'refs': [str(r) for r in o.ref],
        'uso': d.get('usage'), 'segundos': round(time.time() - t0), 'fecha': time.strftime('%Y-%m-%d %H:%M')}, ensure_ascii=False, indent=1))
    print(f'{o.salida} ({round(time.time() - t0)} s) — achícala antes de mirarla: sips -Z 768')


if __name__ == '__main__':
    main()
