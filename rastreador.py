# -*- coding: utf-8 -*-

from time import strftime
from base import *


def cyberelk_net(lista_claves):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from time import sleep

    chromedriver = "C:\Users\jmd\Documents\chromedriver\chromedriver"
    # Carga las opciones de Chromium
    chrome_options = Options()
    # deshabilita las notificaciones de Chrome
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path = chromedriver, chrome_options = chrome_options)

    keywords = lista_claves.split()
    lista_datos = []

    for key in keywords:
        url = 'http://cyberelk.net/tim/?s=' + key
        driver.get(url)
        sleep(5)
        enlaces = driver.find_elements(By.XPATH, '//h3/a')
        for enlace in enlaces:
            datos_notas = {}
            datos_notas['url'] = enlace.get_attribute('href').encode('utf-8')
            datos_notas['titulo'] = enlace.text.encode('utf-8')
            lista_datos.append(datos_notas)
    driver.close()
    driver.quit()
    return lista_datos

def doughellmann_com(lista_claves):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from time import sleep

    chromedriver = "C:\Users\jmd\Documents\chromedriver\chromedriver"
    # Carga las opciones de Chromium
    chrome_options = Options()
    # deshabilita las notificaciones de Chrome
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path = chromedriver, chrome_options = chrome_options)

    keywords = lista_claves.split()
    lista_datos = []

    for key in keywords:
        url = 'https://doughellmann.com/blog/?s=' + key
        driver.get(url)
        sleep(5)
        enlaces = driver.find_elements(By.XPATH, '//h2[@class="entry-title"]/a')
        for enlace in enlaces:
            datos_notas = {}
            datos_notas['url'] = enlace.get_attribute('href').encode('utf-8')
            datos_notas['titulo'] = enlace.text.encode('utf-8')
            lista_datos.append(datos_notas)
    driver.close()
    driver.quit()
    return lista_datos

def economist_com(lista_claves):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from time import sleep

    chromedriver = "C:\Users\jmd\Documents\chromedriver\chromedriver"
    # Carga las opciones de Chromium
    chrome_options = Options()
    # deshabilita las notificaciones de Chrome
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path = chromedriver, chrome_options = chrome_options)

    keywords = lista_claves.split()
    lista_datos = []

    for key in keywords:
        url = 'https://www.economist.com/search?q=' + key
        driver.get(url)
        sleep(3)
        # Ordena los resultados por fecha
        driver.find_element(By.XPATH, '//*[@class="gsc-selected-option"]').click()
        sleep(2)
        driver.find_element(By.XPATH, '(//*[@class="gsc-option"])[2]').click()
        sleep(2)

        # Extrae las urls de las entradas
        entradas = driver.find_elements(By.XPATH, '//*[@id="___gcse_0"]//td[2]/div[1]/a')
        urls = []
        for entrada in entradas:
            try:
                link = str(entrada.get_attribute('href'))
                print '############# Lista: ', link
                # Selecciona el origen de los artículos
                if 'https://www.economist.com' in link and len(link) > 29:
                # Excluye las listas de artículos
                    if not '/latest-updates' in link or not '/topics' in link:
                        urls.append(entrada)
            except:
                pass
        print urls
    for url in urls:
        datos_notas = {}
        datos_notas['url'] = url.get_attribute('href').encode('utf-8')
        datos_notas['titulo'] = url.text.encode('utf-8')
        lista_datos.append(datos_notas)

    driver.close()
    driver.quit()
    return lista_datos

def rastrea(datos):
    sitios = select_sitios(int(datos['sitio']))
    listas = select_claves(int(datos['clave']))
    for sitio, lista in zip(sitios, listas):
        if sitio['nombre'] == 'cyberelk.net':
            insert_rastreos(strftime("%Y-%m-%d %H:%M:%S+00:00"), datos['id'])
            id_rastreo = select_rastreos()
            datosnotas = cyberelk_net(lista['lista'])            
            for datos in datosnotas:
                print datos
                insert_notas(datos, id_rastreo)
        if sitio['nombre'] == 'doughellmann.com':
            insert_rastreos(strftime("%Y-%m-%d %H:%M:%S+00:00"), datos['id'])
            id_rastreo = select_rastreos()
            datosnotas = doughellmann_com(lista['lista'])
            for datos in datosnotas:
                print datos
                insert_notas(datos, id_rastreo)
        if sitio['nombre'] == 'economist.com':
            insert_rastreos(strftime("%Y-%m-%d %H:%M:%S+00:00"), datos['id'])
            id_rastreo = select_rastreos()
            datosnotas = economist_com(lista['lista'])
            for datos in datosnotas:
                print datos
                insert_notas(datos, id_rastreo)
