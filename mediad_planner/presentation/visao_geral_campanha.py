import streamlit as st

from mediad_planner.application.dto.espaco_trabalho import (
    EspacoTrabalhoCampanhaResumo,
)
from mediad_planner.application.services.aplicacao_espaco_trabalho import (
    AplicacaoEspacoTrabalho,
)


ROTULOS_SITUACAO = {
    "RASCUNHO": "Rascunho",
    "EM_ANDAMENTO": "Em andamento",
    "CONCLUIDA": "Concluída",
    "CANCELADA": "Cancelada",
    "ARQUIVADA": "Arquivada",
}
ROTULOS_ETAPA = {
    "ABERTURA": "Abertura",
    "BRIEFING": "Briefing",
    "TRADUCAO_ESTRATEGICA": "Tradução Estratégica",
    "ARQUITETURA_DE_MIDIA": "Arquitetura de Mídia",
    "SIMULACAO": "Simulação",
    "CONSOLIDACAO_DO_PLANO": "Consolidação do Plano",
    "VALIDACAO_E_APROVACAO": "Validação e Aprovação",
    "ACOMPANHAMENTO_E_RESULTADOS": "Acompanhamento e Resultados",
}
ROTULOS_ESTADO_MODULO = {
    "DISPONIVEL": "Disponível",
    "ETAPA_ATUAL": "Etapa atual",
    "BLOQUEADO": "Bloqueado",
}
ROTULOS_ESTADO_BRIEFING = {
    "RASCUNHO": "Rascunho",
    "EM_PREENCHIMENTO": "Em preenchimento",
    "EM_REVISAO": "Em revisão",
    "CONCLUIDO": "Concluído",
    "SUBSTITUIDO": "Substituído",
}


def apresentar_visao_geral_campanha(
    aplicacao_espaco_trabalho: AplicacaoEspacoTrabalho,
    resumo: EspacoTrabalhoCampanhaResumo,
) -> bool:
    campanha = resumo.campanha
    st.header("Visão geral da Campanha")
    st.subheader(f"[{campanha.codigo}] {campanha.nome}")
    st.caption(campanha.marca or campanha.anunciante)

    situacao, etapa, atualizacao = st.columns(3)
    situacao.metric("Situação", ROTULOS_SITUACAO[campanha.situacao])
    etapa.metric("Etapa Atual", ROTULOS_ETAPA[campanha.etapa_atual])
    atualizacao.metric(
        "Última atualização",
        campanha.atualizado_em.strftime("%d/%m/%Y %H:%M"),
    )

    st.subheader("Contexto administrativo")
    with st.container(border=True):
        st.write(f"**Anunciante:** {campanha.anunciante}")
        if campanha.marca:
            st.write(f"**Marca:** {campanha.marca}")
        if campanha.produto_servico:
            st.write(f"**Produto ou Serviço:** {campanha.produto_servico}")
        st.write(
            f"**Planejador Responsável:** {campanha.planejador_responsavel}"
        )
        if campanha.equipe:
            st.write(f"**Equipe:** {', '.join(campanha.equipe)}")
        if campanha.observacao_inicial:
            st.write(f"**Observação inicial:** {campanha.observacao_inicial}")
        st.write(f"**Data de criação:** {campanha.criado_em:%d/%m/%Y %H:%M}")

    st.subheader("Briefing")
    with st.container(border=True):
        if resumo.briefing is None:
            st.info("Briefing ainda não iniciado.")
            if st.button("Iniciar Briefing", key="iniciar-briefing-visao-geral"):
                try:
                    aplicacao_espaco_trabalho.preparar_briefing(
                        campanha.id_campanha
                    )
                except (LookupError, PermissionError, ValueError) as erro:
                    st.error(str(erro))
                else:
                    return True
        else:
            briefing = resumo.briefing
            st.write(f"**Versão:** {briefing.numero_versao}")
            st.write(
                "**Estado:** "
                f"{ROTULOS_ESTADO_BRIEFING[briefing.estado]}"
            )
            st.write(
                "**Registros mercadológicos:** "
                f"{len(briefing.registros_situacao)}"
            )
            st.write(
                "**Objetivos de Marketing:** "
                f"{len(briefing.objetivos_marketing)}"
            )
            st.write(
                "**Objetivos de Comunicação:** "
                f"{len(briefing.objetivos_comunicacao)}"
            )
            st.write(f"**Praças:** {len(briefing.pracas)}")
            st.write(f"**Universos:** {len(briefing.universos)}")
            if st.button(
                "Continuar no Briefing",
                key="continuar-briefing-visao-geral",
            ):
                return True

    st.subheader("Progresso metodológico")
    for modulo in resumo.modulos:
        with st.container(border=True):
            st.write(
                f"**{modulo.rotulo}** — "
                f"{ROTULOS_ESTADO_MODULO[modulo.estado]}"
            )
            st.write(modulo.descricao)
            if modulo.motivo_bloqueio:
                st.caption(modulo.motivo_bloqueio)
    return False
