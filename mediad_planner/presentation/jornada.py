from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.jornada import (
    EtapaJornadaResumo,
    JornadaResumo,
    SalvarEtapaJornadaEntrada,
    SalvarJornadaEntrada,
)
from mediad_planner.application.services.aplicacao_briefings import AplicacaoBriefings
from mediad_planner.presentation.segmentos import ESCALA_OPCIONAL, _escala


CHAVE_JORNADA_EDICAO = "id_jornada_em_edicao"
CHAVE_ETAPA_EDICAO = "id_etapa_jornada_em_edicao"
ERROS = (LookupError, PermissionError, TypeError, ValueError)


def _rotulo_publico(item) -> str:
    return f"{item.nome or 'Público sem nome'} · {str(item.id_publico)[:8]}"


def _formulario_jornada(aplicacao, id_campanha, briefing, jornada) -> None:
    publicos = {_rotulo_publico(item): item for item in briefing.publicos}
    rotulos_por_id = {item.id_publico: rotulo for rotulo, item in publicos.items()}
    padrao = (
        tuple(rotulos_por_id[item] for item in jornada.ids_publicos)
        if jornada is not None else ()
    )
    nome = st.text_input(
        "Nome da Jornada", value=jornada.nome if jornada is not None else ""
    )
    descricao = st.text_area(
        "Descrição da Jornada (opcional)",
        value=(jornada.descricao or "") if jornada is not None else "",
    )
    selecionados = st.multiselect(
        "Públicos associados à Jornada", tuple(publicos), default=padrao
    )
    referencia = st.text_input(
        "Modelo ou referência de origem (opcional)",
        value=(jornada.referencia_modelo or "") if jornada is not None else "",
        help="Não há modelo universal obrigatório nem catálogo canônico presumido.",
    )
    adaptada = st.checkbox(
        "Jornada adaptada localmente para esta Campanha",
        value=jornada.adaptada_localmente if jornada is not None else True,
    )
    acao = "Editar Jornada" if jornada is not None else "Criar Jornada"
    if st.button(acao):
        entrada = SalvarJornadaEntrada(
            nome, descricao, tuple(publicos[item].id_publico for item in selecionados),
            referencia, adaptada,
        )
        try:
            if jornada is None:
                aplicacao.adicionar_jornada(id_campanha, entrada)
            else:
                aplicacao.editar_jornada(id_campanha, jornada.id_jornada, entrada)
        except ERROS as erro:
            st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_JORNADA_EDICAO, None)
            st.rerun()


def _formulario_etapa(aplicacao, id_campanha, briefing, jornada, etapa) -> None:
    categorias = aplicacao.listar_categorias_etapa_jornada()
    categorias_por_rotulo = {item.rotulo: item.codigo for item in categorias}
    rotulos_por_codigo = {item.codigo: item.rotulo for item in categorias}
    rotulo_categoria = st.selectbox(
        "Categoria da Etapa", tuple(categorias_por_rotulo),
        index=(tuple(categorias_por_rotulo).index(rotulos_por_codigo[etapa.categoria])
               if etapa is not None else 0),
    )
    informar_ordem = st.checkbox(
        "Informar ordem relativa", value=etapa is None or etapa.ordem is not None
    )
    ordem = st.number_input(
        "Ordem", min_value=1, step=1,
        value=etapa.ordem if etapa is not None and etapa.ordem is not None else 1,
        disabled=not informar_ordem,
    )
    existe = st.checkbox(
        "Esta Etapa existe na Jornada declarada",
        value=etapa.existe if etapa is not None else True,
    )
    escalas = {}
    for campo, rotulo in (
        ("relevancia", "Relevância da Etapa"),
        ("intensidade", "Intensidade da Etapa"),
        ("prioridade", "Prioridade da Etapa"),
    ):
        atual = getattr(etapa, campo) if etapa is not None else None
        escalas[campo] = st.selectbox(
            rotulo, ESCALA_OPCIONAL, index=atual or 0,
            key=f"etapa_{campo}_{jornada.id_jornada}",
        )
    publicos_briefing = {item.id_publico: item for item in briefing.publicos}
    publicos = {
        _rotulo_publico(publicos_briefing[id_publico]): id_publico
        for id_publico in jornada.ids_publicos
    }
    rotulos_por_id = {id_publico: rotulo for rotulo, id_publico in publicos.items()}
    publicos_selecionados = st.multiselect(
        "Públicos associados à Etapa", tuple(publicos),
        default=(tuple(rotulos_por_id[item] for item in etapa.ids_publicos)
                 if etapa is not None else tuple(publicos)),
    )
    objetivos = {
        f"{item.objetivo} · {str(item.id_objetivo)[:8]}": item.id_objetivo
        for item in briefing.objetivos_comunicacao
    }
    rotulos_objetivos = {valor: chave for chave, valor in objetivos.items()}
    objetivos_selecionados = st.multiselect(
        "Objetivos de Comunicação relacionados (opcional)", tuple(objetivos),
        default=(tuple(rotulos_objetivos[item] for item in etapa.ids_objetivos_comunicacao)
                 if etapa is not None else ()),
    )
    atual = st.text_area(
        "Situação atual (opcional)",
        value=(etapa.situacao_atual or "") if etapa is not None else "",
    )
    pretendida = st.text_area(
        "Situação pretendida (opcional)",
        value=(etapa.situacao_pretendida or "") if etapa is not None else "",
    )
    observacao = st.text_area(
        "Observação complementar da Etapa (opcional)",
        value=(etapa.observacao or "") if etapa is not None else "",
    )
    acao = "Editar Etapa" if etapa is not None else "Criar Etapa"
    if st.button(acao):
        entrada = SalvarEtapaJornadaEntrada(
            categorias_por_rotulo[rotulo_categoria], int(ordem) if informar_ordem else None,
            existe, _escala(escalas["relevancia"]), _escala(escalas["intensidade"]),
            _escala(escalas["prioridade"]),
            tuple(publicos[item] for item in publicos_selecionados),
            tuple(objetivos[item] for item in objetivos_selecionados),
            atual, pretendida, observacao,
        )
        try:
            if etapa is None:
                aplicacao.adicionar_etapa_jornada(id_campanha, jornada.id_jornada, entrada)
            else:
                aplicacao.editar_etapa_jornada(
                    id_campanha, jornada.id_jornada, etapa.id_etapa, entrada
                )
        except ERROS as erro:
            st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_ETAPA_EDICAO, None)
            st.rerun()


