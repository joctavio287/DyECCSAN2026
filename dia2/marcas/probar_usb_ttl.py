"""
Prueba rápida de un pincho USB-TTL con el osciloscopio, sin PsychoPy.

Manda una tanda de marcas por el puerto serie, una cada `INTERVAL`
segundos. `SIGNAL` elige cómo:

- ``"byte"``: escribe `PULSE_BYTE`. En la línea TX de un pincho
  genérico (CH340, CP2102, FTDI) cada byte sale como una trama serie:
  la línea está en alto en reposo y baja durante el bit de arranque.
  Con `0x00` queda en bajo nueve bits seguidos: ~0.94 ms a 9600
  baudios, ~30 ms a 300.
- ``"break"``: mantiene TX en bajo durante `PULSE_DURATION`. Es lo que
  hace falta para que un LED se vea prendido.
- ``"dtr"`` o ``"rts"``: lo mismo, en el pin con ese nombre, si el
  pincho lo tiene.

En todos los casos la marca es un **flanco de bajada**. Un LED que se
prende con la marca va entre VCC y la línea: VCC → resistencia → pata
larga del LED → pata corta → TX (o DTR, o RTS).

Solo necesita `pyserial`, que viene con PsychoPy. Se corre desde la
ventana Coder (botón Ejecutar) o desde una terminal::

    python probar_usb_ttl.py

Con `DRY_RUN = True` usa un puerto de loopback de `pyserial` y no hace
falta ningún hardware.
"""

from __future__ import annotations

import time

import serial
from serial.tools import list_ports

SERIAL_PORT = None
SIGNAL = "break"
BAUDRATE = 9600
PULSE_BYTE = 0x00
PULSE_DURATION = 0.2
N_PULSES = 20
INTERVAL = 0.8
DRY_RUN = False

VALID_SIGNALS = ("byte", "break", "dtr", "rts")


def list_usb_serial_ports() -> list[str]:
    """
    Imprime los puertos serie que ve el sistema y devuelve los USB.

    Returns
    -------
    list[str]
        Nombres de los puertos que son dispositivos USB, por ejemplo
        `"COM3"` o `"/dev/ttyUSB0"`. Los puertos serie internos de la
        placa madre se listan pero no se devuelven.
    """
    ports = sorted(list_ports.comports(), key=lambda port: port.device)
    print("Puertos serie disponibles:")
    for port in ports:
        kind = "USB" if port.vid is not None else "   "
        print(f"  {kind} {port.device:<16} {port.description}")
    if not ports:
        print("  (ninguno)")
    return [port.device for port in ports if port.vid is not None]


def choose_port(requested: str | None, usb_ports: list[str]) -> str:
    """
    Decide qué puerto abrir.

    Parameters
    ----------
    requested : str | None
        Puerto pedido explícitamente en `SERIAL_PORT`. Si es `None`, se
        usa el único puerto USB conectado.
    usb_ports : list[str]
        Puertos devueltos por `list_usb_serial_ports`.

    Returns
    -------
    str
        Nombre del puerto a abrir.

    Raises
    ------
    SystemExit
        Si no se pidió un puerto y no hay exactamente un puerto USB.
    """
    if requested is not None:
        return requested
    if len(usb_ports) == 1:
        return usb_ports[0]
    raise SystemExit(
        "\nNo sé qué puerto usar: poné el nombre en SERIAL_PORT, arriba "
        "de este archivo.\nSi el pincho no aparece como USB, probá otro "
        "cable o puerto (y en Linux, el grupo 'dialout')."
    )


def open_port(
    port_name: str,
    baudrate: int,
    dry_run: bool,
) -> serial.Serial:
    """
    Abre el puerto serie con DTR y RTS en reposo.

    Parameters
    ----------
    port_name : str
        Nombre del dispositivo. Se ignora si `dry_run` es `True`.
    baudrate : int
        Velocidad en baudios. Con `SIGNAL = "byte"` define el ancho del
        pulso: 10 bits por byte.
    dry_run : bool
        Si es `True`, no toca ningún hardware.

    Returns
    -------
    serial.Serial
        El puerto abierto.
    """
    if dry_run:
        return serial.serial_for_url("loop://", baudrate=baudrate)
    port = serial.Serial()
    port.port = port_name
    port.baudrate = baudrate
    port.write_timeout = 1
    port.dtr = False
    port.rts = False
    port.open()
    return port


