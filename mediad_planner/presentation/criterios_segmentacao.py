from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.criterios_segmentacao import (
    DefinirCriteriosSegmentacaoEntrada,
)
from mediad_planner.application.services.aplicacao_briefings import AplicacaoBriefings


def apresentar_criterios_segmentacao(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.subheader("Critérios de segmentação")
    st.caption(
        "Selecione as categorias que poderão estruturar os Segmentos do "
        "Universo. A seleção não cria Segmentos nem Públicos automaticamente."
    )
    definicoes = aplicacao.listar_criterios_segmentacao()
    codigos_por_rotulo = {item.rotulo: item.codigo for item in definicoes}
    rotulos_por_codigo = {item.codigo: item.rotulo for item in definicoes}
    selecionados = st.multiselect(
        "Categorias canônicas",
        options=tuple(codigos_por_rotulo),
        default=tuple(
            rotulos_por_codigo[item]
            for item in briefing.criterios_segmentacao
            if item in rotulos_por_codigo
        ),
    )
    criar, editar = st.columns(2)
    criar_acionado = criar.button(
        "Criar seleção de critérios",
        disabled=bool(briefing.criterios_segmentacao),
    )
    editar_acionado = editar.button(
        "Editar critérios selecionados",
        disabled=not bool(briefing.criterios_segmentacao),
    )
    if criar_acionado or editar_acionado:
        if not selecionados:
            st.error("Selecione ao menos um critério de segmentação.")
            return
        entrada = DefinirCriteriosSegmentacaoEntrada(
            tuple(codigos_por_rotulo[item] for item in selecionados)
        )
        try:
            aplicacao.definir_criterios_segmentacao(id_campanha, entrada)
        except (LookupError, PermissionError, TypeError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success("Critérios de segmentação salvos.")
            st.rerun()

    with st.expander(
        f"Critérios selecionados ({len(briefing.criterios_segmentacao)})",
        expanded=False,
    ):
        if not briefing.criterios_segmentacao:
            st.write("Nenhum critério selecionado.")
        for codigo in briefing.criterios_segmentacao:
            st.write(f"- {rotulos_por_codigo[codigo]}")
