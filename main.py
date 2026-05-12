from ascii_art import convertir_ascii
from ascii_art import guardar_ascii_art
import os

imagen = input("Ingrese la ruta de la imagen: ")
if not os.path.exists(imagen):
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    exit()

while True:
    metodo = input("Ingrese el método (pixel / ascii): ")
    if metodo == "pixel" or metodo == "ascii":
        break
    else:
        print("Método inválido. Escriba 'pixel' o 'ascii'.")

if metodo == 'ascii': 

    ancho = input("Ingrese el ancho de imagen deseado(por default sera 100): ")
    if ancho == "": 
        ancho = 100
    elif int(ancho) <= 0: 
        print("El ancho de la imagen ASCII debe ser un número positivo.")
        exit()
    else: 
        ancho = int(ancho)
    
    resultado = convertir_ascii(imagen , ancho)
    guardar_ascii_art(resultado, "archivos/resultado.txt")
    print("Archivo guardado en archivos/resultado.txt")

elif metodo == 'pixel':
    pass #LLENA MILO ACA