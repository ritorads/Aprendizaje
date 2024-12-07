# Desarrolla un programa que permita al usuario ingresar el número de filas y columnas de una matriz. 
# El programa debe construir una matriz donde :
# cada elemento se calcule multiplicando el número de la fila (comenzando en 1) por el número de la columna (comenzando en 2). 
# Posteriormente, el programa debe contar cuántos elementos de la matriz son mayores a un valor límite ingresado por el usuario.

import numpy as np
import os 

def pideDatos():
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))
    limite = int(input("Ingrese el límite: "))
    return filas, columnas, limite

def manejoError(filas, columnas, limite):
    if (filas <=0 or columnas <= 0 ) and (limite >0):
        print("Error en Dimensiones")
        os._exit(1)
    elif (limite <= 0) and (filas > 0 and columnas > 0):
        print("Error en Límite")
        os._exit(1)
    elif (filas <= 0 or columnas <= 0) and (limite <= 0):
        print("Error en Dimensiones y Límite")
        os._exit(1)
    else:
        pass

def rellenaMatriz(matriz, limite):
    mayores = []
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            numero = (i+1) * (j+2)
            matriz[i, j] = numero
            if numero > limite:
                mayores.append(numero)
    return mayores

def creaMatriz(filas, columnas, limite):
    matriz = np.zeros((filas, columnas))
    mayores = rellenaMatriz(matriz, limite)
    return matriz, mayores


Filas, Columnas, Limite = pideDatos()
manejoError(Filas, Columnas, Limite)

print(creaMatriz(Filas, Columnas, Limite))
print(f"Mayores a {Limite}: {len(creaMatriz(Filas, Columnas, Limite)[1])}")