# Reconocimiento de comandos de voz mediante procesamiento de señales

**Universidad de Manizales — Teoría de Señales (2026)**
**Docente:** Milady Cristina Guapacha Montoya
**Integrantes:** Juan José Osorio Isaza · Julián Andrés Hernández Tobón

---

## 1. Descripción

Estudiamos la señal de voz de cuatro comandos en español: **«arriba», «abajo», «izquierda» y «derecha»**. El objetivo final es un sistema capaz de reconocer cada comando a partir de sus características temporales, espectrales y tiempo-frecuencia, y de evaluar cómo afecta el ruido al reconocimiento.

En esta entrega 2 se construyó el flujo de análisis inicial: carga de grabaciones, segmentación, normalización, caracterización en el tiempo, efecto del ruido, FFT y espectrogramas, aplicado a una primera base de **12 grabaciones de un hablante**.

## 2. Estado actual (Entrega 2)

| Hecho | Pendiente |
|---|---|
| Carga de grabaciones WAV y documentación de fs, Ts y duración | Ampliar la base de datos (más hablantes y más repeticiones) |
| Representación temporal de cada comando | Extracción de MFCC |
| Segmentación del comando (recorte de silencio por energía) | Clasificador (MFCC + kNN/SVM) y métricas (accuracy, matriz de confusión) |
| Normalización por pico | Preprocesamiento adicional (pre-énfasis, filtrado) |
| Caracterización: duración, amplitud, RMS, energía, cruces por cero | Evaluación del reconocimiento en función de la SNR |
| Ruido blanco gaussiano con SNR controlada (20 y 5 dB) | Ruido ambiental real y filtrado para mitigarlo |
| Primer análisis en frecuencia (FFT) y espectrogramas | Separación entrenamiento/prueba por hablante |

**Limitación actual:** todas las grabaciones son de un solo hablante (h01), por lo que aún no se puede medir la variabilidad entre personas. Los resultados de la sección 6 son una primera exploración, no una evaluación del reconocimiento.

## 3. Datos

- **Base propia:** 12 grabaciones (4 comandos × 3 repeticiones) de 1 hablante (h01), en `data/muestras/`. Formato WAV, **16 kHz, mono, 16 bits**. Cada archivo contiene la palabra con unos 0.3 s de silencio antes y después.
- Nombre de archivo: `<comando>_h<hablante>_r<repetición>.wav` (por ejemplo `arriba_h01_r01.wav`).
- Se grabó con Audacity a 16 kHz mono y se separó cada palabra con etiquetas, exportando un archivo por repetición.
- Detalles en [`data/README.md`](data/README.md) y [`docs/guia_de_grabacion.md`](docs/guia_de_grabacion.md).
- **Referencia externa:** Google Speech Commands (Warden, 2018), palabras en inglés *up, down, left, right*. Se usará como comparación en la entrega final, no como base principal.

**Frecuencia de muestreo:** fs = 16 000 Hz → Ts = 1/fs = 62.5 µs. Por Nyquist se representan componentes hasta fs/2 = 8 kHz, rango donde está la información útil de la voz (vocales y fricativas).

## 4. Cómo ejecutar

Requisitos: Python 3.9 o superior.

```bash
git clone https://github.com/Juan-Osorio-I/proyecto-teoria-senales.git
cd proyecto-teoria-senales
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/analisis.py --datos data/muestras --salida results
```

Genera en `results/`: la tabla de características por grabación (`tabla_caracteristicas.csv`), el resumen por comando (`resumen_por_comando.csv`) y las cinco figuras descritas abajo.

Estructura:

```
src/audio_utils.py   funciones: carga, recorte, normalización, ruido, FFT, características
src/analisis.py      script principal: tablas y gráficas
data/                grabaciones (muestras) y documentación de los datos
results/             gráficas y tablas generadas
docs/                guía de grabación y descripción de la entrega
```

## 5. Conceptos de Teoría de Señales utilizados

- **Señal en tiempo discreto y muestreo:** x[n] = x(nTs), Ts = 1/fs; criterio de Nyquist.
- **Dominio temporal:** amplitud, valor medio, valor RMS, energía E = Σ x[n]², duración, cruces por cero.
- **Segmentación por energía** en tramos de 20 ms (la voz es aproximadamente estacionaria en tramos cortos): se conservan los tramos cuya energía supera el 5 % del máximo, más un margen de 40 ms.
- **Normalización** por amplitud pico.
- **Ruido aditivo** y relación señal-ruido: y[n] = x[n] + r[n], SNR = 10·log₁₀(Px/Pr).
- **Análisis en frecuencia:** DFT/FFT con ventana de Hann, espectro de magnitud de 0 a fs/2.
- **Análisis tiempo-frecuencia:** espectrograma (STFT) con ventana de 25 ms y 50 % de traslape.

## 6. Resultados

Las figuras 01 a 05 usan, para cada comando, la **primera repetición** (`*_h01_r01.wav`). La tabla 6.3 usa las tres repeticiones de cada comando.

