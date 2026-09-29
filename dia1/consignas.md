# Consignas del día 1

Cada consigna está escrita para leerse sola, sin depender de haber escuchado la explicación.

---

# Consigna 0 — Correr antes de entender

**Cuándo:** día 1, 9:30, antes de la primera diapositiva.
**Modalidad:** individual.

## Qué hacer

1. Descomprimí los materiales del curso en una carpeta **sin acentos
   ni espacios** en el nombre, fuera de OneDrive, Google Drive o
   Dropbox.
2. Abrí PsychoPy → ventana **Coder** → **File → Open** →
   `dia1/stroop_minimo/stroop_min.py`.
3. Apretá **Run** (el triángulo verde).
4. En el diálogo, en `participant` poné el código que te dimos al
   entrar (`001`, `002`…). **No pongas tu nombre.**
5. Hacé la tarea: aparece una palabra escrita en un color y respondés
   **el color de la letra**:
   - **A** = azul · **N** = naranja · **B** = blanco
6. Al terminar, buscá el archivo `.csv` que quedó en la carpeta
   `data/`, al lado del script, y **subilo ya** a la tarea **Stroop de
   la clase** del Classroom.

Esos archivos son los datos que vamos a analizar mañana entre todxs.

Este experimento está escrito en código (Coder), no en el Builder: el
Builder lo vas a armar vos, desde cero, a partir de las 11:35.

## Si no funciona

Levantá la mano. No te pelees solx media hora: anotá el mensaje de
error exacto (está en la ventana **Runner**, casi siempre en la última
línea) y mirá cómo lo hace alguien al lado.

## Para pensar mientras esperan a lxs demás

1. ¿Qué te costó más, la parte en que la palabra y su color coincidían
   o en la que no? ¿Cuánto más, en milisegundos?
2. ¿Cuántos trials hiciste? ¿Cómo lo sabés?
3. Si tuvieras que armar esta tarea, ¿qué **cambia** de un trial a otro
   y qué se **repite igual**?
4. ¿Qué habría que guardar en cada trial para poder analizarla
   después?

---

# Consigna 1 — El Stroop en Builder

**Cuándo:** partes A y B a las 11:35; parte C a las 13:30, después del
almuerzo; partes D y E a las 14:00.
**Modalidad:** guiada, todxs al mismo tiempo; de a dos si hace falta.

## Objetivo

Reconstruir desde cero, en el Builder, el experimento que corriste a la
mañana. Al final tiene que correr de punta a punta y dejar un CSV.

**Si te atrasás o algo se rompe**, hay un punto de control por cada
etapa en `dia1/stroop_builder/`: abrí el del paso que
corresponde y seguí desde ahí.

---

## Parte A — El archivo de condiciones (15 min)

En Excel o LibreOffice, creá un archivo con estas columnas **exactas**
y guardalo como **CSV** con el nombre `condiciones.csv`, en una carpeta
nueva para tu experimento:

| word | ink_name | ink_colour | congruent | correct_key |
|---|---|---|---|---|
| AZUL | azul | #0072B2 | 1 | a |
| NARANJA | naranja | #E69F00 | 1 | n |
| BLANCO | blanco | #FFFFFF | 1 | b |
| AZUL | naranja | #E69F00 | 0 | n |
| AZUL | blanco | #FFFFFF | 0 | b |
| NARANJA | azul | #0072B2 | 0 | a |
| NARANJA | blanco | #FFFFFF | 0 | b |
| BLANCO | azul | #0072B2 | 0 | a |
| BLANCO | naranja | #E69F00 | 0 | n |

⚠️ Nombres de columna **sin espacios ni acentos**. Guardar como CSV,
no como `.xlsx`.

> **¿Por qué estos colores y no rojo, verde y azul?** Porque uno de
> cada doce varones no distingue el rojo del verde. Si tu estímulo es
> un color, esto es diseño experimental, no estética.

