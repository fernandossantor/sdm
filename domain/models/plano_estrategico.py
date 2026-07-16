from dataclasses import dataclass, field
from typing import List


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

    justificativas: List[str] = field(default_factory=list)


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