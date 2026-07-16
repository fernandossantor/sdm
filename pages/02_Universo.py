import streamlit as st

st.set_page_config(
    page_title="Universo",
    layout="wide"
)

st.title("🌎 Universo e Segmentação")

st.markdown("---")

st.subheader("Universo")

col1, col2 = st.columns(2)

with col1:

    tipo_universo = st.selectbox(
        "Tipo",
        [
            "Pessoas"
        ]
    )

    populacao = st.number_input(
        "População",
        min_value=0,
        value=1000000
    )


with col2:

    publico_alvo = st.number_input(
        "Público-alvo",
        min_value=0,
        value=250000
    )

st.markdown("---")

st.subheader("Praça")

col1, col2, col3 = st.columns(3)

with col1:

    estado = st.text_input(
        "Estado",
        value="RS"
    )

with col2:

    cidade = st.text_input(
        "Cidade",
        value="Santa Maria"
    )

with col3:

    abrangencia = st.selectbox(
        "Abrangência",
        [
            "Local",
            "Regional",
            "Estadual",
            "Nacional"
        ]
    )

st.markdown("---")

st.subheader("Segmentação")


sexo = st.multiselect(

    "Sexo",

    [

        "Masculino",

        "Feminino"

    ]

)


faixa = st.multiselect(

    "Faixa etária",

    [

        "18-24",

        "25-34",

        "35-44",

        "45-59",

        "60+"

    ]

)


classe = st.multiselect(

    "Classe social",

    [

        "A",

        "B",

        "C",

        "D/E"

    ]

)

st.markdown("---")

st.subheader("Interesses")


interesses = st.multiselect(

    "Selecione",

    [

        "Notícias",

        "Esportes",

        "Entretenimento",

        "Tecnologia",

        "Saúde",

        "Finanças",

        "Educação"

    ]

)

st.markdown("---")

st.subheader("Afinidade")


if populacao > 0:

    afinidade = round(

        (publico_alvo / populacao) * 100,

        2

    )

else:

    afinidade = 0


st.metric(

    "Afinidade",

    f"{afinidade}%"

)

st.markdown("---")

st.subheader("Consumo de mídia")

col1, col2 = st.columns(2)

with col1:

    consumo_tv = st.slider(
        "TV",
        0,
        100,
        80
    )

    consumo_radio = st.slider(
        "Rádio",
        0,
        100,
        60
    )

    consumo_digital = st.slider(
        "Digital",
        0,
        100,
        90
    )

with col2:

    consumo_ooh = st.slider(
        "OOH",
        0,
        100,
        40
    )

    consumo_pdv = st.slider(
        "PDV",
        0,
        100,
        35
    )

st.markdown("---")

st.subheader("Afinidade por canal")

afinidades = {

    "TV": round(consumo_tv / 60 * 100, 1),

    "Rádio": round(consumo_radio / 50 * 100, 1),

    "Digital": round(consumo_digital / 65 * 100, 1),

    "OOH": round(consumo_ooh / 40 * 100, 1),

    "PDV": round(consumo_pdv / 35 * 100, 1)

}

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("TV", afinidades["TV"])

col2.metric("Rádio", afinidades["Rádio"])

col3.metric("Digital", afinidades["Digital"])

col4.metric("OOH", afinidades["OOH"])

col5.metric("PDV", afinidades["PDV"])

st.markdown("---")

st.subheader("Ranking dos meios")

ranking = sorted(

    afinidades.items(),

    key=lambda x: x[1],

    reverse=True

)


for posicao, (meio, valor) in enumerate(ranking, start=1):

    st.write(

        f"{posicao}º - {meio}: {valor}"

    )