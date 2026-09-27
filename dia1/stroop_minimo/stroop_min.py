"""
Tarea Stroop mínima: el experimento rompehielo del día 1.

Está escrito a propósito con los mismos objetos que el Builder genera
por detrás (`ExperimentHandler`, `TrialHandler`,
`hardware.keyboard.Keyboard`), así el CSV que produce tiene exactamente
la estructura estándar de PsychoPy que se estudia el día 2.

La paleta es segura para daltonismo: azul, naranja y blanco sobre gris
oscuro. La tríada clásica rojo/verde/azul es inservible para un
deuteranope, que ve rojo y verde a distancia ΔE 10 en CIELAB; esta
tríada se mantiene por encima de ΔE 55 en las tres dicromacias.

Se corre desde la ventana Coder de PsychoPy (botón Ejecutar) o desde
una terminal cuyo entorno de Python tenga PsychoPy instalado::

    python stroop_min.py
"""

from __future__ import annotations

import os
from pathlib import Path

from psychopy import __version__ as PSYCHOPY_VERSION
from psychopy import core, data, event, gui, visual
from psychopy.hardware import keyboard

EXPERIMENT_NAME = "stroop_min"
CONDITIONS_FILE = Path(__file__).parent / "condiciones_stroop.csv"
DATA_DIR = Path(__file__).resolve().parent / "data"

N_REPEATS = 4
FULLSCREEN = True
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOUR = "#4D4D4D"

FIXATION_DURATION = 0.5
FEEDBACK_DURATION = 0.4
MAX_RESPONSE_TIME = 3.0
WORD_HEIGHT = 0.15
MESSAGE_HEIGHT = 0.05

RESPONSE_KEYS = ["a", "n", "b"]
QUIT_KEY = "escape"

INSTRUCTIONS = (
    "TAREA STROOP\n\n"
    "Va a aparecer una palabra escrita en un color.\n"
    "Respondé el COLOR DE LA TINTA, no la palabra.\n\n"
    "    A = azul      N = naranja      B = blanco\n\n"
    "Respondé lo más rápido que puedas sin equivocarte.\n\n"
    "Presioná la barra espaciadora para empezar."
)

GOODBYE = (
    "Listo, gracias.\n\n"
    "Ahora subí a la tarea del Classroom el .csv que quedó\n"
    "en la carpeta data, al lado de este script.\n\n"
    "Presioná la barra espaciadora para salir."
)


def collect_participant_info(experiment_name: str) -> dict:
    """
    Abre el diálogo inicial y devuelve los datos del participante.

    Parameters
    ----------
    experiment_name : str
        Nombre que se guarda en el archivo de datos y que se usa para
        armar su nombre de archivo.

    Returns
    -------
    dict
        Los campos que completó el participante, más `date`,
        `exp_name` y `psychopyVersion`.

    Raises
    ------
    SystemExit
        Si el participante cancela el diálogo.
    """
    exp_info = {"participant": "", "session": "001", "age": "", "hand": "d"}
    dialog = gui.DlgFromDict(
        dictionary=exp_info,
        title=experiment_name,
        order=["participant", "session", "age", "hand"],
    )
    if not dialog.OK:
        core.quit()

    exp_info["date"] = data.getDateStr()
    exp_info["exp_name"] = experiment_name
    exp_info["psychopyVersion"] = PSYCHOPY_VERSION
    return exp_info


