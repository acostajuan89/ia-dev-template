"""Script manual para probar el contrato RespuestaAgenteCyR. No es parte de pytest."""
from pydantic import ValidationError

from app.schemas.agente_cyr import RespuestaAgenteCyR

print("=== Caso 1: JSON valido ===")
data_valida = {
    "respuesta": "La reconexion se asigna siempre por el administrador de cuadrilla.",
    "fuentes_utilizadas": ["PRD.md"],
    "estado_evidencia": "suficiente",
}
resultado = RespuestaAgenteCyR.model_validate(data_valida)
print(resultado)

print("\n=== Caso 2: JSON con campo inventado (debe fallar) ===")
data_invalida = {
    "respuesta": "Algo",
    "fuentes_utilizadas": ["PRD.md"],
    "estado_evidencia": "suficiente",
    "campo_inventado": "esto no deberia existir",
}
try:
    RespuestaAgenteCyR.model_validate(data_invalida)
    print("ERROR: no debería haber pasado la validacion")
except ValidationError as exc:
    print("Rechazado correctamente:")
    print(exc)

print("\n=== Caso 3: estado_evidencia con valor no permitido (debe fallar) ===")
data_invalida_2 = {
    "respuesta": "Algo",
    "fuentes_utilizadas": ["PRD.md"],
    "estado_evidencia": "tal_vez",  # no es "suficiente" ni "insuficiente"
}
try:
    RespuestaAgenteCyR.model_validate(data_invalida_2)
    print("ERROR: no debería haber pasado la validacion")
except ValidationError as exc:
    print("Rechazado correctamente:")
    print(exc)
