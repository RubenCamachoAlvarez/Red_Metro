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


def encontrarRutaMasCorta(estacion_inicio, estacion_final):

    """Esta funcion realiza una implementación del algoritmo A* para poder encontrar la ruta más corta entre dos estaciones que forman parte de la red del metro de la Ciudad de México"""

    
    #Esta lista almacena los nodos que están pendientes por evaluar.
    lista_abierta = []

    #Esta lista almacena los nodos que ya han sido evaluados.
    lista_cerrada = []

    """Esta variable se encarga de almacenar la cantidad de metros que hemos avanzado
    desde la estacion de inicio hasta la estacion actual.
    Practicamente, esta variable tiene la funcion g(n)."""
    distancia_recorrida = 0

    def obtenerEstacionMasCercana():

        estaciones = lista_abierta[1:]

        estacion_mas_cercana = lista_abierta[0]

        coste_menor = distancia_recorrida 

    lista_abierta.append(estacion_inicio)

    while len(lista_abierta) > 0:

        pass

