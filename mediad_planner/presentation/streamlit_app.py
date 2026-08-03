"""Casca mínima da reconstrução limpa do MediAd Planner."""

from pathlib import Path
from uuid import UUID

import streamlit as st

from mediad_planner.application.use_cases.obter_diagnostico_fundacao import (
    obter_diagnostico_fundacao,
)
from mediad_planner.composition.ambiente import (
    AmbienteAplicacao,
    construir_ambiente_aplicacao_em_memoria,
)
from mediad_planner.presentation.briefings import apresentar_briefing
from mediad_planner.presentation.campanhas import apresentar_campanhas


RAIZ = Path(__file__).resolve().parents[2]
MARCA = RAIZ / "assets" / "Marca_nova.png"
FAVICON = RAIZ / "assets" / "favicon2.png"
CHAVE_CAMPANHA_ATIVA = "id_campanha_briefing_ativa"


@st.cache_resource
def _obter_ambiente() -> AmbienteAplicacao:
    return construir_ambiente_aplicacao_em_memoria()


def executar() -> None:
    """Inicializa somente a fundação limpa, sem regras herdadas."""
    st.set_page_config(
        page_title="MediAd Planner",
        page_icon=str(FAVICON) if FAVICON.exists() else "📊",
        layout="wide",
    )

    if MARCA.exists():
        st.image(MARCA, width=320)

    st.title("MediAd Planner")
    st.subheader("Reconstrução limpa do planejamento híbrido de mídia")
    ambiente = _obter_ambiente()
    id_ativo = st.session_state.get(CHAVE_CAMPANHA_ATIVA)
    if id_ativo is None:
        id_selecionado = apresentar_campanhas(ambiente.campanhas)
        if id_selecionado is not None:
            st.session_state[CHAVE_CAMPANHA_ATIVA] = str(id_selecionado)
            st.rerun()
    else:
        voltar = apresentar_briefing(ambiente.briefings, UUID(id_ativo))
        if voltar:
            st.session_state.pop(CHAVE_CAMPANHA_ATIVA, None)
            st.rerun()

    diagnostico = obter_diagnostico_fundacao()
    with st.expander("Estado da fundação"):
        backend, frontoffice = st.columns(2)
        estado_backend = (
            "Operacional" if diagnostico.backend_operacional else "Indisponível"
        )
        backend.metric("Backend", estado_backend)
        frontoffice.metric("Frontoffice", "Conectado")
        if diagnostico.backend_operacional:
            st.success(diagnostico.mensagem)
            st.info(
                "O backend possui contratos funcionais e o frontoffice está "
                "conectado à aplicação. As capacidades de planejamento serão "
                "implementadas incrementalmente."
            )
        else:
            st.error(diagnostico.mensagem)
            for erro in diagnostico.erros:
                st.error(erro)
        st.divider()
        st.markdown("#### Detalhes técnicos")
        st.write(f"Versão do contrato: {diagnostico.versao_contrato}")
        st.write("Motores previstos:")
        for motor in diagnostico.motores_previstos:
            st.write(f"- {motor}")
