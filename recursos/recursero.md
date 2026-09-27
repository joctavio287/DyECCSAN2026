# Recursero

Todo lo que hay que tener a mano: papers para citar, referencias sobre
timing, dónde bajar paradigmas ya hechos, videos y documentación.

---

## 1. Papers para citar

### Los de PsychoPy (van en Métodos)

**El que se cita hoy:**

> Peirce, J., Gray, J. R., Simpson, S., MacAskill, M., Höchenberger, R.,
> Sogo, H., Kastman, E., & Lindeløv, J. K. (2019). PsychoPy2:
> Experiments in behavior made easy. *Behavior Research Methods*, 51(1),
> 195–203. <https://doi.org/10.3758/s13428-018-01193-y>

Los dos originales, por si necesitan la historia o citan la versión 1:

> Peirce, J. W. (2007). PsychoPy — Psychophysics software in Python.
> *Journal of Neuroscience Methods*, 162(1–2), 8–13.
> <https://doi.org/10.1016/j.jneumeth.2006.11.017>

> Peirce, J. W. (2009). Generating stimuli for neuroscience using
> PsychoPy. *Frontiers in Neuroinformatics*, 2, 10.
> <https://doi.org/10.3389/neuro.11.010.2008>

**Cómo redactarlo en el paper** (plantilla para dar en clase):

> El experimento fue implementado en PsychoPy 2026.2.3 (Peirce et al.,
> 2019) y ejecutado en \[SO y versión] sobre un monitor de \[modelo] a
> \[N] Hz, con resolución de \[WxH] px. Las duraciones de los estímulos
> se especificaron en frames. Las respuestas se registraron con
> \[teclado / caja de botones]. \[Para online: los datos se recolectaron
> a través de Pavlovia (PsychoJS).]

---

### El de timing (el que responde a los revisores)

> **Bridges, D., Pitiot, A., MacAskill, M. R., & Peirce, J. W. (2020).
> The timing mega-study: comparing a range of experiment generators,
> both lab-based and online. *PeerJ*, 8, e9414.**
> <https://doi.org/10.7717/peerj.9414> · [PDF abierto](https://peerj.com/articles/9414.pdf)

Los tres números para tener memorizados:

- En laboratorio, Psychtoolbox, PsychoPy, Presentation y E-Prime dieron
  **precisión media por debajo de 1 ms** en visual, audio y respuesta.
- Online hay más variabilidad en todas las medidas; **PsychoPy/PsychoJS
  y Gorilla** fueron los mejores, cerca del milisegundo en varias
  combinaciones navegador/SO.
- En tiempos de respuesta online, la mayoría de los paquetes quedó
  **por debajo de 10 ms**; **PsychoPy por debajo de 3.5 ms en todos los
  navegadores probados**.

---

### Timing online (si el proyecto va al navegador)

> Anwyl-Irvine, A., Dalmaijer, E. S., Hodges, N., & Evershed, J. K.
> (2021). Realistic precision and accuracy of online experiment
> platforms, web browsers, and devices. *Behavior Research Methods*,
> 53(4), 1407–1425. <https://doi.org/10.3758/s13428-020-01501-5>

> Pronk, T., Wiers, R. W., Molenkamp, B., & Murre, J. (2020). Mental
> chronometry in the pocket? Timing accuracy of web applications on
> touchscreen and keyboard devices. *Behavior Research Methods*, 52(3),
> 1371–1382. <https://doi.org/10.3758/s13428-019-01321-2>
> — El de referencia para celulares y pantallas táctiles.

> Reimers, S., & Stewart, N. (2015). Presentation and response timing
> accuracy in Adobe Flash and HTML5/JavaScript Web experiments.
> *Behavior Research Methods*, 47(2), 309–327.
> <https://doi.org/10.3758/s13428-014-0471-1>

> de Leeuw, J. R., & Motz, B. A. (2016). Psychophysics in a Web
> browser? Comparing response times collected with JavaScript and
> Psychophysics Toolbox in a visual search task. *Behavior Research
> Methods*, 48(1), 1–12.
> <https://doi.org/10.3758/s13428-015-0567-2>

> Sauter, M., Draschkow, D., & Mack, W. (2020). Building, hosting and
> recruiting: A brief introduction to running behavioral experiments
> online. *Brain Sciences*, 10(4), 251.
> <https://doi.org/10.3390/brainsci10040251>
> — Panorama práctico, bueno para recomendarle a alguien que arranca.

---

### Timing en laboratorio: el marco conceptual

> Plant, R. R., & Turner, G. (2009). Millisecond precision
> psychological research in a world of commodity computers: New hardware,
> new problems? *Behavior Research Methods*, 41(3), 598–614.
> <https://doi.org/10.3758/BRM.41.3.598>

