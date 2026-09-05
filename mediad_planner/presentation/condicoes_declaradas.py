from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.condicoes_declaradas import (
    SalvarPretensaoEntrada,
    SalvarPrioridadeEntrada,
    SalvarRestricaoEntrada,
)
from mediad_planner.application.services.aplicacao_briefings import AplicacaoBriefings
from mediad_planner.presentation.objetivos_declarados import ESCALA, _valor_escala


ERROS = (LookupError, PermissionError, TypeError, ValueError)
CHAVE_PRIORIDADE = "prioridade_contextual_edicao"
CHAVE_RESTRICAO = "restricao_edicao"
CHAVE_PRETENSAO = "pretensao_edicao"


def _alvos_prioridade(briefing):
    alvos = {}
    for item in briefing.pracas:
        alvos[f"Praça · {item.nome} · {str(item.id_praca)[:8]}"] = ("PRACA", item.id_praca)
    for item in briefing.segmentos:
        alvos[f"Segmento · {item.definicao} · {str(item.id_segmento)[:8]}"] = ("SEGMENTO", item.id_segmento)
    if briefing.periodo_verba:
        alvos["Período pretendido"] = ("PERIODO", None)
    return alvos


def _aba_prioridades(aplicacao, id_campanha, briefing):
    st.caption("Objetivos, Públicos, Etapas, Restrições e Pretensões mantêm suas prioridades nos próprios registros.")
    alvos = _alvos_prioridade(briefing)
    id_edicao = st.session_state.get(CHAVE_PRIORIDADE)
    atual = next((item for item in briefing.prioridades_contextuais if str(item.id_prioridade) == id_edicao), None)
    if not alvos:
        st.info("Cadastre Praça, Segmento ou Período antes de aplicar prioridade contextual.")
    else:
        rotulo_atual = next(
            (rotulo for rotulo, valor in alvos.items() if atual and valor == (atual.tipo_entidade, atual.id_entidade)),
            tuple(alvos)[0],
        )
        alvo = st.selectbox("Entidade priorizada", tuple(alvos), index=tuple(alvos).index(rotulo_atual))
        prioridade = st.selectbox("Prioridade contextual", ESCALA, index=(atual.prioridade - 1 if atual else 2))
        informar_ordem = st.checkbox("Informar ordenação explícita", value=bool(atual and atual.ordem))
        ordem = st.number_input("Ordem da prioridade", min_value=1, step=1, value=atual.ordem if atual and atual.ordem else 1, disabled=not informar_ordem)
        justificativa = st.text_area("Justificativa da prioridade (opcional)", value=atual.justificativa or "" if atual else "")
        acao = "Editar Prioridade" if atual else "Criar Prioridade"
        if st.button(acao):
            tipo, identificador = alvos[alvo]
            try:
                aplicacao.salvar_prioridade(
                    id_campanha,
                    SalvarPrioridadeEntrada(tipo, identificador, _valor_escala(prioridade), int(ordem) if informar_ordem else None, justificativa),
                    atual.id_prioridade if atual else None,
                )
            except ERROS as erro:
                st.error(str(erro))
            else:
                st.session_state.pop(CHAVE_PRIORIDADE, None)
                st.rerun()
    valores = [item.prioridade for item in briefing.prioridades_contextuais]
    if len(valores) > 1 and len(set(valores)) == 1:
        st.warning("Todos os itens estão marcados com a mesma prioridade.")
    if sum(item.prioridade == 5 and not item.justificativa for item in briefing.prioridades_contextuais) > 1:
        st.warning("Há múltiplas prioridades máximas sem justificativa.")
    with st.expander(f"Prioridades contextuais salvas ({len(valores)})", expanded=False):
        for item in briefing.prioridades_contextuais:
            st.write(f"**{item.rotulo_entidade}** — prioridade {item.prioridade}")
            editar, remover = st.columns(2)
            if editar.button("Editar Prioridade", key=f"editar_prioridade_{item.id_prioridade}"):
                st.session_state[CHAVE_PRIORIDADE] = str(item.id_prioridade); st.rerun()
            if remover.button("Remover Prioridade", key=f"remover_prioridade_{item.id_prioridade}"):
                aplicacao.remover_prioridade(id_campanha, item.id_prioridade); st.rerun()


