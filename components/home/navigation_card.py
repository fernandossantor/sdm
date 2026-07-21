import streamlit as st


def render():

    st.subheader(

        "🚀 Ações"

    )

    col1, col2 = st.columns(2)

    with col1:

        st.page_link(

            "pages/00_Briefing.py",

            label="📋 Novo Briefing",

            width="stretch"

        )

        st.page_link(

            "pages/05_Planejamento.py",

            label="🧠 Planejamento",

            width="stretch"

        )

        st.page_link(

            "pages/06_Forecast.py",

            label="📈 Forecast",

            width="stretch"

        )

    with col2:

        st.page_link(

            "pages/07_Dashboard.py",

            label="📊 Dashboard",

            width="stretch"

        )

        st.page_link(

            "pages/08_Exportacao.py",

            label="📄 Exportação",

            width="stretch"

        )

        st.page_link(

            "pages/13_Insights.py",

            label="💡 Insights",

            width="stretch"

        )