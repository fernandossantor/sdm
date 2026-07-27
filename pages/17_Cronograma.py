import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina

from application.services.planejamento_service import PlanejamentoService
from application.services.schedule_service import ScheduleService
from components.formatters import moeda_ptbr, numero_ptbr, percentual_ptbr
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

mapas = ScheduleService().consolidar(plano)
reconciliacao = mapas["reconciliacao"]
st.divider()
st.subheader("Reconciliação")
r1, r2 = st.columns(2)
r1.metric(
    "Quantidade plano × cronograma",
    (
        f"{numero_ptbr(reconciliacao['quantidade_plano'])} × "
        f"{numero_ptbr(reconciliacao['quantidade_cronograma'])}"
    ),
)
r2.metric(
    "Investimento plano × cronograma",
    (
        f"{moeda_ptbr(reconciliacao['investimento_plano'])} × "
        f"{moeda_ptbr(reconciliacao['investimento_cronograma'])}"
    ),
)
if (
    reconciliacao["quantidade_reconciliada"]
    and reconciliacao["investimento_reconciliado"]
):
    st.success("Quantidades e investimento reconciliam com o plano.")
else:
    st.error("O cronograma diverge do plano e deve ser revisado.")

st.subheader("Resumo semanal")
st.dataframe(mapas["semanal"], hide_index=True, width="stretch")
st.subheader("Resumo mensal")
st.dataframe(mapas["mensal"], hide_index=True, width="stretch")
st.subheader("Mapa por meio")
st.dataframe(mapas["por_meio"], hide_index=True, width="stretch")
