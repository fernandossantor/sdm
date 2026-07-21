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


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Exportação",

    page_icon="📤",

    layout="wide"

)

st.title("📤 Exportação")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

exportacao = ExportacaoService()

workflow_service = WorkflowService()

briefings = contexto_service.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

briefing = st.selectbox(

    "Briefing",

    nomes

)

usar_plano_atual = "plano" in st.session_state and st.checkbox(
    "Usar o planejamento atual da sessão",
    value=True,
)

if st.button(

    "Gerar Plano",

    type="primary",

    width="stretch"

):

    plano = (
        st.session_state["plano"]
        if usar_plano_atual
        else planejamento.gerar(nome_briefing=briefing)
    )

    st.session_state["plano_exportacao"] = plano

    workflow_service.registrar_briefing(st.session_state, briefing)
    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "exportacao", True)


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

            f"R$ {plano.verba_total:,.2f}"

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

        df.to_excel(

            writer,

            index=False,

            sheet_name="Plano"

        )

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
