from PIL import Image
import numpy as np


def crear_paleta(niveles_color:int) -> np.ndarray:
    '''Crea una paleta con valores redondeados de color. Recibe la cantidad de niveles de color por canal 
    devuelve un array con los valores posibles por canal.'''
    if niveles_color==1:
        return np.array([127])
    else:
        return np.linspace(0,255,niveles_color).astype(int)
    
def extraer_bloque(img_array: np.ndarray, x:int, y:int, tamaño_bloque:int) -> np.ndarray:
    '''Crea los bloques de pixeles.
    Recibe la matriz de la imagen, las coordenadas xy y el tamaño deseado de cada bloque.
    Devuelve un array con la matriz seccionada. '''
    alto, ancho = img_array.shape[:2]
    #calcula los limites sin salirse de la foto
    x_fin=min(x+tamaño_bloque, ancho)
    y_fin=min(y+tamaño_bloque, alto)
    return img_array[y:y_fin, x:x_fin]


def calcular_color_promedio(bloque: np.ndarray) -> np.ndarray:
    """Calcula el promedio de RGB del bloque. Recibe las coordenadas del bloque y devuelve un array con
    su color promedio."""
    #si el bloque esta vacio, devuelve negro
    if bloque.size == 0:
        return np.array([0, 0, 0])
    #calculo promedio de cada canal usando mean
    prom_r = int(np.mean(bloque[:, :, 0])) #todos los rojos del bloque
    prom_g = int(np.mean(bloque[:, :, 1]))#verdes
    prom_b = int(np.mean(bloque[:, :, 2]))#azules
    return np.array([prom_r, prom_g, prom_b])


def redondear_color(color: np.ndarray, paleta: np.ndarray) -> np.ndarray:
    """Encuentra el color mas cercano en la paleta. Recibe un array con los colores RGB a ajustar, y la paleta con los
    valores permitidos por los niveles de color. Devuelve el color final para cada pixel"""
    color_final = []
    #para cada canal RGB
    for canal in range(3):
        valor = color[canal]
        #Calculo distancias con numpy
        distancias = np.abs(paleta - valor)
        #Busco el índice del mínimo
        idx_minimo=0
        for i in range(len(distancias)):
            if distancias[i] < distancias[idx_minimo]:
                idx_minimo = i
        
        color_final.append(paleta[idx_minimo])
    
    return np.array(color_final)


def pintar_bloque(img_array:np.ndarray, x:int, y:int, tam_bloque:int, color:np.ndarray) -> None:
    """Pinta todo el bloque con el color. Recibe un array de la imagen que se modifica directamente, las coordenadas 
    del bloque y el color a pintar. Pinta directamente la imagen, no devuelve nada."""
    alto, ancho = img_array.shape[:2]
    x_fin = min(x + tam_bloque, ancho)
    y_fin = min(y + tam_bloque, alto)
    #asigno el color al bloque completo 
    img_array[y:y_fin, x:x_fin] = color


def aplicar_pixel_art(ruta_imagen: str, tam_bloque: int, niveles_color: int) -> Image.Image:
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
