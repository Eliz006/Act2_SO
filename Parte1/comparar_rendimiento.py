"""
Script para comparar rendimiento entre versión secuencial y multihilo.
Ejecuta ambas versiones y genera tabla comparativa.
"""

import subprocess
import time
import sys

def ejecutar_y_medir(script, descripcion):
    """Ejecuta un script y mide su tiempo de ejecución."""
    print(f"\n{'='*60}")
    print(f"Ejecutando: {descripcion}")
    print(f"{'='*60}")
    
    inicio = time.time()
    resultado = subprocess.run([sys.executable, script], capture_output=True, text=True)
    fin = time.time()
    
    tiempo = fin - inicio
    
    print(resultado.stdout)
    if resultado.stderr:
        print("ERRORES:", resultado.stderr)
    
    return tiempo

def main():
    print("\n" + "="*60)
    print("COMPARACIÓN DE RENDIMIENTO - MANDELBROT")
    print("="*60)
    
    # Ejecutar versión secuencial
    tiempo_secuencial = ejecutar_y_medir("mandelbrot_secuencial.py", "Versión Secuencial (1 hilo)")
    
    # Ejecutar versión multihilo (ajusta el número de hilos en el archivo antes)
    tiempo_multihilo = ejecutar_y_medir("mandelbrot_multihilo.py", "Versión Multihilo")
    
    # Calcular speedup
    speedup = tiempo_secuencial / tiempo_multihilo
    eficiencia = speedup / 8 * 100  # Asumiendo 8 hilos
    
    # Mostrar tabla comparativa
    print("\n" + "="*60)
    print("RESULTADOS COMPARATIVOS")
    print("="*60)
    print(f"{'Versión':<30} {'Tiempo (s)':<15} {'Speedup':<10}")
    print("-"*60)
    print(f"{'Secuencial (1 hilo)':<30} {tiempo_secuencial:<15.2f} {'1.00x':<10}")
    print(f"{'Multihilo (8 hilos)':<30} {tiempo_multihilo:<15.2f} {f'{speedup:.2f}x':<10}")
    print("-"*60)
    print(f"\nSpeedup: {speedup:.2f}x")
    print(f"Eficiencia: {eficiencia:.1f}%")
    print(f"Reducción de tiempo: {((tiempo_secuencial - tiempo_multihilo) / tiempo_secuencial * 100):.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()
