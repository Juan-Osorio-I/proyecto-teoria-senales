# Datos

## Estructura

```
data/
├── muestras/        <- los .wav usados por el código (pocos y livianos, SÍ se suben)
└── completa/        <- base de datos completa (NO se sube, está en .gitignore)
```

## Formato de los audios

| Parámetro | Valor |
|---|---|
| Formato | WAV (sin compresión) |
| Frecuencia de muestreo | 16 000 Hz |
| Canales | 1 (mono) |
| Resolución | 16 bits |
| Duración de cada archivo | ~1.5 a 2 s (comando con silencio antes y después) |

## Nombre de los archivos

`<comando>_h<hablante>_r<repetición>.wav`

Ejemplos: `arriba_h01_r01.wav`, `izquierda_h03_r02.wav`

Comandos válidos: `arriba`, `abajo`, `izquierda`, `derecha` (en minúscula y sin tilde).

## Base de datos completa

Enlace: **[COMPLETAR: enlace de Google Drive]**

## Referencia externa (comparación)

Google Speech Commands (palabras en inglés: up, down, left, right):
Warden, P. (2018). *Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition*. arXiv:1804.03209. https://arxiv.org/abs/1804.03209