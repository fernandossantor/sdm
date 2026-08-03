import streamlit as st

from mediad_planner.application.dto.espaco_trabalho import (
    EspacoTrabalhoCampanhaResumo,
)
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)
from mediad_planner.application.services.aplicacao_espaco_trabalho import (
    AplicacaoEspacoTrabalho,
)
from mediad_planner.presentation.briefings import apresentar_briefing
from mediad_planner.presentation.visao_geral_campanha import (
    apresentar_visao_geral_campanha,
)


def apresentar_espaco_trabalho(
    aplicacao_espaco_trabalho: AplicacaoEspacoTrabalho,
    aplicacao_briefings: AplicacaoBriefings,
    resumo: EspacoTrabalhoCampanhaResumo,
    modulo_ativo: str,
) -> str | None:
    campanha = resumo.campanha
    if modulo_ativo == "VISAO_GERAL":
        abrir_briefing = apresentar_visao_geral_campanha(
            aplicacao_espaco_trabalho,
            resumo,
        )
        if abrir_briefing:
            return "BRIEFING"
        return None
    if modulo_ativo == "BRIEFING":
        apresentar_briefing(aplicacao_briefings, campanha.id_campanha)
        return None
    st.warning("Módulo indisponível nesta etapa.")
    return None
