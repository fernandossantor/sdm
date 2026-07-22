import streamlit as st
from application.services.identifier_service import IdentifierService


def selecionar_planejamento(service, key="planejamento_origem"):
    """Seleciona explicitamente um planejamento da sessão ou já salvo."""
    opcoes = []
    if "plano" in st.session_state:
        plano = st.session_state["plano"]
        opcoes.append({
            "rotulo": f"Sessão — {plano.codigo + ' · ' if plano.codigo else ''}{plano.campanha}",
            "plano": plano, "id": None,
        })
    for registro in reversed(service.listar()):
        opcoes.append(
            {
                "rotulo": f"Salvo — {IdentifierService.rotulo(registro)}",
                "plano": service.restaurar(registro),
                "id": registro["id"],
            }
        )
    if not opcoes:
        st.warning("Nenhum Plano de Mídia disponível. Gere e salve um plano primeiro.")
        st.page_link("pages/05_Planejamento.py", label="Ir para Plano de Mídia", icon="📋")
        st.stop()
    indice = st.selectbox(
        "Plano de Mídia",
        range(len(opcoes)),
        format_func=lambda valor: opcoes[valor]["rotulo"],
        key=key,
    )
    return opcoes[indice]
