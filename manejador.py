# -*- coding: utf-8 -*-

import sys
from base import select_tareas
from rastreador import *

#f = '1'

def maneja(frecuencia):
    # La lista de tareas
    tareas = select_tareas(frecuencia)
    #print tareas
    for tarea in tareas:
        rastrea(tarea)

if __name__ == '__main__':
    maneja(sys.argv[1])