"""Casca mínima da reconstrução limpa do MediAd Planner."""

from pathlib import Path

import streamlit as st

from mediad_planner.application.use_cases.obter_diagnostico_fundacao import (
    obter_diagnostico_fundacao,
)


RAIZ = Path(__file__).resolve().parents[2]
MARCA = RAIZ / "assets" / "Marca_nova.png"
FAVICON = RAIZ / "assets" / "favicon2.png"


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
    diagnostico = obter_diagnostico_fundacao()
    st.header("Estado da fundação")
    backend, frontoffice = st.columns(2)
    estado_backend = (
        "Operacional" if diagnostico.backend_operacional else "Indisponível"
    )
    backend.metric("Backend", estado_backend)
    frontoffice.metric("Frontoffice", "Conectado")
    if diagnostico.backend_operacional:
        st.success(diagnostico.mensagem)
        st.info(
            "O backend possui contratos funcionais e o frontoffice está conectado "
            "à aplicação. As capacidades de planejamento serão implementadas "
            "incrementalmente."
        )
    else:
        st.error(diagnostico.mensagem)
        for erro in diagnostico.erros:
            st.error(erro)
    with st.expander("Detalhes técnicos"):
        st.write(f"Versão do contrato: {diagnostico.versao_contrato}")
        st.write("Motores previstos:")
        for motor in diagnostico.motores_previstos:
            st.write(f"- {motor}")
