from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# INDICADOR
# ==========================================================

@dataclass
class DashboardIndicator:

    nome: str

    valor: Any

    unidade: str = ""

    descricao: str = ""


# ==========================================================
# VISUALIZAÇÃO
# ==========================================================

@dataclass
class DashboardVisualization:

    nome: str

    tipo: str

    dados: Any = field(default_factory=list)

    configuracao: dict = field(default_factory=dict)


# ==========================================================
# RESUMO
# ==========================================================

@dataclass
class DashboardSummary:

    score_global: float = 0

    verba_total: float = 0

    quantidade_inventarios: int = 0

    principais: int = 0

    complementares: int = 0

    apoio: int = 0

    opcionais: int = 0


# ==========================================================
# DASHBOARD
# ==========================================================

@dataclass
class DashboardResult:

    resumo: DashboardSummary = field(

        default_factory=DashboardSummary

    )

    indicadores: list[DashboardIndicator] = field(

        default_factory=list

    )

    score: dict = field(

        default_factory=dict

    )

    plano: dict = field(

        default_factory=dict

    )

    forecast: dict = field(

        default_factory=dict

    )

    cenarios: dict = field(

        default_factory=dict

    )

    insights: list = field(

        default_factory=list

    )

    recomendacoes: list = field(

        default_factory=list

    )

    alertas: list = field(

        default_factory=list

    )

    riscos: list = field(

        default_factory=list

    )

    visualizacoes: list[DashboardVisualization] = field(

        default_factory=list

    )