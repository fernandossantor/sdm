from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import (
    AdicionarRegistroSituacaoEntrada,
    BriefingResumo,
    RegistroSituacaoResumo,
)
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)
from mediad_planner.application.services.aplicacao_catalogo_territorial import (
    AplicacaoCatalogoTerritorial,
)
from mediad_planner.presentation.objetivos_declarados import (
    apresentar_objetivos_declarados,
)
from mediad_planner.presentation.praca_universo import apresentar_praca_universo


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
    with st.expander("Contexto herdado da Campanha", expanded=False):
        st.caption(
            "Estes dados são herdados da Campanha e não são redefinidos no "
            "Briefing."
        )
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


ROTULOS_ESCOPOS = (
    ("Anunciante", "ANUNCIANTE"),
    ("Mercado", "MERCADO"),
    ("Categoria", "CATEGORIA"),
    ("Concorrência", "CONCORRENCIA"),
)
ROTULOS_NATUREZAS = (
    ("Quantitativo", "QUANTITATIVO"),
    ("Qualitativo", "QUALITATIVO"),
)


def _apresentar_subetapas(briefing: BriefingResumo) -> None:
    subetapas = (
        "4. Segmentos e públicos",
        "5. Jornada",
        "6. Período e verba",
        "7. Prioridades, restrições e pretensões",
        "8. Revisão do Briefing",
    )
    estado_situacao = (
        "Em preenchimento" if briefing.registros_situacao else "Não iniciada"
    )
    estado_objetivos = (
        "Em preenchimento"
        if briefing.objetivos_marketing or briefing.objetivos_comunicacao
        else "Não iniciada"
    )
    estado_praca_universo = (
        "Em preenchimento"
        if briefing.pracas or briefing.universos
        else "Não iniciada"
    )
    with st.expander("Estrutura do Briefing", expanded=False):
        st.write(
            "**1. Situação mercadológica e competitiva** — "
            f"{estado_situacao}"
        )
        st.write(f"**2. Objetivos declarados** — {estado_objetivos}")
        st.write(f"**3. Praça e universo** — {estado_praca_universo}")
        for subetapa in subetapas:
            st.write(f"**{subetapa}** — Não iniciada")


