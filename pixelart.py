from PIL import Image
import numpy as np


def crear_paleta(niveles_color:int):
    '''Crea una paleta con valores redondeados de color. Recibe la cantidad de niveles de color por canal 
    devuelve un array con los valores posibles por canal.'''
    if niveles_color==1:
        return np.array([127])
    else:
        return np.linspace(0,255,niveles_color).astype(int)
    
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


def calcular_color_promedio(bloque):
    """Calcula el promedio de RGB del bloque"""
    #usa sum de numpy para cada canal
    suma_r = np.sum(bloque[:, :, 0])
    suma_g = np.sum(bloque[:, :, 1])
    suma_b = np.sum(bloque[:, :, 2])
    #cantidad de pixeles en el bloque
    cantidad_pixeles = bloque.shape[0] * bloque.shape[1]
    #calcular promedios
    prom_r = int(suma_r / cantidad_pixeles)
    prom_g = int(suma_g / cantidad_pixeles)
    prom_b = int(suma_b / cantidad_pixeles)
    return np.array([prom_r, prom_g, prom_b])


def redondear_color(color, paleta):
    """Encuentra el color mas cercano en la paleta"""
    color_final = []
    
    #para cada canal RGB
    for canal in range(3):
        valor = color[canal]
        
        #Calcula distancias con numpy
        distancias = np.abs(paleta - valor)
        
        #Busco el índice del mínimo
        idx_minimo=0
        for i in range(len(distancias)):
            if distancias[i] < distancias[idx_minimo]:
                idx_minimo = i
        
        color_final.append(paleta[idx_minimo])
    
    return np.array(color_final)


def pintar_bloque(img_array, x, y, tam_bloque, color):
    """Pinta todo el bloque con el color"""
    alto, ancho = img_array.shape[:2]
    x_fin = min(x + tam_bloque, ancho)
    y_fin = min(y + tam_bloque, alto)
    #asigno el color al bloque completo 
    img_array[y:y_fin, x:x_fin] = color


def aplicar_pixel_art(ruta_imagen: str, tam_bloque: int, niveles_color: int):
    """Aplica el filtro de Pixel Art a una imagen y la devuelve."""
    
    #abre la imagen
    imagen = Image.open(ruta_imagen)
    img_array = np.array(imagen)
    alto, ancho = img_array.shape[:2]
    paleta = crear_paleta(niveles_color) 
    #recorre por bloques
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = extraer_bloque(img_array, x, y, tam_bloque)
            color_prom = calcular_color_promedio(bloque)
            color_final = redondear_color(color_prom, paleta)
            pintar_bloque(img_array, x, y, tam_bloque, color_final)
     
    #convierto de vuelta a imagen 
    resultado = Image.fromarray(img_array)
    return resultado