**Pregunta:** ¿por qué hay 3 filas congruentes y 6 incongruentes? ¿Es
un problema? ¿Cómo lo arreglarías si lo fuera?

---

## Parte B — Las rutinas (40 min)

Creá un experimento nuevo (**File → New**), guardalo **en la misma
carpeta que `condiciones.csv`**, y armá tres rutinas.

**1. `instrucciones`**
- **Text**: la explicación de la tarea y las teclas. Sin tiempo de
  corte (*Stop* vacío).
- **Keyboard** `tecla_instrucciones`: *Allowed keys* = `'space'`,
  *Force end of Routine* tildado, sin tiempo de corte.

**2. `trial`**
- **Text** `fijacion`: texto `+`, *Start* 0, *Stop* 0.5 (duración).
- **Text** `palabra`:
  - *Text* = `$word` · **set every repeat**
  - *Color* = `$ink_colour` · **set every repeat**
  - *Color space* = `hex`
  - *Start* 0.5, *Stop* vacío.
- **Keyboard** `respuesta`:
  - *Allowed keys* = `'a','n','b'`
  - *Store correct* tildado · *Correct answer* = `$correct_key`
  - *Force end of Routine* tildado · *Start* 0.5, *Stop* vacío.

**3. `despedida`**
- **Text** con un mensaje de agradecimiento, *Stop* 3.

---

## Parte C — El bucle (20 min, después del almuerzo)

- **Insert Loop**, envolviendo **solo** la rutina `trial`.
- *Name* = `trials` · *loopType* = `random` · *nReps* = `4`
- *Conditions* = `condiciones.csv` (con **Browse**, así queda con la
  ruta correcta).

### Puntos de control a las 14:00

- [ ] La pantalla de instrucciones espera la barra espaciadora
- [ ] La palabra cambia de trial a trial, y el color también
- [ ] Son 36 trials
- [ ] Corre en pantalla completa sin trabarse

Si la palabra es siempre la misma, revisá que los campos digan **set
every repeat** y no *constant*. Es el error número uno.

---

## Parte D — Feedback y sonido (35 min)

Agregá una rutina `feedback` **después** de `trial`, **dentro** del
bucle (el bucle tiene que envolver las dos).

**1. Componente Code** `codigo_feedback`, pestaña **Begin Routine**:

```python
if respuesta.corr:
    mensaje = 'correcto'
    color_mensaje = '#56B4E9'
    volumen_bip = 0
else:
    mensaje = 'incorrecto'
    color_mensaje = '#E69F00'
    volumen_bip = 1
```

Celeste y naranja, no verde y rojo: una tarea pensada para que sea
accesible no puede usar justo el par de colores que no se distinguen.

**2. Text** `texto_feedback`: *Text* = `$mensaje`, *Color* =
`$color_mensaje`, los dos **set every repeat**, *Color space* = `hex`,
*Stop* 0.4.

**3. Sound** `bip_error`: *Sound* = `500` (un número es una frecuencia
en Hz), *Stop* 0.2, *Volume* = `volumen_bip` · **set every repeat**.

⚠️ El componente de código tiene que estar **arriba** de los otros en
la rutina: se ejecutan en el orden de la lista, y si el texto va
primero, `mensaje` todavía no existe.

⚠️ En *Volume* va `volumen_bip`, **sin** `$`: en los campos que son
números no hace falta.

**Pregunta:** el bip suena en todos los trials, con volumen 0 en los
correctos. ¿Por qué no hacer que el Sound arranque solo cuando la
respuesta es incorrecta (*Start* → *condition* → `not respuesta.corr`)?
Probalo y fijate qué pasa en un trial correcto.

---

## Parte E — Datos y primera mirada (25 min)

1. **Settings** (el engranaje) → pestaña **Basic** → *Experiment info*:
   agregá un campo `edad`.
2. **Settings → Data**: verificá que estén tildados *Save wide csv
   file*, *Save psydat file* y *Save log file*.
