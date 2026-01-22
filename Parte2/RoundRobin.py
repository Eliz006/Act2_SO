import os
import threading
import time
import sched

# Definición de la carga de trabajo
def tarea_intensiva(id_hilo):
    inicio = time.time()
    print(f"--> Hilo {id_hilo} iniciado.")
    
    # Simulación de procesamiento (Cálculo matemático)
    conteo = 0
    for _ in range(10**7):
        conteo += 1
        
    fin = time.time()
    print(f"--- Hilo {id_hilo} finalizado en {fin - inicio:.4f} segundos.")

def simular_planificacion(politica_nombre):
    # Mapeo de políticas de Linux
    politicas = {
        "ROUND_ROBIN": os.SCHED_RR,
        "FIFO_RT": os.SCHED_FIFO,
        "NORMAL": os.SCHED_OTHER
    }
    
    politica = politicas[politica_nombre]
    
    # Configurar el proceso principal para usar la política elegida
    # 99 es la prioridad máxima para políticas de Tiempo Real
    param = os.sched_param(99 if politica != os.SCHED_OTHER else 0)
    
    try:
        os.sched_setscheduler(0, politica, param)
        print(f"\n=== Ejecutando con política: {politica_nombre} ===")
    except PermissionError:
        print("Error: Se requieren privilegios de sudo para cambiar políticas de scheduler.")
        return

    hilos = []
    for i in range(4):
        h = threading.Thread(target=tarea_intensiva, args=(i,))
        hilos.append(h)
        h.start()

    for h in hilos:
        h.join()

if __name__ == "__main__":
    # Simulación 1: Round Robin (Equitativo)
    simular_planificacion("ROUND_ROBIN")
    
    # Simulación 2: FIFO Tiempo Real (Prioridad absoluta)
    simular_planificacion("FIFO_RT")