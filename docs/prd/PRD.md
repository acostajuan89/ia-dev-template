## 1. Problema y objetivo

**Problema (corte):** [HECHO] No existe un mecanismo digital para que las
cuadrillas de campo registren en el momento si un corte de suministro de
agua fue efectivizado.

**Problema (reconexión):** [HECHO] Actualmente la reconexión depende de
que un operador reciba la notificación del pago y, de forma manual,
gestione que el servicio se reconecte. Este paso intermedio manual
introduce demora y dependencia de una persona.

**Objetivo:** [DECISIÓN APROBADA] Construir una aplicación para que las
cuadrillas registren en línea el resultado de los cortes y gestionen las
reconexiones. Esta es la visión final del sistema; se espera llegar a
ella de forma progresiva, no necesariamente completa en la primera versión.

## 2. Alcance

### Incluido en esta versión
- [DECISIÓN APROBADA] Registro de corte efectivo por parte de la cuadrilla.
- [DECISIÓN APROBADA] Registro de motivo cuando el corte no pudo efectivizarse.
- [DECISIÓN APROBADA] Asignación de la reconexión a una cuadrilla una vez
  confirmado el pago de la deuda (la cuadrilla recibe la tarea de reconexión
  directamente, sin depender de que el operador la comunique manualmente).
- [PREGUNTA ABIERTA] Consulta del estado de un cliente (cortado / reconectado
  / pendiente) — no confirmado si esto es parte de la v1 o se infiere como
  necesario para que la cuadrilla vea sus tareas asignadas.
- [DECISIÓN APROBADA] Registro del retiro del medidor asociado a un corte, y su ingreso al depósito.

### Fuera de alcance
- [DECISIÓN APROBADA] Facturación y cálculo de deuda: lo gestiona otro sistema.
- [PREGUNTA ABIERTA] Notificaciones automáticas al cliente.
- [PREGUNTA ABIERTA] Exportación de reportes históricos.

## 3. Usuarios y sistemas involucrados

- **Cuadrilla de corte** [HECHO]: usuario de campo que ejecuta el corte
  físico (incluyendo el retiro del medidor cuando corresponda) y registra
  el resultado.
- **Administrador de cuadrilla** [DECISIÓN APROBADA]: rol que asigna los
  cortes/reconexiones a cada cuadrilla.
- **Sistema de facturación** [DECISIÓN APROBADA]: origen de la deuda y de
  la confirmación del pago que habilita la reconexión.
- **Cliente** [HECHO]: usuario final afectado por el corte/reconexión.
- **Funcionario de depósito** [DECISIÓN APROBADA]: recibe y registra el
  ingreso del medidor retirado al depósito. Nota de alcance: el depósito
  solo se contempla en el contexto del proceso de corte/reconexión; otros
  motivos de movimiento de medidores quedan fuera de este PRD.
- 
## 4. Entidades y reglas de negocio

- **Suministro/Cliente** [HECHO]: identificado por código de cuenta o medidor.
- **Medidor** [DECISIÓN APROBADA]: unidad física identificable, asociada a
  un suministro. Debe trackearse individualmente porque el mismo medidor
  retirado se reinstala en la reconexión.
- **Orden de Corte** [HECHO]: instrucción para que una cuadrilla corte un
  suministro.
- **Registro de Corte** [HECHO]: resultado de la ejecución (efectivo / no
  efectivo + motivo), incluye si hubo retiro de medidor.
- **Ingreso a Depósito** [DECISIÓN APROBADA]: registro de que un medidor
  retirado llegó físicamente al depósito, hecho por el funcionario de
  depósito (no por la cuadrilla).
- **Orden de Reconexión** [HECHO]: instrucción generada tras el pago de
  la deuda, asignada directamente a una cuadrilla.

