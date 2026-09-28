"""
El puerto por el que salen las marcas, compartido por los dos demos.

`TriggerPort` expone la misma interfaz para todos los backends, así el
experimento no sabe —ni necesita saber— por dónde sale la marca:

- ``"simulado"``: no toca ningún cable, solo escribe en el log.
- ``"serial"``: un pincho USB-TTL, un Arduino o una caja de triggers por
  puerto serie.
- ``"parallel"``: puerto paralelo.

Con ``"serial"`` hay dos maneras de marcar, que elige `serial_signal`:

- ``"byte"``: se escribe un byte. En una caja de triggers o en el
  Arduino sale por ocho cables; en un pincho USB-TTL genérico sale como
  una trama serie por TX, y la marca es el flanco de bajada del bit de
  arranque.
- ``"break"``, ``"dtr"`` o ``"rts"``: se mantiene una línea del pincho
  en bajo desde `send` hasta `release`. Sirve para prender un LED
  mientras dura el estímulo: ``"break"`` usa TX, que tienen todos los
  pinchos; ``"dtr"`` y ``"rts"``, los pines con esos nombres si el
  pincho los tiene.
"""

from __future__ import annotations

from psychopy import core, logging

VALID_BACKENDS = ("simulado", "serial", "parallel")
VALID_SERIAL_SIGNALS = ("byte", "break", "dtr", "rts")


class TriggerPort:
    """
    Envía marcas por el puerto que haya disponible.

    Parameters
    ----------
    backend : str
        `"simulado"`, `"serial"` o `"parallel"`.
    address : str | int
        Nombre del puerto serie (`"COM3"`, `"/dev/ttyUSB0"`) o dirección
        del puerto paralelo (`0x0378`). Se ignora en modo simulado.
    baudrate : int
        Velocidad del puerto serie, en baudios.
    serial_signal : str
        `"byte"`, `"break"`, `"dtr"` o `"rts"`. Solo cuenta con
        `backend="serial"`.
    pulse_duration : float
        Cuánto se mantiene alto el puerto paralelo antes de bajarlo, en
        segundos.

    Raises
    ------
    ValueError
        Si `backend` o `serial_signal` no son valores admitidos.
    """

    def __init__(
        self,
        backend: str,
        address: str | int,
        baudrate: int,
        serial_signal: str,
        pulse_duration: float,
    ) -> None:
        if backend not in VALID_BACKENDS:
            raise ValueError(
                f"backend '{backend}' desconocido, usar uno de "
                f"{VALID_BACKENDS}"
            )
        if serial_signal not in VALID_SERIAL_SIGNALS:
            raise ValueError(
                f"serial_signal '{serial_signal}' desconocido, usar uno "
                f"de {VALID_SERIAL_SIGNALS}"
            )
        self.backend = backend
        self.serial_signal = serial_signal
        self.pulse_duration = pulse_duration
        self._device = self._open(address, baudrate)

    def _open(self, address: str | int, baudrate: int):
        """
        Abre el dispositivo correspondiente al backend elegido.

        Parameters
        ----------
        address : str | int
            Puerto serie o dirección del puerto paralelo.
        baudrate : int
            Velocidad del puerto serie, en baudios.

        Returns
        -------
        object | None
            El objeto del dispositivo, o `None` en modo simulado.
        """
        if self.backend == "serial":
            import serial

            device = serial.Serial()
            device.port = address
            device.baudrate = baudrate
            device.dtr = False
            device.rts = False
            device.open()
            return device

        if self.backend == "parallel":
            from psychopy import parallel

            parallel.setPortAddress(address)
            return parallel

        print("Modo simulado: las marcas van al log, no a ningún cable.")
        return None

    def send(self, code: int) -> float:
        """
        Manda una marca y devuelve el instante en que salió.

        Parameters
        ----------
        code : int
            Valor de 0 a 255 que identifica el evento. Con las señales
            de línea (`"break"`, `"dtr"`, `"rts"`) solo va al log.

        Returns
        -------
        float
            Marca de tiempo del reloj de PsychoPy, tomada
            inmediatamente después de escribir en el puerto.
        """
        if self.backend == "serial":
            self._set_serial_line(True, code)
        elif self.backend == "parallel":
            self._device.setData(code)

        sent_at = core.getTime()
        logging.data(f"TRIGGER {code} en t={sent_at:.6f}")

        if self.backend == "parallel":
            core.wait(self.pulse_duration)
            self._device.setData(0)
        return sent_at

    def release(self) -> None:
        """
        Suelta la línea, si la marca es una línea sostenida.

        Con las señales `"break"`, `"dtr"` y `"rts"` la línea queda en
        bajo desde `send` hasta acá. Con los demás casos no hace nada:
        el byte serie y el pulso paralelo vuelven a reposo solos.
        """
        if self.backend == "serial":
            self._set_serial_line(False)

    def close(self) -> None:
        """
        Deja la línea en reposo y cierra el puerto.
        """
        if self.backend == "serial":
            self._set_serial_line(False)
            self._device.close()
        elif self.backend == "parallel":
            self._device.setData(0)

    def _set_serial_line(self, active: bool, code: int = 0) -> None:
        """
        Activa o suelta la marca en el puerto serie.

        Parameters
        ----------
        active : bool
            `True` para marcar, `False` para volver a reposo.
        code : int, opcional
            Byte a escribir con la señal `"byte"`, por defecto 0.
        """
        if self.serial_signal == "byte":
            if active:
                self._device.write(bytes([code]))
        elif self.serial_signal == "break":
            self._device.break_condition = active
        elif self.serial_signal == "dtr":
            self._device.dtr = active
        else:
            self._device.rts = active
