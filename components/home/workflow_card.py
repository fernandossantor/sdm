import streamlit as st


def render(

    estado

):

    st.subheader(

        "Workflow"

    )

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Etapas",

        f"{estado.concluidas}/{estado.total}"

    )

    c2.metric(

        "Progresso",

        f"{estado.percentual}%"

    )

    c3.metric(

        "Próxima",

        estado.proxima_etapa

    )

    st.progress(

        estado.percentual / 100

    )