# ERD — Sistema de Corte y Reconexión de Suministro

Basado en docs/prd/PRD.md

## Diagrama

​```mermaid
erDiagram
USUARIO {
uuid id PK
string nombre
string rol
}

    CUADRILLA {
        uuid id PK
        string nombre_o_codigo
        boolean activa
    }

    CUADRILLA_USUARIO {
        uuid id PK
        uuid cuadrilla_id FK
        uuid usuario_id FK
    }

    SUMINISTRO {
        uuid id PK
        string codigo_cuenta
        string estado
    }

    MEDIDOR {
        uuid id PK
        uuid suministro_id FK
        string numero_serie
        string estado_ubicacion
    }

    ORDEN_CORTE {
        uuid id PK
        uuid suministro_id FK
        uuid cuadrilla_id FK
        string estado
        timestamp fecha_asignacion
    }

    REGISTRO_CORTE {
        uuid id PK
        uuid orden_corte_id FK
        uuid usuario_id FK
        boolean efectivo
        string motivo
        boolean medidor_retirado
        timestamp fecha_registro
    }

    INGRESO_DEPOSITO {
        uuid id PK
        uuid medidor_id FK
        uuid usuario_id FK
        timestamp fecha_ingreso
    }

    ORDEN_RECONEXION {
        uuid id PK
        uuid suministro_id FK
        uuid cuadrilla_id FK
        uuid asignado_por_id FK
        string estado
        timestamp fecha_asignacion
    }

    CUADRILLA ||--o{ CUADRILLA_USUARIO : agrupa
    USUARIO ||--o{ CUADRILLA_USUARIO : pertenece
    SUMINISTRO ||--o{ MEDIDOR : tiene
    SUMINISTRO ||--o{ ORDEN_CORTE : genera
    CUADRILLA ||--o{ ORDEN_CORTE : asignada_a
    ORDEN_CORTE ||--|| REGISTRO_CORTE : produce
    USUARIO ||--o{ REGISTRO_CORTE : registra
    MEDIDOR ||--o{ INGRESO_DEPOSITO : "puede_tener"
    USUARIO ||--o{ INGRESO_DEPOSITO : registra
    SUMINISTRO ||--o{ ORDEN_RECONEXION : genera
    CUADRILLA ||--o{ ORDEN_RECONEXION : asignada_a
    USUARIO ||--o{ ORDEN_RECONEXION : asigna
​```

## Notas de auditoría

- **USUARIO** [DECISIÓN APROBADA]: entidad base para autenticación de
  todos los roles (cuadrillero, administrador de cuadrilla, funcionario
  de depósito), con usuario independiente por persona.
- **CUADRILLA** [DECISIÓN APROBADA]: equipo fijo de 2-3 personas.
- **CUADRILLA_USUARIO** [DECISIÓN APROBADA]: relación N:N fija entre
  cuadrilla y usuarios; no requiere vigencia temporal porque el personal
  no rota entre equipos.
- **`rol` en USUARIO** [PROPUESTA IA, requiere confirmación]: campo simple
  de texto. Si los permisos se vuelven más complejos a futuro, convendría
  una tabla de roles separada. Para el alcance de v1, alcanza.
- **ORDEN_CORTE ↔ REGISTRO_CORTE (1:1)** [DECISIÓN APROBADA]: confirmado
  que una orden de corte se procesa una única vez, sin reprocesamiento.
- **`ORDEN_CORTE.cuadrilla_id`** [PROPUESTA IA]: la orden se asigna a la
  cuadrilla como equipo. **`REGISTRO_CORTE.usuario_id`** [PROPUESTA IA]:
  identifica a la persona específica dentro de la cuadrilla que hizo el
  registro. **Pregunta abierta:** ¿es correcto este supuesto, o el
  registro debería quedar a nivel de cuadrilla sin diferenciar persona?
- **INGRESO_DEPOSITO opcional** [DECISIÓN APROBADA]: no todo corte genera
  un ingreso a depósito (si el pago es el mismo día, el medidor no llega
  a depósito).
- **No se incluyen datos sensibles** del cliente más allá del código de
  cuenta, en línea con la restricción de privacidad por diseño.

## Preguntas abiertas para resolver antes de implementar

1. ¿El registro de corte debe diferenciar qué persona específica de la
   cuadrilla lo hizo, o alcanza con registrar la cuadrilla como equipo?
2. ¿El estado del medidor (`estado_ubicacion`) se modela como campo
   simple o como una entidad de historial de movimientos?
3. ¿"ORDEN_RECONEXION" requiere su propio registro de ejecución (similar
   a REGISTRO_CORTE), o el estado de la orden es suficiente evidencia de
   que se completó?