import streamlit as st

from application.services.briefing_service import BriefingService
from application.services.identifier_service import IdentifierService
from application.services.planejamento_service import PlanejamentoService
from application.services.project_service import ProjectService


def render():
    """Restaura registros persistidos sem obrigar a reabrir etapas anteriores."""
    projetos = ProjectService().listar()
    if not projetos:
        return
    atual_id = st.session_state.get("projeto_id")
    opcoes = [None, *projetos]
    indice = next((i for i, p in enumerate(opcoes) if p and p["id"] == atual_id), 0)
    projeto = st.selectbox(
        "Projeto ativo", opcoes, index=indice,
        format_func=lambda item: "Selecione…" if item is None else IdentifierService.rotulo(item),
        key="seletor_contexto_projeto",
    )
    if projeto and projeto["id"] != atual_id:
        ProjectService.selecionar(projeto, st.session_state)
        for chave in ("briefing", "briefing_id", "briefing_ref", "plano", "forecast"):
            st.session_state.pop(chave, None)
        st.rerun()
    if not projeto:
        return

    briefings = BriefingService().listar(projeto["id"])
    if briefings:
        atual_briefing = st.session_state.get("briefing_id")
        opcoes_b = [None, *briefings]
        indice_b = next((i for i, b in enumerate(opcoes_b) if b and b["id"] == atual_briefing), 0)
        briefing = st.selectbox(
            "Briefing ativo", opcoes_b, index=indice_b,
            format_func=lambda item: "Selecione…" if item is None else IdentifierService.rotulo(item),
            key="seletor_contexto_briefing",
        )
        if briefing and briefing["id"] != atual_briefing:
            BriefingService().carregar(briefing, st.session_state)
            for chave in ("plano", "forecast", "diagnostico", "dashboard", "exportacao"):
                st.session_state.pop(chave, None)
            st.rerun()

    planos = [
        item for item in PlanejamentoService().listar()
        if not st.session_state.get("briefing_id")
        or item.get("briefing_id") == st.session_state.get("briefing_id")
    ]
    if planos:
        atual_plano = st.session_state.get("planejamento_id")
        opcoes_p = [None, *reversed(planos)]
        indice_p = next((i for i, p in enumerate(opcoes_p) if p and p["id"] == atual_plano), 0)
        plano = st.selectbox(
            "Plano ativo", opcoes_p, index=indice_p,
            format_func=lambda item: "Selecione…" if item is None else IdentifierService.rotulo(item),
            key="seletor_contexto_plano",
        )
        if plano and plano["id"] != atual_plano:
            st.session_state["plano"] = PlanejamentoService.restaurar(plano)
            st.session_state["planejamento_id"] = plano["id"]
            st.session_state["configuracao_planejamento"] = plano.get("configuracao") or {}
            st.rerun()
