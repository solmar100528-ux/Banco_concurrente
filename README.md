# Banco Andino Digital — Grupo 5

Proyecto de Programación Concurrente y Paralela en Python. Requiere Python 3.10 o superior y solo usa la biblioteca estándar.

## Parámetros del Grupo 5
- 15 cuentas bancarias
- 60 hilos de cajero
- 2.500 transferencias simultáneas
- 30.000 cuentas/historiales para auditar
- 500 notificaciones

## Archivos
- `cuenta.py`: cuenta bancaria, movimientos, `Lock`, depósitos y retiros seguros.
- `banco.py`: transferencias atómicas con orden fijo de candados.
- `auditoria.py`: auditoría secuencial, con hilos y con procesos; mide tiempos y speedup.
- `servicios_async.py`: notificaciones, `asyncio.gather`, límite con `Semaphore` y manejo de errores antifraude.
- `main.py`: integración de las fases.
- `test_banco.py`: pruebas automatizadas.
- `EXPLICACION_CORRECCIONES.md`: explicación de las modificaciones.

## Cómo ejecutar
Desde la carpeta del proyecto:

```bash
python --version
python -m unittest -v
python main.py
```

La auditoría oficial de 30.000 historiales puede tardar varios minutos. Para comprobar primero la integración con una muestra menor:

**Windows CMD**
```bat
set AUDIT_CUENTAS=1000
python main.py
```

**PowerShell**
```powershell
$env:AUDIT_CUENTAS="1000"
python main.py
```

En Linux/macOS:
```bash
AUDIT_CUENTAS=1000 python main.py
```

Para la entrega final, ejecuten de nuevo con el parámetro predeterminado de 30.000 y registren los tiempos reales en el informe.

## Medición
La fase de auditoría imprime tiempos de las tres versiones y speedup (tiempo secuencial / tiempo de cada versión). No inventen los tiempos: copien al informe los resultados que produzca el equipo donde se ejecute el programa.

## Integrantes
Completar con los cinco nombres y el rol asignado por el grupo.
