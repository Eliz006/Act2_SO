"""
Generador de Conjunto de Mandelbrot - Versión Secuencial
Genera una imagen del fractal de Mandelbrot usando un solo hilo.
"""

import numpy as np
from PIL import Image
import time

import psutil
import os

proceso = psutil.Process(os.getpid())
print(f"CPU cores disponibles: {psutil.cpu_count()}")
print(f"Memoria inicial: {proceso.memory_info().rss / 1024 / 1024:.2f} MB")


def calcular_mandelbrot(c, max_iter):
    """
    Calcula cuántas iteraciones toma para que un punto escape del conjunto de Mandelbrot.
    
    Args:
        c: número complejo (posición del pixel)
        max_iter: número máximo de iteraciones a probar
    
    Returns:
        número de iteraciones antes de que el punto escape (o max_iter si nunca escapa)
    """
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:  # Si el número crece más allá de 2, sabemos que va a infinito
            return n
        z = z*z + c  # Fórmula de Mandelbrot: z = z² + c
    return max_iter

def generar_mandelbrot_secuencial(ancho, alto, x_min, x_max, y_min, y_max, max_iter):
    """
    Genera la imagen completa del conjunto de Mandelbrot de forma secuencial.
    
    Args:
        ancho, alto: dimensiones de la imagen en pixels
        x_min, x_max, y_min, y_max: rango del plano complejo a visualizar
        max_iter: máximo número de iteraciones por pixel
    
    Returns:
        array numpy con los valores de escape para cada pixel
    """
    # Crear matriz para almacenar resultados
    imagen = np.zeros((alto, ancho))
    
    print(f"Generando imagen de {ancho}x{alto} pixels...")
    print(f"Calculando {ancho * alto:,} puntos de forma secuencial...")
    
    # Recorrer cada pixel de la imagen
    for fila in range(alto):
        if fila % 100 == 0:  # Mostrar progreso cada 100 filas
            print(f"Procesando fila {fila}/{alto}...")
        
        for columna in range(ancho):
            # Convertir coordenadas de pixel a coordenadas del plano complejo
            x = x_min + (x_max - x_min) * columna / ancho
            y = y_min + (y_max - y_min) * fila / alto
            c = complex(x, y)
            
            # Calcular cuántas iteraciones toma escapar
            imagen[fila, columna] = calcular_mandelbrot(c, max_iter)
    
    return imagen

def guardar_imagen(datos, nombre_archivo):
    """
    Guarda los datos del Mandelbrot como imagen PNG con colores.
    
    Args:
        datos: array numpy con valores de iteraciones
        nombre_archivo: nombre del archivo a guardar
    """
    # Normalizar valores a rango 0-255 para colores
    datos_norm = (datos / datos.max() * 255).astype(np.uint8)
    
    # Crear imagen en modo RGB para tener colores
    img = Image.fromarray(datos_norm, mode='L')  # 'L' es escala de grises
    img = img.convert('RGB')
    
    # Guardar
    img.save(nombre_archivo)
    print(f"Imagen guardada como: {nombre_archivo}")

if __name__ == "__main__":
    # PARÁMETROS CONFIGURABLES
    ANCHO = 1920      # Ancho de imagen en pixels
    ALTO = 1080       # Alto de imagen en pixels
    MAX_ITER = 256    # Máximo de iteraciones (más = más detalle pero más lento)
    
    # Rango del plano complejo a visualizar (vista clásica de Mandelbrot)
    X_MIN, X_MAX = -2.5, 1.0
    Y_MIN, Y_MAX = -1.0, 1.0
    
    print("="*60)
    print("GENERADOR DE MANDELBROT - VERSIÓN SECUENCIAL")
    print("="*60)
    
    # Medir tiempo de ejecución
    inicio = time.time()
    
    # Generar el conjunto de Mandelbrot
    resultado = generar_mandelbrot_secuencial(ANCHO, ALTO, X_MIN, X_MAX, Y_MIN, Y_MAX, MAX_ITER)
    
    # Calcular tiempo transcurrido
    fin = time.time()
    tiempo_total = fin - inicio
    
    # Guardar imagen
    guardar_imagen(resultado, "mandelbrot_secuencial.png")
    
    # Mostrar resultados
    print("="*60)
    print(f"TIEMPO TOTAL DE EJECUCIÓN: {tiempo_total:.2f} segundos")
    print(f"Pixels procesados: {ANCHO * ALTO:,}")
    print(f"Pixels por segundo: {(ANCHO * ALTO) / tiempo_total:,.0f}")
    print("="*60)

# Después de generar
print(f"Memoria final: {proceso.memory_info().rss / 1024 / 1024:.2f} MB")
