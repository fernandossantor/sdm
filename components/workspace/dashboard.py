import streamlit as st

from application.session import Session

from application.services.briefing_service import BriefingService

from application.services.briefing_validator import BriefingValidator


def render():

    st.header("Dashboard")

    campaign = Session.current_campaign()

    briefing = BriefingService().load(
        campaign
    )

    progress = BriefingValidator.progress(
        briefing
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Briefing",
        f"{progress}%"
    )

    c2.metric(
        "Planejamento",
        "0%"
    )

    c3.metric(
        "Forecast",
        "0%"
    )

    c4.metric(
        "KPIs",
        "0%"
    )

    st.progress(
        progress / 100
    )

    st.info(
        "O dashboard passará a refletir automaticamente a evolução da campanha."
    )