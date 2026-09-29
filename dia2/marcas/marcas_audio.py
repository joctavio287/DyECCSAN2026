"""
Demo de audio: cuándo suena de verdad un sonido que se pidió.

Toca una tanda de bips y manda una marca con cada uno. Con la marca en
el canal 1 del osciloscopio y la salida de auriculares en el canal 2,
se ve cuánto tarda el sonido en salir después de pedirlo. La constante
`AUDIO_TIMING` decide cómo se pide:

- ``"inmediato"`` — `play()` y enseguida la marca. El sonido sale
  cuando la placa de audio termina de procesar lo que tiene en el
  buffer: la marca llega primero y el audio después, con un retraso que
  depende de la computadora y no siempre es igual.
- ``"agendado"`` — se le pide a la placa que empiece en un instante
  futuro (`play(when=t)`) y la marca sale en ese mismo instante. El
  audio y la marca quedan alineados.
- ``"con_la_pantalla"`` — lo que hace el componente Sound del Builder:
  el sonido se agenda para el próximo `flip` y la marca sale después del
  `flip`. Con un sensor de luz en el parche se ve que audio, imagen y
  marca coinciden.

Usa el backend de audio de Psychtoolbox (PTB), que es el que permite
agendar. Con ``BACKEND = "simulado"`` corre sin ningún cable.
Es MUY IMPORTANTE SELECCIONAR EL DISPOSITIVO CORRECTO POR DONDE SALDRA 
EL AUDIO: DISTINTOS DRIVERS DISTINTAS LATENCIAS.
En Windows, Realtek >> MME
    python marcas_audio.py
"""

from __future__ import annotations

import random
from pathlib import Path

from psychopy import prefs

prefs.hardware["audioLib"] = ["ptb"]

from time import sleep

from psychopy import core, logging, sound, visual

from marcas_ttl import save_rows, show_instructions
from puerto_marcas import TriggerPort

BACKEND = "simulado"
AUDIO_TIMING = "agendado"


SERIAL_PORT = "COM3"
SERIAL_BAUDRATE = 115200
SERIAL_SIGNAL = "break"
PARALLEL_ADDRESS = 0x0378
PULSE_DURATION = 0.005
TRIGGER_CODE = 2

N_BEEPS = 50
BEEP_FREQUENCY = 1000
BEEP_DURATION = 0.2
SCHEDULE_AHEAD = 0.1
GAP_SECONDS_RANGE = (0.8, 1.2)

FULLSCREEN = True
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOUR = "black"
PATCH_SIZE = 0.25
PATCH_POSITION = (-0.82, -0.42)

OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_NAME = "marcas_audio"

VALID_AUDIO_TIMINGS = ("inmediato", "agendado", "con_la_pantalla")


def run_beep(
    win: visual.Window,
    beep: sound.Sound,
    patch: visual.Rect,
    trigger_port: TriggerPort,
    audio_timing: str,
) -> dict:
    """
    Espera un tiempo al azar, toca un bip y manda la marca.

    Parameters
    ----------
    win : visual.Window
        Ventana, usada para agendar el sonido en el modo
        `"con_la_pantalla"`.
    beep : sound.Sound
        El bip, creado una sola vez.
    patch : visual.Rect
        Parche que acompaña al bip en el modo `"con_la_pantalla"`.
    trigger_port : TriggerPort
        Puerto por el que sale la marca.
    audio_timing : str
        `"inmediato"`, `"agendado"` o `"con_la_pantalla"`.

    Returns
    -------
    dict
        `requested_onset`, el instante en que se pidió que empezara el
        sonido, y `trigger_time`, el instante en que salió la marca,
        ambos en el reloj de la computadora. Cuándo sonó de verdad solo
        lo sabe el osciloscopio.
    """
    core.wait(random.uniform(*GAP_SECONDS_RANGE))

    if audio_timing == "inmediato":
        requested_onset = core.getTime()
        beep.play()
        trigger_time = trigger_port.send(TRIGGER_CODE)
    elif audio_timing == "agendado":
        requested_onset = core.getTime() + SCHEDULE_AHEAD
        beep.play(when=requested_onset)
        while core.getTime() < requested_onset:
            pass
        trigger_time = trigger_port.send(TRIGGER_CODE)
    else:
        patch.draw()
        beep.play(when=win)
        requested_onset = win.flip()
        trigger_time = trigger_port.send(TRIGGER_CODE)

    core.wait(BEEP_DURATION)
    if audio_timing == "con_la_pantalla":
        win.flip()
    trigger_port.release()
    beep.stop()

    return {
        "requested_onset": requested_onset,
        "trigger_time": trigger_time,
        "trigger_minus_request_ms": 1000 * (trigger_time - requested_onset),
    }


def main(
    backend: str,
    serial_signal: str,
    audio_timing: str,
    n_beeps: int,
    output_dir: Path,
    fullscreen: bool,
) -> None:
    """
    Corre la tanda de bips y guarda el registro.

    Parameters
    ----------
    backend : str
        `"serial"`, `"parallel"` o `"simulado"`.
    serial_signal : str
        `"byte"`, `"break"`, `"dtr"` o `"rts"` (ver `puerto_marcas`).
    audio_timing : str
        `"inmediato"`, `"agendado"` o `"con_la_pantalla"`.
    n_beeps : int
        Cuántos bips tocar.
    output_dir : Path
        Carpeta donde se escriben el CSV y el log.
    fullscreen : bool
        Pantalla completa. Hace falta para `"con_la_pantalla"`.

    Raises
    ------
    ValueError
        Si `audio_timing` no es un valor admitido.
    """
    if audio_timing not in VALID_AUDIO_TIMINGS:
        raise ValueError(
            f"audio_timing '{audio_timing}' desconocido, usar uno de "
            f"{VALID_AUDIO_TIMINGS}"
        )
    run_name = f"{OUTPUT_NAME}_{audio_timing}"

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
    beep = sound.Sound(
        value=BEEP_FREQUENCY, secs=BEEP_DURATION, hamming=False,
    )
    patch = visual.Rect(
        win, width=PATCH_SIZE, height=PATCH_SIZE,
        pos=PATCH_POSITION, fillColor="white", lineColor=None,
    )
    show_instructions(
        win,
        trigger_port,
        f"Demo de audio — {audio_timing}\n\n"
        f"{n_beeps} bips de {BEEP_FREQUENCY} Hz.\n"
        "Salida de auriculares al canal 2 del osciloscopio.\n\n"
        "Espacio para empezar · Escape para salir",
    )

    beeps = [
        run_beep(win, beep, patch, trigger_port, audio_timing)
        for _ in range(n_beeps)
    ]

    trigger_port.close()
    win.close()

    print(
        f"\n{len(beeps)} bips en modo '{audio_timing}'. La computadora "
        "solo sabe cuándo pidió\nel sonido y cuándo mandó la marca: "
        "cuándo sonó, lo dice el osciloscopio."
    )
    save_rows(beeps, output_dir / f"{run_name}.csv")
    core.quit()


if __name__ == "__main__":
    main(
        backend=BACKEND,
        serial_signal=SERIAL_SIGNAL,
        audio_timing=AUDIO_TIMING,
        n_beeps=N_BEEPS,
        output_dir=OUTPUT_DIR,
        fullscreen=FULLSCREEN,
    )
