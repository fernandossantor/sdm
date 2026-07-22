import streamlit as st
from application.services.base_conhecimento_service import BaseConhecimentoService
from application.services.universe_service import UniverseService
from application.services.segment_service import SegmentService
from application.services.public_service import PublicService
from application.services.project_service import ProjectService


def render():

    def total(funcao, filtro_ativo=True):
        try:
            itens = funcao()
            return len([i for i in itens if not filtro_ativo or i.get("ativo", True)])
        except Exception:
            return "—"

    st.subheader(

        "Visão geral"

    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(

        "Inventários",

        total(BaseConhecimentoService().listar_inventarios)

    )

    c2.metric(

        "Universos",
        total(UniverseService().listar)

    )

    c3.metric(

        "Segmentos",
        total(SegmentService().listar)

    )

    c4.metric(

        "Públicos",
        total(PublicService().listar)
    )

    c5.metric("Projetos", total(ProjectService().listar, filtro_ativo=False))
