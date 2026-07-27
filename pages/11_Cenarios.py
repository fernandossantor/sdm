import pandas as pd
import streamlit as st

from application.services.planejamento_service import PlanejamentoService
from application.services.scenario_service import ScenarioService
from components.formatters import dataframe_ptbr, moeda_ptbr, numero_ptbr
from components.page_config import PAGE_ICON, titulo_pagina
from components.planning_selector import selecionar_planejamento


st.set_page_config(
    page_title=titulo_pagina("Cenários e Sensibilidade"),
    page_icon=PAGE_ICON,
    layout="wide",
)

st.title("🎭 Cenários e Sensibilidade")
st.info(
    "Os cenários mantêm plano e investimento fixos e variam premissas de "
    "entrega e resposta. São hipóteses condicionais, não previsões probabilísticas."
)

origem = selecionar_planejamento(
    PlanejamentoService(),
    "cenarios_planejamento",
)
service = ScenarioService()

st.subheader("Premissas de variação")
st.caption(
    "Os valores iniciais são apenas pontos de partida editáveis; não representam "
    "benchmarks acadêmicos ou de mercado."
)

configuracoes = {}
padroes = {"CONSERVADOR": -10.0, "BASE": 0.0, "OTIMISTA": 10.0}
for nome, padrao in padroes.items():
    with st.expander(nome.title(), expanded=nome == "BASE"):
        col1, col2, col3 = st.columns(3)
        configuracoes[nome] = {
            "impressoes": col1.number_input(
                "Variação de impressões (%)",
                -100.0,
                500.0,
                padrao,
                1.0,
                key=f"cenario_impressoes_{nome}",
            ),
            "ctr": col2.number_input(
                "Variação de CTR (%)",
                -100.0,
                500.0,
                padrao,
                1.0,
                key=f"cenario_ctr_{nome}",
            ),
            "taxa_conversao": col3.number_input(
                "Variação da taxa de conversão (%)",
                -100.0,
                500.0,
                padrao,
                1.0,
                key=f"cenario_conversao_{nome}",
            ),
        }

if st.button("Calcular sensibilidade", type="primary", width="stretch"):
    st.session_state["cenarios_sensibilidade"] = service.simular_sensibilidade(
        origem["plano"],
        configuracoes,
    )

if "cenarios_sensibilidade" in st.session_state:
    cenarios = st.session_state["cenarios_sensibilidade"]
    resumo = pd.DataFrame([
        {
            "Cenário": nome,
            "Investimento": dados["investimento"],
            "Impressões": dados["impressoes"],
            "Cliques": dados["cliques"],
            "Conversões": dados["conversoes"],
        }
        for nome, dados in cenarios.items()
    ])
    st.subheader("Faixa condicional")
    st.dataframe(
        dataframe_ptbr(
            resumo,
            moedas=["Investimento"],
            inteiros=["Impressões"],
            decimais=["Cliques", "Conversões"],
        ),
        hide_index=True,
        width="stretch",
    )

    abas = st.tabs(list(cenarios))
    for aba, (nome, dados) in zip(abas, cenarios.items()):
        with aba:
            st.caption(
                f"Método: {dados['metodo']} · versão: {dados['versao']} · "
                f"investimento fixo: {moeda_ptbr(dados['investimento'])}."
            )
            st.write("Premissas:", dados["premissas_variacao_percentual"])
            st.dataframe(
                dataframe_ptbr(
                    pd.DataFrame(dados["itens"]),
                    moedas=["investimento"],
                    percentuais=["ctr_percentual", "taxa_conversao_percentual"],
                    inteiros=["impressoes"],
                    decimais=["cliques", "conversoes"],
                ),
                hide_index=True,
                width="stretch",
            )
            for limitacao in dados["limitacoes"]:
                st.caption(f"Limitação: {limitacao}")
            if dados["conversoes"] is None:
                st.warning(
                    "Conversões indisponíveis porque ao menos um inventário "
                    "não possui a cadeia completa de premissas."
                )
            else:
                st.metric(
                    "Conversões condicionais",
                    numero_ptbr(dados["conversoes"], 2),
                )
