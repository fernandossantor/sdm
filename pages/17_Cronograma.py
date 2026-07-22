import streamlit as st

from application.services.planejamento_service import PlanejamentoService
from components.formatters import numero_ptbr
from components.planning_selector import selecionar_planejamento
from components.schedule_editor import render as render_schedule
from components.workflow_guard import exigir


st.set_page_config(
    page_title="Cronograma de Inserções",
    page_icon="🗓️",
    layout="wide",
)
exigir("diagnostico")
st.title("🗓️ Cronograma de Inserções")
st.write(
    "Visualize e configure a distribuição semanal das quantidades planejadas "
    "para cada inventário."
)

service = PlanejamentoService()
origem = selecionar_planejamento(service, key="cronograma_origem")
plano = origem["plano"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Flight", plano.tipo_flight.title())
c2.metric("Frequência média", numero_ptbr(plano.frequencia_alvo, 2))
c3.metric("Alcance", f"{numero_ptbr(plano.alcance_percentual, 2)}%")
c4.metric("GRP", numero_ptbr(plano.grp, 2))

if render_schedule(plano, f"cronograma_pagina_{origem['id'] or 'sessao'}"):
    if origem["id"]:
        service.atualizar_cronograma(origem["id"], plano.cronograma)
        st.success("Cronograma atualizado no Plano de Mídia salvo.")
    else:
        st.session_state["plano"] = plano
        st.success(
            "Cronograma atualizado na sessão. Salve o plano em Plano de Mídia "
            "para manter a alteração."
        )
