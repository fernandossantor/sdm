from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
    PracaResumo,
    UniversoResumo,
)
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)


ERROS_CONTROLADOS = (LookupError, PermissionError, TypeError, ValueError)


def _possui_texto(valor: str | None) -> bool:
    return bool(valor and valor.strip())


def _rotulo_praca(praca: PracaResumo) -> str:
    rotulo = f"[{praca.rotulo_tipo}] {praca.nome}"
    if praca.codigo_oficial:
        rotulo += f" — {praca.codigo_oficial}"
    return rotulo


def _selecionar_unidade(
    aplicacao: AplicacaoBriefings,
    chave: str,
    permite_ausencia: bool,
) -> tuple[str | None, str | None]:
    catalogo = aplicacao.listar_unidades_populacionais()
    rotulos = tuple(item.rotulo for item in catalogo)
    opcoes = (() if not permite_ausencia else ("Não informar",))
    selecionada = st.selectbox(
        "Unidade populacional",
        opcoes + rotulos + ("Outra unidade",),
        key=f"unidade_{chave}",
    )
    if selecionada == "Não informar":
        return None, None
    if selecionada == "Outra unidade":
        return None, st.text_input(
            "Nome da unidade populacional",
            key=f"unidade_personalizada_{chave}",
        )
    definicao = next(item for item in catalogo if item.rotulo == selecionada)
    return definicao.codigo, definicao.rotulo


def _formulario_praca(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
) -> None:
    tipos = aplicacao.listar_tipos_praca()
    rotulos_tipos = tuple(item.rotulo for item in tipos)
    rotulo_tipo = st.selectbox("Tipo territorial", rotulos_tipos)
    tipo = next(item for item in tipos if item.rotulo == rotulo_tipo)
    st.caption(tipo.descricao)
    nome = st.text_input(
        "Nome da Praça",
        placeholder=(
            "Ex.: São Borja; Rio Grande do Sul; Bairro Centro; "
            "Fronteira Oeste."
        ),
    )
    codigo_oficial = st.text_input("Código oficial (opcional)")
    abrangencia = st.text_area("Descrição da abrangência (opcional)")
    valor = st.text_input(
        "População territorial de referência (opcional)",
        help=(
            "Informe apenas o valor numérico e use ponto como separador decimal."
        ),
    )
    codigo_unidade, unidade = _selecionar_unidade(aplicacao, "praca", True)
    fonte = st.text_input("Fonte (opcional)", key="fonte_praca")
    data_referencia = st.text_input(
        "Data ou período de referência (opcional)",
        key="data_praca",
    )
    observacao = st.text_area(
        "Observação complementar (opcional)",
        key="observacao_praca",
    )
    if st.button("Adicionar Praça"):
        entrada = AdicionarPracaEntrada(
            tipo=tipo.codigo,
            nome=nome,
            codigo_oficial=codigo_oficial,
            abrangencia=abrangencia,
            valor_populacao_referencia=valor,
            codigo_unidade_populacional=codigo_unidade,
            unidade_populacional=unidade,
            fonte=fonte,
            data_referencia=data_referencia,
            observacao=observacao,
        )
        try:
            aplicacao.adicionar_praca(id_campanha, entrada)
        except ERROS_CONTROLADOS as erro:
            st.error(str(erro))
        else:
            st.success("Praça adicionada.")
            st.rerun()


def _detalhar_praca(praca: PracaResumo) -> None:
    st.write(f"**{praca.nome}**")
    st.write(f"Tipo territorial: {praca.rotulo_tipo}")
    if _possui_texto(praca.codigo_oficial):
        st.write(f"Código oficial: {praca.codigo_oficial}")
    if _possui_texto(praca.abrangencia):
        st.write(f"Abrangência: {praca.abrangencia}")
    if praca.valor_populacao_referencia is not None:
        st.write(
            "População territorial de referência: "
            f"{praca.valor_populacao_referencia} {praca.unidade_populacional}"
        )
    if _possui_texto(praca.fonte):
        st.write(f"Fonte: {praca.fonte}")
    if _possui_texto(praca.data_referencia):
        st.write(f"Data de referência: {praca.data_referencia}")
    if _possui_texto(praca.observacao):
        st.write(f"Observação: {praca.observacao}")