def apresentar_jornada(
    aplicacao: AplicacaoBriefings, id_campanha: UUID, briefing: BriefingResumo,
) -> None:
    st.subheader("Jornada")
    st.caption("Registre o percurso declarado do Público. Pontos de contato não pertencem ao Briefing.")
    if not briefing.publicos:
        st.info("Cadastre ao menos um Público antes de criar uma Jornada.")
        return
    id_edicao = st.session_state.get(CHAVE_JORNADA_EDICAO)
    jornada_edicao = next(
        (item for item in briefing.jornadas if str(item.id_jornada) == id_edicao), None
    )
    _formulario_jornada(aplicacao, id_campanha, briefing, jornada_edicao)
    ids_com_jornada = {id_publico for item in briefing.jornadas for id_publico in item.ids_publicos}
    sem_jornada = [item for item in briefing.publicos if item.id_publico not in ids_com_jornada]
    if sem_jornada:
        st.warning("Há Público sem Jornada associada; confirme se a Jornada é necessária.")
    with st.expander(f"Jornadas salvas ({len(briefing.jornadas)})", expanded=False):
        for item in briefing.jornadas:
            st.write(f"**{item.nome}** — {', '.join(item.nomes_publicos)}")
            if item.referencia_modelo and not item.adaptada_localmente:
                st.warning("Modelo de Jornada informado sem adaptação local declarada.")
            editar, remover = st.columns(2)
            if editar.button("Editar Jornada", key=f"editar_jornada_{item.id_jornada}"):
                st.session_state[CHAVE_JORNADA_EDICAO] = str(item.id_jornada)
                st.rerun()
            if remover.button("Remover Jornada", key=f"remover_jornada_{item.id_jornada}"):
                try:
                    aplicacao.remover_jornada(id_campanha, item.id_jornada)
                except ERROS as erro:
                    st.error(str(erro))
                else:
                    st.rerun()
    if not briefing.jornadas:
        return
    jornadas = {item.nome: item for item in briefing.jornadas}
    jornada = jornadas[st.selectbox("Jornada para gerenciar Etapas", tuple(jornadas))]
    id_etapa = st.session_state.get(CHAVE_ETAPA_EDICAO)
    etapa = next((item for item in jornada.etapas if str(item.id_etapa) == id_etapa), None)
    _formulario_etapa(aplicacao, id_campanha, briefing, jornada, etapa)
    prioritarias = [item for item in jornada.etapas if item.prioridade == 5]
    if len(prioritarias) > 1 and any(item.ordem is None for item in prioritarias):
        st.warning("Há múltiplas Etapas prioritárias sem ordenação explícita.")
    with st.expander(f"Etapas salvas ({len(jornada.etapas)})", expanded=False):
        for item in jornada.etapas:
            st.write(f"**{item.ordem or 'Sem ordem'} · {item.rotulo_categoria}**")
            st.write("Públicos: " + ", ".join(item.nomes_publicos))
            if not item.ids_objetivos_comunicacao:
                st.warning("Etapa sem relação com Objetivo de Comunicação.")
            editar, remover = st.columns(2)
            if editar.button("Editar Etapa", key=f"editar_etapa_{item.id_etapa}"):
                st.session_state[CHAVE_ETAPA_EDICAO] = str(item.id_etapa)
                st.rerun()
            if remover.button("Remover Etapa", key=f"remover_etapa_{item.id_etapa}"):
                aplicacao.remover_etapa_jornada(id_campanha, jornada.id_jornada, item.id_etapa)
                st.rerun()
