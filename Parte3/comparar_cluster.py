"""
Script para comparar rendimiento:
- Single Node (multihilo)
- Clúster distribuido (MPI)
"""
import threading
import time

def calcular_single_node(n_total, num_hilos):
    """
    Versión single-node usando múltiples hilos.
    Simula el mismo trabajo que el clúster pero en una máquina.
    """
    print(f"\n{'='*70}")
    print(f"EJECUTANDO: SINGLE NODE ({num_hilos} hilos)")
    print(f"{'='*70}")
    
    # Dividir trabajo entre hilos
    resultados = [0] * num_hilos
    
    def tarea(id_hilo, n_por_hilo):
        inicio = time.time()
        conteo = 0
        for _ in range(n_por_hilo):
            conteo += 1
        fin = time.time()
        resultados[id_hilo] = fin - inicio
    
    inicio_total = time.time()
    
    # Crear hilos
    hilos = []
    n_por_hilo = n_total // num_hilos
    for i in range(num_hilos):
        h = threading.Thread(target=tarea, args=(i, n_por_hilo))
        hilos.append(h)
        h.start()
    
    # Esperar que terminen
    for h in hilos:
        h.join()
    
    fin_total = time.time()
    tiempo_total = fin_total - inicio_total
    
    # Mostrar resultados
    print(f"\n{'Hilo':<10} {'Tiempo (s)':<15}")
    print(f"{'-'*70}")
    for i, t in enumerate(resultados):
        print(f"{i:<10} {t:<15.4f}")
    
    print(f"{'-'*70}")
    print(f"TIEMPO TOTAL SINGLE NODE: {tiempo_total:.4f}s")
    print(f"Throughput: {n_total/tiempo_total:,.0f} iteraciones/segundo")
    print(f"{'='*70}\n")
    
    return tiempo_total

if __name__ == "__main__":
    # Misma carga que el clúster
    n_total = 50_000_000
    num_hilos = 4  # Mismo número que nodos del clúster
    
    print("\n" + "="*70)
    print("COMPARACIÓN: SINGLE NODE vs CLÚSTER")
    print("="*70)
    print(f"\nCarga total: {n_total:,} iteraciones")
    print(f"División del trabajo: {num_hilos} partes\n")
    
    # Ejecutar versión single node
    tiempo_single = calcular_single_node(n_total, num_hilos)
    
    print("\nPara comparar con el clúster:")
    print(f"1. Ejecuta: mpirun -n {num_hilos} python3 cluster_mpi.py")
    print(f"2. Compara el tiempo del clúster vs single node ({tiempo_single:.4f}s)")
    print(f"\nSpeedup = Tiempo Single Node / Tiempo Clúster")
    print(f"Eficiencia = (Speedup / {num_hilos}) * 100%")
    print("\n" + "="*70)
