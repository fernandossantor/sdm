import streamlit as st

from application.services.project_service import ProjectService
from application.services.identifier_service import IdentifierService


ROTAS = {
    "briefing": "pages/00_Briefing.py",
    "mcp_papeis": "pages/03_MCP_Papeis.py",
    "planejamento": "pages/05_Planejamento.py",
    "diagnostico": "pages/09_Diagnostico.py",
    "forecast": "pages/06_Forecast.py",
    "dashboard": "pages/07_Dashboard.py",
    "exportacao": "pages/08_Exportacao.py",
}


def render():
    service = ProjectService()
    st.subheader("Projetos")

    with st.form("novo_projeto", clear_on_submit=True):
        nome = st.text_input("Nome do novo projeto")
        criar = st.form_submit_button("Criar projeto", type="primary", width="stretch")
    if criar:
        try:
            service.criar(nome, st.session_state)
        except Exception as erro:
            st.error(str(erro))
        else:
            st.switch_page("pages/00_Briefing.py")

    projetos = service.listar()
    if not projetos:
        st.info("Nenhum projeto iniciado.")
        return

    for projeto in reversed(projetos):
        progresso = projeto.get("progresso") or {}
        concluidas = sum(bool(valor) for valor in progresso.values())
        etapa = projeto.get("etapa_atual") or "briefing"
        with st.container(border=True):
            c_nome, c_status = st.columns([3, 1])
            c_nome.markdown(f"**{IdentifierService.rotulo(projeto)}**")
            c_status.caption(f"{concluidas}/7 etapas")
            st.progress(min(concluidas / 7, 1.0))
            a, copia, b = st.columns([3, 1, 1])
            if a.button("Retomar", key=f"retomar_{projeto['id']}", width="stretch"):
                service.selecionar(projeto, st.session_state)
                if projeto.get("briefing_id"):
                    from application.services.briefing_service import BriefingService
                    briefing_service = BriefingService()
                    registros = briefing_service.listar()
                    registro = next(
                        (item for item in registros if item["id"] == projeto["briefing_id"]),
                        None,
                    )
                    if registro:
                        briefing_service.carregar(registro, st.session_state)
                st.switch_page(ROTAS.get(etapa, "pages/00_Briefing.py"))
            if copia.button("Duplicar", key=f"duplicar_projeto_{projeto['id']}"):
                service.duplicar(projeto["id"], st.session_state)
                st.rerun()
            if b.button("Excluir", key=f"excluir_projeto_{projeto['id']}"):
                service.excluir(projeto["id"])
                st.rerun()
