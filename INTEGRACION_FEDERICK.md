# Parte de Federick: elementos del mapa

`elemento_mapa.py` contiene la clase `ElementoMapa` y las funciones para procesar
una celda y reubicar monstruos. Usa los métodos de la clase `Jugador` existente.

## Elementos

| Tipo | Símbolo | Efecto |
| --- | --- | --- |
| tesoro | $ | Suma 30 puntos y un tesoro al inventario. |
| pocion | + | Recupera 20 de salud. También acepta el tipo `poción`. |
| trampa | X | Resta 20 de salud, sin bajar de cero. |
| monstruo | M | Mata al jugador y termina la partida. |

Los tesoros, pociones y trampas se eliminan después de usarse. La curación usa
`Jugador.curarse`, que actualmente no establece un máximo de salud.

## Integración con Juego

Al crear la partida, usar `Jugador(nombre="Héroe", salud=100)`: el constructor
actual de Jugador tiene salud cero como valor predeterminado.

El mapa debe ofrecer `filas`, `columnas`, `elementos` y
`es_valida(fila, columna)`. Sus elementos deben ser objetos `ElementoMapa`:

```python
from elemento_mapa import ElementoMapa, procesar_celda, reubicar_monstruos

# Dentro de la inicialización de Juego, después de crear el mapa:
self.mapa.elementos.append(ElementoMapa("tesoro", 1, 2))
# Cada posición inicial debe ser transitable y estar desocupada.
```

Agregar estos métodos dentro de la clase Juego:

```python
def procesar_celda(self):
    return procesar_celda(self)

def reubicar_monstruos(self):
    return reubicar_monstruos(self)
```

El controlador de turnos puede usar este orden. `self.activo` empieza en `True`:

```python
if self.jugador.mover(direccion, self.mapa):
    mensaje = self.procesar_celda()
    if mensaje:
        print(mensaje)  # Sustituir por el panel de mensajes de la consola.

    if self.activo:
        mensaje = self.reubicar_monstruos()
        if mensaje:
            print(mensaje)

    quedan_tesoros = False
    for elemento in self.mapa.elementos:
        if elemento.tipo == "tesoro":
            quedan_tesoros = True

    if self.activo and not quedan_tesoros:
        self.activo = False
        print("¡Ganaste! Recuperaste todos los tesoros.")
```

Los monstruos se reubican solo tras movimientos válidos. No ocupan paredes,
objetos ni la misma celda entre sí; pueden aparecer sobre el jugador y causar
derrota. Se construye una lista de celdas disponibles. Para cada monstruo se
elige un índice con `random.randint` y se retira de la lista la celda usada.
Así no se repiten destinos ni se buscan posiciones indefinidamente.
Si no caben todos, se informa con `ValueError` antes de moverlos.

Se utilizan listas, diccionarios, tuplas, clases, funciones, condicionales y
ciclos explícitos. No se utilizan conjuntos, comprensiones, `zip`, `any`,
`random.sample`, `unittest`, `unittest.mock` ni `SimpleNamespace`.
La única biblioteca importada por el módulo es `random`, para la reubicación
aleatoria del juego. Debe confirmarse con el profesor que esa función concreta
se ha visto en clases; las instrucciones compartidas no enumeran las funciones
de aleatoriedad permitidas.

## Estado de integración

Al revisar esta adaptación, `main` contiene `Jugador.py`, `posicion.py`,
`mapa.py` y `elemento_mapa.py`, pero todavía no contiene `Juego`.
En la versión consultada de `mapa.py`, los métodos desde `dentro_de_limites` están anidados dentro
de `cargar_paredes`; deben quedar al nivel de los otros métodos de la clase para
que `Mapa.es_valida` y los demás estén disponibles. Ese archivo no se modifica
en esta entrega.

## Comprobación

```bash
python pruebas_elementos.py
```

Las 10 comprobaciones usan la clase Jugador real y un mapa pequeño de prueba,
con clases, funciones, ciclos y condicionales, sin bibliotecas de pruebas.
Verifican efectos, consumo, derrota, exclusión de paredes y objetos y destinos
únicos, incluidos 100 sorteos. La interfaz de consola completa queda pendiente
de corregir Mapa e integrar Juego.
