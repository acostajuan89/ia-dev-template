"""Script manual para probar el flujo RAG completo (retriever + generacion + validacion)."""
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

from app.services.ai_client import get_ai_client
from app.services.rag_service import answer_question
from app.services.retriever import SimpleRetriever

retriever = SimpleRetriever("app/knowledge_base")
client = get_ai_client()

pregunta = "¿Quién asigna la reconexión?"
print(f"=== Pregunta: {pregunta} ===\n")

resultado = answer_question(pregunta, retriever, client)
print(f"Respuesta: {resultado.respuesta}")
print(f"Fuentes utilizadas: {resultado.fuentes_utilizadas}")
print(f"Estado evidencia: {resultado.estado_evidencia}")