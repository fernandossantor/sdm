import streamlit as st

from application.services.workflow_service import (
    WorkflowService
)

from components.home.hero import render as hero
from components.home.workflow_card import render as workflow_card
from components.home.projects_card import render as projects_card
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

projects_card()

st.divider()

navigation_card()

st.divider()

knowledge_card()