from domain.models.briefing import Briefing

from repositories.briefing_repository import BriefingRepository


class BriefingService:

    def __init__(self):

        self.repository = BriefingRepository()


    def load(

        self,

        campaign_id

    ):

        return self.repository.get_by_campaign(

            campaign_id

        )


    def save(

        self,

        **kwargs

    ):

        briefing = Briefing(

            **kwargs

        )

        return self.repository.save(

            briefing

        )

    # =====================================================
    # SESSION STATE / COMPATIBILIDADE UI
    # =====================================================

    def salvar(
        self,
        session_state,
        briefing,
    ):
        """Salva o briefing no session_state para compatibilidade com a UI."""

        session_state["briefing"] = briefing
        return briefing

    def recuperar(
        self,
        session_state,
    ):
        """Recupera o briefing do session_state para compatibilidade com a UI."""

        return session_state.get("briefing")

    def existe(
        self,
        session_state,
    ):
        """Indica se há briefing carregado no session_state."""

        return session_state.get("briefing") is not None

    def limpar(
        self,
        session_state,
    ):
        """Remove o briefing do session_state para compatibilidade com a UI."""

        session_state.pop("briefing", None)

