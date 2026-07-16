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

            use_container_width=True

        )

        st.page_link(

            "pages/05_Planejamento.py",

            label="🧠 Planejamento",

            use_container_width=True

        )

        st.page_link(

            "pages/06_Forecast.py",

            label="📈 Forecast",

            use_container_width=True

        )

    with col2:

        st.page_link(

            "pages/07_Dashboard.py",

            label="📊 Dashboard",

            use_container_width=True

        )

        st.page_link(

            "pages/08_Exportacao.py",

            label="📄 Exportação",

            use_container_width=True

        )

        st.page_link(

            "pages/13_Insights.py",

            label="💡 Insights",

            use_container_width=True

        )