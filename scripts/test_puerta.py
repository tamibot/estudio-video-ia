#!/usr/bin/env python3
"""Prueba de la puerta en una carpeta temporal: permiso por lote, tope diario, STOP. python3 scripts/test_puerta.py"""
import tempfile
from pathlib import Path

import puerta

puerta.DIR = Path(tempfile.mkdtemp())
puerta.LIMITES = {'pago': (0, 3, True), 'gratis': (0, 2, False)}


def niega(f, *a):
    try:
        f(*a)
    except SystemExit as e:
        return str(e)
    raise AssertionError('debía negarse')


assert 'Sin permiso' in niega(puerta.gastar, 'pago')                 # sin OK no se gasta
puerta.gastar('pago', cobra=False)                                    # llamadas gratis del mismo servicio sí pasan
c = puerta._leer(puerta._archivos('pago')[0])
c['permitidas'] = 1
puerta._archivos('pago')[0].write_text(__import__('json').dumps(c))
puerta.gastar('pago')                                                 # gasta el único permiso
assert 'Sin permiso' in niega(puerta.gastar, 'pago')                 # y el siguiente se niega
puerta.gastar('gratis'); puerta.gastar('gratis')
assert 'Tope diario' in niega(puerta.gastar, 'gratis')               # tope diario
puerta.bloquear('pago', '429 prueba')
assert 'STOP' in niega(puerta.gastar, 'pago')                        # STOP frena todo
print('puerta ok')
