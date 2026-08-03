"""Casca mínima da reconstrução limpa do MediAd Planner."""

from pathlib import Path
from uuid import UUID

import streamlit as st

from mediad_planner.application.use_cases.obter_diagnostico_fundacao import (
    obter_diagnostico_fundacao,
)
from mediad_planner.composition.ambiente import (
    AmbienteAplicacao,
    construir_ambiente_aplicacao_em_memoria,
)
from mediad_planner.presentation.administracao import apresentar_administracao
from mediad_planner.presentation.bibliotecas import apresentar_bibliotecas
from mediad_planner.presentation.campanhas import apresentar_campanhas
from mediad_planner.presentation.espaco_trabalho import (
    apresentar_espaco_trabalho,
)
from mediad_planner.presentation.guia_de_uso import apresentar_guia_de_uso
from mediad_planner.presentation.navegacao_global import (
    apresentar_navegacao_global,
)


RAIZ = Path(__file__).resolve().parents[2]
MARCA = RAIZ / "assets" / "Marca_nova.png"
FAVICON = RAIZ / "assets" / "favicon2.png"
CHAVE_CAMPANHA_ATIVA = "id_campanha_ativa"
CHAVE_MODULO_ATIVO = "modulo_campanha_ativo"
CHAVE_PAGINA_GLOBAL = "pagina_global_ativa"


@st.cache_resource
def _obter_ambiente() -> AmbienteAplicacao:
    return construir_ambiente_aplicacao_em_memoria()


def executar() -> None:
    """Inicializa somente a fundação limpa, sem regras herdadas."""
    st.set_page_config(
        page_title="MediAd Planner",
        page_icon=str(FAVICON) if FAVICON.exists() else "📊",
        layout="wide",
    )

    ambiente = _obter_ambiente()
    diagnostico = obter_diagnostico_fundacao()
    st.session_state.setdefault(CHAVE_PAGINA_GLOBAL, "CAMPANHAS")
    pagina_ativa = st.session_state[CHAVE_PAGINA_GLOBAL]
    id_ativo = st.session_state.get(CHAVE_CAMPANHA_ATIVA)
    resumo = None
    campanha_invalida = False
    if id_ativo is not None:
        try:
            resumo = ambiente.espaco_trabalho.obter_espaco_trabalho(
                UUID(id_ativo)
            )
        except (LookupError, PermissionError, ValueError):
            st.session_state.pop(CHAVE_CAMPANHA_ATIVA, None)
            st.session_state.pop(CHAVE_MODULO_ATIVO, None)
            st.session_state[CHAVE_PAGINA_GLOBAL] = "CAMPANHAS"
            pagina_ativa = "CAMPANHAS"
            campanha_invalida = True

    modulo_ativo = st.session_state.get(CHAVE_MODULO_ATIVO)
    if resumo is not None:
        modulos = {modulo.codigo: modulo for modulo in resumo.modulos}
        modulo = modulos.get(modulo_ativo or "")
        if modulo is None or not modulo.disponivel:
            modulo_ativo = "VISAO_GERAL"
            st.session_state[CHAVE_MODULO_ATIVO] = modulo_ativo

    acao = apresentar_navegacao_global(
        pagina_global_ativa=pagina_ativa,
        resumo_campanha=resumo,
        modulo_campanha_ativo=modulo_ativo,
        diagnostico=diagnostico,
    )
    if acao.fechar_campanha:
        st.session_state.pop(CHAVE_CAMPANHA_ATIVA, None)
        st.session_state.pop(CHAVE_MODULO_ATIVO, None)
        st.session_state[CHAVE_PAGINA_GLOBAL] = "CAMPANHAS"
        st.rerun()
    if acao.modulo_campanha is not None:
        st.session_state[CHAVE_PAGINA_GLOBAL] = "CAMPANHA"
        st.session_state[CHAVE_MODULO_ATIVO] = acao.modulo_campanha
        st.rerun()
    if acao.pagina_global in {
        "CAMPANHAS",
        "BIBLIOTECAS",
        "GUIA_DE_USO",
        "ADMINISTRACAO",
    }:
        st.session_state[CHAVE_PAGINA_GLOBAL] = acao.pagina_global
        st.rerun()

    if MARCA.exists():
        st.image(MARCA, width=320)
    st.title("MediAd Planner")
    if campanha_invalida:
        st.warning(
            "A Campanha ativa não está mais disponível. "
            "Selecione outra Campanha."
        )

    if pagina_ativa == "CAMPANHAS":
        st.subheader("Reconstrução limpa do planejamento híbrido de mídia")
        id_selecionado = apresentar_campanhas(
            ambiente.campanhas,
            ambiente.espaco_trabalho,
        )
        if id_selecionado is not None:
            st.session_state[CHAVE_CAMPANHA_ATIVA] = str(id_selecionado)
            st.session_state[CHAVE_MODULO_ATIVO] = "VISAO_GERAL"
            st.session_state[CHAVE_PAGINA_GLOBAL] = "CAMPANHA"
            st.rerun()
    elif pagina_ativa == "BIBLIOTECAS":
        apresentar_bibliotecas()
    elif pagina_ativa == "GUIA_DE_USO":
        apresentar_guia_de_uso()
    elif pagina_ativa == "ADMINISTRACAO":
        apresentar_administracao(diagnostico)
    elif pagina_ativa == "CAMPANHA" and resumo is not None:
        troca = apresentar_espaco_trabalho(
            ambiente.espaco_trabalho,
            ambiente.briefings,
            resumo,
            modulo_ativo or "VISAO_GERAL",
        )
        if troca is not None:
            st.session_state[CHAVE_MODULO_ATIVO] = troca
            st.rerun()
    else:
        st.session_state[CHAVE_PAGINA_GLOBAL] = "CAMPANHAS"
        st.rerun()
