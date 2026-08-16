"""
app/services/reconexion_service.py — Lógica de negocio (invariantes de
dominio) para procesar el evento de pago notificado por COBOL.

Reglas (PRD Historia 4/5, ADR-0001):
    1. Si el suministro asociado está "cortado" -> genera reconexión.
    2. Si el suministro asociado está "asignado" (corte no
       efectivizado) -> anula la orden de corte.

Fuera de alcance en este Lab 3: caso de identificador_cuenta sin
suministro asociado (bandeja de verificación, de solo lectura).
"""
from app.schemas.reconexion import (
    AnulacionCorteResponse,
    PagoNotificadoRequest,
    PagoProcesadoResponse,
    ReconexionResponse,
)


class SuministroNoEncontradoError(Exception):
    """El identificador_cuenta no corresponde a ningún suministro."""
    pass


class ReconexionService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def procesar_pago(self, request: PagoNotificadoRequest) -> PagoProcesadoResponse:
        suministro = self.repository.buscar_suministro_por_cuenta(
            request.identificador_cuenta
        )

        if suministro is None:
            raise SuministroNoEncontradoError(
                f"Cuenta {request.identificador_cuenta} sin suministro activo"
            )

        if suministro["estado"] == "cortado":
            reconexion = self.repository.crear_reconexion(suministro["id"])
            return PagoProcesadoResponse(
                accion="reconexion",
                detalle=ReconexionResponse(
                    reconexion_id=reconexion["id"],
                    suministro_id=suministro["id"],
                    estado=reconexion["estado"],
                ),
            )

        if suministro["estado"] == "asignado":
            orden_anulada = self.repository.anular_orden_corte(suministro["id"])
            return PagoProcesadoResponse(
                accion="anulacion",
                detalle=AnulacionCorteResponse(
                    orden_corte_id=orden_anulada["id"],
                    suministro_id=suministro["id"],
                    estado=orden_anulada["estado"],
                ),
            )

        raise ValueError(
            f"Estado '{suministro['estado']}' no soportado para procesar pago"
        )
