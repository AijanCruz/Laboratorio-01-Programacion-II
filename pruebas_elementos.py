"""Comprobaciones básicas. Ejecutar: python pruebas_elementos.py"""

from Jugador import Jugador
from elemento_mapa import ElementoMapa, procesar_celda, reubicar_monstruos


class MapaPrueba:
    def __init__(self):
        self.filas = 3
        self.columnas = 3
        self.paredes = [(0, 0)]
        self.elementos = []

    def es_valida(self, fila, columna):
        if fila < 0 or fila >= self.filas:
            return False
        if columna < 0 or columna >= self.columnas:
            return False
        return (fila, columna) not in self.paredes


class JuegoPrueba:
    def __init__(self):
        self.jugador = Jugador("Prueba", 1, 1, salud=100)
        self.mapa = MapaPrueba()
        self.activo = True


def comprobar(condicion, nombre):
    if not condicion:
        raise ValueError("Falló la comprobación: " + nombre)
    print("Correcto: " + nombre)


def ejecutar_pruebas():
    juego = JuegoPrueba()
    juego.mapa.elementos.append(ElementoMapa("tesoro", 1, 1))
    procesar_celda(juego)
    procesar_celda(juego)
    comprobar(juego.jugador.puntos == 30 and juego.jugador.inventario["tesoros"] == 1
              and len(juego.mapa.elementos) == 0, "tesoro recogido una sola vez")

    juego.jugador.salud = 90
    juego.mapa.elementos.append(ElementoMapa("poción", 1, 1))
    procesar_celda(juego)
    comprobar(juego.jugador.salud == 110 and len(juego.mapa.elementos) == 0,
              "poción suma 20 y se elimina")

    juego.mapa.elementos.append(ElementoMapa("trampa", 1, 1))
    procesar_celda(juego)
    comprobar(juego.jugador.salud == 90 and juego.activo
              and len(juego.mapa.elementos) == 0, "trampa resta 20 y se elimina")

    juego.jugador.salud = 10
    juego.mapa.elementos.append(ElementoMapa("trampa", 1, 1))
    procesar_celda(juego)
    comprobar(juego.jugador.salud == 0 and not juego.activo,
              "trampa letal sin salud negativa")

    juego = JuegoPrueba()
    juego.mapa.elementos.append(ElementoMapa("monstruo", 1, 1))
    procesar_celda(juego)
    comprobar(juego.jugador.salud == 0 and not juego.activo
              and len(juego.mapa.elementos) == 1, "monstruo causa derrota y permanece")

    juego = JuegoPrueba()
    comprobar(procesar_celda(juego) is None and juego.jugador.salud == 100,
              "celda vacía no cambia al jugador")

    juego.activo = False
    juego.mapa.elementos.append(ElementoMapa("tesoro", 1, 1))
    juego.mapa.elementos.append(ElementoMapa("monstruo", 2, 2))
    procesar_celda(juego)
    reubicar_monstruos(juego)
    monstruo = juego.mapa.elementos[1]
    comprobar(juego.jugador.puntos == 0 and monstruo.fila == 2 and monstruo.columna == 2,
              "partida inactiva no cambia")

    # Solo hay una celda válida; el monstruo debe caer sobre el jugador.
    juego = JuegoPrueba()
    juego.mapa.filas = 1
    juego.mapa.columnas = 1
    juego.mapa.paredes = []
    juego.jugador.fila = 0
    juego.jugador.columna = 0
    juego.mapa.elementos.append(ElementoMapa("monstruo", 0, 0))
    reubicar_monstruos(juego)
    comprobar(not juego.activo and juego.jugador.salud == 0,
              "reubicación sobre el jugador causa derrota")

    # Repetir el sorteo comprueba que nunca ocupe paredes ni otros elementos.
    correctas = True
    for intento in range(100):
        juego = JuegoPrueba()
        juego.mapa.elementos = [ElementoMapa("tesoro", 0, 1),
                                ElementoMapa("pocion", 0, 2),
                                ElementoMapa("trampa", 1, 0),
                                ElementoMapa("monstruo", 2, 1),
                                ElementoMapa("monstruo", 2, 2)]
        reubicar_monstruos(juego)
        posiciones = []
        for elemento in juego.mapa.elementos:
            posicion = (elemento.fila, elemento.columna)
            if posicion in posiciones or not juego.mapa.es_valida(posicion[0], posicion[1]):
                correctas = False
            posiciones.append(posicion)
        if posiciones[0] != (0, 1) or posiciones[1] != (0, 2) or posiciones[2] != (1, 0):
            correctas = False
    comprobar(correctas, "100 reubicaciones sin superposiciones ni paredes")

    juego = JuegoPrueba()
    reubicar_monstruos(juego)
    comprobar(juego.activo and juego.jugador.salud == 100,
              "mapa sin monstruos no cambia al jugador")


if __name__ == "__main__":
    ejecutar_pruebas()
