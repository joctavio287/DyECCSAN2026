# Formato de datos de PsychoPy — referencia

Documento de consulta para el día 2: la revisión de archivos de datos y
el análisis. Sirve tanto para proyectar como para llevarse.

Todo lo que dice acá está verificado con PsychoPy **2026.2.3**, corriendo
los experimentos del curso. Otras versiones pueden cambiar detalles
(nombres de columnas internas, formato de la fecha); la lógica no
cambia.

---

## 1. Qué archivos escribe PsychoPy

Al terminar una sesión, en la carpeta `data/` aparecen varios archivos
con **el mismo nombre y distinta extensión**:

```
data/
├── sub-07_stroop_2026-09-30_10h15.23.456.csv      ← el que se analiza
├── sub-07_stroop_2026-09-30_10h15.23.456.psydat   ← respaldo completo
└── sub-07_stroop_2026-09-30_10h15.23.456.log      ← cronología de todo
```

| Extensión | Qué es | Cuándo se usa |
|---|---|---|
| **`.csv`** | Tabla ancha, una fila por entrada | **Siempre.** Es el archivo de análisis |
| **`.psydat`** | Objeto Python serializado | Cuando al CSV le falta algo. Se abre con `psychopy.tools.filetools.fromFile()` |
| **`.log`** | Registro cronológico con marca de tiempo | Timing, frames perdidos, marcas, orden de eventos |
| **`.hdf5`** | Datos densos (eyetracking, ioHub) | Solo si se usa ioHub |

En el Builder se eligen en **Settings → Data**. El Stroop mínimo, que
está escrito en Coder, deja solo el `.csv` y el `.psydat`.

> **Regla:** los archivos crudos no se editan **nunca**. Ni para
> arreglar un typo, ni para sacar a alguien. El análisis lee los crudos
> y escribe copias.

---

## 2. De dónde sale el nombre del archivo

Plantilla por defecto, en **Settings → Data → Data filename**:

```python
'data/' + expInfo['participant'] + '_' + expName + '_' + expInfo['date']
```

que produce:

```
data/sub-07_stroop_2026-09-30_10h15.23.456.csv
     └─┬──┘ └──┬─┘ └──────────┬──────────┘
       │       │              └── fecha y hora, con milisegundos
       │       └───────────────── nombre del experimento
       └───────────────────────── campo `participant` del diálogo
```

**Consecuencias prácticas:**

- Si todxs escriben `test` en el diálogo, los archivos no se pisan
  (la hora es distinta), pero es imposible saber quién es quién.
- Nada de nombres y apellidos: es un dato personal viajando en el
  nombre del archivo. Códigos (`sub-01`, `sub-02`…) y la
  correspondencia, si hace falta, guardada aparte.
- Los ceros a la izquierda importan: `sub-01 … sub-12` ordena bien;
  `sub-1 … sub-12` pone `sub-10` antes que `sub-2`.
- En un experimento nuevo, el Builder 2026 propone en `participant` un
  número al azar de seis dígitos: hay que reemplazarlo por el código.

---

## 3. Anatomía del CSV

Toda columna pertenece a uno de estos cuatro grupos. Ante una columna
que no se entiende, la pregunta es "¿de cuál de los cuatro es?".

### Grupo A — Las que vienen del archivo de condiciones

`word`, `ink_name`, `ink_colour`, `congruent`, `correct_key`

Tus columnas, con tus nombres, en el orden en que los trials ocurrieron
de verdad (no en el del archivo de condiciones).

### Grupo B — Las que registró el trial

En un experimento de **Builder**, cada componente escribe columnas con
su nombre como prefijo:

| Columna | Qué guarda |
|---|---|
| `respuesta.keys` | Qué tecla se apretó |
| `respuesta.rt` | Tiempo de respuesta en **segundos** (`0.581` = 581 ms) |
| `respuesta.corr` | 1 o 0, si se tildó *Store correct* |
| `respuesta.duration` | Cuánto se mantuvo apretada la tecla |
| `palabra.started` | Cuándo apareció, en segundos desde el inicio |
| `fijacion.stopped` | Cuándo se apagó |
| `trial.started` / `trial.stopped` | Comienzo y fin de la rutina |

Las columnas `.started` y `.stopped` existen para cada componente y
cada rutina: sirven para verificar si las duraciones fueron las que se
pidieron. Además aparece todo lo que se guarde con
`thisExp.addData('nombre', valor)`.

El **Stroop mínimo** (Coder) guarda las mismas cosas con otros nombres,
porque las elige el script: `response_key`, `response_time`, `correct`
y `stimulus_onset`.

> Ojo: el RT está en **segundos**. Reportar "0.6 ms" en vez de
> "600 ms" pasa más de lo que parece.

### Grupo C — El estado del bucle

Con un bucle llamado `trials`:

| Columna | Qué significa |
|---|---|
| `trials.thisRepN` | En qué repetición del archivo de condiciones va |
| `trials.thisTrialN` | Número de trial **dentro** de la repetición (se reinicia) |
| `trials.thisN` | Número de trial **total** (no se reinicia) |
| `trials.thisIndex` | Qué **fila del archivo de condiciones** se usó |

Todo cuenta **desde 0**. `thisIndex` es la más útil y la más ignorada:
es la prueba de que la aleatorización funcionó. Si
`trials['trials.thisIndex'].value_counts()` no da lo mismo para todas
las condiciones, algo anda mal.

Con bucles anidados aparece un juego de columnas por bucle
(`bloques.thisN`, `trials.thisN`…). El Builder 2026 además repite
algunas: `thisN`, `thisTrialN`, `thisRepN` sin prefijo, y
`trials.respuesta.rt` como copia de `respuesta.rt`.

### Grupo D — Información de la sesión

