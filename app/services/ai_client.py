"""
app/services/ai_client.py — Cliente de IA vendor-agnostic.

Define un contrato (Protocol) que la aplicacion consume, independiente
del proveedor real detras. Implementado con un adapter compatible con
OpenAI Chat Completions, que funciona tanto contra el Mock LLM local
(MOCK_MODE=true) como contra OpenAI real.
"""
from __future__ import annotations

import os
from typing import Protocol

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

class AIIntegrationError(Exception):
    """Error de conexión, configuración o infraestructura con el proveedor de IA."""
    pass


class AIConfigurationError(AIIntegrationError):
    """Falta configuración esencial (API key, modelo, etc.). No reintentar."""
    pass


class AIClient(Protocol):
    """Contrato que la aplicación espera de cualquier proveedor de IA."""

    def generate(self, system_instructions: str, user_message: str) -> str:
        """Devuelve el texto crudo generado por el modelo."""
        ...


class OpenAICompatibleAdapter:
    """
    Adapter que habla el protocolo de OpenAI Chat Completions.

    Funciona indistintamente contra:
      - El Mock LLM local (OPENAI_BASE_URL=http://localhost:8001/v1)
      - OpenAI real (OPENAI_BASE_URL por defecto de la SDK)
    """

    def __init__(self) -> None:
        base_url = os.environ.get("OPENAI_BASE_URL")
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise AIConfigurationError(
                "Falta OPENAI_API_KEY en las variables de entorno"
            )

        self._model = os.environ.get("AI_MODEL", "gpt-4o-mini")
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, system_instructions: str, user_message: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.0,
                 # Baranda BUDGET: limite de tokens de salida por respuesta.
                 # Misma logica que en AnthropicAdapter — arquitectura de un
                 # solo ciclo retrieve->generate, no un loop iterativo.
                 max_tokens=1024,
            )
        except AuthenticationError as exc:
            raise AIConfigurationError(
                "API key invalida o no autorizada"
            ) from exc
        except (APIConnectionError, APITimeoutError, RateLimitError) as exc:
            raise AIIntegrationError(
                "No fue posible conectar con el proveedor de IA"
            ) from exc

        return response.choices[0].message.content or ""


def get_ai_client() -> AIClient:
    """Factory: devuelve el adapter configurado segun variables de entorno."""
    provider = os.environ.get("AI_PROVIDER", "openai").lower()

    if provider == "anthropic":
        from app.services.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter()

    return OpenAICompatibleAdapter()