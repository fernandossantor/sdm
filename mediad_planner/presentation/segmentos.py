from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.segmentos import SalvarSegmentoEntrada, SegmentoResumo
from mediad_planner.application.dto.publicos import PublicoResumo, SalvarPublicoEntrada
from mediad_planner.application.services.aplicacao_briefings import AplicacaoBriefings


CHAVE_SEGMENTO_EDICAO = "id_segmento_em_edicao"
CHAVE_PUBLICO_EDICAO = "id_publico_em_edicao"
ERROS_CONTROLADOS = (LookupError, PermissionError, TypeError, ValueError)


def _formulario(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
    segmento: SegmentoResumo | None,
) -> None:
    universos = {item.nome: item for item in briefing.universos}
    nomes_universos = tuple(universos)
    indice_universo = 0
    if segmento is not None:
        indice_universo = nomes_universos.index(segmento.nome_universo_origem)
    nome_universo = st.selectbox(
        "Universo de origem", nomes_universos, index=indice_universo
    )
    universo = universos[nome_universo]
    pracas = {
        rotulo: id_praca
        for id_praca, rotulo in zip(universo.ids_pracas, universo.rotulos_pracas)
    }
    padrao_pracas = (
        segmento.rotulos_pracas if segmento is not None else tuple(pracas)
    )
    rotulos_pracas = st.multiselect(
        "Praças do Segmento", tuple(pracas), default=padrao_pracas
    )
    catalogo = aplicacao.listar_criterios_segmentacao()
    criterios = {
        item.rotulo: item.codigo
        for item in catalogo
        if item.codigo in briefing.criterios_segmentacao
    }
    padrao_criterios = (
        segmento.rotulos_criterios if segmento is not None else ()
    )
    rotulos_criterios = st.multiselect(
        "Critérios aplicados", tuple(criterios), default=padrao_criterios
    )
    definicao = st.text_area(
        "Definição do Segmento",
        value=segmento.definicao if segmento is not None else "",
    )
    tamanho = st.text_input(
        "Tamanho estimado (opcional)",
        value=(segmento.tamanho_estimado or "") if segmento is not None else "",
        help=f"Unidade herdada do Universo: {universo.unidade}.",
    )
    fonte = st.text_input(
        "Fonte do Segmento (opcional)",
        value=(segmento.fonte or "") if segmento is not None else "",
    )
    data_referencia = st.text_input(
        "Data de referência do Segmento (opcional)",
        value=(segmento.data_referencia or "") if segmento is not None else "",
    )
    rotulo_acao = "Editar Segmento" if segmento is not None else "Criar Segmento"
    if st.button(rotulo_acao):
        entrada = SalvarSegmentoEntrada(
            id_universo_origem=universo.id_universo,
            ids_pracas=tuple(pracas[item] for item in rotulos_pracas),
            criterios_aplicados=tuple(criterios[item] for item in rotulos_criterios),
            definicao=definicao,
            tamanho_estimado=tamanho,
            fonte=fonte,
            data_referencia=data_referencia,
        )
        try:
            if segmento is None:
                aplicacao.adicionar_segmento(id_campanha, entrada)
            else:
                aplicacao.editar_segmento(
                    id_campanha, segmento.id_segmento, entrada
                )
        except ERROS_CONTROLADOS as erro:
            st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_SEGMENTO_EDICAO, None)
            st.success("Segmento salvo.")
            st.rerun()


