"""
analisis.py
Análisis inicial (Entrega 2) de las grabaciones de comandos de voz.

Uso (desde la raíz del repositorio):
    python src/analisis.py --datos data/muestras --salida results

Genera en la carpeta de salida:
    tabla_caracteristicas.csv      una fila por grabación
    resumen_por_comando.csv        promedios y desviaciones por comando
    01_formas_de_onda.png          original vs. recortada, un comando por fila
    02_comparacion_comandos.png    los 4 comandos normalizados, mismo eje
    03_efecto_del_ruido.png        señal limpia vs. SNR 20 dB y 5 dB
    04_espectro_fft.png            espectro de magnitud de cada comando
    05_espectrogramas.png          espectrograma (tiempo-frecuencia) de cada comando
"""
import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")  # sin ventana: solo guarda archivos
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

# Permite ejecutar el script desde la raíz del repo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio_utils as au  # noqa: E402

SNR_NIVELES_DB = [20, 5]   # niveles de ruido de la demostración
SEMILLA_RUIDO = 42          # semilla fija -> resultados reproducibles
COLORES = {"arriba": "#1f77b4", "abajo": "#d62728",
           "izquierda": "#2ca02c", "derecha": "#9467bd"}


# ----------------------------------------------------------------------
# Carga y procesamiento de toda la base
# ----------------------------------------------------------------------
def procesar_base(carpeta):
    """Carga y procesa todas las grabaciones. Devuelve (DataFrame, señales)."""
    registros = au.listar_grabaciones(carpeta)
    if not registros:
        raise SystemExit(f"No se encontraron archivos .wav válidos en '{carpeta}'.\n"
                         "Los nombres deben ser como: arriba_h01_r01.wav")
    filas, senales = [], {}
    for r in registros:
        fs, x = au.cargar_wav(r["ruta"])
        x_rec, (ini, fin) = au.recortar_silencio(x, fs)
        fila = dict(r)
        fila.update({"duracion_total_s": len(x) / fs,
                     "inicio_s": ini / fs,
                     "fin_s": fin / fs})
        fila.update(au.caracteristicas(x_rec, fs))
        fila.pop("ruta")
        filas.append(fila)
        senales[r["archivo"]] = {"fs": fs, "x": x, "x_rec": x_rec, "ini": ini}
    return pd.DataFrame(filas), senales


def representantes(df):
    """Primera grabación disponible de cada comando (para las figuras)."""
    rep = {}
    for c in au.COMANDOS:
        sub = df[df["comando"] == c]
        if len(sub):
            rep[c] = sub.iloc[0]["archivo"]
    return rep


# ----------------------------------------------------------------------
# Figuras
# ----------------------------------------------------------------------
def fig_formas_de_onda(senales, rep, salida):
    fig, ejes = plt.subplots(len(rep), 1, figsize=(10, 2.6 * len(rep)))
    ejes = np.atleast_1d(ejes)
    for ax, (cmd, arch) in zip(ejes, rep.items()):
        s = senales[arch]
        t = np.arange(len(s["x"])) / s["fs"]
        ax.plot(t, s["x"], color="lightgray", lw=0.8, label="Grabación original")
        t_rec = (s["ini"] + np.arange(len(s["x_rec"]))) / s["fs"]
        ax.plot(t_rec, s["x_rec"], color=COLORES[cmd], lw=0.8, label="Segmento recortado")
        ax.set_title(f"Comando «{cmd}» ({arch})")
        ax.set_xlabel("Tiempo t [s]")
        ax.set_ylabel("Amplitud x(t) [escala completa]")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    plt.close(fig)


def fig_comparacion(senales, rep, salida):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for cmd, arch in rep.items():
        s = senales[arch]
        x = au.normalizar_pico(s["x_rec"])
        t = np.arange(len(x)) / s["fs"]
        ax.plot(t, x, color=COLORES[cmd], lw=0.7, alpha=0.75,
                label=f"{cmd} ({len(x) / s['fs']:.2f} s)")
    ax.set_title("Comparación de los comandos (segmentos recortados y normalizados)")
    ax.set_xlabel("Tiempo desde el inicio del comando t [s]")
    ax.set_ylabel("Amplitud normalizada x(t)/|x|máx")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    plt.close(fig)


