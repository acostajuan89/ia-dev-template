"""
tests/test_reconexion_service.py — Suite de tests para
app/services/reconexion_service.py (Lab 3).

Cubre las dos reglas de negocio confirmadas en el PRD/ADR-0001:
    1. Suministro "cortado" -> se genera la reconexión.
    2. Suministro "asignado" (corte no efectivizado) -> se anula
       la orden de corte.

Nota: este archivo se escribe ANTES de que exista la implementación
(app/services/reconexion_service.py). Al ejecutar pytest ahora, debe
FALLAR por ImportError — esa es la Pantalla Roja esperada.
"""
from app.services.reconexion_service import ReconexionService
from app.schemas.reconexion import PagoNotificadoRequest
from tests.mocks.fake_reconexion_repository import FakeReconexionRepository


# ─── Caso 1: suministro cortado → genera reconexión ──────────────────
def test_genera_reconexion_cuando_suministro_esta_cortado() -> None:
    # Arrange
    repo = FakeReconexionRepository(
        suministro_estado="cortado",
        identificador_cuenta="CTA-001",
    )
    service = ReconexionService(repository=repo)

    # Act
    result = service.procesar_pago(
        PagoNotificadoRequest(
            nro_comprobante="COMP-123",
            identificador_cuenta="CTA-001",
        )
    )

    # Assert
    assert result.accion == "reconexion"
    assert repo.reconexion_creada is True
    assert repo.orden_corte_anulada is False


# ─── Caso 2: suministro asignado (corte no efectivizado) → anula ─────
def test_anula_orden_corte_cuando_suministro_esta_asignado() -> None:
    # Arrange
    repo = FakeReconexionRepository(
        suministro_estado="asignado",
        identificador_cuenta="CTA-002",
    )
    service = ReconexionService(repository=repo)

    # Act
    result = service.procesar_pago(
        PagoNotificadoRequest(
            nro_comprobante="COMP-456",
            identificador_cuenta="CTA-002",
        )
    )

    # Assert
    assert result.accion == "anulacion"
    assert repo.orden_corte_anulada is True
    assert repo.reconexion_creada is False