from lib.MetroLib import *

tabla_estaciones = generarTablaEstaciones("datos/Estaciones_Metro.dat", "datos/Distancia_Estaciones.dat")

nombre_estacion_inicio = input("Estacion de inicio: ").strip().lower()

nombre_estacion_final = input("Estacion final: ").strip().lower()

try:

    estacion_inicio = tabla_estaciones[nombre_estacion_inicio]

    estacion_final = tabla_estaciones[nombre_estacion_final]

    resultado, numero_estaciones_recorridas, distancia_recorrida = encontrarRutaMasCorta(estacion_inicio, estacion_final)

    print("\nTrayecto\n")

    for indice_estacion in range(len(resultado)):

        estacion = resultado[indice_estacion]

        print(estacion.nombre, end="\n" if indice_estacion == len(resultado) - 1 else " -> ")

    print(f"\nNúmero de estacion recorridas: {numero_estaciones_recorridas}")

    print(f"\nDistancia total recorrida: {distancia_recorrida} metros")

except KeyError:

    print("Por favor revise el nombre ingresado para cada una de las estaciones")
