#!/usr/bin/env python3
"""Desarma un video para que Claude lo «vea»: planos, cortes, transiciones, ritmo contra la música
y lo que se dice. Sirve para referencias y para revisar nuestros propios renders.

  python3 scripts/referencia.py <url|archivo> <carpeta> [--inicio 0:05] [--fin 0:40]
  python3 scripts/referencia.py transicion <carpeta> <seg|m:ss>...   8 cuadros alrededor de cada momento
  python3 scripts/referencia.py zoom <carpeta> <seg|m:ss>... [--ancho 768]

- URL de YouTube, Instagram, TikTok o cualquier sitio que baje yt-dlp. UNA descarga por video y
  siempre por la puerta (cuota compartida; un 429/403 crea STOP y no se reintenta).
- Retoma: no vuelve a bajar ni a transcribir; cortes, cuadros y ritmo se rehacen sin red.

Deja en <carpeta>:
  resumen.txt        ficha: título, cuenta, métricas, formato, descripción
  transcripcion.txt  [m:ss] frase (whisper local)
  ritmo.md           cortes, duración de planos, bpm, beats, secciones, % de cortes en el beat
  datos.json         lo mismo en crudo (para el sonidista y el editor)
  planos/            un cuadro por plano (y uno cada 3 s en planos largos)
  laminas/           hojas de contacto de ≤768 px · laminas.txt dice qué momento es cada casilla
"""
import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import puerta  # noqa: E402

CERCA = 0.08   # un corte «cae en el beat» si está a ±80 ms
MAX_CUADROS = 60


def seg(s):
    t = 0.0
    for p in str(s).split(':'):
        t = t * 60 + float(p)
    return t


def mmss(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


def ff(*args, **kw):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True, **kw)


