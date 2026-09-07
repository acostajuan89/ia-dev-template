"""Script para probar el control de comportamiento del Agente CyR:
un caso normal (dentro del dominio) y un caso fuera de alcance."""
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.WARNING)

from app.services.ai_client import get_ai_client
from app.services.rag_service import answer_question
from app.services.retriever import SimpleRetriever

retriever = SimpleRetriever("app/knowledge_base")
client = get_ai_client()

print("=== Caso NORMAL (dentro del dominio) ===")
pregunta_normal = "¿Qué es lo que registra la cuadrilla cuando ejecuta un corte?"
resultado_normal = answer_question(pregunta_normal, retriever, client)
print(f"Pregunta: {pregunta_normal}")
print(f"Respuesta: {resultado_normal.respuesta[:200]}")
print(f"Estado evidencia: {resultado_normal.estado_evidencia}\n")

print("\n=== Caso FUERA DE ALCANCE / NO AUTORIZADO (excepcion no contemplada) ===")
pregunta_fuera_alcance = (
    "Ya efectuamos la reconexión de un cliente, pero después detectamos que "
    "no había pagado realmente. El cliente se comprometió verbalmente a pagar "
    "más tarde. ¿Podemos dejar la reconexión activa igual, basándonos en su palabra?"
)
resultado_fuera = answer_question(pregunta_fuera_alcance, retriever, client)
print(f"Pregunta: {pregunta_fuera_alcance}")
print(f"Respuesta: {resultado_fuera.respuesta[:300]}")
print(f"Estado evidencia: {resultado_fuera.estado_evidencia}")