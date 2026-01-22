"""
Generador de Conjunto de Mandelbrot - Versión Secuencial CON COLORES
Genera una imagen del fractal de Mandelbrot usando un solo hilo.
"""

import numpy as np
import time
from mandelbrot_utils import calcular_mandelbrot, guardar_imagen_color

def generar_mandelbrot_secuencial(ancho, alto, x_min, x_max, y_min, y_max, max_iter):
    """
    Genera la imagen completa del conjunto de Mandelbrot de forma secuencial.
    """
    imagen = np.zeros((alto, ancho))
    
    print(f"Generando imagen de {ancho}x{alto} pixels...")
    print(f"Calculando {ancho * alto:,} puntos de forma secuencial...")
    
    for fila in range(alto):
        if fila % 100 == 0:
            print(f"Procesando fila {fila}/{alto}...")
        
        for columna in range(ancho):
            x = x_min + (x_max - x_min) * columna / ancho
            y = y_min + (y_max - y_min) * fila / alto
            c = complex(x, y)
            imagen[fila, columna] = calcular_mandelbrot(c, max_iter)
    
    return imagen

if __name__ == "__main__":
    # PARÁMETROS
    ANCHO = 1920
    ALTO = 1080
    MAX_ITER = 256
    
    X_MIN, X_MAX = -2.5, 1.0
    Y_MIN, Y_MAX = -1.0, 1.0
    
    print("="*60)
    print("GENERADOR DE MANDELBROT - VERSIÓN SECUENCIAL (COLOR)")
    print("="*60)
    
    inicio = time.time()
    resultado = generar_mandelbrot_secuencial(ANCHO, ALTO, X_MIN, X_MAX, Y_MIN, Y_MAX, MAX_ITER)
    fin = time.time()
    tiempo_total = fin - inicio
    
    guardar_imagen_color(resultado, "mandelbrot_secuencial_color.png")
    
    print("="*60)
    print(f"TIEMPO TOTAL DE EJECUCIÓN: {tiempo_total:.2f} segundos")
    print(f"Pixels procesados: {ANCHO * ALTO:,}")
    print(f"Pixels por segundo: {(ANCHO * ALTO) / tiempo_total:,.0f}")
    print("="*60)
