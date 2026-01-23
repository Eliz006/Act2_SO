"""
Script para comparar rendimiento entre ejecución single-node y cluster
"""

import subprocess
import time
import os

def ejecutar_single_node():
    """Ejecuta la versión multihilo en un solo nodo"""
    print("\n" + "="*70)
    print("EJECUTANDO: SINGLE NODE (Multihilo)")
    print("="*70)
    
    # Ejecutar el script de mandelbrot multihilo de Parte1
    inicio = time.time()
    resultado = subprocess.run(
        ['python3', '../Parte1/mandelbrot_multihilo_color.py'],
        capture_output=True,
        text=True
    )
    fin = time.time()
    
    tiempo = fin - inicio
    print(resultado.stdout)
    
    return tiempo

def ejecutar_cluster(num_nodos):
    """Ejecuta la versión MPI con múltiples nodos simulados"""
    print("\n" + "="*70)
    print(f"EJECUTANDO: CLÚSTER ({num_nodos} nodos)")
    print("="*70)
    
    inicio = time.time()
    resultado = subprocess.run(
        ['mpiexec', '-n', str(num_nodos), 'python3', 'mandelbrot_cluster_mpi.py'],
        capture_output=True,
        text=True
    )
    fin = time.time()
    
    tiempo = fin - inicio
    print(resultado.stdout)
    if resultado.stderr:
        print("STDERR:", resultado.stderr)
    
    return tiempo

def main():
    print("\n" + "="*70)
    print("COMPARACIÓN: SINGLE NODE vs CLÚSTER DISTRIBUIDO")
    print("="*70)
    
    # Probar con diferentes configuraciones de clúster
    configuraciones = [
        ("Single Node", 1, ejecutar_single_node),
        ("Clúster 2 nodos", 2, lambda: ejecutar_cluster(2)),
        ("Clúster 4 nodos", 4, lambda: ejecutar_cluster(4)),
        ("Clúster 8 nodos", 8, lambda: ejecutar_cluster(8)),
    ]
    
    resultados = []
    
    for nombre, num_nodos, funcion in configuraciones:
        try:
            if "Single" in nombre:
                tiempo = funcion()
            else:
                tiempo = funcion()
            resultados.append((nombre, num_nodos, tiempo))
        except Exception as e:
            print(f"\n⚠️  Error ejecutando {nombre}: {e}")
            resultados.append((nombre, num_nodos, None))
        
        time.sleep(2)  # Pausa entre ejecuciones
    
    # Mostrar tabla comparativa
    print("\n" + "="*70)
    print("RESULTADOS COMPARATIVOS")
    print("="*70)
    print(f"{'Configuración':<25} {'Nodos':<8} {'Tiempo (s)':<12} {'Speedup':<10} {'Eficiencia':<12}")
    print("-"*70)
    
    tiempo_base = resultados[0][2] if resultados[0][2] else 1
    
    for nombre, nodos, tiempo in resultados:
        if tiempo:
            speedup = tiempo_base / tiempo
            eficiencia = (speedup / nodos) * 100
            print(f"{nombre:<25} {nodos:<8} {tiempo:<12.2f} {speedup:<10.2f}x {eficiencia:<12.1f}%")
        else:
            print(f"{nombre:<25} {nodos:<8} {'ERROR':<12} {'-':<10} {'-':<12}")
    
    print("="*70)
    
    # Análisis
    print("\nANÁLISIS:")
    print("-"*70)
    print("Speedup: Aceleración respecto a single node")
    print("Eficiencia: Qué tan bien se aprovecha cada nodo adicional")
    print("\nIdeal: Eficiencia cercana a 100% indica paralelización perfecta")
    print("Real: Eficiencia < 100% debido a overhead de comunicación MPI")
    print("="*70)

if __name__ == "__main__":
    main()
