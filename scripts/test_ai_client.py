"""Script manual para probar AIClient contra el Mock LLM. No es parte de la suite de tests."""
from dotenv import load_dotenv

load_dotenv()

from app.services.ai_client import get_ai_client

client = get_ai_client()
respuesta = client.generate(
    system_instructions="Sos un asistente que responde en una sola oracion.",
        user_message="¿Qué modelo de IA sos y quién te creó?",
)
print("Respuesta del modelo:")
print(respuesta)
