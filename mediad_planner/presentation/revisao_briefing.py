import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo


def apresentar_revisao_briefing(briefing: BriefingResumo) -> None:
    st.subheader("Revisão do Briefing")
    st.caption(
        "Análise do sistema sobre os dados salvos nesta versão. "
        "As declarações permanecem disponíveis nas respectivas subetapas."
    )
    st.info(
        "Esta revisão é parcial. A avaliação completa de coerência e suficiência, "
        "a declaração de inexistência de restrições, a confirmação da aplicabilidade "
        "da jornada e o reconhecimento de pendências ainda estão em desenvolvimento. "
        "A conclusão do Briefing ainda não está disponível."
    )
    if not briefing.apontamentos_revisao:
        st.write(
            "Nenhum apontamento nas verificações disponíveis. "
            "Isso não certifica a conclusão do Briefing."
        )
        return
    st.write(f"Apontamentos: {len(briefing.apontamentos_revisao)}")
    for subetapa in dict.fromkeys(item.subetapa for item in briefing.apontamentos_revisao):
        with st.expander(subetapa, expanded=True):
            for item in briefing.apontamentos_revisao:
                if item.subetapa == subetapa:
                    st.warning(item.mensagem)
