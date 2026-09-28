"""
Demo visual de marcas TTL: dónde va el trigger y cuánto cuesta
equivocarse.

Es el software del demo en vivo del día 2. Muestra un parche blanco en
una esquina de la pantalla —el que mira el sensor de luz— y manda una
marca en cada aparición. La constante `TRIGGER_TIMING` decide si la
marca sale **antes** o **después** del `flip`:

- ``"antes_del_flip"`` — el error clásico. La marca sale cuando el
  código la pide, que es hasta un frame entero antes de que el estímulo
  exista en la pantalla.
- ``"despues_del_flip"`` — lo correcto. `flip()` bloquea hasta el
  refresco del monitor, así que la marca sale cuando el estímulo
  aparece de verdad.

La constante `GAP_MODE` decide cómo se espera entre destellos:

- ``"segundos"`` — una espera al azar medida en segundos, como en un
  experimento que avanza con un temporizador o con una tecla. El código
  llega a pedir el estímulo en cualquier punto del ciclo del monitor,
  así que la marca de ``"antes_del_flip"`` se adelanta entre 0 y un
  frame entero, **distinto en cada destello**.
- ``"frames"`` — una espera contada en frames. El código queda atado al
  refresco y el adelanto de ``"antes_del_flip"`` es casi siempre un
  frame: un error grande pero constante.

Con ``SERIAL_SIGNAL = "break"`` la línea TX del pincho queda en bajo
mientras el parche está en pantalla, así que un LED conectado a esa
línea se prende junto con el estímulo.

Funciona sin ningún hardware: con ``BACKEND = "simulado"`` escribe las
marcas al log y a un CSV, y el demo se puede ensayar en cualquier
máquina.

    python marcas_ttl.py
"""

from __future__ import annotations

import csv
import random
import statistics
from pathlib import Path

from psychopy import core, event, logging, visual

from puerto_marcas import TriggerPort

BACKEND = "serial"
TRIGGER_TIMING = "antes_del_flip"
GAP_MODE = "segundos"

N_FLASHES = 100
FLASH_FRAMES = 12
GAP_FRAMES = 30
GAP_SECONDS_RANGE = (0.4, 0.8)
PULSE_DURATION = 0.05
TRIGGER_CODE = 255

SERIAL_PORT = "COM3"
SERIAL_BAUDRATE = 115200
SERIAL_SIGNAL = "break"
PARALLEL_ADDRESS = 0x0378

FULLSCREEN = True
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOUR = "black"
PATCH_SIZE = 0.25
PATCH_POSITION = (-0.82, -0.42)

OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_NAME = "marcas_ttl"

VALID_TIMINGS = ("antes_del_flip", "despues_del_flip")
VALID_GAP_MODES = ("segundos", "frames")


def run_flash(
    win: visual.Window,
    patch: visual.Rect,
    trigger_port: TriggerPort,
    trigger_timing: str,
    gap_mode: str,
    flash_frames: int,
    gap_frames: int,
) -> dict:
    """
    Espera, muestra un destello del parche y manda la marca asociada.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibuja.
    patch : visual.Rect
        Parche blanco que mira el sensor de luz.
    trigger_port : TriggerPort
        Puerto por el que sale la marca.
    trigger_timing : str
        `"antes_del_flip"` o `"despues_del_flip"`.
    gap_mode : str
        `"segundos"` para esperar un tiempo al azar antes del destello,
        `"frames"` para esperar `gap_frames` refrescos.
    flash_frames : int
        Cuántos frames dura el destello.
    gap_frames : int
        Cuántos frames de pantalla vacía preceden al destello, si
        `gap_mode` es `"frames"`.

    Returns
    -------
    dict
        `trigger_time`, `flip_time` y `offset_ms`, la diferencia entre
        los dos en milisegundos. Un `offset_ms` negativo significa que
        la marca salió **antes** que el estímulo.
    """
    if gap_mode == "segundos":
        core.wait(random.uniform(*GAP_SECONDS_RANGE))
    else:
        for _ in range(gap_frames):
            win.flip()

    patch.draw()
    if trigger_timing == "antes_del_flip":
        trigger_time = trigger_port.send(TRIGGER_CODE)
        flip_time = win.flip()
    else:
        flip_time = win.flip()
        trigger_time = trigger_port.send(TRIGGER_CODE)

    for _ in range(flash_frames - 1):
        patch.draw()
        win.flip()
    win.flip()
    trigger_port.release()

    return {
        "trigger_time": trigger_time,
        "flip_time": flip_time,
        "offset_ms": 1000 * (trigger_time - flip_time),
    }


