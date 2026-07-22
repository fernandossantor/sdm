import streamlit as st

from application.services.base_conhecimento_service import BaseConhecimentoService
from application.services.briefing_service import BriefingService
from application.services.context_service import ContextService
from application.services.classificacao_papeis_service import ClassificacaoPapeisService
from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir


st.set_page_config(page_title="Papéis dos Meios", page_icon="🧩", layout="wide")
exigir("mcp_papeis")
st.title("🧩 Papéis dos Meios")

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

if any(item.get("classificacao") for item in inventarios):
    st.info("Os controles abaixo carregam os papéis já salvos e permitem editá-los.")
    if st.button("Excluir papéis desta campanha", type="secondary"):
        base.excluir_papeis_campanha(campanha_ref)
        st.session_state.pop("mcp_papeis", None)
        st.rerun()

st.subheader("1. Selecione o recorte de mídia")
canais = [item for item in catalogos["canais"] if item.get("ativo", True)]
ids_inventarios_salvos = {
    item["id"] for item in inventarios if item.get("classificacao")
}
ids_ambientes_salvos = {
    item.get("ambiente_id") for item in inventarios
    if item["id"] in ids_inventarios_salvos
}
ids_canais_salvos = {
    item.get("canal_id") for item in catalogos["ambientes"]
    if item.get("id") in ids_ambientes_salvos
}
canais_sel = st.multiselect(
    "Canais",
    canais,
    default=[item for item in canais if item["id"] in ids_canais_salvos],
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
    default=[item for item in ambientes if item["id"] in ids_ambientes_salvos],
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
    default=tecnologias if ids_inventarios_salvos else [],
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
    default=[
        item for item in inventarios_filtrados if item["id"] in ids_inventarios_salvos
    ],
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
st.caption(
    "Afinidade avalia a qualificação editorial; Consumo representa o hábito "
    "de uso do público; Cobertura estima quanto desse público a mídia alcança. "
    "A adequação é calculada automaticamente a partir desses três critérios."
)
wc1, wc2, wc3, wc4 = st.columns(4)
peso_afinidade = wc1.number_input("Peso afinidade (%)", 0, 100, 30)
peso_consumo = wc2.number_input("Peso consumo (%)", 0, 100, 25)
peso_cobertura = wc3.number_input("Peso cobertura (%)", 0, 100, 25)
peso_jornada = wc4.number_input("Peso jornada (%)", 0, 100, 20)
soma_pesos = peso_afinidade + peso_consumo + peso_cobertura + peso_jornada
if soma_pesos != 100:
    st.error(f"Os pesos devem somar 100% (atual: {soma_pesos}%).")
pesos_mcp = {
    "afinidade": peso_afinidade / 100,
    "consumo": peso_consumo / 100,
    "cobertura": peso_cobertura / 100,
    "jornada": peso_jornada / 100,
}
scores = {}
criterios = {}


def intensidade_salva(valor, padrao):
    return max(0, min(100, int(float(valor or padrao) // 10 * 10)))


for inventario in inventarios_sel:
    salvo = inventario.get("classificacao") or {}
    with st.expander(inventario["nome"], expanded=True):
        afinidade = st.select_slider(
            "Afinidade editorial",
            options=list(range(0, 101, 10)),
            value=intensidade_salva(salvo.get("afinidade"), 70),
            key=f"afinidade_{inventario['id']}",
            help="Quanto a linha editorial qualifica o inventário para este público.",
        )
        consumo = st.select_slider(
            "Intensidade de consumo",
            options=list(range(0, 101, 10)),
            value=intensidade_salva(salvo.get("consumo"), 60),
            key=f"consumo_{inventario['id']}",
            help="Intensidade do hábito de consumo desse meio pelo público.",
        )
        cobertura = st.select_slider(
            "Cobertura do público",
            options=list(range(0, 101, 10)),
            value=intensidade_salva(salvo.get("cobertura"), 70),
            key=f"cobertura_{inventario['id']}",
            help="Parcela estimada do público que pode ser coberta pela mídia.",
        )
        jornada = st.select_slider(
            "Contribuição aos pontos de contato da jornada",
            options=list(range(0, 101, 10)),
            value=intensidade_salva(salvo.get("jornada"), 60),
            key=f"jornada_{inventario['id']}",
        )
        score = classificador.calcular_score(
            afinidade, cobertura, consumo, jornada=jornada, pesos=pesos_mcp
        )
        st.metric("Adequação calculada", f"{score:.0f}%")
    rotulo = f"{inventario['nome']} · {inventario['id'][:8]}"
    scores[rotulo] = score
    criterios[rotulo] = {
        "Inventário ID": inventario["id"],
        "Afinidade": afinidade,
        "Cobertura": cobertura,
        "Consumo": consumo,
        "Jornada": jornada,
        "Adequação": score,
        "score": score,
    }

ranking = classificador.classificar(scores)
st.subheader("3. Revise o ranking")
for item in ranking:
    item["papel"] = st.selectbox(
        f"{item['posicao']}º · {item['meio'].split(' · ')[0]} ({item['score']:.0f}%)",
        ["Principal", "Complementar", "Apoio", "Experimental"],
        index=["Principal", "Complementar", "Apoio", "Experimental"].index(
            item["papel"] if item["papel"] in {"Principal", "Complementar", "Apoio"} else "Experimental"
        ),
        key=f"papel_revisado_{criterios[item['meio']]['Inventário ID']}",
    )
    st.caption(
        f"{item['posicao']}º · **{item['meio'].split(' · ')[0]}** — "
        f"{item['papel']} ({item['score']:.0f}%)"
    )

if st.button("Aplicar papéis à campanha", type="primary", width="stretch", disabled=soma_pesos != 100):
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
                    "jornada": criterio["Jornada"],
                    "pesos": pesos_mcp,
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
        st.success("Papéis aplicados. O Plano de Mídia usará apenas estes inventários.")
        st.page_link(
            "pages/05_Planejamento.py",
            label="Continuar para Plano de Mídia",
            icon="🧠",
            width="stretch",
        )
