"""Tela única da primeira fatia vertical de Tradução Estratégica."""

from datetime import date
from decimal import Decimal

import streamlit as st

from presentation.traducao_vertical_presenter import apresentar_contrato, comparar_contratos
from src.application.traducao_vertical import EntradaTraducaoVertical, ExecutarTraducaoVertical


MARKETING = ("aumento de vendas", "crescimento")
COMUNICACAO = ("intenção", "redução de incerteza", "notoriedade")


def _campanha_minima():
    st.subheader("1. Contexto e decisões")
    campanhas = st.session_state.setdefault("traducao_vertical_campanhas", [])
    campanha = None
    if campanhas:
        opcoes = {item["nome"]: item for item in campanhas}
        campanha = opcoes[st.selectbox("Campanha em análise", tuple(opcoes))]
    else:
        st.info("Crie a campanha mínima para iniciar a análise.")
    with st.expander("Criar outra campanha", expanded=not campanhas):
        with st.form("campanha_vertical"):
            nome = st.text_input("Nome da campanha", "Lume Casa — Primavera 2026")
            marca = st.text_input("Marca", "Lume Casa")
            produto = st.text_input("Produto ou serviço", "assinatura de energia solar residencial")
            criar = st.form_submit_button("Criar e abrir campanha", type="primary")
        if criar:
            if not nome.strip() or not marca.strip() or not produto.strip():
                st.error("Preencha nome, marca e produto ou serviço.")
            else:
                campanhas.append({"id": f"campanha-{len(campanhas) + 1}", "nome": nome.strip(), "marca": marca.strip(), "produto": produto.strip()})
                st.rerun()
    return campanha


def _decisoes(campanha, numero_versao):
    with st.form("decisoes_vertical"):
        situacao = st.text_area("Situação da marca e do mercado", "Notoriedade alta, baixa conclusão e receio sobre economia e retorno.")
        esquerda, direita = st.columns(2)
        with esquerda:
            marketing = st.multiselect("Resultados de Marketing prioritários", MARKETING, default=MARKETING)
            publico = st.text_input("Público prioritário", "Responsáveis pela decisão de energia residencial")
            segmento = st.text_input("Segmento secundário", "Interessados sem pesquisa recente")
            praca = st.text_input("Praça", "Campinas (SP)")
            jornada = st.selectbox("Momento da decisão", ("consideração para intenção", "descoberta"))
        with direita:
            comunicacao = st.multiselect("Resultados de comunicação a avaliar", COMUNICACAO, default=COMUNICACAO)
            inicio = st.date_input("Início", date(2026, 9, 1))
            fim = st.date_input("Fim", date(2026, 10, 31))
            verba = st.number_input("Verba disponível (BRL)", min_value=0.0, value=300000.0)
            prioridade = st.selectbox("Prioridade da campanha", ("muito alta", "alta", "média"))
        restricao = st.text_input("Restrição principal", "A verba total não pode ultrapassar BRL 300.000.")
        tensao = st.text_input("Tensão estratégica", "Aumento de vendas e crescimento disputam a verba rígida.")
        st.caption("Indicadores disponíveis — desmarque quando o dado estiver ausente")
        indicador_a, indicador_b = st.columns(2)
        with indicador_a:
            tem_notoriedade = st.checkbox("Há dado de notoriedade", value=True)
            notoriedade = st.number_input("Notoriedade auxiliada (%)", 0.0, 100.0, 78.0, disabled=not tem_notoriedade)
        with indicador_b:
            tem_conclusao = st.checkbox("Há dado de conclusão", value=True)
            conclusao = st.number_input("Conclusão do pedido de proposta (%)", 0.0, 100.0, 1.1, disabled=not tem_conclusao)
        pressao = st.slider("Pressão competitiva", 0, 100, 35)
        cobertura = st.slider("Quanto da necessidade estimada a verba cobre", 0, 100, 60, format="%d%%")
        observacao = st.text_input("Observação de apoio (não altera a pontuação)")
        executar = st.form_submit_button("Executar tradução", type="primary")
    if not executar:
        return None
    if not marketing or not comunicacao:
        st.error("Informe ao menos um resultado de Marketing e um de comunicação.")
        return None
    return EntradaTraducaoVertical(
        id_comando=f"tela-{campanha['id']}-v{numero_versao}", campanha_id=campanha["id"],
        campanha_nome=campanha["nome"], marca=campanha["marca"], produto_ou_servico=campanha["produto"],
        situacao_marca_mercado=situacao, objetivos_marketing=tuple(marketing),
        objetivos_comunicacao_candidatos=tuple(comunicacao), publico_prioritario=publico,
        segmento_secundario=segmento, praca=praca, data_inicial=inicio, data_final=fim,
        verba=Decimal(str(verba)), prioridade=prioridade, restricao=restricao,
        tensao_estrategica=tensao,
        notoriedade_auxiliada=Decimal(str(notoriedade)) if tem_notoriedade else None,
        taxa_conclusao_proposta=Decimal(str(conclusao)) if tem_conclusao else None,
        pressao_competitiva=float(pressao), verba_disponivel_percentual_do_necessario=float(cobertura),
        jornada=jornada, observacao_nao_decisoria=observacao or None,
    )


def _resultado(apresentacao):
    st.subheader("2. Resultado estratégico")
    estado, confianca = st.columns(2)
    estado.metric("Estado do contrato", apresentacao.estado)
    confianca.metric("Confiança", apresentacao.confianca)
    st.markdown("#### Prioridades de comunicação")
    st.dataframe(apresentacao.comunicacao, hide_index=True, use_container_width=True)
    st.markdown("#### Objetivos de mídia")
    st.dataframe(apresentacao.midia, hide_index=True, use_container_width=True)
    st.markdown("#### Restrições e tensões")
    for texto in apresentacao.restricoes + apresentacao.tensoes:
        st.write(f"• {texto}")
    st.subheader("3. Explicação e alertas")
    for texto in apresentacao.explicacoes:
        st.info(texto)
    for alerta in apresentacao.alertas:
        st.warning(alerta)
    if not apresentacao.alertas:
        st.success("Nenhuma ressalva foi registrada nesta versão.")


def renderizar_traducao_vertical() -> None:
    st.title("Tradução estratégica")
    st.write("Converta decisões do briefing em prioridades de comunicação e objetivos de mídia, sem selecionar canais ou distribuir verba.")
    campanha = _campanha_minima()
    if campanha is None:
        return
    chave = f"traducao_vertical_versoes_{campanha['id']}"
    versoes = st.session_state.setdefault(chave, [])
    entrada = _decisoes(campanha, len(versoes) + 1)
    if entrada:
        try:
            versoes.append(apresentar_contrato(ExecutarTraducaoVertical().executar(entrada)))
        except ValueError as exc:
            st.error(f"Revise as decisões informadas: {exc}")
    if versoes:
        _resultado(versoes[-1])
        st.caption("Altere uma decisão acima e execute novamente para gerar nova versão.")
    if len(versoes) >= 2:
        st.markdown("#### Comparação entre as duas versões mais recentes")
        st.dataframe(comparar_contratos(versoes[-2], versoes[-1]), hide_index=True, use_container_width=True)
