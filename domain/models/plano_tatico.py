from dataclasses import dataclass, field
from typing import List


# ==========================================================
# ITEM DO PLANO TÁTICO
# ==========================================================

@dataclass
class PlanoTaticoItem:

    inventario: str

    plataforma: str

    ambiente: str

    papel: str

    percentual: float

    verba: float

    score: float


# ==========================================================
# PLANO TÁTICO
# ==========================================================

@dataclass
class PlanoTatico:

    verba_total: float

    itens: List[PlanoTaticoItem] = field(default_factory=list)

    # ------------------------------------------------------

    def adicionar(

        self,

        item: PlanoTaticoItem

    ):

        self.itens.append(

            item

        )

    # ------------------------------------------------------

    @property
    def verba_distribuida(self):

        return round(

            sum(

                item.verba

                for item in self.itens

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def percentual_total(self):

        return round(

            sum(

                item.percentual

                for item in self.itens

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def principal(self):

        return len(

            [

                item

                for item in self.itens

                if item.papel == "PRINCIPAL"

            ]

        )

    # ------------------------------------------------------

    @property
    def complementar(self):

        return len(

            [

                item

                for item in self.itens

                if item.papel == "COMPLEMENTAR"

            ]

        )

    # ------------------------------------------------------

    @property
    def apoio(self):

        return len(

            [

                item

                for item in self.itens

                if item.papel == "APOIO"

            ]

        )

    # ------------------------------------------------------

    @property
    def opcional(self):

        return len(

            [

                item

                for item in self.itens

                if item.papel == "OPCIONAL"

            ]

        )

    # ------------------------------------------------------

    @property
    def score_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                item.score

                for item in self.itens

            )

            /

            len(self.itens),

            2

        )