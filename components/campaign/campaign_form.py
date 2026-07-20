import streamlit as st

from application.services.campaign_service import CampaignService

from application.session import Session

service = CampaignService()


def render():

    with st.form("campaign_form"):

        st.subheader("Nova campanha")

        name = st.text_input(
            "Nome da campanha *"
        )

        client = st.text_input(
            "Cliente"
        )

        brand = st.text_input(
            "Marca"
        )

        product = st.text_input(
            "Produto"
        )

        objective = st.selectbox(

            "Objetivo",

            [

                "Awareness",

                "Consideração",

                "Conversão",

                "Fidelização"

            ]

        )

        c1, c2 = st.columns(2)

        with c1:

            start_date = st.date_input(
                "Data inicial"
            )

        with c2:

            end_date = st.date_input(
                "Data final"
            )

        notes = st.text_area(
            "Observações"
        )

        submitted = st.form_submit_button(
            "Criar campanha"
        )

        if submitted:

            if not name:

                st.error(
                    "Informe o nome da campanha."
                )

                return

            campaign = service.create(

                name=name,

                client=client,

                brand=brand,

                product=product,

                objective=objective,

                start_date=start_date,

                end_date=end_date,

                notes=notes

            )

            Session.set_current_campaign(
                campaign["id"]
            )

            st.success(
                "Campanha criada com sucesso."
            )

            st.rerun()