### 6.1 Formas de onda y segmentación — `results/01_formas_de_onda.png`
![Formas de onda](results/01_formas_de_onda.png)

La señal original aparece en gris y el segmento recortado en color. El recorte por energía conserva cada palabra completa y elimina el silencio inicial y final. La amplitud pico difiere mucho entre comandos (de unos 0.3 en «arriba» a unos 0.75 en «abajo»); esa diferencia se debe al volumen de cada toma y no a la palabra, por lo que se normaliza antes de comparar formas.

### 6.2 Comparación entre comandos — `results/02_comparacion_comandos.png`
![Comparación](results/02_comparacion_comandos.png)

Con los segmentos normalizados, la duración de estas cuatro grabaciones es: «arriba» 0.64 s, «derecha» 0.60 s, «izquierda» 0.50 s y «abajo» 0.48 s. «Arriba» termina con una cola larga y de baja amplitud. Como en las tres repeticiones los promedios están entre 0.47 y 0.57 s, **la duración por sí sola no basta** para distinguir los comandos.

### 6.3 Caracterización — `results/tabla_caracteristicas.csv` y `results/resumen_por_comando.csv`

Promedio de las 3 repeticiones de cada comando (hablante h01):

| Comando | Duración (s) | Pico | RMS | Centroide espectral (Hz) |
|---|---|---|---|---|
| abajo | 0.560 | 0.592 | 0.106 | 1132 |
| arriba | 0.567 | 0.459 | 0.088 | 1162 |
| derecha | 0.507 | 0.461 | 0.082 | 1536 |
| izquierda | 0.467 | 0.567 | 0.096 | 1520 |

Las desviaciones estándar por comando están en `resumen_por_comando.csv`. Con solo 3 repeticiones de un único hablante son estimaciones poco robustas. El **centroide espectral** separa los comandos en dos grupos: «arriba» y «abajo» (~1.1 kHz) frente a «derecha» e «izquierda» (~1.5 kHz). Duración, pico y RMS no los separan con claridad.

### 6.4 Efecto del ruido — `results/03_efecto_del_ruido.png`
![Ruido](results/03_efecto_del_ruido.png)

Ruido blanco gaussiano con semilla 42 sobre «arriba». Con SNR = 20 dB (medida 19.9 dB) la forma de onda es prácticamente igual a la original. Con SNR = 5 dB (medida 4.9 dB) el ruido forma una banda continua que oculta las partes de menor amplitud, en especial el inicio y la cola final de la palabra. Esto dificultaría detectar los extremos del comando y reduciría la información útil para reconocerlo.

### 6.5 Espectro (FFT) — `results/04_espectro_fft.png`
![FFT](results/04_espectro_fft.png)

El eje horizontal es la frecuencia en Hz (de 0 a fs/2 = 8 kHz) y el vertical la magnitud |X[k]|/N del espectro de un solo lado, calculado con ventana de Hann. En los cuatro comandos la energía se concentra por debajo de ~1 kHz, con picos regularmente espaciados que corresponden a los armónicos de la voz. «Izquierda» y «derecha» muestran además componentes apreciables entre 1.5 y 2 kHz, coherente con su mayor centroide espectral. Por encima de 4 kHz la energía es muy baja en todos los comandos.

### 6.6 Espectrogramas — `results/05_espectrogramas.png`
![Espectrogramas](results/05_espectrogramas.png)

Ventana de 25 ms con 50 % de traslape. La energía aparece en bandas horizontales, sobre todo por debajo de ~3 kHz, asociadas a las vocales. En «izquierda» y «derecha» se distinguen dos bloques de energía separados por un breve intervalo débil. En «derecha» hay una franja vertical que se extiende hasta ~8 kHz hacia los 0.35 s, compatible con la consonante «ch» (ruido de banda ancha). En «arriba» la energía decae hacia el final de la palabra.

### 6.7 Conclusiones preliminares

- El flujo de carga, segmentación, normalización, ruido, FFT y espectrograma funciona y es reproducible con un solo comando.
- Las características espectrales (centroide, distribución en frecuencia) parecen más útiles que la duración o la amplitud para diferenciar los comandos.
- Con un solo hablante no se pueden sacar conclusiones sobre generalización; ampliar la base es la prioridad de la siguiente entrega.

## 7. Referencias

1. Warden, P. (2018). *Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition*. arXiv:1804.03209. https://arxiv.org/abs/1804.03209
2. Davis, S. B., & Mermelstein, P. (1980). Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 28(4), 357–366.
3. Oppenheim, A. V., & Schafer, R. W. (2010). *Discrete-Time Signal Processing* (3.ª ed.). Pearson.
4. Rabiner, L. R., & Schafer, R. W. (2010). *Theory and Applications of Digital Speech Processing*. Pearson.
5. Documentación de NumPy, SciPy y Matplotlib.

## 8. Autores y trabajo en equipo

Proyecto de Juan José Osorio Isaza y Julián Andrés Hernández Tobón.