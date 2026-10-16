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