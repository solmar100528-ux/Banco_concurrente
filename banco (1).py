"""Operaciones del banco con transferencias seguras."""
from __future__ import annotations

import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from cuenta import CuentaBancaria, FondosInsuficientes, Movimiento


class Banco:
    def __init__(self) -> None:
        self.cuentas: dict[int, CuentaBancaria] = {}

    def abrir_cuenta(self, titular: str, saldo_inicial: int) -> CuentaBancaria:
        numero = len(self.cuentas) + 1
        cuenta = CuentaBancaria(numero, titular, saldo_inicial)
        self.cuentas[numero] = cuenta
        return cuenta

    def saldo_total(self) -> int:
        # Cada saldo se lee bajo su candado para obtener una lectura protegida.
        total = 0
        for cuenta in self.cuentas.values():
            with cuenta.lock:
                total += cuenta.saldo
        return total

    def transferir(self, origen: CuentaBancaria, destino: CuentaBancaria,
                   monto: int) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo.")
        if origen is destino:
            raise ValueError("La cuenta de origen y destino deben ser distintas.")

        #CORRECCIONES FASE 2: 
        primera, segunda = sorted((origen, destino), key=lambda c: c.numero)
        with primera.lock:
            with segunda.lock:
               
                if origen.saldo < monto:
                    raise FondosInsuficientes(
                        f"Cuenta {origen.numero} sin fondos suficientes."
                    )
                origen.saldo -= monto
                destino.saldo += monto
                origen.historial.append(Movimiento("TRANSFER_OUT", monto))
                destino.historial.append(Movimiento("TRANSFER_IN", monto))

    def transferencias_simultaneas(self, cantidad: int, semilla: int = 42) -> tuple[int, int]:
        """Ejecuta transferencias aleatorias y devuelve (total_antes, total_despues)."""
        if len(self.cuentas) < 2:
            raise ValueError("Se necesitan al menos dos cuentas.")

        rnd = random.Random(semilla)
        cuentas = list(self.cuentas.values())
        operaciones = []
        for _ in range(cantidad):
            origen, destino = rnd.sample(cuentas, 2)
            monto = rnd.randint(1, 500)
            operaciones.append((origen, destino, monto))

        total_antes = self.saldo_total()
        errores = 0

        def ejecutar(op):
            try:
                self.transferir(*op)
                return True
            except FondosInsuficientes:
                return False

       
        with ThreadPoolExecutor(max_workers=60) as executor:
            for resultado in executor.map(ejecutar, operaciones):
                if not resultado:
                    errores += 1

        total_despues = self.saldo_total()
        print(f"Transferencias rechazadas por falta de fondos: {errores}")
        return total_antes, total_despues
