# Tu propio experimento — las variantes

El menú de la Consigna 2. Cada pareja convierte su Stroop en otra
tarea: la estructura queda igual (instrucciones, bucle de trial y
feedback, despedida) y cambian el archivo de condiciones, el estímulo y
las teclas.

| Carpeta | Tarea | Qué se mide | Componente nuevo |
|---|---|---|---|
| `simon/` | Un cuadrado azul o naranja a la izquierda o a la derecha; se responde el color | Efecto Simon: más lento cuando el lado no coincide con la tecla | **Polygon**, con posición `(pos_x, 0)` |
| `flanker/` | Cinco flechas; se responde la del medio | Efecto flanker: más lento cuando las de los costados apuntan al revés | Text |
| `auditiva/` | Dos tonos; ¿el segundo es más agudo o más grave? | Acierto según la diferencia en Hz | **Sound** ×2, con `$frecuencia` |
| `orientacion/` | Una rejilla que aparece 200 ms, inclinada | Acierto según el ángulo | **Grating**, con orientación `orientacion` |

Todas usan **Z** (izquierda / grave) y **M** (derecha / agudo), y la
columna de la respuesta correcta se llama `correct_key` en todas, así
el análisis del día 2 sirve para cualquiera.

En cada carpeta está `condiciones.csv`, el archivo de condiciones
listo para usar. Los pasos para armar cada variante están en la
Consigna 2.