**Regla:** [DECISIÓN APROBADA] El flujo de reconexión depende de si el
pago ocurre el mismo día del corte, pero en ambos casos es el
**administrador de cuadrilla** quien asigna la reconexión:
- **Pago en el mismo día:** el medidor no llega a ingresar al depósito
  (la cuadrilla todavía lo tiene consigo). El administrador de cuadrilla
  asigna la reconexión de forma más ágil, ya que no depende de la
  confirmación de ingreso a depósito.
- **Pago en un día posterior:** el medidor ya fue entregado e ingresado
  al depósito por el funcionario correspondiente. Al confirmarse el
  pago, el administrador de cuadrilla asigna la reconexión, y la
  cuadrilla retira el medidor del depósito para reinstalarlo.

**Regla:** [PROPUESTA IA — requiere confirmación] No se puede reconectar
sin un registro de corte previo asociado al mismo suministro.

## 5. Historias de usuario y criterios de aceptación

**Historia 1** [DECISIÓN APROBADA]: Como integrante de una cuadrilla,
quiero registrar si logré efectivizar un corte (incluyendo si retiré el
medidor), para que el sistema actualice el estado del suministro.

*Criterio de aceptación:* Dado un suministro con orden de corte pendiente,
cuando la cuadrilla registra "corte efectivo" indicando si retiró el
medidor, entonces el estado del suministro cambia a "cortado" con
timestamp y queda registrado si el medidor fue retirado.

**Historia 2** [DECISIÓN APROBADA]: Como integrante de una cuadrilla,
quiero registrar el motivo cuando no pude efectivizar un corte, para que
quede evidencia del intento.

*Criterio de aceptación:* Dado un suministro con orden de corte pendiente,
cuando la cuadrilla registra "no efectivizado" con uno de los motivos
válidos, entonces el sistema guarda el motivo y el estado queda como
"pendiente".

**Motivos válidos confirmados** [DECISIÓN APROBADA]:
- El usuario paga en el momento y muestra comprobante (el corte no se
  efectiviza porque ya no corresponde).
- Condiciones físicas del medidor no permiten su retiro (ej. medidor
  trancado).

[PREGUNTA ABIERTA]: ¿Existen otros motivos válidos además de estos dos
(ej. domicilio inaccesible, cliente ausente, medidor no ubicable)?

[PREGUNTA ABIERTA]: Cuando el usuario paga en el momento y muestra
comprobante, ¿la cuadrilla puede aceptar ese comprobante y cancelar el
corte por su cuenta, o debe validarse contra el sistema de facturación
antes de confirmar que el corte no se efectiviza?

**Historia 3** [DECISIÓN APROBADA]: Como funcionario de depósito, quiero
registrar el ingreso de un medidor retirado, para que quede constancia de
su custodia hasta el pago.

*Criterio de aceptación:* Dado un corte efectivo con retiro de medidor,
cuando el funcionario de depósito registra su ingreso, entonces el medidor
queda marcado como "en depósito" asociado a ese suministro.

**Historia 4** [DECISIÓN APROBADA]: Como administrador de cuadrilla,
quiero ver cuándo un cliente cortado pagó su deuda, para asignar la
reconexión a una cuadrilla.

*Criterio de aceptación:* Dado un suministro en estado "cortado", cuando
se confirma el pago de la deuda, entonces el administrador de cuadrilla
puede ver el caso disponible para asignar reconexión (con indicación de
si el medidor está en depósito o aún con la cuadrilla, si el pago fue el
mismo día).

**Historia 5** [DECISIÓN APROBADA]: Como integrante de una cuadrilla,
quiero recibir una orden de reconexión asignada, para reinstalar el
medidor correspondiente.

*Criterio de aceptación:* Dado un suministro con reconexión asignada,
cuando la cuadrilla completa la reinstalación, entonces el estado del
suministro cambia a "reconectado" con timestamp.

## 6. Requisitos no funcionales

- **Conectividad** [DECISIÓN APROBADA]: la aplicación funciona en línea
  (no se contempla modo offline). Las cuadrillas deben tener conexión a
  internet en el momento de registrar cortes y reconexiones.

