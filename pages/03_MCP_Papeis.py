import streamlit as st

st.set_page_config(
    page_title="MCP",
    layout="wide"
)

import streamlit as st

st.set_page_config(
    page_title="MCP",
    layout="wide"
)

st.title("👥 Papéis de Compra")

st.caption(
    "Gerencie os papéis desempenhados pelos participantes do processo de decisão de compra."
)

st.divider()

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

pesos = {

    "afinidade":0.35,

    "cobertura":0.30,

    "consumo":0.20,

    "objetivo":0.15

}

scores = {}

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

    score = (

        afinidade * pesos["afinidade"]

        +

        cobertura * pesos["cobertura"]

        +

        consumo * pesos["consumo"]

        +

        objetivo * pesos["objetivo"]

    )

    scores[meio] = round(score,2)

    st.metric(

        "Score Estratégico",

        round(score,2)

    )

    st.markdown("---")


ranking = sorted(

    scores.items(),

    key=lambda x: x[1],

    reverse=True

)


st.header("🏆 Ranking Estratégico")


for posicao,(meio,valor) in enumerate(

    ranking,

    start=1

):

    if posicao == 1:

        papel = "Principal"

    elif posicao == 2:

        papel = "Complementar"

    else:

        papel = "Apoio"


    st.write(

        f"{posicao}º | {meio} | {papel} | Score: {valor}"

    )