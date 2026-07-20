import streamlit as st

from components.workspace.ui_state import show_saved_state

from application.session import Session

from application.services.campaign_objective_service import CampaignObjectiveService

service = CampaignObjectiveService()


BUSINESS = [

    "",

    "Aumentar vendas",

    "Gerar leads",

    "Lançar produto",

    "Reposicionar marca",

    "Fortalecer marca",

    "Fidelizar clientes"

]

COMMUNICATION = [

    "",

    "Reconhecimento",

    "Consideração",

    "Conversão",

    "Engajamento",

    "Retenção"

]

MEDIA = [

    "",

    "Alcance",

    "Frequência",

    "Cobertura",

    "Tráfego",

    "Conversões",

    "Visualizações"

]

KPIS = [

    "",

    "Reach",

    "Impressions",

    "Frequency",

    "CTR",

    "CPM",

    "CPC",

    "CPA",

    "ROAS",

    "Conversões"

]


def render():

    st.header("🎯 Objetivos")

    campaign = Session.current_campaign()

    values = service.load(campaign)

    if values is None:

        values = {}

    values = dict(values)

    show_saved_state("Objetivos", values)

    with st.form("campaign_objectives"):

        st.subheader("Objetivos")

        values["business_objective"] = st.selectbox(

            "Objetivo de negócio",

            BUSINESS,

            index=0

        )

        values["communication_objective"] = st.selectbox(

            "Objetivo de comunicação",

            COMMUNICATION,

            index=0

        )

        values["media_objective"] = st.selectbox(

            "Objetivo de mídia",

            MEDIA,

            index=0

        )

        st.divider()

        st.subheader("KPIs")

        values["primary_kpi"] = st.selectbox(

            "KPI principal",

            KPIS,

            index=0

        )

        values["secondary_kpis"] = st.text_input(

            "KPIs secundários",

            values.get("secondary_kpis","")

        )

        st.divider()

        st.subheader("Metas")

        c1,c2,c3 = st.columns(3)

        values["desired_reach"] = c1.number_input(

            "Reach (%)",

            value=float(values.get("desired_reach",0))

        )

        values["desired_frequency"] = c2.number_input(

            "Frequência",

            value=float(values.get("desired_frequency",0))

        )

        values["desired_impressions"] = c3.number_input(

            "Impressões",

            value=int(values.get("desired_impressions",0))

        )

        c1,c2,c3 = st.columns(3)

        values["desired_clicks"] = c1.number_input(

            "Cliques",

            value=int(values.get("desired_clicks",0))

        )

        values["desired_ctr"] = c2.number_input(

            "CTR",

            value=float(values.get("desired_ctr",0))

        )

        values["desired_cpm"] = c3.number_input(

            "CPM",

            value=float(values.get("desired_cpm",0))

        )

        c1,c2,c3 = st.columns(3)

        values["desired_cpc"] = c1.number_input(

            "CPC",

            value=float(values.get("desired_cpc",0))

        )

        values["desired_cpa"] = c2.number_input(

            "CPA",

            value=float(values.get("desired_cpa",0))

        )

        values["desired_roas"] = c3.number_input(

            "ROAS",

            value=float(values.get("desired_roas",0))

        )

        values["observations"] = st.text_area(

            "Observações",

            values.get("observations","")

        )

        salvar = st.form_submit_button(

            "Salvar Objetivos",

            use_container_width=True

        )

    if salvar:

        values["campaign_id"] = campaign

        service.save(**values)

        st.success("Objetivos salvos.")

        st.rerun()