> Plant, R. R. (2016). A reminder on millisecond timing accuracy and
> potential replication failure in computer-based psychology
> experiments: An open letter. *Behavior Research Methods*, 48(1),
> 408–411. <https://doi.org/10.3758/s13428-015-0577-0>
> — Corto, contundente, ideal para hacer leer. Argumenta que parte de
> la crisis de replicación es error de medición, no de estadística.

> Garaizar, P., Vadillo, M. A., & López-de-Ipiña, D. (2014). Presentation
> accuracy of the web revisited: Animation methods in the HTML5 era.
> *PLOS ONE*, 9(10), e109812.
> <https://doi.org/10.1371/journal.pone.0109812>

---

### Sobre la tarea Stroop (por si preguntan)

> Stroop, J. R. (1935). Studies of interference in serial verbal
> reactions. *Journal of Experimental Psychology*, 18(6), 643–662.
> <https://doi.org/10.1037/h0054651>

> MacLeod, C. M. (1991). Half a century of research on the Stroop
> effect: An integrative review. *Psychological Bulletin*, 109(2),
> 163–203. <https://doi.org/10.1037/0033-2909.109.2.163>
> — La revisión canónica. Ahí está el rango de efectos esperables.

---

## 2. Documentación de timing en PsychoPy

Todo colgado de <https://psychopy.org/general/timing/>:

