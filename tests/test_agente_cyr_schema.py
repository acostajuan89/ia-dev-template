"""Tests para el contrato RespuestaAgenteCyR."""
import pytest
from pydantic import ValidationError

from app.schemas.agente_cyr import RespuestaAgenteCyR


def test_acepta_respuesta_valida() -> None:
    resultado = RespuestaAgenteCyR(
        respuesta="La reconexion la asigna el administrador de cuadrilla.",
        fuentes_utilizadas=["PRD.md"],
        estado_evidencia="suficiente",
    )
    assert resultado.estado_evidencia == "suficiente"


def test_rechaza_campo_no_definido() -> None:
    with pytest.raises(ValidationError):
        RespuestaAgenteCyR(
            respuesta="Algo",
            fuentes_utilizadas=["PRD.md"],
            estado_evidencia="suficiente",
            campo_inventado="no deberia existir",
        )


def test_rechaza_estado_evidencia_invalido() -> None:
    with pytest.raises(ValidationError):
        RespuestaAgenteCyR(
            respuesta="Algo",
            fuentes_utilizadas=["PRD.md"],
            estado_evidencia="tal_vez",
        )