def _listar(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    with st.expander(f"Segmentos salvos ({len(briefing.segmentos)})", expanded=False):
        if not briefing.segmentos:
            st.write("Nenhum Segmento cadastrado.")
        for item in briefing.segmentos:
            with st.container(border=True):
                st.write(f"**{item.definicao}**")
                st.write(f"Universo de origem: {item.nome_universo_origem}")
                st.write(f"Praças: {', '.join(item.rotulos_pracas)}")
                st.write(f"Critérios: {', '.join(item.rotulos_criterios)}")
                if item.tamanho_estimado is not None:
                    st.write(f"Tamanho estimado: {item.tamanho_estimado} {item.unidade}")
                editar, remover = st.columns(2)
                if editar.button("Editar Segmento", key=f"editar_{item.id_segmento}"):
                    st.session_state[CHAVE_SEGMENTO_EDICAO] = str(item.id_segmento)
                    st.rerun()
                if remover.button("Remover Segmento", key=f"remover_{item.id_segmento}"):
                    try:
                        aplicacao.remover_segmento(id_campanha, item.id_segmento)
                    except ERROS_CONTROLADOS as erro:
                        st.error(str(erro))
                    else:
                        st.rerun()


def apresentar_segmentos(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.subheader("Segmentos e públicos")
    segmentos, publicos = st.tabs(("Segmentos", "Públicos"))
    with segmentos:
        if not briefing.universos or not briefing.criterios_segmentacao:
            st.info(
                "Cadastre um Universo e selecione Critérios de segmentação "
                "antes de criar Segmentos."
            )
            return
        id_edicao = st.session_state.get(CHAVE_SEGMENTO_EDICAO)
        segmento = next(
            (item for item in briefing.segmentos if str(item.id_segmento) == id_edicao),
            None,
        )
        _formulario(aplicacao, id_campanha, briefing, segmento)
        _listar(aplicacao, id_campanha, briefing)
    with publicos:
        if not briefing.segmentos:
            st.info("Cadastre ao menos um Segmento antes de criar Públicos.")
        else:
            id_edicao = st.session_state.get(CHAVE_PUBLICO_EDICAO)
            publico = next(
                (item for item in briefing.publicos if str(item.id_publico) == id_edicao),
                None,
            )
            _formulario_publico(aplicacao, id_campanha, briefing, publico)
            _listar_publicos(aplicacao, id_campanha, briefing)


ESCALA_OPCIONAL = (
    "Não informar", "1 — Muito baixa", "2 — Baixa", "3 — Média",
    "4 — Alta", "5 — Muito alta",
)


def _escala(valor: str) -> int | None:
    return None if valor == "Não informar" else int(valor.split(" ", 1)[0])


def _rotulo_segmento(item: SegmentoResumo) -> str:
    return f"{item.definicao} · {str(item.id_segmento)[:8]}"


def _formulario_publico(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
    publico: PublicoResumo | None,
) -> None:
    segmentos = {_rotulo_segmento(item): item for item in briefing.segmentos}
    rotulos_por_id = {
        item.id_segmento: rotulo for rotulo, item in segmentos.items()
    }
    padrao_segmentos = (
        tuple(rotulos_por_id[item] for item in publico.ids_segmentos_origem)
        if publico is not None else ()
    )
    selecionados = st.multiselect(
        "Segmentos de origem", tuple(segmentos), default=padrao_segmentos
    )
    segmentos_selecionados = tuple(segmentos[item] for item in selecionados)
    ids_pracas_compativeis = {
        id_praca
        for segmento in segmentos_selecionados
        for id_praca in segmento.ids_pracas
    }
    rotulos_pracas = {
        id_praca: rotulo
        for segmento in briefing.segmentos
        for id_praca, rotulo in zip(segmento.ids_pracas, segmento.rotulos_pracas)
        if id_praca in ids_pracas_compativeis
    }
    pracas = {rotulo: id_praca for id_praca, rotulo in rotulos_pracas.items()}
    padrao_pracas = (
        publico.rotulos_pracas if publico is not None else tuple(pracas)
    )
    pracas_selecionadas = st.multiselect(
        "Praças do Público", tuple(pracas), default=padrao_pracas
    )
    nome = st.text_input(
        "Nome do Público (opcional)",
        value=(publico.nome or "") if publico is not None else "",
    )
    prioridade_inicial = publico.prioridade if publico is not None else None
    intensidade_inicial = (
        publico.intensidade_importancia if publico is not None else None
    )
    prioridade = st.selectbox(
        "Prioridade do Público",
        ESCALA_OPCIONAL,
        index=prioridade_inicial or 0,
    )
    intensidade = st.selectbox(
        "Intensidade de importância",
        ESCALA_OPCIONAL,
        index=intensidade_inicial or 0,
    )
    tamanho = st.text_input(
        "Tamanho estimado do Público (opcional)",
        value=(publico.tamanho_estimado or "") if publico is not None else "",
    )
    papel = st.text_input(
        "Papel declarado na Campanha (opcional)",
        value=(publico.papel_declarado or "") if publico is not None else "",
    )
    justificativa = st.text_area(
        "Justificativa complementar do Público (opcional)",
        value=(publico.justificativa or "") if publico is not None else "",
    )
    st.caption(
        "Segmentos podem se sobrepor; seus tamanhos não devem ser somados "
        "automaticamente para estimar o Público."
    )
    acao = "Editar Público" if publico is not None else "Criar Público"
    if st.button(acao):
        entrada = SalvarPublicoEntrada(
            nome=nome,
            ids_segmentos_origem=tuple(
                segmentos[item].id_segmento for item in selecionados
            ),
            ids_pracas=tuple(pracas[item] for item in pracas_selecionadas),
            prioridade=_escala(prioridade),
            intensidade_importancia=_escala(intensidade),
            tamanho_estimado=tamanho,
            papel_declarado=papel,
            justificativa=justificativa,
        )
        try:
            if publico is None:
                aplicacao.adicionar_publico(id_campanha, entrada)
            else:
                aplicacao.editar_publico(id_campanha, publico.id_publico, entrada)
        except ERROS_CONTROLADOS as erro:
            st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_PUBLICO_EDICAO, None)
            st.success("Público salvo.")
            st.rerun()


def _listar_publicos(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    if len(briefing.publicos) > 1 and any(
        item.prioridade is None for item in briefing.publicos
    ):
        st.warning("Há múltiplos Públicos e ao menos um está sem prioridade.")
    with st.expander(f"Públicos salvos ({len(briefing.publicos)})", expanded=False):
        if not briefing.publicos:
            st.write("Nenhum Público cadastrado.")
        for item in briefing.publicos:
            with st.container(border=True):
                st.write(f"**{item.nome or 'Público sem nome'}**")
                st.write("Segmentos: " + ", ".join(item.definicoes_segmentos_origem))
                st.write("Praças: " + ", ".join(item.rotulos_pracas))
                if item.prioridade is not None:
                    st.write(f"Prioridade: {item.prioridade}")
                if item.intensidade_importancia is not None:
                    st.write(f"Intensidade: {item.intensidade_importancia}")
                if item.tamanho_estimado is not None:
                    st.write(f"Tamanho estimado: {item.tamanho_estimado}")
                if item.papel_declarado:
                    st.write(f"Papel declarado: {item.papel_declarado}")
                if item.justificativa:
                    st.write(f"Justificativa: {item.justificativa}")
                editar, remover = st.columns(2)
                if editar.button("Editar Público", key=f"editar_publico_{item.id_publico}"):
                    st.session_state[CHAVE_PUBLICO_EDICAO] = str(item.id_publico)
                    st.rerun()
                if remover.button("Remover Público", key=f"remover_publico_{item.id_publico}"):
                    try:
                        aplicacao.remover_publico(id_campanha, item.id_publico)
                    except ERROS_CONTROLADOS as erro:
                        st.error(str(erro))
                    else:
                        st.rerun()
