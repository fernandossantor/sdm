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


    def criar(
        self,
        **kwargs,
    ):
        """Cria um Briefing a partir da interface legada.

        A UI antiga usa nomes em português, enquanto o modelo novo usa nomes
        em inglês. Este método preserva compatibilidade e mantém atributos
        legados no objeto retornado para os serviços antigos.
        """

        briefing = Briefing(
            campaign_id=kwargs.get("campaign_id"),
            company=kwargs.get("cliente", kwargs.get("company", "")),
            product=kwargs.get("produto", kwargs.get("product", "")),
            objectives=kwargs.get("objetivo", kwargs.get("objectives", "")),
            target_audience=kwargs.get("publico", kwargs.get("target_audience", "")),
            budget=kwargs.get("orcamento", kwargs.get("budget", 0)),
            start_date=kwargs.get("inicio", kwargs.get("start_date")),
            end_date=kwargs.get("fim", kwargs.get("end_date")),
            observations=kwargs.get("observacoes", kwargs.get("observations", "")),
        )

        # Atributos esperados pelo fluxo legado de planejamento.
        for key, value in kwargs.items():
            setattr(
                briefing,
                key,
                value,
            )

        briefing.cliente = kwargs.get(
            "cliente",
            briefing.company,
        )
        briefing.campanha = kwargs.get(
            "campanha",
            "",
        )
        briefing.objetivo_id = kwargs.get(
            "objetivo_id",
        )
        briefing.objetivo = kwargs.get(
            "objetivo",
            briefing.objectives,
        )
        briefing.orcamento = kwargs.get(
            "orcamento",
            briefing.budget,
        )
        briefing.inicio = kwargs.get(
            "inicio",
            briefing.start_date,
        )
        briefing.fim = kwargs.get(
            "fim",
            briefing.end_date,
        )

        return briefing


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

