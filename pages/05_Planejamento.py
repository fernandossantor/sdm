import pandas as pd
import streamlit as st
from math import ceil

from application.services.briefing_service import (
    BriefingService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.context_service import (
    ContextService
)
from application.services.workflow_service import WorkflowService
from application.services.base_conhecimento_service import BaseConhecimentoService
from components.workflow_guard import exigir
from components.formatters import (
    dataframe_ptbr,
    moeda_ptbr,
    numero_ptbr,
    percentual_ptbr,
)
from components.page_config import PAGE_ICON, titulo_pagina
from components.inputs import entrada_monetaria
from components.grp_fields import render as render_grp
from components.schedule_visual import render as render_schedule
from application.services.identifier_service import IdentifierService


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Plano de Mídia"),

    page_icon=PAGE_ICON,

    layout="wide"

)

exigir("planejamento")

st.title("📋 Plano de Mídia")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

briefing_service = BriefingService()

workflow_service = WorkflowService()

base_conhecimento = BaseConhecimentoService()

with st.expander("Planos de mídia salvos", expanded=False):
    planos_salvos = planejamento.listar()
    if not planos_salvos:
        st.info("Nenhum planejamento salvo.")
    else:
        for registro in reversed(planos_salvos):
            c_nome, c_abrir, c_copia, c_excluir = st.columns([5, 1, 1, 1])
            c_nome.write(IdentifierService.rotulo(registro))
            if c_abrir.button("Abrir", key=f"abrir_plano_{registro['id']}"):
                st.session_state["plano"] = planejamento.restaurar(registro)
                st.session_state["configuracao_planejamento"] = registro.get(
                    "configuracao", {}
                )
                st.rerun()
            if c_copia.button("Duplicar", key=f"duplicar_plano_{registro['id']}"):
                planejamento.duplicar(registro)
                st.rerun()
            if c_excluir.button("Excluir", key=f"excluir_plano_{registro['id']}"):
                planejamento.excluir(registro["id"])
                st.rerun()


# ==========================================================
# ESCOLHA DO BRIEFING
# ==========================================================

tem_sessao = briefing_service.existe(

    st.session_state

)

briefings_salvos = contexto_service.listar_briefings()

opcoes = []

if tem_sessao:

    opcoes.append(

        "Briefing da Sessão"

    )

if briefings_salvos:

    opcoes.append(

        "Briefing Salvo"

    )

if not opcoes:

    st.warning(

        "Nenhum briefing disponível."

    )

    st.stop()

modo = st.radio(

    "Origem do Briefing",

    opcoes,

    horizontal=True

)


# ==========================================================
# BRIEFING DA SESSÃO
# ==========================================================

if modo == "Briefing da Sessão":

    briefing = briefing_service.recuperar(

        st.session_state

    )

    st.success(

        "Utilizando Briefing da Sessão."

    )

    st.info(

        f"""
**Cliente:** {briefing.cliente}

**Campanha:** {briefing.campanha}

**Objetivo:** {briefing.objetivo}

**KPI:** {briefing.kpi}

**Orçamento:** {moeda_ptbr(briefing.orcamento)}
"""
    )


# ==========================================================
# BRIEFING SALVO
# ==========================================================

else:

    briefing_salvo = st.selectbox(

        "Briefing",

        briefings_salvos,

        format_func=lambda item: item["nome"],

    )

    nome_briefing = briefing_salvo["nome"]
    briefing_salvo_obj = briefing_service.restaurar(briefing_salvo)

    st.success(

        "Utilizando Briefing salvo."

    )


# ==========================================================
# CONFIGURAÇÃO DO PLANEJAMENTO
# ==========================================================

st.divider()
st.subheader("Configuração do planejamento")