- **Seguridad/Autenticación** [DECISIÓN APROBADA]: cada cuadrillero cuenta
  con usuario independiente (no se comparte usuario por cuadrilla), lo
  que permite identificar individualmente quién ejecutó cada acción.

- **Tiempo de reconexión** [DECISIÓN APROBADA]: cuando el pago se confirma,
  la reconexión debe quedar físicamente completada (medidor reinstalado y
  registrado) dentro del mismo día del pago.

- **Auditoría** [HECHO]: todo registro (corte, ingreso a depósito,
  reconexión) debe quedar trazado con usuario y timestamp.
- 
## 7. Restricciones

- **Integración con facturación** [DECISIÓN APROBADA]: el sistema debe
  contar con una API que esté atenta (monitoree) los pagos registrados en
  el sistema de facturación, para detectar cuándo un cliente cortado
  regularizó su deuda.

- **Dispositivo/Plataforma cuadrillas** [DECISIÓN APROBADA]: la aplicación
  para cuadrillas se lanza en su primera versión solo para **Android**. No
  es necesario un teléfono de alta gama (gama media/baja es suficiente).

- **Plataforma administrador/depósito** [DECISIÓN APROBADA]: el
  administrador de cuadrilla y el funcionario de depósito operan desde una
  interfaz web, accedida desde computadora.

## 8. Dependencias y riesgos

- **Dependencia** [DECISIÓN APROBADA]: el sistema depende de que la API
  de integración con facturación detecte correctamente y a tiempo los
  pagos registrados, dado que el requisito no funcional exige reconexión
  el mismo día del pago.

- **Riesgo** [DECISIÓN APROBADA — reformulado]: al no existir modo
  offline, si la cuadrilla se encuentra sin conexión a internet en el
  domicilio del cliente, no podrá registrar el corte ni la reconexión en
  el momento, lo que podría comprometer el cumplimiento del plazo de
  "mismo día" para la reconexión.

- **Riesgo** [PROPUESTA IA — nuevo, requiere confirmación]: si la API que
  monitorea pagos falla o tiene demoras, podría no detectarse un pago a
  tiempo, incumpliendo el requisito de reconexión en el mismo día.

## 9. Preguntas abiertas

1. ¿Existen otros motivos válidos de no-corte además de "pago con
   comprobante en el momento" y "condiciones físicas del medidor no
   permiten su retiro" (ej. domicilio inaccesible, cliente ausente)?

2. Cuando el usuario paga en el momento y muestra comprobante, ¿la
   cuadrilla puede aceptar ese comprobante y cancelar el corte por su
   cuenta, o debe validarse contra el sistema de facturación antes de
   confirmar que el corte no se efectiviza?

3. ¿La "consulta de estado de un cliente" (cortado/reconectado/pendiente)
   es parte explícita de la v1, o se resuelve implícitamente a través de
   las pantallas de asignación de tareas?

4. ¿Qué patrón de integración usa la API que monitorea los pagos del
   sistema de facturación (polling periódico, webhook/evento disparado
   por facturación, u otro)? — Esto se definirá formalmente en el ADR.

5. Notificaciones automáticas al cliente y exportación de reportes
   históricos quedaron fuera de alcance — confirmar que esto es
   definitivo y no una omisión.

## 10. Evidencia de aceptación

- **Tests automatizados** sobre las reglas de estado del suministro
  (pendiente → cortado → reconectado) y sus transiciones válidas/inválidas.
- **Tests sobre el flujo de medidor**: retiro, ingreso a depósito (o no,
  si es pago el mismo día), y reinstalación del mismo medidor.
- **Revisión manual** del flujo completo con el área operativa de
  cuadrillas y con el administrador de cuadrilla.
- **Demostración en ambiente de prueba** con datos sintéticos, cubriendo
  al menos: corte efectivo con retiro, corte no efectivizado (ambos
  motivos), reconexión mismo día, reconexión con medidor en depósito.
- **Medición del cumplimiento del plazo** "reconexión mismo día del pago"
  sobre un conjunto de casos de prueba.
