# AI_USAGE.md — Lab 3: Implementación y Testing con IA

## Entrada 1 — Contrato de entrada/salida (Pydantic)

**Objetivo:** Definir el contrato de datos para el evento de pago
notificado por el sistema COBOL de facturación.

**Herramienta/modelo:** Claude (Anthropic).

**Contexto proporcionado:** El flujo real fue aportado por el autor
durante la conversación: COBOL envía nro_comprobante +
identificador_cuenta; según el estado del suministro asociado
(cortado/asignado), el sistema debe generar una reconexión o anular
la orden de corte.

**Cambio realizado:** Se definieron PagoNotificadoRequest (entrada) y
las respuestas ReconexionResponse/AnulacionCorteResponse (salida),
validando solo la FORMA de los datos (Pydantic), no las reglas de
negocio.

**Decisión humana clave:** Se acotó explícitamente el alcance del Lab 3
a los 2 casos con reglas 100% confirmadas (cortado->reconexión,
asignado->anulación), dejando el tercer caso real del dominio (bandeja
de verificación cuando la cuenta no tiene orden activa) fuera de
alcance, documentado como decisión consciente y no como omisión.

## Entrada 2 — TDD: contrato → test rojo → implementación → verde

**Objetivo:** Implementar ReconexionService siguiendo el ciclo
Rojo → Verde → Refactor.

**Herramienta/modelo:** Claude (Anthropic).

**Salida obtenida:** Se escribió el test ANTES de la implementación
(tests/test_reconexion_service.py), confirmando la Pantalla Roja real
(ModuleNotFoundError: No module named 'app.services'). Luego se
implementó el ReconexionService mínimo necesario para pasar a verde.

**Problema detectado (proceso, no de la IA):** Al pegar código Python
directamente en la terminal PowerShell en vez del editor, se generaron
errores de parseo de PowerShell — no relacionado con la lógica, sino
con el entorno de trabajo. Se corrigió pegando el contenido en el
editor correctamente.

**Cambio realizado:** Separación en 3 capas desde el diseño inicial
(Router -> Service -> Repository), con Dependency Injection del
repositorio en el Service, siguiendo el patrón Service Layer +
Repository descrito en el material M3.U1.

## Entrada 3 — Casos borde (U2.2)

**Objetivo:** Cubrir 3 riesgos reales del dominio, no genéricos.

**Casos elegidos:**
1. identificador_cuenta que no corresponde a ningún suministro
   (SuministroNoEncontradoError -> HTTP 404 en el router).
2. Suministro en un estado no soportado (ni "cortado" ni "asignado",
   ej. "reconectado") -> ValueError explícito, en vez de fallar
   silenciosamente o aplicar un comportamiento por defecto incorrecto.
3. nro_comprobante vacío -> rechazado por el contrato Pydantic antes
   de llegar al Service (prueba la capa de contrato, no la de dominio).

**Decisión humana:** Estos 3 casos surgen directamente de las reglas
de negocio confirmadas en el PRD/ADR-0001, no fueron generados
genéricamente por la IA sin contexto.

## Entrada 4 — Test con falsa confianza detectado y corregido (U2.3)

**Objetivo:** Producir a propósito un test con el anti-patrón de
"mock excesivo" (Página 26 del material M3), diagnosticarlo
empíricamente, y corregirlo.

**Test alucinado (original):**
```python
def test_procesar_pago_genera_reconexion_MOCK_EXCESIVO():
    with patch.object(ReconexionService, "procesar_pago",
                       return_value={"accion": "reconexion"}):
        ...
        assert result["accion"] == "reconexion"  # siempre pasa
```

**Diagnóstico:** El test parcheaba (`patch.object`) el propio método
bajo prueba (`procesar_pago`), forzando su valor de retorno. El assert
comparaba el mock contra sí mismo — la lógica real del servicio nunca
se ejecutaba.

**Evidencia empírica de que era falsa confianza:** Se rompió
deliberadamente la implementación real (`ReconexionService.procesar_pago`,
condición `suministro["estado"] == "cortado"` reemplazada por un valor
inexistente) y se corrió la suite completa:
- El test real (`test_genera_reconexion_cuando_suministro_esta_cortado`)
  **falló correctamente**, detectando el bug.
- El test con mock excesivo **siguió en verde**, sin detectar nada.

**Corrección aplicada:** Se eliminó el `patch.object` sobre el método
bajo prueba. El nuevo test (`test_procesar_pago_genera_reconexion_SIN_MOCK_EXCESIVO`)
usa el `FakeReconexionRepository` únicamente para aislar la
persistencia, dejando que la lógica de decisión real se ejecute sin
mockear. Se confirmó que, con el bug reintroducido, este nuevo test
también falla — validando que ahora sí protege el comportamiento.

## Resumen de evidencia (checklist U1/U2)

| Indicador | Evidencia |
|---|---|
| U1.1 | Router/Service/Repository separados desde el commit inicial (Git log) |
| U1.2 | Service Layer + Repository + Dependency Injection, justificados |
| U1.3 | pytest verde en cada commit (rojo inicial documentado, luego verde sostenido) |
| U2.1 | 2 tests de camino feliz + endpoint verificado manualmente en /docs |
| U2.2 | 3 casos borde reales del dominio |
| U2.3 | Test con mock excesivo detectado, diagnosticado empíricamente, corregido |