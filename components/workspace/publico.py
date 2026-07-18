import streamlit as st

from application.session import Session

from application.services.audience_service import AudienceService

service = AudienceService()


def render():

    st.header("🎯 Público")

    campaign = Session.current_campaign()

    audience = service.load(campaign)

    if audience is None:
        audience = {}

    values = dict(audience)

    with st.form("audience"):

        st.subheader("Perfil")

        values["target_name"] = st.text_input(
            "Nome do Público",
            values.get("target_name", "")
        )

        values["gender"] = st.selectbox(
            "Gênero",

            [

                "",

                "Masculino",

                "Feminino",

                "Todos"

            ],

            index=0
        )

        c1, c2 = st.columns(2)

        values["age_min"] = c1.number_input(
            "Idade mínima",
            0,
            120,
            int(values.get("age_min",18))
        )

        values["age_max"] = c2.number_input(
            "Idade máxima",
            0,
            120,
            int(values.get("age_max",65))
        )

        st.subheader("Socioeconômico")

        values["social_class"] = st.text_input(
            "Classe Social",
            values.get("social_class","")
        )

        values["income"] = st.text_input(
            "Faixa de renda",
            values.get("income","")
        )

        values["education"] = st.text_input(
            "Escolaridade",
            values.get("education","")
        )

        values["occupation"] = st.text_input(
            "Profissão",
            values.get("occupation","")
        )

        st.subheader("Geografia")

        values["city"] = st.text_input(
            "Cidade",
            values.get("city","")
        )

        values["state"] = st.text_input(
            "Estado",
            values.get("state","")
        )

        values["region"] = st.text_input(
            "Região",
            values.get("region","")
        )

        st.subheader("Comportamento")

        values["interests"] = st.text_area(
            "Interesses",
            values.get("interests","")
        )

        values["habits"] = st.text_area(
            "Hábitos",
            values.get("habits","")
        )

        values["pain_points"] = st.text_area(
            "Dores",
            values.get("pain_points","")
        )

        values["media_consumption"] = st.text_area(
            "Consumo de mídia",
            values.get(
                "media_consumption",
                ""
            )
        )

        values["devices"] = st.text_area(
            "Dispositivos",
            values.get(
                "devices",
                ""
            )
        )

        values["observations"] = st.text_area(
            "Observações",
            values.get(
                "observations",
                ""
            )
        )

        salvar = st.form_submit_button(
            "Salvar Público",
            use_container_width=True
        )

    if salvar:

        values["campaign_id"] = campaign

        service.save(**values)

        st.success(
            "Público salvo."
        )

        st.rerun()