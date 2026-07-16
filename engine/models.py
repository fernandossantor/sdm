from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================================
# CONTEXTO DE DECISÃO
# ==========================================================

@dataclass
class DecisionContext:

    briefing: dict

    objetivo: dict

    audiencias: list

    inventarios: list

    inventarios_objetivos: list

    inventarios_kpis: list

    metricas: list

    consumo: list


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
# RESULTADO DA DECISÃO
# ==========================================================

@dataclass
class DecisionResult:

    inventarios: List[InventarioPlano] = field(default_factory=list)

    verba_total: float = 0.0

    observacoes: List[str] = field(default_factory=list)