import streamlit as st


def apresentar_bibliotecas() -> None:
    st.header("Bibliotecas configuráveis")
    st.write(
        "As bibliotecas armazenarão referências reutilizáveis e versionadas "
        "para as Campanhas e os motores."
    )
    for rotulo in (
        "Inventários de mídia",
        "Catálogos mestres",
        "Parâmetros e curvas",
        "Cenários de referência",
    ):
        with st.container(border=True):
            st.subheader(rotulo)
            st.caption("Implementação futura")
