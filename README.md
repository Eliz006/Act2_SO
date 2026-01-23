# Actividad 2 - Sistemas Operativos
## Implementación Multihilo, Planificación y Clúster

---

## 📋 RESUMEN DE LO QUE TIENES

### ✅ PARTE 1 - Aplicación Multihilo
**Archivos:**
- `mandelbrot_multihilo_color.py` - Versión paralela
- `mandelbrot_secuencial_color.py` - Versión secuencial  
- `comparar_rendimiento.py` - Script de comparación
- `mandelbrot_utils.py` - Utilidades compartidas

**Ejecutar:**
```bash
# En tu server Ubuntu
cd Parte1
python3 comparar_rendimiento.py
```

**Métricas que genera:**
- Tiempo secuencial vs multihilo
- Speedup
- Eficiencia
- Reducción de tiempo


---

### ✅ PARTE 2 - Algoritmos de Planificación
**Archivo:**
- `RoundRobin.py` - Compara Round Robin vs FIFO

**Ejecutar:**
```bash
# REQUIERE SUDO
cd Parte2
sudo python3 RoundRobin.py
```

**Métricas que genera:**
- ✅ Tiempo de espera por hilo
- ✅ Tiempo de respuesta  
- ✅ Throughput (tareas/segundo)
- ✅ Comparación entre ambos algoritmos


---

### ✅ PARTE 3 - Clúster Simulado
**Archivos:**
- `cluster_mpi.py` - Versión distribuida con MPI
- `comparar_cluster.py` - Versión single-node para comparar

**Ejecutar:**
```bash
cd Parte3

# 1. Primero ejecuta single-node
python3 comparar_cluster.py

# 2. Luego ejecuta el clúster con 4 nodos
mpirun -n 4 python3 cluster_mpi.py

# 3. Compara los tiempos
```

**Métricas que genera:**
- ✅ Tiempo por nodo
- ✅ Desbalance de carga
- ✅ Throughput del clúster
- ✅ Comparación single-node vs distribuido
- ✅ Speedup y eficiencia


---

### ✅ PARTE 4 - Gestión de E/S
**Archivo:**
- `COMANDOS.txt` - Lista de todos los comandos a ejecutar

**Ejecutar:**
```bash
cd Parte4

# Ejecuta los comandos del archivo COMANDOS.txt
# Captura screenshots de los resultados para tu reporte

lsblk
lspci  
iostat -x 2 3
cat /proc/interrupts
# ... etc (ver archivo completo)
```

**Qué incluye:**
- ✅ Comandos para identificar dispositivos
- ✅ Análisis de técnicas de E/S (programada/interrupciones/DMA)
- ✅ Justificación de cuál es mejor para tu app


---

## 🚀 ORDEN DE EJECUCIÓN RECOMENDADO

1. **Parte 1** - Corre `comparar_rendimiento.py` y toma screenshots
2. **Parte 2** - Corre `sudo python3 RoundRobin.py` y captura resultados
3. **Parte 3** - Ejecuta ambos scripts y compara
4. **Parte 4** - Ejecuta los comandos y documenta los resultados

---

## 📊 QUÉ MÉTRICAS VAS A REPORTAR

**Parte 1:**
- Tabla: Secuencial vs Multihilo (tiempo, speedup, eficiencia)

**Parte 2:**
- Tabla: Round Robin vs FIFO 
  - Tiempo de espera promedio
  - Tiempo de respuesta promedio
  - Throughput

**Parte 3:**
- Tabla: Single Node vs Clúster
  - Tiempo de ejecución
  - Speedup
  - Eficiencia
  - Desbalance de carga

**Parte 4:**
- Screenshots de comandos lsblk, lspci, iostat
- Análisis de qué técnica E/S es mejor (DMA recomendado)

---

## ⚠️ NOTAS IMPORTANTES

- Parte 2 REQUIERE `sudo` para cambiar políticas de scheduler
- Parte 3 requiere que tengas `mpi4py` instalado: `pip3 install mpi4py`
- Si `iostat` no existe, instala: `sudo apt install sysstat`
- Si `lsof` no existe, instala: `sudo apt install lsof`

---

## 📝 PARA TU REPORTE

Ya tienes TODO el código funcional. Solo falta:
1. Ejecutar todo en tu server Ubuntu
2. Tomar screenshots de los resultados
3. Copiar las tablas de métricas generadas
4. Escribir el análisis/conclusiones

El código ya genera las tablas formateadas que puedes copiar directo a tu reporte.
