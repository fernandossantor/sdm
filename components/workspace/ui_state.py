import streamlit as st


def show_saved_state(label, values):
    """Mostra estado de preenchimento/salvamento de uma seção do workspace."""

    if values:
        st.success(
            f"{label} já possui dados salvos para esta campanha. "
            "Você pode revisar, editar e salvar novamente."
        )
    else:
        st.info(
            f"{label} ainda não possui dados salvos para esta campanha."
        )


def show_workspace_notice():
    """Mostra aviso padrão sobre módulos ainda não liberados."""

    with st.expander("Módulos em breve", expanded=False):
        st.caption(
            "Planejamento, Inventários, Forecast, Cronograma, KPIs e Relatórios "
            "serão integrados ao workspace em uma próxima etapa. "
            "Por enquanto, o workspace exibe apenas os módulos com persistência ativa."
        )
