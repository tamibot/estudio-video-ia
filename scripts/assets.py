#!/usr/bin/env python3
"""Busca y baja assets para la lista de assets de un video, siempre por la puerta.

  python3 scripts/assets.py pinturas "lovers kiss" proyectos/<v>/assets/pinturas [--n 4]
  python3 scripts/assets.py fotos "Arthur Brooks portrait" proyectos/<v>/assets/fotos [--n 4] [--cc]
  python3 scripts/assets.py broll "man fighting shadow" proyectos/<v>/assets/broll [--n 4] [--horizontal]

- pinturas y fotos: Wikimedia Commons, solo dominio público o CC0 (con --cc también CC BY / BY-SA,
  que piden crédito). Gratis, sin key.
- broll: Pexels (gratis; pide PEXELS_API_KEY en .env, se saca en https://www.pexels.com/api/).
  Vertical por defecto.
Deja los archivos y `fuentes.json` (título, autor, licencia, enlace) para dar crédito. La persona
elige entre los candidatos; lo que no se usa se borra al cerrar el video.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import puerta  # noqa: E402

UA = {'User-Agent': 'estudio-video-ia/1.0 (https://github.com/tamibot/estudio-video-ia)'}
LIBRES = re.compile(r'public domain|^pd\b|pd-|cc0', re.I)
CC = re.compile(r'^cc[ -]by', re.I)


def pedir(servicio, url, headers=None, crudo=False):
    puerta.gastar(servicio, cobra=False)
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            datos = r.read()
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            puerta.bloquear(servicio, f'{e.code} {url[:120]}')
            raise SystemExit(f'{servicio} devolvió {e.code}: quedó STOP, no reintentar, avisar.')
        if e.code == 401:
            raise SystemExit(f'{servicio} 401: revisa la key en .env (open -e .env).')
        raise SystemExit(f'{servicio} {e.code}: {e.read()[:200]!r}')
    return datos if crudo else json.loads(datos)


def nombre(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60] or 'asset'


def buscar_commons(busqueda):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'generator': 'search', 'gsrnamespace': 6, 'gsrlimit': 30,
        'gsrsearch': f'{busqueda} filetype:bitmap', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size',
        'iiurlwidth': 1600})
    return list((pedir('wikimedia', url).get('query') or {}).get('pages', {}).values())


def commons(q, carpeta, n, cc, pintura):
    # «painting» ayuda a que salgan cuadros, pero con nombres propios deja la búsqueda vacía: segundo intento sin él
    paginas = (buscar_commons(f'{q} painting') if pintura else []) or buscar_commons(q)
    hechos = []
    for pg in sorted(paginas, key=lambda x: x.get('index', 99)):
        ii = (pg.get('imageinfo') or [{}])[0]
        meta = {k: re.sub('<[^>]+>', '', str((v or {}).get('value', ''))).strip() for k, v in (ii.get('extmetadata') or {}).items()}
        lic = meta.get('LicenseShortName', '')
        if not (LIBRES.search(lic) or (cc and CC.search(lic))) or not ii.get('thumburl'):
            continue
        f = carpeta / f"{nombre(pg['title'].removeprefix('File:').rsplit('.', 1)[0])}.jpg"
        f.write_bytes(pedir('wikimedia', ii['thumburl'], crudo=True))
        hechos.append({'archivo': f.name, 'titulo': pg['title'], 'autor': meta.get('Artist', ''), 'licencia': lic,
                       'credito': meta.get('Attribution', '') or meta.get('Credit', ''), 'enlace': ii.get('descriptionurl')})
        if len(hechos) == n:
            break
    return hechos


def pexels(q, carpeta, n, horizontal):
    key = puerta.clave('PEXELS_API_KEY')
    url = 'https://api.pexels.com/videos/search?' + urllib.parse.urlencode({
        'query': q, 'per_page': max(n * 2, 8), 'orientation': 'landscape' if horizontal else 'portrait'})
    hechos = []
    for v in pedir('pexels', url, {'Authorization': key}).get('videos', []):
        archivos = [a for a in v.get('video_files', []) if a.get('file_type') == 'video/mp4' and (a.get('height') or 0) <= 1920]
        if not archivos:
            continue
        mejor = max(archivos, key=lambda a: a.get('height') or 0)
        f = carpeta / f"pexels-{v['id']}.mp4"
        f.write_bytes(pedir('pexels', mejor['link'], crudo=True))
        hechos.append({'archivo': f.name, 'autor': (v.get('user') or {}).get('name', ''), 'licencia': 'Pexels (uso libre, crédito sugerido)',
                       'enlace': v.get('url'), 'duracion_s': v.get('duration'), 'tamano': f"{mejor.get('width')}x{mejor.get('height')}"})
        if len(hechos) == n:
            break
    return hechos


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('tipo', choices=['pinturas', 'fotos', 'broll'])
    a.add_argument('busqueda')
    a.add_argument('carpeta', type=Path)
    a.add_argument('--n', type=int, default=4)
    a.add_argument('--cc', action='store_true', help='fotos: aceptar también CC BY / BY-SA (piden crédito)')
    a.add_argument('--horizontal', action='store_true', help='broll: horizontal en vez de vertical')
    o = a.parse_args()
    o.carpeta.mkdir(parents=True, exist_ok=True)
    hechos = (pexels(o.busqueda, o.carpeta, o.n, o.horizontal) if o.tipo == 'broll'
              else commons(o.busqueda, o.carpeta, o.n, o.cc, o.tipo == 'pinturas'))
    registro = o.carpeta / 'fuentes.json'
    previos = json.loads(registro.read_text()) if registro.exists() else []
    registro.write_text(json.dumps(previos + [dict(h, busqueda=o.busqueda) for h in hechos], ensure_ascii=False, indent=1))
    for h in hechos:
        print(f"{o.carpeta / h['archivo']} · {h['licencia']} · {h.get('autor', '')[:40]}")
    if not hechos:
        print('Nada con licencia libre para esa búsqueda: prueba en inglés o con otras palabras.')


if __name__ == '__main__':
    main()
