import io

import pandas as pd
import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.exportacao_service import (
    ExportacaoService
)

from application.services.context_service import (
    ContextService
)
from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir
from components.planning_selector import selecionar_planejamento
from components.formatters import moeda_ptbr
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Exportação",

    page_icon="📤",

    layout="wide"

)

exigir("exportacao")

st.title("📤 Exportação")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

exportacao = ExportacaoService()

workflow_service = WorkflowService()
artefatos = WorkflowArtifactService()

origem = selecionar_planejamento(planejamento, "exportacao_planejamento")
gerenciar_artefatos(artefatos, "RELATORIO", "Relatórios")

if st.button(

    "Gerar Plano",

    type="primary",

    width="stretch"

):

    plano = origem["plano"]

    st.session_state["plano_exportacao"] = plano

    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "exportacao", True)
    artefatos.salvar_no_projeto(
        "RELATORIO",
        f"Relatório — {plano.campanha}",
        plano,
        st.session_state,
        origem["id"],
    )
    st.toast("Relatório salvo no projeto.")
    st.rerun()


# ==========================================================
# EXPORTAÇÃO
# ==========================================================

if "plano_exportacao" in st.session_state:

    plano = st.session_state["plano_exportacao"]

    st.success(

        "Plano gerado."

    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Inventários",

            len(plano.itens)

        )

        st.metric(

            "Investimento",

            moeda_ptbr(plano.verba_total)

        )

    with c2:

        st.metric(

            "Cliente",

            plano.cliente

        )

        st.metric(

            "Campanha",

            plano.campanha

        )

        st.divider()

    df = exportacao.dataframe(

        plano

    )

    st.dataframe(

        df,

        hide_index=True,

        width="stretch"

    )

    #
    # Excel
    #

    excel = io.BytesIO()

    with pd.ExcelWriter(

        excel,

        engine="openpyxl"

    ) as writer:

        for aba, tabela in exportacao.tabelas(plano).items():
            tabela.to_excel(writer, index=False, sheet_name=aba)

    excel.seek(0)

    st.download_button(

        "⬇️ Baixar Excel",

        data=excel.getvalue(),

        file_name=f"{plano.campanha}.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        width="stretch"

    )

    #
    # CSV
    #

    csv = df.to_csv(

        index=False,

        encoding="utf-8-sig"

    ).encode(

        "utf-8-sig"

    )

    st.download_button(

        "⬇️ Baixar CSV",

        data=csv,

        file_name=f"{plano.campanha}.csv",

        mime="text/csv",

        width="stretch"

    )
