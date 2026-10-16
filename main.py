from Juego import Juego


def main():
    nombre = input("Ingrese su nombre: ")

    juego = Juego(nombre)
    juego.ejecutar()


if __name__ == "__main__":
    main()