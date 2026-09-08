"""
app/services/anthropic_adapter.py — Adapter de Claude (Anthropic) para AIClient.

Implementacion alternativa a OpenAICompatibleAdapter, usando el SDK
nativo de Anthropic en vez del protocolo de OpenAI Chat Completions.
"""
from __future__ import annotations

import os

from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from app.services.ai_client import AIConfigurationError, AIIntegrationError


class AnthropicAdapter:
    """Adapter que habla directamente con la API de Anthropic (Claude)."""

    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not api_key:
            raise AIConfigurationError(
                "Falta ANTHROPIC_API_KEY en las variables de entorno"
            )

        self._model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        self._client = Anthropic(api_key=api_key)

    def generate(self, system_instructions: str, user_message: str) -> str:
        try:
            response = self._client.messages.create(
                model=self._model,
                # Baranda BUDGET: limite de tokens de salida por respuesta.
                # Nuestra arquitectura usa un unico ciclo retrieve->generate
                # (no un loop iterativo con MAX_STEPS como en otros disenos
                # de agente); el limite de presupuesto aqui se aplica al
                # tamano maximo de cada respuesta generada.
                max_tokens=1024,
                system=system_instructions,
                messages=[{"role": "user", "content": user_message}],
            )
        except AuthenticationError as exc:
            raise AIConfigurationError(
                "API key invalida o no autorizada"
            ) from exc
        except (APIConnectionError, APITimeoutError, RateLimitError, APIStatusError) as exc:
            raise AIIntegrationError(
                "No fue posible conectar con el proveedor de IA"
            ) from exc

        return response.content[0].text if response.content else ""
