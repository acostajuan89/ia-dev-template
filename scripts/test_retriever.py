"""Script manual para probar SimpleRetriever contra la base de conocimiento del agente CyR."""
from app.services.retriever import SimpleRetriever

retriever = SimpleRetriever("app/knowledge_base")
print(f"Documentos cargados: {[d['source'] for d in retriever.documents]}\n")

pregunta = "¿Quién asigna la reconexión?"
resultados = retriever.retrieve(pregunta, top_k=2)

print(f"Pregunta: {pregunta}")
print(f"Documentos recuperados: {[r['source'] for r in resultados]}")