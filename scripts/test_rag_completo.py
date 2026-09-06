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

print("\n\n=== Pregunta trampa (no deberia estar en la documentacion) ===")
pregunta_trampa = "¿Cuál es la política de contracargos internacionales?"
print(f"Pregunta: {pregunta_trampa}\n")

resultado_trampa = answer_question(pregunta_trampa, retriever, client)
print(f"Respuesta: {resultado_trampa.respuesta}")
print(f"Fuentes utilizadas: {resultado_trampa.fuentes_utilizadas}")
print(f"Estado evidencia: {resultado_trampa.estado_evidencia}")