import streamlit as st

from mediad_planner.application.dto.diagnostico_fundacao import (
    DiagnosticoFundacao,
)


def apresentar_administracao(diagnostico: DiagnosticoFundacao) -> None:
    st.header("Administração")
    st.write(
        "As funções administrativas serão habilitadas com autenticação e "
        "persistência."
    )
    for rotulo in (
        "Espaço de trabalho",
        "Usuários e equipe",
        "Papéis e permissões",
        "Configurações",
    ):
        with st.container(border=True):
            st.subheader(rotulo)
            st.caption("Implementação futura")

    st.subheader("Diagnóstico do sistema")
    with st.expander("Detalhes técnicos do sistema", expanded=False):
        backend, frontoffice = st.columns(2)
        estado_backend = (
            "Operacional" if diagnostico.backend_operacional else "Indisponível"
        )
        backend.metric("Backend", estado_backend)
        frontoffice.metric("Frontoffice", "Conectado")
        if diagnostico.backend_operacional:
            st.success(diagnostico.mensagem)
        else:
            st.error(diagnostico.mensagem)
            for erro in diagnostico.erros:
                st.error(erro)
        st.write(f"Versão do contrato: {diagnostico.versao_contrato}")
        st.write("Motores previstos:")
        for motor in diagnostico.motores_previstos:
            st.write(f"- {motor}")
