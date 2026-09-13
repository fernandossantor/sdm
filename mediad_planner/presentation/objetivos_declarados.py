from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.objetivos_declarados import (
    AdicionarObjetivoComunicacaoEntrada,
    AdicionarObjetivoMarketingEntrada,
    DefinirVinculosObjetivoEntrada,
    DefinirRelacoesMarketingEntrada,
    EditarPrioridadeObjetivoEntrada,
    ObjetivoComunicacaoResumo,
    ObjetivoMarketingResumo,
)
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)


ESCALA = (
    "1 — Muito baixa",
    "2 — Baixa",
    "3 — Média",
    "4 — Alta",
    "5 — Muito alta",
)


def _valor_escala(rotulo: str) -> int:
    return int(rotulo.split(" ", 1)[0])


def _editar_prioridade_objetivo(aplicacao, id_campanha, objetivo) -> None:
    chave = f"prioridade_objetivo_{id_campanha}_{objetivo.id_objetivo}"
    with st.expander("Alterar prioridade, intensidade e justificativa"):
        with st.form(chave):
            prioridade = st.selectbox(
                "Prioridade declarada", ESCALA,
                index=objetivo.prioridade_declarada - 1, key=f"{chave}_prioridade",
                help="Importância relativa atribuída pelo usuário.",
            )
            intensidade = st.selectbox(
                "Intensidade declarada", ESCALA,
                index=objetivo.intensidade_declarada - 1, key=f"{chave}_intensidade",
                help="Força ou ambição declarada para o objetivo.",
            )
            justificativa = st.text_area(
                "Justificativa do Objetivo (opcional)",
                value=objetivo.justificativa or "", key=f"{chave}_justificativa",
            )
            salvar = st.form_submit_button("Salvar prioridade do Objetivo")
        if salvar:
            try:
                aplicacao.editar_prioridade_objetivo(id_campanha, EditarPrioridadeObjetivoEntrada(
                    objetivo.id_objetivo, _valor_escala(prioridade),
                    _valor_escala(intensidade), justificativa,
                ))
            except (LookupError, PermissionError, TypeError, ValueError) as erro:
                st.error(str(erro))
            else:
                st.rerun()


def _vinculos_objetivo(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
    objetivo: ObjetivoMarketingResumo | ObjetivoComunicacaoResumo,
) -> None:
    publicos = {
        item.id_publico: f"{indice}. {item.nome or 'Público sem nome'}"
        for indice, item in enumerate(briefing.publicos, 1)
    }
    pracas = {
        item.id_praca: f"{indice}. [{item.rotulo_tipo}] {item.nome}"
        for indice, item in enumerate(briefing.pracas, 1)
    }
    st.write("Públicos relacionados: " + (
        ", ".join(publicos[item] for item in objetivo.ids_publicos_relacionados)
        or "Nenhum vínculo declarado."
    ))
    st.write("Praças relacionadas: " + (
        ", ".join(pracas[item] for item in objetivo.ids_pracas_relacionadas)
        or "Nenhum vínculo declarado."
    ))
    with st.expander("Alterar Públicos e Praças relacionados"):
        st.caption(
            "Selecione os vínculos declarados para este objetivo. "
            "Para retirar um vínculo, desmarque a opção e salve. "
            "Praça aqui é o território da campanha."
        )
        if not publicos:
            st.info("Cadastre Públicos na subetapa Segmentos e públicos para vinculá-los.")
        if not pracas:
            st.info("Cadastre Praças na subetapa Praça e universo para vinculá-las.")
        chave = f"vinculos_objetivo_{id_campanha}_{objetivo.id_objetivo}"
        with st.form(chave):
            selecionados_publicos = st.multiselect(
                "Públicos relacionados (opcional)", tuple(publicos),
                default=objetivo.ids_publicos_relacionados,
                format_func=publicos.__getitem__, key=f"{chave}_publicos",
            )
            selecionadas_pracas = st.multiselect(
                "Praças relacionadas (opcional)", tuple(pracas),
                default=objetivo.ids_pracas_relacionadas,
                format_func=pracas.__getitem__, key=f"{chave}_pracas",
            )
            salvar = st.form_submit_button("Salvar vínculos do Objetivo")
        if salvar:
            try:
                aplicacao.definir_vinculos_objetivo(id_campanha, DefinirVinculosObjetivoEntrada(
                    objetivo.id_objetivo, tuple(selecionados_publicos), tuple(selecionadas_pracas),
                ))
            except (LookupError, PermissionError, TypeError, ValueError) as erro:
                st.error(str(erro))
            else:
                st.rerun()


