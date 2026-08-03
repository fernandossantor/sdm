from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)


def _rotulo_estado(valor: str) -> str:
    rotulos = {
        "RASCUNHO": "Rascunho",
        "EM_PREENCHIMENTO": "Em preenchimento",
        "EM_REVISAO": "Em revisão",
        "CONCLUIDO": "Concluído",
        "SUBSTITUIDO": "Substituído",
    }
    return rotulos[valor]


def _apresentar_contexto(briefing: BriefingResumo) -> None:
    st.subheader("Contexto herdado da Campanha")
    st.info(
        "Estes dados são herdados da Campanha e não são redefinidos no Briefing."
    )
    with st.container(border=True):
        st.write(f"**Código da Campanha:** {briefing.codigo_campanha}")
        st.write(f"**Nome da Campanha:** {briefing.nome_campanha}")
        st.write(f"**Anunciante:** {briefing.anunciante}")
        if briefing.marca:
            st.write(f"**Marca:** {briefing.marca}")
        if briefing.produto_servico:
            st.write(f"**Produto ou Serviço:** {briefing.produto_servico}")
        st.write(f"**Planejador Responsável:** {briefing.planejador_responsavel}")
        if briefing.equipe:
            st.write(f"**Equipe:** {', '.join(briefing.equipe)}")


def _apresentar_subetapas() -> None:
    st.subheader("Estrutura progressiva")
    subetapas = (
        "1. Situação mercadológica e competitiva",
        "2. Objetivos declarados",
        "3. Praça e universo",
        "4. Segmentos e públicos",
        "5. Jornada",
        "6. Período e verba",
        "7. Prioridades, restrições e pretensões",
        "8. Revisão do Briefing",
    )
    for subetapa in subetapas:
        st.write(f"**{subetapa}** — Não iniciada")
    st.info(
        "A estrutura do Briefing está disponível. O conteúdo metodológico será "
        "implementado incrementalmente."
    )


def apresentar_briefing(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
) -> bool:
    if st.button("Voltar às Campanhas"):
        return True
    try:
        briefing = aplicacao.abrir_briefing(id_campanha)
    except (LookupError, PermissionError, ValueError) as erro:
        st.error(str(erro))
        return False

    st.header("Briefing de Mídia")
    st.subheader(f"[{briefing.codigo_campanha}] {briefing.nome_campanha}")
    versao, estado = st.columns(2)
    versao.metric("Versão", briefing.numero_versao)
    estado.metric("Estado", _rotulo_estado(briefing.estado))
    _apresentar_contexto(briefing)
    _apresentar_subetapas()
    return False
