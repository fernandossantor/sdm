from uuid import UUID

import streamlit as st

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.periodo_verba import (
    IntervaloDeclaradoEntrada,
    SalvarPeriodoVerbaEntrada,
)
from mediad_planner.application.services.aplicacao_briefings import AplicacaoBriefings


def _linhas(valor: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in valor.splitlines() if item.strip())


def _intervalos(valor: str) -> tuple[IntervaloDeclaradoEntrada, ...]:
    resultado = []
    for numero, linha in enumerate(_linhas(valor), 1):
        partes = tuple(item.strip() for item in linha.split("|", 2))
        if len(partes) < 2:
            raise ValueError(
                f"Intervalo da linha {numero} deve usar início | fim | descrição"
            )
        resultado.append(
            IntervaloDeclaradoEntrada(
                partes[0], partes[1], partes[2] if len(partes) == 3 else None
            )
        )
    return tuple(resultado)


def _texto_intervalos(itens) -> str:
    return "\n".join(
        f"{item.data_inicial} | {item.data_final}"
        + (f" | {item.descricao}" if item.descricao else "")
        for item in itens
    )


def apresentar_periodo_verba(
    aplicacao: AplicacaoBriefings, id_campanha: UUID, briefing: BriefingResumo,
) -> None:
    st.subheader("Período pretendido e Verba")
    st.caption(
        "Registre as condições declaradas. Flight, distribuição e otimização "
        "da verba pertencem às etapas posteriores."
    )
    atual = briefing.periodo_verba
    periodo, verba = st.tabs(("Período pretendido", "Verba"))
    with periodo:
        data_inicial = st.text_input(
            "Data inicial pretendida (AAAA-MM-DD)",
            value=atual.data_inicial if atual and atual.data_inicial else "",
        )
        data_final = st.text_input(
            "Data final pretendida (AAAA-MM-DD)",
            value=atual.data_final if atual and atual.data_final else "",
        )
        duracao = st.text_input(
            "Duração declarada (opcional)",
            value=atual.duracao if atual and atual.duracao else "",
            help="Informe a duração como declarada, sem gerar flight.",
        )
        datas_criticas = st.text_area(
            "Datas críticas (uma data AAAA-MM-DD por linha)",
            value="\n".join(atual.datas_criticas) if atual else "",
        )
        sazonalidades = st.text_area(
            "Sazonalidades (uma por linha)",
            value="\n".join(atual.sazonalidades) if atual else "",
        )
        eventos = st.text_area(
            "Eventos condicionantes (um por linha)",
            value="\n".join(atual.eventos_condicionantes) if atual else "",
        )
        obrigatorios = st.text_area(
            "Períodos obrigatórios",
            value=_texto_intervalos(atual.periodos_obrigatorios) if atual else "",
            help="Uma linha por intervalo: início | fim | descrição opcional.",
        )
        vedados = st.text_area(
            "Períodos vedados",
            value=_texto_intervalos(atual.periodos_vedados) if atual else "",
            help="Uma linha por intervalo: início | fim | descrição opcional.",
        )
        observacao_periodo = st.text_area(
            "Observação complementar do Período (opcional)",
            value=atual.observacao_periodo if atual and atual.observacao_periodo else "",
        )
    with verba:
        naturezas = aplicacao.listar_naturezas_limite_verba()
        codigos = {item.rotulo: item.codigo for item in naturezas}
        rotulos = tuple(codigos)
        natureza_atual = atual.rotulo_natureza_limite if atual else "Ainda não definido"
        valor_total = st.text_input(
            "Valor total disponível (opcional)",
            value=atual.valor_total if atual and atual.valor_total else "",
        )
        moeda = st.text_input(
            "Moeda (opcional)",
            value=atual.moeda if atual and atual.moeda else "",
            placeholder="Ex.: BRL",
        )
        natureza = st.selectbox(
            "Natureza do limite", rotulos, index=rotulos.index(natureza_atual)
        )
        margem = st.text_input(
            "Margem de flexibilidade (opcional)",
            value=atual.margem_flexibilidade if atual and atual.margem_flexibilidade else "",
            help="Registre como declarada; não é convertida automaticamente em percentual.",
        )
        minimo = st.text_input(
            "Valor mínimo declarado (opcional)",
            value=atual.valor_minimo if atual and atual.valor_minimo else "",
        )
        maximo = st.text_input(
            "Valor máximo declarado (opcional)",
            value=atual.valor_maximo if atual and atual.valor_maximo else "",
        )
        comprometida = st.text_input(
            "Parcela já comprometida (opcional)",
            value=atual.parcela_comprometida if atual and atual.parcela_comprometida else "",
        )
        observacao_verba = st.text_area(
            "Observação complementar da Verba (opcional)",
            value=atual.observacao_verba if atual and atual.observacao_verba else "",
        )
    criar, editar = st.columns(2)
    criar_acionado = criar.button("Criar Período e Verba", disabled=atual is not None)
    editar_acionado = editar.button("Editar Período e Verba", disabled=atual is None)
    if criar_acionado or editar_acionado:
        try:
            entrada = SalvarPeriodoVerbaEntrada(
                data_inicial, data_final, duracao, _linhas(datas_criticas),
                _linhas(sazonalidades), _linhas(eventos), _intervalos(obrigatorios),
                _intervalos(vedados), observacao_periodo, valor_total, moeda,
                codigos[natureza], margem, minimo, maximo, comprometida,
                observacao_verba,
            )
            aplicacao.definir_periodo_verba(id_campanha, entrada)
        except (LookupError, PermissionError, TypeError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success("Período e Verba salvos.")
            st.rerun()
    if atual is not None:
        with st.expander("Resumo e diagnósticos", expanded=False):
            st.write(f"Período: {atual.data_inicial or 'não definido'} a {atual.data_final or 'não definido'}")
            st.write(f"Verba total: {atual.moeda or 'moeda não informada'} {atual.valor_total or 'não definida'}")
            if atual.diagnosticos:
                for diagnostico in atual.diagnosticos:
                    st.warning(diagnostico)
            else:
                st.success("Nenhuma incoerência automática identificada.")
