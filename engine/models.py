from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==========================================================
# CONTEXTO DE DECISÃO
# ==========================================================

@dataclass
class DecisionContext:
    briefing: Dict[str, Any]

    objetivo: Dict[str, Any]

    audiencias: List[Dict[str, Any]]

    inventarios: List[Dict[str, Any]]

    inventarios_objetivos: List[Dict[str, Any]]

    inventarios_kpis: List[Dict[str, Any]]

    metricas: List[Dict[str, Any]]

    consumo: List[Dict[str, Any]]

    parametros: Dict[str, Any] = field(default_factory=dict)

    restricoes: List[Dict[str, Any]] = field(default_factory=list)


# ==========================================================
# AMBIENTE DO PLANO
# ==========================================================

@dataclass
class AmbientePlano:
    ambiente: str

    score: float

    percentual: float

    verba: float

    papel: str


# ==========================================================
# INVENTÁRIO DO PLANO
# ==========================================================

@dataclass
class InventarioPlano:
    inventario: str

    plataforma: str

    ambiente: str

    score: float

    percentual: float

    verba: float

    papel: str

    justificativas: List[str] = field(default_factory=list)


# ==========================================================
# ITEM DE DECISÃO
# ==========================================================

@dataclass
class DecisionItem:

    inventario: str

    plataforma: str

    ambiente: str

    score: float

    papel: str

    prioridade: int

    verba: float = 0.0

    percentual: float = 0.0

    confianca: float = 0.0

    justificativas: List[str] = field(default_factory=list)

    riscos: List[str] = field(default_factory=list)

    restricoes: List[str] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    metadados: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# RESULTADO DA DECISÃO
# ==========================================================

@dataclass
class DecisionResult:

    inventarios: List[InventarioPlano] = field(default_factory=list)

    decisoes: List[DecisionItem] = field(default_factory=list)

    verba_total: float = 0.0

    score_global: float = 0.0

    observacoes: List[str] = field(default_factory=list)

    alertas: List[str] = field(default_factory=list)

    erros: List[str] = field(default_factory=list)