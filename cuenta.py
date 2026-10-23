"""Modelo de cuenta bancaria segura para el proyecto del Grupo 5."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime


class FondosInsuficientes(Exception):
    """Se lanza cuando un retiro o transferencia supera el saldo disponible."""


@dataclass
class Movimiento:
    tipo: str
    monto: int
    fecha: datetime = field(default_factory=datetime.now)


class CuentaBancaria:
    def __init__(self, numero: int, titular: str, saldo_inicial: int = 0) -> None:
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.numero = numero
        self.titular = titular
        self.saldo = saldo_inicial
        self.historial: list[Movimiento] = []
        self.lock = threading.Lock()

    def depositar(self, monto: int) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo.")

        #CORRECCIONES FASE 1:
        with self.lock:
            self.saldo += monto
            self.historial.append(Movimiento("DEPOSITO", monto))

    def retirar(self, monto: int) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo.")

      
        with self.lock:
            if self.saldo < monto:
                raise FondosInsuficientes(
                    f"Cuenta {self.numero}: saldo {self.saldo} < {monto}"
                )
            self.saldo -= monto
            self.historial.append(Movimiento("RETIRO", monto))

    def __repr__(self) -> str:
        return f"Cuenta({self.numero}, {self.titular}, saldo={self.saldo})"
