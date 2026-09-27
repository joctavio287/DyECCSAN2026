# PsychoPy en una página

> Para imprimir en una hoja, doble faz, y repartir el día 1.
> CSAN 2026 · Juan Kamienkowski y Octavio Castro

---

# CARA A — Construir

## Las tres ventanas

**Builder** armás arrastrando · **Coder** escribís Python ·
**Runner** corre y **muestra los errores**

> Si algo falla y no sabés por qué: **mirá el Runner**. La respuesta
> está en la última línea.

## Rutinas y bucles

| | Qué es |
|---|---|
| **Rutina** | Lo que pasa en un momento (un trial, una pantalla) |
| **Bucle** | Lo que se repite, envuelve rutinas |
| **Flow** | El diagrama = tu experimento |

## Componentes que vas a usar

`Text` · `Image` · `Sound` · `Keyboard` · `Mouse` · `Code` ·
`Parallel Port` · `Eyetracker`

## El archivo de condiciones

Una **fila** por condición, una **columna** por variable.

| word | ink_colour | congruent | correct_key |
|---|---|---|---|
| AZUL | #0072B2 | 1 | a |
| AZUL | #E69F00 | 0 | n |

⚠️ Nombres de columna sin espacios, sin acentos. Guardar como **CSV**.

## El signo `$` y *set every repeat*

```
Text  = $word           ← usa la columna "word"
Color = $ink_colour     ← usa la columna "ink_colour"
```

> **Si la palabra no cambia entre trials**, el campo quedó en
> *constant*. Ponelo en **set every repeat**. Es el error nº 1.

El `$` va en campos de texto, color y archivo (`$word`). En campos
numéricos va el nombre solo: *Volume* = `volumen_bip`.

## Tipos de bucle

| | Qué hace |
|---|---|
| `sequential` | En el orden del archivo |
| `random` | Baraja dentro de cada repetición |
| `fullRandom` | Baraja todas las repeticiones juntas |

`nReps` × filas del CSV = cantidad de trials

## Bucles anidados (bloques)

El bucle externo lee `blocks.csv`, cuya columna `archivo_del_bloque`
tiene **nombres de archivo**. El bucle interno pone
`$archivo_del_bloque` en su campo *Conditions*.

## Duraciones

**Frames, no segundos.** A 60 Hz, un frame = 16.7 ms.
Pedir 200 ms → poner **12 frames**. Pedir 20 ms es imposible.

## Antes de correr a nadie

1. ¿Cuál es **un** trial? Dibujalo con tiempos
2. ¿Qué cambia? → columnas del CSV
3. ¿Cuántas veces? → `nReps`
4. **¿Qué se guarda?** → hacé la lista *antes*
5. ¿Qué haría alguien que quiere hacer trampa?

---

# CARA B — Código y datos

## Componente de código: las cinco pestañas

| Pestaña | Cuándo corre |
|---|---|
| `Begin Experiment` | Una vez, al arrancar |
| `Begin Routine` | Al empezar cada trial |
| `Each Frame` | ~60 veces por segundo |
| `End Routine` | Al terminar cada trial |
| `End Experiment` | Una vez, al final |

> El componente de código va **arriba** de los componentes que usan sus
> variables. Se ejecutan en el orden de la lista.

> **Una rutina termina cuando terminan todos sus componentes.** Un
> componente que arranca "por condición" y nunca la cumple deja la
> rutina colgada.

## Recetas

```python
# Terminar la rutina antes de tiempo — Each Frame
if respuesta.keys:
    continueRoutine = False

# Saltear una rutina — Begin Routine
if tipo_de_bloque != 'practica':
    continueRoutine = False

# Contador de trials — Begin Routine
texto = f'trial {trials.thisN + 1} de {trials.nTotal}'

# Feedback acumulado
n_correctas = 0                      # Begin Experiment
n_correctas += respuesta.corr        # End Routine
precision = 100 * n_correctas / trials.thisN

# Guardar algo propio — End Routine
thisExp.addData('mi_columna', valor)
```

> **Si el experimento lo decide, el experimento lo guarda.**
> Todo lo que aleatorices por código, guardalo con `addData`.

