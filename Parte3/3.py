from mpi4py import MPI
import time

# Inicializar el entorno MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # ID del nodo/proceso actual
size = comm.Get_size()  # Número total de nodos/procesos

def calcular_subtarea(n):
    inicio = time.time()
    # Cada nodo procesa una fracción de la carga total
    conteo = 0
    for _ in range(n // size):
        conteo += 1
    fin = time.time()
    return fin - inicio

# Carga de trabajo total
n_total = 50_000_000
tiempo_local = calcular_subtarea(n_total)

# El nodo Maestro (rank 0) recolecta los tiempos de todos los demás
todos_los_tiempos = comm.gather(tiempo_local, root=0)

if rank == 0:
    print(f"\n--- Resultados del Clúster Simulado ({size} Nodos) ---")
    for i, t in enumerate(todos_los_tiempos):
        print(f"Nodo {i}: Tiempo de ejecución = {t:.4f}s")
    print(f"Rendimiento Total: {max(todos_los_tiempos):.4f}s (tiempo del nodo más lento)")