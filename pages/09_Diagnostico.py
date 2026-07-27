from datetime import date

import pandas as pd
import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina
from components.formatters import dataframe_ptbr, numero_ptbr

from application.services.diagnostico_service import (
    DiagnosticoService
)

from application.services.planejamento_service import (
    PlanejamentoService
)
from application.services.forecast_service import ForecastService
from application.services.context_service import ContextService
from domain.models.realizado import RealizadoItem, RealizadoPlano

from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir
from components.planning_selector import selecionar_planejamento
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Diagnóstico do Plano"),

    page_icon=PAGE_ICON,

    layout="wide"

)

exigir("diagnostico")

st.title("🩺 Diagnóstico do Plano")

st.divider()

planejamento = PlanejamentoService()

diagnostico_service = DiagnosticoService()

workflow_service = WorkflowService()
artefatos = WorkflowArtifactService()

origem = selecionar_planejamento(planejamento, "diagnostico_planejamento")
gerenciar_artefatos(artefatos, "DIAGNOSTICO", "Diagnósticos")

plano_selecionado = origem["plano"]
with st.expander("Informar realizado e comparar desempenho", expanded=False):
    st.caption(
        "O realizado não altera o plano. Período e contexto precisam coincidir "
        "para que os desvios sejam calculados."
    )
    r1, r2, r3 = st.columns(3)
    fonte_realizado = r1.text_input(
        "Fonte do realizado",
        key="fonte_realizado_diagnostico",
    )
    inicio_realizado = r2.date_input(
        "Início realizado",
        value=plano_selecionado.inicio or date.today(),
        key="inicio_realizado_diagnostico",
    )
    fim_realizado = r3.date_input(
        "Fim realizado",
        value=plano_selecionado.fim or date.today(),
        key="fim_realizado_diagnostico",
    )
    primeira_premissa = (
        plano_selecionado.itens[0].premissas
        if plano_selecionado.itens else {}
    )
    c1, c2, c3 = st.columns(3)
    universo_realizado = c1.text_input(
        "Universo",
        value=str(primeira_premissa.get("universo") or ""),
        key="universo_realizado_diagnostico",
    )
    publico_realizado = c2.text_input(
        "Público-alvo",
        value=str(primeira_premissa.get("publico_alvo") or ""),
        key="publico_realizado_diagnostico",
    )
    praca_realizada = c3.text_input(
        "Praça",
        value=str(primeira_premissa.get("praca") or ""),
        key="praca_realizada_diagnostico",
    )
    itens_realizados = []
    for item in plano_selecionado.itens:
        st.markdown(f"**{item.inventario}**")
        colunas = st.columns(4)
        valores = {}
        for campo, rotulo, coluna in zip(
            ("investimento", "impressoes", "cliques", "conversoes"),
            ("Investimento", "Impressões", "Cliques", "Conversões"),
            colunas,
        ):
            valores[campo] = coluna.number_input(
                rotulo,
                min_value=0.0,
                value=None,
                key=f"realizado_{campo}_{item.inventario_id or item.inventario}",
                placeholder="Não informado",
            )
        itens_realizados.append(RealizadoItem(
            inventario=item.inventario,
            inventario_id=item.inventario_id,
            **valores,
        ))
    if st.button("Comparar realizado", type="primary"):
        realizado = RealizadoPlano(
            fonte=fonte_realizado,
            inicio=inicio_realizado,
            fim=fim_realizado,
            itens=itens_realizados,
            universo=universo_realizado or None,
            publico_alvo=publico_realizado or None,
            praca=praca_realizada or None,
        )
        forecast = ForecastService().gerar(
            plano_selecionado,
            ContextService().metricas(),
        )
        st.session_state["diagnostico_desempenho"] = (
            diagnostico_service.comparar_desempenho(
                plano_selecionado,
                forecast,
                realizado,
            )
        )

if st.button(

    "Gerar Diagnóstico",

    type="primary",

    width="stretch"

):

    plano = origem["plano"]

    diagnostico = diagnostico_service.gerar(

        plano

    )

    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "diagnostico", diagnostico)

if "diagnostico_desempenho" in st.session_state:
    desempenho = st.session_state["diagnostico_desempenho"]
    st.subheader("Planejado × forecast × realizado")
    if desempenho["situacao_comparabilidade"] == "COMPARAVEL":
        st.success("Período e contexto comparáveis.")
    else:
        st.warning(
            f"{desempenho['situacao_comparabilidade']}: "
            f"{desempenho['motivo']}"
        )
    st.dataframe(
        dataframe_ptbr(
            pd.DataFrame(desempenho["linhas"]),
            percentuais=[
                "desvio_planejado_percentual",
                "desvio_forecast_percentual",
            ],
            decimais=["planejado", "forecast", "realizado"],
        ),
        hide_index=True,
        width="stretch",
    )
    if st.button("Salvar comparação de desempenho"):
        artefatos.salvar_no_projeto(
            "DIAGNOSTICO",
            f"Desempenho realizado — {plano_selecionado.campanha}",
            desempenho,
            st.session_state,
            origem["id"],
        )
        st.success("Comparação de desempenho salva no projeto.")


# ==========================================================
# RESULTADO
# ==========================================================

if "diagnostico" in st.session_state:

    diagnostico = st.session_state["diagnostico"]

    with st.expander("Salvar diagnóstico", expanded=False):
        nome_diagnostico = st.text_input(
            "Nome do diagnóstico",
            value=f"Diagnóstico — {diagnostico.campanha}",
        )
        if st.button("Salvar diagnóstico", type="primary"):
            artefatos.salvar_no_projeto(
                "DIAGNOSTICO",
                nome_diagnostico,
                diagnostico,
                st.session_state,
                origem["id"],
            )
            st.success("Diagnóstico salvo.")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Score médio (%)",

        numero_ptbr(diagnostico.score_medio, 2)

    )

    c2.metric(

        "Principais",

        diagnostico.principais

    )

    c3.metric(

        "Complementares",

        diagnostico.complementares

    )

    c4.metric(

        "Recomendações",

        diagnostico.total_recomendacoes

    )

    st.divider()

    abas = st.tabs(

        [

            "Inventários",

            "Observações"

        ]

    )

    # ======================================================
    # INVENTÁRIOS
    # ======================================================

    with abas[0]:

        for item in diagnostico.itens:

            with st.expander(

                item.inventario,

                expanded=False

            ):

                a, b, c = st.columns(3)

                a.metric(

                    "Score (%)",

                    numero_ptbr(item.score, 2)

                )

                b.metric(

                    "Papel",

                    item.papel

                )

                c.metric(

                    "Ambiente",

                    item.ambiente

                )

                st.markdown(

                    "**Pontos Fortes**"

                )

                if item.pontos_fortes:

                    for texto in item.pontos_fortes:

                        st.success(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhum."

                    )

                st.markdown(

                    "**Pontos de Atenção**"

                )

                if item.pontos_fracos:

                    for texto in item.pontos_fracos:

                        st.warning(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhum."

                    )

                st.markdown(

                    "**Recomendações**"

                )

                if item.recomendacoes:

                    for texto in item.recomendacoes:

                        st.info(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhuma."

                    )

    # ======================================================
    # OBSERVAÇÕES
    # ======================================================

    with abas[1]:

        for obs in diagnostico.observacoes:

            st.info(

                obs

            )
