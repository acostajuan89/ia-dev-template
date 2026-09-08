# Postmortem · Proyecto Final Juan Acosta · Septiembre 2026

## Qué funcionó

- Migrar de un Mock LLM a integración real con Claude (Anthropic) permitió
  detectar en vivo un caso real de alucinación: sin el paso de retrieval
  conectado, el modelo inventó con total confianza un "Departamento de
  Corte y Reconexión de ESSAP" y un plazo de "24 horas hábiles" que no
  existen en el PRD. Esto se corrigió conectando el flujo RAG completo
  (retriever → contexto → generación), y quedó documentado como evidencia
  comparativa (antes/después) en AI_USAGE.md.
- El diseño vendor-agnostic (Protocol + adapters) permitió cambiar de
  OpenAI/Mock a Anthropic sin reescribir el resto del sistema — solo se
  agregó un adapter nuevo y una variable de entorno (AI_PROVIDER).
- Reutilizar la documentación ya construida en módulos anteriores (PRD,
  ADR) como base de conocimiento del RAG evitó escribir contenido nuevo
  y garantizó que las respuestas del agente fueran consistentes con las
  reglas de negocio ya validadas.

## Qué no funcionó

- El primer Eval Set (6 casos) dio 4/6 en la primera corrida, pero los
  2 fallos no eran errores reales del agente: eran criterios de
  evaluación demasiado rígidos (comparación de texto exacto en vez de
  conceptos equivalentes). Hubo que ajustar la lógica de evaluación
  (de "todas las frases esperadas" a "al menos una"), no el agente.
- El SDK de Anthropic instalado no aceptaba el parámetro `temperature`
  en la llamada `messages.create()`, algo que no se esperaba dado que
  es un parámetro estándar de otras integraciones de LLM. Se resolvió
  inspeccionando la firma real del método y quitando el parámetro.
- Claude devolvió el JSON envuelto en un bloque de código Markdown
  (con las tres comillas invertidas que delimitan bloques de código)
  a pesar de que las instrucciones decían explícitamente "sin
  Markdown" — el modelo no siempre obedece instrucciones de formato
  al 100%, incluso siendo explícitas.

## Qué haría distinto

- Definiría el Eval Set con criterios de evaluación más flexibles desde
  el principio (múltiples frases válidas por caso), en vez de descubrir
  el problema recién en la primera corrida.
- Probaría la integración con la API real desde el inicio del desarrollo
  (en vez de empezar con el Mock), para detectar antes comportamientos
  específicos del proveedor real (como el wrapper de Markdown).

## 3 lecciones aprendidas

1. **Sobre agentes/RAG:** un agente sin el paso de recuperación conectado
   no es "menos preciso" — puede ser activamente peligroso, porque
   responde con la misma confianza tanto si tiene evidencia real como si
   está inventando. La diferencia solo se nota comparando las respuestas
   con y sin contexto, lado a lado.

2. **Sobre evaluación:** un Eval Set que falla no siempre significa que
   el sistema esté mal — puede significar que el criterio de evaluación
   está mal diseñado. Antes de "arreglar el agente", hay que confirmar
   que el criterio de éxito realmente refleja el comportamiento correcto.

3. **Sobre trabajo con IA:** las instrucciones explícitas en el prompt
   ("sin Markdown", "solo JSON") reducen pero no eliminan el margen de
   desobediencia del modelo. El código de la aplicación siempre necesita
   una capa de tolerancia (parseo defensivo) para esos casos, no basta
   con confiar en que el modelo va a cumplir la instrucción al pie de
   la letra.