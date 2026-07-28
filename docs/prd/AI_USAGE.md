# AI_USAGE.md — Registro de uso de IA (Lab 2)

## Entrada 1 — Generación y auditoría del PRD

**Objetivo:** Generar un primer borrador de PRD para el sistema de
registro de cortes y gestión de reconexiones de suministro de agua.

**Herramienta/modelo:** Claude (Anthropic), usado como asistente de
generación y auditoría conversacional.

**Contexto proporcionado:** Hechos aprobados sobre el proceso de corte
(existencia de cuadrillas de campo, origen del corte por deuda impaga,
necesidad de registrar reconexión post-pago), junto con restricciones
explícitas de no inventar dispositivos, conectividad, motivos de no-corte,
ni plazos (SLA).

**Salida obtenida (PRD_v1):** Un borrador con estructura completa de 10
secciones, pero que incluía varios supuestos no confirmados: un plazo de
"5 minutos" para generar la reconexión tras el pago, un rol de
"supervisor/coordinador" no confirmado, un dispositivo de "gama media"
no confirmado, y ninguna mención del proceso de retiro y custodia física
del medidor en depósito (un flujo completo que la IA no pudo anticipar
porque no estaba en el contexto inicial).

**Problemas detectados:**
- La IA inventó un SLA de "5 minutos" sin ninguna base.
- La IA asumió reconexión automática disparada por el sistema, cuando en
  realidad la asigna siempre un administrador de cuadrilla.
- La IA no contempló el proceso de retiro/custodia de medidores en
  depósito, porque no fue mencionado en el contexto inicial — esto no es
  un error de la IA sino una omisión del contexto que se corrigió
  durante la auditoría.

**Cambios realizados:**
- Se eliminó el SLA inventado y se reemplazó por el requisito real
  confirmado ("reconexión el mismo día del pago").
- Se agregaron las entidades "Medidor", "Ingreso a Depósito" y el rol
  "Funcionario de depósito", inexistentes en el borrador original.
- Se reescribieron las historias de usuario 3, 4 y 5 para reflejar que
  el administrador de cuadrilla asigna siempre la reconexión (no hay
  automatización total).
- Se confirmaron 2 motivos reales de no-corte (pago con comprobante en
  el momento, medidor trancado) reemplazando el marcador genérico de
  "pregunta abierta" original.

**Evidencia / preguntas abiertas remanentes:**
- ¿Existen otros motivos válidos de no-corte además de los dos
  confirmados?
- ¿La cuadrilla puede aceptar un comprobante de pago in situ sin validar
  contra el sistema de facturación?
- ¿Qué patrón de integración usará la API que monitorea pagos
  (polling vs. evento)? — Pendiente de resolver en el ADR.