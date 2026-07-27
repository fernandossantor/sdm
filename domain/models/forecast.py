from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================================
# ITEM
# ==========================================================

@dataclass
class ForecastItem:

    inventario: str

    verba: float

    impressoes: Optional[int]

    alcance: Optional[int]

    cliques: Optional[int]

    conversoes: Optional[int]

    ctr: Optional[float]

    cpm: Optional[float]

    cpc: Optional[float]

    cpa: Optional[float]

    lacunas: List[str] = field(default_factory=list)


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
        valores = [i.impressoes for i in self.itens if i.impressoes is not None]
        return sum(valores) if valores else None

    # ------------------------------------------------------

    @property
    def alcance(self):
        valores = [i.alcance for i in self.itens if i.alcance is not None]
        return sum(valores) if valores else None

    # ------------------------------------------------------

    @property
    def cliques(self):
        valores = [i.cliques for i in self.itens if i.cliques is not None]
        return sum(valores) if valores else None

    # ------------------------------------------------------

    @property
    def conversoes(self):
        valores = [i.conversoes for i in self.itens if i.conversoes is not None]
        return sum(valores) if valores else None

    # ------------------------------------------------------

    @property
    def ctr_medio(self):

        valores = [i.ctr for i in self.itens if i.ctr is not None]
        return round(sum(valores) / len(valores), 2) if valores else None

    # ------------------------------------------------------

    @property
    def cpm_medio(self):

        valores = [i.cpm for i in self.itens if i.cpm is not None]
        return round(sum(valores) / len(valores), 2) if valores else None

    # ------------------------------------------------------

    @property
    def cpc_medio(self):

        valores = [i.cpc for i in self.itens if i.cpc is not None]
        return round(sum(valores) / len(valores), 2) if valores else None

    # ------------------------------------------------------

    @property
    def cpa_medio(self):

        valores = [i.cpa for i in self.itens if i.cpa is not None]
        return round(sum(valores) / len(valores), 2) if valores else None