def _listar_pracas(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    with st.expander(f"Praças salvas ({len(briefing.pracas)})", expanded=False):
        if not briefing.pracas:
            st.write("Nenhuma Praça cadastrada.")
        for praca in briefing.pracas:
            with st.container(border=True):
                _detalhar_praca(praca)
                if st.button(
                    "Remover Praça",
                    key=f"remover_praca_{praca.id_praca}",
                ):
                    try:
                        aplicacao.remover_praca(id_campanha, praca.id_praca)
                    except ERROS_CONTROLADOS as erro:
                        st.error(str(erro))
                    else:
                        st.rerun()


def _formulario_universo(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    if not briefing.pracas:
        st.info("Cadastre ao menos uma Praça antes de criar um Universo.")
        return
    pracas_por_id = {item.id_praca: item for item in briefing.pracas}
    nome = st.text_input("Nome do Universo")
    definicao = st.text_area(
        "Definição",
        help=(
            "Descreva objetivamente quem ou o que integra esta população de "
            "referência, sem transformá-la em público-alvo."
        ),
    )
    ids_pracas = st.multiselect(
        "Praças relacionadas",
        options=tuple(pracas_por_id),
        format_func=lambda id_praca: _rotulo_praca(pracas_por_id[id_praca]),
    )
    valor = st.text_input(
        "Tamanho estimado do Universo (opcional)",
        help=(
            "Informe apenas o valor numérico e use ponto como separador decimal."
        ),
    )
    codigo_unidade, unidade = _selecionar_unidade(aplicacao, "universo", False)
    fonte = st.text_input("Fonte (opcional)", key="fonte_universo")
    data_referencia = st.text_input(
        "Data ou período de referência (opcional)",
        key="data_universo",
    )
    criterios_inclusao = st.text_area("Critérios de inclusão (opcional)")
    criterios_exclusao = st.text_area("Critérios de exclusão (opcional)")
    observacao = st.text_area(
        "Observação complementar (opcional)",
        key="observacao_universo",
    )
    if st.button("Adicionar Universo"):
        entrada = AdicionarUniversoEntrada(
            nome=nome,
            definicao=definicao,
            ids_pracas=tuple(ids_pracas),
            valor_populacional=valor,
            codigo_unidade=codigo_unidade,
            unidade=unidade or "",
            fonte=fonte,
            data_referencia=data_referencia,
            criterios_inclusao=criterios_inclusao,
            criterios_exclusao=criterios_exclusao,
            observacao=observacao,
        )
        try:
            aplicacao.adicionar_universo(id_campanha, entrada)
        except ERROS_CONTROLADOS as erro:
            st.error(str(erro))
        else:
            st.success("Universo adicionado.")
            st.rerun()


def _detalhar_universo(universo: UniversoResumo) -> None:
    st.write(f"**{universo.nome}**")
    st.write(universo.definicao)
    st.write("Praças relacionadas: " + ", ".join(universo.rotulos_pracas))
    if universo.valor_populacional is not None:
        st.write(f"Tamanho estimado: {universo.valor_populacional} {universo.unidade}")
    else:
        st.write(f"Unidade populacional: {universo.unidade}")
    if _possui_texto(universo.fonte):
        st.write(f"Fonte: {universo.fonte}")
    if _possui_texto(universo.data_referencia):
        st.write(f"Data de referência: {universo.data_referencia}")
    if _possui_texto(universo.criterios_inclusao):
        st.write(f"Critérios de inclusão: {universo.criterios_inclusao}")
    if _possui_texto(universo.criterios_exclusao):
        st.write(f"Critérios de exclusão: {universo.criterios_exclusao}")
    if _possui_texto(universo.observacao):
        st.write(f"Observação: {universo.observacao}")


def _listar_universos(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    with st.expander(
        f"Universos salvos ({len(briefing.universos)})",
        expanded=False,
    ):
        if not briefing.universos:
            st.write("Nenhum Universo cadastrado.")
        for universo in briefing.universos:
            with st.container(border=True):
                _detalhar_universo(universo)
                if st.button(
                    "Remover Universo",
                    key=f"remover_universo_{universo.id_universo}",
                ):
                    try:
                        aplicacao.remover_universo(
                            id_campanha,
                            universo.id_universo,
                        )
                    except ERROS_CONTROLADOS as erro:
                        st.error(str(erro))
                    else:
                        st.rerun()


def apresentar_praca_universo(
    aplicacao: AplicacaoBriefings,
    id_campanha: UUID,
    briefing: BriefingResumo,
) -> None:
    st.subheader("Praça e universo")
    st.write(
        "A Praça delimita territorialmente o planejamento. O Universo "
        "representa a população de referência existente nas praças selecionadas."
    )
    st.caption(
        "Praça territorial não é Praça do composto de Marketing nem cobertura "
        "de mídia. Universo não é audiência, segmento ou público-alvo."
    )
    aba_pracas, aba_universos = st.tabs(("Praças", "Universos"))
    with aba_pracas:
        _formulario_praca(aplicacao, id_campanha)
        _listar_pracas(aplicacao, id_campanha, briefing)
    with aba_universos:
        _formulario_universo(aplicacao, id_campanha, briefing)
        _listar_universos(aplicacao, id_campanha, briefing)