def set_line(port: serial.Serial, signal: str, active: bool) -> None:
    """
    Lleva la línea elegida a bajo (`active=True`) o a reposo.

    Parameters
    ----------
    port : serial.Serial
        Puerto ya abierto.
    signal : str
        `"break"`, `"dtr"` o `"rts"`.
    active : bool
        `True` para marcar, `False` para volver a reposo.
    """
    if signal == "break":
        port.break_condition = active
    elif signal == "dtr":
        port.dtr = active
    else:
        port.rts = active


def send_pulses(
    port: serial.Serial,
    signal: str,
    pulse_byte: int,
    pulse_duration: float,
    n_pulses: int,
    interval: float,
) -> None:
    """
    Manda `n_pulses` marcas, una cada `interval` segundos.

    Parameters
    ----------
    port : serial.Serial
        Puerto ya abierto.
    signal : str
        `"byte"`, `"break"`, `"dtr"` o `"rts"`.
    pulse_byte : int
        Byte a escribir con `signal = "byte"`.
    pulse_duration : float
        Cuánto dura la marca con las demás señales, en segundos.
    n_pulses : int
        Cuántas marcas mandar.
    interval : float
        Tiempo entre el comienzo de una marca y el de la siguiente, en
        segundos.
    """
    for pulse_index in range(1, n_pulses + 1):
        if signal == "byte":
            port.write(bytes([pulse_byte]))
            port.flush()
            time.sleep(interval)
        else:
            set_line(port, signal, True)
            time.sleep(pulse_duration)
            set_line(port, signal, False)
            time.sleep(max(interval - pulse_duration, 0))
        print(f"  marca {pulse_index:>2}/{n_pulses}")


def main(
    serial_port: str | None,
    signal: str,
    baudrate: int,
    pulse_byte: int,
    pulse_duration: float,
    n_pulses: int,
    interval: float,
    dry_run: bool,
) -> None:
    """
    Elige el puerto, manda la tanda de marcas y cierra.

    Parameters
    ----------
    serial_port : str | None
        Puerto a usar, o `None` para elegirlo solo.
    signal : str
        `"byte"`, `"break"`, `"dtr"` o `"rts"`.
    baudrate : int
        Velocidad en baudios.
    pulse_byte : int
        Byte a mandar con `signal = "byte"`.
    pulse_duration : float
        Duración de la marca con las demás señales, en segundos.
    n_pulses : int
        Cuántas marcas mandar.
    interval : float
        Tiempo entre marcas, en segundos.
    dry_run : bool
        Si es `True`, usa un puerto de loopback en vez del pincho.

    Raises
    ------
    ValueError
        Si `signal` no es un valor admitido.
    """
    if signal not in VALID_SIGNALS:
        raise ValueError(
            f"signal '{signal}' desconocido, usar uno de {VALID_SIGNALS}"
        )
    usb_ports = list_usb_serial_ports()
    port_name = (
        "loop://" if dry_run else choose_port(serial_port, usb_ports)
    )

    print(f"\nAbriendo {port_name}: señal '{signal}'.")
    if signal == "byte" and pulse_byte == 0:
        print(f"Cada 0x00 es un pulso de ~{9000 / baudrate:.2f} ms en TX.")

    port = open_port(port_name, baudrate, dry_run)
    try:
        send_pulses(
            port, signal, pulse_byte, pulse_duration, n_pulses, interval
        )
    finally:
        if signal != "byte":
            set_line(port, signal, False)
        port.close()
    print("\nListo.")


if __name__ == "__main__":
    main(
        serial_port=SERIAL_PORT,
        signal=SIGNAL,
        baudrate=BAUDRATE,
        pulse_byte=PULSE_BYTE,
        pulse_duration=PULSE_DURATION,
        n_pulses=N_PULSES,
        interval=INTERVAL,
        dry_run=DRY_RUN,
    )
