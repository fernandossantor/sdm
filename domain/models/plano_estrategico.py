from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================================
# ITEM DO PLANO
# ==========================================================

@dataclass
class PlanoItem:

    inventario: str

    plataforma: str

    ambiente: str

    papel: str

    score: float

    verba: float

    percentual: float

    score_mcp: Optional[float] = None

    objetivo_score: float = 0.0

    kpi_score: float = 0.0

    audiencia_score: float = 0.0

    metricas_score: float = 0.0

    justificativas: List[str] = field(default_factory=list)

    inventario_id: str = ""

    preco_unitario: float = 0.0

    unidade_compra: str = ""

    quantidade_estimada: Optional[float] = None

    impressoes_estimadas: Optional[float] = None

    alcance_estimado: Optional[float] = None


# ==========================================================
# PLANO ESTRATÉGICO
# ==========================================================

@dataclass
class PlanoEstrategico:

    cliente: str

    campanha: str

    objetivo: str

    orcamento: float

    itens: List[PlanoItem] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    tipo_flight: str = "LINEAR"

    frequencia_objetivo: str = "MEDIA"

    frequencia_alvo: float = 5

    alcance_objetivo: str = "MEDIO"

    alcance_percentual: float = 60

    grp: float = 300

    publico_referencia: int = 0

    alcance_meta: int = 0

    alcance_projetado: int = 0

    kpis: List[dict] = field(default_factory=list)

    cronograma: List[dict] = field(default_factory=list)

    # ------------------------------------------------------

    def adicionar_item(self, item: PlanoItem):

        self.itens.append(item)

    # ------------------------------------------------------

    @property
    def verba_total(self):

        return sum(

            item.verba

            for item in self.itens

        )

    # ------------------------------------------------------

    @property
    def principal(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "PRINCIPAL"

            ]

        )

    # ------------------------------------------------------

    @property
    def complementar(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "COMPLEMENTAR"

            ]

        )

    # ------------------------------------------------------

    @property
    def apoio(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "APOIO"

            ]

        )

    # ------------------------------------------------------

    @property
    def opcional(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "OPCIONAL"

            ]

        )
