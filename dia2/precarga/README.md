# Precargar imágenes (y qué pasa con el sonido)

Un demo chico en dos versiones, para ver qué cambia al precargar. La
tarea: suena un tono, agudo o grave, y aparece una flecha. Se responde
**al tono** con las flechas del teclado (arriba = agudo, abajo =
grave); la flecha de la pantalla no importa.

| Archivo | Qué hace |
|---|---|
| `precarga.psyexp` | Un componente Static `ISI` durante la fijación (1 s) carga la imagen del trial: en `imagen`, el campo Image dice **set during: trial.ISI** |
| `sin_precarga.psyexp` | Lo mismo sin Static: la imagen se carga al empezar cada trial (**set every repeat**, como viene por defecto) |

Los dos usan `condiciones.csv` y la carpeta `estimulos/`: dos imágenes
de 4000 × 3000 píxeles, como una foto de celular, y dos tonos `.wav`.
Se abren con **Builder → File → Open** y tienen que quedar en la misma
carpeta que esos archivos.

## Qué pasa sin precarga

Al empezar cada trial, el Builder carga todo lo que está en *set every
repeat*. Una foto de 4000 × 3000 tarda en decodificarse y pasar a la
placa de video: en una notebook del curso, unos 80 ms. Mientras tanto
la pantalla se congela con lo último que mostró (acá, la flecha del
trial anterior, que queda 80 ms más de lo que debería) y se pierde un
frame en cada trial.

Con precarga, esa carga pasa durante la fijación, que igual dura su
segundo exacto: el paso de un trial al siguiente tarda lo de siempre y
no se pierde nada. Medido en esa notebook, 20 trials:

| | Frames perdidos | De `New trial` a la cruz, en el `.log` |
|---|---|---|
| `precarga` | 0 | 14 ms |
| `sin_precarga` | 20, uno por trial | 82 ms |

## Cómo comprobarlo en su computadora

Corré los dos y compará:

- el total que se imprime al final, en la ventana del Runner: `Frames
  perdidos en todo el experimento`;
- en el CSV, la columna `frames_perdidos` de cada trial (la escribe el
  componente Code `control_frames`);
- en el `.log`, cuánto pasa entre la línea `New trial` y la línea
  `fijacion: autoDraw = True` del mismo trial.

## Cómo hacerlo en su experimento

1. En la rutina del trial, agregá un componente **Static** (Custom →
   Static) que dure lo mismo que la fijación o el intervalo antes del
   estímulo.
2. Recién ahí, en el desplegable del campo del archivo (Image o Movie)
   aparece **set during: trial.ISI**. Elegilo.
3. El estímulo tiene que empezar **después** de que termine el Static.
   Mientras dura, la pantalla queda quieta con lo que ya estaba.
4. Si la carga no entra en el Static, el `.log` dice `We overshot the
   intended duration`: alargá el Static o achicá las imágenes.

La otra mitad del remedio: guardar las imágenes al tamaño en que se
muestran. Una de 4000 × 3000 para mostrarla a 800 × 600 es puro peso.

## ¿Y el sonido?

En el Builder, el componente Sound carga su archivo **siempre** al
empezar la rutina, aunque le pongas *set during*: el Static no le
cambia nada. Un `.wav` corto carga en un par de milisegundos, así que
no suele hacer falta. Lo que importa en el sonido es otra cosa:

- **Sync start with screen**, tildado acá, para que arranque con el
  flip en que aparece la imagen;
- la latencia del parlante: la librería PTB y el modo *Latency/
  exclusivity mode* del dispositivo de audio (lo del demo de audio de
  la mañana).