3. Corré el experimento **completo**.
4. Abrí el CSV que quedó en `data/` con Excel o LibreOffice y **solo
   miralo**:
   - ¿Cuántas filas tiene? ¿Coincide con lo que esperabas?
   - ¿Reconocés las columnas de tu archivo de condiciones?
   - **¿Qué tienen de raro la primera y la última fila?**

## Entregable

Un `.psyexp` que corre de punta a punta y deja un CSV en `data/`.
**Guardalo: lo vas a transformar en la Consigna 2.**

---

# Consigna 2 — Su propio experimento

**Cuándo:** día 1, 15:25.
**Modalidad:** de a dos.

## Objetivo

Convertir tu Stroop en otro experimento. La estructura queda igual
(instrucciones, trial y feedback dentro de un bucle, despedida);
cambian las condiciones, el estímulo y las teclas.

**Mañana, el resto de la clase va a correr tu experimento.**

## Parte A — Elegir (5 min)

| Variante | La tarea | Qué se mide |
|---|---|---|
| **Simon** | Un cuadrado azul o naranja a la izquierda o a la derecha; se responde el color | ¿Se tarda más cuando el lado no coincide con la tecla? |
| **Flanker** | Cinco flechas; se responde hacia dónde apunta la del medio | ¿Se tarda más cuando las de los costados apuntan al revés? |
| **Auditiva** | Dos tonos: ¿el segundo es más agudo o más grave? | ¿Cuánto se acierta según la diferencia en Hz? |
| **Orientación** | Un gabor (un parche de rayas) que aparece 200 ms, inclinado | ¿Cuánto se acierta según el ángulo? |
| **Propia** | Si traen una idea y entra en la misma estructura | La que elijan |

Cada variante tiene su `condiciones.csv` listo en
`dia1/variantes/<variante>/`.

## Parte B — Copiar y apuntar el bucle (10 min)

1. Con tu Stroop abierto: **File → Save As**, dentro de la carpeta de
   la variante, con otro nombre (`simon.psyexp`, por ejemplo). Así el
   `condiciones.csv` nuevo queda al lado.
2. En el bucle `trials`: *Conditions* = el `condiciones.csv` de la
   variante (con **Browse**). Mirá qué columnas trae.
3. *nReps* = `10` para Simon y Flanker, `6` para Auditiva y
   Orientación.

## Parte C — Cambiar el estímulo (25 min)

En la rutina `trial`, borrá `palabra` y agregá el componente que
corresponde. En `respuesta`: *Allowed keys* = `'z','m'`; *Correct
answer* sigue siendo `$correct_key`.

**Simon — Polygon** `cuadrado`
- *Shape* = `rectangle` · *Size* = `(0.15, 0.15)`
- *Position* = `(pos_x, 0)` · **set every repeat**
- *Fill color* y *Border color* = `$color` · **set every repeat** ·
  *Color space* = `hex`
- *Start* 0.5, *Stop* vacío

**Flanker — Text** `flechas`
- *Text* = `$estimulo` · **set every repeat**
- *Font* = `Courier New` · *Letter height* = 0.1
- *Start* 0.5, *Stop* vacío

**Auditiva — dos Sound**
- `fijacion`: *Stop* vacío (queda toda la rutina)
- **Sound** `referencia`: *Sound* = `500`, *Start* 0.5, *Stop* 0.3
- **Sound** `comparacion`: *Sound* = `$frecuencia` · **set every
  repeat** · *Start* 1.1, *Stop* 0.3
- `respuesta`: *Start* 1.4
- En la rutina `feedback`, borrá el bip: se confunde con los tonos

**Orientación — Grating** `gabor` (un grating con máscara gaussiana es
un gabor)
- *Texture* = `sin` · *Mask* = `gauss` · *Size* = `(0.4, 0.4)`
- *Spatial frequency* = `20`
- *Orientation* = `orientacion` · **set every repeat**
- *Start* 0.5, *Stop* 0.2

## Parte D — Instrucciones y prueba (15 min)

