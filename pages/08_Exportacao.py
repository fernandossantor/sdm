import io

import pandas as pd
import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.exportacao_service import (
    ExportacaoService
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


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

repo = DecisionRepository()

planejamento = PlanejamentoService()

exportacao = ExportacaoService()

briefings = repo.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

briefing = st.selectbox(

    "Briefing",

    nomes

)

if st.button(

    "Gerar Plano",

    type="primary",

    use_container_width=True

):

    plano = planejamento.gerar(

        briefing

    )

    st.session_state["plano_exportacao"] = plano


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

        use_container_width=True

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

        use_container_width=True

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

        use_container_width=True

    )