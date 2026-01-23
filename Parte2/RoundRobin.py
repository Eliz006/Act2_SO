import os
import threading
import time

# Métricas globales por hilo
metricas = {}
lock = threading.Lock()

# Definición de la carga de trabajo
def tarea_intensiva(id_hilo, tiempo_creacion):
    """
    Tarea intensiva que registra métricas de rendimiento.
    
    Métricas:
    - Tiempo de espera: tiempo desde creación hasta que inicia ejecución
    - Tiempo de ejecución: duración de la tarea
    - Tiempo de respuesta: tiempo total (espera + ejecución)
    """
    tiempo_inicio_ejecucion = time.time()
    tiempo_espera = tiempo_inicio_ejecucion - tiempo_creacion
    
    print(f"--> Hilo {id_hilo} iniciado (esperó {tiempo_espera*1000:.2f}ms)")
    
    # Simulación de procesamiento (Cálculo matemático)
    conteo = 0
    for _ in range(10**7):
        conteo += 1
        
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio_ejecucion
    tiempo_respuesta = tiempo_fin - tiempo_creacion
    
    # Registrar métricas de forma thread-safe
    with lock:
        metricas[id_hilo] = {
            'tiempo_espera': tiempo_espera,
            'tiempo_ejecucion': tiempo_ejecucion,
            'tiempo_respuesta': tiempo_respuesta
        }
    
    print(f"--- Hilo {id_hilo} finalizado (ejecutó {tiempo_ejecucion:.4f}s)")

def simular_planificacion(politica_nombre):
    """
    Simula la planificación de hilos con diferentes políticas del SO.
    Registra y compara métricas de rendimiento.
    """
    global metricas
    metricas = {}  # Resetear métricas
    
    # Mapeo de políticas de Linux
    politicas = {
        "ROUND_ROBIN": os.SCHED_RR,
        "FIFO_RT": os.SCHED_FIFO
    }
    
    politica = politicas[politica_nombre]
    
    # Configurar el proceso principal para usar la política elegida
    # 99 es la prioridad máxima para políticas de Tiempo Real
    param = os.sched_param(99 if politica != os.SCHED_OTHER else 0)
    
    try:
        os.sched_setscheduler(0, politica, param)
        print(f"\n{'='*70}")
        print(f"EJECUTANDO CON POLÍTICA: {politica_nombre}")
        print(f"{'='*70}")
    except PermissionError:
        print("\n⚠️  Error: Se requieren privilegios de sudo para cambiar políticas.")
        print("   Ejecuta: sudo python3 RoundRobin.py")
        return None

    # Tiempo de inicio del experimento
    tiempo_inicio_experimento = time.time()
    
    # Crear e iniciar hilos
    hilos = []
    for i in range(4):
        tiempo_creacion = time.time()
        h = threading.Thread(target=tarea_intensiva, args=(i, tiempo_creacion))
        hilos.append(h)
        h.start()

    # Esperar que todos terminen
    for h in hilos:
        h.join()
    
    tiempo_fin_experimento = time.time()
    tiempo_total = tiempo_fin_experimento - tiempo_inicio_experimento
    
    # Calcular estadísticas
    mostrar_metricas(politica_nombre, tiempo_total)
    
    return metricas

def mostrar_metricas(politica, tiempo_total):
    """Muestra tabla de métricas calculadas."""
    print(f"\n{'-'*70}")
    print(f"MÉTRICAS DE RENDIMIENTO - {politica}")
    print(f"{'-'*70}")
    print(f"{'Hilo':<10} {'Espera (ms)':<15} {'Ejecución (s)':<15} {'Respuesta (s)':<15}")
    print(f"{'-'*70}")
    
    total_espera = 0
    total_respuesta = 0
    
    for hilo_id in sorted(metricas.keys()):
        m = metricas[hilo_id]
        print(f"{hilo_id:<10} {m['tiempo_espera']*1000:<15.2f} "
              f"{m['tiempo_ejecucion']:<15.4f} {m['tiempo_respuesta']:<15.4f}")
        total_espera += m['tiempo_espera']
        total_respuesta += m['tiempo_respuesta']
    
    # Promedios
    num_hilos = len(metricas)
    promedio_espera = (total_espera / num_hilos) * 1000
    promedio_respuesta = total_respuesta / num_hilos
    throughput = num_hilos / tiempo_total
    
    print(f"{'-'*70}")
    print(f"{'PROMEDIOS':<10} {promedio_espera:<15.2f} {'':<15} {promedio_respuesta:<15.4f}")
    print(f"{'-'*70}")
    print(f"\nThroughput: {throughput:.2f} tareas/segundo")
    print(f"Tiempo total del experimento: {tiempo_total:.4f}s")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPARACIÓN DE ALGORITMOS DE PLANIFICACIÓN DE PROCESOS")
    print("="*70)
    print("\nNOTA: Este script requiere privilegios de root/sudo")
    print("Ejecuta: sudo python3 RoundRobin.py\n")
    
    # Almacenar resultados para comparación final
    resultados = {}
    
    # Simulación 1: Round Robin (Equitativo - Quantum fijo)
    resultado_rr = simular_planificacion("ROUND_ROBIN")
    if resultado_rr:
        resultados["ROUND_ROBIN"] = resultado_rr
    
    # Simulación 2: FIFO Tiempo Real (Prioridad absoluta - No interrumpe)
    resultado_fifo = simular_planificacion("FIFO_RT")
    if resultado_fifo:
        resultados["FIFO_RT"] = resultado_fifo
    
    # Comparación final
    if len(resultados) == 2:
        print("\n" + "="*70)
        print("COMPARACIÓN ENTRE ALGORITMOS")
        print("="*70)
        
        for politica, metricas_pol in resultados.items():
            espera_prom = sum(m['tiempo_espera'] for m in metricas_pol.values()) / len(metricas_pol) * 1000
            respuesta_prom = sum(m['tiempo_respuesta'] for m in metricas_pol.values()) / len(metricas_pol)
            
            print(f"\n{politica}:")
            print(f"  Tiempo de espera promedio: {espera_prom:.2f}ms")
            print(f"  Tiempo de respuesta promedio: {respuesta_prom:.4f}s")
        
        print("\n" + "="*70)
