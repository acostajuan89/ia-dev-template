"""
app/services/retriever.py — Retriever lexical simple para el Agente CyR.

Busca coincidencias de palabras clave entre la pregunta del usuario y
los documentos .md de la base de conocimiento. No usa embeddings ni
bases vectoriales.

Limitacion conocida: al ser busqueda lexical (no semantica), no
reconoce sinonimos ni variaciones de una misma idea expresada con
otras palabras.
"""
from __future__ import annotations

import re
from pathlib import Path


def tokenize(text: str) -> set[str]:
    """Separa el texto en palabras utiles (tokens), ignorando muy cortas."""
    return {
        token.lower()
        for token in re.findall(r"\w+", text)
        if len(token) > 2
    }


class SimpleRetriever:
    def __init__(self, docs_path: str) -> None:
        self.documents: list[dict[str, str]] = []
        for path in Path(docs_path).glob("*.md"):
            self.documents.append({
                "source": path.name,
                "content": path.read_text(encoding="utf-8"),
            })

    def retrieve(self, query: str, top_k: int = 3) -> list[dict[str, str]]:
        """Compara palabras de la pregunta contra los documentos, devuelve los mejores."""
        query_tokens = tokenize(query)
        scored = []

        for doc in self.documents:
            doc_tokens = tokenize(doc["content"])
            score = len(query_tokens & doc_tokens)
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]