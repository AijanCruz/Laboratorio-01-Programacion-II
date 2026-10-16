"""================================================================================================
Institute....: Universidad Técnica Nacional
Headquarters.: Pacífico
Career.......: Tecnologías de Información
Period.......: 3-2026
Document.....: posicion.py
Goals........: Declare external function for clase_01_04.py Python file.
Professor....: Jorge Ruiz (york)
Student......:
================================================================================================"""
# this library is used to position the cursor on the screen and this is possible, so you use Cython
# version in the others words, you use C language to do it.
from ctypes import *


# Standard output device, this is the active console screen buffer
STD_OUTPUT_HANDLE = -11


# pass is a null operation, when it is executed, nothing happens.
# It is useful as a placeholder when a statement is required syntactically,
# but no code needs to be executed, for example:
#   def f(arg): pass    # a function that does nothing (yet)
#   class C: pass       # a class with no methods (yet)
class COORD (Structure):
    pass


# define position on screen same form that cartesian blueprint
COORD._fields_ = [("X", c_short), ("Y", c_short)]


# function to position cursor on screen and print text,
# used in the main code
def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    print(s)


# function to position cursor on screen
def goto_xy(r, c):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))