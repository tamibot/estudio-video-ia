#!/usr/bin/env python3
"""Puerta única para todo servicio con cuota o con costo: descargas (YouTube, Instagram, TikTok),
ElevenLabs y OpenAI. Ningún script llama a esos servicios sin pasar por gastar().

- Contador compartido entre procesos en ~/.cache/estudio-video-ia/<servicio>.json, con lock,
  pausa mínima entre llamadas y tope diario. El límite lo rompe la SUMA de procesos: por eso es uno solo.
- Falla CERRADO: si el contador no se puede leer o existe el STOP del servicio, no se llama.
- Un 401/403/429 crea STOP: no se reintenta hasta que una persona confirme que pasó el bloqueo.
- Lo que cuesta dinero necesita permiso por lote: el director pregunta al usuario y recién
  corre `puerta.py permitir <servicio> N`. Cada llamada pagada gasta 1; en 0 se niega.

  python3 scripts/puerta.py estado
  python3 scripts/puerta.py permitir openai 4        (solo tras el OK del usuario en el chat)
  python3 scripts/puerta.py desbloquear youtube      (solo tras confirmar que el bloqueo pasó)
"""
import fcntl
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

DIR = Path.home() / '.cache/estudio-video-ia'
# servicio: (pausa mínima en s, tope diario, cuesta dinero)
LIMITES = {
    'youtube': (5, 40, False),
    'instagram': (8, 30, False),
    'tiktok': (5, 40, False),
    'web': (5, 40, False),
    'elevenlabs': (2, 40, True),
    'openai': (2, 20, True),
}


def _archivos(servicio):
    if servicio not in LIMITES:
        raise SystemExit(f'servicio desconocido: {servicio} (válidos: {", ".join(LIMITES)})')
    DIR.mkdir(parents=True, exist_ok=True)
    return DIR / f'{servicio}.json', DIR / f'STOP-{servicio}'


def _leer(f):
    return json.loads(f.read_text()) if f.exists() else {'dia': '', 'n': 0, 'ultima': 0, 'permitidas': 0}


def gastar(servicio, cobra=True):
    """Bloquea hasta que se pueda llamar; si no se puede, termina el proceso con el motivo."""
    f, stop = _archivos(servicio)
    pausa, tope, cuesta = LIMITES[servicio]
    if stop.exists():
        raise SystemExit(f'STOP en {servicio}: {stop.read_text().strip()}\nNo se reintenta. Avisa al usuario.')
    with open(DIR / f'{servicio}.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        c = _leer(f)
        hoy = date.today().isoformat()
        if c['dia'] != hoy:
            c.update(dia=hoy, n=0)
        if c['n'] >= tope:
            raise SystemExit(f'Tope diario de {servicio} alcanzado ({tope}). Sigue mañana.')
        if cuesta and cobra:
            if c.get('permitidas', 0) <= 0:
                raise SystemExit(f'Sin permiso para gastar en {servicio}. Di al usuario qué vas a generar, '
                                 f'cuántas llamadas y el costo; con su OK corre: python3 scripts/puerta.py permitir {servicio} N')
            c['permitidas'] -= 1
        time.sleep(max(0, c['ultima'] + pausa - time.time()))
        c['n'] += 1
        c['ultima'] = time.time()
        f.write_text(json.dumps(c))
    with open(DIR / 'llamadas.log', 'a') as log:
        log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}\t{servicio}\t{Path(sys.argv[0]).name}\t{" ".join(sys.argv[1:3])}\n')


def clave(nombre, opcional=False):
    """Valor desde el entorno o desde .env del repo (keys incluidas). Nunca se imprime."""
    if os.environ.get(nombre):
        return os.environ[nombre]
    env = Path(__file__).resolve().parent.parent / '.env'
    if env.exists():
        for linea in env.read_text().splitlines():
            k, _, v = linea.partition('=')
            if k.strip() == nombre and v.strip():
                return v.strip().strip('"\'')
    if opcional:
        return None
    raise SystemExit(f'Falta {nombre} en .env. El usuario la pega en el archivo .env (nunca en el chat).')


def bloquear(servicio, motivo):
    _, stop = _archivos(servicio)
    stop.write_text(f'{time.ctime()} · {motivo}\n')


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else 'estado'
    if orden == 'permitir' and len(sys.argv) == 4:
        f, _ = _archivos(sys.argv[2])
        with open(DIR / f'{sys.argv[2]}.lock', 'w') as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            c = _leer(f)
            c['permitidas'] = int(sys.argv[3])
            f.write_text(json.dumps(c))
        print(f'{sys.argv[2]}: {sys.argv[3]} llamadas permitidas')
    elif orden == 'desbloquear' and len(sys.argv) == 3:
        _archivos(sys.argv[2])[1].unlink(missing_ok=True)
        print(f'{sys.argv[2]}: STOP borrado')
    elif orden == 'estado':
        hoy = date.today().isoformat()
        for s, (pausa, tope, cuesta) in LIMITES.items():
            f, stop = _archivos(s)
            c = _leer(f)
            n = c['n'] if c['dia'] == hoy else 0
            extra = f" · permitidas {c.get('permitidas', 0)}" if cuesta else ''
            print(f"{s:11s} hoy {n}/{tope}{extra}{' · STOP: ' + stop.read_text().strip() if stop.exists() else ''}")
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
