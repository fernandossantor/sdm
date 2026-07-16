from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


class ContextService:

    def __init__(self):

        self.repository = DecisionRepository()

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