def sonda(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate:format=duration',
                        '-of', 'json', str(video)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video')
    num, den = v.get('r_frame_rate', '30/1').split('/')
    return {'ancho': v['width'], 'alto': v['height'], 'fps': round(float(num) / float(den or 1), 2),
            'duracion': float(j['format']['duration']), 'audio': any(s['codec_type'] == 'audio' for s in j['streams'])}


def servicio(url):
    u = url.lower()
    for clave, s in (('youtu', 'youtube'), ('instagram.com', 'instagram'), ('tiktok.com', 'tiktok')):
        if clave in u:
            return s
    return 'web'


def bajar(src, d, ini, fin, cookies):
    video = d / 'video.mp4'
    if video.exists():
        return
    if Path(src).is_file():
        if ini is None and fin is None:
            video.symlink_to(Path(src).resolve())
        else:
            corte = (['-ss', str(ini)] if ini is not None else []) + (['-to', str(fin)] if fin is not None else [])
            ff(*corte, '-i', src, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', str(video))
        return
    s = servicio(src)
    puerta.gastar(s)
    cmd = ['yt-dlp', '-q', '--no-playlist', '-S', 'res:1080', '-f', 'bv*+ba/b', '--merge-output-format', 'mp4',
           '--remux-video', 'mp4', '--write-info-json', '-o', str(d / 'video.%(ext)s')]
    if cookies:  # solo con OK del usuario: lee las cookies de su navegador
        cmd += ['--cookies-from-browser', cookies]
    if ini is not None or fin is not None:
        cmd += ['--download-sections', f'*{ini or 0}-{fin if fin is not None else "inf"}', '--force-keyframes-at-cuts']
    r = subprocess.run(cmd + [src], capture_output=True, text=True)
    if r.returncode:
        err = r.stderr.strip()[-600:]
        if re.search(r'HTTP Error (429|403)|Too Many Requests|rate.?limit', err, re.I):
            puerta.bloquear(s, err[-200:])
            raise SystemExit(f'{s} devolvió bloqueo (429/403). Quedó STOP: no reintentar, avisar al usuario.\n'
                             f'Si yt-dlp está viejo, actualizarlo (brew upgrade yt-dlp) antes de desbloquear.\n{err}')
        if re.search(r'log ?in|cookies|private|sign in|age', err, re.I):
            raise SystemExit('El sitio pide iniciar sesión. Opciones: el usuario baja el video y pasa el archivo, '
                             'o (con su OK) --cookies-navegador chrome.\n' + err)
        raise SystemExit(err)
    if not video.exists():  # yt-dlp a veces deja otra extensión
        otro = next(p for p in d.glob('video.*') if p.suffix not in ('.json',) and not p.name.endswith('.info.json'))
        ff('-i', str(otro), '-c', 'copy', str(video))
        otro.unlink()


def resumen(d, m):
    f = d / 'video.info.json'
    i = json.loads(f.read_text()) if f.exists() else {}
    u = i.get('upload_date') or ''
    lineas = [
        f"titulo  : {i.get('title') or Path(os.path.realpath(d / 'video.mp4')).name}",
        f"cuenta  : {i.get('channel') or i.get('uploader') or '-'} ({i.get('channel_follower_count') or '?'} seguidores)",
        f"fecha   : {u[6:]}-{u[4:6]}-{u[:4]}" if u else 'fecha   : -',
        f"link    : {i.get('webpage_url') or '-'}",
        f"metricas: {i.get('view_count')} vistas · {i.get('like_count')} likes · {i.get('comment_count')} comentarios",
        f"formato : {m['ancho']}x{m['alto']} · {m['fps']} fps · {m['duracion']:.1f} s · {'con' if m['audio'] else 'sin'} audio",
        '', 'descripcion:', i.get('description') or '-',
    ]
    (d / 'resumen.txt').write_text('\n'.join(lineas) + '\n')
    return i.get('title') or 'video'


def modelo_whisper():
    if puerta.clave('WHISPER_MODEL', opcional=True):
        return Path(puerta.clave('WHISPER_MODEL'))
    modelos = sorted((Path.home() / 'modelos-whisper').glob('ggml-*.bin'), key=lambda p: 'turbo' not in p.name)
    return modelos[0] if modelos else None


def transcribir(d, m):
    """Arranca whisper en segundo plano; mientras, la CPU saca cuadros."""
    if (d / 'transcripcion.txt').exists():
        return None
    if not m['audio']:
        (d / 'transcripcion.txt').write_text('(sin audio)\n')
        return None
    modelo = modelo_whisper()
    if not shutil.which('whisper-cli') or not modelo:
        (d / 'transcripcion.txt').write_text('(sin whisper: corre bash scripts/kit.sh instalar)\n')
        return None
    ff('-i', str(d / 'video.mp4'), '-vn', '-ac', '1', '-ar', '16000', str(d / 'audio.wav'))
    return subprocess.Popen(['whisper-cli', '-m', str(modelo), '-l', 'auto', '-np', '-ovtt',
                             '-of', str(d / 'transcripcion'), '-f', str(d / 'audio.wav')],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def terminar_transcripcion(d, proceso, offset):
    if proceso is not None:
        if proceso.wait():
            raise SystemExit('whisper falló')
        (d / 'audio.wav').unlink()
        vtt, segmentos, t = d / 'transcripcion.vtt', [], None
        for linea in vtt.read_text().splitlines():
            if '-->' in linea:
                a, b = (seg(x.strip()) for x in linea.split('-->'))
                t = (offset + a, offset + b)
            elif linea.strip() and t:
                segmentos.append([round(t[0], 2), round(t[1], 2), linea.strip()])
        vtt.unlink()
        (d / 'segmentos.json').write_text(json.dumps(segmentos, ensure_ascii=False))
        (d / 'transcripcion.txt').write_text(''.join(f'[{mmss(a)}] {x}\n' for a, _, x in segmentos))
    f = d / 'segmentos.json'
    return json.loads(f.read_text()) if f.exists() else []


def distinto(a, b):
    """Fracción de píxeles (miniatura 64x36 en grises) que cambian más de 25 niveles."""
    return sum(abs(x - y) > 25 for x, y in zip(a, b)) / len(a)


def cortes(d, m, umbral_corte, umbral_cambio):
    """Dos tipos de cambio de plano, medidos sobre miniaturas de 64x36 cuadro a cuadro:
    - corte: salto brusco de un cuadro al siguiente (pico frente a sus vecinos). Varios en <0,25 s = ráfaga (flash, glitch).
    - animada: transición que dura (cortina, push, zoom, fundido); el cuadro cambia mucho en 0,5 s pero ningún
      salto es brusco. Su tiempo es aproximado (±0,2 s): mirarla con `transicion`.
    Los umbrales se adaptan al video (un motion graphics oscuro cambia pocos píxeles; un vlog, muchos);
    calibrados el 30-oct-2026 con un motion graphics oscuro, un vlog con TransitionSeries y un explicativo.
    """
    fps = min(m['fps'], 30)
    args = ['-an', '-vf', f'fps={fps},scale=64:36,format=gray', '-f', 'rawvideo', '-']
    try:  # decodificar por hardware gasta la mitad de CPU en Mac
        crudo = subprocess.run(['ffmpeg', '-v', 'error', '-hwaccel', 'videotoolbox', '-i', 'video.mp4', *args],
                               cwd=d, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        crudo = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'video.mp4', *args], cwd=d, capture_output=True, check=True).stdout
    n = 64 * 36
    f = [crudo[i:i + n] for i in range(0, len(crudo) - n + 1, n)]
    d1 = [0.0] + [distinto(f[i], f[i - 1]) for i in range(1, len(f))]
    k = max(1, round(fps / 2))
    w = [0.0] * k + [distinto(f[i], f[i - k]) for i in range(k, len(f))]
    umbral_corte = umbral_corte or max(0.15, min(0.4, 6 * statistics.median(d1)))
    umbral_cambio = umbral_cambio or max(0.15, min(0.55, 4 * statistics.median(w)))
    lista = []
    for i in range(1, len(f)):
        vecinos = sorted(d1[max(1, i - 5):i] + d1[i + 1:i + 6]) or [0]
        if d1[i] >= umbral_corte and d1[i] >= 3 * vecinos[len(vecinos) // 2] + 0.02:
            t = i / fps
            if lista and t - lista[-1]['ultimo'] < 0.25:
                lista[-1]['rafaga'] += 1
                lista[-1]['ultimo'] = t
            else:
                lista.append({'t': t, 'tipo': 'corte', 'fuerza': round(d1[i], 2), 'rafaga': 0, 'ultimo': t})
    duros = [c['t'] for c in lista]
    for i in range(k + 1, len(f) - 1):
        t = (i - k / 2) / fps
        if (w[i] >= umbral_cambio and w[i] >= w[i - 1] and w[i] > w[i + 1]
                and all(abs(t - x) > 0.6 for x in duros) and all(abs(t - c['t']) > 0.8 for c in lista if c['tipo'] == 'animada')):
            lista.append({'t': t, 'tipo': 'animada', 'fuerza': round(w[i], 2), 'rafaga': 0})
    lista.sort(key=lambda c: c['t'])
    return [{'t': round(c['t'], 3), 'tipo': c['tipo'], 'fuerza': c['fuerza'], 'rafaga': c['rafaga']} for c in lista]


def celdas(m):
    vertical = m['alto'] > m['ancho']
    return (188, '4x2', 8) if vertical else (252, '3x3', 9)  # ≤768 px de ancho


def cuadros(d, m, lista, offset):
    p = d / 'planos'
    shutil.rmtree(p, ignore_errors=True)
    p.mkdir()
    bordes = [0.0] + [c['t'] for c in lista] + [m['duracion']]
    tomas = []  # (tiempo, nº de plano, es inicio de plano)
    for k, (a, b) in enumerate(zip(bordes, bordes[1:]), 1):
        if b - a <= 3:
            tomas.append(((a + b) / 2, k, True))
        else:
            tomas += [(t, k, t == a + 0.4) for t in [a + 0.4 + 3 * i for i in range(int((b - a - 0.6) // 3) + 1)]]
    if len(tomas) > MAX_CUADROS:  # ponytail: muestreo parejo; si un video largo lo pide, analizar por tramos (--inicio/--fin)
        tomas = [tomas[round(i * (len(tomas) - 1) / (MAX_CUADROS - 1))] for i in range(MAX_CUADROS)]
    ancho = 360 if m['alto'] > m['ancho'] else 640
    for t, _, _ in tomas:
        ff('-ss', f'{t:.2f}', '-i', 'video.mp4', '-frames:v', '1', '-vf', f'scale={ancho}:-2', '-q:v', '3',
           f'planos/t{int((offset + t) * 10):06d}.jpg', cwd=d)
    l = d / 'laminas'
    shutil.rmtree(l, ignore_errors=True)
    l.mkdir()
    celda, grilla, n = celdas(m)
    ff('-pattern_type', 'glob', '-i', 'planos/t*.jpg', '-vf', f'scale={celda}:-2,tile={grilla}:padding=4:color=white',
       'laminas/l_%02d.jpg', cwd=d)
    (d / 'laminas.txt').write_text(''.join(
        f'l_{i // n + 1:02d}: ' + '  '.join(f'[{mmss(offset + t)} plano {k}]' for t, k, _ in tomas[i:i + n]) + '\n'
        for i in range(0, len(tomas), n)))
    return len(tomas)


def audio(d, m):
    """bpm, beats, secciones, golpes y volumen con HyperFrames (local, sin cuenta)."""
    if not m['audio'] or not shutil.which('npx'):
        return {}
    r = subprocess.run(['npx', '-y', 'hyperframes@latest', 'audio', 'video.mp4', '--only',
                        'bpm,beats,downbeats,sections,onsets,silence,loudness', '--json'],
                       cwd=d, capture_output=True, text=True)
    if r.returncode:
        print('aviso: hyperframes audio falló:', r.stderr.strip()[-300:])
        return {}
    return json.loads(r.stdout)['items'][0]


def cercano(t, tiempos):
    return min((x - t for x in tiempos), key=abs, default=None)


def ritmo(d, m, titulo, lista, a, segmentos, offset):
    bordes = [0.0] + [c['t'] for c in lista] + [m['duracion']]
    planos = [b - x for x, b in zip(bordes, bordes[1:])]
    beats = (a.get('beats') or {}).get('times') or []
    onsets = (a.get('onsets') or {}).get('events') or []
    fuertes = sorted(o['strength'] for o in onsets)
    piso = fuertes[int(len(fuertes) * 0.7)] if fuertes else 1
    golpes = [o['t'] for o in onsets if o['strength'] >= piso]
    for c in lista:
        c['beat'] = cercano(c['t'], beats)
        c['golpe'] = cercano(c['t'], golpes)
    en_beat = sum(1 for c in lista if c['beat'] is not None and abs(c['beat']) <= CERCA)
    en_golpe = sum(1 for c in lista if c['golpe'] is not None and abs(c['golpe']) <= CERCA)
    palabras = sum(len(x.split()) for _, _, x in segmentos)
    habla = sum(b - x for x, b, _ in segmentos)
    bpm = (a.get('bpm') or {}).get('value')
    vol = a.get('loudness') or {}
    pct = lambda n: f'{n} de {len(lista)} ({round(100 * n / len(lista))} %)' if lista else '-'
    filas = [
        ('Duración', f"{m['duracion']:.1f} s · {m['ancho']}x{m['alto']} · {m['fps']} fps"),
        ('Planos', f"{len(planos)} · {sum(c['tipo'] == 'corte' for c in lista)} cortes secos, "
                   f"{sum(c['tipo'] == 'animada' for c in lista)} transiciones animadas, {sum(1 for c in lista if c['rafaga'])} ráfagas (flash/glitch)"),
        ('Duración de plano', f"media {statistics.mean(planos):.2f} s · mediana {statistics.median(planos):.2f} s · "
                              f"mín {min(planos):.2f} · máx {max(planos):.2f}"),
        ('Cambios de plano por minuto', f"{60 * len(lista) / m['duracion']:.0f}"),
        ('Cambios en los primeros 3 s', str(sum(1 for c in lista if c['t'] < 3))),
        ('Música', f"{bpm:.0f} bpm · {len(beats)} beats" if bpm else f"sin beat estable detectado ({len(onsets)} golpes)"),
        ('Cortes en el beat (±80 ms)', pct(en_beat) if beats else '-'),
        ('Cortes en un golpe fuerte (±80 ms)', pct(en_golpe) if golpes else '-'),
        ('Habla', f"{palabras / habla:.1f} palabras/s · {palabras} palabras" if habla else 'sin voz detectada'),
        ('Volumen', f"{vol.get('lufsIntegrated')} LUFS · pico {vol.get('truePeakDb')} dB" if vol else '-'),
    ]
    ms = lambda x: '-' if x is None else f'{x * 1000:+.0f} ms'
    texto = [f'# Ritmo · {titulo}', '', '| Dato | Valor |', '|---|---|', *(f'| {k} | {v} |' for k, v in filas), '',
             '## Cambios de plano', '', 'Las animadas tienen tiempo aproximado (±0,2 s): mirarlas con `transicion`.', '',
             '| # | tiempo | tipo | plano que termina | beat más cercano | golpe más cercano | nota |', '|---|---|---|---|---|---|---|',
             *(f"| {i} | {mmss(offset + c['t'])} | {c['tipo']} | {planos[i - 1]:.2f} s | {ms(c['beat'])} | {ms(c['golpe'])} | "
               f"{'ráfaga ×' + str(c['rafaga'] + 1) if c['rafaga'] else ''} |" for i, c in enumerate(lista, 1)), '']
    secciones = (a.get('sections') or {}).get('spans') or []
    if secciones:
        texto += ['## Secciones de la música', '', '  '.join(f"{s['label']} {mmss(offset + s['start'])}–{mmss(offset + s['end'])}" for s in secciones), '']
    silencios = a.get('silence') or []
    if silencios:
        texto += ['## Silencios', '', str(silencios)[:600], '']
    (d / 'ritmo.md').write_text('\n'.join(texto))
    (d / 'datos.json').write_text(json.dumps({
        'offset': offset, 'medidas': m, 'cortes': lista, 'planos_s': [round(x, 3) for x in planos], 'bpm': bpm,
        'beats': beats, 'downbeats': (a.get('downbeats') or {}).get('times') or [], 'golpes_fuertes': golpes,
        'secciones': secciones, 'silencio': silencios, 'volumen': vol, 'segmentos': segmentos}, ensure_ascii=False))
    return filas


def tira(d, tiempos, modo, ancho):
    meta = json.loads((d / 'meta.json').read_text())
    m, offset = meta['medidas'], meta['offset']
    carpeta = d / ('transiciones' if modo == 'transicion' else 'zoom')
    carpeta.mkdir(exist_ok=True)
    for t in map(seg, tiempos):
        local = t - offset
        if modo == 'transicion':  # 8 cuadros a 10 fps: de 0,4 s antes a 0,4 s después
            celda = 180 if m['alto'] > m['ancho'] else 190
            f = carpeta / f'tr_{int(t * 10):05d}.jpg'
            ff('-ss', f'{max(0, local - 0.4):.2f}', '-t', '0.8', '-i', 'video.mp4', '-vf',
               f'fps=10,scale={celda}:-2,tile=4x2:padding=2:color=white', '-frames:v', '1', str(f), cwd=d)
        else:
            f = carpeta / f'z_{int(t * 10):05d}.jpg'
            ff('-ss', f'{local:.2f}', '-i', 'video.mp4', '-frames:v', '1', '-vf', f'scale={ancho}:-2', str(f), cwd=d)
        print(f)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('transicion', 'zoom'):
        a = argparse.ArgumentParser(prog=f'referencia.py {sys.argv[1]}')
        a.add_argument('carpeta', type=Path)
        a.add_argument('tiempos', nargs='+')
        a.add_argument('--ancho', type=int, default=768)
        o = a.parse_args(sys.argv[2:])
        return tira(o.carpeta.resolve(), o.tiempos, sys.argv[1], o.ancho)

    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('fuente', help='URL o archivo local')
    a.add_argument('carpeta', type=Path)
    a.add_argument('--inicio', type=seg)
    a.add_argument('--fin', type=seg)
    a.add_argument('--corte', type=float, help='salto mínimo para un corte seco, 0-1 (por defecto se adapta al video)')
    a.add_argument('--cambio', type=float, help='cambio mínimo en 0,5 s para una transición animada (por defecto se adapta)')
    a.add_argument('--cookies-navegador', help='chrome, safari… solo con OK del usuario (Instagram con login)')
    o = a.parse_args()

    d = o.carpeta.resolve()
    d.mkdir(parents=True, exist_ok=True)
    offset = o.inicio or 0.0
    bajar(o.fuente, d, o.inicio, o.fin, o.cookies_navegador)
    m = sonda(d / 'video.mp4')
    (d / 'meta.json').write_text(json.dumps({'fuente': o.fuente, 'offset': offset, 'medidas': m}))
    titulo = resumen(d, m)
    whisper = transcribir(d, m)
    lista = cortes(d, m, o.corte, o.cambio)
    n = cuadros(d, m, lista, offset)
    sonido = audio(d, m)
    segmentos = terminar_transcripcion(d, whisper, offset)
    filas = ritmo(d, m, titulo, lista, sonido, segmentos, offset)

    print(f'{titulo}\n')
    print('\n'.join(f'{k:36s} {v}' for k, v in filas))
    print(f"\ncuadros : {n} en planos/ · {len(list((d / 'laminas').glob('*.jpg')))} láminas en laminas/ (ver laminas.txt)")
    print(f'listo   : {d}/ritmo.md · transcripcion.txt · resumen.txt')
    print(f'siguiente: referencia.py transicion {d} <tiempos de 3-5 cortes>  para ver cómo está hecha cada transición')


if __name__ == '__main__':
    main()