def fig_ruido(senales, rep, salida):
    cmd = next(iter(rep))
    s = senales[rep[cmd]]
    x = s["x_rec"]
    t = np.arange(len(x)) / s["fs"]
    versiones = [("Señal original (limpia)", x)]
    for snr in SNR_NIVELES_DB:
        y = au.agregar_ruido(x, snr, semilla=SEMILLA_RUIDO)
        versiones.append((f"Con ruido blanco gaussiano, SNR objetivo = {snr} dB "
                          f"(medida = {au.snr_medida(x, y):.1f} dB)", y))
    fig, ejes = plt.subplots(len(versiones), 1, figsize=(10, 2.5 * len(versiones)),
                             sharex=True, sharey=True)
    for ax, (titulo, y) in zip(ejes, versiones):
        ax.plot(t, y, color=COLORES[cmd], lw=0.7)
        ax.set_title(f"«{cmd}» — {titulo}", fontsize=10)
        ax.set_ylabel("Amplitud [escala completa]")
        ax.grid(alpha=0.3)
    ejes[-1].set_xlabel("Tiempo t [s]")
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    plt.close(fig)


def fig_espectro(senales, rep, salida):
    fig, ejes = plt.subplots(len(rep), 1, figsize=(10, 2.5 * len(rep)), sharex=True)
    ejes = np.atleast_1d(ejes)
    for ax, (cmd, arch) in zip(ejes, rep.items()):
        s = senales[arch]
        f, mag = au.espectro_fft(s["x_rec"], s["fs"])
        ax.plot(f, mag, color=COLORES[cmd], lw=0.8)
        ax.set_xlim(0, min(8000, s["fs"] / 2))
        ax.set_title(f"Espectro de magnitud (FFT con ventana de Hann) — «{cmd}»", fontsize=10)
        ax.set_ylabel("|X[k]|/N")
        ax.grid(alpha=0.3)
    ejes[-1].set_xlabel("Frecuencia f [Hz]  (de 0 a fs/2)")
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    plt.close(fig)


def fig_espectrogramas(senales, rep, salida):
    n = len(rep)
    cols = 2 if n > 1 else 1
    filas = int(np.ceil(n / cols))
    fig, ejes = plt.subplots(filas, cols, figsize=(6 * cols, 3.2 * filas), squeeze=False)
    ejes = ejes.ravel()
    for ax, (cmd, arch) in zip(ejes, rep.items()):
        s = senales[arch]
        fs, x = s["fs"], s["x_rec"]
        nper = int(0.025 * fs)              # ventana de 25 ms (la voz es ~estacionaria)
        f, t, Sxx = signal.spectrogram(x, fs, window="hann", nperseg=nper,
                                       noverlap=nper // 2, mode="magnitude")
        img = ax.pcolormesh(t, f, 20 * np.log10(Sxx + 1e-10), shading="auto", cmap="magma")
        ax.set_ylim(0, min(8000, fs / 2))
        ax.set_title(f"Espectrograma — «{cmd}»", fontsize=10)
        ax.set_xlabel("Tiempo t [s]")
        ax.set_ylabel("Frecuencia f [Hz]")
        fig.colorbar(img, ax=ax, label="Magnitud [dB]")
    for ax in ejes[n:]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Análisis inicial de comandos de voz")
    ap.add_argument("--datos", default="data/muestras", help="carpeta con los .wav")
    ap.add_argument("--salida", default="results", help="carpeta para gráficas y tablas")
    args = ap.parse_args()

    os.makedirs(args.salida, exist_ok=True)
    df, senales = procesar_base(args.datos)
    rep = representantes(df)

    # Tabla con una fila por grabación
    df.to_csv(os.path.join(args.salida, "tabla_caracteristicas.csv"),
              index=False, float_format="%.5f")

    # Resumen por comando (promedio y desviación estándar)
    resumen = (df.groupby("comando")[["duracion_s", "pico_abs", "rms", "energia",
                                      "f_dominante_Hz", "centroide_Hz", "cruces_por_cero"]]
                 .agg(["mean", "std"]).round(4))
    resumen.to_csv(os.path.join(args.salida, "resumen_por_comando.csv"))

    # Gráficas
    fig_formas_de_onda(senales, rep, os.path.join(args.salida, "01_formas_de_onda.png"))
    fig_comparacion(senales, rep, os.path.join(args.salida, "02_comparacion_comandos.png"))
    fig_ruido(senales, rep, os.path.join(args.salida, "03_efecto_del_ruido.png"))
    fig_espectro(senales, rep, os.path.join(args.salida, "04_espectro_fft.png"))
    fig_espectrogramas(senales, rep, os.path.join(args.salida, "05_espectrogramas.png"))

    print(f"Grabaciones procesadas: {len(df)}  |  fs = {[int(v) for v in sorted(df['fs_Hz'].unique())]} Hz")
    print(f"Hablantes: {df['hablante'].nunique()}  |  Comandos: {sorted(df['comando'].unique())}")
    print("\nResumen por comando (media):")
    print(df.groupby("comando")[["duracion_s", "pico_abs", "rms", "centroide_Hz"]].mean().round(3))
    print(f"\nResultados guardados en '{args.salida}/'")


if __name__ == "__main__":
    main()