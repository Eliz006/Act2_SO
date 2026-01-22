"""
Generador de Conjunto de Mandelbrot - Versión Multihilo CON COLORES
Genera una imagen del fractal de Mandelbrot usando múltiples hilos en paralelo.
"""

import numpy as np
import time
import threading
from mandelbrot_utils import calcular_mandelbrot, guardar_imagen_color

def procesar_filas(imagen, filas_inicio, filas_fin, ancho, alto, x_min, x_max, y_min, y_max, max_iter, thread_id):
    """
    Procesa un rango de filas de la imagen (trabajo de un hilo).
    """
    print(f"  Hilo {thread_id}: procesando filas {filas_inicio} a {filas_fin-1}")
    
    for fila in range(filas_inicio, filas_fin):
        for columna in range(ancho):
            x = x_min + (x_max - x_min) * columna / ancho
            y = y_min + (y_max - y_min) * fila / alto
            c = complex(x, y)
            imagen[fila, columna] = calcular_mandelbrot(c, max_iter)
    
    print(f"  Hilo {thread_id}: completado")

def generar_mandelbrot_multihilo(ancho, alto, x_min, x_max, y_min, y_max, max_iter, num_hilos):
    """
    Genera la imagen completa del conjunto de Mandelbrot usando múltiples hilos.
    """
    imagen = np.zeros((alto, ancho))
    
    print(f"Generando imagen de {ancho}x{alto} pixels usando {num_hilos} hilos...")
    print(f"Calculando {ancho * alto:,} puntos en paralelo...")
    
    filas_por_hilo = alto // num_hilos
    hilos = []
    
    print(f"\nDistribución de trabajo:")
    print(f"  Total de filas: {alto}")
    print(f"  Filas por hilo: ~{filas_por_hilo}")
    print(f"\nIniciando hilos...")
    
    for i in range(num_hilos):
        fila_inicio = i * filas_por_hilo
        fila_fin = alto if i == num_hilos - 1 else (i + 1) * filas_por_hilo
        
        hilo = threading.Thread(
            target=procesar_filas,
            args=(imagen, fila_inicio, fila_fin, ancho, alto, x_min, x_max, y_min, y_max, max_iter, i+1)
        )
        hilos.append(hilo)
        hilo.start()
    
    print(f"\nEsperando a que todos los hilos terminen...")
    for hilo in hilos:
        hilo.join()
    
    print(f"Todos los hilos completados\n")
    return imagen

if __name__ == "__main__":
    # PARÁMETROS
    ANCHO = 1920
    ALTO = 1080
    MAX_ITER = 256
    NUM_HILOS = 8  # CAMBIA ESTO: 2, 4, 8, 16, etc.
    
    X_MIN, X_MAX = -2.5, 1.0
    Y_MIN, Y_MAX = -1.0, 1.0
    
    print("="*60)
    print(f"GENERADOR DE MANDELBROT - MULTIHILO ({NUM_HILOS} hilos) COLOR")
    print("="*60)
    
    inicio = time.time()
    resultado = generar_mandelbrot_multihilo(ANCHO, ALTO, X_MIN, X_MAX, Y_MIN, Y_MAX, MAX_ITER, NUM_HILOS)
    fin = time.time()
    tiempo_total = fin - inicio
    
    nombre_archivo = f"mandelbrot_multihilo_{NUM_HILOS}hilos_color.png"
    guardar_imagen_color(resultado, nombre_archivo)
    
    print("="*60)
    print(f"TIEMPO TOTAL DE EJECUCIÓN: {tiempo_total:.2f} segundos")
    print(f"Número de hilos utilizados: {NUM_HILOS}")
    print(f"Pixels procesados: {ANCHO * ALTO:,}")
    print(f"Pixels por segundo: {(ANCHO * ALTO) / tiempo_total:,.0f}")
    print("="*60)
    print(f"\nPara calcular speedup: divide el tiempo secuencial entre {tiempo_total:.2f}")
