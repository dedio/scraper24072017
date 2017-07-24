# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from custom_scraper.models import *

# Extrae las tareas
def select_tareas(codigo):
    datos_rastreo = Tareas.objects.filter(frecrastreo=codigo, fbaja=None).values('id', 'sitio', 'clave')
    return list(datos_rastreo)

# Extrae el nombre de los sitios a partir del id
def select_sitios(id_sitio):
    nombre_sitio = Sitios.objects.filter(id=id_sitio, fbaja=None).values('nombre')
    return list(nombre_sitio)

# Extrae la lista de claves a partir del id
def select_claves(id_claves):
    lista_claves = Claves.objects.filter(id=id_claves, fbaja=None).values('lista')
    return list(lista_claves)

# Inserta un registro en rastreos
def insert_rastreos(ahora, id_tarea):
    rastreo = Rastreos(fechahora=ahora, tarea_id=id_tarea)
    rastreo.save()

# Extrae el último registro de rastreos
def select_rastreos():
    rastreo = Rastreos.objects.order_by('-id')[0]
    return rastreo.id

# Inserta un registro en notas si no existe
def insert_notas(datos, id_rastreo):
    fila = Notas.objects.filter(titulo=datos['titulo'], url=datos['url'])
    if not fila:
        nota = Notas(titulo=datos['titulo'], url=datos['url'], rastreo_id=id_rastreo)
        nota.save()
        print True