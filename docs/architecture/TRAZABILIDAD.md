# Trazabilidad — Sistema de Corte y Reconexión

## De necesidad a artefacto

| Necesidad / Regla de negocio | PRD (sección) | Modelo/Diagrama | Decisión (ADR) |
|---|---|---|---|
| Registrar corte efectivo/no efectivizado | PRD Historia 1, 2 | ERD: ORDEN_CORTE, REGISTRO_CORTE | — |
| Retiro y custodia de medidor en depósito | PRD Sección 3, 4 | ERD: MEDIDOR, INGRESO_DEPOSITO | — |
| Cuadrilla como equipo de 2-3 personas fijo | PRD Sección 3 | ERD: CUADRILLA, CUADRILLA_USUARIO | — |
| Usuario independiente por persona (seguridad) | PRD Sección 6 | ERD: USUARIO; Secuencia: validación de sesión | — |
| Reconexión asignada siempre por administrador | PRD Sección 4, Historia 4 | ERD: ORDEN_RECONEXION.asignado_por_id | — |
| Flujo distinto según pago mismo día vs. posterior | PRD Sección 4 (regla) | ERD: INGRESO_DEPOSITO opcional | — |
| Reconexión debe completarse el mismo día del pago | PRD Sección 6 (RNF) | — | ADR-0001 (consecuencias/trade-offs) |
| Detección de pagos vía script existente + notificación | PRD Sección 7 (restricción) | — | ADR-0001 (decisión completa) |
| Motivos válidos de no-corte | PRD Historia 2 | Secuencia: flujo alternativo `alt` | — |

## Preguntas abiertas aún sin resolver (heredadas de todo el portafolio)

1. ¿Existen otros motivos válidos de no-corte además de los dos
   confirmados? (PRD Sección 9)
2. ¿La cuadrilla puede aceptar un comprobante de pago in situ sin validar
   contra facturación? (PRD Sección 9, Secuencia)
3. ¿El registro de corte debe diferenciar la persona específica de la
   cuadrilla? (ERD)
4. ¿El estado del medidor se modela como campo simple o historial? (ERD)
5. ¿"ORDEN_RECONEXION" necesita su propio registro de ejecución? (ERD)
6. ¿Validación de geolocalización antes del registro? (Secuencia)
7. Sin mecanismo automatizado de respaldo ante fallo de notificación
   push — riesgo aceptado para v1 (ADR-0001)

## Nota de coherencia

Todas las entidades del ERD (`erd.md`) están justificadas por una
sección específica del PRD. Ninguna entidad fue agregada sin trazar a
una necesidad o decisión explícita. El único artefacto pendiente de
mayor profundidad de trazabilidad es el diagrama de secuencia de
reconexión (no se llegó a crear en este sprint, solo el de corte).