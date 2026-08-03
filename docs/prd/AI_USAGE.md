# AI_USAGE.md — Registro de uso de IA (Lab 2)

## Entrada 1 — Generación y auditoría del PRD

**Objetivo:** Generar un primer borrador de PRD para el sistema de
registro de cortes y gestión de reconexiones de suministro de agua.

**Herramienta/modelo:** Claude (Anthropic), usado como asistente de
generación y auditoría conversacional.

**Contexto proporcionado:** Hechos aprobados sobre el proceso de cortemkdir docs\architecture\diagrams
New-Item docs\architecture\diagrams\erd.md
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

## Entrada 2 — ERD: modelo de datos

**Objetivo:** Traducir las entidades del PRD a un diagrama entidad-relación.

**Herramienta/modelo:** Claude (Anthropic).

**Salida obtenida:** Un primer ERD con las entidades principales del
proceso de corte/reconexión (Suministro, Medidor, Orden de Corte,
Registro de Corte, Ingreso a Depósito, Orden de Reconexión), pero sin
ninguna entidad de usuarios o cuadrillas — los roles (cuadrillero,
administrador, funcionario de depósito) quedaron como simples IDs sueltos
sin entidad que los respalde.

**Problema detectado:** Omisión real: la IA no había considerado que los
distintos roles (personas) necesitan su propia entidad para ser
consistente con el requisito de auditoría (usuario independiente por
persona) y con el hecho de que las cuadrillas son equipos de 2-3 personas,
no individuos sueltos.

**Cambio realizado:** Se agregaron las entidades USUARIO, CUADRILLA y la
tabla intermedia CUADRILLA_USUARIO, y se referenciaron correctamente desde
ORDEN_CORTE, REGISTRO_CORTE, INGRESO_DEPOSITO y ORDEN_RECONEXION.

**Preguntas abiertas remanentes:**
- ¿El registro de corte debe diferenciar la persona específica de la
  cuadrilla, o alcanza con registrar la cuadrilla como equipo?
- ¿El estado del medidor se modela como campo simple o como historial?

## Entrada 3 — Diagrama de secuencia: registro de corte

**Objetivo:** Modelar el flujo de registro de corte (efectivo / no
efectivizado) como diagrama de secuencia, cubriendo las Historias 1 y 2
del PRD.

**Herramienta/modelo:** Claude (Anthropic).

**Contexto proporcionado:** PRD.md auditado, con foco en las Historias
1 y 2 (registro de corte efectivo y no efectivizado con motivo).

**Salida obtenida:** Un diagrama de secuencia con actor Cuadrillero, la
App Android, la API y la base de datos, con un flujo alternativo (`alt`)
separando corte efectivo de no efectivizado.

**Decisión humana clave:** Se evaluó si incluir en el diagrama la
validación contra el sistema de facturación para el caso "el cliente
paga en el momento y muestra comprobante" (uno de los motivos de
no-corte). Se decidió **no incluir esa interacción**, porque el PRD la
dejó explícitamente como pregunta abierta (Sección 5, Historia 2) —
incluirla habría significado que la IA (o el autor) inventara un
servicio externo y un contrato de API no confirmados.

**Cambio realizado:** Se agregó explícitamente la validación de sesión/
usuario autenticado antes de consultar la orden, en línea con el
requisito no funcional de seguridad (usuario independiente por persona)
que sí está confirmado en el PRD.

**Evidencia / preguntas abiertas remanentes:**
- ¿Existe validación de geolocalización antes de permitir el registro?
- ¿La validación de "pago con comprobante en el momento" requiere una
  llamada síncrona a facturación? — Pendiente de un segundo diagrama de
  secuencia si se confirma esta necesidad.