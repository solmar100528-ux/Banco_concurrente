"""Pruebas automatizadas con unittest. Ejecutar: python -m unittest -v"""
import unittest
from concurrent.futures import ThreadPoolExecutor

from cuenta import CuentaBancaria, FondosInsuficientes
from banco import Banco


class PruebasBanco(unittest.TestCase):
    def test_depositos_con_hilos(self):
        cuenta = CuentaBancaria(1, "Prueba", 0)
        def cajero():
            for _ in range(200):
                cuenta.depositar(1)
        with ThreadPoolExecutor(max_workers=20) as ex:
            list(ex.map(lambda _: cajero(), range(20)))
        self.assertEqual(cuenta.saldo, 4000)

    def test_retiro_no_deja_saldo_negativo(self):
        cuenta = CuentaBancaria(1, "Prueba", 100)
        resultados = []
        def retirar():
            try:
                cuenta.retirar(80)
                resultados.append("ok")
            except FondosInsuficientes:
                resultados.append("sin_fondos")
        with ThreadPoolExecutor(max_workers=10) as ex:
            list(ex.map(lambda _: retirar(), range(10)))
        self.assertGreaterEqual(cuenta.saldo, 0)
        self.assertEqual(cuenta.saldo, 20)
        self.assertEqual(resultados.count("ok"), 1)

    def test_conservacion_transferencias(self):
        banco = Banco()
        cuentas = [banco.abrir_cuenta(f"Persona{i}", 10_000) for i in range(5)]
        antes = banco.saldo_total()
        banco.transferencias_simultaneas(300, semilla=123)
        despues = banco.saldo_total()
        self.assertEqual(antes, despues)
        self.assertTrue(all(c.saldo >= 0 for c in cuentas))

    def test_transferencia_atomica_y_fondos(self):
        banco = Banco()
        a = banco.abrir_cuenta("A", 100)
        b = banco.abrir_cuenta("B", 0)
        banco.transferir(a, b, 60)
        self.assertEqual((a.saldo, b.saldo), (40, 60))
        with self.assertRaises(FondosInsuficientes):
            banco.transferir(a, b, 50)


if __name__ == "__main__":
    unittest.main()
