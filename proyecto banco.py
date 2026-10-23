"""Auditoria CPU-bound: version secuencial, con hilos y con procesos."""
from __future__ import annotations

import hashlib
import random
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Iterable


def generar_historiales(n_cuentas: int, movimientos: int = 40,
                        semilla: int = 42) -> list[list[tuple[str, int]]]:
    rnd = random.Random(semilla)
    historiales = []
    for _ in range(n_cuentas):
        historial = [("DEPOSITO", rnd.randint(10_000, 500_000))]
        for _ in range(movimientos - 1):
            historial.append(
                (rnd.choice(["DEPOSITO", "RETIRO"]), rnd.randint(1_000, 50_000))
            )
        historiales.append(historial)
    return historiales


def auditar_cuenta(historial: list[tuple[str, int]],
                   iteraciones: int = 2_000) -> tuple[int, str]:
    saldo = 0
    for tipo, monto in historial:
        saldo += monto if tipo == "DEPOSITO" else -monto

    digest = repr(historial).encode()
    for _ in range(iteraciones):
        digest = hashlib.sha256(digest).digest()
    return saldo, digest.hex()[:16]


def auditoria_secuencial(historiales: list[list[tuple[str, int]]],
                         iteraciones: int = 2_000) -> list[tuple[int, str]]:
    return [auditar_cuenta(h, iteraciones) for h in historiales]


#FASE 3 CORRECCIONES:
def auditoria_con_hilos(historiales: list[list[tuple[str, int]]],
                        workers: int, iteraciones: int = 2_000) -> list[tuple[int, str]]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_auditar_con_iteraciones,
                                 ((h, iteraciones) for h in historiales)))


def _auditar_con_iteraciones(argumentos: tuple[list[tuple[str, int]], int]):
    """Funcion a nivel de modulo: puede serializarse para enviarse a procesos."""
    historial, iteraciones = argumentos
    return auditar_cuenta(historial, iteraciones)



def auditoria_con_procesos(historiales: list[list[tuple[str, int]]],
                           workers: int, iteraciones: int = 2_000) -> list[tuple[int, str]]:
   
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_auditar_con_iteraciones,
                                 ((h, iteraciones) for h in historiales)))


def medir_tiempo(funcion, *args):
    inicio = time.perf_counter()
    resultado = funcion(*args)
    return resultado, time.perf_counter() - inicio


def comparar_versiones(historiales, workers: int, iteraciones: int = 2_000):
    resultados = {}
    for nombre, funcion, args in (
        ("Secuencial", auditoria_secuencial, (historiales, iteraciones)),
        ("Hilos", auditoria_con_hilos, (historiales, workers, iteraciones)),
        ("Procesos", auditoria_con_procesos, (historiales, workers, iteraciones)),
    ):
        _, segundos = medir_tiempo(funcion, *args)
        resultados[nombre] = segundos
    base = resultados["Secuencial"]
    print("\nComparacion de auditoria")
    print(f"{'Version':<15}{'Tiempo (s)':>12}{'Speedup':>12}")
    for nombre, segundos in resultados.items():
        print(f"{nombre:<15}{segundos:>12.2f}{base / segundos:>12.2f}x")
    return resultados