def _formulario_situacao(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
) -> None:
    st.subheader("Situação mercadológica e competitiva")
    st.caption(
        "Registre fatos, indicadores e condições informadas sobre o anunciante, "
        "o mercado, a categoria e a concorrência. O sistema organiza as "
        "declarações sem produzir interpretação estratégica."
    )
    mapa_escopos = dict(ROTULOS_ESCOPOS)
    rotulo_escopo = st.selectbox("Escopo", tuple(mapa_escopos))
    escopo = mapa_escopos[rotulo_escopo]
    aspectos = aplicacao.listar_aspectos_situacao(escopo)
    rotulos_aspectos = tuple(item.rotulo for item in aspectos)
    aspecto_selecionado = st.selectbox(
        "Aspecto observado",
        rotulos_aspectos + ("Outro aspecto",),
    )
    definicao = next(
        (item for item in aspectos if item.rotulo == aspecto_selecionado),
        None,
    )
    if definicao is not None:
        st.caption(definicao.descricao)
    aspecto_personalizado = None
    if aspecto_selecionado == "Outro aspecto":
        aspecto_personalizado = st.text_input(
            "Nome do aspecto observado",
            help=(
                "Informe de forma objetiva o indicador, condição ou "
                "característica que está sendo registrada."
            ),
        )
    aspecto_informado = aspecto_personalizado or (
        aspecto_selecionado if definicao is not None else ""
    )
    rotulo_campo = aspecto_informado or "aspecto observado"
    entidade = None
    if escopo == "CONCORRENCIA":
        entidade = st.text_input("Concorrente relacionado")
    mapa_naturezas = dict(ROTULOS_NATUREZAS)
    rotulo_natureza = st.selectbox("Natureza", tuple(mapa_naturezas))
    natureza = mapa_naturezas[rotulo_natureza]
    valor = None
    unidade = None
    qualitativo = None
    if natureza == "QUANTITATIVO":
        valor = st.text_input(
            (
                f"Valor de “{rotulo_campo}”"
                if aspecto_informado
                else "Valor do aspecto observado"
            ),
            help=(
                "Informe apenas o valor numérico. Use ponto como separador "
                "decimal. Exemplo: 10.5"
            ),
        )
        sugestoes = ""
        if definicao is not None and definicao.unidades_sugeridas:
            sugestoes = "Sugestões: " + ", ".join(definicao.unidades_sugeridas) + "."
        unidade = st.text_input(
            "Unidade de medida",
            help=sugestoes or None,
        )
    else:
        qualitativo = st.text_area(
            (
                f"Descrição de “{rotulo_campo}”"
                if aspecto_informado
                else "Descrição do aspecto observado"
            ),
            help=(
                "Descreva a condição observada sem interpretar causas ou "
                "recomendar ações."
            ),
            placeholder="Ex.: Crescimento moderado nos últimos dois anos.",
        )
    fonte = st.text_input(
        "Fonte dos dados (opcional)",
        help=(
            "Informe a origem da informação, como pesquisa, relatório, "
            "instituto, sistema interno ou declaração do anunciante."
        ),
        placeholder=(
            "Ex.: IBGE; Kantar Ibope; relatório comercial interno."
        ),
    )
    periodo = st.text_input(
        "Período de referência (opcional)",
        help="Informe a data ou intervalo ao qual o dado se refere.",
        placeholder="Ex.: 2025; jan–jun/2026; 2º trimestre de 2026.",
    )
    observacao = st.text_area(
        "Observação complementar (opcional)",
        help="Acrescente apenas contexto necessário para compreender este registro.",
    )
    if st.button("Adicionar registro"):
        if definicao is None and not aspecto_personalizado.strip():
            st.error("Informe o nome do aspecto observado")
            return
        entrada = AdicionarRegistroSituacaoEntrada(
            escopo=escopo,
            codigo_aspecto=definicao.codigo if definicao is not None else None,
            aspecto=aspecto_informado,
            entidade_referencia=entidade,
            natureza=natureza,
            valor_quantitativo=valor,
            unidade=unidade,
            valor_qualitativo=qualitativo,
            fonte=fonte,
            periodo_referencia=periodo,
            observacao=observacao,
        )
        try:
            aplicacao.adicionar_registro_situacao(id_campanha, entrada)
        except (LookupError, PermissionError, TypeError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success("Registro adicionado.")
            st.rerun()


def _possui_texto(valor: str | None) -> bool:
    return bool(valor and valor.strip())


def _detalhar_registro(registro: RegistroSituacaoResumo) -> None:
    st.write(f"**{registro.aspecto}**")
    if _possui_texto(registro.entidade_referencia):
        st.write(f"Concorrente relacionado: {registro.entidade_referencia}")
    if registro.valor_quantitativo is not None:
        if _possui_texto(registro.unidade):
            st.write(
                f"{registro.valor_quantitativo} {registro.unidade.strip()}"
            )
        else:
            st.write(registro.valor_quantitativo)
    if _possui_texto(registro.valor_qualitativo):
        st.write(registro.valor_qualitativo)
    if _possui_texto(registro.fonte):
        st.write(f"Fonte dos dados: {registro.fonte}")
    if _possui_texto(registro.periodo_referencia):
        st.write(f"Período de referência: {registro.periodo_referencia}")
    if _possui_texto(registro.observacao):
        st.write(f"Observação: {registro.observacao}")


def _apresentar_registros(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    quantidade = len(briefing.registros_situacao)
    with st.expander(
        f"Registros salvos ({quantidade})",
        expanded=False,
    ):
        if quantidade == 0:
            st.write("Nenhum registro salvo nesta subetapa.")
        for rotulo, escopo in ROTULOS_ESCOPOS:
            registros = tuple(
                item
                for item in briefing.registros_situacao
                if item.escopo == escopo
            )
            if not registros:
                continue
            st.markdown(f"#### {rotulo}")
            for registro in registros:
                with st.container(border=True):
                    _detalhar_registro(registro)
                    if st.button(
                        "Remover registro",
                        key=f"remover_{registro.id_registro}",
                    ):
                        try:
                            aplicacao.remover_registro_situacao(
                                id_campanha,
                                registro.id_registro,
                            )
                        except (LookupError, PermissionError, ValueError) as erro:
                            st.error(str(erro))
                        else:
                            st.rerun()


def apresentar_briefing(
    aplicacao: AplicacaoBriefings,
    aplicacao_catalogo: AplicacaoCatalogoTerritorial,
    id_campanha: UUID,
) -> None:
    try:
        briefing = aplicacao.abrir_briefing(id_campanha)
    except (LookupError, PermissionError, ValueError) as erro:
        st.error(str(erro))
        return

    st.header("Briefing de Mídia")
    st.subheader(f"[{briefing.codigo_campanha}] {briefing.nome_campanha}")
    versao, estado = st.columns(2)
    versao.metric("Versão", briefing.numero_versao)
    estado.metric("Estado", _rotulo_estado(briefing.estado))
    contexto_resumido = f"Anunciante: {briefing.anunciante}"
    if briefing.marca:
        contexto_resumido += f" · Marca: {briefing.marca}"
    contexto_resumido += f" · Planejador: {briefing.planejador_responsavel}"
    st.caption(contexto_resumido)
    if briefing.produto_servico:
        st.caption(f"Produto ou Serviço: {briefing.produto_servico}")
    _apresentar_contexto(briefing)
    _apresentar_subetapas(briefing)
    subetapa = st.radio(
        "Subetapa em preenchimento",
        (
            "Situação mercadológica e competitiva",
            "Objetivos declarados",
            "Praça e universo",
        ),
        horizontal=True,
    )
    if subetapa == "Situação mercadológica e competitiva":
        _formulario_situacao(aplicacao, id_campanha)
        _apresentar_registros(aplicacao, id_campanha, briefing)
    elif subetapa == "Objetivos declarados":
        apresentar_objetivos_declarados(aplicacao, id_campanha, briefing)
    else:
        apresentar_praca_universo(
            aplicacao,
            aplicacao_catalogo,
            id_campanha,
            briefing,
        )
