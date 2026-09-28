"""
Funciones para cargar y limpiar los CSV anchos que escribe PsychoPy.

El día 2 usa estos tres pasos en orden: cargar un archivo para mirarle
las columnas, cargar una carpeta entera en una sola tabla, y recién
después descartar las filas que no son trials reales.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

TRIAL_MARKER_COLUMN = "response_time"
RT_LOWER_BOUND = 0.2
RT_UPPER_BOUND = 2.0


def load_trial_file(csv_path: str | Path) -> pd.DataFrame:
    """
    Lee un único CSV ancho de PsychoPy y lo devuelve como DataFrame.

    Parameters
    ----------
    csv_path : str o Path
        Ruta a un archivo `*_<exp_name>_<fecha>.csv`.

    Returns
    -------
    pd.DataFrame
        El archivo tal cual está, más una columna `source_file` con el
        nombre del archivo. A propósito no se descarta ninguna fila: la
        forma cruda, con filas vacías incluidas, es justamente lo que
        la clase tiene que mirar primero.
    """
    csv_path = Path(csv_path)
    trials = pd.read_csv(csv_path)
    trials["source_file"] = csv_path.name
    return trials


def load_session_directory(
    data_dir: str | Path, pattern: str = "*.csv"
) -> pd.DataFrame:
    """
    Concatena todos los archivos de participante de una carpeta.

    Parameters
    ----------
    data_dir : str o Path
        Carpeta con un CSV por participante.
    pattern : str, opcional
        Patrón usado para elegir los archivos, por defecto `"*.csv"`.

    Returns
    -------
    pd.DataFrame
        Todos los archivos apilados, con el índice reiniciado.

    Raises
    ------
    FileNotFoundError
        Si la carpeta no tiene ningún archivo que coincida con
        `pattern`.
    """
    data_dir = Path(data_dir)
    csv_paths = sorted(data_dir.glob(pattern))
    if not csv_paths:
        raise FileNotFoundError(
            f"No hay archivos {pattern} en {data_dir}"
        )
    return pd.concat(
        [load_trial_file(path) for path in csv_paths],
        ignore_index=True,
    )


def clean_trials(
    trials: pd.DataFrame,
    rt_lower_bound: float = RT_LOWER_BOUND,
    rt_upper_bound: float = RT_UPPER_BOUND,
) -> pd.DataFrame:
    """
    Deja solo los trials correctos y con un tiempo de respuesta creíble.

    Se aplican tres filtros, en este orden: las filas que no son trials
    (PsychoPy escribe una fila final que solo tiene metadata de la
    sesión), las respuestas incorrectas o ausentes, y los tiempos de
    respuesta fuera de la ventana plausible.

    Parameters
    ----------
    trials : pd.DataFrame
        Tabla devuelta por `load_trial_file` o
        `load_session_directory`.
    rt_lower_bound : float, opcional
        Las respuestas más rápidas que esto son anticipaciones, por
        defecto 0.2 s.
    rt_upper_bound : float, opcional
        Las respuestas más lentas que esto son despistes, por defecto
        2.0 s.

    Returns
    -------
    pd.DataFrame
        Copia filtrada, con el índice reiniciado.
    """
    is_trial = trials[TRIAL_MARKER_COLUMN].notna()
    is_correct = trials["correct"] == 1
    in_window = trials["response_time"].between(
        rt_lower_bound, rt_upper_bound
    )
    return trials[is_trial & is_correct & in_window].reset_index(drop=True)


def summarise_by_participant(trials: pd.DataFrame) -> pd.DataFrame:
    """
    Colapsa los trials a una fila por participante y congruencia.

    Parameters
    ----------
    trials : pd.DataFrame
        Tabla de trials ya limpia.

    Returns
    -------
    pd.DataFrame
        Columnas `participant`, `congruent`, `mean_rt`, `median_rt` y
        `n_trials`.
    """
    summary = (
        trials
        .groupby(["participant", "congruent"], as_index=False)
        .agg(
            mean_rt=("response_time", "mean"),
            median_rt=("response_time", "median"),
            n_trials=("response_time", "size"),
        )
    )
    return summary


def stroop_effect_by_participant(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el resumen por congruencia en un efecto Stroop por persona.

    Parameters
    ----------
    summary : pd.DataFrame
        Salida de `summarise_by_participant`.

    Returns
    -------
    pd.DataFrame
        Columnas `participant`, `rt_congruent`, `rt_incongruent` y
        `stroop_effect` (incongruente menos congruente, en segundos).
    """
    wide = summary.pivot(
        index="participant", columns="congruent", values="mean_rt"
    )
    wide = wide.rename(columns={0: "rt_incongruent", 1: "rt_congruent"})
    wide["stroop_effect"] = wide["rt_incongruent"] - wide["rt_congruent"]
    return wide.reset_index()
