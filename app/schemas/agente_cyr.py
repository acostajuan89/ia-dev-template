"""
app/schemas/agente_cyr.py — Contrato de salida estructurada para el
Agente CyR (Corte y Reconexion).

Obliga al modelo a declarar sus fuentes y si tuvo evidencia suficiente,
en vez de responder con texto libre sin trazabilidad.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RespuestaAgenteCyR(BaseModel):
    """Contrato de salida del agente CyR. Rechaza campos no definidos."""

    model_config = ConfigDict(extra="forbid")

    respuesta: str = Field(min_length=1)
    fuentes_utilizadas: list[str]
    estado_evidencia: Literal["suficiente", "insuficiente"]