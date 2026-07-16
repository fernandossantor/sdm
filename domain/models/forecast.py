from dataclasses import dataclass, field
from typing import List


# ==========================================================
# ITEM
# ==========================================================

@dataclass
class ForecastItem:

    inventario: str

    verba: float

    impressoes: int

    alcance: int

    cliques: int

    conversoes: int

    ctr: float

    cpm: float

    cpc: float

    cpa: float


# ==========================================================
# FORECAST
# ==========================================================

@dataclass
class Forecast:

    itens: List[ForecastItem] = field(default_factory=list)

    # ------------------------------------------------------

    def adicionar(

        self,

        item: ForecastItem

    ):

        self.itens.append(

            item

        )

    # ------------------------------------------------------

    @property
    def verba_total(self):

        return round(

            sum(

                i.verba

                for i in self.itens

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def impressoes(self):

        return sum(

            i.impressoes

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def alcance(self):

        return sum(

            i.alcance

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def cliques(self):

        return sum(

            i.cliques

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def conversoes(self):

        return sum(

            i.conversoes

            for i in self.itens

        )

    # ------------------------------------------------------

    @property
    def ctr_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                i.ctr

                for i in self.itens

            )

            /

            len(self.itens),

            2

        )

    # ------------------------------------------------------

    @property
    def cpm_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                i.cpm

                for i in self.itens

            )

            /

            len(self.itens),

            2

        )

    # ------------------------------------------------------

    @property
    def cpc_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                i.cpc

                for i in self.itens

            )

            /

            len(self.itens),

            2

        )

    # ------------------------------------------------------

    @property
    def cpa_medio(self):

        if not self.itens:

            return 0

        return round(

            sum(

                i.cpa

                for i in self.itens

            )

            /

            len(self.itens),

            2

        )