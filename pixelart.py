from PIL import Image
import numpy as np



def crear_paleta(niveles_color:int):
    '''Crea una paleta con valores redondeados de color. Recibe la cantidad de niveles de color por canal 
    devuelve un array con los valores posibles por canal.'''
    if niveles_color==1:
        return np.array([127])
    else:
        return int(np.linspace(0,255,niveles_color))
    

def extraer_bloque(matriz_imagen: np.ndarray, x:int, y:int, tamaño_bloque:int) -> np.ndarray:
    '''Crea los bloques de pixeles.
    Recibe la matriz de la imagen, las coordenadas xy y el tamaño deseado de cada bloque.
    Devuelve un array con la matriz seccionada. '''
    alto=len(matriz_imagen)
    ancho=len(matriz_imagen[0])
    #calcula los limites sin salirse de la foto
    x_fin=min(y+tamaño_bloque, ancho)
    y_fin=min(x+tamaño_bloque, alto)
    return matriz_imagen[y:y_fin, x:x_fin]

