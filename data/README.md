# Datos

## Estructura

```
data/
└── muestras/        <- grabaciones .wav de la entrega (livianas, se suben a GitHub)
```

## Contenido actual

12 grabaciones de **un hablante (h01)**: 4 comandos (`arriba`, `abajo`, `izquierda`, `derecha`) × 3 repeticiones.

Las grabó el propio integrante Juan José Osorio Isaza con el micrófono de su computador, en un lugar silencioso, usando Audacity. Cada palabra se separó de la grabación continua con la herramienta de etiquetas y se exportó como un archivo individual.

## Formato de los audios

| Parámetro | Valor |
|---|---|
| Formato | WAV (sin compresión) |
| Frecuencia de muestreo | 16 000 Hz |
| Canales | 1 (mono) |
| Resolución | 16 bits |
| Duración de cada archivo | ~1 s (palabra con ~0.3 s de silencio antes y después) |

## Nombre de los archivos

`<comando>_h<hablante>_r<repetición>.wav`

Ejemplos: `arriba_h01_r01.wav`, `izquierda_h03_r02.wav`

Comandos válidos: `arriba`, `abajo`, `izquierda`, `derecha` (en minúscula y sin tilde).

## Limitaciones

- Un solo hablante: no permite medir la variabilidad entre personas.
- Solo 3 repeticiones por comando.
- Para la entrega final se planea ampliar a más hablantes y repeticiones (ver [`docs/guia_de_grabacion.md`](../docs/guia_de_grabacion.md)).

## Referencia externa (comparación)

Google Speech Commands v0.02 (palabras en inglés: up, down, left, right):
Warden, P. (2018). *Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition*. arXiv:1804.03209.
https://arxiv.org/abs/1804.03209