def build_output_stem(data_dir: Path, exp_info: dict) -> str:
    """
    Arma el prefijo de ruta que comparten el .csv y el .psydat.

    Parameters
    ----------
    data_dir : Path
        Carpeta donde se escriben los archivos del participante.
    exp_info : dict
        Metadata devuelta por `collect_participant_info`.

    Returns
    -------
    str
        Ruta absoluta sin extensión, siguiendo la convención por
        defecto de PsychoPy ``<participant>_<exp_name>_<date>``.
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    stem = (
        f"{exp_info['participant']}_{exp_info['exp_name']}"
        f"_{exp_info['date']}"
    )
    return os.path.join(str(data_dir), stem)


def show_message(win: visual.Window, text: str) -> None:
    """
    Muestra un mensaje a pantalla completa hasta que se presione espacio.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibuja el mensaje.
    text : str
        Cuerpo del mensaje.
    """
    message = visual.TextStim(
        win, text=text, height=MESSAGE_HEIGHT, color="white",
        wrapWidth=1.6, alignText="center",
    )
    message.draw()
    win.flip()
    pressed = event.waitKeys(keyList=["space", QUIT_KEY])
    if QUIT_KEY in pressed:
        core.quit()


def run_trial(
    win: visual.Window,
    word_stim: visual.TextStim,
    fixation_stim: visual.TextStim,
    response_device: keyboard.Keyboard,
    trial: dict,
) -> dict:
    """
    Corre un trial de Stroop y devuelve todo lo que vale la pena guardar.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibujan los estímulos.
    word_stim : visual.TextStim
        Estímulo reutilizado, al que se le cambian texto y color en
        cada trial.
    fixation_stim : visual.TextStim
        Cruz de fijación que se muestra antes de la palabra.
    response_device : keyboard.Keyboard
        Teclado sobre PTB, usado para medir el tiempo de respuesta.
    trial : dict
        Una fila del archivo de condiciones: `word`, `ink_name`,
        `ink_colour`, `congruent`, `correct_key`.

    Returns
    -------
    dict
        Claves `response_key`, `response_time`, `correct` y
        `stimulus_onset`. `response_key` queda en `None` si se agotó
        el tiempo.
    """
    fixation_stim.draw()
    win.flip()
    core.wait(FIXATION_DURATION)

    word_stim.setText(trial["word"])
    word_stim.setColor(trial["ink_colour"])
    word_stim.draw()

    response_device.clearEvents()
    stimulus_onset = win.flip()
    response_device.clock.reset()

    presses = []
    while not presses:
        presses = response_device.getKeys(
            keyList=RESPONSE_KEYS + [QUIT_KEY], waitRelease=False
        )
        if response_device.clock.getTime() > MAX_RESPONSE_TIME:
            break

    if presses and presses[0].name == QUIT_KEY:
        core.quit()

    response_key = presses[0].name if presses else None
    response_time = presses[0].rt if presses else None
    correct = int(response_key == trial["correct_key"])

    return {
        "response_key": response_key,
        "response_time": response_time,
        "correct": correct,
        "stimulus_onset": stimulus_onset,
    }


def show_feedback(win: visual.Window, outcome: dict) -> None:
    """
    Muestra una pantalla de feedback de una palabra para el trial recién
    terminado.

    Parameters
    ----------
    win : visual.Window
        Ventana sobre la que se dibuja el feedback.
    outcome : dict
        Resultado del trial, tal como lo devuelve `run_trial`.

    Notes
    -----
    El feedback está codificado por partida doble, con símbolo y con
    color, y evita el eje rojo-verde por la misma razón que la paleta
    de los estímulos.
    """
    if outcome["response_key"] is None:
        text, colour = "— muy lento", "#FFFFFF"
    elif outcome["correct"]:
        text, colour = "✓ correcto", "#56B4E9"
    else:
        text, colour = "✗ incorrecto", "#E69F00"

    feedback = visual.TextStim(
        win, text=text, height=MESSAGE_HEIGHT, color=colour
    )
    feedback.draw()
    win.flip()
    core.wait(FEEDBACK_DURATION)


def main(
    conditions_path: Path,
    data_dir: Path,
    experiment_name: str,
    n_repeats: int,
    fullscreen: bool,
) -> None:
    """
    Corre la sesión completa: diálogo, instrucciones, trials y archivos.

    Parameters
    ----------
    conditions_path : Path
        CSV con una fila por condición del Stroop.
    data_dir : Path
        Carpeta donde se escriben los archivos del participante.
    experiment_name : str
        Nombre que se guarda en el archivo de datos y que aparece en su
        nombre de archivo.
    n_repeats : int
        Cantidad de veces que se repite el conjunto de condiciones.
    fullscreen : bool
        Si la ventana se abre a pantalla completa. Dejar en `True`
        para cualquier medición real; `False` es solo para depurar.
    """
    exp_info = collect_participant_info(experiment_name)
    output_stem = build_output_stem(data_dir, exp_info)

    experiment = data.ExperimentHandler(
        name=experiment_name,
        extraInfo=exp_info,
        dataFileName=output_stem,
        savePickle=True,
        saveWideText=True,
    )

    win = visual.Window(
        size=WINDOW_SIZE,
        fullscr=fullscreen,
        color=BACKGROUND_COLOUR,
        units="height",
        allowGUI=not fullscreen,
    )
    frame_rate = win.getActualFrameRate()
    experiment.extraInfo["frame_rate"] = frame_rate

    word_stim = visual.TextStim(win, text="", height=WORD_HEIGHT, bold=True)
    fixation_stim = visual.TextStim(
        win, text="+", height=WORD_HEIGHT, color="white"
    )
    response_device = keyboard.Keyboard()

    show_message(win, INSTRUCTIONS)

    trials = data.TrialHandler(
        trialList=data.importConditions(str(conditions_path)),
        nReps=n_repeats,
        method="random",
        name="trials",
    )
    experiment.addLoop(trials)

    for trial in trials:
        outcome = run_trial(
            win, word_stim, fixation_stim, response_device, trial
        )
        for key, value in outcome.items():
            experiment.addData(key, value)
        experiment.nextEntry()
        show_feedback(win, outcome)

    show_message(win, GOODBYE)

    experiment.saveAsWideText(output_stem + ".csv", delim=",")
    experiment.saveAsPickle(output_stem)
    experiment.abort()
    win.close()
    core.quit()


if __name__ == "__main__":
    main(
        conditions_path=CONDITIONS_FILE,
        data_dir=DATA_DIR,
        experiment_name=EXPERIMENT_NAME,
        n_repeats=N_REPEATS,
        fullscreen=FULLSCREEN,
    )
