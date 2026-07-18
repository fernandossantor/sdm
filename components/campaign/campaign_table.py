import streamlit as st

from application.services.campaign_service import CampaignService

from application.session import Session

service = CampaignService()


def render():

    campaigns = service.list()

    if not campaigns:

        st.info("Nenhuma campanha cadastrada.")

        return

    st.subheader("Campanhas")

    if Session.has_campaign():
        st.success(
            f"Campanha ativa: {Session.current_campaign()}"
        )

    header = st.columns([2.2, 1.2, 1.2, 1.2, 1.4, 0.8, 0.8])

    header[0].markdown("**Campanha**")
    header[1].markdown("**Cliente**")
    header[2].markdown("**Marca**")
    header[3].markdown("**Status**")
    header[4].markdown("**Código**")
    header[5].markdown("**Abrir**")
    header[6].markdown("**Excluir**")

    st.divider()

    for campaign in campaigns:

        cols = st.columns([2.2, 1.2, 1.2, 1.2, 1.4, 0.8, 0.8])

        cols[0].write(campaign["name"])
        cols[1].write(campaign["client"])
        cols[2].write(campaign["brand"])
        cols[3].write(campaign["status"])
        cols[4].write(campaign["code"])

        if cols[5].button(
            "Abrir",
            key=f"open_{campaign['id']}"
        ):

            Session.set_current_campaign(
                campaign["id"]
            )

            st.success("Campanha selecionada.")

            st.rerun()

        if cols[6].button(
            "🗑",
            key=f"delete_{campaign['id']}"
        ):

            service.delete(
                campaign["id"]
            )

            st.rerun()