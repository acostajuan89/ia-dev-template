"""
app/services/agente_cyr_service.py — Orquestacion del Agente CyR.

Conecta el AIClient (integracion) con el contrato RespuestaAgenteCyR
(estructura), forzando al modelo a responder en JSON validable.
"""
from __future__ import annotations

import json
import logging

from pydantic import ValidationError

from app.schemas.agente_cyr import RespuestaAgenteCyR
from app.services.ai_client import AIClient

logger = logging.getLogger(__name__)


class InvalidModelOutputError(Exception):
    """La respuesta del modelo no cumple el contrato esperado."""
    pass


SYSTEM_INSTRUCTIONS = (
    "Sos el Agente CyR (Corte y Reconexion) de ESSAP. "
    "Respondé ÚNICAMENTE con un objeto JSON válido, sin Markdown ni texto adicional. "
    "El JSON debe tener exactamente estos campos: "
    "respuesta (string), fuentes_utilizadas (lista de strings), "
    "estado_evidencia ('suficiente' o 'insuficiente')."
)


def parse_respuesta_cyr(raw_text: str) -> RespuestaAgenteCyR:
    """Convierte el texto crudo del modelo en un objeto validado."""
    try:
        data = json.loads(raw_text)
        return RespuestaAgenteCyR.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise InvalidModelOutputError(
            f"La respuesta del modelo no cumple el contrato: {exc}"
        ) from exc


def consultar_agente_cyr(pregunta: str, client: AIClient) -> RespuestaAgenteCyR:
    """Función principal: pregunta -> respuesta estructurada y validada."""
    raw = client.generate(
        system_instructions=SYSTEM_INSTRUCTIONS,
        user_message=pregunta,
    )

    try:
        resultado = parse_respuesta_cyr(raw)
        logger.info("agente_cyr_respuesta_ok")
        return resultado
    except InvalidModelOutputError:
        logger.warning("agente_cyr_output_invalido", extra={"raw_preview": raw[:100]})
        raise