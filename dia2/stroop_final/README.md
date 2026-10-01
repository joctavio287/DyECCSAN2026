# El Stroop, versión final

El Stroop que armaron el día 1 (práctica y test con bucles anidados,
feedback en la práctica y un descanso) con los recaudos de timing del
día 2. Sirve de modelo para su propio experimento.

## Cómo abrirlo

**Builder → File → Open →** `stroop_final.psyexp`. Tiene que quedar en
la misma carpeta que `bloques.csv`, `practica.csv` y `test.csv`. Los
datos se guardan en `data/`, al lado.

## Qué tiene de nuevo

| Recaudo | Para qué | Dónde está |
|---|---|---|
| Precargar el estímulo | Que cargarlo no demore su aparición | Rutina `trial`: componente Static `ISI`, de 0 a 0.5 s, durante la fijación. En `palabra`, Text y Color dicen **set during: trial.ISI** |
| La marca en el flip | Que la marca salga cuando el estímulo aparece, no antes | Componente Code `marca` (el de la Consigna 5) y la columna `trigger_code` en `practica.csv` y `test.csv` |
| Contar frames perdidos | Saber si cada estímulo duró lo que se pidió | Componente Code `control_frames`: guarda `frames_perdidos` en cada trial e imprime el total al final |
| Guardar lo que sirve | Un CSV con una fila por trial, más el `.log` y el `.psydat` | Experiment Settings → Data. *Save csv file (summaries)* está destildado: con bucles que repiten condiciones, ese resumen se rompe con `IndexError` |
| Pantalla completa | Menos frames perdidos | Experiment Settings → Screen |

## Cómo precargar en su experimento

1. En la rutina del trial, agregá un componente **Static** (Custom →
   Static) que dure lo mismo que la fijación o el intervalo antes del
   estímulo.
2. Recién ahí, en el desplegable del campo del estímulo (Image, Sound,
   Movie o Text) aparece **set during: trial.ISI**. Elegilo.
3. El estímulo tiene que empezar **después** de que termine el Static.
   Mientras dura, la pantalla queda quieta con lo que ya estaba (acá,
   la cruz).

Con texto la carga es mínima: acá está para mostrar cómo se hace. Donde
de verdad importa es con imágenes, sonidos y videos.

## Cómo comprobar que anduvo

En el `.log` de `data/`, que se abre con cualquier editor de texto:

- una línea `DATA TRIGGER <código>` por trial, con la misma hora que
  `palabra: autoDraw = True`;
- ninguna línea `We overshot the intended duration`: si aparece, la
  carga no entró en el tiempo del Static;
- al final, `DATA FRAMES PERDIDOS <n>`.

En el CSV, la columna `frames_perdidos`: lo importante es que no haya
más en una condición que en otra, porque esa diferencia de duración
quedaría confundida con la condición.
