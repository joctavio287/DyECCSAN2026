# Qué reportar en Métodos

Checklist y plantillas para el día que publiquen. Se reparte al cierre
del curso y se menciona en el bloque 1 del día 2, cuando se habla de
timing.

**La regla que ordena todo:** reporten lo suficiente para que otro
laboratorio pueda **reconstruir** su experimento y **evaluar** si su
medición era lo bastante buena para el efecto que reportan.

---

## 1. La checklist

### Software — siempre

- [ ] **PsychoPy y su versión exacta** (ej. `2026.2.3`)
- [ ] Cita: Peirce et al. (2019)
- [ ] Builder o Coder (o ambos)
- [ ] Si fue online: Pavlovia / PsychoJS
- [ ] Sistema operativo y versión

### Hardware de presentación — siempre en laboratorio

- [ ] Modelo del monitor y **frecuencia de refresco en Hz**
- [ ] Resolución en píxeles
- [ ] Distancia del ojo a la pantalla, en cm
- [ ] Tamaño de los estímulos en **grados de ángulo visual**
- [ ] Si hubo audio: placa de sonido, auriculares o parlantes, y con
      qué se calibró el volumen

### Registro de respuestas — siempre

- [ ] Teclado, caja de botones, mouse o pantalla táctil
- [ ] Marca y modelo si es una caja de botones
- [ ] Qué teclas correspondían a qué respuesta

### Timing — siempre que el efecto dependa de él

- [ ] Duraciones **en frames y en ms**, no solo en ms
- [ ] Si se midió con hardware externo, cómo y con qué resultado
- [ ] Si se registraron frames perdidos, cuántos y qué se hizo con ellos

### Diseño

- [ ] Cantidad de condiciones, de trials por condición, de bloques
- [ ] Método de aleatorización (`random`, `fullRandom`, con
      restricciones)
- [ ] Cómo se contrabalanceó, y sobre qué
- [ ] Trials de práctica: cuántos, y si se descartaron
- [ ] Descansos: cada cuántos trials

### Preprocesamiento — el que más se omite

- [ ] Criterios de exclusión de **participantes**, con el n antes y
      después
- [ ] Criterios de exclusión de **trials** (umbrales de RT), con el
      porcentaje descartado
- [ ] Si se analizaron solo trials correctos
- [ ] Si los criterios estaban **preregistrados** o se decidieron
      después
- [ ] Qué estadístico se usó por celda: media, mediana, media
      recortada

### Disponibilidad — lo más barato que pueden hacer

- [ ] Link al experimento (repositorio de Pavlovia, OSF, GitHub)
- [ ] Link a los datos crudos
- [ ] Link al código de análisis

---

## 2. Plantilla para un experimento de laboratorio

> El experimento fue implementado en PsychoPy 2026.2.3 (Peirce et al.,
> 2019) usando la interfaz Builder, y ejecutado bajo Windows 11 en una
> computadora \[modelo]. Los estímulos se presentaron en un monitor
> \[modelo] de \[N] pulgadas, con una resolución de \[W×H] píxeles y
> una frecuencia de refresco de \[N] Hz, verificada al inicio de cada
> sesión. Lxs participantes se ubicaron a \[N] cm de la pantalla, con
> apoyo de mentón. Todas las duraciones de los estímulos se
> especificaron en frames; se informan también en milisegundos, para
> una frecuencia de refresco de \[N] Hz.
>
> Cada trial comenzó con una cruz de fijación central de \[N] frames
> (\[N] ms), seguida por \[el estímulo] durante \[N] frames (\[N] ms).
> Lxs participantes respondieron con las teclas \[X] e \[Y] de un
> \[teclado estándar / caja de botones \[modelo]]. Los tiempos de
> respuesta se midieron con la clase `Keyboard` de PsychoPy, basada en
> PsychToolbox.
>
> El diseño incluyó \[N] condiciones, con \[N] trials por condición,
> distribuidos en \[N] bloques presentados en orden \[contrabalanceado
> según un cuadrado latino / aleatorio]. El orden de los trials dentro
> de cada bloque fue aleatorio. Antes del experimento, lxs
> participantes completaron \[N] trials de práctica con feedback, que
> no se incluyeron en el análisis.
>
> Se excluyeron \[N] participantes por \[criterio], quedando un n final
> de \[N]. Del total de trials, se descartaron los incorrectos
> (\[N] %) y aquellos con tiempos de respuesta menores a \[N] ms o
> mayores a \[N] ms (\[N] % adicional). Estos criterios se
> establecieron \[antes de la recolección / de manera preregistrada,
> ver \[link]]. Para cada participante y condición se calculó la
> \[media / mediana] de los tiempos de respuesta de los trials
> restantes.
>
> El experimento, los datos crudos y el código de análisis están
> disponibles en \[link].

