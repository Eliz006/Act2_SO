"""
Implementación de cómputo distribuido usando MPI (Message Passing Interface)
Simula un clúster con múltiples nodos procesando en paralelo
"""

from mpi4py import MPI
import time
import sys

def calcular_subtarea(n, rank, size):
    """
    Cada nodo procesa su parte del trabajo total
    """
    inicio = time.time()
    
    # Dividir trabajo equitativamente
    elementos_por_nodo = n // size
    inicio_rango = rank * elementos_por_nodo
    fin_rango = inicio_rango + elementos_por_nodo
    
    # Simulación de procesamiento intensivo
    conteo = 0
    for i in range(inicio_rango, fin_rango):
        conteo += (i % 1000)  # Operación simple para simular carga
    
    fin = time.time()
    tiempo_local = fin - inicio
    
    return tiempo_local, conteo

def main():
    # Inicializar MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # ID del nodo actual (0, 1, 2, ...)
    size = comm.Get_size()  # Número total de nodos
    
    # Carga de trabajo total
    N_TOTAL = 100_000_000  # 100 millones de operaciones
    
    if rank == 0:
        print("="*70)
        print(f"EJECUCIÓN EN CLÚSTER DISTRIBUIDO")
        print("="*70)
        print(f"Nodos activos: {size}")
        print(f"Carga total: {N_TOTAL:,} operaciones")
        print(f"Carga por nodo: {N_TOTAL // size:,} operaciones")
        print("="*70)
        print(f"\nIniciando procesamiento distribuido...\n")
    
    # Sincronizar todos los nodos antes de empezar
    comm.Barrier()
    tiempo_inicio_global = MPI.Wtime()
    
    # Cada nodo procesa su parte
    tiempo_local, resultado_local = calcular_subtarea(N_TOTAL, rank, size)
    
    # Nodo maestro recolecta todos los tiempos
    todos_los_tiempos = comm.gather(tiempo_local, root=0)
    todos_los_resultados = comm.gather(resultado_local, root=0)
    
    # Sincronizar para medir tiempo total
    comm.Barrier()
    tiempo_fin_global = MPI.Wtime()
    
    # Solo el nodo maestro imprime resultados
    if rank == 0:
        tiempo_total = tiempo_fin_global - tiempo_inicio_global
        
        print("="*70)
        print("RESULTADOS POR NODO")
        print("="*70)
        print(f"{'Nodo':<8} {'Tiempo (s)':<15} {'Operaciones':<15} {'Ops/seg':<15}")
        print("-"*70)
        
        for i, (t, ops) in enumerate(zip(todos_los_tiempos, todos_los_resultados)):
            ops_por_seg = (N_TOTAL // size) / t if t > 0 else 0
            print(f"{i:<8} {t:<15.4f} {N_TOTAL // size:<15,} {ops_por_seg:<15,.0f}")
        
        print("-"*70)
        
        # Métricas de rendimiento
        tiempo_max = max(todos_los_tiempos)
        tiempo_min = min(todos_los_tiempos)
        tiempo_promedio = sum(todos_los_tiempos) / len(todos_los_tiempos)
        desbalance = ((tiempo_max - tiempo_min) / tiempo_promedio) * 100
        
        print(f"\nTiempo total de ejecución: {tiempo_total:.4f} s")
        print(f"Tiempo del nodo más rápido: {tiempo_min:.4f} s")
        print(f"Tiempo del nodo más lento: {tiempo_max:.4f} s")
        print(f"Tiempo promedio: {tiempo_promedio:.4f} s")
        print(f"Desbalance de carga: {desbalance:.2f}%")
        
        # Throughput del clúster
        throughput = N_TOTAL / tiempo_total
        print(f"\nThroughput del clúster: {throughput:,.0f} operaciones/segundo")
        
        # Eficiencia (comparado con ejecución teórica perfecta)
        eficiencia = (tiempo_promedio * size) / tiempo_total * 100
        print(f"Eficiencia de paralelización: {eficiencia:.2f}%")
        
        print("="*70)
        
        # Guardar métricas en archivo
        with open('metricas_cluster.txt', 'w') as f:
            f.write(f"MÉTRICAS DE CLÚSTER - {size} nodos\n")
            f.write("="*70 + "\n")
            f.write(f"Tiempo total: {tiempo_total:.4f} s\n")
            f.write(f"Throughput: {throughput:,.0f} ops/s\n")
            f.write(f"Eficiencia: {eficiencia:.2f}%\n")
            f.write(f"Desbalance: {desbalance:.2f}%\n")
            f.write(f"\nTiempos por nodo:\n")
            for i, t in enumerate(todos_los_tiempos):
                f.write(f"  Nodo {i}: {t:.4f} s\n")
        
        print("\n✓ Métricas guardadas en 'metricas_cluster.txt'")

if __name__ == "__main__":
    main()
