"""Script para ejecutar el Eval Set completo contra el Agente CyR."""
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.WARNING)

from app.services.ai_client import get_ai_client
from app.services.eval_set import EVAL_SET
from app.services.rag_service import answer_question
from app.services.retriever import SimpleRetriever

retriever = SimpleRetriever("app/knowledge_base")
client = get_ai_client()

resultados = []

for caso in EVAL_SET:
    print(f"\n{'=' * 60}")
    print(f"CASO: {caso['id']}")
    print(f"Pregunta: {caso['question']}")

    resultado = answer_question(caso["question"], retriever, client)
    respuesta_lower = resultado.respuesta.lower()

    facts_ok = any(fact.lower() in respuesta_lower for fact in caso["required_facts"])
    forbidden_ok = not any(claim.lower() in respuesta_lower for claim in caso["forbidden_claims"])
    sources_ok = (
        not caso["expected_sources"]
        or any(src in resultado.fuentes_utilizadas for src in caso["expected_sources"])
    )

    paso = facts_ok and forbidden_ok and sources_ok

    print(f"Respuesta: {resultado.respuesta[:150]}...")
    print(f"Fuentes: {resultado.fuentes_utilizadas}")
    print(f"required_facts OK: {facts_ok}")
    print(f"forbidden_claims OK (no invento): {forbidden_ok}")
    print(f"expected_sources OK: {sources_ok}")
    print(f">>> RESULTADO: {'PASS' if paso else 'FAIL'}")

    resultados.append({"id": caso["id"], "paso": paso})

print(f"\n{'=' * 60}")
total = len(resultados)
exitosos = sum(1 for r in resultados if r["paso"])
print(f"RESUMEN: {exitosos}/{total} casos pasaron")
for r in resultados:
    estado = "✓" if r["paso"] else "✗"
    print(f"  {estado} {r['id']}")