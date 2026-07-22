import re

import streamlit as st

from components.formatters import numero_ptbr


def interpretar_numero_ptbr(valor):
    """Converte números digitados em pt-BR sem alterar os dados internos."""
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = re.sub(r"[^0-9,.-]", "", str(valor or "").strip())
    if not texto:
        return 0.0
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")
    elif "." in texto and len(texto.rsplit(".", 1)[1]) == 3:
        texto = texto.replace(".", "")
    return float(texto)


def entrada_monetaria(
    rotulo,
    valor=0.0,
    *,
    key,
    container=st,
    minimo=0.0,
    ajuda=None,
):
    """Exibe e interpreta moeda com ponto de milhar e vírgula decimal."""
    texto = container.text_input(
        rotulo,
        value=numero_ptbr(valor, 2),
        key=key,
        help=ajuda,
        placeholder="0,00",
    )
    try:
        numero = interpretar_numero_ptbr(texto)
    except ValueError:
        container.error(
            f"Informe {rotulo.lower()} no formato brasileiro, como 1.000,00."
        )
        st.stop()
    if numero < minimo:
        container.error(
            f"{rotulo} deve ser igual ou maior que {numero_ptbr(minimo, 2)}."
        )
        st.stop()
    return numero