st.markdown("#### Critérios estratégicos")
st.caption(
    "Os pesos são explícitos e podem ser alterados. Eles orientam a proposta; "
    "quantidades, preços e restrições determinam a alocação final."
)
p1, p2, p3, p4, p5 = st.columns(5)
peso_objetivo = p1.number_input("Objetivo/OKR (%)", 0.0, 100.0, 40.0, format="%.2f")
peso_kpi = p2.number_input("KPI (%)", 0.0, 100.0, 30.0, format="%.2f")
peso_publico = p3.number_input("Público e jornada (%)", 0.0, 100.0, 20.0, format="%.2f")
peso_metricas = p4.number_input("Qualidade das métricas (%)", 0.0, 100.0, 10.0, format="%.2f")
peso_mcp = p5.number_input("Influência do MCP (%)", 0.0, 100.0, 20.0, format="%.2f")
soma_pesos = peso_objetivo + peso_kpi + peso_publico + peso_metricas
impedimentos_geracao = []
if soma_pesos != 100:
    st.error(
        "Os quatro pesos estratégicos devem somar 100,00% "
        f"(atual: {percentual_ptbr(soma_pesos)})."
    )
    impedimentos_geracao.append(
        "Ajuste os quatro pesos estratégicos para totalizar 100,00% "
        f"(atual: {percentual_ptbr(soma_pesos)})."
    )

if modo == "Briefing da Sessão":
    orcamento_inicial = float(briefing.orcamento)
    kpi_inicial = briefing.kpi
    flight_inicial = briefing.tipo_flight
    frequencia_alvo_inicial = briefing.frequencia_alvo or 5
    alcance_percentual_inicial = briefing.alcance_percentual or 60
    grp_inicial = briefing.grp or alcance_percentual_inicial * frequencia_alvo_inicial
else:
    orcamento_inicial = float(briefing_salvo.get("orcamento", 0))
    kpi_inicial = briefing_salvo.get("kpi")
    flight_inicial = briefing_salvo.get("tipo_flight", "LINEAR")
    frequencia_alvo_inicial = float(briefing_salvo.get("frequencia_alvo", 5))
    alcance_percentual_inicial = float(
        briefing_salvo.get("alcance_percentual", 60)
    )
    grp_inicial = float(
        briefing_salvo.get("grp")
        or alcance_percentual_inicial * frequencia_alvo_inicial
    )

kpis_catalogo = base_conhecimento.kpis()
nomes_kpis = [item["nome"] for item in kpis_catalogo]
kpi_indice = nomes_kpis.index(kpi_inicial) if kpi_inicial in nomes_kpis else 0

c1, c2 = st.columns(2)

with c1:
    orcamento_plano = entrada_monetaria(
        "Orçamento do planejamento (R$)",
        orcamento_inicial,
        key="orcamento_planejamento_br",
        ajuda=(
            "Verba total disponível para este plano, no formato 1.000,00."
        ),
    )
    kpi_plano = st.selectbox("KPI principal", nomes_kpis, index=kpi_indice)
    reserva_testes = st.number_input(
        "Reserva para testes (%)", min_value=0.0, max_value=30.0,
        value=5.0, step=0.01, format="%.2f",
    )

with c2:
    flights = ["LINEAR", "ONDA", "CONCENTRADO"]
    flight_indice = flights.index(flight_inicial) if flight_inicial in flights else 0
    flight_plano = st.selectbox("Flight", flights, index=flight_indice)
st.markdown("#### Alcance, frequência média e GRP")
metricas_plano = render_grp(
    "planejamento_metricas",
    alcance=alcance_percentual_inicial,
    frequencia=frequencia_alvo_inicial,
    grp=grp_inicial,
)
frequencia_plano = metricas_plano["frequencia_objetivo"]
frequencia_alvo_plano = metricas_plano["frequencia_alvo"]
alcance_plano = metricas_plano["alcance_objetivo"]
alcance_percentual_plano = metricas_plano["alcance_percentual"]
grp_plano = metricas_plano["grp"]

configuracao = {
    "orcamento": float(orcamento_plano),
    "kpi": kpi_plano,
    "kpis": [{"nome": kpi_plano, "peso": 100}],
    "tipo_flight": flight_plano,
    "frequencia_objetivo": frequencia_plano,
    "frequencia_alvo": float(frequencia_alvo_plano),
    "alcance_objetivo": alcance_plano,
    "alcance_percentual": float(alcance_percentual_plano),
    "grp": float(grp_plano),
    "reserva_testes_percentual": float(reserva_testes),
}

