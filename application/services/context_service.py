from infrastructure.repositories.decision_repository import (
    DecisionRepository
)
from engine.inventory_engine import InventoryEngine


class ContextService:

    def __init__(self):

        self.repository = DecisionRepository()
        self.inventory_engine = InventoryEngine()

    def listar_briefings(self):

        return self.repository.listar_briefings()

    def metricas(self):

        return self.repository.metricas()

    def ranking(self, nome_briefing):

        contexto = self.carregar(nome_briefing)

        return contexto, self.inventory_engine.calcular(contexto)

    # =====================================================
    # BRIEFING DO BANCO
    # =====================================================

    def carregar(

        self,

        nome_briefing

    ):

        return self.repository.carregar_contexto(

            nome_briefing

        )

    # =====================================================
    # BRIEFING DA INTERFACE
    # =====================================================

    def carregar_por_objeto(

        self,

        briefing

    ):

        return self.repository.carregar_contexto_por_objeto(

            briefing

        )
