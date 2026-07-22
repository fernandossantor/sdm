import pandas as pd
import streamlit as st

from application.services.base_conhecimento_service import BaseConhecimentoService
from application.services.briefing_service import BriefingService
from application.services.context_service import ContextService
from application.services.classificacao_papeis_service import ClassificacaoPapeisService
from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir


st.set_page_config(page_title="MCP — Papéis de mídia", page_icon="🧩", layout="wide")
exigir("mcp_papeis")
st.title("🧩 Papéis de mídia da campanha")

base = BaseConhecimentoService()
classificador = ClassificacaoPapeisService()
briefing = BriefingService().recuperar(st.session_state)
origens = [
    {
        "rotulo": f"Sessão — {briefing.campanha}",
        "campanha": briefing.campanha,
        "ref": f"sessao:{briefing.campanha}",
    }
]
for salvo in ContextService().listar_briefings():
    origens.append(
        {
            "rotulo": f"Salvo — {salvo['nome']}",
            "campanha": salvo["nome"],
            "ref": f"briefing:{salvo['id']}",
        }
    )
origem = st.selectbox(
    "Campanha / briefing",
    origens,
    format_func=lambda item: item["rotulo"],
)
campanha_ref = origem["ref"]
st.success(f"Campanha: {origem['campanha']}")

try:
    catalogos = base.catalogos_inventario()
    inventarios = base.inventarios_com_papeis(campanha_ref)
except Exception as erro:
    st.error(f"Não foi possível carregar o MCP: {erro}")
    st.stop()

st.subheader("1. Selecione o recorte de mídia")
canais = [item for item in catalogos["canais"] if item.get("ativo", True)]
canais_sel = st.multiselect(
    "Canais",
    canais,
    format_func=lambda item: item["nome"],
)

ids_canais = {item["id"] for item in canais_sel}
ambientes = [
    item
    for item in catalogos["ambientes"]
    if item.get("ativo", True) and item.get("canal_id") in ids_canais
]
ambientes_sel = st.multiselect(
    "Ambientes",
    ambientes,
    format_func=lambda item: item["nome"],
    disabled=not canais_sel,
)

ids_tecnologias = {
    item.get("tecnologia_id") for item in canais_sel if item.get("tecnologia_id")
}
tecnologias = [
    item
    for item in catalogos["tecnologias"]
    if item.get("ativo", True) and item["id"] in ids_tecnologias
]
tecnologias_sel = st.multiselect(
    "Tecnologias",
    tecnologias,
    format_func=lambda item: item["nome"],
    disabled=not ambientes_sel,
)

ids_ambientes = {item["id"] for item in ambientes_sel}
ids_tecnologias_sel = {item["id"] for item in tecnologias_sel}
ids_canais_validos = {
    item["id"]
    for item in canais_sel
    if item.get("tecnologia_id") in ids_tecnologias_sel
}
ids_ambientes_validos = {
    item["id"]
    for item in ambientes_sel
    if item.get("canal_id") in ids_canais_validos
}
inventarios_filtrados = [
    item
    for item in inventarios
    if item.get("ativo", True) and item.get("ambiente_id") in ids_ambientes_validos
]

inventarios_sel = st.multiselect(
    "Inventários que participarão desta campanha",
    inventarios_filtrados,
    format_func=lambda item: item["nome"],
    disabled=not tecnologias_sel,
)

if not inventarios_sel:
    st.info(
        "Selecione Canais, Ambientes, Tecnologias e ao menos um Inventário "
        "para configurar os papéis."
    )
    st.stop()

st.subheader("2. Ajuste os critérios")
linhas = []
for inventario in inventarios_sel:
    salvo = inventario.get("classificacao") or {}
    linhas.append(
        {
            "Inventário": inventario["nome"],
            "Inventário ID": inventario["id"],
            "Afinidade": float(salvo.get("afinidade", 100)),
            "Cobertura": float(salvo.get("cobertura", 70)),
            "Consumo": float(salvo.get("consumo", 60)),
            "Adequação": float(salvo.get("adequacao_objetivo", 80)),
        }
    )

editado = st.data_editor(
    pd.DataFrame(linhas),
    hide_index=True,
    width="stretch",
    disabled=["Inventário", "Inventário ID"],
    column_config={
        "Inventário ID": None,
        "Afinidade": st.column_config.NumberColumn(min_value=0, max_value=200),
        "Cobertura": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Consumo": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Adequação": st.column_config.NumberColumn(min_value=0, max_value=100),
    },
)

scores = {}
criterios = {}
for _, linha in editado.iterrows():
    score = classificador.calcular_score(
        linha["Afinidade"],
        linha["Cobertura"],
        linha["Consumo"],
        linha["Adequação"],
    )
    rotulo = f"{linha['Inventário']} · {linha['Inventário ID'][:8]}"
    scores[rotulo] = score
    criterios[rotulo] = {**linha.to_dict(), "score": score}

ranking = classificador.classificar(scores)
st.subheader("3. Revise o ranking")
st.dataframe(ranking, hide_index=True, width="stretch")

if st.button("Aplicar papéis à campanha", type="primary", width="stretch"):
    try:
        base.desmarcar_papeis_campanha(campanha_ref)
        for item in ranking:
            criterio = criterios[item["meio"]]
            base.salvar_papel_inventario(
                {
                    "inventario_id": criterio["Inventário ID"],
                    "campanha_ref": campanha_ref,
                    "selecionado": True,
                    "afinidade": criterio["Afinidade"],
                    "cobertura": criterio["Cobertura"],
                    "consumo": criterio["Consumo"],
                    "adequacao_objetivo": criterio["Adequação"],
                    "score": criterio["score"],
                    "papel": item["papel"].upper(),
                }
            )
    except Exception as erro:
        st.error(f"Não foi possível aplicar os papéis: {erro}")
    else:
        st.session_state["mcp_inventarios"] = [
            item["id"] for item in inventarios_sel
        ]
        WorkflowService().concluir(st.session_state, "mcp_papeis", campanha_ref)
        st.success("Papéis aplicados. O Planejamento usará apenas estes inventários.")
        st.page_link(
            "pages/05_Planejamento.py",
            label="Continuar para Planejamento",
            icon="🧠",
            width="stretch",
        )
