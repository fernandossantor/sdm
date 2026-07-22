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


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Planejamento",

    page_icon="📋",

    layout="wide"

)

exigir("planejamento")

st.title("📋 Planejamento Estratégico")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

briefing_service = BriefingService()

workflow_service = WorkflowService()

base_conhecimento = BaseConhecimentoService()

with st.expander("Planejamentos salvos", expanded=False):
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

**Orçamento:** R$ {briefing.orcamento:,.2f}
"""
    )


# ==========================================================
# BRIEFING SALVO
# ==========================================================

else:

    nomes = [

        b["nome"]

        for b in briefings_salvos

    ]

    nome_briefing = st.selectbox(

        "Briefing",

        nomes

    )

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
    frequencia_inicial = briefing.frequencia_objetivo or "MEDIA"
    frequencia_alvo_inicial = briefing.frequencia_alvo or 5
    alcance_inicial = briefing.alcance_objetivo or "MEDIO"
    alcance_percentual_inicial = briefing.alcance_percentual or 60
else:
    briefing_salvo = next(item for item in briefings_salvos if item["nome"] == nome_briefing)
    orcamento_inicial = float(briefing_salvo.get("orcamento", 0))
    kpi_inicial = briefing_salvo.get("kpi")
    flight_inicial = briefing_salvo.get("tipo_flight", "LINEAR")
    frequencia_inicial = briefing_salvo.get("frequencia_objetivo", "MEDIA")
    frequencia_alvo_inicial = int(briefing_salvo.get("frequencia_alvo", 5))
    alcance_inicial = briefing_salvo.get("alcance_objetivo", "MEDIO")
    alcance_percentual_inicial = int(
        briefing_salvo.get("alcance_percentual", 60)
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
    frequencia_plano = st.selectbox(
        "Faixa de frequência",
        ["BAIXA", "MEDIA", "ALTA"],
        index={"BAIXA": 0, "MEDIA": 1, "ALTA": 2}.get(frequencia_inicial, 1),
        format_func=lambda valor: {
            "BAIXA": "Baixa (1–3)",
            "MEDIA": "Média (4–7)",
            "ALTA": "Alta (8+)",
        }[valor],
    )

limites = {"BAIXA": (1, 3, 2), "MEDIA": (4, 7, 5), "ALTA": (8, 30, 8)}
freq_min, freq_max, freq_padrao = limites[frequencia_plano]
valor_frequencia = frequencia_alvo_inicial
if not freq_min <= valor_frequencia <= freq_max:
    valor_frequencia = freq_padrao

frequencia_alvo_plano = st.number_input(
    "Frequência alvo",
    min_value=freq_min,
    max_value=freq_max,
    value=valor_frequencia,
)

c_alcance_faixa, c_alcance_percentual = st.columns(2)
with c_alcance_faixa:
    alcance_plano = st.selectbox(
        "Faixa de alcance",
        ["BAIXO", "MEDIO", "ALTO"],
        index={"BAIXO": 0, "MEDIO": 1, "ALTO": 2}.get(alcance_inicial, 1),
        format_func=lambda valor: {
            "BAIXO": "Baixo (até 50% do público)",
            "MEDIO": "Médio (51% a 69% do público)",
            "ALTO": "Alto (70% a 100% do público)",
        }[valor],
    )

limites_alcance = {
    "BAIXO": (0, 50, 40),
    "MEDIO": (51, 69, 60),
    "ALTO": (70, 100, 80),
}
alcance_min, alcance_max, alcance_padrao = limites_alcance[alcance_plano]
valor_alcance = alcance_percentual_inicial
if not alcance_min <= valor_alcance <= alcance_max:
    valor_alcance = alcance_padrao

with c_alcance_percentual:
    alcance_percentual_plano = st.number_input(
        "Percentual de alcance desejado",
        min_value=alcance_min,
        max_value=alcance_max,
        value=valor_alcance,
        format="%d%%",
    )

configuracao = {
    "orcamento": float(orcamento_plano),
    "kpi": kpi_plano,
    "kpis": [{"nome": kpi_plano, "peso": 100}],
    "tipo_flight": flight_plano,
    "frequencia_objetivo": frequencia_plano,
    "frequencia_alvo": int(frequencia_alvo_plano),
    "alcance_objetivo": alcance_plano,
    "alcance_percentual": int(alcance_percentual_plano),
}


st.divider()

gerar = st.button(

    "Gerar Plano",

    type="primary",

    width="stretch"

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

                nome_briefing=nome_briefing,

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
            st.success("Planejamento salvo.")

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

                    "Inventário": i.inventario,

                    "Plataforma": i.plataforma,

                    "Ambiente": i.ambiente,

                    "Papel": i.papel,

                    "Score": i.score,

                    "Score MCP": i.score_mcp or None,

                    "Percentual": i.percentual,

                    "Verba": i.verba

                    ,"Preço unitário": i.preco_unitario

                    ,"Unidade": i.unidade_compra

                    ,"Quantidade estimada": i.quantidade_estimada

                    ,"Alcance estimado": i.alcance_estimado

                }

                for i in plano.itens

            ]

        )

        df_editado = st.data_editor(

            df,

            hide_index=True,

            width="stretch",

            disabled=[
                coluna
                for coluna in df.columns
                if coluna != "Papel"
            ],

            column_config={
                "Papel": st.column_config.SelectboxColumn(
                    "Papel",
                    options=["PRINCIPAL", "COMPLEMENTAR", "APOIO", "OPCIONAL"],
                    required=True,
                )
            },

            key="editor_papeis_planejamento",

        )

        if st.button("Aplicar papéis de mídia"):
            papeis = dict(zip(df_editado["Inventário"], df_editado["Papel"]))
            for item in plano.itens:
                item.papel = papeis[item.inventario]
            st.success("Papéis de mídia atualizados no planejamento.")

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

            f"R$ {plano.verba_total:,.2f}"

        )

        st.subheader("Meta de alcance da campanha")
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Faixa", plano.alcance_objetivo.title())
        a2.metric("Meta", f"{plano.alcance_percentual}%")
        a3.metric("Público estimado", f"{plano.publico_referencia:,}")
        a4.metric(
            "Alcance projetado",
            f"{plano.alcance_projetado:,}",
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
            f"{plano.alcance_meta:,} pessoas)"
        )
        if plano.cronograma:
            st.dataframe(pd.DataFrame(plano.cronograma), hide_index=True)
        else:
            st.info("Defina as datas do briefing para gerar o cronograma semanal.")
