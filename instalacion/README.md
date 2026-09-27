# Guía de instalación de PsychoPy

Esto hay que hacerlo ANTES del primer día. No alcanza con "descargarlo
el lunes a la mañana": en Mac y Linux hay permisos del sistema que
tardan y que, si no están, hacen que el experimento no registre teclas.

## Versión de referencia del curso

| | |
|---|---|
| Versión | PsychoPy Standalone 2026.2.3 (canal *Stable*) |
| Python | 3.10 (viene incluido en el Standalone) |
| Descarga | <https://www.psychopy.org/download.html> |

Dos aclaraciones que evitan el 80 % de los problemas:

- **Todxs la misma versión.** Como veremos, los archivos `.psyexp`
  guardan con qué versión se hicieron los experimentos; si cada uno
  tiene una distinta, los ejercicios compartidos pueden romperse en
  formas que son difíciles de gestionar. Si cuando leen esto la web ya
  ofrece una versión más nueva, traten de usar la de referencia de
  todos modos, no la última.
- **Bajar "Standalone", no "Studio".** PsychoPy Studio es la interfaz
  nueva y todavía está marcada como Beta. Es tentadora porque es más
  linda y en Linux se instala mucho más fácil, pero para dar clase
  queremos el camino probado y soportado por Psychopy. Excepción: ver
  la sección de Linux.

Si, por algún motivo, se les complica instalar la versión Standalone y
quieren hacer una instalación manual, pueden pedirnos ayuda (más abajo
dejamos detalles del canal de comunicación que usaremos).

## Windows

### Instalación

- Bajar el instalador `.exe` de PsychoPy Standalone 2026.2.3 desde la
  página de descargas.
- Ejecutarlo. Si Windows muestra "Windows protegió su PC", hacer clic
  en Más información → Ejecutar de todas formas. Instalar para todos
  los usuarios si tienen permisos de administrador; si no, la
  instalación por usuario también sirve. Aceptar la ruta por defecto.

### Detalles que pueden romperse en Windows

