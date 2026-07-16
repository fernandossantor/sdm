from application.services.briefing_service import (
    BriefingService
)

from domain.models.workflow_state import (
    WorkflowState
)

class WorkflowService:

    def __init__(self):

        self.briefing_service = BriefingService()

    # =====================================================
    # STATUS
    # =====================================================

    def status(

        self,

        session_state

    ):

        possui_briefing = self.briefing_service.existe(

            session_state

        )

        return {

            "briefing": possui_briefing,

            "planejamento": False,

            "forecast": False,

            "dashboard": False,

            "exportacao": False

        }
    
    # =====================================================
    # ESTADO GLOBAL
    # =====================================================

    def estado(

        self,

        session_state

    ):

        return WorkflowState(

            briefing=self.briefing_service.existe(

                session_state

            ),

            planejamento=session_state.get(

                "plano"

            ) is not None,

            diagnostico=session_state.get(

                "diagnostico"

            ) is not None,

            forecast=session_state.get(

                "forecast"

            ) is not None,

            dashboard=session_state.get(

                "dashboard"

            ) is not None,

            exportacao=session_state.get(

                "exportacao"

            ) is not None

        )

        # =====================================================
    # PRÓXIMA ETAPA
    # =====================================================

    def proxima_etapa(

        self,

        session_state

    ):

        estado = self.estado(

            session_state

        )

        return estado.proxima_etapa
    
    # =====================================================
    # PROGRESSO
    # =====================================================

    def progresso(

        self,

        session_state

    ):

        estado = self.estado(

            session_state

        )

        return {

            "total": estado.total,

            "concluidas": estado.concluidas,

            "percentual": estado.percentual

    }