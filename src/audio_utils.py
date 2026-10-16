"""
audio_utils.py
Funciones básicas para cargar, preprocesar y caracterizar grabaciones de
comandos de voz (arriba, abajo, izquierda, derecha).

Convención de nombres de archivo:  <comando>_h<hablante>_r<repetición>.wav
Ejemplo: arriba_h01_r02.wav
"""
import os
import re

import numpy as np
from scipy.io import wavfile

COMANDOS = ["arriba", "abajo", "izquierda", "derecha"]
_PATRON_NOMBRE = re.compile(r"^(?P<comando>[a-z]+)_h(?P<hablante>\d+)_r(?P<rep>\d+)\.wav$")


def cargar_wav(ruta):
    """Carga un WAV y devuelve (fs, x).

    x es una señal mono en punto flotante con escala completa en [-1, 1].
    Se divide por el máximo del tipo de dato (no por el pico de la señal)
    para conservar la amplitud real de la grabación.
    """
    fs, x = wavfile.read(ruta)
    if x.ndim > 1:                      # estéreo -> mono (promedio de canales)
        x = x.mean(axis=1)
    if x.dtype == np.uint8:             # WAV de 8 bits (sin signo)
        x = (x.astype(np.float64) - 128.0) / 128.0
    elif np.issubdtype(x.dtype, np.integer):
        x = x.astype(np.float64) / np.iinfo(x.dtype).max
    else:                               # ya viene en punto flotante
        x = x.astype(np.float64)
    return fs, x


def parsear_nombre(nombre_archivo):
    """Extrae (comando, hablante, repetición) del nombre del archivo."""
    m = _PATRON_NOMBRE.match(os.path.basename(nombre_archivo).lower())
    if m is None:
        return None
    return m.group("comando"), int(m.group("hablante")), int(m.group("rep"))


def listar_grabaciones(carpeta):
    """Devuelve una lista de dicts con ruta, comando, hablante y repetición."""
    registros = []
    for nombre in sorted(os.listdir(carpeta)):
        info = parsear_nombre(nombre)
        if info is None:
            continue
        comando, hablante, rep = info
        registros.append({
            "ruta": os.path.join(carpeta, nombre),
            "archivo": nombre,
            "comando": comando,
            "hablante": hablante,
            "repeticion": rep,
        })
    return registros