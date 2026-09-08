"""Tests para agente_cyr_service: parseo y validacion de respuestas del modelo."""
import pytest

from app.services.agente_cyr_service import (
    InvalidModelOutputError,
    parse_respuesta_cyr,
)


def test_parsea_json_valido() -> None:
    raw = (
        '{"respuesta": "El administrador de cuadrilla asigna la reconexion.", '
        '"fuentes_utilizadas": ["PRD.md"], "estado_evidencia": "suficiente"}'
    )
    resultado = parse_respuesta_cyr(raw)
    assert resultado.estado_evidencia == "suficiente"
    assert resultado.fuentes_utilizadas == ["PRD.md"]


def test_parsea_json_envuelto_en_markdown() -> None:
    """Reproduce el caso real detectado con Claude: JSON envuelto en ```json ... ```."""
    raw = (
        '```json\n'
        '{"respuesta": "Respuesta de prueba", '
        '"fuentes_utilizadas": [], "estado_evidencia": "insuficiente"}\n'
        '```'
    )
    resultado = parse_respuesta_cyr(raw)
    assert resultado.estado_evidencia == "insuficiente"


def test_rechaza_json_invalido() -> None:
    with pytest.raises(InvalidModelOutputError):
        parse_respuesta_cyr("esto no es JSON en absoluto")


def test_rechaza_json_que_no_cumple_contrato() -> None:
    raw = '{"respuesta": "Falta el campo estado_evidencia"}'
    with pytest.raises(InvalidModelOutputError):
        parse_respuesta_cyr(raw)