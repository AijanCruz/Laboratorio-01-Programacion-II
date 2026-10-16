from colorama import Fore, Style
from posicion import print_at

# # es pared y espacio es camino libre
DISENO = [
    "##################################################",
    "#        #           #              #            #",
    "#  ####  #  #######  #  ##########  #  ########  #",
    "#  #     #        #     #           #  #         #",
    "#  #  ########   #  ####  ##########  #  ######  #",
    "#  #           #  #                 #            #",
    "#  ########### #  ############  ###  ########### #",
    "#              #                 #               #",
    "#  ##########  ###############  ###  ##########  #",
    "#  #                          #                  #",
    "#     ######################     ############### #",
    "##################################################",
]


class Mapa:
    SIMBOLOS = {"tesoro": "$", "pocion": "+", "trampa": "X", "monstruo": "M"}
    COLORES = {
        "tesoro": Fore.YELLOW,
        "pocion": Fore.GREEN,
        "trampa": Fore.MAGENTA,
        "monstruo": Fore.RED,
    }
    PARED = "░"

    def __init__(self, diseno, fila_base=3, col_base=7):
        # fila_base y col_base es donde empieza el mapa dentro del marco
        self.filas = len(diseno)
        self.columnas = len(diseno[0])
        self.fila_base = fila_base
        self.col_base = col_base
        self.paredes = []
        self.elementos = []
        self.cargar_paredes(diseno)

    def cargar_paredes(self, diseno):
        # guarda la posicion de cada # del diseno
        self.paredes = []
        for f in range(len(diseno)):
            for c in range(len(diseno[f])):
                if diseno[f][c] == "#":
                    self.paredes.append((f, c))

                    def dentro_de_limites(self, fila, columna):
                        return 0 <= fila < self.filas and 0 <= columna < self.columnas

                    def hay_pared(self, fila, columna):
                        return (fila, columna) in self.paredes

                    def es_valida(self, fila, columna):
                        # se puede pasar si esta dentro del mapa y no es pared
                        if not self.dentro_de_limites(fila, columna):
                            return False
                        return not self.hay_pared(fila, columna)

                    def agregar_elemento(self, elemento):
                        self.elementos.append(elemento)

                    def quitar_elemento(self, elemento):
                        # se usa cuando el jugador recoge algo
                        if elemento in self.elementos:
                            self.elementos.remove(elemento)

                    def obtener_elemento(self, fila, columna):
                        # devuelve el elemento de esa casilla, o None si no hay nada
                        for e in self.elementos:
                            if e.fila == fila and e.columna == columna:
                                return e
                        return None

                    def contar_tipo(self, tipo):
                        # cuantos quedan de ese tipo, por ejemplo "tesoro"
                        total = 0
                        for e in self.elementos:
                            if e.tipo == tipo:
                                total += 1
                        return total

                    def celdas_libres(self):
                        # casillas sin pared ni elementos, sirve para ubicar y mover monstruos
                        libres = []
                        for f in range(self.filas):
                            for c in range(self.columnas):
                                if self.es_valida(f, c) and self.obtener_elemento(f, c) is None:
                                    libres.append((f, c))
                        return libres