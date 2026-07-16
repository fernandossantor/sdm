from dataclasses import dataclass, field
from typing import List


# ==========================================================
# ITEM DO DIAGNÓSTICO
# ==========================================================

@dataclass
class DiagnosticoInventario:

    inventario: str

    plataforma: str

    ambiente: str

    papel: str

    score: float

    objetivo: float

    kpi: float

    audiencia: float

    metricas: float

    pontos_fortes: List[str] = field(default_factory=list)

    pontos_fracos: List[str] = field(default_factory=list)

    recomendacoes: List[str] = field(default_factory=list)


# ==========================================================
# DIAGNÓSTICO
# ==========================================================

@dataclass
class DiagnosticoPlano:

    cliente: str

    campanha: str

    objetivo: str

    itens: List[DiagnosticoInventario] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    # ------------------------------------------------------

    def adicionar(

        self,

        item: DiagnosticoInventario

    ):

        self.itens.append(

            item

        )

    # ------------------------------------------------------

    @property
    def score_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                i.score

                for i in self.itens

            )

            /

            len(self.itens),

            2

        )

    # ------------------------------------------------------

    @property
    def principais(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "PRINCIPAL"

            ]

        )

    # ------------------------------------------------------

    @property
    def complementares(self):

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
    def opcionais(self):

        return len(

            [

                i

                for i in self.itens

                if i.papel == "OPCIONAL"

            ]

        )

    # ------------------------------------------------------

    @property
    def total_pontos_fortes(self):

        return sum(

            len(

                i.pontos_fortes

            )

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def total_pontos_fracos(self):

        return sum(

            len(

                i.pontos_fracos

            )

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def total_recomendacoes(self):

        return sum(

            len(

                i.recomendacoes

            )

            for i in self.itens

        )