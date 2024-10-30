# Diccionario de ejemplo con 2 parámetros en cada ítem
llamadas_telf = {
    12 : ("América del Norte", 2),
    15 : ("América del Centro", 2.2),
    18 : ("América del Sur", 4.5),
    19 : ("Europa", 3.5),
    23 : ("Asia", 6),
    25 : ("África", 6),
    29 : ("Oceanía", 5)
}

# Desarrolla un programa que permita al usuario ingresar el número de minutos que habló por teléfono y el país al que llamó.

entrada = input("Ingresa un valor (por ejemplo, 12,5): ")
clave_str, valor_str = entrada.split(",")
clave = int(clave_str)
valor = int(valor_str)

print("Clave:", clave)
print("Valor:", valor)


costoLlamada = llamadas_telf[clave][1] * valor

print(f"Clave {clave} , Valor {valor}")
print(f"Costo de la llamada: {costoLlamada}")