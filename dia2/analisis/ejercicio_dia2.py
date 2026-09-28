"""
Esqueleto del ejercicio del día 2. Completar los TODO en orden.

Cada TODO corresponde a una de las cinco partes de la Consigna 6. Los
CSV del Stroop mínimo de toda la clase van en la carpeta `datos_clase`,
al lado de este archivo; las figuras quedan en `figuras`.

Se corre desde el Coder (botón Ejecutar) o, desde esta carpeta::

    python ejercicio_dia2.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from lectura_datos_psychopy import (
    clean_trials,
    load_session_directory,
    stroop_effect_by_participant,
    summarise_by_participant,
)

DATA_DIR = Path(__file__).resolve().parent / "datos_clase"
FIGURE_DIR = Path(__file__).resolve().parent / "figuras"


def inspect_raw_table(trials: pd.DataFrame) -> None:
    """
    Parte 1: mirar el archivo antes de tocarlo.

    Parameters
    ----------
    trials : pd.DataFrame
        Tabla cruda, sin filtrar.
    """
    # TODO 1a: imprimir cuántas filas y columnas tiene la tabla.
    # TODO 1b: imprimir la lista de nombres de columna.
    # TODO 1c: imprimir las primeras 5 filas y las últimas 5 filas.
    #          ¿Hay filas que no sean trials? Compararlo con un CSV de
    #          tu experimento de Builder.
    # TODO 1d: separar las columnas en tres grupos y decir a qué grupo
    #          pertenece cada una: (i) vienen del archivo de
    #          condiciones, (ii) las escribió el experimento en cada
    #          trial, (iii) son metadata de la sesión.
    raise NotImplementedError("Completar la parte 1")


def describe_response_times(trials: pd.DataFrame) -> pd.DataFrame:
    """
    Parte 2: describir los tiempos de respuesta antes de limpiarlos.

    Parameters
    ----------
    trials : pd.DataFrame
        Tabla cruda, sin filtrar.

    Returns
    -------
    pd.DataFrame
        Una fila por participante con cantidad de trials, RT medio, RT
        mediano y proporción de respuestas correctas.
    """
    # TODO 2a: contar cuántos trials tiene cada participante.
    # TODO 2b: calcular RT medio, RT mediano y accuracy por
    #          participante.
    # TODO 2c: ¿la media y la mediana dan lo mismo? ¿Por qué no?
    raise NotImplementedError("Completar la parte 2")


def plot_rt_distribution(trials: pd.DataFrame, figure_dir: Path) -> None:
    """
    Parte 3: graficar la distribución de RT por congruencia.

    Parameters
    ----------
    trials : pd.DataFrame
        Tabla ya limpia.
    figure_dir : Path
        Carpeta donde guardar la figura.
    """
    # TODO 3a: un histograma de response_time para congruent == 1 y
    #          otro para congruent == 0, en los mismos ejes.
    # TODO 3b: marcar con una línea vertical la mediana de cada grupo.
    # TODO 3c: guardar la figura en figure_dir.
    raise NotImplementedError("Completar la parte 3")


def test_stroop_effect(effects: pd.DataFrame) -> None:
    """
    Parte 4: ¿hay efecto Stroop en el grupo?

    Parameters
    ----------
    effects : pd.DataFrame
        Salida de `stroop_effect_by_participant`.
    """
    # TODO 4a: imprimir el efecto Stroop medio del grupo, en ms.
    # TODO 4b: contar en cuántos participantes el efecto es positivo.
    # TODO 4c: correr un t-test pareado (scipy.stats.ttest_rel) entre
    #          rt_incongruent y rt_congruent, e imprimir t y p.
    # TODO 4d: escribir en un comentario la conclusión en una frase,
    #          incluyendo el n.
    raise NotImplementedError("Completar la parte 4")


def main(data_dir: Path, figure_dir: Path) -> None:
    """
    Corre las cinco partes del ejercicio en orden.

    Parameters
    ----------
    data_dir : Path
        Carpeta con un CSV por participante.
    figure_dir : Path
        Carpeta donde guardar las figuras.
    """
    figure_dir.mkdir(parents=True, exist_ok=True)

    raw_trials = load_session_directory(data_dir)
    inspect_raw_table(raw_trials)
    describe_response_times(raw_trials)

    trials = clean_trials(raw_trials)
    plot_rt_distribution(trials, figure_dir)

    summary = summarise_by_participant(trials)
    effects = stroop_effect_by_participant(summary)
    test_stroop_effect(effects)

    # TODO 5: guardar `effects` como CSV al lado de este archivo
    #         (figure_dir.parent) y explicar en un comentario por
    #         qué conviene guardar la tabla resumida además de los
    #         datos crudos.
    plt.close("all")


if __name__ == "__main__":
    main(data_dir=DATA_DIR, figure_dir=FIGURE_DIR)
