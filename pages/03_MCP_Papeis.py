import streamlit as st

from application.services.base_conhecimento_service import BaseConhecimentoService
from application.services.classificacao_papeis_service import ClassificacaoPapeisService


st.set_page_config(page_title="MCP — Papéis de mídia", page_icon="🧩", layout="wide")
st.title("🧩 MCP — Papéis de mídia")
st.write(
    "Classifique os inventários reais. O score e o papel salvos aqui passam a "
    "compor o ranking e a distribuição de verba do Planejamento."
)

base = BaseConhecimentoService()
classificador = ClassificacaoPapeisService()

try:
    inventarios = base.inventarios_com_papeis()
except Exception as erro:
    st.error(f"Não foi possível carregar a classificação dos inventários: {erro}")
    st.stop()

if not inventarios:
    st.warning("Cadastre pelo menos um Inventário antes de classificar papéis.")
    st.page_link("pages/04_Inventarios.py", label="Ir para Inventários", icon="📦")
    st.stop()

st.info(
    "Afinidade aceita índice até 200. Cobertura, consumo e adequação variam de 0 a 100."
)

criterios = {}
for inventario in inventarios:
    salvo = inventario.get("classificacao") or {}
    inventario_id = inventario["id"]
    with st.expander(inventario["nome"], expanded=len(inventarios) <= 4):
        c1, c2 = st.columns(2)
        with c1:
            afinidade = st.slider(
                "Afinidade", 0, 200, int(float(salvo.get("afinidade", 100))),
                key=f"mcp_afinidade_{inventario_id}",
            )
            cobertura = st.slider(
                "Cobertura", 0, 100, int(float(salvo.get("cobertura", 70))),
                key=f"mcp_cobertura_{inventario_id}",
            )
        with c2:
            consumo = st.slider(
                "Consumo", 0, 100, int(float(salvo.get("consumo", 60))),
                key=f"mcp_consumo_{inventario_id}",
            )
            adequacao = st.slider(
                "Adequação ao objetivo", 0, 100,
                int(float(salvo.get("adequacao_objetivo", 80))),
                key=f"mcp_objetivo_{inventario_id}",
            )

        score = classificador.calcular_score(
            afinidade, cobertura, consumo, adequacao
        )
        st.metric("Score MCP", score)
        criterios[inventario_id] = {
            "inventario_id": inventario_id,
            "nome": inventario["nome"],
            "rotulo": f"{inventario['nome']} · {inventario_id[:8]}",
            "afinidade": afinidade,
            "cobertura": cobertura,
            "consumo": consumo,
            "adequacao_objetivo": adequacao,
            "score": score,
        }

ranking = classificador.classificar(
    {item["rotulo"]: item["score"] for item in criterios.values()}
)
por_rotulo = {item["rotulo"]: item for item in criterios.values()}

st.subheader("Ranking estratégico")
st.dataframe(ranking, hide_index=True, width="stretch")

if st.button("Salvar e integrar ao Planejamento", type="primary", width="stretch"):
    try:
        for item in ranking:
            criterio = por_rotulo[item["meio"]]
            base.salvar_papel_inventario(
                {
                    "inventario_id": criterio["inventario_id"],
                    "afinidade": criterio["afinidade"],
                    "cobertura": criterio["cobertura"],
                    "consumo": criterio["consumo"],
                    "adequacao_objetivo": criterio["adequacao_objetivo"],
                    "score": criterio["score"],
                    "papel": item["papel"].upper(),
                }
            )
    except Exception as erro:
        st.error(f"Não foi possível salvar os papéis: {erro}")
    else:
        st.success("Papéis salvos e integrados. Gere novamente o Planejamento.")
        st.page_link(
            "pages/05_Planejamento.py",
            label="Gerar Planejamento com estes papéis",
            icon="🧠",
        )
