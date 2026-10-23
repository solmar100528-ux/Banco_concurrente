"""Programa integrado del Grupo 5. Python 3.10+."""
import asyncio
import os
import time

from banco import Banco
from auditoria import generar_historiales, comparar_versiones
from servicios_async import comparar_notificaciones, antifraude_con_manejo_errores


# Parametros Grupo 5
CUENTAS = 15
HILOS_CAJERO = 60
TRANSFERENCIAS = 2500
CUENTAS_A_AUDITAR = 30000
NOTIFICACIONES = 500


def fase1():
    print("\n=== FASE 1: cajeros simultaneos ===")
    from cuenta import CuentaBancaria
    from concurrent.futures import ThreadPoolExecutor

    cuenta = CuentaBancaria(1, "Cuenta de prueba", 0)
    def cajero():
        for _ in range(1000):
            cuenta.depositar(1)

    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=HILOS_CAJERO) as ex:
        list(ex.map(lambda _: cajero(), range(HILOS_CAJERO)))
    esperado = HILOS_CAJERO * 1000
    print(f"Esperado: {esperado} | Obtenido: {cuenta.saldo} | "
          f"Correcto: {cuenta.saldo == esperado} | Tiempo: {time.perf_counter()-inicio:.2f}s")


def fase2(banco):
    print("\n=== FASE 2: transferencias sin deadlock ===")
    antes, despues = banco.transferencias_simultaneas(TRANSFERENCIAS)
    print(f"Saldo total antes: {antes} | despues: {despues}")
    print(f"Invariante de conservacion: {'CUMPLIDA' if antes == despues else 'FALLO'}")


def fase3():
    print("\n=== FASE 3: auditoria CPU-bound ===")
    cantidad = int(os.getenv("AUDIT_CUENTAS", str(CUENTAS_A_AUDITAR)))
    workers = os.cpu_count() or 1
    print(f"Generando {cantidad} historiales; workers disponibles: {workers}.")
    print("Esta fase puede tardar varios minutos con los 30.000 historiales del Grupo 5.")
    historiales = generar_historiales(cantidad)
    comparar_versiones(historiales, workers=workers, iteraciones=2000)


async def fase4():
    print("\n=== FASE 4: notificaciones y antifraude ===")
    await comparar_notificaciones(NOTIFICACIONES)
    resumen = await antifraude_con_manejo_errores(NOTIFICACIONES)
    print("Resultado de consultas antifraude:", resumen)


async def jornada():
    fase1()
    banco = Banco()
    for i in range(CUENTAS):
        banco.abrir_cuenta(f"Cliente {i+1}", 100_000)
    fase2(banco)
    fase3()
    await fase4()


# CORRECCIONES FASE 5: 
if __name__ == "__main__":
 asyncio.run(jornada())
