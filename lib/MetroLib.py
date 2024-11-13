from lib.MetroEstructuras import *

import math

import sys

def generarTablaEstaciones(nombre_archivo_estaciones, nombre_archivo_distancias):

    tabla_hash = {}

    with open(nombre_archivo_estaciones, "r") as registros_estaciones:

        for registro in registros_estaciones:

            registro = registro.strip().split(",")

            nombre_estacion = registro[0]

            if nombre_estacion not in tabla_hash:

                latitud = float(registro[1])

                longitud = float(registro[2])

                lineas = registro[3:]

                if len(lineas) == 1:
	
                    nueva_estacion = EstacionPaso(nombre_estacion, latitud, longitud, lineas[0])

                else:

                    nueva_estacion = EstacionCorrespondencia(nombre_estacion, latitud, longitud, lineas)
                

                tabla_hash[nombre_estacion] = nueva_estacion

    with open(nombre_archivo_distancias, "r") as registros_distancias:

        for registro in registros_distancias:

            registro = registro.strip().split(",")

            estaciones = [tabla_hash[registro[0]], tabla_hash[registro[1]]]

            distancia = int(registro[2])

            indice_estacion_adyacente = 1

            for estacion in estaciones:

                estacion_adyacente = estaciones[indice_estacion_adyacente]

                indice_estacion_adyacente = ~indice_estacion_adyacente & 1

                if isinstance(estacion, EstacionPaso):

                    estacion.estaciones_adyacentes.append([estacion_adyacente, distancia])

                else:

                    if isinstance(estacion_adyacente, EstacionPaso):

                        estacion.transbordos[estacion_adyacente.linea].append([estacion_adyacente, distancia])

                    else:

                        conjunto_lineas_estacion = set(estacion.transbordos.keys())

                        conjunto_lineas_estacion_adyacente = set(estacion_adyacente.transbordos.keys())

                        linea_conexion = list(conjunto_lineas_estacion & conjunto_lineas_estacion_adyacente)[0]

                        estacion.transbordos[linea_conexion].append([estacion_adyacente, distancia])


    return tabla_hash


def obtenerEstacionInicioFin(nombre_estacion_inicio, nombre_estacion_final, tabla_estaciones):

    estacion_inicio = tabla_estaciones[nombre_estacion_inicio]

    estacion_final = tabla_estaciones[nombre_estacion_final]

    return estacion_inicio, estacion_final


def getInformacionEstacion(estacion):

    if isinstance(estacion, EstacionPaso):

        return f"{estacion} -> {estacion.estaciones_adyacentes}"

    else:

        return f"{estacion} -> {estacion.transbordos}"


def calcularDistancia(la1, lo1, la2, lo2):

    """Esta funcion hace una implementación de la formula de Haversine para obtener la
    distancia en metro que hay entre dos puntos geográficos. En este caso, los puntos 
    geográficos son representados por la latitud y longitud de una estacion inicial y 
    una estacion final.

    Justamente este es el mecanismo que utilizamos como función heurística."""

    la1 = math.radians(la1)

    la2 = math.radians(la2)

    lo1 = math.radians(lo1)

    lo2 = math.radians(lo2)

    delta_latitud = la2 - la1

    delta_longitud = lo2 - lo1

    return 2 * 6371000 * math.asin( math.sqrt( ( math.sin( delta_latitud / 2 )**2 ) + math.cos( la1 ) * ( math.cos( la2 ) ) * ( math.sin( delta_longitud / 2 )**2 ) ) )

def obtenerEstacionesAdyacentes(estacion):

    if isinstance(estacion, EstacionPaso):

        #Si la estación es una estación de paso

        estaciones_adyacentes = [registro_estacion[0] for registro_estacion in estacion.estaciones_adyacentes]

    else:

        #Si la estacion es una estación de correspondencia

        estaciones_adyacentes = [registro_estacion[0] for estaciones_adyacentes_linea in estacion.transbordos.values() for registro_estacion in estaciones_adyacentes_linea]

    return estaciones_adyacentes


