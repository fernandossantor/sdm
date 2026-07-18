import streamlit as st

from application.session import Session

from application.services.briefing_service import BriefingService

from components.workspace.briefing_sections import (
    company_section,
    positioning_section,
    communication_section,
    audience_section,
    investment_section,
)

service = BriefingService()


def render():

    st.header("📝 Briefing")

    campaign_id = Session.current_campaign()

    briefing = service.load(
        campaign_id
    )

    if briefing is None:
        briefing = {}

    values = dict(briefing)

    with st.form("briefing"):

        company_section(values)

        positioning_section(values)

        communication_section(values)

        audience_section(values)

        investment_section(values)

        salvar = st.form_submit_button(
            "💾 Salvar Briefing",
            use_container_width=True
        )

    if salvar:

        values["campaign_id"] = campaign_id

        service.save(**values)

        st.success(
            "Briefing salvo com sucesso."
        )

        st.rerun()