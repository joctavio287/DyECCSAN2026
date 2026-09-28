"""
Mide cómo refresca la pantalla de esta computadora, frame por frame.

Es la actividad del bloque de timing del día 2. Abre una ventana, mide
la frecuencia de refresco real, dibuja una barra que gira durante
`N_FRAMES` frames y registra cuánto duró cada uno. Al final muestra:

- la frecuencia medida y cuánto dura un frame;
- la duración media de los frames y cuánto varía;
- cuántos frames se perdieron: los que duraron más de un frame y
  medio, o sea que la pantalla se quedó un refresco sin dibujo nuevo.

Se corre dos veces, con `FULLSCREEN = True` y con `False`, y se
comparan los números. Desde el Coder (botón Run) o desde una terminal::

    python medir_maquina.py
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

from psychopy import core, event, visual

N_FRAMES = 600
FULLSCREEN = True
WINDOW_SIZE = (1280, 720)
DROPPED_THRESHOLD = 1.5

OUTPUT_DIR = Path(__file__).resolve().parent / "data"


def measure_frame_intervals(
    win: visual.Window,
    stimulus: visual.Rect,
    n_frames: int,
) -> list[float]:
    """
    Dibuja un estímulo que gira durante `n_frames` y mide cada frame.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibuja.
    stimulus : visual.Rect
        Estímulo que gira un poco en cada frame, para que haya algo
        nuevo que dibujar.
    n_frames : int
        Cuántos frames medir.

    Returns
    -------
    list[float]
        Duración de cada frame, en milisegundos.
    """
    win.recordFrameIntervals = True
    for frame in range(n_frames):
        stimulus.ori = (3 * frame) % 360
        stimulus.draw()
        win.flip()
    win.recordFrameIntervals = False
    return [1000 * interval for interval in win.frameIntervals]


def summarise(intervals_ms: list[float], frame_rate: float) -> str:
    """
    Arma el resumen que se muestra en pantalla y en la consola.

    Parameters
    ----------
    intervals_ms : list[float]
        Duración de cada frame, en milisegundos.
    frame_rate : float
        Frecuencia de refresco medida al abrir la ventana, en Hz.

    Returns
    -------
    str
        Texto de varias líneas con los números de la medición.
    """
    frame_ms = 1000 / frame_rate
    dropped = sum(
        interval > DROPPED_THRESHOLD * frame_ms for interval in intervals_ms
    )
    return (
        f"Frecuencia de refresco: {frame_rate:.2f} Hz "
        f"({frame_ms:.2f} ms por frame)\n\n"
        f"Duración de los frames: media {statistics.mean(intervals_ms):.2f}"
        f" ms, DE {statistics.stdev(intervals_ms):.2f} ms\n"
        f"El más corto: {min(intervals_ms):.2f} ms · "
        f"el más largo: {max(intervals_ms):.2f} ms\n\n"
        f"Frames perdidos: {dropped} de {len(intervals_ms)}"
    )


def save_intervals(intervals_ms: list[float], output_path: Path) -> None:
    """
    Guarda la duración de cada frame en un CSV.

    Parameters
    ----------
    intervals_ms : list[float]
        Duración de cada frame, en milisegundos.
    output_path : Path
        Archivo a escribir.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["frame", "interval_ms"])
        writer.writerows(enumerate(intervals_ms, start=1))


def main(
    n_frames: int,
    fullscreen: bool,
    output_dir: Path,
) -> None:
    """
    Mide los frames, muestra el resumen y guarda el detalle.

    Parameters
    ----------
    n_frames : int
        Cuántos frames medir.
    fullscreen : bool
        Si la ventana ocupa toda la pantalla.
    output_dir : Path
        Carpeta donde se guarda el CSV.
    """
    win = visual.Window(
        size=WINDOW_SIZE,
        fullscr=fullscreen,
        color="black",
        units="height",
        allowGUI=not fullscreen,
    )
    frame_rate = win.getActualFrameRate() or 60.0
    bar = visual.Rect(
        win, width=0.5, height=0.04, fillColor="white", lineColor=None
    )

    intervals_ms = measure_frame_intervals(win, bar, n_frames)
    summary = summarise(intervals_ms, frame_rate)
    mode = "pantalla_completa" if fullscreen else "ventana"
    save_intervals(intervals_ms, output_dir / f"frames_{mode}.csv")

    print(f"\n{summary}\n")
    visual.TextStim(
        win,
        text=f"{summary}\n\nApretá cualquier tecla para salir.",
        height=0.035,
        wrapWidth=1.5,
        color="white",
    ).draw()
    win.flip()
    event.waitKeys()
    win.close()
    core.quit()


if __name__ == "__main__":
    main(n_frames=N_FRAMES, fullscreen=FULLSCREEN, output_dir=OUTPUT_DIR)
