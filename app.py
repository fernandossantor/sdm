import streamlit as st

from application.services.workflow_service import (
    WorkflowService
)

from components.home.hero import render as hero
from components.home.workflow_card import render as workflow_card
from components.home.campaign_card import render as campaign_card
from components.home.knowledge_card import render as knowledge_card
from components.home.navigation_card import render as navigation_card

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="SDM",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================================
# WORKFLOW
# ==========================================================

workflow = WorkflowService()

estado = workflow.estado(

    st.session_state

)

# ==========================================================
# HOME
# ==========================================================

hero()

workflow_card(

    estado

)

st.divider()

campaign_card()

st.divider()

navigation_card()

st.divider()

knowledge_card()