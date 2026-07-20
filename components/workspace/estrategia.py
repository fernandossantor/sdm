import streamlit as st

from components.workspace.ui_state import show_saved_state

from application.session import Session
from application.services.media_strategy_service import MediaStrategyService

service = MediaStrategyService()

STRATEGIES = [
    "",
    "Always On",
    "Flighting",
    "Pulsing",
    "Sazonal",
    "Lançamento"
]

PURCHASE = [
    "",
    "Programática",
    "Direta",
    "Híbrida"
]

CAMPAIGN = [
    "",
    "Branding",
    "Performance",
    "Brandformance"
]

SCOPE = [
    "",
    "Local",
    "Regional",
    "Nacional",
    "Internacional"
]

PHASE = [
    "",
    "Awareness",
    "Consideração",
    "Conversão",
    "Retenção"
]

PRIORITY = [
    "",
    "Alcance",
    "Frequência",
    "Eficiência",
    "Conversão",
    "ROI"
]


def render():

    st.header("🧭 Estratégia de Mídia")

    campaign = Session.current_campaign()

    values = service.load(campaign)

    if values is None:
        values = {}

    values = dict(values)

    show_saved_state("Estratégia", values)

    with st.form("media_strategy"):

        values["strategy_type"] = st.selectbox(
            "Estratégia",
            STRATEGIES,
            index=STRATEGIES.index(values.get("strategy_type", ""))
            if values.get("strategy_type", "") in STRATEGIES else 0
        )

        values["purchase_model"] = st.selectbox(
            "Modelo de Compra",
            PURCHASE,
            index=PURCHASE.index(values.get("purchase_model", ""))
            if values.get("purchase_model", "") in PURCHASE else 0
        )

        values["campaign_type"] = st.selectbox(
            "Tipo de Campanha",
            CAMPAIGN,
            index=CAMPAIGN.index(values.get("campaign_type", ""))
            if values.get("campaign_type", "") in CAMPAIGN else 0
        )

        values["coverage_scope"] = st.selectbox(
            "Abrangência",
            SCOPE,
            index=SCOPE.index(values.get("coverage_scope", ""))
            if values.get("coverage_scope", "") in SCOPE else 0
        )

        values["communication_phase"] = st.selectbox(
            "Fase da Comunicação",
            PHASE,
            index=PHASE.index(values.get("communication_phase", ""))
            if values.get("communication_phase", "") in PHASE else 0
        )

        values["priority"] = st.selectbox(
            "Prioridade",
            PRIORITY,
            index=PRIORITY.index(values.get("priority", ""))
            if values.get("priority", "") in PRIORITY else 0
        )

        values["budget_distribution"] = st.text_area(
            "Estratégia de Distribuição de Verba",
            values.get("budget_distribution", "")
        )

        values["channel_mix"] = st.text_area(
            "Mix Inicial de Canais",
            values.get("channel_mix", "")
        )

        values["observations"] = st.text_area(
            "Observações",
            values.get("observations", "")
        )

        salvar = st.form_submit_button(
            "Salvar Estratégia",
            use_container_width=True
        )

    if salvar:

        values["campaign_id"] = campaign

        service.save(**values)

        st.success("Estratégia salva.")

        st.rerun()