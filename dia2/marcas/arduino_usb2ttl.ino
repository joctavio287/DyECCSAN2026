/*
 * USB a TTL con un Arduino: la version barata del hardware de marcas.
 *
 * Lee un byte por el puerto serie y lo saca por 8 pines digitales,
 * manteniendo el valor durante PULSE_MS y volviendo despues a cero.
 * Con esto un Arduino de mil pesos hace lo mismo que un adaptador
 * USB-TTL comercial para el 90% de los casos.
 *
 * Placa recomendada: Arduino Leonardo o Micro (ATmega32u4). Tienen USB
 * nativo, asi que no reinician al abrir el puerto ni agregan el
 * retraso del conversor serie de la Uno.
 *
 * Cableado: los pines 2 a 9 son los bits 0 a 7 del codigo. Para mirar
 * en el osciloscopio alcanza con el pin 2 (bit 0) y GND.
 *
 * ATENCION: el Arduino saca 5 V. Antes de conectarlo a la entrada de
 * triggers de un amplificador de EEG, verificar en el manual que
 * tolere 5 V; varios esperan 3.3 V y hace falta un divisor resistivo o
 * un optoacoplador. Un optoacoplador ademas aisla electricamente al
 * participante del equipo, que es lo que corresponde.
 *
 * Del lado de PsychoPy, en marcas_ttl.py o marcas_audio.py:
 *     BACKEND = "serial"
 *     SERIAL_PORT = "COM3"   // o "/dev/ttyACM0" en Linux
 *     SERIAL_SIGNAL = "byte"
 *     SERIAL_BAUDRATE = 115200
 */

const uint8_t FIRST_PIN = 2;
const uint8_t N_BITS = 8;
const unsigned long PULSE_MS = 5;
const unsigned long BAUDRATE = 115200;

void writeCode(uint8_t code) {
  for (uint8_t bit = 0; bit < N_BITS; bit++) {
    digitalWrite(FIRST_PIN + bit, (code >> bit) & 1);
  }
}

void setup() {
  for (uint8_t bit = 0; bit < N_BITS; bit++) {
    pinMode(FIRST_PIN + bit, OUTPUT);
  }
  writeCode(0);
  Serial.begin(BAUDRATE);
}

void loop() {
  if (Serial.available() > 0) {
    uint8_t code = Serial.read();
    writeCode(code);
    delay(PULSE_MS);
    writeCode(0);
  }
}
