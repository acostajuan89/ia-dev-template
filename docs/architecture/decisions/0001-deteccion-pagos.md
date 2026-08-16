# ADR-0001: Estrategia de detección de pagos para habilitar reconexión

**Fecha:** 2026-08-03
**Estado:** Aceptado
**Responsables:** Juan Acosta (DTDI, ESSAP)

## Contexto y problema

El sistema debe detectar cuándo un cliente con suministro cortado paga
su deuda, para que el administrador de cuadrilla pueda asignar la
reconexión el mismo día del pago (requisito no funcional del PRD).

## Criterios de decisión

- Compatibilidad con la infraestructura existente
- Oportunidad de detección (rapidez para cumplir "mismo día")
- Complejidad de implementación
- Experiencia del equipo con la tecnología

## Alternativas consideradas

### 1. Polling periódico + notificación push (Firebase Cloud Messaging)
Un script Python ya existente corre cada 5 minutos, consulta la tabla de
pagos, marca los pagos detectados, y dispara una notificación push vía
Firebase Cloud Messaging (FCM) hacia el administrador de cuadrilla.

### 2. Webhook / evento en tiempo real desde facturación
El sistema de facturación notificaría activamente en el momento del
pago, sin esperar el ciclo de 5 minutos.

## Decisión

**[DECISIÓN APROBADA]** Se adopta la **Alternativa 1**: mantener el
script Python de polling cada 5 minutos ya existente como mecanismo de
detección, e integrar **Firebase Cloud Messaging** para notificar al
administrador de cuadrilla en cuanto el script detecta un pago.

## Consecuencias

### Positivas
- Reutiliza un mecanismo ya existente y probado (el script Python), sin
  necesidad de modificar el sistema de facturación.
- Firebase Cloud Messaging es un servicio gestionado, con SDKs maduros
  para Android — compatible con la restricción confirmada de que la app
  de cuadrillas es Android-only en la v1.
- Bajo acoplamiento: un fallo en el sistema de corte/reconexión no
  afecta al sistema de facturación.

### Negativas o trade-offs
- Existe una ventana de demora de hasta 5 minutos entre el pago real y
  su detección. Frente al requisito de "mismo día", esta ventana no
  debería comprometer el cumplimiento, pero conviene monitorear casos
  límite (pagos muy cercanos al cierre del horario operativo).
- Introduce una dependencia externa a un servicio de terceros (Firebase/
  Google) para la notificación.
- **[DECISIÓN APROBADA]** Si la notificación push no llega o no se
  atiende a tiempo, actualmente **no existe un mecanismo automatizado de
  respaldo**: la única alternativa es la comunicación personal directa
  con el cuadrillero o el administrador. Este es un riesgo operativo
  conocido y aceptado para la v1.

## Evidencia y validación
- El script Python de polling cada 5 minutos ya existe y está en
  funcionamiento (confirmado por el autor).
- Pendiente: prototipo de integración con Firebase Cloud Messaging desde
  el script existente.

## Revisión
Revisar esta decisión si el volumen de pagos crece al punto de que la
ventana de 5 minutos deje de ser adecuada, si se evalúa migrar el sistema
de facturación a un modelo basado en eventos en tiempo real, o si se
decide construir un mecanismo automatizado de respaldo ante fallos de
notificación.