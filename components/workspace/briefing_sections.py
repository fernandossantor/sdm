import streamlit as st


def company_section(values):

    with st.expander(
        "🏢 Empresa e Produto",
        expanded=True
    ):

        values["company"] = st.text_input(
            "Empresa",
            values.get("company", "")
        )

        values["market"] = st.text_input(
            "Mercado",
            values.get("market", "")
        )

        values["product"] = st.text_input(
            "Produto",
            values.get("product", "")
        )

        values["category"] = st.text_input(
            "Categoria",
            values.get("category", "")
        )


def positioning_section(values):

    with st.expander(
        "🎯 Posicionamento",
        expanded=True
    ):

        values["positioning"] = st.text_area(
            "Posicionamento",
            values.get("positioning", "")
        )

        values["differential"] = st.text_area(
            "Diferencial",
            values.get("differential", "")
        )


def communication_section(values):

    with st.expander(
        "📢 Comunicação",
        expanded=True
    ):

        values["objectives"] = st.text_area(
            "Objetivos",
            values.get("objectives", "")
        )

        values["communication_problem"] = st.text_area(
            "Problema de Comunicação",
            values.get(
                "communication_problem",
                ""
            )
        )


def audience_section(values):

    with st.expander(
        "👥 Público",
        expanded=True
    ):

        values["target_audience"] = st.text_area(
            "Público-alvo",
            values.get(
                "target_audience",
                ""
            )
        )

        values["competitors"] = st.text_area(
            "Concorrentes",
            values.get(
                "competitors",
                ""
            )
        )


def investment_section(values):

    with st.expander(
        "💰 Investimento",
        expanded=True
    ):

        values["budget"] = st.number_input(
            "Orçamento",
            value=float(
                values.get(
                    "budget",
                    0
                )
            )
        )

        values["start_date"] = st.date_input(
            "Data inicial",
            value=values.get(
                "start_date"
            )
        )

        values["end_date"] = st.date_input(
            "Data final",
            value=values.get(
                "end_date"
            )
        )

        values["observations"] = st.text_area(
            "Observações",
            values.get(
                "observations",
                ""
            )
        )