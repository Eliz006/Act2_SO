"""
Funciones compartidas para generar imágenes con colores del fractal de Mandelbrot.
"""

import numpy as np
from PIL import Image

def calcular_mandelbrot(c, max_iter):
    """
    Calcula cuántas iteraciones toma para que un punto escape del conjunto de Mandelbrot.
    """
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def guardar_imagen_color(datos, nombre_archivo):
    """
    Guarda los datos del Mandelbrot como imagen PNG con colores vibrantes.
    
    Aplica un mapa de colores personalizado que hace el fractal mucho más visual.
    """
    # Normalizar datos
    datos_norm = datos / datos.max()
    
    # Crear imagen RGB
    alto, ancho = datos.shape
    imagen_rgb = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # Aplicar mapa de colores personalizado (estilo clásico de Mandelbrot)
    for i in range(alto):
        for j in range(ancho):
            valor = datos_norm[i, j]
            
            if valor == 1.0:  # Puntos que nunca escapan (dentro del conjunto)
                # Negro
                imagen_rgb[i, j] = [0, 0, 0]
            else:
                # Crear gradiente de colores basado en velocidad de escape
                t = valor % 1.0  # Usar módulo para crear patrón repetitivo
                
                # Fórmula de colores que crea ese efecto azul-morado-naranja típico
                r = int(9 * (1 - t) * t**3 * 255)
                g = int(15 * (1 - t)**2 * t**2 * 255)
                b = int(8.5 * (1 - t)**3 * t * 255)
                
                # Asegurar que los valores estén en rango 0-255
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                imagen_rgb[i, j] = [r, g, b]
    
    # Guardar
    img = Image.fromarray(imagen_rgb, mode='RGB')
    img.save(nombre_archivo)
    print(f"Imagen guardada como: {nombre_archivo}")
