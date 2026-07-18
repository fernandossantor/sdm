import streamlit as st

from components.crud.form import render as form

from components.crud.table import render as table


def render(

    metadata,

    service

):

    st.title(metadata.title)

    tab1, tab2 = st.tabs(

        [

            "Novo",

            "Registros"

        ]

    )

    with tab1:

        salvar, values = form(metadata)

        if salvar:

            service.save(**values)

            st.success("Registro salvo.")

            st.rerun()

    with tab2:

        table(

            metadata,

            service.list()

        )