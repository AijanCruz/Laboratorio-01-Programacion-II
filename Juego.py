
from Jugador import Jugador
from mapa import Mapa, DISENO
from elemento_mapa import ElementoMapa, procesar_celda, reubicar_monstruos
from colorama import Fore, Style, init
from posicion import print_at
from Interfaz import marco

import os
import random


class Juego:

    def __init__(self, nombre):
        self.mapa = Mapa(DISENO)

        self.jugador = Jugador(
            nombre=nombre,
            fila=1,
            columna=1,
            salud=100
        )

        self.activo = True
        self.mensaje = ""

        self.colocar_elementos()

    def procesar_celda(self):
        return procesar_celda(self)

    def reubicar_monstruos(self):
        return reubicar_monstruos(self)

    def colocar_elementos(self):
        cantidades = {
            "tesoro": 5,
            "pocion": 3,
            "trampa": 4,
            "monstruo": 3
        }

        libres = self.mapa.celdas_libres()

        # Reservar la posicion inicial del jugador
        posicion_jugador = (
            self.jugador.fila,
            self.jugador.columna
        )

        if posicion_jugador not in libres:
            raise ValueError(
                "La posicion inicial del jugador no es valida."
            )

        libres.remove(posicion_jugador)

        total_elementos = sum(cantidades.values())

        if len(libres) < total_elementos:
            raise ValueError(
                "No hay suficientes celdas libres."
            )

        for tipo, cantidad in cantidades.items():
            for i in range(cantidad):

                posicion = random.choice(libres)

                fila, columna = posicion

                elemento = ElementoMapa(
                    tipo, fila, columna
                )

                self.mapa.agregar_elemento(elemento)

                # Evitar colocar dos elementos en la misma posicion
                libres.remove(posicion)

    def mostrar(self):
        # Limpiar la consola
        os.system("cls")
        init(autoreset=True)

        # Dibujar marco principal
        print(Fore.LIGHTBLUE_EX)
        marco(1, 1, 65, 23)

        # Titulo del juego
        print_at(
            2, 15,
            Fore.YELLOW + Style.BRIGHT +
            "MAZMORRA PERDIDA DE LA UTN"
        )

        # Dibujar mapa y elementos
        self.mapa.dibujar()

        # Obtener posicion del jugador en pantalla
        fila, columna = self.mapa.pos_pantalla(
            self.jugador.fila,
            self.jugador.columna
        )

        # Dibujar jugador
        print_at(
            fila,
            columna,
            Fore.CYAN + Style.BRIGHT + "@" + Style.RESET_ALL
        )

        # Panel informativo
        print_at(
            16, 3,
            f"JUGADOR: {self.jugador.nombre} | "
            f"VIDA: {self.jugador.salud}/100 | "
            f"PUNTOS: {self.jugador.puntos}"
        )

        print_at(
            17, 3,
            f"POSICION: Fila {self.jugador.fila}, "
            f"Columna {self.jugador.columna} | "
            f"TESOROS: {self.mapa.contar_tipo('tesoro')}"
        )

        # Mensaje del turno anterior
        print_at(
            21, 3,
            self.mensaje[:59]
        )

    def ejecutar(self):
        # Dibujar todo el mapa una sola vez
        self.mostrar()

        while self.activo:

            print_at(
                18, 3,
                "W=Arriba | S=Abajo | A=Izquierda | D=Derecha | Q=Salir"
            )

            print_at(20, 3, "Movimiento: ")
            direccion = input().lower().strip()

            if direccion == "q":
                self.activo = False
                self.mensaje = "Saliste del juego."
                break

            # Guardar posicion anterior del jugador
            fila_anterior = self.jugador.fila
            columna_anterior = self.jugador.columna

            # Intentar movimiento
            movimiento = self.jugador.mover(direccion, self.mapa)

            if not movimiento:
                self.mensaje = "Movimiento invalido o pared."
                print_at(21, 3, " " * 59)
                print_at(21, 3, self.mensaje)
                continue

            # Guardar posiciones anteriores de monstruos
            posiciones_monstruos = [
                (e.fila, e.columna)
                for e in self.mapa.elementos
                if e.tipo == "monstruo"
            ]

            # Procesar objeto de la celda
            self.mensaje = self.procesar_celda() or ""

            if self.activo and self.mapa.contar_tipo("tesoro") == 0:
                self.activo = False
                self.mensaje = "Ganaste! Recogiste todos los tesoros."

            if self.activo:
                mensaje = self.reubicar_monstruos()
                if mensaje:
                    self.mensaje = mensaje

            # Actualizar solamente lo necesario
            self.actualizar_pantalla(
                fila_anterior,
                columna_anterior,
                posiciones_monstruos
            )

        print_at(22, 3, "PARTIDA FINALIZADA")
        print_at(25, 1, "")



    def actualizar_pantalla(self, fila_anterior, columna_anterior, posiciones_monstruos):
        # Borrar las posiciones anteriores de los monstruos
        for fila, columna in posiciones_monstruos:
            r, c = self.mapa.pos_pantalla(fila, columna)
            print_at(r, c, " ")

        # Restaurar la casilla anterior del jugador
        self.mapa.dibujar_celda(fila_anterior, columna_anterior)

        # Dibujar los elementos en sus posiciones actuales
        self.mapa.dibujar_elementos()

        # Dibujar al jugador en su nueva posicion
        fila, columna = self.mapa.pos_pantalla(
            self.jugador.fila,
            self.jugador.columna
        )

        print_at(
            fila, columna,
            Fore.CYAN + Style.BRIGHT + "@" + Style.RESET_ALL
        )

        # Actualizar el panel informativo
        print_at(
            16, 3,
            f"JUGADOR: {self.jugador.nombre} | "
            f"VIDA: {self.jugador.salud}/100 | "
            f"PUNTOS: {self.jugador.puntos}     "
        )

        print_at(
            17, 3,
            f"POSICION: Fila {self.jugador.fila}, "
            f"Columna {self.jugador.columna} | "
            f"TESOROS: {self.mapa.contar_tipo('tesoro')}     "
        )

        print_at(21, 3, " " * 59)
        print_at(21, 3, self.mensaje[:59])
