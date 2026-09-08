"""
app/schemas/reconexion.py — Contratos de entrada/salida para el proceso
de reconexión de suministros (Lab 3).

Basado en docs/prd/PRD.md (Historia 4, 5) y ADR-0001.

Origen del evento: el sistema COBOL de facturación notifica el pago
mediante nro_comprobante + identificador_cuenta. El MS resuelve qué
acción corresponde según el estado ACTUAL del suministro asociado:

    1. SUMINISTRO.estado == "cortado"
       -> genera la reconexión (ORDEN_RECONEXION).

    2. SUMINISTRO.estado == "asignado" (corte aún no efectivizado)
       -> anula la orden de corte (nunca llegó a cortarse).

[PREGUNTA ABIERTA / FUERA DE ALCANCE Lab 3]: si identificador_cuenta
no corresponde a ningún suministro con orden activa, el pago se
registra en una bandeja de verificación de solo lectura (tabla
consultada y mostrada en pantalla, sin lógica de negocio asociada).
No se implementa en este laboratorio.

Distinción clave: este contrato valida la FORMA de los datos.
No valida reglas de negocio (qué acción corresponde) — de eso se
encarga el Service (invariante de dominio).
"""
from pydantic import BaseModel, Field


class PagoNotificadoRequest(BaseModel):
    """
    Contrato de entrada: evento de pago que envía el sistema COBOL
    de facturación.
    """
    nro_comprobante: str = Field(min_length=1)
    identificador_cuenta: str = Field(min_length=1)


class ReconexionResponse(BaseModel):
    """Contrato de salida cuando la acción resultante es RECONEXION."""
    reconexion_id: str
    suministro_id: str
    estado: str = Field(min_length=1)


class AnulacionCorteResponse(BaseModel):
    """Contrato de salida cuando la acción resultante es ANULACION."""
    orden_corte_id: str
    suministro_id: str
    estado: str = Field(min_length=1)


class PagoProcesadoResponse(BaseModel):
    """
    Contrato de salida unificado: informa qué acción se tomó
    (reconexion | anulacion) y el detalle correspondiente.
    """
    accion: str = Field(min_length=1)  # "reconexion" | "anulacion"
    detalle: ReconexionResponse | AnulacionCorteResponse
