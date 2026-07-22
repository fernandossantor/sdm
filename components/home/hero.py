import streamlit as st
from pathlib import Path


LOGO_PLANOS = Path(__file__).parents[2] / "assets" / "PlanOS.png"


def render():

    st.image(LOGO_PLANOS, width=450)

    st.subheader(

        "Plataforma Inteligente de Planejamento Híbrido de Mídia"

    )

    st.markdown(

        """
Planejamento estratégico de mídia baseado em conhecimento,
motores de decisão e workflow inteligente.
"""
    )

    st.divider()
