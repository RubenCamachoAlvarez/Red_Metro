from lib.MetroLib import *

tabla_estaciones = generarTablaEstaciones("datos/Estaciones_Metro.dat", "datos/Distancia_Estaciones.dat")

nombre_estacion_inicio = input("Estacion de inicio: ")

nombre_estacion_final = input("Estacion final: ")

estacion_inicio = tabla_estaciones[nombre_estacion_inicio]

estacion_final = tabla_estaciones[nombre_estacion_final]

print("Estacion de inicio:", getInformacionEstacion(estacion_inicio))

print("Estacion final:", getInformacionEstacion(estacion_final))
