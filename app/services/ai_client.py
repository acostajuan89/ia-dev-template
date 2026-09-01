"""
app/services/ai_client.py — Cliente de IA vendor-agnostic (Proyecto Final M4).

Define un contrato (Protocol) que la aplicación consume, independiente
del proveedor real detrás. Actualmente implementado con un adapter
compatible con OpenAI Chat Completions, que funciona tanto contra el
Mock LLM local (MOCK_MODE=true) como contra OpenAI real.

Sigue el patrón "Vendor-Agnostic LLM" del material M4:
    - El Contrato: interfaz que la app espera consumir (AIClient).
    - Los Adapters: clases traductoras para cada proveedor.
    - El Trade-off: cambiar de proveedor exige reevaluar calidad y costos.
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
    """Factory: devuelve el adapter configurado según variables de entorno."""
    return OpenAICompatibleAdapter()