campanha_ref = (
    f"sessao:{briefing.campanha}"
    if modo == "Briefing da Sessão"
    else f"briefing:{briefing_salvo.get('id')}"
)
inventarios_mcp = [
    item for item in base_conhecimento.inventarios_com_papeis(campanha_ref)
    if (item.get("classificacao") or {}).get("selecionado", True)
    and item.get("classificacao")
]
st.subheader("Papéis dos Meios aplicados antes da geração")
if not inventarios_mcp:
    st.warning(
        "Este briefing ainda não possui inventários selecionados no MCP Papéis."
    )
    st.page_link("pages/03_MCP_Papeis.py", label="Configurar MCP Papéis", icon="🧩")
else:
    inventarios_plano = st.multiselect(
        "Inventários que entrarão no plano",
        inventarios_mcp,
        default=inventarios_mcp,
        format_func=lambda item: (
            f"{item['nome']} — {item['classificacao'].get('papel', 'SEM PAPEL')}"
        ),
    )
    configuracao["inventarios_selecionados"] = [
        item["id"] for item in inventarios_plano
    ]
    if not inventarios_plano:
        impedimentos_geracao.append(
            "Selecione ao menos um inventário para entrar no plano."
        )

    st.markdown("#### Entrega, compra e premissas por inventário")
    st.info(
        "Audiência, alcance e frequência são obrigatórios. Valores sugeridos "
        "podem ser substituídos e ficam registrados somente neste plano."
    )
    premissas_inventarios = {}
    componentes_inventarios = {}
    premissas_validas = True
    investimento_proposto = 0.0
    briefing_previa = briefing if modo == "Briefing da Sessão" else briefing_salvo_obj
    try:
        ranking_previa = {
            item["inventario_id"]: item
            for item in planejamento.previsualizar(briefing_previa)
        }
    except Exception:
        ranking_previa = {}
    for ordem, item in enumerate(inventarios_plano):
        classificacao = item.get("classificacao") or {}
        previa = ranking_previa.get(item["id"], {})
        precos_item = base_conhecimento.precos_inventario(item["id"])
        preco_item = next((p for p in reversed(precos_item) if p.get("ativo", True)), {})
        preco_cadastrado_liquido = float(preco_item.get("valor_bruto") or 0) * (
            1 - float(preco_item.get("desconto_percentual") or 0) / 100
        )
        unidade_cadastrada = str(
            preco_item.get("unidade") or item.get("unidade_compra") or "Unidade"
        )
        medicoes_item = base_conhecimento.medicoes_inventario(item["id"])
        medicao_item = next((m for m in reversed(medicoes_item) if m.get("ativo", True)), {})
        with st.expander(item["nome"], expanded=True):
            preco_col, unidade_col = st.columns([2, 1])
            preco_liquido = entrada_monetaria(
                "Preço líquido por unidade (R$)",
                preco_cadastrado_liquido,
                key=f"preco_plano_br_{item['id']}",
                container=preco_col,
                ajuda=(
                    "Custo usado para calcular a compra deste plano. Pode ser "
                    "informado aqui mesmo quando o inventário não possui preço "
                    "cadastrado. Não é o valor de uma conversão."
                ),
            )
            unidade_preco = unidade_col.text_input(
                "Unidade de compra",
                value=unidade_cadastrada,
                key=f"unidade_preco_plano_{item['id']}",
            )
            quantidade_sugerida = (
                int(
                    ceil(
                        float(orcamento_plano) * (1 - reserva_testes / 100)
                        / max(len(inventarios_plano), 1)
                        / preco_liquido
                    )
                )
                if preco_liquido
                else 0
            )
            a, b, c, d = st.columns(4)
            audiencia_item = a.number_input(
                "Audiência por unidade (%)", min_value=0.0, max_value=100.0,
                value=float(medicao_item.get("audiencia_percentual") or 0), key=f"audiencia_plano_{item['id']}",
                step=0.01, format="%.2f",
            )
            alcance_item = b.number_input(
                "Alcance do meio (%)", min_value=0.0, max_value=100.0,
                value=float(medicao_item.get("alcance_percentual") or classificacao.get("cobertura") or 0),
                key=f"alcance_plano_{item['id']}",
                step=0.01, format="%.2f",
            )
            incremental_item = c.number_input(
                "Alcance incremental (%)", min_value=0.0, max_value=100.0,
                value=float(classificacao.get("cobertura") or 0) if ordem == 0 else 0.0,
                key=f"incremental_plano_{item['id']}",
                step=0.01, format="%.2f",
            )
            frequencia_item = d.number_input(
                "Frequência do meio", min_value=0, value=int(round(float(medicao_item.get("frequencia") or 0))), step=1,
                key=f"frequencia_plano_{item['id']}",
            )
            modo_calculo = st.radio(
                "Variável de decisão",
                ["Metas geram a quantidade", "Quantidade informa a entrega"],
                horizontal=True, key=f"modo_calculo_{item['id']}",
                help="No primeiro modo, alcance, frequência e audiência calculam a compra. No segundo, a compra recalcula frequência e GRP.",
            )
            if audiencia_item > 0 and alcance_item > 0 and frequencia_item > 0:
                if "mil impress" in unidade_preco.casefold() and getattr(briefing_previa, "publicos", None):
                    publico_base = planejamento.publico_referencia(briefing_previa.publicos)
                    quantidade_meta = publico_base * alcance_item / 100 * frequencia_item / 1000
                elif "impress" in unidade_preco.casefold() and getattr(briefing_previa, "publicos", None):
                    publico_base = planejamento.publico_referencia(briefing_previa.publicos)
                    quantidade_meta = publico_base * alcance_item / 100 * frequencia_item
                else:
                    quantidade_meta = float(ceil(alcance_item * frequencia_item / audiencia_item))
            else:
                quantidade_meta = quantidade_sugerida
            qmin_key = f"qmin_plano_{item['id']}"
            qmax_key = f"qmax_plano_{item['id']}"
            vmin_key = f"vmin_plano_br_{item['id']}"
            vmax_key = f"vmax_plano_br_{item['id']}"
            if st.button(
                "Restaurar restrições",
                key=f"restaurar_restricoes_{item['id']}",
                help="Zera pisos e tetos opcionais deste inventário.",
            ):
                st.session_state[qmin_key] = 0
                st.session_state[qmax_key] = 0
                st.session_state[vmin_key] = "0,00"
                st.session_state[vmax_key] = "0,00"

            st.markdown("**Restrições opcionais de compra**")
            r1, r2, r3, r4 = st.columns(4)
            quantidade_minima = r1.number_input(
                "Piso de quantidade", min_value=0, value=0, step=1,
                key=qmin_key,
                help=(
                    "Quantidade mínima. No cálculo automático, o plano eleva "
                    "a compra até este piso. Zero significa sem piso."
                ),
            )
            quantidade_maxima = r2.number_input(
                "Teto de quantidade", min_value=0, value=0, step=1,
                key=qmax_key,
                help="Quantidade máxima permitida. Zero significa sem teto.",
            )
            verba_minima = entrada_monetaria(
                "Piso de verba (R$)",
                0.0,
                key=vmin_key,
                container=r3,
                ajuda=(
                    "Investimento mínimo. No cálculo automático, a quantidade "
                    "é elevada até atingir este piso. Zero significa sem piso."
                ),
            )
            verba_maxima = entrada_monetaria(
                "Teto de verba (R$)",
                0.0,
                key=vmax_key,
                container=r4,
                ajuda="Investimento máximo permitido. Zero significa sem teto.",
            )

            quantidade_automatica = int(ceil(quantidade_meta))
            quantidade_automatica = max(
                quantidade_automatica, int(quantidade_minima)
            )
            if preco_liquido > 0 and verba_minima > 0:
                quantidade_automatica = max(
                    quantidade_automatica,
                    int(ceil(verba_minima / preco_liquido)),
                )

            e, f, g, h = st.columns(4)
            if modo_calculo == "Metas geram a quantidade":
                quantidade_item = quantidade_automatica
                e.metric("Quantidade calculada", numero_ptbr(quantidade_item))
                e.caption("Atualizada automaticamente pelas metas e pelos pisos.")
            else:
                quantidade_item = e.number_input(
                    "Quantidade de compra", min_value=0,
                    value=quantidade_sugerida,
                    step=1,
                    key=f"quantidade_manual_plano_{item['id']}",
                    help="Quantidade inteira definida manualmente para a compra.",
                )
            frequencia_maxima = f.number_input(
                "Frequência máxima", min_value=1, value=10, step=1,
                key=f"freq_max_plano_{item['id']}",
                help="Limite de frequência antes de sinalizar saturação.",
            )
            ctr_item = g.number_input(
                "CTR/resposta (%)", min_value=0.0, value=0.0, step=0.01, format="%.2f",
                key=f"ctr_plano_{item['id']}",
            )
            conversao_item = h.number_input(
                "Taxa de conversão (%)", min_value=0.0, value=0.0, step=0.01, format="%.2f",
                key=f"conversao_plano_{item['id']}",
            )
            valor_conversao = entrada_monetaria(
                "Valor por conversão (R$)",
                0.0,
                key=f"valor_conversao_plano_br_{item['id']}",
                ajuda=(
                    "Receita estimada gerada por uma conversão. É usada somente "
                    "para retorno e ROI; não representa o custo da mídia e pode "
                    "ficar em zero."
                ),
            )
            st.caption(
                f"Custo de mídia considerado: {moeda_ptbr(preco_liquido)} por "
                f"{unidade_preco} · proposta inicial: "
                f"{numero_ptbr(quantidade_sugerida)} unidades."
            )
            obrigatorio = st.checkbox(
                "Inventário obrigatório nesta versão", value=False,
                key=f"obrigatorio_plano_{item['id']}",
            )
            atualizar_cadastro = st.checkbox(
                "Salvar estes valores também nas medições do inventário",
                value=False, key=f"atualizar_medicao_{item['id']}",
            )
            cobertura_jornada = st.slider(
                "Cobertura dos pontos de contato da jornada (%)", 0.0, 100.0, 50.0,
                step=0.01, format="%.2f",
                key=f"jornada_plano_{item['id']}",
                help="Avalie a contribuição deste inventário às etapas da jornada do público.",
            )
            confianca = st.selectbox(
                "Natureza dos dados", ["INFORMADO", "MEDIDO", "ESTIMADO"],
                index=["INFORMADO", "MEDIDO", "ESTIMADO"].index(
                    medicao_item.get("confianca") if medicao_item.get("confianca") in {"INFORMADO", "MEDIDO", "ESTIMADO"} else "INFORMADO"
                ), key=f"confianca_plano_{item['id']}",
            )
            st.markdown("**Aderência estratégica — revise os valores sugeridos**")
            s1, s2, s3, s4 = st.columns(4)
            score_objetivo = s1.number_input(
                "Objetivo/OKR (%)", 0.0, 100.0, min(100.0, float(previa.get("objetivo") or 0)), format="%.2f",
                key=f"score_obj_{item['id']}",
            )
            score_kpi = s2.number_input(
                "KPI (%)", 0.0, 100.0, min(100.0, float(previa.get("kpi") or 0)), format="%.2f",
                key=f"score_kpi_{item['id']}",
            )
            score_publico = s3.number_input(
                "Público e jornada (%)", 0.0, 100.0, min(100.0, float(previa.get("audiencia") or 0)), format="%.2f",
                key=f"score_publico_{item['id']}",
            )
            score_metricas = s4.number_input(
                "Qualidade das métricas (%)", 0.0, 110.0, float(previa.get("metricas") or 0), format="%.2f",
                key=f"score_metricas_{item['id']}",
            )
        campos_ausentes = []
        if preco_liquido <= 0:
            campos_ausentes.append("preço líquido por unidade maior que R$ 0,00")
        if audiencia_item <= 0:
            campos_ausentes.append("audiência por unidade")
        if alcance_item <= 0:
            campos_ausentes.append("alcance do meio")
        if frequencia_item <= 0:
            campos_ausentes.append("frequência do meio")
        if campos_ausentes:
            premissas_validas = False
            impedimentos_geracao.append(
                f"{item['nome']}: informe " + ", ".join(campos_ausentes) + "."
            )
        investimento_item = quantidade_item * preco_liquido
        investimento_proposto += investimento_item
        limites_invalidos = []
        if quantidade_item < quantidade_minima:
            limites_invalidos.append(
                "quantidade abaixo do piso "
                f"({numero_ptbr(quantidade_item)} calculada; "
                f"{numero_ptbr(quantidade_minima)} mínima)"
            )
        if quantidade_maxima > 0 and quantidade_item > quantidade_maxima:
            limites_invalidos.append(
                "quantidade acima do teto "
                f"({numero_ptbr(quantidade_item)} calculada; "
                f"{numero_ptbr(quantidade_maxima)} máxima)"
            )
        if investimento_item < verba_minima:
            limites_invalidos.append(
                "verba abaixo do piso "
                f"({moeda_ptbr(investimento_item)} calculada; "
                f"{moeda_ptbr(verba_minima)} mínima)"
            )
        if verba_maxima > 0 and investimento_item > verba_maxima:
            limites_invalidos.append(
                "verba acima do teto "
                f"({moeda_ptbr(investimento_item)} calculada; "
                f"{moeda_ptbr(verba_maxima)} máxima)"
            )
        if limites_invalidos:
            premissas_validas = False
            impedimentos_geracao.append(
                f"{item['nome']}: corrija " + ", ".join(limites_invalidos) + "."
            )
        premissas_inventarios[item["id"]] = {
            "audiencia_percentual": audiencia_item,
            "alcance_percentual": alcance_item,
            "alcance_incremental": incremental_item,
            "frequencia": frequencia_item,
            "frequencia_maxima": frequencia_maxima,
            "quantidade": quantidade_item,
            "preco_unitario": preco_liquido,
            "unidade_compra": unidade_preco,
            "modo_calculo": "METAS" if modo_calculo == "Metas geram a quantidade" else "COMPRA",
            "quantidade_minima": quantidade_minima,
            "quantidade_maxima": quantidade_maxima or None,
            "verba_minima": verba_minima,
            "verba_maxima": verba_maxima or None,
            "obrigatorio": obrigatorio,
            "atualizar_cadastro": atualizar_cadastro,
            "ctr": ctr_item,
            "taxa_conversao": conversao_item,
            "valor_conversao": valor_conversao,
            "cobertura_jornada": cobertura_jornada,
            "confianca": confianca,
            "medicao_origem_id": medicao_item.get("id"),
            "fonte": medicao_item.get("fonte") or "Informado no plano",
        }
        componentes_inventarios[item["id"]] = {
            "objetivo": score_objetivo, "kpi": score_kpi,
            "audiencia": score_publico, "metricas": score_metricas,
        }
    configuracao["premissas_inventarios"] = premissas_inventarios
    configuracao["componentes_inventarios"] = componentes_inventarios
    limite_compra = float(orcamento_plano) * (1 - reserva_testes / 100)
    if investimento_proposto > limite_compra + 0.01:
        premissas_validas = False
        impedimentos_geracao.append(
            "Reduza a compra proposta para que ela não ultrapasse a verba "
            "disponível após a reserva para testes."
        )
        st.error(
            f"A compra proposta ({moeda_ptbr(investimento_proposto)}) excede "
            f"a verba disponível após a reserva ({moeda_ptbr(limite_compra)})."
        )
    else:
        st.caption(
            f"Compra proposta: {moeda_ptbr(investimento_proposto)} · "
            f"saldo não alocado: {moeda_ptbr(limite_compra - investimento_proposto)}."
        )

