"""
Script manual para demostrar TG3: manejo de errores de configuracion
y de conexion, sin que la aplicacion colapse (crash opaco).
"""
import logging
import os

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.services.ai_client import (
    AIConfigurationError,
    AIIntegrationError,
    OpenAICompatibleAdapter,
)

print("=== Caso 1: Error de CONFIGURACION (falta API key) ===")
os.environ.pop("OPENAI_API_KEY", None)  # simulamos que no esta configurada
try:
    client = OpenAICompatibleAdapter()
    print("ERROR: no deberia haber llegado aca")
except AIConfigurationError as exc:
    logger.error("error_configuracion_capturado", extra={"error_type": "AIConfigurationError"})
    print(f"Capturado correctamente (sin exponer valores): {exc}")

print("\n=== Caso 2: Error de CONEXION (servidor inalcanzable) ===")
os.environ["OPENAI_API_KEY"] = "sk-mock-key-123"
os.environ["OPENAI_BASE_URL"] = "http://localhost:9999/v1"  # puerto que no existe
try:
    client = OpenAICompatibleAdapter()
    respuesta = client.generate(
        system_instructions="Test",
        user_message="Test",
    )
    print("ERROR: no deberia haber llegado aca")
except AIIntegrationError as exc:
    logger.error("error_conexion_capturado", extra={"error_type": "AIIntegrationError"})
    print(f"Capturado correctamente (sin exponer valores): {exc}")

print("\n=== Ambos casos manejados sin que la aplicacion colapse ===")