`participant`, `session`, `date`, `expName`, `psychopyVersion`,
`frameRate`, `expStart`, y cualquier campo que se agregue al diálogo
(`edad`).

Se repite idéntica en todas las filas: por eso se pueden juntar
archivos de muchas personas y seguir sabiendo de quién es cada fila.
`psychopyVersion` es la que van a agradecer cuando tengan que
reportarla en Métodos. `frameRate` es la frecuencia de refresco que
midió PsychoPy al empezar.

> Aparecen también columnas de contabilidad interna (`thisRow.t`,
> `notes`, `piloting`) y una última columna sin nombre, porque cada
> línea termina en coma: pandas la lee como `Unnamed: 45`. Si una
> columna no encaja en A, B o C, es de sesión o interna, y no se
> analiza.

---

## 4. Las filas que no son trials

Esto es lo que más confunde al abrir un CSV del Builder, y depende de
cómo está armado el experimento.

**En el Builder, cada rutina que está fuera de un bucle escribe su
propia fila.** El Stroop de la Consigna 1 tiene 38 filas, no 36:

| Fila | Qué es | Qué columnas tienen algo |
|---|---|---|
| 0 | La rutina `instrucciones` | `instrucciones.started`, `tecla_instrucciones.started`… y las de sesión |
| 1 a 36 | Los 36 trials | Todas las de trial |
| 37 | La rutina `despedida` | `despedida.started`… y las de sesión |

Con bucles anidados, además, **cada bloque cierra con una fila
propia**. El Stroop con práctica y test tiene 46 filas: 42 trials, las
instrucciones, la despedida y el cierre de cada uno de los dos bloques.

**En el Stroop mínimo (Coder) no hay filas extra**: son exactamente 36,
porque el script solo cierra una fila después de cada trial.

No es un error. Pero si no se filtran, meten un `NaN` en cada promedio
y trials de más en cada conteo. **El filtro, siempre el primero:**

```python
trials = trials[trials['respuesta.rt'].notna()]   # Builder
trials = trials[trials['response_time'].notna()]  # Stroop mínimo
```

Un trial sin respuesta también tiene el RT vacío. Si el experimento
tiene tiempo límite y importa contar las omisiones, filtrar por una
columna que siempre tenga valor en los trials (`trials.thisN`).

---

## 5. Los datos de Pavlovia

Si el experimento corre online, los CSV quedan en el servidor:

1. <https://pavlovia.org/> → **Dashboard** → **Experiments**
2. Elegir el experimento → **Download results**
3. Se baja un `.zip` con un CSV por participante

**Diferencias con los archivos locales:**

- Aparecen columnas propias de PsychoJS (navegador, resolución).
- El campo `participant` puede venir de la URL
  (`?participant=sub-07`), que es lo recomendable para no depender de
  que la gente escriba bien.
- Hay sesiones incompletas: gente que cerró la pestaña. Decidir qué
  hacer con ellas **antes** de mirarlas.
- En modo *piloting* no queda nada en el servidor: el CSV se descarga
  en la computadora de quien corrió.

---

## 6. Recetas de pandas

```python
from pathlib import Path
import pandas as pd

# --- un solo archivo -------------------------------------------------
trials = pd.read_csv('data/sub-07_stroop_2026-09-30_10h15.23.456.csv')

trials.shape          # 38 filas en el Stroop de Builder: 36 trials + 2
trials.columns        # para clasificarlas en A, B, C y D
trials.head()         # la primera fila son las instrucciones
trials.tail()         # la última, la despedida

# --- todos los participantes ----------------------------------------
csv_paths = sorted(Path('data').glob('*.csv'))
trials = pd.concat(
    [pd.read_csv(path).assign(source_file=path.name)
     for path in csv_paths],
    ignore_index=True,
)

# --- limpiar ---------------------------------------------------------
is_trial   = trials['respuesta.rt'].notna()
is_correct = trials['respuesta.corr'] == 1
in_window  = trials['respuesta.rt'].between(0.2, 2.0)
clean = trials[is_trial & is_correct & in_window]

# --- verificar que la aleatorización anduvo --------------------------
clean.groupby('participant')['trials.thisIndex'].value_counts()

# --- un número por persona y condición -------------------------------
por_persona = (
    clean
    .groupby(['participant', 'congruent'], as_index=False)['respuesta.rt']
    .mean()
)

# --- efecto Stroop ---------------------------------------------------
ancho = por_persona.pivot(
    index='participant', columns='congruent', values='respuesta.rt'
)
efecto = (ancho[0] - ancho[1]) * 1000   # en ms
```

Las mismas operaciones para el Stroop mínimo, ya empaquetadas en
funciones, están en
[`dia2/analisis/lectura_datos_psychopy.py`](../dia2/analisis/lectura_datos_psychopy.py).

---

## 7. Checklist de control de calidad

Antes de analizar nada, sobre los datos crudos:

- [ ] Cada participante tiene la cantidad de trials esperada (después
      de filtrar las filas que no son trials)
- [ ] Hay un archivo por participante, y ninguno duplicado
- [ ] `participant` es distinto en cada archivo
- [ ] `psychopyVersion` es la misma en todos
- [ ] `frameRate` es cercano al valor nominal del monitor (60, 120,
      144)
- [ ] `trials.thisIndex` aparece la misma cantidad de veces por
      condición
- [ ] Los aciertos no están en el azar (~33 % con tres teclas, ~50 %
      con dos) ni en 100 % para todxs
- [ ] No hay RT negativos ni mayores al máximo que permite la tarea
- [ ] `.started` y `.stopped` dan las duraciones que se pidieron

Si alguno falla, **el problema es del experimento, no del análisis**.
Vale más media hora acá que un mes de análisis sobre datos rotos.
