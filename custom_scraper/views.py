# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import *

# Extrae los datos para mostrarlos en el html de cliente01
def cliente01(request):
    sitios = []
    for tarea in Tareas.objects.filter(cliente=1, fbaja=None).values('id', 'sitio', 'clave', 'frecrastreo'):
        for sitio in Sitios.objects.filter(id=tarea['sitio'], fbaja=None).values('nombre'):
            sitios.append(sitio)
            frecuencia = FrecuenciaRastreos.objects.filter(id=tarea['frecrastreo']).values('descripcion')[0]
            sitios.append(frecuencia)
            rastreo = Rastreos.objects.filter(tarea=tarea['id']).order_by('-id').values('id', 'fechahora')[0]
            sitios.append(rastreo)
            keyword = Claves.objects.filter(id=tarea['clave']).values('lista')[0]
            sitios.append(keyword)
            for nota in Notas.objects.filter(rastreo=rastreo['id']).values('url', 'titulo'):
                sitios.append(nota)
    return render(request, 'custom_scraper/cliente01.html', 
        {'sitios': sitios})
