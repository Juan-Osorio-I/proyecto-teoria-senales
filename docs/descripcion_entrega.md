# Descripción para la plataforma (máximo 5 líneas)

Cargamos y segmentamos por energía 12 grabaciones WAV (16 kHz, mono) de los comandos «arriba», «abajo», «izquierda» y «derecha», con normalización por pico.
Caracterizamos cada señal en el tiempo (duración, amplitud, RMS, energía) y la analizamos con FFT y espectrogramas, interpretando las diferencias entre comandos.
Añadimos ruido blanco gaussiano con SNR controlada (20 y 5 dB) y comparamos la señal limpia con la alterada.
El código es reproducible con `python src/analisis.py` y el README documenta datos, conceptos y resultados.
Pendiente: ampliar la base a más hablantes, extraer MFCC, implementar el clasificador y evaluar el reconocimiento según el nivel de ruido.