class Jugador:
    def __init__(self, nombre = "",fila = 0, columna = 0,puntos = 0, salud = 0):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna
        self.puntos = puntos
        self.salud = salud
        self.inventario = {"tesoros":0}


    def mover(self,direccion,mapa):
        movimientos = {
            "w": (-1, 0),  # Arriba: resta 1 a la fila.
            "s": (1, 0),  # Abajo: suma 1 a la fila.
            "a": (0, -1),  # Izquierda: resta 1 a la columna.
            "d": (0, 1)  # Derecha: suma 1 a la columna.
        }

        direccion = direccion.lower().strip()
        if direccion not  in movimientos or not self.esta_vivo():
            return False

        #obtiene los valores asociados a la tecla
        cambio_fila, cambio_columna = movimientos[direccion]

        #calcula la nueva fila, sin cambiar la posicio  del jugador
        nueva_fila = self.fila + cambio_fila

        #igual que con la fila, calcula la columna destino
        nueva_columna = self.columna + cambio_columna


        #Aqui se consulta al mapa si se puede ocupar esa posicion
        if not mapa.es_valida(nueva_fila, nueva_columna):
            #Devuelve falso si hay una pared, osea cancela el movimiento
            return False

         # si la posición es válida, actualiza la fila del jugador.
        self.fila = nueva_fila

        # Actualiza también su columna.
        self.columna = nueva_columna

        # Indica que el jugador sí se movió.
        return True

    def sumar_puntos(self,cantidad):
        if cantidad < 0:
            raise ValueError("Los puntos por sumar no pueden ser negativos")
        self.puntos += cantidad

    def recoger_tesoro(self, valor=30):
        self.sumar_puntos(valor)

        # Accede a la clave "tesoros" del diccionario y aumenta su cantidad en 1.
        self.inventario["tesoros"] += 1

    def curarse(self, cantidad=20):
        if cantidad < 0:
            raise ValueError("La curación no puede ser negativa")

        if self.salud >= 100:
            return "Tu salud ya está al máximo (100/100). No puedes curarte."

        self.salud = min(100, self.salud + cantidad)
        return f"Tu salud actual es {self.salud}/100."


    def recibir_dano(self,cantidad=20):
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo")

        # Calcula la salud restante y elige el mayor entre ese resultado y 0.
        # Así, la salud nunca queda negativa.
        self.salud = max(0,self.salud-cantidad)


    def morir(self):
        self.salud = 0

    def esta_vivo(self):
        # La comparación devuelve True si tiene salud y False si tiene 0 o menos.
        return self.salud > 0


