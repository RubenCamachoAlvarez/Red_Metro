from lib.MetroEstructuras import *

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