| Página | Para qué |
|---|---|
| [Can PsychoPy deliver millisecond precision?](https://psychopy.org/general/timing/millisecondPrecision.html) | La página madre: monitores, SO, teclados, audio |
| [Detecting dropped frames](https://psychopy.org/general/timing/detectingFrameDrops.html) | Cómo saber si se perdieron frames |
| [Reducing dropped frames](https://psychopy.org/general/timing/reducingFrameDrops.html) | Qué hacer al respecto |
| [Non-slip timing](https://psychopy.org/general/timing/nonSlipTiming.html) | Sincronización con fMRI |
| [Comparing OS under PsychoPy](https://psychopy.org/general/timing/timingTestByOS.html) | Windows vs macOS vs Linux |

Números concretos que salen de ahí y sirven para la clase:

- Monitor a 60 Hz → frame de **16.7 ms**; los píxeles de abajo se
  dibujan hasta **10 ms** después que los de arriba.
- Teclado: **4–25 ms** de latencia según plataforma y modelo.
- macOS 10.13+: estímulos con un frame (**16.66 ms**) de retraso.
- Monitores con post-procesado: **20–30 ms** de lag variable.
- Audio: pygame ~**100 ms**; PsychPortAudio (PTB), sub-milisegundo.

---

## 3. Hardware, marcas y sincronización

Lo del bloque de sincronización y hardware del día 2, y para seguir
después.

### Documentación de PsychoPy

| Tema | Link |
|---|---|
| Puerto paralelo | <https://psychopy.org/api/parallel.html> |
| Puerto serie | <https://psychopy.org/api/serial.html> |
| ioHub y eyetracking | <https://psychopy.org/api/iohub/index.html> |
| Non-slip timing para fMRI | <https://psychopy.org/general/timing/nonSlipTiming.html> |
| Componentes de hardware en Builder | <https://psychopy.org/builder/components/index.html> |

### Dispositivos de marcas

| Tipo | Ejemplos | Nota |
|---|---|---|
| USB-TTL comercial | LabHackers USB2TTL8, Black Box ToolKit USB TTL Module, Cedrus StimTracker | Aislación y latencia especificadas |
| Casero | Arduino Leonardo o Micro | Sketch `arduino_usb2ttl.ino`, en los materiales del día 2 |
| Cajas de botones | Cedrus RB-x40, BBTK, LabHackers | Reloj propio, resuelven la latencia del teclado |
| Validación | Black Box ToolKit, fotodiodo + osciloscopio USB | Digilent Analog Discovery, PicoScope 2000, Hantek 6022BE |

> Verificar disponibilidad y precios: los modelos cambian. El combo
> **Arduino Leonardo + osciloscopio USB + fotodiodo casero** hace el
> demo completo y es el que lxs asistentes pueden replicar.

### Lab Streaming Layer

- Proyecto: <https://labstreaminglayer.readthedocs.io/>
- App para grabar varios streams: LabRecorder
- Integración con PsychoPy: <https://psychopy.org/api/liaison.html>

### Leer y analizar el archivo del EEG

- **MNE-Python** — <https://mne.tools/> · el estándar abierto para
  EEG/MEG en Python. Leer el canal de triggers y segmentar son dos
  funciones: `mne.find_events()` y `mne.Epochs()`.
- Tutorial de eventos y anotaciones:
  <https://mne.tools/stable/auto_tutorials/intro/20_events_from_raw.html>

### Sobre validar la sincronización

> Plant, R. R., & Turner, G. (2009). Millisecond precision
> psychological research in a world of commodity computers.
> *Behavior Research Methods*, 41(3), 598–614.
> — Ya está citado arriba; acá es la referencia de por qué hay que
> medir el setup con hardware externo en vez de confiar en el reloj.

---

## 4. Dónde correr un experimento online

Lo del bloque «Del laboratorio al navegador», y todo lo que no entró
en esa hora.

### datapruebas.org — la plataforma del laboratorio

> **<https://datapruebas.org/>**

Plataforma desarrollada en nuestro propio laboratorio para hospedar
experimentos online. **Frente a pedidos concretos puede hacerse
compatible con experimentos de PsychoPy.**

Para quién tiene sentido:

- Proyectos que quieran evitar el esquema de créditos de Pavlovia.
- Grupos que necesiten mantener los datos en infraestructura propia,
  por razones institucionales o de comité de ética.
- Cualquiera del curso que esté armando algo online y quiera consultar
  si su caso encaja.

La vía es escribirle a los docentes; no es un servicio de
autoservicio como Pavlovia.

### Pavlovia

- Plataforma: <https://pavlovia.org/>
- Documentación oficial: <https://psychopy.org/online/index.html>
- Repositorios: <https://gitlab.pavlovia.org/>

Lo que quedó fuera del curso y está documentado acá:

| Tema | Dónde |
|---|---|
| Debugging online, los tres tipos de error | [Workshop, día 2](https://workshops.psychopy.org/3days/day2.html) |
| Traducción Python → JavaScript y qué no cruza | <https://psychopy.org/online/psychoJSCodingDifferences.html> |
| GitLab: versiones y hacer público un experimento | <https://psychopy.org/online/usingGitLab.html> |
| Contrabalanceo online y *the Shelf* | <https://psychopy.org/online/shelf.html> |
| Cadenas de consulta en la URL | <https://psychopy.org/online/onlineParticipants.html> |

**Lo mínimo para arrancar solo:** sincronizar, poner en *piloting* para
probar, pasar a *running* para recolectar, y acordarse de que en
*piloting* **no se guardan datos**. Con eso y el video de Jason Geller
del recursero de video, alcanza.

---

## 5. Paradigmas ya implementados

### Lo primero: los que ya tienen instalados

**PsychoPy → menú Demos.** Vienen con el programa, no hay que bajar
nada. Incluye Stroop, Posner, N-back, sperling, psicofísica con
escaleras, eyetracking y bastante más. **Es el primer lugar a mirar y
el que todos ignoran.**

### Colecciones online

| Recurso | Qué tiene | Link |
|---|---|---|
| **Pavlovia Explore** | Cientos de experimentos públicos, filtrables. Se puede *forkear* y correr | <https://pavlovia.org/explore> |
| **Pavlovia Demos** | Los demos oficiales, ya listos para online | <https://pavlovia.org/explore/demos> · <https://gitlab.pavlovia.org/demos> |
| **Experiment Recipe Book** | Recetas del equipo de PsychoPy: contadores, feedback, escaleras, contrabalanceo | <https://workshops.psychopy.org/tutorials/index.html> |
| **Demos en el repo fuente** | Carpeta `psychopy/demos` del código fuente | <https://github.com/psychopy/psychopy> |
| **Temple Coding Outreach** | Curso completo con materiales de Builder | <https://github.com/TU-Coding-Outreach-Group/cog_summer_workshops_2021/tree/main/psychopy> |
| **VESPR (Morys-Carter)** | Recursos, plantillas y utilidades para PsychoPy/Pavlovia | <https://moryscarter.com/vespr/psychopy.php> |
| **OSF** | Buscar el paper, después buscar el material. Muchos suben el `.psyexp` | <https://osf.io/search> |

**Cómo forkear un demo de Pavlovia** (para mostrar en clase):
entrar a <https://pavlovia.org/explore>, abrir el experimento, botón
*Fork*, y después sincronizarlo desde el Builder como si fuera propio.

### Fuera de PsychoPy, útiles como referencia de diseño

- **PsyToolkit** — biblioteca de tareas clásicas con la descripción del
  procedimiento y sus referencias: <https://www.psytoolkit.org/experiment-library/>
- **Millisecond Task Library** — implementaciones en Inquisit (paga),
  pero cada tarea documenta parámetros y citas:
  <https://www.millisecond.com/download/library>
- **jsPsych demos** — <https://www.jspsych.org/latest/demos/>

> Nota para dar en clase: aunque terminen implementando la tarea desde
> cero, mirar dos o tres implementaciones existentes antes de arrancar
> ahorra semanas. Los parámetros (duraciones, ISI, cantidad de trials)
> ya fueron discutidos por alguien.

---

## 6. Video

### Canal oficial

**PsychoPy en YouTube:** <https://www.youtube.com/c/officialpsy/playlists>

- [Playlist oficial de tutoriales](https://www.youtube.com/playlist?list=PLFB5A1BE51964D587)
- [PsychoPy Tutorials](https://www.youtube.com/playlist?list=PLerfwwRppg_XyC-wJIXhgU_0LGfx5xnDX)
- [PsychoPy Mini-Tutorials](https://www.youtube.com/playlist?list=PL6PJquR5BWXmj2y_niC5TdoXx9ABS19yO)

### Las mejores series de terceros

Todas recomendadas por la propia documentación de PsychoPy
(<https://psychopy.org/teaching/>):

| Serie | Enfoque | Link |
|---|---|---|
| **Jason Ozubko** — Builder | La mejor para empezar de cero con la interfaz | [playlist](https://www.youtube.com/playlist?list=PL6PJquR5BWXllUt585cRJWcRTly55iXTm) |
| **Damien Mannion** — Coder | Programar experimentos en Python, más técnica | [playlist](https://www.youtube.com/playlist?list=PLuqBA9VDSXk7Z06RtJ6Gh6Y5YznVrFrK6) |
| **Holly Sullivan-Toole** — Getting started con Pavlovia | Video único, buen resumen de arranque | [video](https://www.youtube.com/watch?v=0a05xCc6X8s) |
| **Jason Geller** — Pavlovia | Integración con Pavlovia paso a paso | [video](https://youtu.be/SAbKAz4M-Rg) |

**Recomendación para los asistentes:** si un solo link se van a
guardar, que sea la serie de **Ozubko** para Builder y la de
**Mannion** para Coder.

---

## 7. Documentación y comunidad

| Recurso | Link |
|---|---|
| Documentación oficial | <https://psychopy.org/> |
| Foro (donde se contesta todo) | <https://discourse.psychopy.org/> |
| Workshops oficiales | <https://workshops.psychopy.org/> |
| Workshop de 3 días (base de este curso) | <https://workshops.psychopy.org/3days/> |
| Recursos de enseñanza | <https://psychopy.org/teaching/> |
| Código fuente / issues | <https://github.com/psychopy/psychopy> |
| Pavlovia | <https://pavlovia.org/> |

**Sobre el foro:** antes de preguntar, buscar — la respuesta ya está el
90 % de las veces. Cuando pregunten, incluir versión de PsychoPy, SO,
el error completo, y un archivo mínimo que reproduzca el problema.

---

## 8. Libros

> Peirce, J., Hirst, R., & MacAskill, M. (2022). *Building Experiments
> in PsychoPy* (2ª ed.). SAGE.
> <https://us.sagepub.com/en-us/nam/building-experiments-in-psychopy/book273700>

Escrito por el creador de PsychoPy. Es el libro de referencia y sigue
la misma lógica que el workshop: Builder primero, código después.

> Bertamini, M. (2017). *Programming Illusions for Everyone*. Springer.

Menos manual y más divertido: ilusiones visuales implementadas en
PsychoPy. Buen regalo para quien quiere seguir jugando.

---

## 9. Cursos completos en línea

| Curso | Enfoque |
|---|---|
| [Jonas Lindeløv — PsychoPy course](https://lindeloev.net/psychopy-course/) | Curso completo, de los más citados |
| [Lukas Snoek — introPy](https://lukas-snoek.com/introPy/) | Python + PsychoPy desde cero, con notebooks |
| [Damien Mannion — Psychology programming](https://www.djmannion.net/psych_programming/vision/intro/intro.html) | Visión y psicofísica en Python |
| [Gary Lupyan — Programming for Psychologists](http://sapir.psych.wisc.edu/programming_for_psychologists/) | Curso universitario completo |
| [Nottingham — PsychoPy basics](https://psychology.nottingham.ac.uk/staff/lpzjd/psgy1001-21/psychopy-basics.html) | Prácticas de grado, muy graduales |

---

## 10. Análisis de datos conductuales

- **pandas** — <https://pandas.pydata.org/docs/user_guide/10min.html>
  (los "10 minutes to pandas" alcanzan para el 80 % del curso)
- **seaborn** — <https://seaborn.pydata.org/tutorial.html> (gráficos
  estadísticos con una línea)
- **pingouin** — <https://pingouin-stats.org/> (tests clásicos con
  salida legible; más amable que scipy para ANOVA y t-tests)
- **statsmodels** — <https://www.statsmodels.org/> (modelos mixtos,
  que es a dónde va cualquier análisis de RT serio)

Nota metodológica para mencionar en clase: los tiempos de respuesta no
son normales (tienen cola derecha). Para análisis serios, mirar
modelos mixtos con familia gamma o inversa gaussiana, o transformar.
Para la clase, la media por participante alcanza.
