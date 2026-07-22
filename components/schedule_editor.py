import pandas as pd
import streamlit as st


def render(plano, key="cronograma_semanal"):
    if not plano.cronograma:
        st.info("Defina as datas do briefing para gerar o cronograma semanal.")
        return False

    cronograma = pd.DataFrame(plano.cronograma)
    colunas_fixas = ["Inventário", "Unidade", "Total"]
    colunas_semana = [
        coluna for coluna in cronograma.columns if coluna not in colunas_fixas
    ]
    st.caption(
        "A distribuição inicial segue o flight. Edite as quantidades semanais "
        "e aplique para incorporar o ajuste ao plano."
    )
    editado = st.data_editor(
        cronograma,
        hide_index=True,
        width="stretch",
        disabled=colunas_fixas,
        column_config={
            coluna: st.column_config.NumberColumn(
                coluna, min_value=0.0, format="%.2f"
            )
            for coluna in colunas_semana
        },
        key=f"{key}_editor",
    )
    if not st.button(
        "Aplicar cronograma ao plano", type="primary", key=f"{key}_aplicar"
    ):
        return False

    for indice in editado.index:
        editado.at[indice, "Total"] = round(
            sum(
                float(editado.at[indice, coluna] or 0)
                for coluna in colunas_semana
            ),
            2,
        )
    plano.cronograma = editado.to_dict("records")
    return True