def _aba_restricoes(aplicacao, id_campanha, briefing):
    categorias = {item.rotulo: item.codigo for item in aplicacao.listar_categorias_restricao()}
    codigos = {codigo: rotulo for rotulo, codigo in categorias.items()}
    id_edicao = st.session_state.get(CHAVE_RESTRICAO)
    atual = next((item for item in briefing.restricoes if str(item.id_restricao) == id_edicao), None)
    rotulo = codigos[atual.categoria] if atual else tuple(categorias)[0]
    categoria = st.selectbox("Categoria da Restrição", tuple(categorias), index=tuple(categorias).index(rotulo))
    descricao = st.text_area("Descrição estruturada da Restrição", value=atual.descricao if atual else "")
    entidade = st.text_input("Entidade afetada (opcional)", value=atual.entidade_afetada or "" if atual else "")
    intensidade = st.selectbox("Intensidade da Restrição", ESCALA, index=(atual.intensidade - 1 if atual else 2))
    prioridade = st.selectbox("Prioridade da Restrição", ESCALA, index=(atual.prioridade - 1 if atual else 2))
    origem = st.text_input("Origem da Restrição (opcional)", value=atual.origem or "" if atual else "")
    justificativa = st.text_area("Justificativa da Restrição (opcional)", value=atual.justificativa or "" if atual else "")
    documento = st.text_input("Documento ou fonte (opcional)", value=atual.documento_fonte or "" if atual else "")
    observacao = st.text_area("Observação complementar da Restrição (opcional)", value=atual.observacao or "" if atual else "")
    acao = "Editar Restrição" if atual else "Criar Restrição"
    if st.button(acao):
        entrada = SalvarRestricaoEntrada(categorias[categoria], descricao, entidade, _valor_escala(intensidade), _valor_escala(prioridade), origem, justificativa, documento, observacao)
        try:
            aplicacao.salvar_restricao(id_campanha, entrada, atual.id_restricao if atual else None)
        except ERROS as erro: st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_RESTRICAO, None); st.rerun()
    with st.expander(f"Restrições salvas ({len(briefing.restricoes)})", expanded=False):
        for item in briefing.restricoes:
            st.write(f"**{item.rotulo_categoria}** — {item.descricao}")
            for alerta in item.diagnosticos: st.warning(alerta)
            editar, remover = st.columns(2)
            if editar.button("Editar Restrição", key=f"editar_restricao_{item.id_restricao}"):
                st.session_state[CHAVE_RESTRICAO] = str(item.id_restricao); st.rerun()
            if remover.button("Remover Restrição", key=f"remover_restricao_{item.id_restricao}"):
                aplicacao.remover_restricao(id_campanha, item.id_restricao); st.rerun()


def _opcoes_relacoes(briefing):
    publicos = {"Não associar": None} | {f"{item.nome or 'Público sem nome'} · {str(item.id_publico)[:8]}": item.id_publico for item in briefing.publicos}
    pracas = {"Não associar": None} | {f"{item.nome} · {str(item.id_praca)[:8]}": item.id_praca for item in briefing.pracas}
    etapas = {"Não associar": None} | {f"{etapa.rotulo_categoria} · {str(etapa.id_etapa)[:8]}": etapa.id_etapa for jornada in briefing.jornadas for etapa in jornada.etapas}
    return publicos, pracas, etapas


def _rotulo_por_valor(opcoes, valor):
    return next(rotulo for rotulo, item in opcoes.items() if item == valor)


