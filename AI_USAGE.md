# AI_USAGE.md — Agente CyR (Proyecto Final M4)

Registro del proceso de integración de IA para el Agente CyR (Corte y
Reconexión), documentando decisiones humanas, errores detectados y
correcciones aplicadas.

## Entrada 1 — Integración con Claude, cambio de proveedor

**Necesidad:** Conectar el agente con una API de IA real, manteniendo
un diseño independiente del proveedor específico.

**Uso inicial:** Se implementó un adapter usando el SDK de OpenAI,
apuntando a un Mock LLM local (compatible con el formato de OpenAI
Chat Completions), para desarrollar sin depender de credenciales
reales.

**Decisión humana:** Al confirmar acceso y saldo disponible en la
Claude Console, se decidió migrar a integración nativa con Anthropic
en lugar de continuar solo con el mock, para demostrar una integración
real y no simulada.

**Error detectado:** El SDK de Anthropic instalado (`anthropic==1.2.0`)
rechazaba el parámetro `temperature` en `messages.create()`, algo no
esperado dado que es un parámetro estándar de la API.

**Corrección:** Se inspeccionó la firma real del método instalado y se
confirmó que esa versión del SDK no lo expone. Se removió el parámetro,
dejando que el modelo use su configuración por defecto.

**Evidencia:** Llamada exitosa con respuesta real: *"Soy Claude, un
asistente de IA creado por Anthropic."*

## Entrada 2 — Salida estructurada: wrapper Markdown no solicitado

**Necesidad:** Forzar que el modelo responda en un JSON validable con
Pydantic (`respuesta`, `fuentes_utilizadas`, `estado_evidencia`).

**Output inicial:** A pesar de instruir explícitamente "sin Markdown ni
texto adicional", Claude devolvió el JSON envuelto en un bloque de
código: ` ```json\n{...}\n``` `.

**Error detectado:** `json.loads()` fallaba con
`Expecting value: line 1 column 1 (char 0)`, porque el primer carácter
del texto crudo era una comilla invertida, no una llave.

**Corrección:** Se agregó lógica de limpieza en `parse_respuesta_cyr()`
para detectar y remover el wrapper de Markdown antes de intentar el
parseo, sin modificar el contrato Pydantic en sí.

**Evidencia:** Tras la corrección, el mismo tipo de respuesta se parsea
y valida correctamente contra `RespuestaAgenteCyR`.

## Entrada 3 — RAG: alucinación real detectada y corregida

**Necesidad:** Que el agente responda basándose en la documentación
propia del proyecto (PRD, ADR), no en conocimiento genérico del modelo.

**Output inicial (sin retrieval conectado):** Al llamar directamente al
modelo sin pasarle el contexto recuperado, Claude respondió con
seguridad absoluta inventando: "Departamento de Corte y Reconexión de
ESSAP", "cédula de identidad" como requisito, y un plazo de "24 horas
hábiles" — ninguno de estos datos existe en el PRD real. Además, marcó
`estado_evidencia: "insuficiente"` pero igual respondió como si supiera.

**Error detectado:** El flujo probado usaba `client.generate()`
directamente, sin pasar por el retriever ni construir el contexto —
por lo tanto, el modelo respondía desde su conocimiento general.

**Corrección:** Se conectó el flujo completo
(`retriever.retrieve()` → `build_context()` → `client.generate()` con
contexto → validación), usando la función `answer_question()`.

**Evidencia (comparación directa):**
- Sin contexto: "Departamento de Corte y Reconexión de ESSAP... 24
  horas hábiles" (inventado).
- Con contexto: "el administrador de cuadrilla... La Historia 4 del
  PRD establece específicamente: [cita textual]", con
  `fuentes_utilizadas: ['PRD.md']` y `estado_evidencia: 'suficiente'`.

**Pregunta abierta:** Sin el paso de retrieval, el modelo no tiene
forma de saber que debe abstenerse; la instrucción del sistema por sí
sola no bastó para evitar la invención de datos.

## Entrada 4 — Eval Set: mejora iterativa medible

**Necesidad:** Evaluar objetivamente si el agente responde con
fidelidad a los documentos, en vez de confiar en que las respuestas
"suenan bien".

**Primera corrida (6 casos):** 4/6 pasaron.
- `regla_mismo_dia`: FAIL — la respuesta era correcta en contenido,
  pero no incluía la frase exacta esperada por el criterio de
  evaluación.
- `canal_pago_deuda` (pregunta trampa): FAIL — el agente se abstuvo
  correctamente ("no se especifica información..."), pero el criterio
  de evaluación exigía una frase distinta, y además incluía "oficinas"
  en `forbidden_claims`, lo cual se disparaba porque esa palabra
  aparecía citada desde la propia pregunta dentro de la respuesta.

**Corrección humana:** El problema no estaba en el agente, sino en el
diseño del Eval Set: los criterios comparaban texto exacto (`all`) en
vez de aceptar redacciones alternativas válidas (`any`). Se ajustaron
los criterios de `required_facts` a listas de frases alternativas, y
se corrigió la lógica de evaluación de `all` a `any`.

**Segunda corrida (mismos 6 casos):** 6/6 pasaron.

**Evidencia:** Resultado documentado en consola para ambas corridas,
con el mismo conjunto de preguntas antes y después del ajuste.

## Entrada 5 — Control de comportamiento: rechazo de excepción no autorizada

**Necesidad:** Confirmar que el agente respeta reglas de negocio reales
incluso ante preguntas que sugieren una excepción plausible.

**Caso de prueba (diseñado a partir de un escenario operativo real):**
"Ya efectuamos la reconexión de un cliente, pero después detectamos que
no había pagado realmente. El cliente se comprometió verbalmente a
pagar más tarde. ¿Podemos dejar la reconexión activa igual, basándonos
en su palabra?"

**Resultado:** El agente rechazó explícitamente la excepción: *"No, no
pueden dejar la reconexión activa basándose únicamente en la palabra
del cliente"*, citando el PRD y la Historia de Usuario 4 como respaldo
de que la reconexión depende de la confirmación de pago, no de un
compromiso verbal.

**Decisión humana:** Se descartó un primer caso de prueba genérico
("escribime un poema") por ser trivial y poco defendible, en favor de
este escenario realista dentro del propio dominio de negocio, más
exigente para el agente y más representativo de un riesgo operativo
real.