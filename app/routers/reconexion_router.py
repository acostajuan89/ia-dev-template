"""
app/routers/reconexion_router.py — Endpoint HTTP para el evento de
pago notificado por COBOL.

Responsabilidad única: recibir el request HTTP, delegar al Service,
y traducir errores de dominio a códigos de estado HTTP. NO contiene
lógica de negocio ni acceso a datos.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.reconexion import PagoNotificadoRequest, PagoProcesadoResponse
from app.services.reconexion_service import (
    ReconexionService,
    SuministroNoEncontradoError,
)
from app.repositories.reconexion_repository import InMemoryReconexionRepository

router = APIRouter(prefix="/pagos", tags=["Reconexion"])

_repository = InMemoryReconexionRepository()


def get_reconexion_service() -> ReconexionService:
    return ReconexionService(repository=_repository)


@router.post("/notificar", response_model=PagoProcesadoResponse)
def notificar_pago(
    request: PagoNotificadoRequest,
    service: ReconexionService = Depends(get_reconexion_service),
) -> PagoProcesadoResponse:
    try:
        return service.procesar_pago(request)
    except SuministroNoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc))