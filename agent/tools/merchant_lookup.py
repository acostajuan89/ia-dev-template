"""
agent/tools/merchant_lookup.py — Herramienta de consulta de comerciantes LegacyPay.

FIX BUG 3: el bloque que silenciaba todos los errores ("hacer que el lookup
no crashee si algo falla") fue reemplazado por manejo de excepciones
especificas. Ahora se distingue entre archivo inexistente, JSON corrupto,
problemas de permisos/IO, y estructura de datos inesperada. Cada caso se
loguea (para que quede rastro en produccion) y el llamador recibe un
diccionario vacio para que lookup_merchant() devuelva un mensaje de
ERROR claro en vez de fallar en silencio.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DATA_FILE = Path(__file__).parent.parent.parent / "data" / "merchants_sample.json"
_CACHE: dict[str, Any] | None = None


def _load_merchants() -> dict[str, Any]:
    """Carga y cachea los datos de comerciantes desde disco."""
    global _CACHE  # noqa: PLW0603
    if _CACHE is None:
        _CACHE = {}
        try:
            with _DATA_FILE.open(encoding="utf-8") as f:
                data = json.load(f)
            _CACHE = {m["merchant_id"]: m for m in data.get("merchants", [])}
        except FileNotFoundError:
            logger.error("Archivo de comerciantes no encontrado: %s", _DATA_FILE)
        except PermissionError:
            logger.error("Permiso denegado al leer: %s", _DATA_FILE)
        except json.JSONDecodeError as e:
            logger.error("JSON invalido en %s: %s", _DATA_FILE, e)
        except (OSError, KeyError, TypeError) as e:
            logger.error("Error inesperado cargando comerciantes desde %s: %s", _DATA_FILE, e)
    return _CACHE


def lookup_merchant(merchant_id: str) -> str:
    """
    Busca un comerciante por su ID y retorna sus datos relevantes.

    Args:
        merchant_id: ID del comerciante en formato MCHT-NNNNN.

    Returns:
        JSON string con los datos del comerciante, o mensaje de error si no existe.
    """
    if not isinstance(merchant_id, str):
        return f"ERROR: 'merchant_id' debe ser string, recibio {type(merchant_id).__name__}"

    merchant_id = merchant_id.strip().upper()
    if not merchant_id.startswith("MCHT-"):
        return f"ERROR: formato invalido '{merchant_id}'. Use MCHT-NNNNN"

    merchants = _load_merchants()

    if not merchants:
        return "ERROR: base de datos de comerciantes no disponible"

    merchant = merchants.get(merchant_id)
    if merchant is None:
        return f"NOT_FOUND: comerciante '{merchant_id}' no existe en el sistema"

    safe_fields = {
        "merchant_id": merchant.get("merchant_id"),
        "name": merchant.get("name"),
        "category": merchant.get("category"),
        "status": merchant.get("status"),
        "daily_limit_usd": merchant.get("daily_limit_usd"),
        "risk_level": merchant.get("risk_level"),
    }
    return json.dumps(safe_fields, ensure_ascii=False)
