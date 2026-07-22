import pandas as pd
import streamlit as st

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
from components.formatters import dataframe_ptbr, moeda_ptbr, numero_ptbr
from components.grp_fields import render as render_grp
from components.schedule_editor import render as render_schedule


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Plano de Mídia",

    page_icon="📋",

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
            c_nome, c_abrir, c_excluir = st.columns([5, 1, 1])
            c_nome.write(registro["nome"])
            if c_abrir.button("Abrir", key=f"abrir_plano_{registro['id']}"):
                st.session_state["plano"] = planejamento.restaurar(registro)
                st.session_state["configuracao_planejamento"] = registro.get(
                    "configuracao", {}
                )
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
    orcamento_plano = st.number_input(
        "Orçamento do planejamento",
        min_value=0.0,
        value=orcamento_inicial,
        step=1000.0,
    )
    kpi_plano = st.selectbox("KPI principal", nomes_kpis, index=kpi_indice)

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


st.divider()

gerar = st.button(

    "Gerar Plano",

    type="primary",

    width="stretch",
    disabled=not inventarios_mcp,

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
            planejamento.salvar(
                nome_plano,
                plano,
                st.session_state.get("configuracao_planejamento", configuracao),
            )
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
                    "Frequência média": plano.frequencia_alvo,
                    "Alcance (%)": plano.alcance_percentual,
                    "Inventário": i.inventario,
                    "Plataforma": i.plataforma,
                    "Ambiente": i.ambiente,
                    "Verba": i.verba,
                    "GRP": plano.grp,
                    "Score estratégico": i.score,
                    "Participação da verba (%)": i.percentual,
                    "Preço unitário": i.preco_unitario,
                    "Unidade de compra": i.unidade_compra,
                    "Quantidade comprada": i.quantidade_estimada,
                    "Impressões estimadas": i.impressoes_estimadas,
                    "Alcance estimado (pessoas)": i.alcance_estimado,
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
                percentuais=["Alcance (%)", "Participação da verba (%)"],
                inteiros=["Impressões estimadas", "Alcance estimado (pessoas)"],
                decimais=[
                    "Score do papel", "Frequência média", "GRP",
                    "Score estratégico", "Quantidade comprada",
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
- **Score do papel:** adequação do MCP, calculada por 40% de afinidade editorial, 35% de consumo e 25% de cobertura. O papel decorre da posição no ranking desse score.
- **Score estratégico:** aderência usada na distribuição da verba. Combina objetivo (40%), KPI (30%), público (20%) e qualidade das métricas (10%); quando há MCP, recebe 80% desse resultado e 20% do Score do papel.
- **Participação da verba:** proporção do orçamento após ponderar o Score estratégico pelo papel (Principal 1,20; Complementar 1,00; Apoio 0,80; Opcional 0,50), aplicar limites e normalizar para 100%.
- **Unidade de compra:** unidade comercial cadastrada no preço do inventário.
- **Quantidade comprada:** verba dividida pelo preço líquido unitário.
- **Impressões estimadas:** calculadas apenas para unidades de impressão; em “Mil impressões”, quantidade × 1.000.
- **Alcance estimado:** impressões ou contatos divididos pela frequência média. Sem base compatível, o campo fica em branco.
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

            "Verba",

            moeda_ptbr(plano.verba_total)

        )

        st.subheader("Metas de exposição da campanha")
        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("Faixa", plano.alcance_objetivo.title())
        a2.metric("Meta", f"{plano.alcance_percentual}%")
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
            f"({plano.alcance_percentual}% do público; meta de "
            f"{numero_ptbr(plano.alcance_meta)} pessoas)"
        )
        st.write(f"**GRP:** {numero_ptbr(plano.grp, 2)}")
        if render_schedule(plano, "cronograma_no_plano"):
            st.session_state["plano"] = plano
            st.success("Cronograma incorporado ao plano. Salve o planejamento para persistir.")
