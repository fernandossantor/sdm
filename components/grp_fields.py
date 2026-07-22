import streamlit as st

from components.formatters import numero_ptbr
from domain.media_metrics import (
    classificar_alcance,
    classificar_frequencia,
    resolver_grp,
)


ROTULOS_CALCULO = {
    "GRP": "GRP",
    "FREQUENCIA": "Frequência média",
    "ALCANCE": "Alcance (%)",
}


def render(prefixo, alcance=60, frequencia=5, grp=None):
    if grp is None and alcance is not None and frequencia is not None:
        grp = float(alcance) * float(frequencia)

    calcular = st.selectbox(
        "Calcular automaticamente",
        list(ROTULOS_CALCULO),
        format_func=ROTULOS_CALCULO.get,
        key=f"{prefixo}_calcular",
        help="Informe os outros dois valores; o terceiro será calculado.",
    )
    c1, c2, c3 = st.columns(3)

    if calcular == "ALCANCE":
        frequencia = c2.number_input(
            "Frequência média",
            min_value=0.01,
            value=float(frequencia or 5),
            step=0.1,
            key=f"{prefixo}_frequencia",
        )
        grp = c3.number_input(
            "GRP",
            min_value=0.01,
            value=float(grp or 300),
            step=1.0,
            key=f"{prefixo}_grp",
        )
        alcance = grp / frequencia
        try:
            alcance, frequencia, grp = resolver_grp(None, frequencia, grp)
        except ValueError as erro:
            st.error(str(erro))
        c1.metric("Alcance calculado", f"{numero_ptbr(alcance, 2)}%")
    elif calcular == "FREQUENCIA":
        alcance = c1.number_input(
            "Alcance (%)",
            min_value=0.01,
            max_value=100.0,
            value=float(alcance or 60),
            step=1.0,
            key=f"{prefixo}_alcance",
        )
        grp = c3.number_input(
            "GRP",
            min_value=0.01,
            value=float(grp or 300),
            step=1.0,
            key=f"{prefixo}_grp",
        )
        alcance, frequencia, grp = resolver_grp(alcance, None, grp)
        c2.metric("Frequência calculada", numero_ptbr(frequencia, 2))
    else:
        alcance = c1.number_input(
            "Alcance (%)",
            min_value=0.01,
            max_value=100.0,
            value=float(alcance or 60),
            step=1.0,
            key=f"{prefixo}_alcance",
        )
        frequencia = c2.number_input(
            "Frequência média",
            min_value=0.01,
            value=float(frequencia or 5),
            step=0.1,
            key=f"{prefixo}_frequencia",
        )
        alcance, frequencia, grp = resolver_grp(alcance, frequencia, None)
        c3.metric("GRP calculado", numero_ptbr(grp, 2))

    st.caption(
        f"Faixa de alcance: {classificar_alcance(alcance).title()} · "
        f"Faixa de frequência: {classificar_frequencia(frequencia).title()} · "
        "GRP = alcance (%) × frequência média."
    )
    return {
        "alcance_percentual": alcance,
        "alcance_objetivo": classificar_alcance(alcance),
        "frequencia_alvo": frequencia,
        "frequencia_objetivo": classificar_frequencia(frequencia),
        "grp": grp,
    }
