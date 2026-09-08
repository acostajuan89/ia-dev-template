"""Tests para rag_service: orquestacion RAG con AIClient fake."""
from app.services.rag_service import answer_question, build_context
from app.services.retriever import SimpleRetriever


class FakeAIClient:
    """AIClient falso que devuelve una respuesta JSON fija, sin llamar a ninguna API."""

    def __init__(self, respuesta_json: str) -> None:
        self.respuesta_json = respuesta_json
        self.ultima_instruccion = None
        self.ultimo_mensaje = None

    def generate(self, system_instructions: str, user_message: str) -> str:
        self.ultima_instruccion = system_instructions
        self.ultimo_mensaje = user_message
        return self.respuesta_json


def test_build_context_con_documentos() -> None:
    docs = [{"source": "PRD.md", "content": "contenido de prueba"}]
    context = build_context(docs)
    assert "[SOURCE: PRD.md]" in context
    assert "contenido de prueba" in context


def test_build_context_sin_documentos() -> None:
    context = build_context([])
    assert "No se encontraron documentos relevantes" in context


def test_answer_question_flujo_completo() -> None:
    fake_json = (
        '{"respuesta": "El administrador de cuadrilla asigna la reconexion.", '
        '"fuentes_utilizadas": ["PRD.md"], "estado_evidencia": "suficiente"}'
    )
    fake_client = FakeAIClient(fake_json)
    retriever = SimpleRetriever("app/knowledge_base")

    resultado = answer_question("¿Quien asigna la reconexion?", retriever, fake_client)

    assert resultado.estado_evidencia == "suficiente"
    assert resultado.fuentes_utilizadas == ["PRD.md"]
    # Confirma que el contexto recuperado realmente se paso al cliente
    assert "PREGUNTA:" in fake_client.ultimo_mensaje
    assert "DOCUMENTOS RECUPERADOS" in fake_client.ultimo_mensaje
