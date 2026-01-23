from mpi4py import MPI
import time

# Inicializar el entorno MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # ID del nodo/proceso actual
size = comm.Get_size()  # Número total de nodos/procesos

def calcular_subtarea(n):
    """
    Cada nodo procesa una fracción de la carga total.
    Simula procesamiento intensivo de CPU.
    """
    inicio = time.time()
    conteo = 0
    for _ in range(n // size):
        conteo += 1
    fin = time.time()
    return fin - inicio

# Carga de trabajo total
n_total = 50_000_000

# Tiempo individual de cada nodo
tiempo_local = calcular_subtarea(n_total)

# El nodo Maestro (rank 0) recolecta los tiempos de todos los demás
todos_los_tiempos = comm.gather(tiempo_local, root=0)

if rank == 0:
    print(f"\n{'='*70}")
    print(f"RESULTADOS DEL CLÚSTER SIMULADO ({size} Nodos)")
    print(f"{'='*70}")
    print(f"\n{'Nodo':<10} {'Tiempo (s)':<15} {'Carga procesada':<20}")
    print(f"{'-'*70}")
    
    for i, t in enumerate(todos_los_tiempos):
        carga = n_total // size
        print(f"{i:<10} {t:<15.4f} {carga:,} iteraciones")
    
    # Métricas del clúster
    tiempo_max = max(todos_los_tiempos)
    tiempo_min = min(todos_los_tiempos)
    tiempo_prom = sum(todos_los_tiempos) / len(todos_los_tiempos)
    
    print(f"{'-'*70}")
    print(f"\nMÉTRICAS DE RENDIMIENTO:")
    print(f"  Tiempo máximo (cuello de botella): {tiempo_max:.4f}s")
    print(f"  Tiempo mínimo: {tiempo_min:.4f}s")
    print(f"  Tiempo promedio: {tiempo_prom:.4f}s")
    print(f"  Desbalance de carga: {((tiempo_max - tiempo_min) / tiempo_max * 100):.2f}%")
    
    # Throughput del clúster
    throughput = n_total / tiempo_max
    print(f"  Throughput: {throughput:,.0f} iteraciones/segundo")
    
    print(f"\n{'='*70}")
    print(f"TIEMPO TOTAL DEL CLÚSTER: {tiempo_max:.4f}s")
    print(f"({'El nodo más lento determina el tiempo total'})")
    print(f"{'='*70}\n")
