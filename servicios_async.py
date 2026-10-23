"""Servicios simulados de red y notificaciones asíncronas."""
from __future__ import annotations

import asyncio
import random
import time


class ErrorAntifraude(Exception):
    pass


async def enviar_notificacion(cuenta: int, mensaje: str) -> str:
    await asyncio.sleep(random.uniform(0.2, 1.0))
    return f"OK cuenta {cuenta}: {mensaje}"


async def consultar_antifraude(cuenta: int, monto: int) -> bool:
    await asyncio.sleep(random.uniform(0.2, 1.0))
    if random.random() < 0.05:
        raise ErrorAntifraude(f"Servicio antifraude no disponible (cuenta {cuenta})")
    return monto < 5_000_000


async def notificaciones_secuenciales(n: int) -> float:
    inicio = time.perf_counter()
    for i in range(n):
        await enviar_notificacion(i, "Movimiento registrado")
    return time.perf_counter() - inicio


# CORRECCIONES FASE 4: 
async def notificaciones_gather(n: int) -> float:
    inicio = time.perf_counter()
    await asyncio.gather(*(
        enviar_notificacion(i, "Movimiento registrado") for i in range(n)
    ))
    return time.perf_counter() - inicio



async def notificaciones_limitadas(n: int, limite: int = 20) -> float:
    semaforo = asyncio.Semaphore(limite)

    async def enviar(i: int):
        async with semaforo:
            return await enviar_notificacion(i, "Movimiento registrado")

    inicio = time.perf_counter()
    await asyncio.gather(*(enviar(i) for i in range(n)))
    return time.perf_counter() - inicio


async def antifraude_con_manejo_errores(n: int) -> dict[str, int]:
    async def revisar(i: int):
        try:
            aprobado = await consultar_antifraude(i, random.randint(1_000, 6_000_000))
            return "aprobada" if aprobado else "rechazada"
        except ErrorAntifraude:
            return "pendiente de revision"

    resultados = await asyncio.gather(*(revisar(i) for i in range(n)))
    return {
        "aprobada": resultados.count("aprobada"),
        "rechazada": resultados.count("rechazada"),
        "pendiente de revision": resultados.count("pendiente de revision"),
    }


async def ejemplo_bloqueo_incorrecto():
    time.sleep(0.5)


async def ejemplo_corregido():
    await asyncio.to_thread(time.sleep, 0.5)


async def comparar_notificaciones(n: int = 500):
    t_secuencial = await notificaciones_secuenciales(n)
    t_gather = await notificaciones_gather(n)
    t_limitado = await notificaciones_limitadas(n, 20)
    print("\nComparacion de notificaciones")
    print(f"Secuencial:       {t_secuencial:.2f} s")
    print(f"asyncio.gather:   {t_gather:.2f} s")
    print(f"Semaphore(20):    {t_limitado:.2f} s")
    return t_secuencial, t_gather, t_limitado