def summarise(flashes: list[dict], frame_rate: float) -> None:
    """
    Imprime el desfasaje medido entre la marca y el estímulo.

    Parameters
    ----------
    flashes : list[dict]
        Resultados devueltos por `run_flash`.
    frame_rate : float
        Frecuencia de refresco medida, para poner el número en
        contexto.
    """
    offsets = [flash["offset_ms"] for flash in flashes]
    frame_ms = 1000 / frame_rate

    print(
        f"\n{len(flashes)} destellos a {frame_rate:.2f} Hz "
        f"({frame_ms:.2f} ms por frame)"
    )
    print(
        f"Desfasaje marca − flip: {statistics.mean(offsets):+.2f} ms "
        f"(DE {statistics.stdev(offsets):.2f} ms, "
        f"rango {max(offsets) - min(offsets):.2f} ms)"
    )
    print(
        "\nEste número es el que mide el reloj de la computadora, o sea "
        "lo que\nella *cree*. El osciloscopio con el sensor de luz mide "
        "lo que pasó de verdad,\ny por eso el demo necesita las dos cosas."
    )


def save_rows(rows: list[dict], output_path: Path) -> None:
    """
    Guarda un CSV con una fila por evento.

    Parameters
    ----------
    rows : list[dict]
        Filas a guardar, todas con las mismas claves.
    output_path : Path
        Archivo a escribir.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV escrito en {output_path}")


def show_instructions(
    win: visual.Window,
    trigger_port: TriggerPort,
    text: str,
) -> None:
    """
    Muestra un texto hasta que se apriete espacio, o sale con escape.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibuja.
    trigger_port : TriggerPort
        Puerto a cerrar si se sale con escape.
    text : str
        Texto a mostrar.
    """
    instructions = visual.TextStim(
        win, text=text, height=0.045, color="white", alignText="center",
    )
    instructions.draw()
    win.flip()
    if "escape" in event.waitKeys(keyList=["space", "escape"]):
        trigger_port.close()
        win.close()
        core.quit()
    win.flip()


def main(
    backend: str,
    serial_signal: str,
    trigger_timing: str,
    gap_mode: str,
    n_flashes: int,
    output_dir: Path,
    fullscreen: bool,
) -> None:
    """
    Corre la tanda de destellos y guarda el registro.

    Parameters
    ----------
    backend : str
        `"serial"`, `"parallel"` o `"simulado"`.
    serial_signal : str
        `"byte"`, `"break"`, `"dtr"` o `"rts"` (ver `puerto_marcas`).
    trigger_timing : str
        `"antes_del_flip"` o `"despues_del_flip"`.
    gap_mode : str
        `"segundos"` o `"frames"`.
    n_flashes : int
        Cuántos destellos correr.
    output_dir : Path
        Carpeta donde se escriben el CSV y el log.
    fullscreen : bool
        Pantalla completa. En modo ventana el compositor del sistema
        agrega retrasos y el demo pierde sentido.

    Raises
    ------
    ValueError
        Si `trigger_timing` o `gap_mode` no son valores admitidos.
    """
    if trigger_timing not in VALID_TIMINGS:
        raise ValueError(
            f"trigger_timing '{trigger_timing}' desconocido, usar uno "
            f"de {VALID_TIMINGS}"
        )
    if gap_mode not in VALID_GAP_MODES:
        raise ValueError(
            f"gap_mode '{gap_mode}' desconocido, usar uno de "
            f"{VALID_GAP_MODES}"
        )
    run_name = f"{OUTPUT_NAME}_{trigger_timing}_{gap_mode}"

    address = SERIAL_PORT if backend == "serial" else PARALLEL_ADDRESS
    trigger_port = TriggerPort(
        backend, address, SERIAL_BAUDRATE, serial_signal, PULSE_DURATION
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    logging.LogFile(str(output_dir / f"{run_name}.log"), level=logging.DATA)

    win = visual.Window(
        size=WINDOW_SIZE,
        fullscr=fullscreen,
        color=BACKGROUND_COLOUR,
        units="height",
        allowGUI=not fullscreen,
    )
    frame_rate = win.getActualFrameRate() or 60.0

    patch = visual.Rect(
        win, width=PATCH_SIZE, height=PATCH_SIZE,
        pos=PATCH_POSITION, fillColor="white", lineColor=None,
    )
    show_instructions(
        win,
        trigger_port,
        f"Demo de marcas TTL — {trigger_timing}, {gap_mode}\n\n"
        f"{n_flashes} destellos en la esquina inferior izquierda.\n"
        "Poné ahí el sensor de luz.\n\n"
        "Espacio para empezar · Escape para salir",
    )

    flashes = [
        run_flash(
            win, patch, trigger_port, trigger_timing, gap_mode,
            FLASH_FRAMES, GAP_FRAMES,
        )
        for _ in range(n_flashes)
    ]

    trigger_port.close()
    win.close()

    summarise(flashes, frame_rate)
    save_rows(flashes, output_dir / f"{run_name}.csv")
    core.quit()


if __name__ == "__main__":
    main(
        backend=BACKEND,
        serial_signal=SERIAL_SIGNAL,
        trigger_timing=TRIGGER_TIMING,
        gap_mode=GAP_MODE,
        n_flashes=N_FLASHES,
        output_dir=OUTPUT_DIR,
        fullscreen=FULLSCREEN,
    )
