"""
app/services/agent_logger.py — Registro auditable de ejecuciones del
Agente CyR. Cada consulta queda registrada como una linea JSON en
logs/agent_run.jsonl (formato JSONL: un objeto JSON por linea).
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

LOG_PATH = Path("logs/agent_run.jsonl")


def log_step(
    question: str,
    sources_found: list[str],
    estado_evidencia: str,
    respuesta_preview: str,
) -> None:
    """Registra un paso de ejecucion del agente en el log auditable."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "question": question,
        "sources_found": sources_found,
        "estado_evidencia": estado_evidencia,
        "respuesta_preview": respuesta_preview[:150],
    }

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
