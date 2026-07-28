# PRD_v1: Sistema de Registro de Cortes y Gestión de Reconexiones

## 1. Problema y objetivo

**Problema:** Actualmente no existe un mecanismo digital para que las cuadrillas de campo registren en el momento si un corte de suministro de agua fue efectivizado, ni un proceso claro para gestionar la reconexión del servicio una vez que el cliente regulariza su deuda.

**Objetivo:** Implementar un sistema que permita a las cuadrillas registrar el resultado de cada intento de corte, y que gestione el flujo de reconexión posterior al pago.

**Para quién:** Cuadrillas de corte en campo, área de facturación/cobranzas, y clientes afectados.

## 2. Alcance

### Incluido en esta versión
- Registro de corte efectivo por parte de la cuadrilla.
- Registro de motivo cuando el corte no pudo efectivizarse. [PROPUESTA IA]
- Gestión del proceso de reconexión luego del pago de la deuda.
- Consulta del estado de un cliente (cortado / reconectado / pendiente). [PROPUESTA IA]

### Fuera de alcance
- Facturación y cálculo de deuda (se asume que proviene de otro sistema). [PROPUESTA IA]
- Notificaciones automáticas al cliente. [PROPUESTA IA]
- Exportación de reportes históricos. [PROPUESTA IA]

## 3. Usuarios y sistemas involucrados
- **Cuadrilla de corte**: usuario de campo que ejecuta el corte físico y registra el resultado.
- **Sistema de facturación**: origen de la deuda y del pago que dispara la reconexión. [PROPUESTA IA — no confirmado cuál es este sistema]
- **Supervisor/coordinador de cuadrillas**: rol que asigna y supervisa el trabajo diario. [PROPUESTA IA]
- **Cliente**: usuario final afectado por el corte/reconexión.

## 4. Entidades y reglas de negocio

- **Cliente/Suministro**: identificado por un código de cuenta o medidor.
- **Orden de Corte**: instrucción para que una cuadrilla corte un suministro específico.
- **Registro de Corte**: resultado de la ejecución (efectivo / no efectivo + motivo).
- **Orden de Reconexión**: instrucción generada tras el pago de la deuda.

**Regla propuesta:** Un corte solo puede reconectarse si existe un pago confirmado de la deuda que lo originó. [PROPUESTA IA]

**Regla propuesta:** No se puede registrar una reconexión sin un registro de corte previo asociado. [PROPUESTA IA]

## 5. Historias de usuario y criterios de aceptación

**Historia 1:** Como integrante de una cuadrilla, quiero registrar si logré efectivizar un corte, para que el sistema actualice el estado del suministro.

*Criterio de aceptación:* Dado un suministro con orden de corte pendiente, cuando la cuadrilla registra "corte efectivo", entonces el estado del suministro cambia a "cortado" y queda timestamp de la operación.

**Historia 2:** Como integrante de una cuadrilla, quiero registrar por qué no pude efectivizar un corte, para que quede evidencia del intento.

*Criterio de aceptación:* Dado un suministro con orden de corte pendiente, cuando la cuadrilla registra "no efectivizado" con un motivo, entonces el sistema guarda el motivo y reprograma el intento. [PROPUESTA IA — mecanismo de reprogramación no confirmado]

**Historia 3:** Como sistema, quiero detectar automáticamente cuando un cliente cortado paga su deuda, para generar una orden de reconexión. [PROPUESTA IA — se asume integración automática con facturación]

*Criterio de aceptación:* Dado un suministro en estado "cortado", cuando se confirma el pago total de la deuda, entonces se genera una orden de reconexión en menos de 5 minutos. [PROPUESTA IA — plazo inventado, no confirmado]

## 6. Requisitos no funcionales
- **Disponibilidad offline**: las cuadrillas deben poder registrar cortes sin conexión a internet y sincronizar después. [PROPUESTA IA — no confirmado]
- **Seguridad**: solo usuarios autenticados pueden registrar cortes/reconexiones.
- **Auditoría**: todo registro debe quedar trazado con usuario y timestamp.

## 7. Restricciones
- Debe integrarse con el sistema de facturación existente. [PROPUESTA IA]
- Debe funcionar en dispositivos móviles de gama media. [PROPUESTA IA — dispositivo no confirmado]

## 8. Dependencias y riesgos
- Depende de la disponibilidad de datos de pago en tiempo real desde facturación.
- Riesgo: si no hay conectividad en campo, puede haber demoras en la actualización de estados.

## 9. Preguntas abiertas
- ¿Qué dispositivo usan las cuadrillas (app móvil nativa, web responsive, tablet)?
- ¿Tienen conectividad a internet en el momento del corte?
- ¿De dónde sale la lista diaria de cortes a realizar?
- ¿Cuáles son los motivos válidos de "no corte"?
- ¿La reconexión se dispara automáticamente al detectar el pago, o alguien la solicita manualmente?
- ¿Existe un plazo máximo (SLA) para reconectar tras el pago?
- ¿Qué roles exactos pueden operar cada parte del sistema?

## 10. Evidencia de aceptación
- Tests automatizados sobre las reglas de estado (corte → reconexión).
- Revisión manual del flujo con el área operativa de cuadrillas.
- Demostración en ambiente de prueba con datos sintéticos.