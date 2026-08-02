"""Casca mínima da reconstrução limpa do MediAd Planner."""

from pathlib import Path

import streamlit as st


RAIZ = Path(__file__).resolve().parents[2]
MARCA = RAIZ / "assets" / "Marca_nova.png"
FAVICON = RAIZ / "assets" / "favicon2.png"


def executar() -> None:
    """Inicializa somente a fundação limpa, sem regras herdadas."""
    st.set_page_config(
        page_title="MediAd Planner",
        page_icon=str(FAVICON) if FAVICON.exists() else "📊",
        layout="wide",
    )

    if MARCA.exists():
        st.image(MARCA, width=320)

    st.title("MediAd Planner")
    st.subheader("Reconstrução limpa do planejamento híbrido de mídia")
    st.info(
        "A fundação foi isolada do aplicativo anterior. As próximas capacidades "
        "serão implementadas exclusivamente a partir de docs/new_app."
    )
