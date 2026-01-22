# Generador de Fractales Mandelbrot

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

### Versión Secuencial (1 hilo)
```bash
python mandelbrot_secuencial.py
```

### Versión Multihilo (N hilos)
```bash
python mandelbrot_multihilo.py
```

Modifica `NUM_HILOS` dentro del archivo para probar con 2, 4, 8, 16 hilos.

### Comparación Automática
```bash
python comparar_rendimiento.py
```

Ejecuta ambas versiones y genera tabla comparativa con speedup.

## Parámetros Configurables

En `mandelbrot_multihilo.py`:
- `NUM_HILOS`: cantidad de hilos (2, 4, 8, 16, etc.)
- `ANCHO` y `ALTO`: resolución de la imagen
- `MAX_ITER`: iteraciones máximas

## Para el Informe

1. Ejecuta con diferentes números de hilos: 1, 2, 4, 8, 16
2. Toma captura del Task Manager mostrando uso de CPU
3. Anota tiempos para cada configuración
4. Calcula speedup = tiempo_secuencial / tiempo_multihilo

## Próximos Pasos

- ✅ Versión secuencial (Parte 1)
- ✅ Versión multihilo (Parte 1)
- ⏳ Algoritmos de planificación (Parte 2)
- ⏳ Versión distribuida con MPI (Parte 3)