1. Reescribí el texto de `instrucciones`: qué va a ver, qué tiene que
   responder, con qué teclas.
2. Corré el experimento completo con tu código de participante.

### Puntos de control

- [ ] El estímulo cambia de trial a trial como dice el CSV
- [ ] Las teclas `z` y `m` responden, y el feedback dice si acertaste
- [ ] En el CSV aparecen las columnas de tu archivo de condiciones

## Preguntas

1. ¿Qué esperás encontrar? Escribilo ahora, antes de ver ningún dato.
2. ¿Qué columna del CSV va a responder esa pregunta?
3. ¿Qué cambiarías si fuera un experimento de verdad (cantidad de
   trials, práctica, descansos)?

## Si terminás antes

Agregale práctica y test con bucles anidados, como en
`dia1/stroop_builder/paso3_bloques/`.

---

# Consigna 3 — Del laboratorio al navegador

**Cuándo:** día 1, 16:40, después de la demo.
**Modalidad:** de a dos, sobre el experimento de la Consigna 2.

## Objetivo

Dejar tu experimento listo para que mañana lo corran otras personas en
tu computadora, y revisar qué habría que cambiar para que corra en un
navegador.

## Parte A — ¿Cruza a JavaScript? (15 min)

1. **Settings → Basic**: *Units* = `height`. En cada componente,
   *Units* = `from exp settings`.
2. En cada componente de código: *Code Type* = `Auto -> JS`. Mirá la
   columna de la derecha: es tu código traducido a JavaScript.
3. Si algún componente de código usa `import`, anotalo: en el navegador
   no hay Python, y eso no cruza.

## Parte B — Dejarlo listo en tu computadora (15 min)

1. Tu carpeta tiene que quedar con **solo** el `.psyexp` y los CSV de
   condiciones. Borrá la carpeta `data/` de las pruebas y cualquier
   `*_lastrun.py`: así, mañana, lo único que hay en `data/` son los
   datos de lxs demás.
2. Renombrala `pareja_XX_variante` (el número de pareja está en el
   pizarrón).
3. Escribí en un papel, al lado de la computadora, cómo se responde:
   las teclas y qué significa cada una.

## Parte C — Probar en limpio (10 min)

Que una persona de **otra** pareja corra tu experimento en tu
computadora, como si fuera mañana, con su código de participante.
Mirá sin ayudar: si algo no se entiende, arreglalo hoy. Después borrá
ese CSV de prueba.

---

# Consigna 7 — Preguntas sobre tu proyecto

**Cuándo:** se presentan al cierre del día 1; se charlan el día 2, a
las 17:00, con quien quiera.
**Modalidad:** individual o por grupo de investigación.

No es una hoja para entregar: son las preguntas que conviene traer
pensadas para charlar sobre tu proyecto. Con las respuestas en la
cabeza, diez minutos de charla rinden lo que sin ellas rinde una hora.

1. **La pregunta.** ¿Qué querés averiguar? Una frase, sin
   tecnicismos.
2. **Un trial.** ¿Cuál es la secuencia de un trial, con sus tiempos?
3. **Lo que varía.** ¿Qué cambia entre trials? Cada ítem va a ser una
   columna del archivo de condiciones.
4. **Lo que se mide.** ¿Qué registrás en cada trial? ¿En qué unidades?
5. **Diseño.** ¿Cuántas condiciones? ¿Cuántos trials por condición?
   ¿Cuántxs participantes? ¿Intra o entre sujetos? ¿Hay bloques?
6. **Dónde corre.** ¿Laboratorio, online o ambos? ¿De qué tamaño es el
   efecto que esperás, en ms? ¿Qué precisión temporal necesita?
7. **Hardware.** ¿EEG, eyetracker, fMRI, caja de botones, otro? ¿Ya
   tienen el equipo? ¿Alguien lo usó antes en tu laboratorio?
8. **El obstáculo.** ¿Qué es lo que **no** sabés cómo hacer? Sé
   específicx: ahí es donde la charla rinde.
