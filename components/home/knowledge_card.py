import streamlit as st


def render():

    st.subheader(

        "Abrir Base de Conhecimento"

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Inventários",

        "-"

    )

    c2.metric(

        "Objetivos",

        "-"

    )

    c3.metric(

        "KPIs",

        "-"

    )

    c4.metric(

        "Audiências",

        "-"
    )