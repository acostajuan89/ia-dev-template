"""Script manual para probar consultar_agente_cyr contra el Mock LLM."""
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

from app.services.agente_cyr_service import (
    InvalidModelOutputError,
    consultar_agente_cyr,
)
from app.services.ai_client import get_ai_client

client = get_ai_client()

print("=== Pregunta al agente (el Mock NO devuelve JSON, debe fallar) ===")
from app.services.agente_cyr_service import SYSTEM_INSTRUCTIONS
from app.services.ai_client import get_ai_client

client_debug = get_ai_client()
raw_debug = client_debug.generate(
    system_instructions=SYSTEM_INSTRUCTIONS,
    user_message="¿Quién asigna la reconexión?",
)
print("=== RESPUESTA CRUDA DE CLAUDE ===")
print(repr(raw_debug))
print("==================================\n")

try:
    resultado = consultar_agente_cyr(
        "¿Quién asigna la reconexión?", client
    )
    print(resultado)
except InvalidModelOutputError as exc:
    print(f"Error esperado capturado correctamente: {exc}")
