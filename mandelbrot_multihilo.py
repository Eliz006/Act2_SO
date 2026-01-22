"""
Generador de Conjunto de Mandelbrot - Versión Multihilo
Genera una imagen del fractal de Mandelbrot usando múltiples hilos en paralelo.
"""

import numpy as np
from PIL import Image
import time
import threading
from queue import Queue

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
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def procesar_filas(imagen, filas_inicio, filas_fin, ancho, alto, x_min, x_max, y_min, y_max, max_iter, thread_id):
    """
    Procesa un rango de filas de la imagen (trabajo de un hilo).
    
    Args:
        imagen: matriz compartida donde escribir resultados
        filas_inicio, filas_fin: rango de filas que este hilo debe procesar
        ancho, alto: dimensiones totales de la imagen
        x_min, x_max, y_min, y_max: rango del plano complejo
        max_iter: máximo número de iteraciones
        thread_id: identificador del hilo (para debug)
    """
    print(f"  Hilo {thread_id}: procesando filas {filas_inicio} a {filas_fin-1}")
    
    for fila in range(filas_inicio, filas_fin):
        for columna in range(ancho):
            # Convertir coordenadas de pixel a coordenadas del plano complejo
            x = x_min + (x_max - x_min) * columna / ancho
            y = y_min + (y_max - y_min) * fila / alto
            c = complex(x, y)
            
            # Calcular cuántas iteraciones toma escapar
            imagen[fila, columna] = calcular_mandelbrot(c, max_iter)
    
    print(f"  Hilo {thread_id}: completado")

def generar_mandelbrot_multihilo(ancho, alto, x_min, x_max, y_min, y_max, max_iter, num_hilos):
    """
    Genera la imagen completa del conjunto de Mandelbrot usando múltiples hilos.
    
    Args:
        ancho, alto: dimensiones de la imagen en pixels
        x_min, x_max, y_min, y_max: rango del plano complejo a visualizar
        max_iter: máximo número de iteraciones por pixel
        num_hilos: número de hilos a utilizar
    
    Returns:
        array numpy con los valores de escape para cada pixel
    """
    # Crear matriz compartida para almacenar resultados
    imagen = np.zeros((alto, ancho))
    
    print(f"Generando imagen de {ancho}x{alto} pixels usando {num_hilos} hilos...")
    print(f"Calculando {ancho * alto:,} puntos en paralelo...")
    
    # Dividir el trabajo: calcular cuántas filas procesa cada hilo
    filas_por_hilo = alto // num_hilos
    hilos = []
    
    print(f"\nDistribución de trabajo:")
    print(f"  Total de filas: {alto}")
    print(f"  Filas por hilo: ~{filas_por_hilo}")
    print(f"\nIniciando hilos...")
    
    # Crear y lanzar hilos
    for i in range(num_hilos):
        # Calcular rango de filas para este hilo
        fila_inicio = i * filas_por_hilo
        
        # El último hilo procesa todas las filas restantes
        if i == num_hilos - 1:
            fila_fin = alto
        else:
            fila_fin = (i + 1) * filas_por_hilo
        
        # Crear hilo con su trabajo asignado
        hilo = threading.Thread(
            target=procesar_filas,
            args=(imagen, fila_inicio, fila_fin, ancho, alto, x_min, x_max, y_min, y_max, max_iter, i+1)
        )
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos los hilos terminen (sincronización)
    print(f"\nEsperando a que todos los hilos terminen...")
    for hilo in hilos:
        hilo.join()  # Bloquea hasta que el hilo termine
    
    print(f"Todos los hilos completados\n")
    
    return imagen

def guardar_imagen(datos, nombre_archivo):
    """
    Guarda los datos del Mandelbrot como imagen PNG con colores.
    
    Args:
        datos: array numpy con valores de iteraciones
        nombre_archivo: nombre del archivo a guardar
    """
    datos_norm = (datos / datos.max() * 255).astype(np.uint8)
    img = Image.fromarray(datos_norm, mode='L')
    img = img.convert('RGB')
    img.save(nombre_archivo)
    print(f"Imagen guardada como: {nombre_archivo}")

if __name__ == "__main__":
    # PARÁMETROS CONFIGURABLES
    ANCHO = 1920
    ALTO = 1080
    MAX_ITER = 256
    NUM_HILOS = 8  # CAMBIA ESTE VALOR PARA PROBAR: 2, 4, 8, 16, etc.
    
    # Rango del plano complejo
    X_MIN, X_MAX = -2.5, 1.0
    Y_MIN, Y_MAX = -1.0, 1.0
    
    print("="*60)
    print(f"GENERADOR DE MANDELBROT - VERSIÓN MULTIHILO ({NUM_HILOS} hilos)")
    print("="*60)
    
    # Medir tiempo de ejecución
    inicio = time.time()
    
    # Generar el conjunto de Mandelbrot en paralelo
    resultado = generar_mandelbrot_multihilo(ANCHO, ALTO, X_MIN, X_MAX, Y_MIN, Y_MAX, MAX_ITER, NUM_HILOS)
    
    # Calcular tiempo transcurrido
    fin = time.time()
    tiempo_total = fin - inicio
    
    # Guardar imagen
    nombre_archivo = f"mandelbrot_multihilo_{NUM_HILOS}hilos.png"
    guardar_imagen(resultado, nombre_archivo)
    
    # Mostrar resultados
    print("="*60)
    print(f"TIEMPO TOTAL DE EJECUCIÓN: {tiempo_total:.2f} segundos")
    print(f"Número de hilos utilizados: {NUM_HILOS}")
    print(f"Pixels procesados: {ANCHO * ALTO:,}")
    print(f"Pixels por segundo: {(ANCHO * ALTO) / tiempo_total:,.0f}")
    print("="*60)
    
    # NOTA: Para calcular el speedup, anota el tiempo de la versión secuencial
    # y divide: speedup = tiempo_secuencial / tiempo_multihilo
    print(f"\nPara calcular speedup: divide el tiempo secuencial entre {tiempo_total:.2f}")
