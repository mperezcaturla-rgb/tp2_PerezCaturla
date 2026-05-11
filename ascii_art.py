from PIL import Image
import numpy as np

PALETA = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def convertir_grises(ruta_imagen:str): 
    '''pillow abre la imagen y la convierte a escala de grises con el convert,
    recibe la ruta de la imagen y devuelve imagen de pillow'''

    img = Image.open(ruta_imagen) #Abre imagen
    img = img.convert("L") #Convierte imagen a escala de grises

    return img

def normalizar(matriz:np.ndarray): 
    '''utilizando numpy, aplico la formula a cada pixel de la matriz para normalizar.
    recibe un array de numpy (la matriz) y devuelve otro array de numpy ya normalizado. '''

    minimo = matriz.min() #calcula el pixel con menos intesidad de la matriz con numpy
    maximo = matriz.max() #calcula el pixel con mas intensidad de la matriz con numpy

    matriz_normalizada = ((matriz - minimo) / (maximo - minimo)) * 255 #aplica la formula de normalizacion por cada pixel con numpy

    return matriz_normalizada

def redimensionamiento(img:Image.Image , ancho:int):
    '''recibe la imagen de pillow ya en escala de grises y la redimensiona en base al ancho indicado por el usuario''' 

    ancho_original , alto_original = img.size #el size de pillow me devuelve una tupla con el ancho y alto de la imagen orignal
    alto = int((ancho / (ancho_original/alto_original)) * 0.45) #calculamos el alto nuevo respetando la relacion de aspecto original
    img = img.resize((ancho , alto)) #redimensiono imagen con el ancho del usuario y al alto nuevo con el resize de pillow

    return img 

def convertir_matriz(img:Image.Image): 
    ''' convierte una imagen de pillow a un array de numpy para poder leerlo como matriz'''
    
    matriz = np.array(img)

    return matriz 

def mapeo(matriz:np.ndarray): 
    ''' recibe la matriz normalizada y asigna un caracter de la paleta a cada pixel, en base a la intensidad del pixel. 
    Devuelve una lista con los strings'''

    lista = []
    
    for fila in matriz: 
        linea = "" #hago que cada fila sea un string vacio
        for pixel in fila: 
            i = round((1 - (pixel / 255)) * ((len(PALETA)) - 1)) #calculo el indice de la paleta correspondiente al pixel
            linea += PALETA[i] #agrego el caracter de la paleta a la fila vacia
        lista.append(linea)

    return lista

def guardar_ascii_art(ascii_art, ruta_salida):
    with open(ruta_salida, 'w') as f:
        f.write(ascii_art)

def convertir_ascii(ruta_imagen:str, ancho:int):

    '''Funcion principal que invoca al resto en orden. 
    recibe la ruta de imagen y el ancho elegido, convierte a ascii art
    y devuelve un string con el arte'''

    img = convertir_grises(ruta_imagen) #PASO 1, CONVIERTE A ESCALA DE GRISES
    img = redimensionamiento(img , ancho) #PASO 2, REDIMENSIONO LA IMAGEN
    matriz = convertir_matriz(img) #PASO 3, CONVIERTO A ARRAY DE NUMPY
    matriz = normalizar(matriz) #PASO 4, NORMALIZAMOS
    lista = mapeo(matriz) #PASO 5, HACEMOS LA LISTA DE STRINGS
    ascii_art = "\n".join(lista)  # CONSTRUYO STRING FINAL CON SALTOS DE LINEA

    return ascii_art