configuracao["estrategia"] = {
    "pesos": {
        "objetivo": peso_objetivo, "kpi": peso_kpi,
        "audiencia": peso_publico, "metricas": peso_metricas,
    },
    "peso_mcp": peso_mcp,
}

if not inventarios_mcp:
    impedimentos_geracao.append(
        "Selecione e classifique ao menos um inventário no MCP Papéis."
    )
if orcamento_plano <= 0:
    impedimentos_geracao.append(
        "Informe um orçamento do planejamento maior que R$ 0,00."
    )


st.divider()

if impedimentos_geracao:
    st.warning(
        "**Para habilitar Gerar Plano:**\n\n"
        + "\n".join(f"- {motivo}" for motivo in impedimentos_geracao)
    )

geracao_bloqueada = bool(impedimentos_geracao)

gerar = st.button(

    "Gerar Plano",

    type="primary",

    width="stretch",
    disabled=geracao_bloqueada,

)


# ==========================================================
# GERAÇÃO
# ==========================================================

if gerar:

    with st.spinner(

        "Gerando plano..."

    ):

        if modo == "Briefing da Sessão":

            plano = planejamento.gerar(

                briefing=briefing,

                configuracao=configuracao,

            )

        else:

            plano = planejamento.gerar(
                briefing=briefing_salvo_obj,
                configuracao=configuracao,
            )

    if modo == "Briefing Salvo":
        workflow_service.registrar_briefing(st.session_state, nome_briefing)

    for inventario_id, premissa in configuracao.get("premissas_inventarios", {}).items():
        if premissa.get("atualizar_cadastro"):
            base_conhecimento.salvar_medicao_inventario({
                "inventario_id": inventario_id,
                "tipo_original": "Premissa validada no Plano de Mídia",
                "valor_original": premissa["audiencia_percentual"],
                "unidade_original": "% do público-alvo",
                "audiencia_percentual": premissa["audiencia_percentual"],
                "alcance_percentual": premissa["alcance_percentual"],
                "frequencia": premissa["frequencia"],
                "fonte": "Planejador — Plano de Mídia",
                "metodologia": "Valor revisado e confirmado na configuração do plano.",
                "confianca": premissa["confianca"], "ativo": True,
            })

    workflow_service.concluir(st.session_state, "planejamento", plano)

    st.session_state["configuracao_planejamento"] = configuracao


