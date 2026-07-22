import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina

from application.services.planejamento_service import PlanejamentoService
from components.formatters import numero_ptbr, percentual_ptbr
from components.planning_selector import selecionar_planejamento
from components.schedule_visual import render as render_schedule
from components.workflow_guard import exigir


st.set_page_config(
    page_title=titulo_pagina("Cronograma de Inserções"),
    page_icon=PAGE_ICON,
    layout="wide",
)
exigir("diagnostico")
st.title("🗓️ Cronograma de Inserções")
st.write(
    "Visualize a distribuição semanal das quantidades planejadas "
    "para cada inventário."
)

service = PlanejamentoService()
origem = selecionar_planejamento(service, key="cronograma_origem")
plano = origem["plano"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Flight", plano.tipo_flight.title())
c2.metric("Frequência média", numero_ptbr(plano.frequencia_alvo, 2))
c3.metric("Alcance (%)", percentual_ptbr(plano.alcance_percentual))
c4.metric("GRP", numero_ptbr(plano.grp, 2))

render_schedule(plano)