- **No trabajar dentro de OneDrive / Google Drive / Dropbox.** La
  sincronización toca los archivos mientras el experimento corre y
  produce errores al guardar datos. Crear una carpeta local, por
  ejemplo `C:\psychopy_curso\`. Una vez cerrado el diseño se puede
  mover la carpeta entera.
- **Evitar tildes y espacios en la ruta.**
  `C:\Users\María José\Mis documentos\` traerá problemas en la lectura
  de archivos una vez dentro de Psychopy. La versión más amigable sería
  `C:\Users\MariaJose\Documentos\`.
- **Antivirus.** Algunos (Avast, McAfee) bloquean la ventana en
  pantalla completa. Si la ventana no abre, agregar la carpeta de
  PsychoPy a las excepciones.

## macOS

### Instalación

- Bajar el `.dmg` de PsychoPy Standalone 2026.2.3. Elegir la build
  arm64 si tienen Apple Silicon (M1/M2/M3/M4) o la Intel si la Mac es
  de 2019 o anterior. Si no saben:  → Acerca de esta Mac.
- Arrastrar PsychoPy a Aplicaciones. La primera vez no abrirlo con
  doble clic: clic derecho → Abrir → Abrir. Si dice "PsychoPy está
  dañado y no se puede abrir", ejecutar en la Terminal:
  `xattr -cr /Applications/PsychoPy.app`

### Instalación alternativa Homebrew

- En la terminal correr: `brew install --cask psychopy`

### Detalles que pueden romperse en macOS

- **No trabajar dentro de OneDrive / Google Drive / Dropbox.** La
  sincronización toca los archivos mientras el experimento corre y
  produce errores al guardar datos. Crear una carpeta local, por
  ejemplo `~/psychopy_curso/`. Una vez cerrado el diseño se puede mover
  la carpeta entera.
- **Evitar tildes y espacios en la ruta.**
  `/Users/María José/Mis documentos/` traerá problemas en la lectura de
  archivos una vez dentro de Psychopy. La versión más amigable sería
  `/Users/MariaJose/Documentos/`.
- **Permisos del sistema.** Ir a Ajustes del Sistema → Privacidad y
  seguridad y agregar `PsychoPy.app` en:
  - Monitorización de entrada (Input Monitoring) → sin esto no se
    registran las teclas y todos los tiempos de respuesta salen vacíos.
  - Grabación de pantalla (Screen Recording) → necesario para la
    ventana en pantalla completa.
  - Accesibilidad (Accessibility).
- Después de darle los permisos, cerrar y volver a abrir PsychoPy.

## Linux

En Linux no hay un `.exe` que resuelva todo: wxPython (la librería de
la interfaz gráfica) tiene soporte pobre en Linux y es la fuente de
casi todos los dolores. Hay tres caminos, de más fácil a más control:

### Opción A — Instalador de la comunidad (recomendada)

Script mantenido que detecta la distro, instala las dependencias del
sistema, arma el entorno de Python y resuelve wxPython:

```bash
bash <(curl -LsSf https://github.com/wieluk/psychopy_linux_installer/releases/latest/download/psychopy_linux_installer) --gui --psychopy-version=2026.2.3
```

Probado en Ubuntu 20.04/22.04/24.04, Debian 11/12/13, Fedora 39/40/41,
Rocky/CentOS 9, Pop!_OS, Mint, openSUSE y Manjaro.
Repo: <https://github.com/wieluk/psychopy_linux_installer>

Dos advertencias sobre este camino. La opción `--gui` necesita tener
zenity instalado; si no lo tienen, corran el mismo comando sin `--gui`
y el instalador va por consola. Y si el script pregunta por la versión
de Python, la respuesta es **3.10**, que es la que trae el Standalone y
la que el instalador usa por defecto. Si algo falla igual, no insistan:
pasen a la Opción B y avísennos.

### Opción B — PsychoPy Studio

Es la única situación donde la versión Beta se justifica: en Linux es
mucho más fácil de instalar porque no depende de wxPython. Si la opción
A falla y no quieren pelearse, esta sirve para seguir la clase.

### Opción C — pip en un environment

Háblenos si quieren ir por este camino.

## Verificación

En el Classroom del curso dejamos un archivo de prueba,
`verificacion.psyexp`. Es lo más simple posible: abre una ventana en
pantalla completa, muestra la palabra FUNCIONA y se cierra con
cualquier tecla. No es el experimento del curso, ese lo vamos a
construir juntos el primer día.

- **Bajar `verificacion.psyexp`** del Classroom y guardarlo en la
  carpeta de trabajo que crearon antes.
- **Abrir PsychoPy.** Se abren dos ventanas: Builder, donde se arman
  los experimentos, y Runner, donde se corren y donde aparecen los
  errores.
- **En Builder: File → Open** y elegir `verificacion.psyexp`.
- **Apretar el botón verde de Ejecutar.** Es el triángulo verde del
  grupo Desktop. Ojo con el interruptor Pilot / Run que está a la
  izquierda: tiene que estar en **Run**. En modo *Pilot* el experimento
  corre en una ventana chica y no prueba la pantalla completa, que es
  justamente una de las cosas que queremos verificar. La primera vez
  puede tardar unos segundos.
- **Tiene que aparecer FUNCIONA** en pantalla completa. Apretar
  cualquier tecla para salir.

Con eso sabemos las tres cosas que nos importan antes de la clase: que
PsychoPy abre, que puede tomar la pantalla completa y que registra el
teclado. Son justamente las que fallan por antivirus en Windows y por
permisos en macOS.

Si al abrir el archivo PsychoPy avisa que se hizo con otra versión,
avísennos: significa que la instalada no es la de referencia, y es
justo lo que queremos detectar ahora y no el primer día.

## Si tienen inconvenientes o algo falla

El canal de comunicación del curso es Google Classroom:
<https://classroom.google.com/c/ODg0MzY5NTY5ODE0>. Ahí van a estar los
materiales, el archivo de verificación y el espacio para hacer
preguntas. Conviene entrar y anotarse antes del primer día.

Escribirnos por el Classroom del curso, en un solo mensaje, con estos
cuatro datos:

- Sistema operativo y versión.
- Versión de PsychoPy que están tratando de instalar.
- Captura de pantalla del error completo, o el texto de la ventana
  Runner de PsychoPy (se copia y pega).
- Qué estaban haciendo cuando falló.

Foros oficiales, por si quieren buscar antes:
<https://discourse.psychopy.org/>