def _aba_pretensoes(aplicacao, id_campanha, briefing):
    categorias = {item.rotulo: item.codigo for item in aplicacao.listar_categorias_pretensao()}
    codigos = {codigo: rotulo for rotulo, codigo in categorias.items()}
    id_edicao = st.session_state.get(CHAVE_PRETENSAO)
    atual = next((item for item in briefing.pretensoes if str(item.id_pretensao) == id_edicao), None)
    categoria_atual = codigos[atual.categoria] if atual else tuple(categorias)[0]
    categoria = st.selectbox("Categoria da Pretensão", tuple(categorias), index=tuple(categorias).index(categoria_atual))
    descricao = st.text_input("Descrição da outra pretensão controlada", value=atual.descricao_controlada or "" if atual else "", disabled=categorias[categoria] != "OUTRA")
    prioridade = st.selectbox("Prioridade da Pretensão", ESCALA, index=(atual.prioridade - 1 if atual else 2))
    intensidade = st.selectbox("Intensidade da Pretensão", ESCALA, index=(atual.intensidade - 1 if atual else 2))
    publicos, pracas, etapas = _opcoes_relacoes(briefing)
    publico = st.selectbox("Público associado (opcional)", tuple(publicos), index=tuple(publicos).index(_rotulo_por_valor(publicos, atual.id_publico if atual else None)))
    praca = st.selectbox("Praça associada (opcional)", tuple(pracas), index=tuple(pracas).index(_rotulo_por_valor(pracas, atual.id_praca if atual else None)))
    etapa = st.selectbox("Etapa da Jornada associada (opcional)", tuple(etapas), index=tuple(etapas).index(_rotulo_por_valor(etapas, atual.id_etapa_jornada if atual else None)))
    periodo = st.text_input("Período associado (opcional)", value=atual.periodo_associado or "" if atual else "", disabled=briefing.periodo_verba is None)
    flexibilidade = st.text_input("Flexibilidade declarada (opcional)", value=atual.flexibilidade_declarada or "" if atual else "")
    justificativa = st.text_area("Justificativa complementar da Pretensão (opcional)", value=atual.justificativa or "" if atual else "")
    acao = "Editar Pretensão" if atual else "Criar Pretensão"
    if st.button(acao):
        entrada = SalvarPretensaoEntrada(categorias[categoria], descricao, _valor_escala(prioridade), _valor_escala(intensidade), publicos[publico], pracas[praca], etapas[etapa], periodo, flexibilidade, justificativa)
        try: aplicacao.salvar_pretensao(id_campanha, entrada, atual.id_pretensao if atual else None)
        except ERROS as erro: st.error(str(erro))
        else:
            st.session_state.pop(CHAVE_PRETENSAO, None); st.rerun()
    with st.expander(f"Pretensões salvas ({len(briefing.pretensoes)})", expanded=False):
        for item in briefing.pretensoes:
            st.write(f"**{item.rotulo_categoria}** — prioridade {item.prioridade}, intensidade {item.intensidade}")
            editar, remover = st.columns(2)
            if editar.button("Editar Pretensão", key=f"editar_pretensao_{item.id_pretensao}"):
                st.session_state[CHAVE_PRETENSAO] = str(item.id_pretensao); st.rerun()
            if remover.button("Remover Pretensão", key=f"remover_pretensao_{item.id_pretensao}"):
                aplicacao.remover_pretensao(id_campanha, item.id_pretensao); st.rerun()


def apresentar_condicoes_declaradas(aplicacao: AplicacaoBriefings, id_campanha: UUID, briefing: BriefingResumo) -> None:
    st.subheader("Prioridades, Restrições e Pretensões")
    st.caption("Registre declarações do usuário. A classificação técnica e as decisões de mídia pertencem às etapas posteriores.")
    prioridades, restricoes, pretensoes = st.tabs(("Prioridades", "Restrições", "Pretensões"))
    with prioridades: _aba_prioridades(aplicacao, id_campanha, briefing)
    with restricoes: _aba_restricoes(aplicacao, id_campanha, briefing)
    with pretensoes: _aba_pretensoes(aplicacao, id_campanha, briefing)
