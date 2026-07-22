import streamlit as st
from components.page_config import PAGE_ICON
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
from components.planning_selector import selecionar_planejamento
from components.formatters import moeda_ptbr, numero_ptbr


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Comparação de Planos",

    page_icon=PAGE_ICON,

    layout="wide"

)

st.title("⚖️ Comparação de Planos")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

comparador = ComparadorService()

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
    ("jornada", "Jornada", 15), ("saturacao", "Baixa saturação", 10),
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