def obtenerCosteEntreEstacionesAdyacentes(estacion_padre, estacion_adyacente):

    distancia_padre_hijo = 0

    if estacion_padre is not estacion_adyacente:

        if isinstance(estacion_padre, EstacionPaso):

            for registro_estacion in estacion_padre.estaciones_adyacentes:

                if registro_estacion[0] == estacion_adyacente:

                    distancia_padre_hijo = registro_estacion[1]

                    break

        else:

            adyacentes = [adyacente for estaciones_linea in estacion_padre.transbordos for adyacente in estaciones_linea]

            for registro_estacion in adyacentes:

                if registro_estacion[0] == estacion_adyacente:

                    distancia_padre_hijo = registro_estacion[1]

                    break

    return distancia_padre_hijo

def obtenerEstacionMenorCoste(estacion_final, distancias, lista_abierta):

    estacion_menor_coste = lista_abierta[0]

    menor_coste = distancias[estacion_menor_coste] + calcularDistancia(estacion_menor_coste.latitud, estacion_menor_coste.longitud, estacion_final.latitud, estacion_final.longitud)

    for estacion in lista_abierta[1:]:

        coste = distancias[estacion] + calcularDistancia(estacion.latitud, estacion.longitud, estacion_final.latitud, estacion_final.longitud)

        if coste < menor_coste:

            menor_coste = coste

            estacion_menor_coste = estacion

    return estacion_menor_coste 


def encontrarRutaMasCorta(estacion_inicio, estacion_final):

    """Esta funcion realiza una implementación del algoritmo A* para poder encontrar la ruta más corta entre dos estaciones que forman parte de la red del metro de la Ciudad de México."""

    """Inicialmente la lista abierta comienza almacenando únicamente la estacion a partir de
    la cual iniciaremos el recorrido.

    La función de esta lista es almacenar todos los nodos que debemos de ir evaluando y que
    probablemente puedan llegar a formar parte del camino final."""
    
    lista_abierta = [estacion_inicio]

    """La lista cerrada inicialmente está vacía.

    El propósito de esta lista es almacenar todos aquellos nodos del grafo que previamente
    ya han sido evaluados."""

    lista_cerrada = []

    """Este diccionario tiene la finalidad de que para cada estación del metro que se vaya
    explorando, se le asigna la estación de metro padre a partir de la cual llegamos a la
    estacion del metro de evaluación.

    La clave del diccionario es la estacion del metro hijo y la clave asociada es la
    estacion del metro padre a partir de la cual llegamos al hijo.

    Inicialmente esta lista almacena a la estacion de inicio como la estacion padre e hijo.
    De esta manera, al ser tanto el hijo como el padre la misma estación, podemos comenzar
    el proceso correctamente."""

    predecesores = {estacion_inicio : estacion_inicio}

    """Este diccionario se encarga de llevar un registro de las distancia real (coste real)
    de moverse desde la estacion padre hacia la estación hijo.

    La clave de diccionario es el nodo hijo en cuestión, mientras que el valor asociado
    es la distancia (en metro) de haberse movido desde la estación padre hasta la estación
    hijo."""

    distancias = {estacion_inicio : 0}

    while lista_abierta:

        estacion = obtenerEstacionMenorCoste(estacion_final, distancias, lista_abierta)

        lista_abierta.remove(estacion)

        lista_cerrada.append(estacion)

        if estacion == estacion_final:

            return construirRuta(estacion_inicio, estacion_final, predecesores)

        for estacion_adyacente in obtenerEstacionesAdyacentes(estacion):

            if estacion_adyacente not in lista_abierta and estacion_adyacente not in lista_cerrada:

                predecesores[estacion_adyacente] = estacion

                distancias[estacion_adyacente] = obtenerCosteEntreEstacionesAdyacentes(estacion, estacion_adyacente)

                lista_abierta.append(estacion_adyacente)

    return False


def construirRuta(estacion_inicio, estacion_final, antecesores):

    ruta = [estacion_final]

    estacion = estacion_final

    while estacion != estacion_inicio:

        ruta.insert(0, antecesores[estacion])

        estacion = antecesores[estacion]

    return ruta

