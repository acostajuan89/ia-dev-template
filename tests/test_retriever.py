"""Tests para SimpleRetriever."""
from app.services.retriever import SimpleRetriever, tokenize


def test_tokenize_ignora_palabras_cortas() -> None:
    tokens = tokenize("El de la asignacion")
    assert "el" not in tokens
    assert "de" not in tokens
    assert "asignacion" in tokens


def test_tokenize_normaliza_minusculas() -> None:
    tokens = tokenize("RECONEXION")
    assert "reconexion" in tokens


def test_retriever_carga_documentos_md() -> None:
    retriever = SimpleRetriever("app/knowledge_base")
    assert len(retriever.documents) >= 1
    assert all(doc["source"].endswith(".md") for doc in retriever.documents)


def test_retriever_encuentra_documento_relevante() -> None:
    retriever = SimpleRetriever("app/knowledge_base")
    resultados = retriever.retrieve("reconexion administrador cuadrilla", top_k=3)
    assert len(resultados) > 0


def test_retriever_no_encuentra_nada_para_query_irrelevante() -> None:
    retriever = SimpleRetriever("app/knowledge_base")
    resultados = retriever.retrieve("zzz xyzabc noexiste", top_k=3)
    assert len(resultados) == 0
