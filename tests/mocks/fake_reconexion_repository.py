"""
tests/mocks/fake_reconexion_repository.py — Repositorio falso en memoria
para testear ReconexionService sin depender de PostgreSQL real.

Simula el estado de un único suministro y registra qué acciones
fueron invocadas por el Service, para poder verificarlas en los
asserts (patrón: fixture + verificación de comportamiento).
"""


class FakeReconexionRepository:
    def __init__(self, suministro_estado: str, identificador_cuenta: str) -> None:
        self.suministro_estado = suministro_estado
        self.identificador_cuenta = identificador_cuenta
        self.reconexion_creada = False
        self.orden_corte_anulada = False

    def buscar_suministro_por_cuenta(self, identificador_cuenta: str) -> dict | None:
        if identificador_cuenta != self.identificador_cuenta:
            return None
        return {
            "id": "suministro-fake-id",
            "estado": self.suministro_estado,
        }

    def crear_reconexion(self, suministro_id: str) -> dict:
        self.reconexion_creada = True
        return {"id": "reconexion-fake-id", "estado": "asignada"}

    def anular_orden_corte(self, suministro_id: str) -> dict:
        self.orden_corte_anulada = True
        return {"id": "orden-corte-fake-id", "estado": "anulada"}
