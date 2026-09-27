# Stroop mínimo

El experimento que se corre apenas empieza el día 1, antes de cualquier
explicación (Consigna 0).

## Cómo correrlo

1. Abrir PsychoPy → ventana **Coder** → **File → Open** →
   `stroop_min.py`
2. Apretar **Ejecutar** (la flecha verde)
3. Completar `participant` con el código asignado (`sub-01`, `sub-02`…).
   **No poner el nombre propio.**
4. Responder **el color del texto**, no la palabra:
   **A** = azul · **N** = naranja · **B** = blanco
5. `Escape` sale en cualquier momento

También corre desde una terminal, si el entorno tiene PsychoPy:

```bash
python stroop_min.py
```

## Qué produce

Dos archivos en la carpeta `data/`, al lado del script, con el mismo
nombre y distinta extensión:

```
sub-07_stroop_min_2026-09-30_09h45.12.345.csv      ← el que se analiza
sub-07_stroop_min_2026-09-30_09h45.12.345.psydat
```

El CSV tiene exactamente 36 filas, una por trial: a diferencia de un
experimento de Builder, no hay filas de instrucciones ni de despedida.

## Qué hay adentro

| Archivo | Qué es |
|---|---|
| `stroop_min.py` | El experimento entero, ~280 líneas con documentación |
| `condiciones_stroop.csv` | 9 condiciones: 3 congruentes, 6 incongruentes, en paleta accesible |

**36 trials** en total (9 condiciones × 4 repeticiones), unos 3 minutos.

## Parámetros que se pueden tocar

Están todos como constantes en mayúsculas al principio de
`stroop_min.py`:

| Constante | Por defecto | Qué cambia |
|---|---|---|
| `N_REPEATS` | `4` | Cantidad de trials (9 × N) |
| `FULLSCREEN` | `True` | Poner en `False` **solo** para depurar |
| `FIXATION_DURATION` | `0.5` | Duración de la cruz de fijación, en segundos |
| `MAX_RESPONSE_TIME` | `3.0` | Cuánto se espera antes de dar el trial por perdido |
| `RESPONSE_KEYS` | `["a", "n", "b"]` | Teclas de respuesta |

## La paleta no es rojo, verde y azul

Azul `#0072B2`, naranja `#E69F00` y blanco `#FFFFFF` sobre gris oscuro
`#4D4D4D`. La tríada clásica del Stroop es inservible para un
deuteranope —rojo y verde le quedan a ΔE 10 en CIELAB, prácticamente el
mismo color— y con ~8 % de los varones afectados, en un grupo de 27
personas es probable que haya al menos una.

Esta paleta se mantiene por encima de ΔE 33 en protanopía, deuteranopía
y tritanopía.

El feedback también evita el eje rojo-verde, y va codificado por
partida doble con símbolo y color.

## Por qué está escrito en Coder y no en Builder

Tres razones, y las tres son pedagógicas:

1. **Cero dependencia de versión.** Un `.psyexp` hecho con otra versión
   puede abrirse mal; un script de Python corre igual en cualquiera.
2. **Usa los mismos objetos que genera el Builder** —
   `ExperimentHandler`, `TrialHandler`, `hardware.keyboard.Keyboard` —
   así el CSV que produce tiene exactamente la estructura estándar que
   se estudia el día 2.
3. **Sirve como referencia del "otro extremo"**: el mismo experimento
   que arman en el Builder, escrito a mano.

## Con pantalla completa hay un detalle

`FULLSCREEN = True` es lo correcto para cualquier medición: en modo
ventana el compositor del sistema operativo agrega retrasos variables.
Si durante la clase alguien necesita ver el código y el experimento a
la vez, puede ponerlo en `False`, pero entonces **sus datos no sirven
para hablar de timing** — lo cual, dicho en clase, es una buena
demostración del punto.
