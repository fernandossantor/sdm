import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina
import pandas as pd

from application.services.comparador_service import (
    ComparadorService
)

from application.services.forecast_service import (
    ForecastService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.context_service import (
    ContextService
)
from application.services.version_comparison_service import (
    VersionComparisonService
)
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos
from components.planning_selector import selecionar_planejamento
from components.formatters import moeda_ptbr, numero_ptbr


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Comparação de Planos"),

    page_icon=PAGE_ICON,

    layout="wide"

)

st.title("⚖️ Comparação de Planos")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

comparador = ComparadorService()
comparador_versoes = VersionComparisonService()
artefatos = WorkflowArtifactService()
gerenciar_artefatos(artefatos, "COMPARACAO", "Comparações salvas")

with st.expander("Comparar versões do mesmo planejamento", expanded=False):
    salvos = planejamento.listar()
    if not salvos:
        st.info("Salve um planejamento para consultar seu histórico.")
    else:
        registro_historico = st.selectbox(
            "Planejamento com histórico",
            salvos,
            format_func=lambda item: (
                f"{item.get('codigo') or item['id'][:8]} · {item['nome']}"
            ),
            key="historico_planejamento",
        )
        try:
            versoes = planejamento.versoes(registro_historico["id"])
        except Exception as erro:
            st.error(f"Não foi possível carregar as versões: {erro}")
            versoes = []
        if len(versoes) < 2:
            st.info("Este planejamento ainda não possui duas versões.")
        else:
            v1, v2 = st.columns(2)
            versao_anterior = v1.selectbox(
                "Versão anterior",
                versoes,
                index=len(versoes) - 1,
                format_func=lambda item: (
                    f"v{item['numero']} · {item['evento']} · "
                    f"{item['criado_em']}"
                ),
                key="versao_historica_anterior",
            )
            versao_atual = v2.selectbox(
                "Versão atual",
                versoes,
                index=0,
                format_func=lambda item: (
                    f"v{item['numero']} · {item['evento']} · "
                    f"{item['criado_em']}"
                ),
                key="versao_historica_atual",
            )
            if st.button("Comparar histórico", type="primary"):
                if versao_anterior["numero"] == versao_atual["numero"]:
                    st.error("Selecione versões diferentes.")
                else:
                    st.session_state["comparacao_historica"] = (
                        comparador_versoes.comparar(
                            planejamento.restaurar_versao(versao_anterior),
                            planejamento.restaurar_versao(versao_atual),
                            {
                                "planejamento_id": registro_historico["id"],
                                "versao_anterior": versao_anterior["numero"],
                                "versao_atual": versao_atual["numero"],
                                "hash_anterior": versao_anterior["hash_conteudo"],
                                "hash_atual": versao_atual["hash_conteudo"],
                            },
                        )
                    )

if "comparacao_historica" in st.session_state:
    historico = st.session_state["comparacao_historica"]
    st.subheader("Mudanças entre versões")
    st.caption(historico["natureza"])
    st.dataframe(
        pd.DataFrame(historico["metricas"]),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        pd.DataFrame(historico["itens"]),
        hide_index=True,
        width="stretch",
    )
    if st.button("Salvar comparação histórica"):
        artefatos.salvar_no_projeto(
            "COMPARACAO",
            (
                "Comparação histórica — "
                f"v{historico['metadados']['versao_anterior']} × "
                f"v{historico['metadados']['versao_atual']}"
            ),
            historico,
            st.session_state,
            historico["metadados"]["planejamento_id"],
        )
        st.success("Comparação histórica salva no projeto.")

col1, col2 = st.columns(2)

with col1:

    origem1 = selecionar_planejamento(planejamento, "plano_a")

with col2:

    origem2 = selecionar_planejamento(planejamento, "plano_b")

st.subheader("Critérios da decisão")
st.caption("Defina o que significa 'melhor' para esta comparação. Os pesos devem somar 100%.")
colunas = st.columns(7)
rotulos = [
    ("alcance", "Alcance", 25), ("frequencia", "Frequência", 20),
    ("conversoes", "Conversões", 15), ("roi", "ROI", 10),
    ("jornada", "Jornada", 15),
    ("sobre_exposicao", "Baixa sobre-exposição", 10),
    ("investimento", "Menor custo", 5),
]
pesos = {
    chave: coluna.number_input(
        f"{rotulo} (%)", 0.0, 100.0, float(padrao), step=0.01,
        format="%.2f", key=f"peso_comp_{chave}"
    )
    for coluna, (chave, rotulo, padrao) in zip(colunas, rotulos)
}
soma = sum(pesos.values())
if soma != 100:
    st.error(f"Os pesos somam {numero_ptbr(soma, 2)}%; ajuste para 100,00%.")

if st.button(

    "Comparar",

    type="primary",

    width="stretch",
    disabled=soma != 100,

):

    plano1 = origem1["plano"]
    plano2 = origem2["plano"]

    try:
        resultado = comparador.comparar_configuravel(plano1, plano2, pesos)
    except ValueError as erro:
        st.error(str(erro))
        resultado = None

    if resultado:
        st.session_state["resultado_comparacao"] = resultado


# ==========================================================
# RESULTADOS
# ==========================================================

if "resultado_comparacao" in st.session_state:

    r = st.session_state["resultado_comparacao"]

    st.success(

        f"Estratégia mais aderente: {r['vencedor']}"

    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Score Plano A",

            numero_ptbr(r["scores"][0], 2)

        )

    with c2:

        st.metric(

            "Score Plano B",

            numero_ptbr(r["scores"][1], 2)

        )


    st.dataframe(pd.DataFrame(r["detalhes"]), hide_index=True, width="stretch")

    st.divider()

    st.subheader(

        "Justificativa"

    )

    st.info(

        r["justificativa"]

    )
