# Proyecto Final · Juan Acosta

Agente RAG que responde preguntas sobre el proceso de corte y
reconexión de suministro de agua de ESSAP, basado en el patrón
Retrieval-Augmented Generation con un retriever lexical sobre
`app/knowledge_base/*.md` (PRD y ADR del proyecto).

## Cómo probarlo en 5 minutos

1. Clonar y sincronizar:
```bash
git clone <url-de-tu-fork>
cd ia-dev-template
git checkout proyecto-final-juan-acosta
uv sync
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
```
Editá `.env`: agregá tu `ANTHROPIC_API_KEY` y seteá `AI_PROVIDER=anthropic`
(o dejá `MOCK_MODE=true` para usar el Mock LLM local sin API key real).

3. Correr el agente con una consulta real:
```bash
uv run python -m scripts.test_rag_completo
```

4. Correr el Eval Set (6 casos, incluye una pregunta trampa):
```bash
uv run python -m scripts.run_eval_set
```

5. Ver el log auditable generado:
```bash
cat logs/agent_run.jsonl
```

## Arquitectura del agente

**Componentes:**
- `app/services/retriever.py` — recuperación lexical (sin embeddings)
- `app/services/rag_service.py` — orquestación (retrieve → context → generate → validate)
- `app/services/ai_client.py` + `anthropic_adapter.py` — integración vendor-agnostic
- `app/schemas/agente_cyr.py` — contrato de salida estructurada
- `app/services/agent_logger.py` — log auditable JSONL
- `app/knowledge_base/` — base de conocimiento (PRD.md, ADR-0001)

## Barandas aplicadas

| Baranda | Dónde vive | Qué hace |
|---|---|---|
| **SCOPE** | `app/services/rag_service.py` (`SYSTEM_INSTRUCTIONS_RAG`) | Restringe el dominio de respuesta al proceso de corte/reconexión; prohíbe usar conocimiento fuera de los documentos recuperados |
| **BUDGET** | `app/services/ai_client.py` y `anthropic_adapter.py` (`max_tokens=1024`) | Limita el tamaño máximo de cada respuesta generada |

## Criterios de aceptación

- [x] El agente responde con precisión cuando hay evidencia en la documentación (Eval Set: 6/6 casos pasan)
- [x] El agente se abstiene explícitamente ante preguntas sin evidencia suficiente
- [x] El agente rechaza correctamente excepciones de negocio no autorizadas
- [x] Cada consulta genera un log auditable en `logs/agent_run.jsonl`
- [x] Integración funcional con Claude real (Anthropic API)

## Limitaciones conocidas

- **Retriever lexical, no semántico**: la búsqueda se basa en coincidencia
  de palabras clave (tokenización simple), no en embeddings. No reconoce
  sinónimos ni reformulaciones de una misma pregunta.
- **Sin autorización por documento**: cualquier consulta puede recuperar
  cualquier documento de la base de conocimiento; no hay control de
  acceso por rol.
- **Base de conocimiento acotada**: solo cubre el PRD y el ADR del
  proceso de corte/reconexión; no incluye otras operaciones del dominio
  de medidores (mantenimiento, calibración).
- **Sin loop iterativo**: la arquitectura usa un único ciclo
  retrieve → generate → validate, no un patrón ReAct con múltiples
  pasos de decisión.

## Documentación relacionada

- [docs/prd/PRD.md](docs/prd/PRD.md) — requisitos del sistema de corte/reconexión
- [docs/architecture/decisions/0001-deteccion-pagos.md](docs/architecture/decisions/0001-deteccion-pagos.md) — ADR de detección de pagos
- [AI_USAGE.md](AI_USAGE.md) — registro del proceso de integración de IA
- [postmortem_final.md](postmortem_final.md) — reflexión final del proyecto
- [README_DIPLOMADO.md](README_DIPLOMADO.md) — documentación general del template del diplomado (setup, Docker, CI, estructura de módulos)