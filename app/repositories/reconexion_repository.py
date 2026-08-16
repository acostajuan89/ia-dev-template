"""
app/repositories/reconexion_repository.py — Acceso a datos para el
proceso de reconexión.

NOTA IMPORTANTE: esta es una implementación EN MEMORIA, temporal,
para efectos del Lab 3 (foco en testing y separación de capas, no en
integración real con PostgreSQL). La conexión real a base de datos
(SQLAlchemy + tabla `suministro` del ERD) queda como trabajo futuro
fuera de alcance de este laboratorio.

Precarga datos sintéticos para poder probar el endpoint manualmente.
"""
import uuid


class InMemoryReconexionRepository:
    def __init__(self) -> None:
        # Datos sintéticos de ejemplo (no reales, solo para demo/pruebas manuales)
        self._suministros = {
            "CTA-001": {"id": str(uuid.uuid4()), "estado": "cortado"},
            "CTA-002": {"id": str(uuid.uuid4()), "estado": "asignado"},
        }

    def buscar_suministro_por_cuenta(self, identificador_cuenta: str) -> dict | None:
        return self._suministros.get(identificador_cuenta)

    def crear_reconexion(self, suministro_id: str) -> dict:
        self._actualizar_estado(suministro_id, "reconexion_asignada")
        return {"id": str(uuid.uuid4()), "estado": "asignada"}

    def anular_orden_corte(self, suministro_id: str) -> dict:
        self._actualizar_estado(suministro_id, "corte_anulado")
        return {"id": str(uuid.uuid4()), "estado": "anulada"}

    def _actualizar_estado(self, suministro_id: str, nuevo_estado: str) -> None:
        for datos in self._suministros.values():
            if datos["id"] == suministro_id:
                datos["estado"] = nuevo_estado
                break