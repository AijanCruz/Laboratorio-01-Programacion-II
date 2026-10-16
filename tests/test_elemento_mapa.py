import unittest
from types import SimpleNamespace
from unittest.mock import patch

from Jugador import Jugador
from elemento_mapa import ElementoMapa, procesar_celda, reubicar_monstruos


class MapaPrueba:
    filas = 3
    columnas = 3

    def __init__(self):
        self.elementos = []

    def es_valida(self, fila, columna):
        return 0 <= fila < 3 and 0 <= columna < 3 and (fila, columna) != (0, 0)


class PruebasElementos(unittest.TestCase):
    def setUp(self):
        self.juego = SimpleNamespace(
            jugador=Jugador("Prueba", 1, 1, salud=100),
            mapa=MapaPrueba(), activo=True,
        )

    def colocar(self, tipo):
        elemento = ElementoMapa(tipo, 1, 1)
        self.juego.mapa.elementos.append(elemento)
        return elemento

    def test_tesoro_se_recoge_una_sola_vez(self):
        self.colocar("tesoro")
        procesar_celda(self.juego)
        self.assertIsNone(procesar_celda(self.juego))
        self.assertEqual(self.juego.jugador.puntos, 30)
        self.assertEqual(self.juego.jugador.inventario["tesoros"], 1)
        self.assertEqual(self.juego.mapa.elementos, [])

    def test_pocion_usa_curacion_del_jugador(self):
        self.juego.jugador.salud = 90
        self.colocar("poción")
        procesar_celda(self.juego)
        self.assertEqual(self.juego.jugador.salud, 110)
        self.assertEqual(self.juego.mapa.elementos, [])

    def test_trampa_no_letal(self):
        self.colocar("trampa")
        procesar_celda(self.juego)
        self.assertEqual(self.juego.jugador.salud, 80)
        self.assertTrue(self.juego.activo)
        self.assertEqual(self.juego.mapa.elementos, [])

    def test_trampa_letal_no_deja_salud_negativa(self):
        self.juego.jugador.salud = 10
        self.colocar("trampa")
        procesar_celda(self.juego)
        self.assertEqual(self.juego.jugador.salud, 0)
        self.assertFalse(self.juego.activo)

    def test_monstruo_causa_derrota_y_permanece(self):
        monstruo = self.colocar("monstruo")
        procesar_celda(self.juego)
        self.assertEqual(self.juego.jugador.salud, 0)
        self.assertFalse(self.juego.activo)
        self.assertIn(monstruo, self.juego.mapa.elementos)

    def test_celda_vacia(self):
        self.assertIsNone(procesar_celda(self.juego))
        self.assertEqual(self.juego.jugador.salud, 100)

    def test_reubicacion_excluye_paredes_objetos_y_repeticiones(self):
        for tipo, fila, columna in [("tesoro", 0, 1), ("pocion", 0, 2),
                                     ("trampa", 1, 0), ("monstruo", 2, 1),
                                     ("monstruo", 2, 2)]:
            self.juego.mapa.elementos.append(ElementoMapa(tipo, fila, columna))
        def sortear(celdas, cantidad):
            self.assertEqual(set(celdas), {(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)})
            self.assertEqual(cantidad, 2)
            return [(2, 0), (1, 2)]
        with patch("elemento_mapa.random.sample", side_effect=sortear):
            reubicar_monstruos(self.juego)
        posiciones = [(e.fila, e.columna) for e in self.juego.mapa.elementos]
        self.assertEqual(len(posiciones), len(set(posiciones)))
        self.assertTrue(self.juego.activo)

    def test_monstruo_aparece_sobre_jugador(self):
        self.juego.mapa.elementos.append(ElementoMapa("monstruo", 2, 2))
        with patch("elemento_mapa.random.sample", return_value=[(1, 1)]):
            reubicar_monstruos(self.juego)
        self.assertFalse(self.juego.activo)
        self.assertEqual(self.juego.jugador.salud, 0)

    def test_partida_inactiva_no_cambia(self):
        elemento = self.colocar("tesoro")
        self.juego.activo = False
        with patch("elemento_mapa.random.sample") as sorteo:
            procesar_celda(self.juego)
            reubicar_monstruos(self.juego)
            sorteo.assert_not_called()
        self.assertIn(elemento, self.juego.mapa.elementos)
        self.assertEqual(self.juego.jugador.puntos, 0)

    def test_sin_espacio_no_mueve_monstruos(self):
        self.juego.mapa.elementos = [ElementoMapa("monstruo", 2, 1),
                                    ElementoMapa("monstruo", 2, 2)]
        self.juego.mapa.es_valida = lambda fila, columna: (fila, columna) == (1, 1)
        with self.assertRaises(ValueError):
            reubicar_monstruos(self.juego)
        self.assertEqual([(e.fila, e.columna) for e in self.juego.mapa.elementos],
                         [(2, 1), (2, 2)])

    def test_rechaza_tipo_y_valor_invalidos(self):
        with self.assertRaises(ValueError):
            ElementoMapa("pared", 1, 1)
        with self.assertRaises(ValueError):
            ElementoMapa("trampa", 1, 1, -20)


if __name__ == "__main__":
    unittest.main()
