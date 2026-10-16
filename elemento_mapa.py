"""Parte de Federick Umaña Gutiérrez - Laboratorio 01.

Integración en la clase Juego del equipo:
    from elemento_mapa import procesar_celda, reubicar_monstruos

    def procesar_celda(self):
        return procesar_celda(self)

    def reubicar_monstruos(self):
        return reubicar_monstruos(self)

Después de mover al jugador a una celda válida, llamar a procesar_celda().
Si juego.activo sigue siendo True, llamar a reubicar_monstruos().
Un movimiento contra una pared no debe ejecutar estas funciones.
El bucle de Juego controla la victoria cuando ya no quedan tesoros.

Se usan los atributos y Mapa.es_valida(fila, columna) del documento.
El jugador debe inicializarse con salud=100 al crear la partida.
"""

import random


class ElementoMapa:
    VALORES = {"tesoro": 30, "pocion": 20, "trampa": 20, "monstruo": 0}
    SIMBOLOS = {"tesoro": "$", "pocion": "+", "trampa": "X", "monstruo": "M"}

    def __init__(self, tipo, fila, columna, valor=None):
        # Acepta tanto "poción" como "pocion".
        tipo = tipo.strip().lower().replace("ó", "o")
        if tipo not in self.VALORES:
            raise ValueError("Tipo de elemento desconocido: " + tipo)
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        if valor is None:
            self.valor = self.VALORES[tipo]
        else:
            self.valor = valor
        if self.valor < 0:
            raise ValueError("El valor del elemento no puede ser negativo.")

    def obtener_simbolo(self):
        return self.SIMBOLOS[self.tipo]

    def aplicar_efecto(self, jugador):
        """Modifica al jugador y devuelve un mensaje para la pantalla."""
        if self.tipo == "tesoro":
            jugador.recoger_tesoro(self.valor)
            return f"Recogiste un tesoro: +{self.valor} puntos."
        if self.tipo == "pocion":
            jugador.curarse(self.valor)
            return f"Recuperaste {self.valor} de salud."
        if self.tipo == "trampa":
            jugador.recibir_dano(self.valor)
            return f"Activaste una trampa: -{self.valor} de salud."
        jugador.morir()
        return "Un monstruo te atrapó. Fin de la partida."


def procesar_celda(juego):
    """Aplica el efecto del elemento en la posición actual del jugador."""
    if not juego.activo:
        return None
    jugador = juego.jugador
    for elemento in juego.mapa.elementos:
        if (elemento.fila, elemento.columna) == (jugador.fila, jugador.columna):
            mensaje = elemento.aplicar_efecto(jugador)
            if elemento.tipo != "monstruo":
                juego.mapa.elementos.remove(elemento)
            if not jugador.esta_vivo():
                juego.activo = False
            return mensaje
    return None


def reubicar_monstruos(juego):
    """Reubica todos los monstruos sin paredes ni elementos superpuestos.

    Los destinos se eligen de una lista, sin repetición. Pueden coincidir con
    la posición del jugador o con posiciones que otros monstruos abandonan.
    """
    if not juego.activo:
        return None
    mapa = juego.mapa
    monstruos = []
    ocupadas = []
    for elemento in mapa.elementos:
        if elemento.tipo == "monstruo":
            monstruos.append(elemento)
        else:
            ocupadas.append((elemento.fila, elemento.columna))
    disponibles = []
    for fila in range(mapa.filas):
        for columna in range(mapa.columnas):
            if mapa.es_valida(fila, columna) and (fila, columna) not in ocupadas:
                disponibles.append((fila, columna))

    if len(disponibles) < len(monstruos):
        raise ValueError("No hay suficientes celdas libres para los monstruos.")

    destinos = []
    for monstruo in monstruos:
        # Elegir una posición y retirarla evita que se repita el destino.
        indice = random.randint(0, len(disponibles) - 1)
        posicion = disponibles[indice]
        disponibles.remove(posicion)
        destinos.append(posicion)
        monstruo.fila = posicion[0]
        monstruo.columna = posicion[1]

    posicion_jugador = (juego.jugador.fila, juego.jugador.columna)
    if posicion_jugador in destinos:
        juego.jugador.morir()
        juego.activo = False
        return "Un monstruo apareció sobre el jugador. Fin de la partida."
    return None
