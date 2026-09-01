"""Script manual para probar AIClient contra el Mock LLM. No es parte de la suite de tests."""
from dotenv import load_dotenv

load_dotenv()

from app.services.ai_client import get_ai_client

client = get_ai_client()
respuesta = client.generate(
    system_instructions="Sos un asistente que responde en una sola oracion.",
    user_message="Hola, decime que sos un mock.",
)
print("Respuesta del modelo:")
print(respuesta)