## Los dos objetos que explican el CSV

`TrialHandler` = tu bucle · `ExperimentHandler` = tu archivo de datos

## El archivo de datos

```
data/sub-07_stroop_2026-09-30_10h15.23.456.csv
     └─┬──┘ └──┬─┘ └──────────┬──────────┘
 participante  experimento   fecha y hora
```

| Extensión | Para qué |
|---|---|
| `.csv` | El que se analiza |
| `.psydat` | Respaldo completo |
| `.log` | Timing y frames perdidos |

## Las cuatro clases de columna

| Grupo | Ejemplo |
|---|---|
| Del archivo de condiciones | `word`, `congruent` |
| Registradas en el trial | `respuesta.keys`, `respuesta.rt`, `respuesta.corr`, `palabra.started` |
| Estado del bucle | `trials.thisRepN`, `.thisTrialN`, `.thisN`, `.thisIndex` |
| Metadata de sesión | `participant`, `date`, `psychopyVersion`, `frame_rate` |

⚠️ `.rt` está en **segundos**. 0.581 = 581 ms.
⚠️ Todo cuenta **desde 0**.
⚠️ Las rutinas **fuera del bucle** (instrucciones, despedida) escriben
su propia fila: la primera y la última no son trials. Filtralas.

## pandas en seis líneas

```python
import pandas as pd
from pathlib import Path

trials = pd.concat(
    [pd.read_csv(p).assign(source_file=p.name)
     for p in sorted(Path('data').glob('*.csv'))],
    ignore_index=True,
)
trials.shape; trials.columns; trials.head(); trials.tail()

clean = trials[
    trials['respuesta.rt'].notna()
    & (trials['respuesta.corr'] == 1)
    & trials['respuesta.rt'].between(0.2, 2.0)
]

clean.groupby(['participant', 'congruent'])['respuesta.rt'].mean()
```

> Promediá **primero dentro de cada participante**, después entre
> participantes.

## Timing: los números

| | |
|---|---|
| Frame a 60 Hz | 16.7 ms |
| Teclado USB | 4–25 ms de latencia |
| Monitor con post-procesado | 20–30 ms extra, variable |
| PsychoPy en lab | precisión < 1 ms |
| PsychoPy online (RT) | precisión < 3.5 ms |

Pantalla completa · cerrá todo · precargá los estímulos ·
medí el frame rate real

## Marcas TTL — las seis reglas

```python
# En Coder: primero el flip, después la marca
win.flip()
puerto.setData(codigo)
core.wait(0.005)
puerto.setData(0)                    # y bajala a cero

# En Builder, desde un componente de código (Each Frame):
if estimulo.status == STARTED and marca_pendiente:
    win.callOnFlip(puerto.setData, codigo)   # sale con el flip
    marca_pendiente = False

thisExp.addData('trigger_code', codigo)      # guardala también
```

1. El reloj de la compu **no puede** medirse a sí mismo
2. El trigger va **después** del `flip`
3. La línea **vuelve a cero**, o dos eventos iguales se ven como uno
4. **Un código por condición** (10 = congruente, 20 = incongruente)
5. Se **valida una vez** con fotodiodo + osciloscopio, y sirve para
   siempre
6. Lo que el experimento decide, el experimento lo **guarda**

En Builder: componente **Parallel Port Out** o **Serial Out**.
*Start data* acepta `$trigger_code` — sale del CSV, igual que `$word`.

⚠️ Arduino saca 5 V; muchos amplificadores esperan 3.3 V.
⚠️ Entre la compu y alguien conectado a un equipo: **optoacoplador**.
⚠️ Masa común, o no se mide nada.

## Citar

> Peirce et al. (2019). PsychoPy2: Experiments in behavior made easy.
> *Behavior Research Methods*, 51(1), 195–203.

Reportá también: versión, SO, monitor, Hz, teclado.

## Cuando algo falla

1. Mirá el **Runner** (o **F12 → Console** si corre en el navegador)
2. Buscá en <https://discourse.psychopy.org/>
3. Preguntá con: versión, SO, error completo, archivo mínimo
