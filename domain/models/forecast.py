from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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
    consolidado: Dict[str, Any] = field(default_factory=dict)

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
        valor = self.consolidado.get("investimento")
        if valor is not None:
            return round(float(valor), 2)
        return round(sum(i.verba for i in self.itens), 2)

    def _total(self, campo):
        valor = self.consolidado.get(campo)
        if valor is not None:
            return valor
        valores = [getattr(item, campo) for item in self.itens]
        if not valores or any(item is None for item in valores):
            return None
        return sum(valores)

    # ------------------------------------------------------

    @property
    def impressoes(self):
        return self._total("impressoes")

    # ------------------------------------------------------

    @property
    def alcance(self):
        valor = self.consolidado.get("alcance_liquido_pessoas")
        if valor is not None:
            return valor
        return self._total("alcance")

    # ------------------------------------------------------

    @property
    def cliques(self):
        return self._total("cliques")

    # ------------------------------------------------------

    @property
    def conversoes(self):
        return self._total("conversoes")

    # ------------------------------------------------------

    @property
    def ctr_medio(self):
        if self.impressoes is None or self.cliques is None:
            return None
        return (
            round(self.cliques / self.impressoes * 100, 2)
            if self.impressoes
            else None
        )

    # ------------------------------------------------------

    @property
    def cpm_medio(self):
        if self.impressoes is None:
            return None
        return (
            round(self.verba_total * 1000 / self.impressoes, 2)
            if self.impressoes
            else None
        )

    # ------------------------------------------------------

    @property
    def cpc_medio(self):
        if self.cliques is None:
            return None
        return round(self.verba_total / self.cliques, 2) if self.cliques else None

    # ------------------------------------------------------

    @property
    def cpa_medio(self):
        if self.conversoes is None:
            return None
        return (
            round(self.verba_total / self.conversoes, 2)
            if self.conversoes
            else None
        )