# ==========================================================
# EXIBIÇÃO
# ==========================================================

if "plano" in st.session_state:

    plano = st.session_state["plano"]

    with st.expander("Salvar planejamento", expanded=False):
        nome_plano = st.text_input(
            "Nome do planejamento",
            value=f"{plano.campanha} — {flight_plano.title()}",
        )
        if st.button("Salvar planejamento", type="primary"):
            resposta = planejamento.salvar(
                nome_plano,
                plano,
                st.session_state.get("configuracao_planejamento", configuracao),
                briefing_id=st.session_state.get("briefing_id"),
            )
            if getattr(resposta, "data", None):
                st.session_state["planejamento_id"] = resposta.data[0]["id"]
            st.success("Plano de Mídia salvo.")

    abas = st.tabs(

        [

            "🎯 Estratégia",

            "📊 Resumo",

            "💬 Justificativas"

            ,"🗓️ Cronograma"

        ]

    )

    with abas[0]:

        df = pd.DataFrame(

            [

                {

                    "Papel": i.papel,
                    "Score do papel": (
                        i.score_mcp if i.score_mcp is not None else i.score
                    ),
                    "Flight": plano.tipo_flight.title(),
                    "Frequência do meio": i.frequencia,
                    "Alcance do meio (%)": i.alcance_percentual,
                    "Alcance incremental (%)": i.alcance_incremental,
                    "Inventário": i.inventario,
                    "Plataforma": i.plataforma,
                    "Ambiente": i.ambiente,
                    "Verba": i.verba,
                    "GRP do meio": i.grp,
                    "Score estratégico": i.score,
                    "Participação da verba (%)": i.percentual,
                    "Preço unitário": i.preco_unitario,
                    "Unidade de compra": i.unidade_compra,
                    "Quantidade comprada": i.quantidade_estimada,
                    "Impressões estimadas": i.impressoes_estimadas,
                    "Alcance estimado (pessoas)": i.alcance_estimado,
                    "CPP": i.cpp,
                    "CPM": i.cpm,
                    "Cliques projetados": i.cliques_estimados,
                    "Conversões projetadas": i.conversoes_estimadas,
                    "Retorno projetado": i.retorno_estimado,
                    "ROI": i.roi,
                    "Excesso de frequência": i.excesso_frequencia,
                    "Aderência ao objetivo": i.objetivo_score,
                    "Aderência aos KPIs": i.kpi_score,
                    "Aderência ao público": i.audiencia_score,
                    "Qualidade das métricas": i.metricas_score,

                }

                for i in plano.itens

            ]

        )

        st.dataframe(

            dataframe_ptbr(
                df,
                moedas=["Verba", "Preço unitário"],
                percentuais=[
                    "Alcance do meio (%)", "Alcance incremental (%)",
                    "Participação da verba (%)",
                ],
                inteiros=[
                    "Quantidade comprada", "Impressões estimadas",
                    "Alcance estimado (pessoas)", "Cliques projetados",
                    "Conversões projetadas",
                ],
                decimais=[
                    "Score do papel", "Frequência do meio", "GRP do meio",
                    "Score estratégico",
                    "Aderência ao objetivo", "Aderência aos KPIs",
                    "Aderência ao público", "Qualidade das métricas",
                ],
            ),

            hide_index=True,

            width="stretch",

        )

        with st.expander("Como interpretar e calcular as colunas"):
            st.markdown(
                """
- **Índice de adequação MCP:** afinidade editorial, consumo e cobertura configurados em Papéis dos Meios. Não determina sozinho a verba.
- **Aderência estratégica:** combinação auditável dos pesos de objetivo/OKR, KPI, público/jornada e qualidade das métricas definidos acima.
- **Participação da verba:** consequência da quantidade comprada e do preço líquido, normalizada sobre o investimento calculado.
- **Unidade de compra:** unidade comercial cadastrada no preço do inventário.
- **Quantidade comprada:** decisão configurável do planejador; custo = quantidade × preço para unidades discretas.
- **Alcance incremental:** contribuição deduplicada informada; quando ausente, o motor identifica a estimativa por independência.
- **CPP:** investimento dividido pelo GRP entregue. CTR, conversão, retorno e ROI usam somente as premissas registradas no plano.
"""
            )

    with abas[1]:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Inventários",

            len(plano.itens)

        )

        c2.metric(

            "Principais",

            plano.principal

        )

        c3.metric(

            "Complementares",

            plano.complementar

        )

        c4.metric(

            "Verba (R$)",

            moeda_ptbr(plano.verba_total)

        )

        st.subheader("Metas de exposição da campanha")
        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("Faixa", plano.alcance_objetivo.title())
        a2.metric("Meta (%)", percentual_ptbr(plano.alcance_percentual))
        a3.metric("Frequência média", numero_ptbr(plano.frequencia_alvo, 2))
        a4.metric("GRP", numero_ptbr(plano.grp, 2))
        a5.metric(
            "Alcance projetado",
            numero_ptbr(plano.alcance_projetado),
            delta=(
                f"{plano.alcance_projetado - plano.alcance_meta:+,} vs. meta"
                if plano.alcance_meta > 0
                else None
            ),
        )
        if plano.publico_referencia <= 0:
            st.info(
                "Cadastre população nos Segmentos do Público para converter "
                "a meta percentual em pessoas."
            )
        else:
            st.caption(
                f"Público de referência: {numero_ptbr(plano.publico_referencia)} · "
                f"Meta de alcance: {numero_ptbr(plano.alcance_meta)} pessoas."
            )

        st.divider()

        st.write(

            f"**Cliente:** {plano.cliente}"

        )

        st.write(

            f"**Campanha:** {plano.campanha}"

        )

        st.write(

            f"**Objetivo:** {plano.objetivo}"

        )

    with abas[2]:

        for item in plano.itens:

            with st.expander(

                item.inventario

            ):

                for texto in item.justificativas:

                    st.markdown(

                        f"- {texto}"

                    )

    with abas[3]:
        st.write(f"**Flight:** {plano.tipo_flight.title()}")
        st.write(
            f"**Frequência:** {plano.frequencia_objetivo.title()} "
            f"({plano.frequencia_alvo})"
        )
        st.write(
            f"**Alcance:** {plano.alcance_objetivo.title()} "
            f"({percentual_ptbr(plano.alcance_percentual)} do público; meta de "
            f"{numero_ptbr(plano.alcance_meta)} pessoas)"
        )
        st.write(f"**GRP:** {numero_ptbr(plano.grp, 2)}")
        render_schedule(plano)
