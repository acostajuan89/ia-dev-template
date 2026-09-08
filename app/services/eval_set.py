"""
app/services/eval_set.py — Conjunto de casos de evaluacion para el
Agente CyR. Cada caso define criterios explicitos y verificables:
fuentes esperadas, hechos que la respuesta debe incluir, y
afirmaciones que NO deberia inventar.
"""

EVAL_SET = [
    {
        "id": "asignacion_reconexion",
        "question": "¿Quién asigna la reconexión de un suministro cortado?",
        "expected_sources": ["PRD.md"],
        "required_facts": ["administrador de cuadrilla"],
        "forbidden_claims": ["departamento de corte", "sistema automatico asigna"],
    },
    {
        "id": "regla_mismo_dia",
        "question": "¿Qué pasa si el cliente paga la deuda el mismo día del corte?",
        "expected_sources": ["PRD.md"],
        "required_facts": ["deposito", "cuadrilla"],  # sin tilde, mas flexible
        "forbidden_claims": ["24 horas", "plazo de 48 horas"],
    },
    {
        "id": "motivos_no_corte",
        "question": "¿Cuáles son los motivos válidos para no efectivizar un corte?",
        "expected_sources": ["PRD.md"],
        "required_facts": ["comprobante", "medidor trancado"],
        "forbidden_claims": ["domicilio cerrado", "perro"],
    },
    {
        "id": "deteccion_pago",
        "question": "¿Cómo se detecta que un cliente pagó su deuda?",
        "expected_sources": ["ADR-0001-deteccion-pagos.md"],
        "required_facts": ["polling", "5 minutos", "Firebase"],
        "forbidden_claims": ["webhook en tiempo real"],
    },
    {
        "id": "plataforma_cuadrillas",
        "question": "¿En qué plataforma opera la aplicación de las cuadrillas?",
        "expected_sources": ["PRD.md"],
        "required_facts": ["Android"],
        "forbidden_claims": ["iOS", "Windows"],
    },
    {
        "id": "canal_pago_deuda",
        "question": "¿El cliente debe pagar la deuda únicamente en oficinas de ESSAP, o existen otros canales habilitados?",
        "expected_sources": [],
        "required_facts": ["no se especifica", "no tengo evidencia", "no se define"],
        "forbidden_claims": ["aplicación móvil", "transferencia bancaria", "billetera electrónica"],
    },
]
