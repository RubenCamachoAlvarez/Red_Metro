from lib.MetroLib import *

tabla_estaciones = generarTablaEstaciones("datos/Estaciones_Metro.dat", "datos/Distancia_Estaciones.dat")

nombre_estacion_inicio = input("Estacion de inicio: ")

nombre_estacion_final = input("Estacion final: ")

estacion_inicio = tabla_estaciones[nombre_estacion_inicio]

estacion_final = tabla_estaciones[nombre_estacion_final]

resultado = encontrarRutaMasCorta(estacion_inicio, estacion_final)

if isinstance(resultado, bool) and resultado == False:

    print("No se ha podido encontrar una ruta adecuada entre las estaciones")

elif isinstance(resultado, list):

    print("RUTA")

    for indice_estacion in range(len(resultado)):

        estacion = resultado[indice_estacion]

        print(estacion.nombre, end="\n" if indice_estacion == len(resultado) - 1 else " -> ")

else:

    print("Error valor no contemplado:", resultado)