---

## 3. Plantilla para un experimento online

> El experimento fue implementado en PsychoPy 2026.2.3 (Peirce et al.,
> 2019), exportado a JavaScript mediante PsychoJS y alojado en Pavlovia
> (pavlovia.org). Lxs participantes accedieron desde sus propios
> dispositivos, a través de un enlace personalizado que incluía su
> código de participante.
>
> Los estímulos se especificaron en unidades relativas a la altura de
> la ventana, de modo que su tamaño relativo se mantuviera constante
> entre dispositivos. No fue posible controlar la distancia de
> visualización ni las características del monitor, por lo que los
> tamaños no se informan en grados de ángulo visual. Se \[excluyó / no
> se excluyó] el acceso desde dispositivos móviles.
>
> La precisión temporal de PsychoJS en navegadores fue evaluada por
> Bridges et al. (2020), quienes informaron una precisión en tiempos de
> respuesta por debajo de 3.5 ms en todas las combinaciones de
> navegador y sistema operativo evaluadas. Dado que el efecto esperado
> en el presente estudio es del orden de \[N] ms, esta precisión se
> consideró adecuada.
>
> \[Diseño, exclusiones y disponibilidad: igual que en la plantilla de
> laboratorio.]
>
> Se registraron \[N] sesiones, de las cuales \[N] estaban incompletas
> y fueron excluidas.

---

## 4. Frase para agregar si midieron el timing con hardware

> La sincronización entre la presentación de los estímulos y los
> registros \[de EEG] se verificó mediante un fotodiodo adosado a la
> pantalla, cuya señal se registró en un canal adicional. Sobre \[N]
> trials de prueba, el retraso medio entre el pulso de sincronización y
> la aparición efectiva del estímulo fue de \[N] ms (DE = \[N] ms).
> Este retraso constante fue corregido en el análisis.

**Si hacen esto, díganlo.** Es media hora de trabajo y les da una
respuesta sólida al revisor que pregunte por el timing — que en
neurociencia cognitiva pregunta siempre.

---

## 5. Los tres errores más frecuentes

**1. Reportar solo milisegundos.** "El estímulo se presentó durante
200 ms" es una intención, no una medición. Si el monitor era de 60 Hz,
200 ms no existe. Reporten frames **y** milisegundos.

**2. Omitir los criterios de exclusión, o el porcentaje descartado.**
Un artículo que dice "se excluyeron los outliers" no es reproducible.
Digan el umbral, el porcentaje y cuándo se decidió.

**3. No reportar la versión del software.** PsychoPy cambia entre
versiones; sin ese dato, su experimento no se puede reconstruir. Es una
palabra y falta en la mitad de los papers.

---

## 6. Cómo citar

> Peirce, J., Gray, J. R., Simpson, S., MacAskill, M., Höchenberger, R.,
> Sogo, H., Kastman, E., & Lindeløv, J. K. (2019). PsychoPy2:
> Experiments in behavior made easy. *Behavior Research Methods*, 51(1),
> 195–203. <https://doi.org/10.3758/s13428-018-01193-y>

Para respaldar afirmaciones sobre precisión temporal:

> Bridges, D., Pitiot, A., MacAskill, M. R., & Peirce, J. W. (2020).
> The timing mega-study: comparing a range of experiment generators,
> both lab-based and online. *PeerJ*, 8, e9414.
> <https://doi.org/10.7717/peerj.9414>

Más referencias en [`04_recursero.md`](04_recursero.md).
