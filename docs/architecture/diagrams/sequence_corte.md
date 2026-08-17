# Diagrama de secuencia — Registro de corte

Basado en docs/prd/PRD.md, Historias 1 y 2.

## Diagrama

```mermaid
sequenceDiagram
actor Cuadrillero
participant App as App Android (Cuadrilla)
participant API as API Corte y Reconexión
participant DB as Base de datos

    Cuadrillero->>App: Abre orden de corte asignada
    App->>API: GET /ordenes-corte/{id}
    API->>API: Validar sesion/usuario autenticado
    API->>DB: Consultar orden de corte
    DB-->>API: Datos de la orden
    API-->>App: Detalle de la orden

    Cuadrillero->>App: Registra resultado del corte

    alt Corte efectivo
        App->>API: POST /ordenes-corte/{id}/registro (efectivo=true, medidor_retirado)
        API->>API: Validar que la orden no tenga registro previo
        API->>DB: Guardar REGISTRO_CORTE (efectivo)
        API->>DB: Actualizar estado SUMINISTRO = "cortado"
        DB-->>API: Confirmacion
        API-->>App: 200 OK - Corte registrado
    else Corte no efectivizado
        App->>API: POST /ordenes-corte/{id}/registro (efectivo=false, motivo)
        API->>API: Validar motivo dentro de lista permitida
        API->>DB: Guardar REGISTRO_CORTE (no efectivo, motivo)
        DB-->>API: Confirmacion
        API-->>App: 200 OK - Registro guardado, suministro sigue "pendiente"
    end
    ```


## Auditoría del diagrama

- **¿Cada mensaje representa una interacción real?** Sí, cada llamada
  corresponde a una acción descrita en las Historias 1 y 2 del PRD.
- **¿El orden respeta la lógica?** Sí: primero se consulta la orden
  asignada, luego se registra el resultado.
- **¿Hay autorización antes de consultar?** [DECISIÓN APROBADA] Se agregó
  validación de sesión/usuario autenticado, en línea con el requisito no
  funcional de seguridad del PRD (usuario independiente por persona).
- **¿Se muestra un flujo alternativo?** Sí — corte efectivo vs. no
  efectivizado, cubriendo la Historia 2 con motivo.
- **¿No se expone información sensible?** No se incluyen datos de
  autenticación ni datos personales del cliente más allá de lo necesario.
- **No se inventaron servicios externos**: no aparece facturación ni
  ningún sistema no confirmado en este flujo (el corte es autónomo del
  pago).

## Preguntas abiertas

1. ¿Existe alguna validación adicional antes de permitir el registro
   (ej. geolocalización, verificación de que el cuadrillero está en el
   domicilio correcto)? No confirmado en el PRD — no se incluyó en el
   diagrama para no inventar.
2. El caso de "el cliente paga en el momento y muestra comprobante"
   (uno de los motivos válidos de no-corte) podría requerir una llamada
   adicional a facturación para validar el pago — no se incluyó en este
   diagrama porque el PRD lo dejó como pregunta abierta (Sección 5,
   Historia 2). Se recomienda un segundo diagrama si esta validación se
   confirma como necesaria.