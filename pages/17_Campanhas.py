import streamlit as st

from application.session import Session

from components.campaign.campaign_form import render as campaign_form
from components.campaign.campaign_table import render as campaign_table
from components.campaign.campaign_workspace import render as workspace

from components.workspace.dashboard import render as dashboard
from components.workspace.briefing import render as briefing
from components.workspace.publico import render as publico
from components.workspace.objetivos import render as objetivos
from components.workspace.planejamento import render as planejamento
from components.workspace.inventarios import render as inventarios
from components.workspace.forecast import render as forecast
from components.workspace.cronograma import render as cronograma
from components.workspace.kpis import render as kpis
from components.workspace.relatorios import render as relatorios
from components.workspace.estrategia import render as estrategia

st.set_page_config(
    page_title="Campanhas",
    layout="wide"
)

Session.initialize()

workspace()

st.title("📁 Campanhas")

if not Session.has_campaign():

    tab1, tab2 = st.tabs(

        [

            "Nova campanha",

            "Campanhas"

        ]

    )

    with tab1:

        campaign_form()

    with tab2:

        campaign_table()

else:

    module = st.session_state.get(

        "workspace_module",

        "dashboard"

    )

    if module == "dashboard":
        dashboard()

    elif module == "briefing":
        briefing()

    elif module == "publico":
        publico()

    elif module == "objetivos":
        objetivos()

    elif module == "estrategia":
        estrategia()

    elif module == "planejamento":
        planejamento()
    
    elif module == "inventarios":
        inventarios()

    elif module == "forecast":
        forecast()

    elif module == "cronograma":
        cronograma()

    elif module == "kpis":
        kpis()

    elif module == "relatorios":
        relatorios()