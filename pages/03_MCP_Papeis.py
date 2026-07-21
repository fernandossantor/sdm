import streamlit as st

from application.services.classificacao_papeis_service import (
    ClassificacaoPapeisService,
)

st.set_page_config(
    page_title="MCP",
    layout="wide"
)

st.title("🎯 MCP - Motor de Classificação dos Papéis")

st.markdown("---")

st.markdown("""
Este módulo classifica automaticamente os meios em:

- Principal
- Complementar
- Apoio

com base em:

- Afinidade
- Cobertura
- Consumo
- Adequação ao objetivo
""")

st.markdown("---")

meios = [

    "TV",

    "Rádio",

    "Digital",

    "OOH",

    "PDV"

]

scores = {}

service = ClassificacaoPapeisService()

for meio in meios:

    st.subheader(meio)

    col1, col2 = st.columns(2)

    with col1:

        afinidade = st.slider(

            f"Afinidade {meio}",

            0,

            200,

            100,

            key=f"afi_{meio}"

        )

        cobertura = st.slider(

            f"Cobertura {meio}",

            0,

            100,

            70,

            key=f"cob_{meio}"

        )

    with col2:

        consumo = st.slider(

            f"Consumo {meio}",

            0,

            100,

            60,

            key=f"cons_{meio}"

        )

        objetivo = st.slider(

            f"Adequação ao objetivo",

            0,

            100,

            80,

            key=f"obj_{meio}"

        )

    score = service.calcular_score(
        afinidade,
        cobertura,
        consumo,
        objetivo,
    )

    scores[meio] = round(score,2)

    st.metric(

        "Score Estratégico",

        round(score,2)

    )

    st.markdown("---")


ranking = service.classificar(scores)


st.header("🏆 Ranking Estratégico")


for item in ranking:
    st.write(
        f"{item['posicao']}º | {item['meio']} | "
        f"{item['papel']} | Score: {item['score']}"
    )
