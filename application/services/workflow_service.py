from application.services.briefing_service import (
    BriefingService
)

from domain.models.workflow_state import (
    WorkflowState
)
from application.services.project_service import ProjectService

class WorkflowService:

    ORDEM = (
        "briefing",
        "mcp_papeis",
        "planejamento",
        "diagnostico",
        "forecast",
        "dashboard",
        "exportacao",
    )

    CHAVES = {
        "mcp_papeis": "mcp_papeis",
        "planejamento": "plano",
        "diagnostico": "diagnostico",
        "forecast": "forecast",
        "dashboard": "dashboard",
        "exportacao": "exportacao",
    }

    def __init__(self):

        self.briefing_service = BriefingService()
        self.projetos = ProjectService()

    # =====================================================
    # STATUS
    # =====================================================

    def status(

        self,

        session_state

    ):

        estado = self.estado(session_state)

        return {
            etapa: getattr(estado, etapa)
            for etapa in self.ORDEM
        }

    def registrar_briefing(self, session_state, referencia):

        session_state["briefing_ref"] = referencia

    def concluir(self, session_state, etapa, valor=True):

        if etapa not in self.CHAVES:
            raise ValueError(f"Etapa de workflow inválida: {etapa}")

        session_state[self.CHAVES[etapa]] = valor
        self.projetos.registrar(session_state, etapa, True)

    def pode_acessar(self, session_state, etapa):

        if etapa not in self.ORDEM:
            raise ValueError(f"Etapa de workflow inválida: {etapa}")

        estado = self.status(session_state)
        indice = self.ORDEM.index(etapa)

        return all(estado[nome] for nome in self.ORDEM[:indice])
    
    # =====================================================
    # ESTADO GLOBAL
    # =====================================================

    def estado(

        self,

        session_state

    ):

        return WorkflowState(

            briefing=(
                self.briefing_service.existe(session_state)
                or session_state.get("briefing_ref") is not None
                or bool((session_state.get("projeto_progresso") or {}).get("briefing"))
            ),

            planejamento=session_state.get(

                "plano"

            ) is not None or bool((session_state.get("projeto_progresso") or {}).get("planejamento")),

            mcp_papeis=session_state.get("mcp_papeis") is not None or bool((session_state.get("projeto_progresso") or {}).get("mcp_papeis")),

            diagnostico=session_state.get(

                "diagnostico"

            ) is not None or bool((session_state.get("projeto_progresso") or {}).get("diagnostico")),

            forecast=session_state.get(

                "forecast"

            ) is not None or bool((session_state.get("projeto_progresso") or {}).get("forecast")),

            dashboard=session_state.get(

                "dashboard"

            ) is not None or bool((session_state.get("projeto_progresso") or {}).get("dashboard")),

            exportacao=session_state.get(

                "exportacao"

            ) is not None or bool((session_state.get("projeto_progresso") or {}).get("exportacao"))

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