def _formulario_marketing(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
) -> None:
    catalogo = aplicacao.listar_objetivos_marketing()
    dimensoes = aplicacao.listar_dimensoes_composto_marketing()
    rotulos = tuple(item.rotulo for item in catalogo)
    selecionado = st.selectbox(
        "Objetivo de Marketing",
        rotulos + ("Outro objetivo",),
    )
    definicao = next(
        (item for item in catalogo if item.rotulo == selecionado),
        None,
    )
    if definicao:
        st.caption(definicao.descricao)
    personalizado = ""
    if selecionado == "Outro objetivo":
        personalizado = st.text_input(
            "Informe o Objetivo de Marketing",
            help=(
                "Descreva de forma objetiva o resultado de Marketing "
                "declarado pelo anunciante."
            ),
        )
    mapa_dimensoes = {item.rotulo: item for item in dimensoes}
    dimensoes_selecionadas = st.multiselect(
        "Dimensões do composto relacionadas (opcional)",
        tuple(mapa_dimensoes),
        help=(
            "Praça (distribuição), neste campo, refere-se à distribuição e ao acesso da "
            "oferta, não à praça territorial da campanha."
        ),
    )
    prioridade = st.selectbox(
        "Prioridade declarada",
        ESCALA,
        index=2,
        help="Importância relativa atribuída pelo usuário.",
        key="prioridade_marketing",
    )
    intensidade = st.selectbox(
        "Intensidade declarada",
        ESCALA,
        index=2,
        help="Força ou ambição declarada para o objetivo.",
        key="intensidade_marketing",
    )
    justificativa = st.text_area(
        "Justificativa do Objetivo de Marketing (opcional)",
        help=(
            "Registre por que este objetivo foi declarado, sem formular "
            "objetivo de mídia ou recomendação."
        ),
    )
    if st.button("Adicionar Objetivo de Marketing"):
        if definicao is None and not personalizado.strip():
            st.error("Informe o Objetivo de Marketing")
            return
        entrada = AdicionarObjetivoMarketingEntrada(
            codigo_objetivo=definicao.codigo if definicao else None,
            objetivo=definicao.rotulo if definicao else personalizado,
            dimensoes_composto=tuple(
                mapa_dimensoes[item].codigo for item in dimensoes_selecionadas
            ),
            prioridade_declarada=_valor_escala(prioridade),
            intensidade_declarada=_valor_escala(intensidade),
            justificativa=justificativa,
        )
        try:
            aplicacao.adicionar_objetivo_marketing(id_campanha, entrada)
        except (LookupError, PermissionError, TypeError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success("Objetivo de Marketing adicionado.")
            st.rerun()


def _listar_marketing(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.markdown("#### Objetivos de Marketing salvos")
    for objetivo in briefing.objetivos_marketing:
        with st.container(border=True):
            st.write(f"**{objetivo.objetivo}**")
            st.write(f"Prioridade declarada: {objetivo.prioridade_declarada}")
            st.write(f"Intensidade declarada: {objetivo.intensidade_declarada}")
            if objetivo.dimensoes_composto:
                st.write(
                    "Dimensões do composto: "
                    + ", ".join(objetivo.rotulos_dimensoes_composto)
                )
            if objetivo.justificativa:
                st.write(f"Justificativa: {objetivo.justificativa}")
            _editar_prioridade_objetivo(aplicacao, id_campanha, objetivo)
            _vinculos_objetivo(aplicacao, id_campanha, briefing, objetivo)
            if st.button(
                "Remover Objetivo de Marketing",
                key=f"remover_marketing_{objetivo.id_objetivo}",
            ):
                try:
                    aplicacao.remover_objetivo_marketing(
                        id_campanha,
                        objetivo.id_objetivo,
                    )
                except (LookupError, PermissionError, ValueError) as erro:
                    st.error(str(erro))
                else:
                    st.rerun()


def _formulario_comunicacao(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    catalogo = aplicacao.listar_objetivos_comunicacao()
    rotulos = tuple(item.rotulo for item in catalogo)
    selecionado = st.selectbox(
        "Objetivo de Comunicação",
        rotulos + ("Outro objetivo",),
    )
    definicao = next(
        (item for item in catalogo if item.rotulo == selecionado),
        None,
    )
    if definicao:
        st.caption(definicao.descricao)
    personalizado = ""
    if selecionado == "Outro objetivo":
        personalizado = st.text_input(
            "Informe o Objetivo de Comunicação",
            help=(
                "Descreva de forma objetiva o resultado de Comunicação "
                "declarado pelo anunciante."
            ),
        )
    objetivos_por_id = {
        item.id_objetivo: item
        for item in briefing.objetivos_marketing
    }
    ordens_marketing = {
        item.id_objetivo: indice
        for indice, item in enumerate(briefing.objetivos_marketing, start=1)
    }
    opcoes_marketing = tuple(objetivos_por_id)
    relacionados = st.multiselect(
        "Objetivos de Marketing relacionados (opcional)",
        options=opcoes_marketing,
        format_func=lambda id_objetivo: (
            f"{ordens_marketing[id_objetivo]}. "
            f"{objetivos_por_id[id_objetivo].objetivo} — prioridade "
            f"{objetivos_por_id[id_objetivo].prioridade_declarada}"
        ),
    )
    if not opcoes_marketing:
        st.info(
            "Nenhum Objetivo de Marketing foi registrado. O Objetivo de "
            "Comunicação poderá ser salvo sem vínculo explícito."
        )
    prioridade = st.selectbox(
        "Prioridade declarada",
        ESCALA,
        index=2,
        key="prioridade_comunicacao",
        help="Importância relativa atribuída pelo usuário.",
    )
    intensidade = st.selectbox(
        "Intensidade declarada",
        ESCALA,
        index=2,
        key="intensidade_comunicacao",
        help="Força ou ambição declarada para o objetivo.",
    )
    justificativa = st.text_area(
        "Justificativa do Objetivo de Comunicação (opcional)",
        help=(
            "Registre por que este objetivo foi declarado e como ele se "
            "relaciona ao resultado de Marketing pretendido."
        ),
    )
    if st.button("Adicionar Objetivo de Comunicação"):
        if definicao is None and not personalizado.strip():
            st.error("Informe o Objetivo de Comunicação")
            return
        entrada = AdicionarObjetivoComunicacaoEntrada(
            codigo_objetivo=definicao.codigo if definicao else None,
            objetivo=definicao.rotulo if definicao else personalizado,
            ids_objetivos_marketing_relacionados=tuple(relacionados),
            prioridade_declarada=_valor_escala(prioridade),
            intensidade_declarada=_valor_escala(intensidade),
            justificativa=justificativa,
        )
        try:
            aplicacao.adicionar_objetivo_comunicacao(id_campanha, entrada)
        except (LookupError, PermissionError, TypeError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success("Objetivo de Comunicação adicionado.")
            st.rerun()


def _relacoes_marketing(aplicacao, id_campanha, briefing, objetivo) -> None:
    opcoes = {item.id_objetivo: f"{indice}. {item.objetivo}"
              for indice, item in enumerate(briefing.objetivos_marketing, 1)}
    chave = f"relacoes_marketing_{id_campanha}_{objetivo.id_objetivo}"
    with st.expander("Alterar Objetivos de Marketing relacionados"):
        st.caption("Selecione as relações declaradas. Para retirar uma relação, desmarque e salve.")
        if not opcoes:
            st.info("Cadastre Objetivos de Marketing para relacioná-los a este objetivo.")
        with st.form(chave):
            selecionados = st.multiselect(
                "Objetivos de Marketing relacionados (opcional)", tuple(opcoes),
                default=objetivo.ids_objetivos_marketing_relacionados,
                format_func=opcoes.__getitem__, key=f"{chave}_objetivos",
            )
            salvar = st.form_submit_button("Salvar relações com Marketing")
        if salvar:
            try:
                aplicacao.definir_relacoes_marketing(id_campanha, DefinirRelacoesMarketingEntrada(
                    objetivo.id_objetivo, tuple(selecionados),
                ))
            except (LookupError, PermissionError, TypeError, ValueError) as erro:
                st.error(str(erro))
            else:
                st.rerun()


def _listar_comunicacao(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.markdown("#### Objetivos de Comunicação salvos")
    objetivos_marketing = {
        item.id_objetivo: (indice, item)
        for indice, item in enumerate(briefing.objetivos_marketing, start=1)
    }
    for objetivo in briefing.objetivos_comunicacao:
        with st.container(border=True):
            st.write(f"**{objetivo.objetivo}**")
            st.write(f"Prioridade declarada: {objetivo.prioridade_declarada}")
            st.write(f"Intensidade declarada: {objetivo.intensidade_declarada}")
            if objetivo.ids_objetivos_marketing_relacionados:
                rotulos = []
                for id_relacionado in (
                    objetivo.ids_objetivos_marketing_relacionados
                ):
                    relacionado = objetivos_marketing.get(id_relacionado)
                    if relacionado is None:
                        st.error("Objetivo de Marketing relacionado não localizado.")
                        rotulos.append("Objetivo não localizado")
                        continue
                    ordem, item = relacionado
                    rotulos.append(f"{ordem}. {item.objetivo}")
                st.write(
                    "Objetivos de Marketing relacionados: " + ", ".join(rotulos)
                )
            else:
                st.write("Sem vínculo explícito com Objetivo de Marketing.")
            if objetivo.justificativa:
                st.write(f"Justificativa: {objetivo.justificativa}")
            _editar_prioridade_objetivo(aplicacao, id_campanha, objetivo)
            _vinculos_objetivo(aplicacao, id_campanha, briefing, objetivo)
            if st.button(
                "Remover Objetivo de Comunicação",
                key=f"remover_comunicacao_{objetivo.id_objetivo}",
            ):
                try:
                    aplicacao.remover_objetivo_comunicacao(
                        id_campanha,
                        objetivo.id_objetivo,
                    )
                except (LookupError, PermissionError, ValueError) as erro:
                    st.error(str(erro))
                else:
                    st.rerun()

            _relacoes_marketing(aplicacao, id_campanha, briefing, objetivo)


def apresentar_objetivos_declarados(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.subheader("Objetivos declarados")
    st.write(
        "Registre o que o anunciante declara querer alcançar em Marketing e "
        "Comunicação. O objetivo de mídia será produzido posteriormente pela "
        "Tradução Estratégica."
    )
    st.info(
        "Prioridade e intensidade registram a declaração do Briefing. "
        "Elas não são pesos calculados pelos motores."
    )
    aba_marketing, aba_comunicacao = st.tabs(("Marketing", "Comunicação"))
    for item in briefing.apontamentos_revisao:
        if (
            item.subetapa == "Objetivos declarados"
            and item.referencia_normativa == "02_BRIEFING.md § 13.3"
        ):
            st.warning(item.mensagem)
    with aba_marketing:
        _formulario_marketing(aplicacao, id_campanha)
        _listar_marketing(aplicacao, id_campanha, briefing)
    with aba_comunicacao:
        _formulario_comunicacao(aplicacao, id_campanha, briefing)
        _listar_comunicacao(aplicacao, id_campanha, briefing)
