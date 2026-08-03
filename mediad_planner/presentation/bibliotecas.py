import streamlit as st


def apresentar_bibliotecas() -> None:
    st.header("Bibliotecas configuráveis")
    st.write(
        "As bibliotecas armazenarão referências reutilizáveis e versionadas "
        "para as Campanhas e os motores."
    )
    with st.container(border=True):
        st.subheader("Catálogo territorial oficial")
        st.write("Fonte: IBGE — Divisão Territorial Brasileira 2025")
        st.write("Base: snapshot local versionado da DTB 2025")
        st.write("Cobertura atual: Unidades da Federação, Regiões Geográficas "
            "Intermediárias, Regiões Geográficas Imediatas e Municípios")
        st.write("Atualização: controlada por nova edição oficial")
        st.write("Fallback: preenchimento manual")
    for rotulo in (
        "Inventários de mídia",
        "Catálogos mestres",
        "Parâmetros e curvas",
        "Cenários de referência",
    ):
        with st.container(border=True):
            st.subheader(rotulo)
            st.caption("Implementação futura")
